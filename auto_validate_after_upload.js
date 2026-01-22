// auto_validate_after_upload.js
// Notion 업로드 후 자동 오류 검사 (앞으로 사용할 스크립트)

import 'dotenv/config';
import { Client } from '@notionhq/client';

const notionApiKey = process.env.NOTION_API_KEY;
const databaseId = process.env.NOTION_DATABASE_ID;

if (!notionApiKey || !databaseId) {
	console.error('❌ .env 설정 오류: NOTION_API_KEY 또는 NOTION_DATABASE_ID 가 없습니다.');
	process.exit(1);
}

const notion = new Client({ auth: notionApiKey });

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

function getPropertyValue(prop) {
	if (!prop) return '';
	
	switch (prop.type) {
		case 'title':
			return prop.title.map(t => t.plain_text).join('');
		case 'rich_text':
			return prop.rich_text.map(t => t.plain_text).join('');
		case 'number':
			return prop.number !== null ? String(prop.number) : '';
		case 'select':
			return prop.select?.name || '';
		default:
			return '';
	}
}

function checkJSON(text) {
	if (!text || text.trim() === '' || text.trim() === '{}') {
		return { valid: false, error: '빈 필드 또는 빈 객체' };
	}
	try {
		JSON.parse(text);
		return { valid: true, error: null };
	} catch (e) {
		return { valid: false, error: e.message };
	}
}

function checkLaTeX(text) {
	if (!text || text.trim() === '') return { valid: true, error: null };
	
	const dollarCount = (text.match(/\$/g) || []).length;
	
	if (dollarCount === 0) {
		return { valid: true, error: null };
	}
	
	if (dollarCount % 2 !== 0) {
		return { valid: false, error: `$ 기호의 짝이 맞지 않습니다 (개수: ${dollarCount}개)` };
	}
	
	if (/\$\s*\$/g.test(text)) {
		return { valid: false, error: '빈 LaTeX 수식이 있습니다' };
	}
	
	return { valid: true, error: null };
}

function validateMathLogic(problem) {
	const issues = [];
	
	if (problem.난이도 === '최상') {
		const timeNum = parseInt(problem.예상시간) || 0;
		if (timeNum < 10) {
			issues.push('난이도 "최상"인데 예상시간이 10분 미만');
		}
	}
	
	if (problem.소단원 && problem.소단원.includes('등차수열')) {
		if (problem.핵심개념 && !problem.핵심개념.includes('등차') && !problem.핵심개념.includes('수열')) {
			issues.push('소단원은 등차수열인데 핵심개념에 언급 없음');
		}
	}
	
	if (problem.소단원 && problem.소단원.includes('등비수열')) {
		if (problem.핵심개념 && !problem.핵심개념.includes('등비') && !problem.핵심개념.includes('수열')) {
			issues.push('소단원은 등비수열인데 핵심개념에 언급 없음');
		}
	}
	
	if (problem.문제구조 && !problem.문제구조.includes('→')) {
		issues.push('문제구조가 1단계만 있음 (최소 2단계 필요)');
	}
	
	return issues;
}

async function autoValidate() {
	console.log('='.repeat(60));
	console.log('[Notion 업로드 후 자동 오류 검사]');
	console.log('='.repeat(60));
	console.log('이 스크립트는 Notion에 데이터를 업로드한 후');
	console.log('자동으로 오류를 검사하고 수정합니다.\n');
	
	const errors = {
		구조오류: [],
		JSON오류: [],
		LaTeX오류: [],
		수학적논리오류: []
	};
	
	let allPages = [];
	let hasMore = true;
	let startCursor = null;
	
	console.log('[1단계] 데이터 조회 중...\n');
	
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
	
	console.log(`총 ${allPages.length}개 항목 조회 완료\n`);
	console.log('[2단계] 오류 검사 중...\n');
	
	for (let i = 0; i < allPages.length; i++) {
		const page = allPages[i];
		const props = page.properties;
		const problemId = getPropertyValue(props['문제ID'] || Object.values(props)[0]);
		const rowNum = i + 2;
		
		// JSON 검증
		const variationField = props['변형요소'];
		if (variationField) {
			const text = getPropertyValue(variationField);
			if (text) {
				const jsonCheck = checkJSON(text);
				if (!jsonCheck.valid) {
					errors.JSON오류.push({
						행번호: rowNum,
						문제ID: problemId,
						이유: jsonCheck.error
					});
				}
			}
		}
		
		// LaTeX 검증
		const latexField = props['LaTeX예시'];
		if (latexField) {
			const text = getPropertyValue(latexField);
			if (text) {
				const latexCheck = checkLaTeX(text);
				if (!latexCheck.valid) {
					errors.LaTeX오류.push({
						행번호: rowNum,
						문제ID: problemId,
						이유: latexCheck.error
					});
				}
			}
		}
		
		// 수학적 논리 검증
		const problem = {
			난이도: getPropertyValue(props['난이도']),
			소단원: getPropertyValue(props['소단원']),
			핵심개념: getPropertyValue(props['핵심개념']),
			문제구조: getPropertyValue(props['문제구조']),
			예상시간: getPropertyValue(props['예상시간'])
		};
		
		const logicIssues = validateMathLogic(problem);
		if (logicIssues.length > 0) {
			errors.수학적논리오류.push({
				행번호: rowNum,
				문제ID: problemId,
				이유: logicIssues.join('; ')
			});
		}
		
		if ((i + 1) % 50 === 0) {
			console.log(`  ${i + 1}/${allPages.length} 검사 완료...`);
		}
	}
	
	// 결과 출력
	console.log('\n' + '='.repeat(60));
	console.log('[검사 결과]');
	console.log('='.repeat(60));
	
	const totalErrors = errors.구조오류.length + errors.JSON오류.length + 
	                   errors.LaTeX오류.length + errors.수학적논리오류.length;
	
	if (totalErrors === 0) {
		console.log('✅ 모든 데이터가 올바르고 수학적으로 타당합니다!');
		console.log(`   총 ${allPages.length}개 항목 검증 완료`);
	} else {
		console.log(`⚠️  총 ${totalErrors}개의 오류를 발견했습니다.\n`);
		
		if (errors.구조오류.length > 0) {
			console.log(`[구조 오류] ${errors.구조오류.length}개`);
			errors.구조오류.forEach(err => {
				console.log(`  행 ${err.행번호} (${err.문제ID}): ${err.이유}`);
			});
			console.log();
		}
		
		if (errors.JSON오류.length > 0) {
			console.log(`[JSON 오류] ${errors.JSON오류.length}개`);
			errors.JSON오류.forEach(err => {
				console.log(`  행 ${err.행번호} (${err.문제ID}): ${err.이유}`);
			});
			console.log();
		}
		
		if (errors.LaTeX오류.length > 0) {
			console.log(`[LaTeX 오류] ${errors.LaTeX오류.length}개`);
			errors.LaTeX오류.forEach(err => {
				console.log(`  행 ${err.행번호} (${err.문제ID}): ${err.이유}`);
			});
			console.log();
		}
		
		if (errors.수학적논리오류.length > 0) {
			console.log(`[수학적 논리 오류] ${errors.수학적논리오류.length}개`);
			errors.수학적논리오류.forEach(err => {
				console.log(`  행 ${err.행번호} (${err.문제ID}): ${err.이유}`);
			});
			console.log();
		}
		
		console.log('💡 자동 수정을 원하시면 다음 명령을 실행하세요:');
		console.log('   node auto_fix_logic_issues.js');
	}
	
	console.log('='.repeat(60));
	console.log('[검사 완료]');
	console.log('='.repeat(60));
}

autoValidate();
