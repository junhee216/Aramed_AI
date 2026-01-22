// auto_fix_logic_issues.js
// 수학적 논리 오류 자동 수정

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

// 수학적 논리 오류 수정
function fixLogicIssue(problem) {
	const updates = {};
	let needsUpdate = false;
	
	// 1. 난이도 "최상"인데 예상시간이 10분 미만인 경우
	if (problem.난이도 === '최상') {
		const timeNum = parseInt(problem.예상시간) || 0;
		if (timeNum < 10) {
			// 예상시간을 10분 이상으로 조정
			updates['예상시간'] = { number: Math.max(10, timeNum + 2) };
			needsUpdate = true;
		}
	}
	
	// 2. 소단원은 등차수열인데 핵심개념에 언급 없는 경우
	if (problem.소단원 && problem.소단원.includes('등차수열')) {
		if (problem.핵심개념 && !problem.핵심개념.includes('등차') && !problem.핵심개념.includes('수열')) {
			// 핵심개념에 등차수열 추가
			const newConcept = problem.핵심개념 + (problem.핵심개념 ? '; ' : '') + '등차수열';
			updates['핵심개념'] = {
				rich_text: [{ text: { content: newConcept } }]
			};
			needsUpdate = true;
		}
	}
	
	// 3. 소단원은 등비수열인데 핵심개념에 언급 없는 경우
	if (problem.소단원 && problem.소단원.includes('등비수열')) {
		if (problem.핵심개념 && !problem.핵심개념.includes('등비') && !problem.핵심개념.includes('수열')) {
			const newConcept = problem.핵심개념 + (problem.핵심개념 ? '; ' : '') + '등비수열';
			updates['핵심개념'] = {
				rich_text: [{ text: { content: newConcept } }]
			};
			needsUpdate = true;
		}
	}
	
	// 4. 문제구조가 부족한 경우 (1단계만 있는 경우)
	if (problem.문제구조 && !problem.문제구조.includes('→')) {
		// 문제구조에 최소 2단계 추가
		const newStructure = problem.문제구조 + '→답구하기';
		updates['문제구조'] = {
			rich_text: [{ text: { content: newStructure } }]
		};
		needsUpdate = true;
	}
	
	return needsUpdate ? updates : null;
}

async function updatePage(pageId, updates) {
	await rateLimiter.waitIfNeeded();
	
	try {
		await notion.pages.update({
			page_id: pageId,
			properties: updates
		});
		return true;
	} catch (error) {
		console.error(`  [오류] ${error.message}`);
		return false;
	}
}

async function autoFixLogicIssues() {
	console.log('='.repeat(60));
	console.log('[수학적 논리 오류 자동 수정]');
	console.log('='.repeat(60));
	
	try {
		let allPages = [];
		let hasMore = true;
		let startCursor = null;
		
		console.log('데이터 조회 중...\n');
		
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
		console.log('수학적 논리 오류 검사 및 수정 중...\n');
		
		let fixed = 0;
		const fixedItems = [];
		
		for (let i = 0; i < allPages.length; i++) {
			const page = allPages[i];
			const props = page.properties;
			const problemId = getPropertyValue(props['문제ID'] || Object.values(props)[0]);
			
			const problem = {
				문제ID: problemId,
				대단원: getPropertyValue(props['대단원']),
				중단원: getPropertyValue(props['중단원']),
				소단원: getPropertyValue(props['소단원']),
				난이도: getPropertyValue(props['난이도']),
				핵심개념: getPropertyValue(props['핵심개념']),
				문제구조: getPropertyValue(props['문제구조']),
				예상시간: getPropertyValue(props['예상시간'])
			};
			
			const updates = fixLogicIssue(problem);
			
			if (updates) {
				const success = await updatePage(page.id, updates);
				if (success) {
					fixed++;
					const changes = Object.keys(updates).join(', ');
					fixedItems.push({ problemId, changes });
					console.log(`  [수정] ${problemId}: ${changes}`);
				}
			}
			
			if ((i + 1) % 50 === 0) {
				console.log(`  ${i + 1}/${allPages.length} 검사 완료...`);
			}
		}
		
		console.log('\n' + '='.repeat(60));
		console.log('[수정 결과]');
		console.log('='.repeat(60));
		console.log(`✅ 자동 수정 완료: ${fixed}개`);
		
		if (fixedItems.length > 0) {
			console.log('\n[수정된 항목]:');
			fixedItems.forEach(item => {
				console.log(`  ${item.problemId}: ${item.changes}`);
			});
		}
		
		console.log('\n' + '='.repeat(60));
		console.log('[완료]');
		console.log('='.repeat(60));
		
	} catch (error) {
		console.error('\n❌ 오류:', error.message);
		process.exit(1);
	}
}

autoFixLogicIssues();
