// check_specific_items.js
// 특정 항목의 상세 내용 확인

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
		case 'multi_select':
			return prop.multi_select.map(s => s.name).join(', ');
		default:
			return '';
	}
}

async function checkSpecificItems() {
	console.log('='.repeat(70));
	console.log('[문제 항목 상세 확인]');
	console.log('='.repeat(70));
	
	await rateLimiter.waitIfNeeded();
	
	const response = await notion.databases.query({
		database_id: databaseId,
		filter: {
			property: '문제ID',
			title: {
				contains: '미적분_2025학년도_현우진_드릴_P2'
			}
		},
		page_size: 100,
	});
	
	const items = response.results;
	
	console.log(`\n총 ${items.length}개 항목 발견\n`);
	
	for (let i = 0; i < items.length; i++) {
		const page = items[i];
		const props = page.properties;
		
		const problem = {
			문제ID: getPropertyValue(props['문제ID']),
			출처: getPropertyValue(props['출처']),
			대단원: getPropertyValue(props['대단원']),
			중단원: getPropertyValue(props['중단원']),
			소단원: getPropertyValue(props['소단원']),
			난이도: getPropertyValue(props['난이도']),
			핵심개념: getPropertyValue(props['핵심개념']),
			LaTeX예시: getPropertyValue(props['LaTeX예시']),
			문제구조: getPropertyValue(props['문제구조']),
			변형요소: getPropertyValue(props['변형요소']),
			예상시간: getPropertyValue(props['예상시간'])
		};
		
		console.log(`[${i + 1}] ${problem.문제ID}`);
		console.log('-'.repeat(70));
		console.log(`  대단원: ${problem.대단원}`);
		console.log(`  중단원: ${problem.중단원}`);
		console.log(`  소단원: ${problem.소단원}`);
		console.log(`  난이도: ${problem.난이도}`);
		console.log(`  예상시간: ${problem.예상시간}분`);
		console.log(`  핵심개념: ${problem.핵심개념}`);
		console.log(`  문제구조: ${problem.문제구조}`);
		
		if (problem.중단원.includes('수열')) {
			console.log(`\n  ⚠️  중단원에 "수열"이 포함되어 있습니다.`);
			console.log(`     "수열의극한"은 미적분의 시작 부분이므로 정상일 수 있습니다.`);
			console.log(`     하지만 "등차수열", "등비수열" 등은 수학I 단원입니다.`);
		}
		
		// JSON 확인
		if (problem.변형요소) {
			try {
				const parsed = JSON.parse(problem.변형요소);
				console.log(`  변형요소: ${Object.keys(parsed).length}개 키`);
			} catch (e) {
				console.log(`  ⚠️  변형요소 JSON 오류: ${e.message}`);
			}
		}
		
		// LaTeX 확인
		if (problem.LaTeX예시) {
			const dollarCount = (problem.LaTeX예시.match(/\$/g) || []).length;
			if (dollarCount % 2 !== 0) {
				console.log(`  ⚠️  LaTeX $ 기호 짝이 맞지 않음 (${dollarCount}개)`);
			} else {
				console.log(`  LaTeX: 정상 (${dollarCount / 2}개 수식)`);
			}
		}
		
		console.log();
	}
	
	console.log('='.repeat(70));
}

checkSpecificItems();
