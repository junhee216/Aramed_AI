// restore_json_from_csv.js
// 다운로드 폴더의 CSV 파일에서 원본 데이터를 읽어 Notion의 빈 JSON 필드 복구

import 'dotenv/config';
import { Client } from '@notionhq/client';
import fs from 'fs';
import csv from 'csv-parser';
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
		default:
			return '';
	}
}

// MATLAB 스타일을 JSON으로 변환 (개선 버전)
function matlabToJSON(text) {
	if (!text || text.trim() === '' || text.trim() === '{}') {
		return null;
	}
	
	let result = text.trim();
	
	// 큰따옴표로 감싸진 경우 제거 (CSV에서 온 경우)
	if ((result.startsWith('"') && result.endsWith('"')) ||
	    (result.startsWith("'") && result.endsWith("'"))) {
		result = result.slice(1, -1);
	}
	
	// 이미 올바른 JSON인 경우
	try {
		const parsed = JSON.parse(result);
		if (Object.keys(parsed).length > 0) {
			return JSON.stringify(parsed); // 정규화된 JSON 반환
		}
	} catch (e) {
		// 변환 필요
	}
	
	// MATLAB 스타일: {'키':[값]; '키2':[값2]} 또는 {'키':'값', '키2':[값2]}
	
	// 1. 작은따옴표 키를 큰따옴표로
	result = result.replace(/'([^']+)'\s*:/g, '"$1":');
	
	// 2. 세미콜론을 쉼표로 (키 구분자, 배열 내부는 제외)
	result = result.replace(/;\s*(?=")/g, ', ');
	
	// 3. 배열 내부 처리
	result = result.replace(/\[([^\]]+)\]/g, (match, content) => {
		// 세미콜론을 쉼표로
		let arrContent = content.replace(/;/g, ',');
		
		// 각 항목 처리
		const items = arrContent.split(',').map(item => {
			item = item.trim();
			
			// 이미 따옴표로 감싸진 문자열
			if ((item.startsWith('"') && item.endsWith('"')) || 
			    (item.startsWith("'") && item.endsWith("'"))) {
				return item.replace(/'/g, '"');
			}
			
			// 숫자
			if (/^-?\d+(\.\d+)?$/.test(item)) {
				return item;
			}
			
			// LaTeX 수식이나 특수 문자 포함 (√, π 등)
			if (item.includes('\\') || item.includes('frac') || item.includes('pi') || 
			    item.includes('√') || item.includes('^') || item.includes('_')) {
				return '"' + item.replace(/"/g, '\\"') + '"';
			}
			
			// 일반 문자열
			return '"' + item.replace(/"/g, '\\"') + '"';
		});
		
		return '[' + items.join(', ') + ']';
	});
	
	// 4. 문자열 값 처리 (배열이 아닌 단일 값)
	// {'mid':'4√3','const':'k^2+2k'} 같은 경우
	result = result.replace(/:\s*'([^']+)'/g, (match, value) => {
		// 숫자가 아닌 경우만 따옴표로 감싸기
		if (/^-?\d+(\.\d+)?$/.test(value)) {
			return ': ' + value;
		}
		// 특수 문자 포함 시
		if (value.includes('√') || value.includes('^') || value.includes('_') || 
		    value.includes('\\') || value.includes('/')) {
			return ': "' + value.replace(/"/g, '\\"') + '"';
		}
		return ': "' + value.replace(/"/g, '\\"') + '"';
	});
	
	// 최종 검증
	try {
		const parsed = JSON.parse(result);
		return JSON.stringify(parsed);
	} catch (e) {
		// 변환 실패 시 원본 반환 (이미 올바른 형식일 수 있음)
		return result;
	}
}

// CSV 파일 읽기
async function readCSV(csvPath) {
	return new Promise((resolve, reject) => {
		const rows = [];
		fs.createReadStream(csvPath)
			.pipe(csv())
			.on('data', (row) => {
				rows.push(row);
			})
			.on('end', () => {
				resolve(rows);
			})
			.on('error', reject);
	});
}

// 다운로드 폴더의 모든 CSV 파일 찾기
function findCSVFiles(downloadPath) {
	const files = fs.readdirSync(downloadPath);
	return files
		.filter(file => file.endsWith('.csv') && file.includes('현우진'))
		.map(file => path.join(downloadPath, file));
}

// Notion 페이지 업데이트
async function updatePage(pageId, jsonValue) {
	await rateLimiter.waitIfNeeded();
	
	try {
		await notion.pages.update({
			page_id: pageId,
			properties: {
				'변형요소': {
					rich_text: [
						{
							text: {
								content: jsonValue
							}
						}
					]
				}
			}
		});
		return true;
	} catch (error) {
		console.error(`  [오류] ${error.message}`);
		return false;
	}
}

async function restoreFromCSV() {
	console.log('='.repeat(60));
	console.log('[CSV 파일에서 원본 데이터 복구]');
	console.log('='.repeat(60));
	
	const downloadPath = 'C:\\Users\\a\\Downloads';
	
	// 1. CSV 파일 찾기
	console.log('\n[1단계] CSV 파일 찾기');
	console.log('='.repeat(60));
	
	const csvFiles = findCSVFiles(downloadPath);
	console.log(`총 ${csvFiles.length}개의 CSV 파일을 찾았습니다.\n`);
	
	// 2. 모든 CSV 파일에서 데이터 읽기
	console.log('[2단계] CSV 파일 읽기');
	console.log('='.repeat(60));
	
	const csvDataMap = new Map(); // 문제ID -> 변형요소 데이터
	
	for (const csvFile of csvFiles) {
		console.log(`  읽는 중: ${path.basename(csvFile)}`);
		try {
			const rows = await readCSV(csvFile);
			for (const row of rows) {
				const problemId = row['문제ID'];
				const variationData = row['변형요소'];
				
				if (problemId && variationData && variationData.trim() !== '') {
					// 문제ID 정규화 (형식 통일)
					const normalizedId = problemId.replace(/^수1_|^수2_|^미적분_/, '');
					csvDataMap.set(normalizedId, variationData);
					csvDataMap.set(problemId, variationData); // 원본 ID도 저장
				}
			}
		} catch (error) {
			console.error(`  [오류] ${csvFile}: ${error.message}`);
		}
	}
	
	console.log(`\n총 ${csvDataMap.size}개의 변형요소 데이터를 읽었습니다.\n`);
	
	// 3. Notion에서 빈 객체인 항목 찾기
	console.log('[3단계] Notion 데이터베이스 조회');
	console.log('='.repeat(60));
	
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
	
	console.log(`총 ${allPages.length}개 항목 조회 완료\n`);
	
	// 4. 빈 객체인 항목 복구
	console.log('[4단계] 빈 객체 복구');
	console.log('='.repeat(60));
	
	let restored = 0;
	let notFound = 0;
	const restoredItems = [];
	const notFoundItems = [];
	
	for (let i = 0; i < allPages.length; i++) {
		const page = allPages[i];
		const props = page.properties;
		const problemId = getPropertyValue(props['문제ID'] || Object.values(props)[0]);
		const variationField = props['변형요소'];
		
		if (!variationField) continue;
		
		const currentValue = getPropertyValue(variationField);
		
		// 빈 객체인 경우만 복구 시도
		if (currentValue === '{}') {
			// 문제ID로 원본 데이터 찾기
			let originalData = csvDataMap.get(problemId);
			
			// 문제ID 형식이 다를 수 있으므로 여러 패턴 시도
			if (!originalData) {
				// 수1_2025학년도_현우진_드릴_P6_01 -> 수1_현우진_P6_01
				const pattern1 = problemId.replace(/2025학년도_|2025_/g, '');
				originalData = csvDataMap.get(pattern1);
			}
			
			if (!originalData) {
				// 수1_2025학년도_현우진_드릴_P6_01 -> P6_01
				const match = problemId.match(/P\d+_\d+$/);
				if (match) {
					for (const [key, value] of csvDataMap.entries()) {
						if (key.includes(match[0])) {
							originalData = value;
							break;
						}
					}
				}
			}
			
			if (originalData) {
				// MATLAB 스타일을 JSON으로 변환
				const jsonValue = matlabToJSON(originalData);
				
				if (jsonValue) {
					const success = await updatePage(page.id, jsonValue);
					if (success) {
						restored++;
						restoredItems.push({ problemId, jsonValue: jsonValue.substring(0, 80) });
						console.log(`  [복구] ${problemId}`);
					}
				} else {
					notFound++;
					notFoundItems.push({ problemId, reason: 'JSON 변환 실패' });
				}
			} else {
				notFound++;
				notFoundItems.push({ problemId, reason: 'CSV에서 데이터 없음' });
			}
		}
		
		if ((i + 1) % 50 === 0) {
			console.log(`  ${i + 1}/${allPages.length} 검사 완료...`);
		}
	}
	
	// 결과 출력
	console.log('\n' + '='.repeat(60));
	console.log('[복구 결과]');
	console.log('='.repeat(60));
	console.log(`✅ 복구 완료: ${restored}개`);
	console.log(`⚠️  복구 불가: ${notFound}개`);
	
	if (restoredItems.length > 0) {
		console.log('\n[복구된 항목 (처음 10개)]:');
		restoredItems.slice(0, 10).forEach(item => {
			console.log(`  ${item.problemId}: ${item.jsonValue}...`);
		});
	}
	
	if (notFoundItems.length > 0 && notFoundItems.length <= 20) {
		console.log('\n[복구 불가 항목 (처음 20개)]:');
		notFoundItems.slice(0, 20).forEach(item => {
			console.log(`  ${item.problemId}: ${item.reason}`);
		});
	}
	
	console.log('\n' + '='.repeat(60));
	console.log('[완료]');
	console.log('='.repeat(60));
}

restoreFromCSV();
