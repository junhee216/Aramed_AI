// check_field_types.js
// 필드 타입 확인

import 'dotenv/config';
import { Client } from '@notionhq/client';

const notionApiKey = process.env.NOTION_API_KEY;
const databaseId = process.env.NOTION_DATABASE_ID;

if (!notionApiKey || !databaseId) {
	console.error('❌ .env 설정 오류');
	process.exit(1);
}

const notion = new Client({ auth: notionApiKey });

async function checkFieldTypes() {
	const response = await notion.databases.retrieve({
		database_id: databaseId
	});
	
	console.log('필드 타입 확인:\n');
	
	Object.entries(response.properties).forEach(([name, prop]) => {
		console.log(`${name}: ${prop.type}`);
		if (prop.type === 'select' && prop.select) {
			console.log(`  옵션: ${prop.select.options?.map(o => o.name).join(', ') || '없음'}`);
		}
	});
}

checkFieldTypes();
