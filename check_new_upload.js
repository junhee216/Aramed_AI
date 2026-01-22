// check_new_upload.js
// 새로 업로드된 미적분 데이터 검토

import 'dotenv/config';
import { Client } from '@notionhq/client';

const notionApiKey = process.env.NOTION_API_KEY;
const databaseId = process.env.NOTION_DATABASE_ID;

if (!notionApiKey || !databaseId) {
	console.error('❌ .env 설정 오류');
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
		case 'multi_select':
			return prop.multi_select.map(s => s.name).join(', ');
		default:
			return '';
	}
}

function checkJSON(text) {
	if (!text || text.trim() === '' || text.trim() === '{}') {
		return { valid: false, error: '빈 필드 또는 빈 객체' };
	}
	try {
		const parsed = JSON.parse(text);
		if (typeof parsed !== 'object' || Array.isArray(parsed)) {
			return { valid: false, error: 'JSON이 객체가 아닙니다' };
		}
		return { valid: true, error: null, parsed };
	} catch (e) {
		return { valid: false, error: e.message };
	}
}

function checkLaTeX(text) {
	if (!text || text.trim() === '') return { valid: true, error: null, issues: [] };
	
	const issues = [];
	const dollarCount = (text.match(/\$/g) || []).length;
	
	if (dollarCount > 0 && dollarCount % 2 !== 0) {
		issues.push(`$ 기호의 짝이 맞지 않습니다 (개수: ${dollarCount}개)`);
	}
	
	if (/\$\s*\$/g.test(text)) {
		issues.push('빈 LaTeX 수식이 있습니다');
	}
	
	// 수식 내부에 닫히지 않은 괄호 확인
	const mathBlocks = text.match(/\$[^$]+\$/g) || [];
	for (const block of mathBlocks) {
		const openParen = (block.match(/\(/g) || []).length;
		const closeParen = (block.match(/\)/g) || []).length;
		const openBrace = (block.match(/\{/g) || []).length;
		const closeBrace = (block.match(/\}/g) || []).length;
		
		if (openParen !== closeParen) {
			issues.push(`수식 내 괄호 불일치: ( ${openParen}개, ) ${closeParen}개`);
		}
		if (openBrace !== closeBrace) {
			issues.push(`수식 내 중괄호 불일치: { ${openBrace}개, } ${closeBrace}개`);
		}
	}
	
	return { valid: issues.length === 0, error: issues.length > 0 ? issues.join('; ') : null, issues };
}

function validateMathLogic(problem) {
	const issues = [];
	const warnings = [];
	
	// 최근 수능은 1학년(수학I)과 2학년(미적분) 교과를 함께 중요시하므로
	// 1학년과 2학년 개념이 함께 포함되는 것은 정상
	// 단원 분류 일관성 검사는 제외
	
	// 1. 난이도와 예상시간 일관성
	if (problem.난이도 && problem.예상시간) {
		const timeNum = parseInt(problem.예상시간) || 0;
		if (problem.난이도 === '하' && timeNum > 5) {
			warnings.push('난이도 "하"인데 예상시간이 5분 초과 (일반적으로 3-5분)');
		}
		if (problem.난이도 === '중' && (timeNum < 3 || timeNum > 10)) {
			warnings.push(`난이도 "중"인데 예상시간이 ${timeNum}분 (일반적으로 5-8분)`);
		}
		if (problem.난이도 === '상' && timeNum < 5) {
			warnings.push('난이도 "상"인데 예상시간이 5분 미만 (일반적으로 8-12분)');
		}
		if (problem.난이도 === '최상' && timeNum < 10) {
			issues.push('난이도 "최상"인데 예상시간이 10분 미만 (일반적으로 12-20분)');
		}
	}
	
	// 2. 핵심개념과 소단원 일관성
	if (problem.소단원 && problem.핵심개념) {
		if (problem.소단원.includes('등차수열') && !problem.핵심개념.includes('등차') && !problem.핵심개념.includes('수열')) {
			warnings.push('소단원은 등차수열인데 핵심개념에 언급 없음');
		}
		if (problem.소단원.includes('등비수열') && !problem.핵심개념.includes('등비') && !problem.핵심개념.includes('수열')) {
			warnings.push('소단원은 등비수열인데 핵심개념에 언급 없음');
		}
		if (problem.소단원.includes('미분') && !problem.핵심개념.includes('미분')) {
			warnings.push('소단원에 미분이 있는데 핵심개념에 미분 언급 없음');
		}
		if (problem.소단원.includes('적분') && !problem.핵심개념.includes('적분')) {
			warnings.push('소단원에 적분이 있는데 핵심개념에 적분 언급 없음');
		}
	}
	
	// 3. 문제구조 논리성
	if (problem.문제구조) {
		const steps = problem.문제구조.split('→').map(s => s.trim()).filter(s => s);
		if (steps.length < 2) {
			issues.push('문제구조가 1단계만 있음 (최소 2단계 필요)');
		}
		if (steps.length > 6) {
			warnings.push(`문제구조가 ${steps.length}단계로 너무 복잡함 (일반적으로 3-5단계)`);
		}
	}
	
	// 4. LaTeX와 핵심개념 일관성
	if (problem.LaTeX예시 && problem.핵심개념) {
		if (problem.핵심개념.includes('미분') && !problem.LaTeX예시.includes('\\frac') && !problem.LaTeX예시.includes('d') && !problem.LaTeX예시.includes('\\prime')) {
			warnings.push('핵심개념에 미분이 있는데 LaTeX에 미분 기호 없음');
		}
		if (problem.핵심개념.includes('적분') && !problem.LaTeX예시.includes('\\int')) {
			warnings.push('핵심개념에 적분이 있는데 LaTeX에 적분 기호 없음');
		}
	}
	
	// 5. 변형요소 타당성
	if (problem.변형요소) {
		const jsonCheck = checkJSON(problem.변형요소);
		if (jsonCheck.valid && jsonCheck.parsed) {
			const keys = Object.keys(jsonCheck.parsed);
			if (keys.length === 0) {
				issues.push('변형요소가 빈 객체입니다');
			}
		}
	}
	
	return { issues, warnings };
}

async function checkNewUpload() {
	console.log('='.repeat(70));
	console.log('[새로 업로드된 미적분 데이터 검토]');
	console.log('='.repeat(70));
	
	let allPages = [];
	let hasMore = true;
	let startCursor = null;
	
	console.log('\n[1단계] 데이터 조회 중...\n');
	
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
	
	// 새로 업로드된 항목 필터링 (미적분_2025학년도_현우진_드릴_P3)
	const newItems = allPages.filter(page => {
		const props = page.properties;
		const problemId = getPropertyValue(props['문제ID'] || Object.values(props)[0]);
		return problemId && problemId.includes('미적분_2025학년도_현우진_드릴_P3');
	});
	
	if (newItems.length === 0) {
		console.log('⚠️  "미적분_2025학년도_현우진_드릴_P3"로 시작하는 항목을 찾을 수 없습니다.');
		console.log('전체 데이터베이스를 검토합니다...\n');
		// 전체 검토로 전환
	} else {
		console.log(`✅ 새로 업로드된 항목 ${newItems.length}개 발견\n`);
	}
	
	const itemsToReview = newItems.length > 0 ? newItems : allPages;
	
	console.log(`[2단계] ${itemsToReview.length}개 항목 검토 중...\n`);
	
	const results = {
		구조오류: [],
		JSON오류: [],
		LaTeX오류: [],
		수학적논리오류: [],
		경고: []
	};
	
	for (let i = 0; i < itemsToReview.length; i++) {
		const page = itemsToReview[i];
		const props = page.properties;
		const problemId = getPropertyValue(props['문제ID'] || Object.values(props)[0]);
		const rowNum = i + 2;
		
		const problem = {
			문제ID: problemId,
			행번호: rowNum,
			출처: getPropertyValue(props['출처']),
			대단원: getPropertyValue(props['대단원']),
			중단원: getPropertyValue(props['중단원']),
			소단원: getPropertyValue(props['소단원']),
			난이도: getPropertyValue(props['난이도']),
			핵심개념: getPropertyValue(props['핵심개념']),
			LaTeX예시: getPropertyValue(props['LaTeX예시']),
			문제구조: getPropertyValue(props['문제구조']),
			핵심패턴: getPropertyValue(props['핵심패턴']),
			변형요소: getPropertyValue(props['변형요소']),
			난이도조절: getPropertyValue(props['난이도조절']),
			함정설계: getPropertyValue(props['함정설계']),
			출제의도: getPropertyValue(props['출제의도']),
			예상시간: getPropertyValue(props['예상시간'])
		};
		
		// JSON 검사
		if (problem.변형요소) {
			const jsonCheck = checkJSON(problem.변형요소);
			if (!jsonCheck.valid) {
				results.JSON오류.push({
					행번호: rowNum,
					문제ID: problemId,
					이유: jsonCheck.error
				});
			}
		}
		
		// LaTeX 검사
		if (problem.LaTeX예시) {
			const latexCheck = checkLaTeX(problem.LaTeX예시);
			if (!latexCheck.valid) {
				results.LaTeX오류.push({
					행번호: rowNum,
					문제ID: problemId,
					이유: latexCheck.error
				});
			}
		}
		
		// 수학적 논리 검토
		const logicCheck = validateMathLogic(problem);
		if (logicCheck.issues.length > 0) {
			results.수학적논리오류.push({
				행번호: rowNum,
				문제ID: problemId,
				이유: logicCheck.issues.join('; ')
			});
		}
		if (logicCheck.warnings.length > 0) {
			results.경고.push({
				행번호: rowNum,
				문제ID: problemId,
				이유: logicCheck.warnings.join('; ')
			});
		}
		
		if ((i + 1) % 20 === 0) {
			console.log(`  ${i + 1}/${itemsToReview.length} 검사 완료...`);
		}
	}
	
	// 결과 출력
	console.log('\n' + '='.repeat(70));
	console.log('[검토 결과]');
	console.log('='.repeat(70));
	
	const totalErrors = results.구조오류.length + results.JSON오류.length + 
	                   results.LaTeX오류.length + results.수학적논리오류.length;
	
	if (totalErrors === 0) {
		console.log('✅ 모든 데이터가 올바르고 수학적으로 타당합니다!');
		console.log(`   총 ${itemsToReview.length}개 항목 검증 완료\n`);
		
		if (results.경고.length > 0) {
			console.log(`💡 참고사항 (경고): ${results.경고.length}개\n`);
			results.경고.forEach(warn => {
				console.log(`  행 ${warn.행번호} (${warn.문제ID}): ${warn.이유}`);
			});
			console.log();
		}
	} else {
		console.log(`⚠️  총 ${totalErrors}개의 오류를 발견했습니다.\n`);
		
		if (results.JSON오류.length > 0) {
			console.log(`[JSON 오류] ${results.JSON오류.length}개`);
			console.log('-'.repeat(70));
			results.JSON오류.forEach(err => {
				console.log(`  행 ${err.행번호} (${err.문제ID}): ${err.이유}`);
			});
			console.log();
		}
		
		if (results.LaTeX오류.length > 0) {
			console.log(`[LaTeX 오류] ${results.LaTeX오류.length}개`);
			console.log('-'.repeat(70));
			results.LaTeX오류.forEach(err => {
				console.log(`  행 ${err.행번호} (${err.문제ID}): ${err.이유}`);
			});
			console.log();
		}
		
		if (results.수학적논리오류.length > 0) {
			console.log(`[수학적 논리 오류] ${results.수학적논리오류.length}개`);
			console.log('-'.repeat(70));
			results.수학적논리오류.forEach(err => {
				console.log(`  행 ${err.행번호} (${err.문제ID}): ${err.이유}`);
			});
			console.log();
		}
		
		if (results.경고.length > 0) {
			console.log(`[경고] ${results.경고.length}개 (수정 권장)`);
			console.log('-'.repeat(70));
			results.경고.forEach(warn => {
				console.log(`  행 ${warn.행번호} (${warn.문제ID}): ${warn.이유}`);
			});
			console.log();
		}
	}
	
	// 통계 정보
	if (newItems.length > 0) {
		console.log('='.repeat(70));
		console.log('[새로 업로드된 항목 통계]');
		console.log('='.repeat(70));
		
		const stats = {
			난이도: {},
			중단원: {}
		};
		
		for (const page of newItems) {
			const props = page.properties;
			const difficulty = getPropertyValue(props['난이도']);
			const minorUnit = getPropertyValue(props['중단원']);
			
			stats.난이도[difficulty] = (stats.난이도[difficulty] || 0) + 1;
			stats.중단원[minorUnit] = (stats.중단원[minorUnit] || 0) + 1;
		}
		
		console.log('\n[난이도별 분포]:');
		for (const [level, count] of Object.entries(stats.난이도)) {
			console.log(`  ${level}: ${count}개`);
		}
		
		console.log('\n[중단원별 분포]:');
		for (const [unit, count] of Object.entries(stats.중단원)) {
			console.log(`  ${unit}: ${count}개`);
		}
	}
	
	console.log('\n' + '='.repeat(70));
	console.log('[검토 완료]');
	console.log('='.repeat(70));
}

checkNewUpload();
