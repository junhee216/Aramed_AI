// check_p6_fields.js
// 확통 P6 문제의 실제 필드 값 확인

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
		default:
			return null;
	}
}

async function checkP6Fields() {
	try {
		// P6 문제만 가져오기
		const pages = await collectPaginatedAPI(notion.databases.query, {
			database_id: databaseId,
			filter: {
				property: '문제ID',
				title: {
					contains: '확통_2024학년도_현우진_드릴_P6'
				}
			}
		});
		
		console.log(`\n📖 총 ${pages.length}개 페이지 발견\n`);
		
		if (pages.length === 0) {
			console.log('❌ P6 문제를 찾을 수 없습니다.');
			return;
		}
		
		// 첫 번째 문제의 모든 필드 확인
		const firstPage = pages[0];
		const props = firstPage.properties;
		const allFieldNames = Object.keys(props);
		
		console.log('='.repeat(80));
		console.log(`[${extractPropertyValue(props['문제ID'])} 필드 확인]`);
		console.log('='.repeat(80));
		
		// 해설이 들어있을 가능성이 있는 필드들 확인
		const possibleFields = [
			'해설', '25', '소단원', '후행개념', '선행개념', '개념연결',
			'핵심개념', '출제의도', '문제구조', '핵심패턴'
		];
		
		console.log('\n🔍 해설 관련 필드 값 확인:\n');
		
		for (const fieldName of allFieldNames) {
			const value = extractPropertyValue(props[fieldName]);
			if (value && value.length > 50) {
				console.log(`[${fieldName}]`);
				console.log(`  길이: ${value.length}자`);
				console.log(`  내용: ${value.substring(0, 200)}...`);
				console.log('');
			}
		}
		
		// 모든 필드 이름과 값 요약
		console.log('\n📋 모든 필드 요약:\n');
		allFieldNames.forEach((fieldName, i) => {
			const value = extractPropertyValue(props[fieldName]);
			const valueStr = value ? (typeof value === 'string' ? value.substring(0, 50) : String(value)) : '(비어있음)';
			console.log(`${i + 1}. ${fieldName}: ${valueStr}${value && typeof value === 'string' && value.length > 50 ? '...' : ''}`);
		});
		
	} catch (error) {
		console.error('\n❌ 오류 발생:', error.message);
		if (error.code) {
			console.error(`   코드: ${error.code}`);
		}
		console.error(error.stack);
	}
}

checkP6Fields();
