// test_db_connection.js
// 데이터베이스 ID를 직접 입력해서 테스트

import 'dotenv/config';
import { Client } from '@notionhq/client';

const notionApiKey = process.env.NOTION_API_KEY;

if (!notionApiKey) {
    console.error('❌ NOTION_API_KEY가 없습니다.');
    process.exit(1);
}

// 명령줄 인자로 데이터베이스 ID 받기
const databaseId = process.argv[2];

if (!databaseId) {
    console.error('❌ 사용법: node test_db_connection.js <데이터베이스_ID>');
    console.error('예시: node test_db_connection.js 2e66d1f1c771802b83c6fb0bb314db1a');
    process.exit(1);
}

const notion = new Client({ auth: notionApiKey });

console.log('✅ API 키 로드됨:', notionApiKey.slice(0, 8) + '...');
console.log('📋 테스트할 데이터베이스 ID:', databaseId);
console.log('\n연결 시도 중...\n');

async function testConnection() {
    try {
        // 1. 데이터베이스 정보 조회
        const db = await notion.databases.retrieve({
            database_id: databaseId,
        });

        const title = db.title && db.title.length > 0
            ? db.title.map((t) => t.plain_text).join('')
            : '(제목 없음)';

        console.log('✅ 연결 성공!\n');
        console.log('📋 데이터베이스 정보:');
        console.log('  제목:', title);
        console.log('  ID:', db.id);
        console.log('\n📊 속성 구조:');
        
        const properties = db.properties;
        console.log(`  총 ${Object.keys(properties).length}개의 속성:\n`);
        
        for (const [propName, propInfo] of Object.entries(properties)) {
            console.log(`  - ${propName} (${propInfo.type})`);
        }

        // 2. 샘플 데이터 조회 (최대 5개)
        console.log('\n📖 샘플 데이터 (최대 5개):');
        console.log('='.repeat(60));
        
        const response = await notion.databases.query({
            database_id: databaseId,
            page_size: 5,
        });

        if (response.results.length === 0) {
            console.log('⚠️  데이터베이스가 비어있습니다.');
            return;
        }

        for (let i = 0; i < response.results.length; i++) {
            const page = response.results[i];
            const props = page.properties;
            
            console.log(`\n[${i + 1}]`);
            
            // 제목 속성 찾기
            for (const [propName, propValue] of Object.entries(props)) {
                if (propValue.type === 'title') {
                    const titleText = propValue.title.map(t => t.plain_text).join('');
                    console.log(`  제목: ${titleText || '(비어있음)'}`);
                    break;
                }
            }
            
            // 주요 속성 몇 개만 출력
            let count = 0;
            for (const [propName, propValue] of Object.entries(props)) {
                if (propValue.type === 'title') continue;
                if (count >= 3) break; // 최대 3개만
                
                let value = '';
                switch (propValue.type) {
                    case 'rich_text':
                        value = propValue.rich_text.map(t => t.plain_text).join('').substring(0, 50);
                        break;
                    case 'select':
                        value = propValue.select?.name || '';
                        break;
                    case 'number':
                        value = propValue.number;
                        break;
                    case 'checkbox':
                        value = propValue.checkbox;
                        break;
                    default:
                        value = `[${propValue.type}]`;
                }
                
                if (value) {
                    console.log(`  ${propName}: ${value}`);
                    count++;
                }
            }
            console.log('-'.repeat(60));
        }

        console.log(`\n✅ 총 ${response.results.length}개 항목 조회 완료`);
        if (response.has_more) {
            console.log('⚠️  더 많은 항목이 있습니다.');
        }

        console.log('\n💡 이 ID를 .env 파일에 다음과 같이 저장하세요:');
        console.log(`NOTION_DATABASE_ID=${databaseId}`);

    } catch (error) {
        if (error.code === 'object_not_found') {
            console.error('\n❌ 데이터베이스를 찾을 수 없습니다.');
            console.error('\n가능한 원인:');
            console.error('1. 데이터베이스 ID가 잘못되었습니다');
            console.error('2. Integration이 데이터베이스와 공유되지 않았습니다');
            console.error('\n해결 방법:');
            console.error('1. Notion에서 데이터베이스를 엽니다');
            console.error('2. 우측 상단 "..." → "연결 추가" → Integration 선택');
        } else {
            console.error('\n❌ 오류 발생:', error.message);
        }
        process.exit(1);
    }
}

testConnection();
