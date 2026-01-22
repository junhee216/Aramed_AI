// review_haktong_p1.js
// 확통 P1 데이터 검토 (원본 파일과 대조)

import 'dotenv/config';
import { Client } from '@notionhq/client';
import fs from 'fs';
import path from 'path';
import os from 'os';

const notionApiKey = process.env.NOTION_API_KEY;
const databaseId = process.env.NOTION_DATABASE_ID;

if (!notionApiKey || !databaseId) {
	console.error('❌ .env 설정 오류');
	process.exit(1);
}

const notion = new Client({ auth: notionApiKey });

class RateLimiter {
	constructor(maxRequestsPerSecond = 3) {
		this.maxRequests = maxRequestsPerSecond;
		this.requests = [];
	}

	async waitIfNeeded() {
		const now = Date.now();
		this.requests = this.requests.filter((time) => now - time < 1000);
		if (this.requests.length >= this.maxRequests) {
			const oldestRequest = Math.min(...this.requests);
			const waitTime = 1000 - (now - oldestRequest) + 10;
			if (waitTime > 0) {
				await new Promise((resolve) => setTimeout(resolve, waitTime));
			}
		}
		this.requests.push(Date.now());
	}
}

const rateLimiter = new RateLimiter(3);

function getPropertyValue(prop) {
	if (!prop) return '';
	
	switch (prop.type) {
		case 'title':
			return prop.title.map(t => t.plain_text).join('');
		case 'rich_text':
			return prop.rich_text.map(t => t.plain_text).join('');
		case 'number':
			return prop.number !== null ? String(prop.number) : '';
		case 'select':
			return prop.select?.name || '';
		default:
			return '';
	}
}

function findOriginalFile() {
	const downloadsPath = path.join(os.homedir(), 'Downloads');
	
	if (!fs.existsSync(downloadsPath)) {
		return null;
	}
	
	const files = fs.readdirSync(downloadsPath);
	
	// 확통 P1 관련 파일 찾기
	const targetFiles = files.filter(f => {
		if (!f.endsWith('.csv')) return false;
		return (f.includes('확통') || f.includes('확률') || f.includes('통계')) &&
		       (f.includes('P1') || f.includes('p1')) &&
		       (f.includes('2024') || f.includes('현우진'));
	});
	
	if (targetFiles.length === 0) {
		return null;
	}
	
	// 가장 최근 파일 선택
	const fileStats = targetFiles.map(f => {
		const filePath = path.join(downloadsPath, f);
		const stats = fs.statSync(filePath);
		return { name: f, path: filePath, mtime: stats.mtime };
	}).sort((a, b) => b.mtime - a.mtime);
	
	return fileStats[0].path;
}

function readCSV(filePath) {
	try {
		let content = fs.readFileSync(filePath, 'utf-8');
		if (content.charCodeAt(0) === 0xFEFF) {
			content = content.slice(1);
		}
		
		const lines = content.split('\n').filter(line => line.trim());
		if (lines.length < 2) return [];
		
		const headers = lines[0].split(',').map(h => h.trim().replace(/"/g, ''));
		const rows = [];
		
		for (let i = 1; i < lines.length; i++) {
			const values = [];
			let current = '';
			let inQuotes = false;
			
			for (let j = 0; j < lines[i].length; j++) {
				const char = lines[i][j];
				if (char === '"') {
					inQuotes = !inQuotes;
				} else if (char === ',' && !inQuotes) {
					values.push(current.trim());
					current = '';
				} else {
					current += char;
				}
			}
			values.push(current.trim());
			
			const row = {};
			headers.forEach((header, idx) => {
				row[header] = values[idx] || '';
			});
			
			if (row['문제ID'] || row['변형요소']) {
				rows.push(row);
			}
		}
		
		return rows;
	} catch (error) {
		console.error(`[오류] CSV 읽기 실패: ${error.message}`);
		return [];
	}
}

function checkJSON(text) {
	if (!text || text.trim() === '' || text.trim() === '{}') {
		return { valid: false, error: '빈 필드 또는 빈 객체' };
	}
	try {
		const parsed = JSON.parse(text);
		if (typeof parsed !== 'object' || Array.isArray(parsed)) {
			return { valid: false, error: 'JSON이 객체가 아닙니다' };
		}
		return { valid: true, error: null, parsed };
	} catch (e) {
		return { valid: false, error: e.message };
	}
}

function checkLaTeX(text) {
	if (!text || text.trim() === '') return { valid: true, error: null };
	
	const dollarCount = (text.match(/\$/g) || []).length;
	if (dollarCount > 0 && dollarCount % 2 !== 0) {
		return { valid: false, error: `$ 기호의 짝이 맞지 않습니다 (${dollarCount}개)` };
	}
	
	if (/\$\s*\$/g.test(text)) {
		return { valid: false, error: '빈 LaTeX 수식이 있습니다' };
	}
	
	return { valid: true, error: null };
}

function pythonDictToJSON(text) {
	if (!text || text.trim() === '' || text.trim() === '{}') {
		return null;
	}
	
	let result = text.trim();
	
	// 수동 파싱으로 키-값 쌍 추출 (키에 작은따옴표가 포함된 경우 처리)
	const pairs = [];
	let i = 1; // 첫 번째 '{' 건너뛰기
	let currentKey = '';
	let currentValue = '';
	let inKey = false;
	let inValue = false;
	let keyStart = -1;
	let depth = 0;
	
	while (i < result.length - 1) { // 마지막 '}' 전까지
		const char = result[i];
		
		if (char === "'" && !inValue) {
			if (!inKey) {
				// 키 시작
				inKey = true;
				keyStart = i + 1;
			} else {
				// 키 끝 확인 (다음 문자가 ':'인지 확인)
				let j = i + 1;
				while (j < result.length && (result[j] === ' ' || result[j] === '\t')) {
					j++;
				}
				if (j < result.length && result[j] === ':') {
					// 키 끝
					currentKey = result.substring(keyStart, i);
					inKey = false;
					i = j; // ':' 위치로 이동
					continue;
				}
				// 키 내부의 작은따옴표
			}
		} else if (char === ':' && !inKey && !inValue) {
			// 값 시작
			inValue = true;
			let j = i + 1;
			while (j < result.length && (result[j] === ' ' || result[j] === '\t')) {
				j++;
			}
			if (j < result.length && result[j] === '[') {
				// 배열 값
				let arrayStart = j;
				depth = 1;
				j++;
				while (j < result.length && depth > 0) {
					if (result[j] === '[') depth++;
					if (result[j] === ']') depth--;
					j++;
				}
				currentValue = result.substring(arrayStart, j);
				pairs.push({ key: currentKey, value: currentValue });
				currentKey = '';
				currentValue = '';
				inValue = false;
				i = j - 1;
				continue;
			}
		} else if (char === ',' && !inKey && depth === 0) {
			// 다음 키-값 쌍
			inValue = false;
		}
		
		i++;
	}
	
	// 수동 파싱이 실패하면 기존 방법 사용
	if (pairs.length === 0) {
		// 키에 작은따옴표가 포함된 경우를 더 정교하게 처리
		result = result.replace(/'([^']*(?:'[^':]*)*)'\s*:/g, (match, key) => {
			const escapedKey = key.replace(/\\/g, '\\\\').replace(/"/g, '\\"');
			return `"${escapedKey}":`;
		});
	} else {
		// 수동 파싱 결과로 재구성
		const jsonPairs = pairs.map(pair => {
			const key = `"${pair.key.replace(/\\/g, '\\\\').replace(/"/g, '\\"')}"`;
			// 값은 배열이므로 그대로 사용하되, 내부 작은따옴표 처리
			let value = pair.value;
			value = value.replace(/\[([^\]]+)\]/g, (match, content) => {
				const items = content.split(',').map(item => {
					item = item.trim();
					if (item.startsWith("'") && item.endsWith("'")) {
						const content = item.slice(1, -1);
						return `"${content.replace(/\\/g, '\\\\').replace(/"/g, '\\"')}"`;
					}
					if (/^-?\d+(\.\d+)?$/.test(item)) {
						return item;
					}
					return `"${item.replace(/\\/g, '\\\\').replace(/"/g, '\\"')}"`;
				});
				return '[' + items.join(', ') + ']';
			});
			return `${key}: ${value}`;
		});
		result = '{' + jsonPairs.join(', ') + '}';
	}
	
	result = result.replace(/\[([^\]]+)\]/g, (match, content) => {
		const items = [];
		let current = '';
		let depth = 0;
		
		for (let i = 0; i < content.length; i++) {
			const char = content[i];
			if (char === '(' || char === '[') {
				depth++;
				current += char;
			} else if (char === ')' || char === ']') {
				depth--;
				current += char;
			} else if (char === ',' && depth === 0) {
				items.push(current.trim());
				current = '';
			} else {
				current += char;
			}
		}
		if (current.trim()) {
			items.push(current.trim());
		}
		
		const processedItems = items.map(item => {
			item = item.trim();
			if (item.startsWith("'") && item.endsWith("'")) {
				const content = item.slice(1, -1);
				const escaped = content
					.replace(/\\/g, '\\\\')
					.replace(/"/g, '\\"')
					.replace(/\n/g, '\\n')
					.replace(/\r/g, '\\r')
					.replace(/\t/g, '\\t');
				return '"' + escaped + '"';
			}
			if (/^-?\d+(\.\d+)?$/.test(item)) {
				return item;
			}
			if (item.startsWith('"') && item.endsWith('"')) {
				return item;
			}
			const escaped = item
				.replace(/\\/g, '\\\\')
				.replace(/"/g, '\\"')
				.replace(/\n/g, '\\n')
				.replace(/\r/g, '\\r')
				.replace(/\t/g, '\\t');
			return '"' + escaped + '"';
		});
		
		return '[' + processedItems.join(', ') + ']';
	});
	
	try {
		const parsed = JSON.parse(result);
		return JSON.stringify(parsed, null, 0);
	} catch (e) {
		return null;
	}
}

async function updatePage(pageId, jsonText) {
	await rateLimiter.waitIfNeeded();
	
	try {
		await notion.pages.update({
			page_id: pageId,
			properties: {
				'변형요소': {
					rich_text: [{ text: { content: jsonText } }]
				}
			}
		});
		return true;
	} catch (error) {
		console.error(`  [오류] ${error.message}`);
		return false;
	}
}

function validateMathLogic(problem) {
	const issues = [];
	const warnings = [];
	
	// 난이도와 예상시간 일관성
	if (problem.난이도 && problem.예상시간) {
		const timeNum = parseInt(problem.예상시간) || 0;
		if (problem.난이도 === '하' && timeNum > 5) {
			warnings.push('난이도 "하"인데 예상시간이 5분 초과');
		}
		if (problem.난이도 === '중' && (timeNum < 3 || timeNum > 10)) {
			warnings.push(`난이도 "중"인데 예상시간이 ${timeNum}분`);
		}
		if (problem.난이도 === '상' && timeNum < 5) {
			warnings.push('난이도 "상"인데 예상시간이 5분 미만');
		}
		if (problem.난이도 === '최상' && timeNum < 10) {
			issues.push('난이도 "최상"인데 예상시간이 10분 미만');
		}
	}
	
	// 문제구조 논리성
	if (problem.문제구조) {
		const steps = problem.문제구조.split('→').map(s => s.trim()).filter(s => s);
		if (steps.length < 2) {
			issues.push('문제구조가 1단계만 있음 (최소 2단계 필요)');
		}
	}
	
	return { issues, warnings };
}

async function review확통P1() {
	console.log('='.repeat(70));
	console.log('[확통 P1 데이터 검토]');
	console.log('='.repeat(70));
	
	// 원본 파일 찾기
	console.log('\n[1단계] 원본 파일 찾기...\n');
	const originalPath = findOriginalFile();
	
	if (!originalPath) {
		console.log('⚠️  원본 파일을 찾을 수 없습니다.');
		console.log('다운로드 폴더에서 확인해주세요.\n');
	} else {
		console.log(`✅ 원본 파일: ${path.basename(originalPath)}\n`);
	}
	
	// 원본 파일 읽기
	let originalData = [];
	let originalMap = {};
	
	if (originalPath) {
		originalData = readCSV(originalPath);
		originalData.forEach(row => {
			const problemId = row['문제ID'] || row['문제 ID'] || '';
			if (problemId) {
				originalMap[problemId] = row;
			}
		});
		console.log(`원본 파일: ${originalData.length}개 행 발견\n`);
	}
	
	// Notion 데이터 조회
	console.log('[2단계] Notion 데이터 조회 중...\n');
	
	await rateLimiter.waitIfNeeded();
	
	const response = await notion.databases.query({
		database_id: databaseId,
		filter: {
			property: '문제ID',
			title: {
				contains: '확통_2024학년도_현우진_드릴_P1'
			}
		},
		page_size: 100,
	});
	
	const items = response.results;
	console.log(`✅ Notion 데이터: ${items.length}개 항목 발견\n`);
	
	// 검증
	console.log('[3단계] 검증 및 수정 중...\n');
	
	const results = {
		JSON오류: [],
		LaTeX오류: [],
		수학적논리오류: [],
		수정완료: [],
		정상: [],
		경고: []
	};
	
	for (let i = 0; i < items.length; i++) {
		const page = items[i];
		const props = page.properties;
		const problemId = getPropertyValue(props['문제ID']);
		const variation = getPropertyValue(props['변형요소']);
		const latex = getPropertyValue(props['LaTeX예시']);
		
		const problem = {
			난이도: getPropertyValue(props['난이도']),
			예상시간: getPropertyValue(props['예상시간']),
			문제구조: getPropertyValue(props['문제구조'])
		};
		
		console.log(`[${i + 1}/${items.length}] ${problemId}`);
		
		// JSON 검사
		const jsonCheck = checkJSON(variation);
		if (!jsonCheck.valid) {
			// Python 딕셔너리 형식인 경우 변환 시도
			const converted = pythonDictToJSON(variation);
			
			if (converted) {
				try {
					JSON.parse(converted);
					const success = await updatePage(page.id, converted);
					if (success) {
						results.수정완료.push(problemId);
						console.log('  ✅ JSON 변환 및 수정 완료');
					} else {
						results.JSON오류.push({ 문제ID: problemId, 이유: jsonCheck.error });
						console.log('  ❌ 수정 실패');
					}
				} catch (e) {
					results.JSON오류.push({ 문제ID: problemId, 이유: jsonCheck.error });
					console.log('  ❌ 변환 실패');
				}
			} else {
				results.JSON오류.push({ 문제ID: problemId, 이유: jsonCheck.error });
				console.log('  ❌ JSON 오류');
			}
		} else {
			// LaTeX 검사
			const latexCheck = checkLaTeX(latex);
			if (!latexCheck.valid) {
				results.LaTeX오류.push({ 문제ID: problemId, 이유: latexCheck.error });
				console.log(`  ⚠️  LaTeX 오류: ${latexCheck.error}`);
			} else {
				// 수학적 논리 검토
				const logicCheck = validateMathLogic(problem);
				if (logicCheck.issues.length > 0) {
					results.수학적논리오류.push({
						문제ID: problemId,
						이유: logicCheck.issues.join('; ')
					});
					console.log(`  ⚠️  수학적 논리 오류: ${logicCheck.issues.join(', ')}`);
				} else if (logicCheck.warnings.length > 0) {
					results.경고.push({
						문제ID: problemId,
						이유: logicCheck.warnings.join('; ')
					});
					console.log(`  💡 경고: ${logicCheck.warnings.join(', ')}`);
				} else {
					results.정상.push(problemId);
					console.log('  ✅ 정상');
				}
			}
		}
	}
	
	// 결과 출력
	console.log('\n' + '='.repeat(70));
	console.log('[검토 결과]');
	console.log('='.repeat(70));
	
	const totalErrors = results.JSON오류.length + results.LaTeX오류.length + results.수학적논리오류.length;
	
	if (totalErrors === 0) {
		console.log(`\n✅ 모든 데이터가 정상입니다!`);
		console.log(`   정상: ${results.정상.length}개`);
		if (results.수정완료.length > 0) {
			console.log(`   수정 완료: ${results.수정완료.length}개`);
		}
		if (results.경고.length > 0) {
			console.log(`   경고: ${results.경고.length}개`);
		}
	} else {
		console.log(`\n⚠️  총 ${totalErrors}개의 오류 발견\n`);
		
		if (results.JSON오류.length > 0) {
			console.log(`[JSON 오류] ${results.JSON오류.length}개`);
			results.JSON오류.forEach(err => {
				console.log(`  ${err.문제ID}: ${err.이유}`);
			});
			console.log();
		}
		
		if (results.LaTeX오류.length > 0) {
			console.log(`[LaTeX 오류] ${results.LaTeX오류.length}개`);
			results.LaTeX오류.forEach(err => {
				console.log(`  ${err.문제ID}: ${err.이유}`);
			});
			console.log();
		}
		
		if (results.수학적논리오류.length > 0) {
			console.log(`[수학적 논리 오류] ${results.수학적논리오류.length}개`);
			results.수학적논리오류.forEach(err => {
				console.log(`  ${err.문제ID}: ${err.이유}`);
			});
			console.log();
		}
		
		if (results.수정완료.length > 0) {
			console.log(`[수정 완료] ${results.수정완료.length}개`);
			results.수정완료.forEach(id => {
				console.log(`  ✅ ${id}`);
			});
			console.log();
		}
		
		if (results.경고.length > 0) {
			console.log(`[경고] ${results.경고.length}개`);
			results.경고.forEach(warn => {
				console.log(`  ${warn.문제ID}: ${warn.이유}`);
			});
			console.log();
		}
		
		console.log(`정상: ${results.정상.length}개`);
	}
	
	console.log('\n' + '='.repeat(70));
	console.log('[검토 완료]');
	console.log('='.repeat(70));
}

review확통P1();
