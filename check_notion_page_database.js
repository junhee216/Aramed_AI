// check_notion_page_database.js
// Notion 페이지 내부의 데이터베이스 확인 스크립트

import 'dotenv/config';
import { Client } from '@notionhq/client';

const notionApiKey = process.env.NOTION_API_KEY;
const pageOrDatabaseId = process.env.NOTION_DATABASE_ID;

if (!notionApiKey || !pageOrDatabaseId) {
	console.error('❌ .env 설정 오류: NOTION_API_KEY 또는 NOTION_DATABASE_ID 가 없습니다.');
	process.exit(1);
}

const notion = new Client({ auth: notionApiKey });

console.log('✅ ENV LOADED:', {
	keyPrefix: notionApiKey.slice(0, 8) + '...',
	pageOrDatabaseId,
});

async function findDatabase() {
	try {
		// 1. 먼저 페이지로 시도
		console.log('\n📄 페이지 정보 확인 중...');
		const page = await notion.pages.retrieve({
			page_id: pageOrDatabaseId,
		});

		console.log('✅ 페이지를 찾았습니다!');
		const title = page.properties?.title || 
			(page.properties && Object.keys(page.properties).length > 0 
				? Object.keys(page.properties)[0] 
				: '제목 없음');
		
		console.log('페이지 ID:', page.id);
		console.log('페이지 URL:', page.url);

		// 2. 페이지의 자식 블록들을 확인하여 데이터베이스 찾기
		console.log('\n🔍 페이지 내부의 데이터베이스 찾는 중...');
		
		const children = await notion.blocks.children.list({
			block_id: pageOrDatabaseId,
			page_size: 100,
		});

		let databaseFound = false;

		for (const block of children.results) {
			if (block.type === 'child_database') {
				databaseFound = true;
				const dbId = block.id;
				const dbTitle = block.child_database?.title || '제목 없음';
				
				console.log(`\n✅ 데이터베이스를 찾았습니다!`);
				console.log(`제목: ${dbTitle}`);
				console.log(`ID: ${dbId}`);
				
				// 데이터베이스 정보 조회
				const db = await notion.databases.retrieve({
					database_id: dbId,
				});

				console.log('\n📊 데이터베이스 속성 구조:');
				const properties = db.properties;
				console.log(`총 ${Object.keys(properties).length}개의 속성이 있습니다:\n`);
				
				for (const [propName, propInfo] of Object.entries(properties)) {
					console.log(`- ${propName} (${propInfo.type})`);
					if (propInfo.type === 'select' && propInfo.select?.options) {
						console.log(`  옵션: ${propInfo.select.options.map(o => o.name).join(', ')}`);
					}
				}

				// 데이터베이스 내용 조회 (최대 10개 샘플)
				console.log('\n\n📖 데이터베이스 내용 (최대 10개 샘플):');
				console.log('='.repeat(60));
				
				const response = await notion.databases.query({
					database_id: dbId,
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
					console.log('⚠️  더 많은 항목이 있습니다.');
				}

				return;
			}
		}

		if (!databaseFound) {
			console.log('⚠️  페이지 내부에 데이터베이스를 찾을 수 없습니다.');
			console.log('\n다른 방법:');
			console.log('1. Notion에서 "[Aramed] 수학 문제 메타데이터 뱅크" 데이터베이스를 직접 엽니다');
			console.log('2. URL에서 데이터베이스 ID를 확인합니다 (페이지 ID가 아닌)');
			console.log('3. 데이터베이스는 보통 /v/ 경로를 사용합니다');
		}

	} catch (error) {
		if (error.code === 'object_not_found') {
			console.error('\n❌ 페이지 또는 데이터베이스를 찾을 수 없습니다.');
			console.error('\n해결 방법:');
			console.error('1. Notion에서 "[Aramed] 수학 문제 메타데이터 뱅크" 데이터베이스를 엽니다');
			console.error('2. 우측 상단의 "..." 메뉴를 클릭합니다');
			console.error('3. "연결 추가" 또는 "Add connections"를 선택합니다');
			console.error('4. 사용 중인 Integration을 선택하여 데이터베이스와 연결합니다');
		} else {
			console.error('\n❌ 오류 발생:', error.message);
			console.error('상세:', error);
		}
		process.exit(1);
	}
}

findDatabase();