// check_su2_p3_notion.js
// 수2_2025학년도_현우진_드릴_P3 페이지 전체 내용 확인

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
			return prop.date ? prop.date.start : null;
		case 'checkbox':
			return prop.checkbox;
		case 'url':
			return prop.url || null;
		default:
			return `[${prop.type}]`;
	}
}

async function checkPage() {
	console.log('📖 수2_2025학년도_현우진_드릴_P3 페이지 찾는 중...\n');
	
	try {
		// P3 관련 페이지 찾기
		const allPages = await collectPaginatedAPI(notion.databases.query, {
			database_id: databaseId,
			filter: {
				property: '문제ID',
				title: {
					contains: '수2_2025학년도_현우진_드릴_P3'
				}
			}
		});
		
		if (allPages.length === 0) {
			console.log('❌ 페이지를 찾을 수 없습니다.');
			return;
		}
		
		console.log(`✅ ${allPages.length}개 페이지 발견\n`);
		console.log('='.repeat(80));
		
		for (const page of allPages) {
			const titleProp = page.properties['문제ID'];
			const title = titleProp?.title?.map(t => t.plain_text).join('') || '제목 없음';
			
			console.log(`\n📄 페이지: ${title}`);
			console.log(`   ID: ${page.id}`);
			console.log(`   URL: https://www.notion.so/${page.id.replace(/-/g, '')}`);
			console.log('\n' + '-'.repeat(80));
			
			// 모든 속성 출력
			const props = page.properties;
			const allFields = Object.keys(props);
			
			console.log(`\n📋 총 ${allFields.length}개 필드:\n`);
			
			for (let i = 0; i < allFields.length; i++) {
				const fieldName = allFields[i];
				const prop = props[fieldName];
				const value = extractPropertyValue(prop);
				
				console.log(`[${i + 1}] ${fieldName} (${prop.type})`);
				
				if (value === null || value === undefined || value === '') {
					console.log(`    값: (비어있음)`);
				} else if (typeof value === 'string') {
					const displayValue = value.length > 200 ? value.substring(0, 200) + '...' : value;
					console.log(`    값: ${displayValue}`);
				} else if (Array.isArray(value)) {
					console.log(`    값: [${value.join(', ')}]`);
				} else {
					console.log(`    값: ${value}`);
				}
				console.log('');
			}
			
			console.log('='.repeat(80));
		}
		
	} catch (error) {
		console.error('❌ 오류:', error.message);
		if (error.code) {
			console.error(`   코드: ${error.code}`);
		}
	}
}

checkPage();
