import 'dotenv/config';
import { Client, collectPaginatedAPI } from '@notionhq/client';

const notion = new Client({ auth: process.env.NOTION_API_KEY });
const databaseId = process.env.NOTION_DATABASE_ID;

function extractPropertyValue(prop) {
	if (!prop) return null;
	if (prop.type === 'title') {
		return prop.title.map(t => t.plain_text).join('');
	}
	if (prop.type === 'rich_text') {
		return prop.rich_text.map(t => t.plain_text).join('');
	}
	return null;
}

function extractAllPropertyValue(prop) {
	if (!prop) return null;
	if (prop.type === 'title') {
		return prop.title.map(t => t.plain_text).join('');
	}
	if (prop.type === 'rich_text') {
		return prop.rich_text.map(t => t.plain_text).join('');
	}
	if (prop.type === 'number') {
		return prop.number;
	}
	return null;
}

async function findSinXField() {
	const allPages = await collectPaginatedAPI(notion.databases.query, {
		database_id: databaseId,
		filter: {
			or: [
				{
					property: '후행개념',
					rich_text: {
						contains: 'sin x'
					}
				},
				{
					property: '후행개념',
					rich_text: {
						contains: '부호 변화'
					}
				}
			]
		}
	});
	
	console.log(`찾은 페이지: ${allPages.length}개\n`);
	
	for (const page of allPages) {
		const props = page.properties;
		
		console.log(`페이지 ID: ${page.id}`);
		console.log(`\n모든 필드 확인:`);
		
		// 모든 필드 확인
		for (const [key, prop] of Object.entries(props)) {
			const value = extractAllPropertyValue(prop);
			if (value !== null && value !== '' && value !== 0) {
				const displayValue = typeof value === 'string' && value.length > 50 
					? value.substring(0, 50) + '...' 
					: value;
				console.log(`  ${key}: ${displayValue}`);
			}
		}
		
		// 특별히 확인할 필드
		const 문제ID = extractAllPropertyValue(props['문제ID']);
		const 후행개념 = extractAllPropertyValue(props['후행개념']);
		const 예상시간 = extractAllPropertyValue(props['예상시간']);
		
		console.log(`\n주요 필드:`);
		console.log(`  문제ID: ${문제ID || '(비어있음)'}`);
		console.log(`  후행개념: ${후행개념 || '(비어있음)'}`);
		console.log(`  예상시간: ${예상시간 !== null ? 예상시간 : '(비어있음)'}`);
		console.log('---\n');
	}
}

findSinXField();
