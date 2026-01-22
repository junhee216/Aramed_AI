// read_notion_database.js
// Node >= 18, ESM("type": "module") 환경 기준

import 'dotenv/config';
import { Client, collectPaginatedAPI } from '@notionhq/client';

// ✅ 1. 환경변수 읽기
const notionApiKey = process.env.NOTION_API_KEY;
const databaseId = process.env.NOTION_DATABASE_ID;

if (!notionApiKey || !databaseId) {
	console.error('❌ .env 설정 오류: NOTION_API_KEY 또는 NOTION_DATABASE_ID 가 없습니다.');
	process.exit(1);
}

// ✅ 2. Notion 클라이언트 생성
const notion = new Client({ auth: notionApiKey });

console.log('✅ ENV LOADED:', {
	keyPrefix: notionApiKey.slice(0, 8) + '...',
	databaseId,
});

// ✅ 3. 데이터베이스 메타 정보 조회
async function getDatabaseInfo() {
	const db = await notion.databases.retrieve({
		database_id: databaseId,
	});

	console.log('\n📋 데이터베이스 정보:');
	const title =
		db.title && db.title.length > 0
			? db.title.map((t) => t.plain_text).join('')
			: '(제목 없음)';

	console.log('제목:', title);
	console.log('ID:', db.id);

	return db;
}

// ✅ 4. Rate Limiting 유틸리티 (Notion API는 초당 3회 제한)
class RateLimiter {
	constructor(maxRequestsPerSecond = 3) {
		this.maxRequests = maxRequestsPerSecond;
		this.requests = [];
	}

	async waitIfNeeded() {
		const now = Date.now();
		// 1초 이상 지난 요청 제거
		this.requests = this.requests.filter((time) => now - time < 1000);

		// 초당 제한에 도달했으면 대기
		if (this.requests.length >= this.maxRequests) {
			const oldestRequest = Math.min(...this.requests);
			const waitTime = 1000 - (now - oldestRequest) + 10; // 10ms 여유
			if (waitTime > 0) {
				await new Promise((resolve) => setTimeout(resolve, waitTime));
			}
		}

		this.requests.push(Date.now());
	}
}

const rateLimiter = new RateLimiter(3);

// ✅ 5. 데이터베이스 페이지들 조회 (페이지네이션 처리)
async function readDatabase(options = {}) {
	const { 
		limit = null, // 전체 조회 시 null, 일부만 조회 시 숫자
		progressCallback = null, // 진행 상황 콜백
		filter = null,
		sorts = null
	} = options;

	console.log('\n📖 데이터베이스 조회 중...');
	console.log(limit ? `⚠️ 제한: 최대 ${limit}개까지만 조회` : '✅ 전체 조회 모드 (페이지네이션 사용)');

	const allPages = [];
	let hasMore = true;
	let startCursor = null;
	let totalFetched = 0;

	try {
		// collectPaginatedAPI를 사용하면 자동으로 모든 페이지를 가져옵니다
		// 하지만 Rate Limiting과 진행 상황 추적을 위해 수동 처리
		while (hasMore) {
			await rateLimiter.waitIfNeeded();

			const response = await notion.databases.query({
				database_id: databaseId,
				start_cursor: startCursor || undefined,
				page_size: 100, // Notion API 최대값
				filter: filter || undefined,
				sorts: sorts || undefined,
			});

			allPages.push(...response.results);
			totalFetched += response.results.length;

			// 진행 상황 콜백 호출
			if (progressCallback) {
				progressCallback({
					totalFetched,
					currentBatch: response.results.length,
					hasMore: response.has_more,
				});
			}

			hasMore = response.has_more;
			startCursor = response.next_cursor;

			// 제한이 설정된 경우 체크
			if (limit && totalFetched >= limit) {
				hasMore = false;
				allPages.splice(limit); // 초과분 제거
			}
		}

		console.log(`\n🔢 총 ${allPages.length}개 페이지를 가져왔습니다.\n`);

		// 페이지 처리
		for (const page of allPages) {
			const pageId = page.id;
			const props = page.properties;

			console.log('----------------------------------------');
			console.log('페이지 ID:', pageId);

			// 👉 title 속성 이름이 "마스터 프로토콜 v1.0" 이라고 가정
			const titleProp = props['마스터 프로토콜 v1.0'];
			let titleText = '(제목 없음)';

			if (titleProp && titleProp.type === 'title') {
				titleText =
					titleProp.title.map((t) => t.plain_text).join('') || '(제목 없음)';
			}

			console.log('제목(마스터 프로토콜 v1.0):', titleText);
		}

		console.log('\n✅ 데이터베이스 조회 완료');
		return allPages;
	} catch (err) {
		console.error('\n❌ 데이터베이스 조회 중 오류 발생:');
		console.error(err);
		throw err;
	}
}

// ✅ 6. 메인 실행 함수
async function main() {
	try {
		await getDatabaseInfo();
		
		// 진행 상황 콜백 추가
		await readDatabase({
			limit: null, // 전체 조회 (13만 개 처리 가능)
			progressCallback: ({ totalFetched, currentBatch, hasMore }) => {
				if (totalFetched % 1000 === 0 || !hasMore) {
					console.log(`📊 진행 상황: ${totalFetched}개 조회 완료${hasMore ? ' (계속 조회 중...)' : ''}`);
				}
			},
		});
	} catch (err) {
		console.error('\n❌ 실행 중 오류 발생:');
		console.error(err);
		process.exit(1);
	}
}

main();