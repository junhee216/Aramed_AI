// check_notion_database.js
// Notion 데이터베이스 내용 확인 스크립트
// "[Aramed] 수학 문제 메타데이터 뱅크" 데이터베이스의 모든 속성과 내용을 출력

import 'dotenv/config';
import { Client } from '@notionhq/client';

const notionApiKey = process.env.NOTION_API_KEY;
const databaseId = process.env.NOTION_DATABASE_ID;

if (!notionApiKey || !databaseId) {
	console.error('❌ .env 설정 오류: NOTION_API_KEY 또는 NOTION_DATABASE_ID 가 없습니다.');
	process.exit(1);
}

const notion = new Client({ auth: notionApiKey });

console.log('✅ ENV LOADED:', {
	keyPrefix: notionApiKey.slice(0, 8) + '...',
	databaseId,
});

// 데이터베이스 정보 및 구조 확인
async function checkDatabase() {
	try {
		// 1. 데이터베이스 메타 정보 조회
		const db = await notion.databases.retrieve({
			database_id: databaseId,
		});

		console.log('\n📋 데이터베이스 정보:');
		const title = db.title && db.title.length > 0
			? db.title.map((t) => t.plain_text).join('')
			: '(제목 없음)';
		
		console.log('제목:', title);
		console.log('ID:', db.id);
		console.log('\n📊 데이터베이스 속성 구조:');
		
		// 모든 속성(컬럼) 정보 출력
		const properties = db.properties;
		console.log(`총 ${Object.keys(properties).length}개의 속성이 있습니다:\n`);
		
		for (const [propName, propInfo] of Object.entries(properties)) {
			console.log(`- ${propName} (${propInfo.type})`);
			if (propInfo.type === 'select' && propInfo.select?.options) {
				console.log(`  옵션: ${propInfo.select.options.map(o => o.name).join(', ')}`);
			}
		}

		// 2. 데이터베이스 내용 조회 (최대 10개 샘플)
		console.log('\n\n📖 데이터베이스 내용 (최대 10개 샘플):');
		console.log('='.repeat(60));
		
		const response = await notion.databases.query({
			database_id: databaseId,
			page_size: 10,
		});

		if (response.results.length === 0) {
			console.log('⚠️  데이터베이스가 비어있습니다.');
			return;
		}

		for (let i = 0; i < response.results.length; i++) {
			const page = response.results[i];
			const props = page.properties;
			
			console.log(`\n[${i + 1}] 페이지 ID: ${page.id}`);
			
			// 모든 속성 출력
			for (const [propName, propValue] of Object.entries(props)) {
				let value = '';
				
				switch (propValue.type) {
					case 'title':
						value = propValue.title.map(t => t.plain_text).join('');
						break;
					case 'rich_text':
						value = propValue.rich_text.map(t => t.plain_text).join('');
						break;
					case 'number':
						value = propValue.number;
						break;
					case 'select':
						value = propValue.select?.name || '';
						break;
					case 'multi_select':
						value = propValue.multi_select.map(s => s.name).join(', ');
						break;
					case 'date':
						value = propValue.date ? propValue.date.start : '';
						break;
					case 'checkbox':
						value = propValue.checkbox;
						break;
					case 'url':
						value = propValue.url || '';
						break;
					case 'email':
						value = propValue.email || '';
						break;
					case 'phone_number':
						value = propValue.phone_number || '';
						break;
					default:
						value = `[${propValue.type}]`;
				}
				
				console.log(`  ${propName}: ${value || '(비어있음)'}`);
			}
			console.log('-'.repeat(60));
		}

		console.log(`\n✅ 총 ${response.results.length}개 항목 조회 완료`);
		if (response.has_more) {
			console.log('⚠️  더 많은 항목이 있습니다. 전체 조회를 원하시면 read_notion_database.js를 사용하세요.');
		}

	} catch (error) {
		if (error.code === 'object_not_found') {
			console.error('\n❌ 데이터베이스를 찾을 수 없습니다.');
			console.error('\n해결 방법:');
			console.error('1. Notion에서 "[Aramed] 수학 문제 메타데이터 뱅크" 데이터베이스를 엽니다');
			console.error('2. 우측 상단의 "..." 메뉴를 클릭합니다');
			console.error('3. "연결 추가" 또는 "Add connections"를 선택합니다');
			console.error('4. 사용 중인 Integration을 선택하여 데이터베이스와 연결합니다');
			console.error('5. .env 파일의 NOTION_DATABASE_ID가 올바른지 확인합니다');
			console.error('\n데이터베이스 ID 확인 방법:');
			console.error('- Notion 데이터베이스 URL에서 32자리 ID를 추출합니다');
			console.error('- 예: https://www.notion.so/2e66d1f1c771802b83c6fb0bb314db1a');
			console.error('  → ID: 2e66d1f1c771802b83c6fb0bb314db1a');
		} else {
			console.error('\n❌ 오류 발생:', error.message);
		}
		process.exit(1);
	}
}

checkDatabase();