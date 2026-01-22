// compare_with_original.js
// 다운로드 폴더의 원본 파일과 Notion 데이터 대조

import 'dotenv/config';
import { Client } from '@notionhq/client';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import os from 'os';

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

function findOriginalFile() {
	const downloadsPath = path.join(os.homedir(), 'Downloads');
	
	if (!fs.existsSync(downloadsPath)) {
		console.log(`[오류] 다운로드 폴더를 찾을 수 없습니다: ${downloadsPath}`);
		return null;
	}
	
	const files = fs.readdirSync(downloadsPath);
	
	// 미적분 P2 - 시트16 파일 찾기
	const targetFiles = files.filter(f => 
		f.endsWith('.csv') &&
		(f.includes('미적분') || f.includes('미적')) &&
		(f.includes('P2') || f.includes('p2')) &&
		(f.includes('시트16') || f.includes('시트 16'))
	);
	
	if (targetFiles.length === 0) {
		console.log('[경고] 미적분 P3 관련 CSV 파일을 찾을 수 없습니다.');
		console.log('다운로드 폴더의 모든 CSV 파일:');
		files.filter(f => f.endsWith('.csv')).slice(0, 10).forEach(f => {
			console.log(`  - ${f}`);
		});
		return null;
	}
	
	const filePath = path.join(downloadsPath, targetFiles[0]);
	console.log(`[발견] 원본 파일: ${targetFiles[0]}`);
	return filePath;
}

function readCSV(filePath) {
	try {
		// BOM 제거를 위해 먼저 읽고 처리
		let content = fs.readFileSync(filePath, 'utf-8');
		// BOM 제거
		if (content.charCodeAt(0) === 0xFEFF) {
			content = content.slice(1);
		}
		const lines = content.split('\n').filter(line => line.trim());
		
		if (lines.length < 2) {
			return [];
		}
		
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
		console.error(`[오류] CSV 파일 읽기 실패: ${error.message}`);
		return [];
	}
}

function normalizeJSON(text) {
	if (!text || text.trim() === '' || text.trim() === '{}') {
		return '';
	}
	
	// Python 딕셔너리 형식을 JSON으로 변환
	let result = text.trim();
	
	// 작은따옴표를 큰따옴표로 변환
	result = result.replace(/'([^']+)'\s*:/g, '"$1":');
	
	// 배열 내부 처리
	result = result.replace(/\[([^\]]+)\]/g, (match, content) => {
		const items = content.split(',').map(item => {
			item = item.trim();
			if (item.startsWith("'") && item.endsWith("'")) {
				const content = item.slice(1, -1);
				return '"' + content.replace(/\\/g, '\\\\').replace(/"/g, '\\"') + '"';
			}
			if (/^-?\d+(\.\d+)?$/.test(item)) {
				return item;
			}
			return '"' + item.replace(/\\/g, '\\\\').replace(/"/g, '\\"') + '"';
		});
		return '[' + items.join(', ') + ']';
	});
	
	return result;
}

async function compareWithOriginal() {
	console.log('='.repeat(70));
	console.log('[원본 파일과 Notion 데이터 대조]');
	console.log('='.repeat(70));
	
	// 원본 파일 찾기
	const originalPath = findOriginalFile();
	if (!originalPath) {
		return;
	}
	
	// 원본 파일 읽기
	console.log('\n[1단계] 원본 파일 읽기 중...\n');
	const originalData = readCSV(originalPath);
	
	if (originalData.length === 0) {
		console.log('[오류] 원본 파일에서 데이터를 읽을 수 없습니다.');
		return;
	}
	
	console.log(`✅ 원본 파일: ${originalData.length}개 행 발견\n`);
	
	// Notion 데이터 조회
	console.log('[2단계] Notion 데이터 조회 중...\n');
	
	let allPages = [];
	let hasMore = true;
	let startCursor = null;
	
	while (hasMore) {
		await rateLimiter.waitIfNeeded();
		
		const response = await notion.databases.query({
			database_id: databaseId,
			filter: {
				or: [
					{
						property: '문제ID',
						title: {
							contains: '미적분_2025학년도_현우진_드릴_P3'
						}
					},
					{
						property: '문제ID',
						title: {
							contains: '미적분_2025학년도_현우진_드릴_P2'
						}
					}
				]
			},
			page_size: 100,
		});
		
		allPages.push(...response.results);
		hasMore = response.has_more;
		startCursor = response.next_cursor;
	}
	
	console.log(`✅ Notion 데이터: ${allPages.length}개 항목 발견\n`);
	
	// 대조
	console.log('[3단계] 원본과 Notion 데이터 대조 중...\n');
	
	const comparison = {
		일치: [],
		변형요소불일치: [],
		LaTeX불일치: [],
		Notion에없음: [],
		원본에없음: []
	};
	
	// 원본 데이터를 문제ID로 인덱싱
	const originalMap = {};
	originalData.forEach(row => {
		const problemId = row['문제ID'] || row['문제 ID'] || '';
		if (problemId) {
			originalMap[problemId] = row;
		}
	});
	
	// Notion 데이터와 비교
	for (const page of allPages) {
		const props = page.properties;
		const problemId = getPropertyValue(props['문제ID']);
		
		const notionVariation = getPropertyValue(props['변형요소']);
		const notionLatex = getPropertyValue(props['LaTeX예시']);
		
		const original = originalMap[problemId];
		
		if (!original) {
			comparison.원본에없음.push(problemId);
			continue;
		}
		
		const originalVariation = original['변형요소'] || original['변형 요소'] || '';
		const originalLatex = original['LaTeX예시'] || original['LaTeX 예시'] || '';
		
		// 변형요소 비교 (정규화 후)
		const normalizedOriginal = normalizeJSON(originalVariation);
		const normalizedNotion = normalizeJSON(notionVariation);
		
		if (normalizedOriginal !== normalizedNotion && normalizedOriginal !== '') {
			comparison.변형요소불일치.push({
				문제ID: problemId,
				원본: originalVariation.substring(0, 50),
				Notion: notionVariation.substring(0, 50)
			});
		}
		
		// LaTeX 비교
		if (originalLatex !== notionLatex && originalLatex !== '') {
			comparison.LaTeX불일치.push({
				문제ID: problemId,
				원본: originalLatex.substring(0, 50),
				Notion: notionLatex.substring(0, 50)
			});
		}
		
		if (normalizedOriginal === normalizedNotion && originalLatex === notionLatex) {
			comparison.일치.push(problemId);
		}
	}
	
	// 원본에만 있는 항목
	Object.keys(originalMap).forEach(problemId => {
		if (!allPages.find(p => getPropertyValue(p.properties['문제ID']) === problemId)) {
			comparison.Notion에없음.push(problemId);
		}
	});
	
	// 결과 출력
	console.log('='.repeat(70));
	console.log('[대조 결과]');
	console.log('='.repeat(70));
	
	console.log(`\n✅ 일치: ${comparison.일치.length}개`);
	if (comparison.일치.length > 0 && comparison.일치.length <= 10) {
		comparison.일치.forEach(id => console.log(`  - ${id}`));
	}
	
	if (comparison.변형요소불일치.length > 0) {
		console.log(`\n⚠️  변형요소 불일치: ${comparison.변형요소불일치.length}개`);
		comparison.변형요소불일치.forEach(item => {
			console.log(`  ${item.문제ID}:`);
			console.log(`    원본: ${item.원본}...`);
			console.log(`    Notion: ${item.Notion}...`);
		});
	}
	
	if (comparison.LaTeX불일치.length > 0) {
		console.log(`\n⚠️  LaTeX 불일치: ${comparison.LaTeX불일치.length}개`);
		comparison.LaTeX불일치.forEach(item => {
			console.log(`  ${item.문제ID}:`);
			console.log(`    원본: ${item.원본}...`);
			console.log(`    Notion: ${item.Notion}...`);
		});
	}
	
	if (comparison.Notion에없음.length > 0) {
		console.log(`\n⚠️  원본에만 있는 항목: ${comparison.Notion에없음.length}개`);
		comparison.Notion에없음.forEach(id => console.log(`  - ${id}`));
	}
	
	if (comparison.원본에없음.length > 0) {
		console.log(`\n⚠️  Notion에만 있는 항목: ${comparison.원본에없음.length}개`);
		comparison.원본에없음.forEach(id => console.log(`  - ${id}`));
	}
	
	console.log('\n' + '='.repeat(70));
	console.log('[대조 완료]');
	console.log('='.repeat(70));
}

compareWithOriginal();
