// auto_validate_with_original.js
// 새로 업로드된 데이터를 원본 파일과 자동 대조 및 검증

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

function findOriginalFile(problemIdPattern) {
	const downloadsPath = path.join(os.homedir(), 'Downloads');
	
	if (!fs.existsSync(downloadsPath)) {
		return null;
	}
	
	const files = fs.readdirSync(downloadsPath);
	
	// 문제ID 패턴에서 정보 추출 (예: 미적분_2025학년도_현우진_드릴_P3)
	const parts = problemIdPattern.split('_');
	const subject = parts[0]; // 미적분
	const year = parts[1]; // 2025학년도
	const part = parts[parts.length - 1]; // P3
	
	// 파일 찾기
	const targetFiles = files.filter(f => {
		if (!f.endsWith('.csv')) return false;
		return f.includes(subject) && 
		       (f.includes(year) || f.includes('2025')) &&
		       (f.includes(part) || f.includes(part.replace('P', 'p')));
	});
	
	if (targetFiles.length === 0) {
		// 더 넓게 검색
		const recentFiles = files
			.filter(f => f.endsWith('.csv') && f.includes(subject))
			.map(f => {
				const filePath = path.join(downloadsPath, f);
				const stats = fs.statSync(filePath);
				return { name: f, path: filePath, mtime: stats.mtime };
			})
			.sort((a, b) => b.mtime - a.mtime);
		
		if (recentFiles.length > 0) {
			return recentFiles[0].path;
		}
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

function normalizeForComparison(text) {
	if (!text) return '';
	// Python 딕셔너리와 JSON을 비교 가능하도록 정규화
	return text.trim()
		.replace(/'/g, '"')
		.replace(/\\/g, '')
		.toLowerCase();
}

function checkJSON(text) {
	if (!text || text.trim() === '' || text.trim() === '{}') {
		return { valid: false, error: '빈 필드 또는 빈 객체' };
	}
	try {
		JSON.parse(text);
		return { valid: true, error: null };
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

async function autoValidateWithOriginal() {
	console.log('='.repeat(70));
	console.log('[원본 파일과 자동 대조 및 검증]');
	console.log('='.repeat(70));
	
	// 최근 업로드된 항목 찾기 (문제ID 패턴으로)
	console.log('\n[1단계] 최근 업로드된 항목 찾기...\n');
	
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
	
	// 문제ID로 그룹화하여 최근 업로드된 그룹 찾기
	const problemGroups = {};
	allPages.forEach(page => {
		const problemId = getPropertyValue(page.properties['문제ID']);
		if (problemId) {
			const pattern = problemId.split('_').slice(0, -1).join('_'); // 마지막 번호 제외
			if (!problemGroups[pattern]) {
				problemGroups[pattern] = [];
			}
			problemGroups[pattern].push(page);
		}
	});
	
	// 가장 최근 그룹 선택 (또는 사용자가 지정한 패턴)
	const recentPattern = Object.keys(problemGroups).sort().pop();
	const recentItems = problemGroups[recentPattern] || [];
	
	if (recentItems.length === 0) {
		console.log('⚠️  최근 업로드된 항목을 찾을 수 없습니다.');
		return;
	}
	
	console.log(`✅ 최근 업로드된 항목: ${recentItems.length}개 (패턴: ${recentPattern})\n`);
	
	// 원본 파일 찾기
	console.log('[2단계] 원본 파일 찾기...\n');
	const originalPath = findOriginalFile(recentPattern);
	
	if (!originalPath) {
		console.log('⚠️  원본 파일을 찾을 수 없습니다.');
		console.log('다운로드 폴더에서 수동으로 확인해주세요.\n');
	} else {
		console.log(`✅ 원본 파일 발견: ${path.basename(originalPath)}\n`);
	}
	
	// 검증
	console.log('[3단계] 검증 중...\n');
	
	const results = {
		JSON오류: [],
		LaTeX오류: [],
		원본불일치: [],
		정상: []
	};
	
	let originalData = null;
	let originalMap = {};
	
	if (originalPath) {
		originalData = readCSV(originalPath);
		originalData.forEach(row => {
			const problemId = row['문제ID'] || row['문제 ID'] || '';
			if (problemId) {
				originalMap[problemId] = row;
			}
		});
		console.log(`원본 파일: ${originalData.length}개 행\n`);
	}
	
	for (const page of recentItems) {
		const props = page.properties;
		const problemId = getPropertyValue(props['문제ID']);
		const variation = getPropertyValue(props['변형요소']);
		const latex = getPropertyValue(props['LaTeX예시']);
		
		// JSON 검사
		const jsonCheck = checkJSON(variation);
		if (!jsonCheck.valid) {
			results.JSON오류.push({
				문제ID: problemId,
				이유: jsonCheck.error
			});
			continue;
		}
		
		// LaTeX 검사
		const latexCheck = checkLaTeX(latex);
		if (!latexCheck.valid) {
			results.LaTeX오류.push({
				문제ID: problemId,
				이유: latexCheck.error
			});
			continue;
		}
		
		// 원본과 대조
		if (originalMap[problemId]) {
			const originalVariation = originalMap[problemId]['변형요소'] || originalMap[problemId]['변형 요소'] || '';
			const normalizedOriginal = normalizeForComparison(originalVariation);
			const normalizedNotion = normalizeForComparison(variation);
			
			if (normalizedOriginal !== normalizedNotion && normalizedOriginal !== '') {
				results.원본불일치.push({
					문제ID: problemId,
					원본: originalVariation.substring(0, 50),
					Notion: variation.substring(0, 50)
				});
			} else {
				results.정상.push(problemId);
			}
		} else {
			results.정상.push(problemId);
		}
	}
	
	// 결과 출력
	console.log('='.repeat(70));
	console.log('[검증 결과]');
	console.log('='.repeat(70));
	
	const totalErrors = results.JSON오류.length + results.LaTeX오류.length + results.원본불일치.length;
	
	if (totalErrors === 0) {
		console.log(`\n✅ 모든 데이터가 정상입니다!`);
		console.log(`   정상: ${results.정상.length}개\n`);
	} else {
		console.log(`\n⚠️  총 ${totalErrors}개의 이슈 발견\n`);
		
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
		
		if (results.원본불일치.length > 0) {
			console.log(`[원본 불일치] ${results.원본불일치.length}개`);
			results.원본불일치.forEach(item => {
				console.log(`  ${item.문제ID}:`);
				console.log(`    원본: ${item.원본}...`);
				console.log(`    Notion: ${item.Notion}...`);
			});
			console.log();
		}
		
		console.log(`정상: ${results.정상.length}개`);
	}
	
	console.log('='.repeat(70));
}

autoValidateWithOriginal();
