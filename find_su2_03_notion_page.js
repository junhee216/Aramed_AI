// find_su2_03_notion_page.js
// 수2_2025학년도_현우진_드릴_03 페이지 정확히 찾기

import 'dotenv/config';
import { Client, collectPaginatedAPI } from '@notionhq/client';

const notionApiKey = process.env.NOTION_API_KEY;
const databaseId = process.env.NOTION_DATABASE_ID;

if (!notionApiKey || !databaseId) {
	console.error('❌ .env 설정 오류');
	process.exit(1);
}

const notion = new Client({ auth: notionApiKey });

async function findPage() {
	console.log('📖 수2_2025학년도_현우진_드릴_03 페이지 찾는 중...\n');
	
	try {
		// 모든 페이지 가져오기
		const allPages = await collectPaginatedAPI(notion.databases.query, {
			database_id: databaseId,
			filter: {
				property: '문제ID',
				title: {
					contains: '수2_2025'
				}
			}
		});
		
		console.log(`총 ${allPages.length}개 페이지 발견\n`);
		
		// 수2_2025학년도_현우진_드릴_03 관련 페이지 찾기
		const targetPages = allPages.filter(page => {
			const titleProp = page.properties['문제ID'];
			if (titleProp && titleProp.type === 'title') {
				const title = titleProp.title.map(t => t.plain_text).join('');
				return title.includes('수2_2025학년도_현우진_드릴_03') || 
				       title.includes('수2_2025_현우진_드릴_03');
			}
			return false;
		});
		
		if (targetPages.length === 0) {
			console.log('❌ 수2_2025학년도_현우진_드릴_03 페이지를 찾을 수 없습니다.\n');
			console.log('찾은 수2 관련 페이지들:');
			allPages.slice(0, 10).forEach((page, i) => {
				const titleProp = page.properties['문제ID'];
				const title = titleProp?.title?.map(t => t.plain_text).join('') || '제목 없음';
				console.log(`  ${i+1}. ${title}`);
			});
			return;
		}
		
		console.log(`✅ ${targetPages.length}개 페이지 발견:\n`);
		
		for (const page of targetPages) {
			const titleProp = page.properties['문제ID'];
			const title = titleProp.title.map(t => t.plain_text).join('');
			
			console.log(`📄 ${title}`);
			console.log(`   ID: ${page.id}`);
			console.log(`   URL: https://www.notion.so/${page.id.replace(/-/g, '')}`);
			
			// 모든 속성 출력
			console.log(`\n   속성 목록:`);
			const props = page.properties;
			Object.keys(props).forEach(propName => {
				const prop = props[propName];
				console.log(`     - ${propName} (${prop.type})`);
			});
			console.log('');
		}
		
	} catch (error) {
		console.error('❌ 오류:', error.message);
	}
}

findPage();
