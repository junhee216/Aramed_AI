// check_all_problems.js
// 노션 데이터베이스의 모든 문제를 조회하여 구조 파악

import 'dotenv/config';
import { Client, collectPaginatedAPI } from '@notionhq/client';

const notionApiKey = process.env.NOTION_API_KEY;
const databaseId = process.env.NOTION_DATABASE_ID;

if (!notionApiKey || !databaseId) {
    console.error('❌ .env 설정 오류');
    process.exit(1);
}

const notion = new Client({ auth: notionApiKey });

// Rate Limiter
class RateLimiter {
    constructor(maxRequestsPerSecond = 3) {
        this.maxRequests = maxRequestsPerSecond;
        this.requests = [];
    }

    async waitIfNeeded() {
        const now = Date.now();
        this.requests = this.requests.filter((time) => now - time < 1000);
        if (this.requests.length >= this.maxRequests) {
            const oldestRequest = Math.min(...this.requests);
            const waitTime = 1000 - (now - oldestRequest) + 10;
            if (waitTime > 0) {
                await new Promise((resolve) => setTimeout(resolve, waitTime));
            }
        }
        this.requests.push(Date.now());
    }
}

const rateLimiter = new RateLimiter(3);

async function getAllProblems() {
    console.log('📖 모든 문제 조회 중...\n');
    
    const allPages = [];
    let hasMore = true;
    let startCursor = null;
    let totalFetched = 0;

    try {
        while (hasMore) {
            await rateLimiter.waitIfNeeded();

            const response = await notion.databases.query({
                database_id: databaseId,
                start_cursor: startCursor || undefined,
                page_size: 100,
            });

            allPages.push(...response.results);
            totalFetched += response.results.length;

            if (totalFetched % 100 === 0) {
                console.log(`📊 진행: ${totalFetched}개 조회 완료...`);
            }

            hasMore = response.has_more;
            startCursor = response.next_cursor;
        }

        console.log(`\n✅ 총 ${allPages.length}개 문제를 조회했습니다.\n`);

        // 문제ID별로 그룹화
        const problemsByFile = {};
        
        for (const page of allPages) {
            const props = page.properties;
            const problemIdProp = props['문제ID'];
            
            if (problemIdProp && problemIdProp.type === 'title') {
                const problemId = problemIdProp.title.map(t => t.plain_text).join('');
                
                // 파일명 추출 (예: 수1_2025학년도_현우진_드릴_P1_15)
                const match = problemId.match(/^(.+)_(\d+)$/);
                if (match) {
                    const filePrefix = match[1];
                    const problemNum = parseInt(match[2]);
                    
                    if (!problemsByFile[filePrefix]) {
                        problemsByFile[filePrefix] = [];
                    }
                    problemsByFile[filePrefix].push(problemNum);
                }
            }
        }

        // 결과 출력
        console.log('📊 파일별 문제 개수:\n');
        console.log('='.repeat(60));
        
        for (const [filePrefix, problemNums] of Object.entries(problemsByFile)) {
            problemNums.sort((a, b) => a - b);
            const maxNum = Math.max(...problemNums);
            const count = problemNums.length;
            
            console.log(`${filePrefix}:`);
            console.log(`  총 ${count}개 문제 (${problemNums[0]}번 ~ ${maxNum}번)`);
            console.log(`  문제 번호: ${problemNums.join(', ')}`);
            console.log('');
        }

        // 샘플 데이터 확인 (각 파일의 첫 번째 문제)
        console.log('\n📋 샘플 데이터 (각 파일의 첫 번째 문제):\n');
        console.log('='.repeat(60));
        
        const seenFiles = new Set();
        let sampleCount = 0;
        
        for (const page of allPages) {
            if (sampleCount >= 15) break; // 최대 15개 샘플
            
            const props = page.properties;
            const problemIdProp = props['문제ID'];
            
            if (problemIdProp && problemIdProp.type === 'title') {
                const problemId = problemIdProp.title.map(t => t.plain_text).join('');
                const match = problemId.match(/^(.+)_(\d+)$/);
                
                if (match) {
                    const filePrefix = match[1];
                    
                    if (!seenFiles.has(filePrefix)) {
                        seenFiles.add(filePrefix);
                        sampleCount++;
                        
                        console.log(`\n[${sampleCount}] ${problemId}`);
                        
                        // 주요 필드 출력
                        const fields = [
                            '대단원', '중단원', '소단원', '난이도', '핵심개념',
                            '문제구조', '핵심패턴', '변형요소', '함정설계', '출제의도'
                        ];
                        
                        for (const field of fields) {
                            const prop = props[field];
                            if (prop) {
                                let value = '';
                                switch (prop.type) {
                                    case 'title':
                                        value = prop.title.map(t => t.plain_text).join('');
                                        break;
                                    case 'rich_text':
                                        value = prop.rich_text.map(t => t.plain_text).join('').substring(0, 50);
                                        break;
                                    case 'select':
                                        value = prop.select?.name || '';
                                        break;
                                    case 'number':
                                        value = prop.number;
                                        break;
                                    default:
                                        value = `[${prop.type}]`;
                                }
                                if (value) {
                                    console.log(`  ${field}: ${value}`);
                                }
                            }
                        }
                        console.log('-'.repeat(60));
                    }
                }
            }
        }

        console.log('\n✅ 분석 완료!');
        
    } catch (error) {
        console.error('\n❌ 오류 발생:', error.message);
        process.exit(1);
    }
}

getAllProblems();
