// check_matching.js
// MathPDF 폴더와 노션 데이터베이스 간 매칭 가능 여부 확인

import 'dotenv/config';
import { Client, collectPaginatedAPI } from '@notionhq/client';
import { readdir } from 'fs/promises';
import { join } from 'path';

const notionApiKey = process.env.NOTION_API_KEY;
const databaseId = process.env.NOTION_DATABASE_ID;
const mathPdfPath = 'C:\\Users\\a\\Documents\\MathPDF\\organized';

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

async function checkMatching() {
    console.log('='.repeat(60));
    console.log('[MathPDF ↔ 노션 데이터베이스 매칭 확인]');
    console.log('='.repeat(60));
    console.log('');

    // 1. MathPDF 폴더 구조 확인
    console.log('📁 [1단계] MathPDF 폴더 구조 확인\n');
    
    const mathPdfFiles = {};
    
    try {
        const subjects = await readdir(mathPdfPath);
        
        for (const subject of subjects) {
            const subjectPath = join(mathPdfPath, subject);
            const files = await readdir(subjectPath);
            const pdfFiles = files.filter(f => f.endsWith('.pdf'));
            
            if (pdfFiles.length > 0) {
                mathPdfFiles[subject] = pdfFiles.sort();
                console.log(`  ${subject}/`);
                pdfFiles.forEach(f => console.log(`    - ${f}`));
            }
        }
    } catch (error) {
        console.error(`❌ MathPDF 폴더 읽기 오류: ${error.message}`);
        return;
    }

    console.log('\n');

    // 2. 노션 데이터베이스 문제ID 확인
    console.log('📋 [2단계] 노션 데이터베이스 문제ID 확인\n');
    
    const notionProblems = {};
    
    try {
        const allPages = [];
        let hasMore = true;
        let startCursor = null;

        while (hasMore) {
            await rateLimiter.waitIfNeeded();

            const response = await notion.databases.query({
                database_id: databaseId,
                start_cursor: startCursor || undefined,
                page_size: 100,
            });

            allPages.push(...response.results);
            hasMore = response.has_more;
            startCursor = response.next_cursor;
        }

        console.log(`  총 ${allPages.length}개 문제 조회 완료\n`);

        // 문제ID에서 파일명 추출
        for (const page of allPages) {
            const props = page.properties;
            const problemIdProp = props['문제ID'];
            
            if (problemIdProp && problemIdProp.type === 'title') {
                const problemId = problemIdProp.title.map(t => t.plain_text).join('');
                
                // 문제ID 형식: 수1_2025학년도_현우진_드릴_P1_15
                const match = problemId.match(/^(.+)_(\d+)$/);
                if (match) {
                    const filePrefix = match[1]; // 수1_2025학년도_현우진_드릴_P1
                    const problemNum = parseInt(match[2]);
                    
                    if (!notionProblems[filePrefix]) {
                        notionProblems[filePrefix] = [];
                    }
                    notionProblems[filePrefix].push(problemNum);
                }
            }
        }

        // 파일명별로 정리
        for (const [filePrefix, problemNums] of Object.entries(notionProblems)) {
            problemNums.sort((a, b) => a - b);
            const expectedFileName = filePrefix + '.pdf';
            console.log(`  ${expectedFileName}: ${problemNums.length}개 문제 (${problemNums[0]}~${problemNums[problemNums.length-1]}번)`);
        }

    } catch (error) {
        console.error(`❌ 노션 데이터 조회 오류: ${error.message}`);
        return;
    }

    console.log('\n');

    // 3. 매칭 확인
    console.log('🔍 [3단계] 매칭 가능 여부 확인\n');
    console.log('='.repeat(60));

    let matchCount = 0;
    let mismatchCount = 0;
    const mismatches = [];

    // MathPDF 파일과 노션 문제ID 비교
    for (const [subject, pdfFiles] of Object.entries(mathPdfFiles)) {
        for (const pdfFile of pdfFiles) {
            // PDF 파일명에서 확장자 제거
            const pdfBaseName = pdfFile.replace('.pdf', '');
            
            // 노션에서 해당 파일명 찾기
            const notionFilePrefix = pdfBaseName;
            const notionProblemsForFile = notionProblems[notionFilePrefix];
            
            if (notionProblemsForFile && notionProblemsForFile.length > 0) {
                matchCount++;
                console.log(`✅ ${subject}/${pdfFile}`);
                console.log(`   → 노션: ${notionProblemsForFile.length}개 문제 매칭됨`);
            } else {
                mismatchCount++;
                mismatches.push(`${subject}/${pdfFile}`);
                console.log(`❌ ${subject}/${pdfFile}`);
                console.log(`   → 노션: 매칭되는 문제 없음`);
            }
            console.log('');
        }
    }

    // 노션에만 있는 파일 확인
    const mathPdfFileSet = new Set();
    for (const [subject, pdfFiles] of Object.entries(mathPdfFiles)) {
        for (const pdfFile of pdfFiles) {
            mathPdfFileSet.add(pdfFile.replace('.pdf', ''));
        }
    }

    const notionOnly = [];
    for (const filePrefix of Object.keys(notionProblems)) {
        if (!mathPdfFileSet.has(filePrefix)) {
            notionOnly.push(filePrefix);
        }
    }

    console.log('\n');
    console.log('='.repeat(60));
    console.log('📊 매칭 결과 요약');
    console.log('='.repeat(60));
    console.log(`✅ 매칭 성공: ${matchCount}개 파일`);
    console.log(`❌ 매칭 실패: ${mismatchCount}개 파일`);
    
    if (mismatches.length > 0) {
        console.log(`\n⚠️  MathPDF에 있지만 노션에 없는 파일:`);
        mismatches.forEach(f => console.log(`   - ${f}`));
    }
    
    if (notionOnly.length > 0) {
        console.log(`\n⚠️  노션에 있지만 MathPDF에 없는 파일:`);
        notionOnly.forEach(f => console.log(`   - ${f}.pdf`));
    }

    console.log('\n');

    // 4. 매칭 가능 여부 결론
    console.log('='.repeat(60));
    console.log('💡 결론');
    console.log('='.repeat(60));
    
    if (matchCount > 0 && mismatchCount === 0 && notionOnly.length === 0) {
        console.log('✅ 완벽하게 매칭됩니다!');
        console.log('   - 모든 PDF 파일이 노션 데이터베이스와 연결 가능');
        console.log('   - 문제ID 형식: [파일명]_[문제번호]');
        console.log('   - 예: 수1_2025학년도_현우진_드릴_P1.pdf → 수1_2025학년도_현우진_드릴_P1_15');
    } else if (matchCount > 0) {
        console.log('⚠️  부분적으로 매칭됩니다.');
        console.log('   - 일부 파일은 매칭 가능');
        console.log('   - 문제ID 형식이 일치하는 파일만 자동 매칭 가능');
    } else {
        console.log('❌ 매칭이 어렵습니다.');
        console.log('   - 파일명 형식이 다르거나 문제ID 규칙이 일치하지 않음');
    }

    console.log('\n');
    console.log('📝 매칭 규칙:');
    console.log('   PDF 파일명: [과목]_[교재명]_[파트].pdf');
    console.log('   노션 문제ID: [파일명]_[문제번호]');
    console.log('   예: 수1_2025학년도_현우진_드릴_P1.pdf');
    console.log('       → 수1_2025학년도_현우진_드릴_P1_01, P1_02, ..., P1_15');
}

checkMatching();
