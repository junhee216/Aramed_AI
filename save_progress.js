// save_progress.js
// 현재 세션의 대화 요약과 진행 상황을 노션 데이터베이스에 새 페이지로 저장
// Node >= 18, ESM("type": "module") 환경 기준

import 'dotenv/config';
import { Client } from '@notionhq/client';

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

// ✅ 3. 현재 시간 기반 제목 생성
function generateTitle() {
	const now = new Date();
	const dateStr = now.toLocaleDateString('ko-KR', {
		year: 'numeric',
		month: '2-digit',
		day: '2-digit',
	});
	const timeStr = now.toLocaleTimeString('ko-KR', {
		hour: '2-digit',
		minute: '2-digit',
	});
	return `세이브 ${dateStr} ${timeStr}`;
}

// ✅ 4. 블록 구조 생성 함수
function buildBlocks(summary, progress) {
	const blocks = [];

	// 요약 섹션
	if (summary) {
		blocks.push({
			object: 'block',
			type: 'heading_2',
			heading_2: {
				rich_text: [{ type: 'text', text: { content: '📝 세션 요약' } }],
			},
		});

		blocks.push({
			object: 'block',
			type: 'paragraph',
			paragraph: {
				rich_text: [{ type: 'text', text: { content: summary } }],
			},
		});

		blocks.push({
			object: 'block',
			type: 'divider',
			divider: {},
		});
	}

	// 진행 상황 섹션
	if (progress) {
		blocks.push({
			object: 'block',
			type: 'heading_2',
			heading_2: {
				rich_text: [{ type: 'text', text: { content: '🚀 진행 상황' } }],
			},
		});

		blocks.push({
			object: 'block',
			type: 'paragraph',
			paragraph: {
				rich_text: [{ type: 'text', text: { content: progress } }],
			},
		});
	}

	return blocks;
}

// ✅ 5. 노션 데이터베이스에 새 페이지 생성
async function saveProgress(summary = '', progress = '') {
	try {
		const title = generateTitle();
		const blocks = buildBlocks(summary, progress);

		// 데이터베이스에 새 페이지 생성
		const newPage = await notion.pages.create({
			parent: {
				database_id: databaseId,
			},
			properties: {
				// '마스터 프로토콜 v1.0' 속성이 title 타입이라고 가정
				'마스터 프로토콜 v1.0': {
					title: [
						{
							text: {
								content: title,
							},
						},
					],
				},
			},
			children: blocks.length > 0 ? blocks : undefined,
		});

		console.log('\n✅ 노션에 저장 완료!');
		console.log('📄 페이지 ID:', newPage.id);
		console.log('📝 제목:', title);
		console.log('🔗 URL:', newPage.url);

		return newPage;
	} catch (err) {
		console.error('\n❌ 저장 중 오류 발생:');
		console.error(err.body || err);
		throw err;
	}
}

// ✅ 6. 메인 실행 함수
async function main() {
	try {
		// 예시: 현재 세션의 요약과 진행 상황
		// 실제 사용 시에는 인자로 받거나 환경변수에서 읽어올 수 있음
		const sessionSummary = process.env.SESSION_SUMMARY || 
			'현재 세션의 대화 요약과 진행 상황을 노션에 저장하는 시스템 구축 중.';
		
		const sessionProgress = process.env.SESSION_PROGRESS || 
			'기기간 동기화 및 기억 유지를 위한 노션 세이브/로드 시스템 개발 진행 중. save_progress.js 작성 완료.';

		await saveProgress(sessionSummary, sessionProgress);
	} catch (err) {
		console.error('\n❌ 실행 중 오류 발생:');
		console.error(err);
		process.exit(1);
	}
}

// 직접 실행 시에만 main 함수 실행
// Windows에서는 import.meta.url이 file:/// 형식으로 올 수 있으므로 더 간단하게 처리
if (import.meta.url.endsWith(process.argv[1].replace(/\\/g, '/'))) {
	main();
}

// 다른 파일에서 import 시 사용할 수 있도록 export
export { saveProgress, generateTitle, buildBlocks };
