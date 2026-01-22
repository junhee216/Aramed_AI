// check_notion_field_names.js
// Notion 데이터베이스의 실제 필드 이름 확인

import 'dotenv/config';
import { Client } from '@notionhq/client';

const notionApiKey = process.env.NOTION_API_KEY;
const databaseId = process.env.NOTION_DATABASE_ID;

if (!notionApiKey || !databaseId) {
	console.error('❌ .env 설정 오류');
	process.exit(1);
}

const notion = new Client({ auth: notionApiKey });

async function checkFieldNames() {
	try {
		const db = await notion.databases.retrieve({
			database_id: databaseId
		});
		
		console.log('='.repeat(80));
		console.log('[Notion 데이터베이스 필드 이름 확인]');
		console.log('='.repeat(80));
		
		const allFields = Object.keys(db.properties);
		console.log(`\n📋 총 ${allFields.length}개 필드 발견\n`);
		
		// 해설 관련 필드 찾기
		const 해설Fields = allFields.filter(field => 
			field.includes('해설') || 
			field.includes('Stage') ||
			field.includes('전략') ||
			field.includes('개념')
		);
		
		console.log('🔍 해설 관련 필드:');
		해설Fields.forEach(field => {
			const prop = db.properties[field];
			console.log(`  - ${field} (${prop.type})`);
		});
		
		// 모든 필드 출력
		console.log('\n📋 모든 필드 목록:');
		allFields.forEach((field, i) => {
			const prop = db.properties[field];
			console.log(`${i + 1}. ${field} (${prop.type})`);
		});
		
	} catch (error) {
		console.error('❌ 오류 발생:', error.message);
		if (error.code) {
			console.error(`   코드: ${error.code}`);
		}
	}
}

checkFieldNames();
