// auto_review_with_downloads.js
// 새로 업로드된 데이터를 다운로드 폴더 원본과 대조하여 자동 검토

import 'dotenv/config';
import { Client } from '@notionhq/client';
import fs from 'fs';
import path from 'path';

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

function parseCSV(filePath) {
	try {
		let content = fs.readFileSync(filePath, 'utf8');
		// BOM 제거
		if (content.charCodeAt(0) === 0xFEFF) {
			content = content.slice(1);
		}
		
		const lines = content.split('\n').filter(line => line.trim());
		
		if (lines.length < 2) {
			return [];
		}
		
		// 헤더 파싱 (쉼표로 분리, 따옴표 처리)
		const parseCSVLine = (line) => {
			const values = [];
			let current = '';
			let inQuotes = false;
			
			for (let i = 0; i < line.length; i++) {
				const char = line[i];
				if (char === '"') {
					inQuotes = !inQuotes;
				} else if (char === ',' && !inQuotes) {
					values.push(current.trim().replace(/^"|"$/g, ''));
					current = '';
				} else {
					current += char;
				}
			}
			values.push(current.trim().replace(/^"|"$/g, ''));
			return values;
		};
		
		const headers = parseCSVLine(lines[0]);
		
		// 데이터 파싱
		const data = [];
		for (let i = 1; i < lines.length; i++) {
			const values = parseCSVLine(lines[i]);
			if (values.length === headers.length) {
				const row = {};
				headers.forEach((header, idx) => {
					row[header] = values[idx] || '';
				});
				data.push(row);
			}
		}
		
		return data;
	} catch (error) {
		console.error(`CSV 파싱 오류 (${filePath}): ${error.message}`);
		return [];
	}
}

function findCSVInDownloads(problemId) {
	// 문제ID에서 정보 추출
	// 예: 미적분_2025학년도_현우진_드릴_P3_01
	const parts = problemId.split('_');
	if (parts.length < 4) return null;
	
	const subject = parts[0];
	const year = parts[1];
	const part = parts[3] || '';
	
	const downloadsPath = path.join(process.env.USERPROFILE || process.env.HOME, 'Downloads');
	
	if (!fs.existsSync(downloadsPath)) {
		return null;
	}
	
	const files = fs.readdirSync(downloadsPath);
	const csvFiles = files
		.filter(f => f.endsWith('.csv'))
		.filter(f => {
			const lowerF = f.toLowerCase();
			return (lowerF.includes(subject.toLowerCase()) || 
			        lowerF.includes(year) || 
			        (part && lowerF.includes(part.toLowerCase())));
		})
		.map(f => path.join(downloadsPath, f));
	
	// 모든 관련 CSV 파일에서 찾기
	for (const csvFile of csvFiles) {
		const data = parseCSV(csvFile);
		const row = data.find(r => {
			const id = (r['문제ID'] || r['문제 ID'] || '').trim();
			return id === problemId || id.includes(problemId.split('_').pop());
		});
		
		if (row) {
			return { file: csvFile, row: row };
		}
	}
	
	return null;
}

function pythonDictToJSON(text) {
	if (!text || text.trim() === '' || text.trim() === '{}') {
		return null;
	}
	
	let result = text.trim();
	
	// 작은따옴표를 큰따옴표로 변환 (키)
	result = result.replace(/'([^']+)'\s*:/g, '"$1":');
	
	// 배열 내부의 작은따옴표 처리
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
	if (!text || text.trim() === '') return { valid: true, error: null, issues: [] };
	
	const issues = [];
	const dollarCount = (text.match(/\$/g) || []).length;
	
	if (dollarCount > 0 && dollarCount % 2 !== 0) {
		issues.push(`$ 기호의 짝이 맞지 않습니다 (개수: ${dollarCount}개)`);
	}
	
	if (/\$\s*\$/g.test(text)) {
		issues.push('빈 LaTeX 수식이 있습니다');
	}
	
	return { valid: issues.length === 0, error: issues.length > 0 ? issues.join('; ') : null, issues };
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

async function autoReviewWithDownloads() {
	console.log('='.repeat(70));
	console.log('[다운로드 원본과 대조 자동 검토]');
	console.log('='.repeat(70));
	console.log('이 스크립트는 Notion에 업로드된 데이터를');
	console.log('다운로드 폴더의 원본 CSV 파일과 대조하여 검토합니다.\n');
	
	// 검토할 문제ID 패턴 (기본값: 최근 업로드된 항목 자동 감지)
	// 명령줄 인자가 있으면 사용, 없으면 최근 항목 자동 감지
	let searchPattern = null;
	if (process.argv[2]) {
		searchPattern = process.argv[2];
	}
	
	console.log(`검색 모드: ${searchPattern ? `패턴 "${searchPattern}"` : '최근 업로드 자동 감지'}\n`);
	
	// 1. Notion에서 데이터 조회
	console.log('[1단계] Notion 데이터 조회 중...\n');
	
	let allPages = [];
	let hasMore = true;
	let startCursor = null;
	
	while (hasMore) {
		await rateLimiter.waitIfNeeded();
		
		const response = await notion.databases.query({
			database_id: databaseId,
			start_cursor: startCursor || undefined,
			page_size: 100,
		});
		
		allPages.push(...response.results);
		hasMore = response.has_more;
		startCursor = response.next_cursor;
	}
	
	// 필터링
	let targetItems;
	if (searchPattern) {
		targetItems = allPages.filter(page => {
			const props = page.properties;
			const problemId = getPropertyValue(props['문제ID'] || Object.values(props)[0]);
			return problemId && problemId.includes(searchPattern);
		});
	} else {
		// 최근 업로드된 항목 자동 감지 (최근 20개)
		targetItems = allPages.slice(-20);
	}
	
	if (targetItems.length === 0) {
		console.log(`⚠️  검토할 항목을 찾을 수 없습니다.`);
		return;
	}
	
	console.log(`✅ ${targetItems.length}개 항목 발견\n`);
	
	// 2. 검토 및 대조
	console.log('[2단계] 다운로드 원본과 대조 검토 중...\n');
	
	const results = {
		JSON오류: [],
		LaTeX오류: [],
		원본대조복구: [],
		수정완료: []
	};
	
	for (let i = 0; i < targetItems.length; i++) {
		const page = targetItems[i];
		const props = page.properties;
		const problemId = getPropertyValue(props['문제ID']);
		
		console.log(`[${i + 1}/${targetItems.length}] ${problemId}`);
		
		const notionVariation = getPropertyValue(props['변형요소']);
		const notionLaTeX = getPropertyValue(props['LaTeX예시']);
		
		// JSON 검사
		const jsonCheck = checkJSON(notionVariation);
		if (!jsonCheck.valid) {
			console.log(`  ⚠️  JSON 오류: ${jsonCheck.error}`);
			
			// 다운로드 폴더에서 원본 찾기
			const csvData = findCSVInDownloads(problemId);
			
			if (csvData && csvData.row) {
				const csvVariation = csvData.row['변형요소'] || csvData.row['변형 요소'] || '';
				
				if (csvVariation && csvVariation.trim() !== '') {
					console.log(`  → 원본 CSV 발견: ${path.basename(csvData.file)}`);
					
					// Python 딕셔너리 형식인 경우 변환
					const converted = pythonDictToJSON(csvVariation);
					
					if (converted) {
						// Notion 업데이트
						const success = await updatePage(page.id, converted);
						
						if (success) {
							results.원본대조복구.push(problemId);
							results.수정완료.push(problemId);
							console.log(`  ✅ 원본에서 복구 완료`);
						} else {
							console.log(`  ❌ 업데이트 실패`);
						}
					} else {
						console.log(`  ⚠️  원본도 변환 실패`);
						results.JSON오류.push({ 문제ID: problemId, 오류: jsonCheck.error });
					}
				} else {
					results.JSON오류.push({ 문제ID: problemId, 오류: jsonCheck.error });
				}
			} else {
				console.log(`  ⚠️  원본 CSV 파일을 찾을 수 없음`);
				results.JSON오류.push({ 문제ID: problemId, 오류: jsonCheck.error });
			}
		} else {
			console.log(`  ✅ JSON 정상`);
		}
		
		// LaTeX 검사
		const latexCheck = checkLaTeX(notionLaTeX);
		if (!latexCheck.valid) {
			console.log(`  ⚠️  LaTeX 오류: ${latexCheck.error}`);
			results.LaTeX오류.push({ 문제ID: problemId, 오류: latexCheck.error });
		}
	}
	
	// 3. 결과 출력
	console.log('\n' + '='.repeat(70));
	console.log('[검토 결과]');
	console.log('='.repeat(70));
	
	const totalErrors = results.JSON오류.length + results.LaTeX오류.length;
	
	if (totalErrors === 0 && results.수정완료.length === 0) {
		console.log('✅ 모든 데이터가 올바릅니다!');
	} else {
		if (results.수정완료.length > 0) {
			console.log(`\n[원본에서 복구 완료] ${results.수정완료.length}개`);
			console.log('-'.repeat(70));
			results.수정완료.forEach(id => {
				console.log(`  ✅ ${id}`);
			});
		}
		
		if (results.JSON오류.length > 0) {
			console.log(`\n[JSON 오류 (복구 불가)] ${results.JSON오류.length}개`);
			console.log('-'.repeat(70));
			results.JSON오류.forEach(err => {
				console.log(`  ${err.문제ID}: ${err.오류}`);
			});
		}
		
		if (results.LaTeX오류.length > 0) {
			console.log(`\n[LaTeX 오류] ${results.LaTeX오류.length}개`);
			console.log('-'.repeat(70));
			results.LaTeX오류.forEach(err => {
				console.log(`  ${err.문제ID}: ${err.오류}`);
			});
		}
	}
	
	console.log('\n' + '='.repeat(70));
	console.log('[검토 완료]');
	console.log('='.repeat(70));
}

// 사용법: node auto_review_with_downloads.js [검색패턴]
// 예: node auto_review_with_downloads.js "미적분_2025학년도_현우진_드릴_P3"
autoReviewWithDownloads();
