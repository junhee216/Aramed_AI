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

async function findMissingProblem() {
	const targetContent = 'sin x 부호 변화 무시 2. 연결부 불연속 간과 3. 수열 대입 실수';
	const emptyPageId = '2e96d1f1-c771-81b7-8b15-ca2802f41372';
	
	console.log('다른 페이지에서 정확한 내용 검색 중...\n');
	
	// 모든 페이지 가져오기 (필터 없이)
	const allPages = await collectPaginatedAPI(notion.databases.query, {
		database_id: databaseId
	});
	
	console.log(`전체 페이지 수: ${allPages.length}개\n`);
	
	let found = false;
	for (const page of allPages) {
		if (page.id === emptyPageId) continue; // 빈 페이지 제외
		
		const props = page.properties;
		const 문제ID = extractPropertyValue(props['문제ID']);
		const 후행개념 = extractPropertyValue(props['후행개념']);
		const 실수포인트 = extractPropertyValue(props['실수포인트']);
		const 함정설계 = extractPropertyValue(props['함정설계']);
		const 선행개념 = extractPropertyValue(props['선행개념']);
		
		// 정확한 내용 검색
		const searchText = `${후행개념 || ''} ${실수포인트 || ''} ${함정설계 || ''} ${선행개념 || ''}`;
		
		if (searchText.includes('sin x 부호 변화 무시') && 
		    searchText.includes('연결부 불연속 간과') && 
		    searchText.includes('수열 대입 실수')) {
			console.log(`✅ 정확히 일치하는 페이지 발견: ${문제ID || '(문제ID 없음)'}`);
			console.log(`   페이지 ID: ${page.id}`);
			if (후행개념?.includes('sin x')) {
				console.log(`   후행개념: ${후행개념}`);
			}
			if (실수포인트?.includes('sin x')) {
				console.log(`   실수포인트: ${실수포인트}`);
			}
			console.log('---');
			found = true;
		}
	}
	
	if (!found) {
		console.log('❌ 다른 페이지에서 해당 내용을 찾을 수 없습니다.');
		console.log('수학 논리적으로 적절한 장소가 없으므로 빈 페이지를 삭제합니다...\n');
		
		try {
			await notion.pages.update({
				page_id: emptyPageId,
				archived: true
			});
			console.log('✅ 빈 페이지 삭제 완료');
		} catch (error) {
			console.error('❌ 삭제 실패:', error.message);
		}
	}
}

findMissingProblem();
