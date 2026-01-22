// check_notion_p4_fields.js
// 노션 P4 페이지의 실수포인트 필드 확인

import 'dotenv/config';
import { Client, collectPaginatedAPI } from '@notionhq/client';

const notionApiKey = process.env.NOTION_API_KEY;
const databaseId = process.env.NOTION_DATABASE_ID;

if (!notionApiKey || !databaseId) {
	console.error('❌ .env 설정 오류');
	process.exit(1);
}

const notion = new Client({ auth: notionApiKey });

function extractPropertyValue(prop) {
	if (!prop) return null;
	
	switch (prop.type) {
		case 'title':
			return prop.title.map(t => t.plain_text).join('');
		case 'rich_text':
			return prop.rich_text.map(t => t.plain_text).join('');
		case 'number':
			return prop.number;
		case 'select':
			return prop.select?.name || null;
		case 'multi_select':
			return prop.multi_select.map(s => s.name);
		case 'date':
			return prop.date;
		case 'checkbox':
			return prop.checkbox;
		case 'url':
			return prop.url;
		default:
			return null;
	}
}

async function checkP4Fields() {
	console.log('='.repeat(80));
	console.log('노션 P4 페이지의 실수포인트 및 오답시나리오 필드 확인');
	console.log('='.repeat(80));
	
	try {
		// 노션에서 P4 관련 페이지 찾기
		const allPages = await collectPaginatedAPI(notion.databases.query, {
			database_id: databaseId,
			filter: {
				property: '문제ID',
				title: {
					contains: '확통_2024학년도_현우진_드릴_P4'
				}
			}
		});
		
		console.log(`\n📖 노션에서 발견된 P4 페이지: ${allPages.length}개\n`);
		
		for (const page of allPages) {
			const props = page.properties;
			const 문제ID = extractPropertyValue(props['문제ID']);
			const 실수포인트 = extractPropertyValue(props['실수포인트']);
			const 오답시나리오 = extractPropertyValue(props['오답시나리오']);
			
			console.log(`\n📄 ${문제ID}`);
			console.log(`실수포인트: ${실수포인트 || '(비어있음)'}`);
			console.log(`오답시나리오 (길이: ${오답시나리오?.length || 0}자):`);
			if (오답시나리오) {
				const lines = 오답시나리오.split('\n');
				console.log(`  총 ${lines.length}줄`);
				lines.forEach((line, i) => {
					if (line.trim()) {
						console.log(`  ${i + 1}. ${line.substring(0, 80)}${line.length > 80 ? '...' : ''}`);
					}
				});
			} else {
				console.log('  (비어있음)');
			}
		}
		
	} catch (error) {
		console.error('\n❌ 오류 발생:', error.message);
		if (error.code) {
			console.error(`   코드: ${error.code}`);
		}
		console.error(error.stack);
	}
}

checkP4Fields();
