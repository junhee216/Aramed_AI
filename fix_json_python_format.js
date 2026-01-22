// fix_json_python_format.js
// Python 딕셔너리 형식을 표준 JSON으로 변환

import 'dotenv/config';
import { Client } from '@notionhq/client';

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

function pythonDictToJSON(text) {
	if (!text || text.trim() === '' || text.trim() === '{}') {
		return null;
	}
	
	let result = text.trim();
	
	// 작은따옴표를 큰따옴표로 변환 (키)
	result = result.replace(/'([^']+)'\s*:/g, '"$1":');
	
	// 배열 내부의 작은따옴표 처리
	result = result.replace(/\[([^\]]+)\]/g, (match, content) => {
		// 배열 내용을 항목별로 분리 (괄호 안의 쉼표는 제외)
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
			
			// 작은따옴표로 감싸진 경우
			if (item.startsWith("'") && item.endsWith("'")) {
				const content = item.slice(1, -1);
				// 백슬래시 이스케이프 처리
				const escaped = content
					.replace(/\\/g, '\\\\')  // 백슬래시를 먼저 이스케이프
					.replace(/"/g, '\\"')    // 큰따옴표 이스케이프
					.replace(/\n/g, '\\n')    // 줄바꿈 이스케이프
					.replace(/\r/g, '\\r')  // 캐리지 리턴 이스케이프
					.replace(/\t/g, '\\t'); // 탭 이스케이프
				return '"' + escaped + '"';
			}
			
			// 숫자인 경우
			if (/^-?\d+(\.\d+)?$/.test(item)) {
				return item;
			}
			
			// 작은따옴표가 없는 경우 (이미 처리된 경우)
			if (item.startsWith('"') && item.endsWith('"')) {
				return item;
			}
			
			// 일반 문자열 (작은따옴표 없이)
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
		console.error(`변환 실패: ${e.message}`);
		console.error(`원본: ${text}`);
		console.error(`변환 후: ${result}`);
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

async function fixJSONErrors() {
	console.log('='.repeat(70));
	console.log('[Python 딕셔너리 형식 JSON 변환]');
	console.log('='.repeat(70));
	
	await rateLimiter.waitIfNeeded();
	
	const response = await notion.databases.query({
		database_id: databaseId,
		filter: {
			property: '문제ID',
			title: {
				contains: '미적분_2025학년도_현우진_드릴_P3'
			}
		},
		page_size: 100,
	});
	
	const items = response.results;
	
	console.log(`\n총 ${items.length}개 항목 발견\n`);
	
	let fixed = 0;
	const fixedItems = [];
	
	for (let i = 0; i < items.length; i++) {
		const page = items[i];
		const props = page.properties;
		const problemId = getPropertyValue(props['문제ID']);
		const variation = getPropertyValue(props['변형요소']);
		
		console.log(`[${i + 1}] ${problemId}`);
		
		// JSON 파싱 시도
		try {
			JSON.parse(variation);
			console.log('  ✅ 이미 올바른 JSON 형식');
			continue;
		} catch (e) {
			// Python 딕셔너리 형식인 경우 변환
			const converted = pythonDictToJSON(variation);
			
			if (converted) {
				// 변환된 JSON이 올바른지 확인
				try {
					JSON.parse(converted);
					
					// Notion 업데이트
					const success = await updatePage(page.id, converted);
					
					if (success) {
						fixed++;
						fixedItems.push(problemId);
						console.log(`  ✅ 변환 완료 및 업데이트`);
					} else {
						console.log(`  ❌ 업데이트 실패`);
					}
				} catch (parseError) {
					console.log(`  ❌ 변환된 JSON도 파싱 실패: ${parseError.message}`);
				}
			} else {
				console.log(`  ❌ 변환 실패`);
			}
		}
	}
	
	console.log('\n' + '='.repeat(70));
	console.log('[수정 결과]');
	console.log('='.repeat(70));
	console.log(`✅ 총 ${fixed}개 항목 수정 완료\n`);
	
	if (fixedItems.length > 0) {
		console.log('[수정된 항목]:');
		fixedItems.forEach(id => {
			console.log(`  - ${id}`);
		});
	}
	
	console.log('\n' + '='.repeat(70));
}

fixJSONErrors();
