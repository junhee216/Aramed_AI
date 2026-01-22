// check_env.js
// .env 파일 로드 확인 스크립트

import 'dotenv/config';

console.log('=== .env 파일 확인 ===\n');

const notionApiKey = process.env.NOTION_API_KEY;
const databaseId = process.env.NOTION_DATABASE_ID;
const pageId = process.env.NOTION_PAGE_ID;

console.log('NOTION_API_KEY:', notionApiKey ? `${notionApiKey.slice(0, 8)}... (${notionApiKey.length}자)` : '❌ 없음');
console.log('NOTION_DATABASE_ID:', databaseId || '❌ 없음');
console.log('NOTION_PAGE_ID:', pageId || '❌ 없음');

if (!notionApiKey || !databaseId) {
    console.log('\n⚠️  필수 환경 변수가 누락되었습니다.');
    console.log('\n.env 파일 위치: C:\\Users\\a\\Documents\\Aramed_AI\\.env');
    console.log('\n.env 파일 형식 예시:');
    console.log('NOTION_API_KEY=secret_xxxxx');
    console.log('NOTION_DATABASE_ID=2e66d1f1c771802b83c6fb0bb314db1a');
    process.exit(1);
} else {
    console.log('\n✅ 모든 환경 변수가 로드되었습니다.');
}
