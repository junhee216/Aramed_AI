// fix_remaining_json_errors.js
// 남은 5개 JSON 오류 수정

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

// 개선된 JSON 변환 함수
function fixJSON(text) {
	if (!text || text.trim() === '' || text.trim() === '{}') {
		return null;
	}
	
	let result = text.trim();
	
	// 큰따옴표로 감싸진 경우 제거
	if ((result.startsWith('"') && result.endsWith('"')) ||
	    (result.startsWith("'") && result.endsWith("'"))) {
		result = result.slice(1, -1);
	}
	
	// 이미 올바른 JSON인 경우
	try {
		const parsed = JSON.parse(result);
		return JSON.stringify(parsed);
	} catch (e) {
		// 변환 필요
	}
	
	// MATLAB 스타일 변환
	// 1. 작은따옴표 키를 큰따옴표로
	result = result.replace(/'([^']+)'\s*:/g, '"$1":');
	
	// 2. 세미콜론을 쉼표로 (키 구분자)
	result = result.replace(/;\s*(?=")/g, ', ');
	
	// 3. 배열 내부 처리 (중첩 배열 포함)
	// 먼저 외부 배열 처리
	result = result.replace(/\[([^\]]+)\]/g, (match, content) => {
		// 세미콜론을 쉼표로
		let arrContent = content.replace(/;/g, ',');
		
		// 중첩 배열 처리
		if (arrContent.includes('[')) {
			// 중첩 배열이 있는 경우
			arrContent = arrContent.replace(/\[([^\]]+)\]/g, (innerMatch, innerContent) => {
				const innerItems = innerContent.split(',').map(item => {
					item = item.trim();
					if (/^-?\d+(\.\d+)?$/.test(item)) return item;
					return '"' + item.replace(/"/g, '\\"') + '"';
				});
				return '[' + innerItems.join(', ') + ']';
			});
		}
		
		// 각 항목 처리
		const items = arrContent.split(',').map(item => {
			item = item.trim();
			
			// 이미 배열인 경우
			if (item.startsWith('[') && item.endsWith(']')) {
				return item;
			}
			
			// 이미 따옴표로 감싸진 문자열
			if ((item.startsWith('"') && item.endsWith('"')) || 
			    (item.startsWith("'") && item.endsWith("'"))) {
				return item.replace(/'/g, '"');
			}
			
			// boolean 값
			if (item === 'true' || item === 'false') {
				return item;
			}
			
			// 숫자
			if (/^-?\d+(\.\d+)?$/.test(item)) {
				return item;
			}
			
			// 특수 문자 포함
			if (item.includes('\\') || item.includes('√') || item.includes('^') || 
			    item.includes('_') || item.includes('/') || item.includes('frac')) {
				return '"' + item.replace(/"/g, '\\"') + '"';
			}
			
			// 일반 문자열
			return '"' + item.replace(/"/g, '\\"') + '"';
		});
		
		return '[' + items.join(', ') + ']';
	});
	
	// 4. 문자열 값 처리 (배열이 아닌 단일 값)
	result = result.replace(/:\s*'([^']+)'/g, (match, value) => {
		if (/^-?\d+(\.\d+)?$/.test(value)) {
			return ': ' + value;
		}
		if (value === 'true' || value === 'false') {
			return ': ' + value;
		}
		return ': "' + value.replace(/"/g, '\\"') + '"';
	});
	
	// 최종 검증
	try {
		const parsed = JSON.parse(result);
		return JSON.stringify(parsed);
	} catch (e) {
		// 변환 실패 시 원본 반환 시도
		return result;
	}
}

// 특정 문제ID에 대한 원본 데이터 매핑
const specificFixes = {
	'수2_2025학년도_현우진_드릴_P7_01': "{'interval': [[-1, 5], [0, 6]], 'value_g': [216, 54, 108], 'point_symmetry': [true, false]}",
	'수2_2025학년도_현우진_드릴_P7_05': "{'v1': ['3t^2-12t+9'], 'v2_type': ['constant', 'linear'], 'meet_times': [[2, 4], [1, 3]]}",
	'수1_2025학년도_현우진_드릴_P7_08': "{'규칙':['등차';'등비';'계차';'기타']; '첫째항':[1;2;3]; '항번호':[5;10;n]}",
	'수2_2025학년도_현우진_드릴_P2_09': "{'함수':['다항';'이차';'삼차']; '구간':['[0,2]';'[1,3]']; '계산':['직접대입']}",
	'수2_2025학년도_현우진_드릴_P7_03': "{'range_g': ['(0, a]', '[0, a)'], 'int_val': [1, 2], 'f_root': [-2, 0]}"
};

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

async function fixRemainingErrors() {
	console.log('='.repeat(60));
	console.log('[남은 5개 JSON 오류 수정]');
	console.log('='.repeat(60));
	
	try {
		// 모든 페이지 가져오기
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
			'수1_2025학년도_현우진_드릴_P7_08',
			'수2_2025학년도_현우진_드릴_P2_09',
			'수2_2025학년도_현우진_드릴_P7_03'
		];
		
		let fixed = 0;
		
		for (const page of allPages) {
			const props = page.properties;
			const problemId = getPropertyValue(props['문제ID'] || Object.values(props)[0]);
			
			if (targetProblemIds.includes(problemId)) {
				const originalData = specificFixes[problemId];
				if (originalData) {
					const jsonValue = fixJSON(originalData);
					if (jsonValue) {
						const success = await updatePage(page.id, jsonValue);
						if (success) {
							fixed++;
							console.log(`  [수정] ${problemId}`);
							console.log(`    → ${jsonValue.substring(0, 100)}...`);
						}
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

fixRemainingErrors();
