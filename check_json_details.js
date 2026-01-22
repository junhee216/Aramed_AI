// check_json_details.js
// JSON 오류 상세 확인

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

async function checkJSONDetails() {
	console.log('='.repeat(70));
	console.log('[JSON 오류 상세 확인]');
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
	
	for (let i = 0; i < items.length; i++) {
		const page = items[i];
		const props = page.properties;
		const problemId = getPropertyValue(props['문제ID']);
		const variation = getPropertyValue(props['변형요소']);
		
		console.log(`[${i + 1}] ${problemId}`);
		console.log('-'.repeat(70));
		console.log(`변형요소 원본: ${variation.substring(0, 100)}${variation.length > 100 ? '...' : ''}`);
		console.log(`길이: ${variation.length}자`);
		
		// JSON 파싱 시도
		try {
			const parsed = JSON.parse(variation);
			console.log('✅ JSON 파싱 성공');
			console.log(`키 개수: ${Object.keys(parsed).length}`);
		} catch (e) {
			console.log(`❌ JSON 파싱 실패: ${e.message}`);
			
			// 빈 객체인지 확인
			if (variation.trim() === '{}' || variation.trim() === '') {
				console.log('  → 빈 객체 또는 빈 문자열');
			} else {
				console.log('  → 형식 오류 가능성');
			}
		}
		console.log();
	}
}

checkJSONDetails();
