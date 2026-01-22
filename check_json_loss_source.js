// check_json_loss_source.js
// JSON 손실이 발생한 원인과 위치 확인

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
		case 'date':
			return prop.date ? prop.date.start : '';
		default:
			return '';
	}
}

async function checkLossSource() {
	console.log('='.repeat(60));
	console.log('[JSON 손실 원인 확인]');
	console.log('='.repeat(60));
	
	console.log('\n[손실 발생 원인]');
	console.log('='.repeat(60));
	console.log('1. 실행된 스크립트: fix_notion_errors.js');
	console.log('2. 실행 시점: 첫 번째 수정 시도 시');
	console.log('3. 문제가 된 로직:');
	console.log('   - MATLAB 스타일 데이터를 JSON으로 변환 실패');
	console.log('   - 변환 실패 시 빈 객체 {}로 대체');
	console.log('   - 원본 데이터가 손실됨\n');
	
	console.log('[손실된 데이터 형식]');
	console.log('='.repeat(60));
	console.log('원본 형식 (MATLAB 스타일):');
	console.log("  {'항수':[5;10;20]; '첫째항':[1;2;3;5]; '공차':[1;2;3]}");
	console.log("  {'각도':[30;45;60;90;120;150;180]}");
	console.log("  {'밑':[2;3;5]; '진수밑':[2;4;8]; '지수':[2;3;4]}");
	console.log('\n변환 후 (잘못된 처리):');
	console.log('  {}  ← 빈 객체로 변경됨\n');
	
	console.log('[복구 가능한 방법]');
	console.log('='.repeat(60));
	console.log('1. Notion 페이지 히스토리 확인');
	console.log('   - 각 페이지의 우측 상단 "..." 메뉴');
	console.log('   - "History" 또는 "히스토리" 클릭');
	console.log('   - 수정 전 버전으로 되돌리기 가능\n');
	
	console.log('2. Notion API를 통한 페이지 히스토리 조회');
	console.log('   - pages.retrieve()로 최근 수정 정보 확인');
	console.log('   - 하지만 이전 버전 내용은 직접 조회 불가\n');
	
	console.log('3. CSV 백업 파일 확인');
	console.log('   - 업로드 전 CSV 파일이 있다면 사용 가능\n');
	
	console.log('[현재 상태 확인]');
	console.log('='.repeat(60));
	
	try {
		// 빈 객체인 항목들의 최근 수정 정보 확인
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
		
		const emptyJsonItems = [];
		
		for (let i = 0; i < allPages.length; i++) {
			const page = allPages[i];
			const props = page.properties;
			const problemId = getPropertyValue(props['문제ID'] || Object.values(props)[0]);
			const variationField = props['변형요소'];
			
			if (variationField) {
				const variationText = getPropertyValue(variationField);
				if (variationText === '{}') {
					// 페이지의 최근 수정 정보
					const lastEditedTime = page.last_edited_time;
					emptyJsonItems.push({
						row: i + 2,
						problemId,
						pageId: page.id,
						lastEdited: lastEditedTime
					});
				}
			}
		}
		
		console.log(`총 ${emptyJsonItems.length}개 항목이 빈 객체 {}로 되어 있습니다.\n`);
		
		if (emptyJsonItems.length > 0) {
			console.log('[빈 객체 항목 목록 (처음 20개)]:');
			console.log('Notion에서 다음 페이지들을 확인하세요:\n');
			
			emptyJsonItems.slice(0, 20).forEach(item => {
				const notionUrl = `https://www.notion.so/${item.pageId.replace(/-/g, '')}`;
				console.log(`  행 ${item.row}: ${item.problemId}`);
				console.log(`    페이지 ID: ${item.pageId}`);
				console.log(`    URL: ${notionUrl}`);
				console.log(`    최근 수정: ${item.lastEdited}`);
				console.log(`    → 우측 상단 "..." → "History"에서 이전 버전 확인 가능`);
				console.log();
			});
			
			if (emptyJsonItems.length > 20) {
				console.log(`  ... 외 ${emptyJsonItems.length - 20}개 항목\n`);
			}
		}
		
		// 수정 시간 분석
		if (emptyJsonItems.length > 0) {
			const editTimes = emptyJsonItems.map(item => new Date(item.lastEdited));
			const earliestEdit = new Date(Math.min(...editTimes.map(d => d.getTime())));
			const latestEdit = new Date(Math.max(...editTimes.map(d => d.getTime())));
			
			console.log('[수정 시간 분석]');
			console.log(`  가장 이른 수정: ${earliestEdit.toLocaleString('ko-KR')}`);
			console.log(`  가장 늦은 수정: ${latestEdit.toLocaleString('ko-KR')}`);
			console.log(`  → 이 시간대에 fix_notion_errors.js가 실행되었을 가능성이 높습니다.\n`);
		}
		
		console.log('='.repeat(60));
		console.log('[복구 방법 안내]');
		console.log('='.repeat(60));
		console.log('1. Notion 웹/앱에서 각 페이지 열기');
		console.log('2. 우측 상단 "..." 메뉴 클릭');
		console.log('3. "History" 또는 "히스토리" 선택');
		console.log('4. 수정 전 버전으로 되돌리기');
		console.log('5. 또는 이전 버전의 내용을 복사하여 현재 버전에 붙여넣기\n');
		
		console.log('또는 CSV 백업 파일이 있다면:');
		console.log('1. CSV 파일에서 변형요소 필드 확인');
		console.log('2. 올바른 JSON 형식으로 변환');
		console.log('3. Notion에 다시 업로드\n');
		
	} catch (error) {
		console.error('\n❌ 오류:', error.message);
		process.exit(1);
	}
}

checkLossSource();
