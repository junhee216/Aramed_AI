// fix_complex_json.js
// 복잡한 JSON 구조 (중첩 배열, 구간 표기) 정확히 수정

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
		default:
			return '';
	}
}

// 복잡한 JSON 구조를 정확히 변환
function fixComplexJSON(problemId, originalText) {
	// 원본 데이터 기반 정확한 JSON 생성
	const fixes = {
		'수2_2025학년도_현우진_드릴_P7_01': {
			original: "{'interval': [[-1, 5], [0, 6]], 'value_g': [216, 54, 108], 'point_symmetry': [true, false]}",
			fixed: '{"interval": [[-1, 5], [0, 6]], "value_g": [216, 54, 108], "point_symmetry": [true, false]}'
		},
		'수2_2025학년도_현우진_드릴_P7_05': {
			original: "{'v1': ['3t^2-12t+9'], 'v2_type': ['constant', 'linear'], 'meet_times': [[2, 4], [1, 3]]}",
			fixed: '{"v1": ["3t^2-12t+9"], "v2_type": ["constant", "linear"], "meet_times": [[2, 4], [1, 3]]}'
		},
		'수2_2025학년도_현우진_드릴_P2_09': {
			original: "{'함수':['다항';'이차';'삼차']; '구간':['[0,2]';'[1,3]']; '계산':['직접대입']}",
			fixed: '{"함수": ["다항", "이차", "삼차"], "구간": ["[0,2]", "[1,3]"], "계산": ["직접대입"]}'
		},
		'수2_2025학년도_현우진_드릴_P7_03': {
			original: "{'range_g': ['(0, a]', '[0, a)'], 'int_val': [1, 2], 'f_root': [-2, 0]}",
			fixed: '{"range_g": ["(0, a]", "[0, a)"], "int_val": [1, 2], "f_root": [-2, 0]}'
		}
	};
	
	if (fixes[problemId]) {
		return fixes[problemId].fixed;
	}
	
	return null;
}

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

async function fixComplexErrors() {
	console.log('='.repeat(60));
	console.log('[복잡한 JSON 구조 수정]');
	console.log('='.repeat(60));
	
	try {
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
		
		const targetProblemIds = [
			'수2_2025학년도_현우진_드릴_P7_01',
			'수2_2025학년도_현우진_드릴_P7_05',
			'수2_2025학년도_현우진_드릴_P2_09',
			'수2_2025학년도_현우진_드릴_P7_03'
		];
		
		let fixed = 0;
		
		for (const page of allPages) {
			const props = page.properties;
			const problemId = getPropertyValue(props['문제ID'] || Object.values(props)[0]);
			
			if (targetProblemIds.includes(problemId)) {
				const jsonValue = fixComplexJSON(problemId);
				if (jsonValue) {
					const success = await updatePage(page.id, jsonValue);
					if (success) {
						fixed++;
						console.log(`  [수정] ${problemId}`);
						console.log(`    → ${jsonValue}`);
					}
				}
			}
		}
		
		console.log('\n' + '='.repeat(60));
		console.log(`[수정 완료] ${fixed}개 항목 수정`);
		console.log('='.repeat(60));
		
	} catch (error) {
		console.error('\n❌ 오류:', error.message);
		process.exit(1);
	}
}

fixComplexErrors();
