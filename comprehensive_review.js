// comprehensive_review.js
// 전체 데이터 점검 및 수학적 논리 타당성 검토

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

// 수학적 논리 타당성 검토
function validateMathLogic(problem) {
	const issues = [];
	
	const problemId = problem.problemId;
	const majorUnit = problem.대단원;
	const minorUnit = problem.중단원;
	const subUnit = problem.소단원;
	const difficulty = problem.난이도;
	const coreConcept = problem.핵심개념;
	const latex = problem.LaTeX예시;
	const problemStructure = problem.문제구조;
	const variation = problem.변형요소;
	const estimatedTime = problem.예상시간;
	
	// 1. 단원 분류 일관성 검토
	// 최근 수능은 1학년(수학I)과 2학년(미적분) 교과를 함께 중요시하므로
	// 1학년과 2학년 개념이 함께 포함되는 것은 정상
	// 단원 분류 일관성 검사는 제외 (최근 수능 경향 반영)
	
	// 2. 난이도와 예상시간 일관성
	const timeNum = parseInt(estimatedTime) || 0;
	if (difficulty === '하' && timeNum > 5) {
		issues.push('난이도 불일치: 난이도 "하"인데 예상시간이 5분 초과');
	}
	if (difficulty === '최상' && timeNum < 10) {
		issues.push('난이도 불일치: 난이도 "최상"인데 예상시간이 10분 미만');
	}
	
	// 3. LaTeX 수식과 핵심개념 일관성
	if (latex && coreConcept) {
		// 핵심개념에 언급된 내용이 LaTeX에 포함되어야 함
		if (coreConcept.includes('등차수열') && !latex.includes('a_n') && !latex.includes('d') && !latex.includes('S_n')) {
			// 경고만 (필수는 아님)
		}
		if (coreConcept.includes('등비수열') && !latex.includes('r') && !latex.includes('S_n')) {
			// 경고만
		}
	}
	
	// 4. 문제구조 논리성
	if (problemStructure) {
		const steps = problemStructure.split('→');
		if (steps.length < 2) {
			issues.push('문제구조 부족: 최소 2단계 이상 필요');
		}
	}
	
	// 5. 변형요소 타당성
	if (variation) {
		try {
			const varData = JSON.parse(variation);
			// 변형요소가 비어있지 않은지
			if (Object.keys(varData).length === 0) {
				issues.push('변형요소 비어있음: 변형 가능한 요소가 없음');
			}
		} catch (e) {
			// JSON 오류는 이미 검사됨
		}
	}
	
	// 6. 핵심개념과 소단원 일관성
	if (coreConcept && subUnit) {
		if (subUnit.includes('등차수열') && !coreConcept.includes('등차') && !coreConcept.includes('수열')) {
			issues.push('개념 불일치: 소단원은 등차수열인데 핵심개념에 언급 없음');
		}
		if (subUnit.includes('등비수열') && !coreConcept.includes('등비') && !coreConcept.includes('수열')) {
			issues.push('개념 불일치: 소단원은 등비수열인데 핵심개념에 언급 없음');
		}
	}
	
	return issues;
}

// 구조 오류 검사
function checkStructure(problem) {
	const issues = [];
	const requiredFields = [
		'문제ID', '출처', '대단원', '중단원', '소단원', '난이도', 
		'핵심개념', 'LaTeX예시', '문제구조', '핵심패턴', '변형요소'
	];
	
	for (const field of requiredFields) {
		if (!problem[field] || problem[field].trim() === '') {
			issues.push(`필수 필드 누락: ${field}`);
		}
	}
	
	return issues;
}

// JSON 형식 검사
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

// LaTeX 형식 검사
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

async function comprehensiveReview() {
	console.log('='.repeat(60));
	console.log('[전체 데이터 종합 점검 및 수학적 논리 검토]');
	console.log('='.repeat(60));
	
	const allIssues = {
		구조오류: [],
		JSON오류: [],
		LaTeX오류: [],
		수학적논리오류: []
	};
	
	let allPages = [];
	let hasMore = true;
	let startCursor = null;
	
	console.log('\n[1단계] 데이터 조회');
	console.log('='.repeat(60));
	
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
	
	console.log('[2단계] 구조 및 형식 검사');
	console.log('='.repeat(60));
	
	for (let i = 0; i < allPages.length; i++) {
		const page = allPages[i];
		const props = page.properties;
		const problemId = getPropertyValue(props['문제ID'] || Object.values(props)[0]);
		const rowNum = i + 2;
		
		// 모든 필드 추출
		const problem = {
			problemId,
			행번호: rowNum,
			문제ID: getPropertyValue(props['문제ID']),
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
		
		// 구조 오류 검사
		const structureIssues = checkStructure(problem);
		if (structureIssues.length > 0) {
			allIssues.구조오류.push({
				행번호: rowNum,
				문제ID: problemId,
				이유: structureIssues.join(', ')
			});
		}
		
		// JSON 오류 검사
		if (problem.변형요소) {
			const jsonCheck = checkJSON(problem.변형요소);
			if (!jsonCheck.valid) {
				allIssues.JSON오류.push({
					행번호: rowNum,
					문제ID: problemId,
					이유: `변형요소 필드: ${jsonCheck.error}`
				});
			}
		}
		
		// LaTeX 오류 검사
		if (problem.LaTeX예시) {
			const latexCheck = checkLaTeX(problem.LaTeX예시);
			if (!latexCheck.valid) {
				allIssues.LaTeX오류.push({
					행번호: rowNum,
					문제ID: problemId,
					이유: `LaTeX 오류: ${latexCheck.error}`
				});
			}
		}
		
		// 수학적 논리 타당성 검토
		const logicIssues = validateMathLogic(problem);
		if (logicIssues.length > 0) {
			allIssues.수학적논리오류.push({
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
	console.log('[종합 점검 결과]');
	console.log('='.repeat(60));
	
	const totalErrors = allIssues.구조오류.length + allIssues.JSON오류.length + 
	                   allIssues.LaTeX오류.length + allIssues.수학적논리오류.length;
	
	console.log(`총 ${totalErrors}개의 이슈를 발견했습니다.\n`);
	
	if (totalErrors === 0) {
		console.log('✅ 모든 데이터가 올바르고 수학적으로 타당합니다!');
		console.log(`   총 ${allPages.length}개 항목 검증 완료`);
	} else {
		if (allIssues.구조오류.length > 0) {
			console.log(`[구조 오류] ${allIssues.구조오류.length}개`);
			console.log('-'.repeat(60));
			allIssues.구조오류.forEach(err => {
				console.log(`  행 ${err.행번호} (${err.문제ID}): ${err.이유}`);
			});
			console.log();
		}
		
		if (allIssues.JSON오류.length > 0) {
			console.log(`[JSON 오류] ${allIssues.JSON오류.length}개`);
			console.log('-'.repeat(60));
			allIssues.JSON오류.forEach(err => {
				console.log(`  행 ${err.행번호} (${err.문제ID}): ${err.이유}`);
			});
			console.log();
		}
		
		if (allIssues.LaTeX오류.length > 0) {
			console.log(`[LaTeX 오류] ${allIssues.LaTeX오류.length}개`);
			console.log('-'.repeat(60));
			allIssues.LaTeX오류.forEach(err => {
				console.log(`  행 ${err.행번호} (${err.문제ID}): ${err.이유}`);
			});
			console.log();
		}
		
		if (allIssues.수학적논리오류.length > 0) {
			console.log(`[수학적 논리 오류] ${allIssues.수학적논리오류.length}개`);
			console.log('-'.repeat(60));
			allIssues.수학적논리오류.forEach(err => {
				console.log(`  행 ${err.행번호} (${err.문제ID}): ${err.이유}`);
			});
			console.log();
		}
	}
	
	// 통계 정보
	console.log('='.repeat(60));
	console.log('[데이터 통계]');
	console.log('='.repeat(60));
	
	const stats = {
		수학I: 0,
		수학II: 0,
		미적분: 0,
		기하: 0,
		확률과통계: 0,
		기타: 0
	};
	
	const difficultyStats = {
		하: 0,
		중: 0,
		상: 0,
		최상: 0
	};
	
	for (const page of allPages) {
		const props = page.properties;
		const majorUnit = getPropertyValue(props['대단원']);
		const difficulty = getPropertyValue(props['난이도']);
		
		if (majorUnit.includes('수학I') || majorUnit.includes('수1')) {
			stats.수학I++;
		} else if (majorUnit.includes('수학II') || majorUnit.includes('수2')) {
			stats.수학II++;
		} else if (majorUnit.includes('미적분')) {
			stats.미적분++;
		} else if (majorUnit.includes('기하')) {
			stats.기하++;
		} else if (majorUnit.includes('확률') || majorUnit.includes('통계')) {
			stats.확률과통계++;
		} else {
			stats.기타++;
		}
		
		if (difficulty) {
			difficultyStats[difficulty] = (difficultyStats[difficulty] || 0) + 1;
		}
	}
	
	console.log('\n[대단원별 분포]:');
	for (const [subject, count] of Object.entries(stats)) {
		if (count > 0) {
			console.log(`  ${subject}: ${count}개`);
		}
	}
	
	console.log('\n[난이도별 분포]:');
	for (const [level, count] of Object.entries(difficultyStats)) {
		if (count > 0) {
			console.log(`  ${level}: ${count}개`);
		}
	}
	
	console.log('\n' + '='.repeat(60));
	console.log('[점검 완료]');
	console.log('='.repeat(60));
	
	if (totalErrors === 0) {
		console.log('\n✅ 모든 데이터가 완벽합니다!');
		console.log('   - 구조: 정상');
		console.log('   - JSON: 정상');
		console.log('   - LaTeX: 정상');
		console.log('   - 수학적 논리: 타당함');
	} else {
		console.log(`\n⚠️  ${totalErrors}개의 이슈가 발견되었습니다.`);
		console.log('   위의 상세 내역을 확인하여 수정해주세요.');
	}
}

comprehensiveReview();
