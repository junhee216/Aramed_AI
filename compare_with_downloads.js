// compare_with_downloads.js
// Notion 데이터와 다운로드 폴더의 원본 CSV 파일 대조 검토

import 'dotenv/config';
import { Client } from '@notionhq/client';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

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
		
		// 헤더 파싱
		const headers = lines[0].split(',').map(h => h.trim().replace(/"/g, ''));
		
		// 데이터 파싱
		const data = [];
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

function findCSVFiles(problemId) {
	// 문제ID에서 정보 추출
	// 예: 미적분_2025학년도_현우진_드릴_P3_01
	const match = problemId.match(/(.+?)_(\d{4})학년도_현우진_드릴_(P\d+)/);
	if (!match) {
		return [];
	}
	
	const subject = match[1];
	const year = match[2];
	const part = match[3];
	
	const downloadsPath = path.join(process.env.USERPROFILE || process.env.HOME, 'Downloads');
	
	if (!fs.existsSync(downloadsPath)) {
		return [];
	}
	
	const files = fs.readdirSync(downloadsPath);
	const csvFiles = files
		.filter(f => f.endsWith('.csv'))
		.filter(f => f.includes(subject) || f.includes(year) || f.includes(part))
		.map(f => path.join(downloadsPath, f));
	
	return csvFiles;
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

async function compareWithDownloads() {
	console.log('='.repeat(70));
	console.log('[Notion 데이터와 다운로드 원본 파일 대조 검토]');
	console.log('='.repeat(70));
	
	// 1. Notion에서 새로 업로드된 항목 조회
	console.log('\n[1단계] Notion 데이터 조회 중...\n');
	
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
	
	// 미적분_2025학년도_현우진_드릴_P3 필터링
	const newItems = allPages.filter(page => {
		const props = page.properties;
		const problemId = getPropertyValue(props['문제ID'] || Object.values(props)[0]);
		return problemId && problemId.includes('미적분_2025학년도_현우진_드릴_P3');
	});
	
	if (newItems.length === 0) {
		console.log('⚠️  "미적분_2025학년도_현우진_드릴_P3"로 시작하는 항목을 찾을 수 없습니다.');
		return;
	}
	
	console.log(`✅ Notion에서 ${newItems.length}개 항목 발견\n`);
	
	// 2. 다운로드 폴더에서 원본 CSV 파일 찾기
	console.log('[2단계] 다운로드 폴더에서 원본 CSV 파일 찾기...\n');
	
	const downloadsPath = path.join(process.env.USERPROFILE || process.env.HOME, 'Downloads');
	
	if (!fs.existsSync(downloadsPath)) {
		console.log('⚠️  다운로드 폴더를 찾을 수 없습니다.');
		return;
	}
	
	const csvFiles = fs.readdirSync(downloadsPath)
		.filter(f => f.endsWith('.csv'))
		.filter(f => f.includes('미적분') && (f.includes('2025') || f.includes('P3')))
		.map(f => path.join(downloadsPath, f));
	
	if (csvFiles.length === 0) {
		console.log('⚠️  관련 CSV 파일을 찾을 수 없습니다.');
		console.log(`검색 경로: ${downloadsPath}`);
		return;
	}
	
	console.log(`✅ ${csvFiles.length}개 CSV 파일 발견:`);
	csvFiles.forEach(f => {
		console.log(`  - ${path.basename(f)}`);
	});
	console.log();
	
	// 3. CSV 파일 파싱
	console.log('[3단계] CSV 파일 파싱 중...\n');
	
	const csvData = {};
	for (const csvFile of csvFiles) {
		const data = parseCSV(csvFile);
		csvData[path.basename(csvFile)] = data;
		console.log(`  ${path.basename(csvFile)}: ${data.length}개 행`);
	}
	console.log();
	
	// 4. Notion 데이터와 CSV 데이터 대조
	console.log('[4단계] Notion 데이터와 CSV 원본 대조 중...\n');
	
	const results = {
		JSON오류: [],
		LaTeX오류: [],
		원본대조불일치: [],
		수정완료: []
	};
	
	for (let i = 0; i < newItems.length; i++) {
		const page = newItems[i];
		const props = page.properties;
		const problemId = getPropertyValue(props['문제ID']);
		
		console.log(`[${i + 1}/${newItems.length}] ${problemId} 검토 중...`);
		
		// Notion 데이터 추출
		const notionVariation = getPropertyValue(props['변형요소']);
		const notionLaTeX = getPropertyValue(props['LaTeX예시']);
		
		// CSV에서 해당 문제 찾기
		let csvVariation = null;
		for (const [filename, data] of Object.entries(csvData)) {
			const row = data.find(r => {
				const id = r['문제ID'] || r['문제 ID'] || '';
				return id.includes(problemId.split('_').pop()) || id === problemId;
			});
			
			if (row) {
				csvVariation = row['변형요소'] || row['변형 요소'] || '';
				break;
			}
		}
		
		// JSON 검사
		const jsonCheck = checkJSON(notionVariation);
		if (!jsonCheck.valid) {
			results.JSON오류.push({
				문제ID: problemId,
				Notion: notionVariation.substring(0, 50) + '...',
				오류: jsonCheck.error
			});
			
			// CSV 원본이 있으면 복구 가능
			if (csvVariation && csvVariation.trim() !== '') {
				console.log(`  → JSON 오류 발견, CSV 원본에서 복구 가능`);
			}
		}
		
		// LaTeX 검사
		const latexCheck = checkLaTeX(notionLaTeX);
		if (!latexCheck.valid) {
			results.LaTeX오류.push({
				문제ID: problemId,
				오류: latexCheck.error
			});
		}
		
		// 원본 대조
		if (csvVariation && csvVariation.trim() !== '') {
			const csvJsonCheck = checkJSON(csvVariation);
			if (csvJsonCheck.valid && !jsonCheck.valid) {
				// CSV 원본은 유효한데 Notion은 오류인 경우
				results.원본대조불일치.push({
					문제ID: problemId,
					상태: 'CSV 원본은 유효, Notion은 오류',
					CSV원본: csvVariation.substring(0, 50) + '...'
				});
			}
		}
	}
	
	// 5. 결과 출력
	console.log('\n' + '='.repeat(70));
	console.log('[대조 검토 결과]');
	console.log('='.repeat(70));
	
	const totalErrors = results.JSON오류.length + results.LaTeX오류.length;
	
	if (totalErrors === 0) {
		console.log('✅ 모든 데이터가 올바릅니다!');
	} else {
		if (results.JSON오류.length > 0) {
			console.log(`\n[JSON 오류] ${results.JSON오류.length}개`);
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
		
		if (results.원본대조불일치.length > 0) {
			console.log(`\n[원본 대조 불일치] ${results.원본대조불일치.length}개`);
			console.log('-'.repeat(70));
			results.원본대조불일치.forEach(item => {
				console.log(`  ${item.문제ID}: ${item.상태}`);
			});
		}
	}
	
	console.log('\n' + '='.repeat(70));
	console.log('[검토 완료]');
	console.log('='.repeat(70));
}

compareWithDownloads();
