// comprehensive_notion_review.js
// 전체 노션 데이터베이스 종합 검토 (문제-해설-27개 필드 일관성 확인)

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
		case 'date':
			return prop.date;
		case 'checkbox':
			return prop.checkbox;
		case 'url':
			return prop.url;
		default:
			return null;
	}
}

// LaTeX 수식 괄호 검사
function checkLaTeXSyntax(text) {
	if (!text) return { valid: true, errors: [] };
	
	const errors = [];
	
	// 달러 기호 개수 확인
	const dollarCount = (text.match(/\$/g) || []).length;
	if (dollarCount % 2 !== 0) {
		errors.push(`LaTeX 수식 괄호 불일치 (달러 기호 ${dollarCount}개)`);
	}
	
	// 중괄호 확인 (단, \로 이스케이프된 것은 제외)
	const openBraces = (text.match(/(?<!\\)\{/g) || []).length;
	const closeBraces = (text.match(/(?<!\\)\}/g) || []).length;
	if (openBraces !== closeBraces) {
		errors.push(`LaTeX 중괄호 불일치 (열림: ${openBraces}, 닫힘: ${closeBraces})`);
	}
	
	// 수식 환경 확인
	const beginMath = (text.match(/\\begin\{equation\}/g) || []).length;
	const endMath = (text.match(/\\end\{equation\}/g) || []).length;
	if (beginMath !== endMath) {
		errors.push(`LaTeX 수식 환경 불일치 (begin: ${beginMath}, end: ${endMath})`);
	}
	
	return {
		valid: errors.length === 0,
		errors: errors
	};
}

// 주제 일관성 검사
function checkTopicConsistency(대단원, 중단원, 소단원, 핵심개념, 문제구조) {
	const errors = [];
	const warnings = [];
	
	// 대단원과 중단원 일관성
	if (대단원 && 중단원) {
		const validCombinations = {
			'수1': ['집합과 명제', '함수', '수열', '지수와 로그', '삼각함수'],
			'수2': ['함수의 극한과 연속', '미분', '적분'],
			'미적분': ['수열의 극한', '미분법', '적분법'],
			'확률과 통계': ['경우의 수', '확률', '통계']
		};
		
		if (validCombinations[대단원] && !validCombinations[대단원].includes(중단원)) {
			warnings.push(`대단원(${대단원})과 중단원(${중단원}) 불일치 가능성`);
		}
	}
	
	// 핵심개념과 주제 일관성
	if (핵심개념 && 중단원) {
		const conceptTopicMap = {
			'경우의 수': ['순열', '조합', '원순열', '중복조합', '이웃', '여사건'],
			'미분': ['도함수', '미분가능', '접선', '극값', '변곡점'],
			'적분': ['정적분', '넓이', '부정적분', '치환적분'],
			'함수의 극한과 연속': ['극한', '연속', '불연속']
		};
		
		const relevantConcepts = conceptTopicMap[중단원] || [];
		if (relevantConcepts.length > 0) {
			const hasRelevantConcept = relevantConcepts.some(concept => 핵심개념.includes(concept));
			if (!hasRelevantConcept) {
				warnings.push(`핵심개념이 중단원(${중단원})과 관련성이 낮을 수 있음`);
			}
		}
	}
	
	return { errors, warnings };
}

// 문제-해설 일관성 검사
function checkProblemSolutionConsistency(문제, 해설, 문제구조, 핵심개념) {
	const errors = [];
	const warnings = [];
	
	if (!문제 || !해설) {
		return { errors, warnings };
	}
	
	// 문제에 언급된 개념이 해설에 포함되는지 확인
	const problemConcepts = [];
	if (문제.includes('미분가능')) problemConcepts.push('미분가능');
	if (문제.includes('연속')) problemConcepts.push('연속');
	if (문제.includes('극한')) problemConcepts.push('극한');
	if (문제.includes('적분')) problemConcepts.push('적분');
	if (문제.includes('삼차함수')) problemConcepts.push('삼차함수');
	if (문제.includes('합성함수')) problemConcepts.push('합성함수');
	if (문제.includes('경우의 수')) problemConcepts.push('경우의 수');
	if (문제.includes('순열')) problemConcepts.push('순열');
	if (문제.includes('조합')) problemConcepts.push('조합');
	
	const solutionText = 해설.join(' ') || 해설;
	
	for (const concept of problemConcepts) {
		if (!solutionText.includes(concept) && !solutionText.includes(concept.replace('함수', ''))) {
			warnings.push(`문제에 언급된 개념 "${concept}"이 해설에 명시적으로 다뤄지지 않음`);
		}
	}
	
	// 핵심개념이 해설에 포함되는지 확인
	if (핵심개념 && solutionText) {
		const 핵심개념List = 핵심개념.split(/[,;]/).map(c => c.trim());
		for (const concept of 핵심개념List) {
			if (concept && !solutionText.includes(concept)) {
				warnings.push(`핵심개념 "${concept}"이 해설에 명시적으로 다뤄지지 않음`);
			}
		}
	}
	
	return { errors, warnings };
}

// 필수 필드 완전성 검사
function checkRequiredFields(page) {
	const props = page.properties;
	const errors = [];
	const warnings = [];
	
	// 필수 필드 목록
	const requiredFields = [
		'문제ID', '대단원', '중단원', '핵심개념', '문제구조', 
		'난이도', '예상시간', '출제의도', '선행개념'
	];
	
	for (const field of requiredFields) {
		const value = extractPropertyValue(props[field]);
		if (!value || (typeof value === 'string' && value.trim() === '')) {
			warnings.push(`필수 필드 "${field}" 비어있음`);
		}
	}
	
	// 해설 관련 필드 확인 (실제 필드명 사용)
	const 해설Fields = ['개념연결', '후행개념', '선행개념', '핵심개념'];
	const has해설 = 해설Fields.some(field => {
		const value = extractPropertyValue(props[field]);
		return value && typeof value === 'string' && value.trim() !== '';
	});
	
	if (!has해설) {
		warnings.push('개념 관련 필드가 모두 비어있음');
	}
	
	return { errors, warnings };
}

// 수학적 논리 검사
function checkMathLogic(문제, 해설, 핵심개념, 문제구조) {
	const errors = [];
	const warnings = [];
	
	if (!문제) return { errors, warnings };
	
	const allText = (문제 + ' ' + (Array.isArray(해설) ? 해설.join(' ') : 해설 || '')).toLowerCase();
	
	// 극한 관련
	if (문제.includes('\\lim') || 문제.includes('극한')) {
		if (문제.includes('\\frac') && 문제.includes('0')) {
			if (!allText.includes('인수분해') && !allText.includes('로피탈')) {
				warnings.push('0/0 꼴 극한에서 인수분해나 로피탈 법칙 언급 없음');
			}
		}
	}
	
	// 미분가능성 관련
	if (문제.includes('미분가능')) {
		if (문제.includes('\\begin{cases}')) {
			if (!allText.includes('연속') && !allText.includes('미분계수')) {
				warnings.push('구간별 함수의 미분가능성에서 연속성과 미분계수 일치 확인 언급 없음');
			}
		}
	}
	
	// 삼차함수 비율 관계
	if (문제.includes('삼차함수') && (문제.includes('비율') || 핵심개념?.includes('비율'))) {
		if (!allText.includes('2:1') && !allText.includes('1:2') && !allText.includes('√3')) {
			warnings.push('삼차함수 비율 관계에서 구체적 수치(2:1, 1:2, √3) 언급 없음');
		}
	}
	
	// 적분과 넓이
	if (문제.includes('\\int') && 문제.includes('넓이')) {
		if (!allText.includes('정적분') && !allText.includes('넓이')) {
			warnings.push('적분과 넓이 문제에서 정적분과 넓이의 관계 언급 없음');
		}
	}
	
	// 확통 관련
	if (문제.includes('경우의 수') || 문제.includes('순열') || 문제.includes('조합')) {
		if (문제.includes('원형') || 문제.includes('원순열')) {
			if (!allText.includes('회전') && !allText.includes('원순열')) {
				warnings.push('원순열 문제에서 회전하여 일치하는 것은 같은 것으로 본다는 언급 없음');
			}
		}
		if (문제.includes('이웃') || 문제.includes('이웃하지')) {
			if (!allText.includes('이웃') && !allText.includes('여사건')) {
				warnings.push('이웃하는 것/이웃하지 않는 것 문제에서 계산 원칙 언급 없음');
			}
		}
		if (문제.includes('부정방정식') || 문제.includes('음이 아닌 정수')) {
			if (!allText.includes('중복조합') && !allText.includes('H_')) {
				warnings.push('부정방정식 문제에서 중복조합 언급 없음');
			}
		}
	}
	
	return { errors, warnings };
}

// 필드 간 상호 참조 일관성 검사
function checkFieldConsistency(page) {
	const props = page.properties;
	const errors = [];
	const warnings = [];
	
	const 문제ID = extractPropertyValue(props['문제ID']);
	const 대단원 = extractPropertyValue(props['대단원']);
	const 중단원 = extractPropertyValue(props['중단원']);
	const 핵심개념 = extractPropertyValue(props['핵심개념']);
	const 유사유형 = extractPropertyValue(props['유사유형']);
	const 원리공유문제 = extractPropertyValue(props['원리공유문제']);
	const 오답시나리오 = extractPropertyValue(props['오답시나리오']);
	const 함정설계 = extractPropertyValue(props['함정설계']);
	const 실수포인트 = extractPropertyValue(props['실수포인트']);
	
	// 문제ID와 대단원 일관성
	if (문제ID && 대단원) {
		if (문제ID.includes('수1_') && 대단원 !== '수1') {
			errors.push(`문제ID(${문제ID})와 대단원(${대단원}) 불일치`);
		}
		if (문제ID.includes('수2_') && 대단원 !== '수2') {
			errors.push(`문제ID(${문제ID})와 대단원(${대단원}) 불일치`);
		}
		if (문제ID.includes('미적분_') && 대단원 !== '미적분') {
			errors.push(`문제ID(${문제ID})와 대단원(${대단원}) 불일치`);
		}
		if (문제ID.includes('확통_') && 대단원 !== '확률과 통계') {
			errors.push(`문제ID(${문제ID})와 대단원(${대단원}) 불일치`);
		}
	}
	
	// 유사유형과 원리공유문제 일관성
	if (유사유형 && 원리공유문제) {
		// 유사유형이 원리공유문제에 포함되어야 함
		const 유사유형List = Array.isArray(유사유형) ? 유사유형 : [유사유형];
		for (const 유형 of 유사유형List) {
			if (유형 && !원리공유문제.includes(유형)) {
				warnings.push(`유사유형 "${유형}"이 원리공유문제에 포함되지 않음`);
			}
		}
	}
	
	// 함정설계와 오답시나리오 일관성
	if (함정설계 && 오답시나리오) {
		if (!오답시나리오.includes(함정설계.substring(0, 20))) {
			warnings.push('함정설계와 오답시나리오의 내용이 일치하지 않을 수 있음');
		}
	}
	
	// 실수포인트와 오답시나리오 일관성
	if (실수포인트 && 오답시나리오) {
		const 실수포인트Keywords = 실수포인트.split(/[1-9]\./).filter(p => p.trim()).slice(0, 3);
		let matchedCount = 0;
		for (const keyword of 실수포인트Keywords) {
			if (keyword.trim() && 오답시나리오.includes(keyword.trim().substring(0, 10))) {
				matchedCount++;
			}
		}
		if (matchedCount === 0 && 실수포인트Keywords.length > 0) {
			warnings.push('실수포인트와 오답시나리오의 내용이 일치하지 않을 수 있음');
		}
	}
	
	return { errors, warnings };
}

async function comprehensiveReview() {
	console.log('='.repeat(80));
	console.log('[전체 노션 데이터베이스 종합 검토]');
	console.log('='.repeat(80));
	
	try {
		// 모든 페이지 가져오기
		const allPages = await collectPaginatedAPI(notion.databases.query, {
			database_id: databaseId
		});
		
		console.log(`\n📖 총 ${allPages.length}개 페이지 발견\n`);
		
		const allErrors = [];
		const allWarnings = [];
		const pageReports = [];
		
		// 각 페이지 검토
		for (let i = 0; i < allPages.length; i++) {
			const page = allPages[i];
			const props = page.properties;
			
			const 문제ID = extractPropertyValue(props['문제ID']);
			const 대단원 = extractPropertyValue(props['대단원']);
			const 중단원 = extractPropertyValue(props['중단원']);
			const 소단원 = extractPropertyValue(props['소단원']);
			const 핵심개념 = extractPropertyValue(props['핵심개념']);
			const 문제구조 = extractPropertyValue(props['문제구조']);
			const 핵심패턴 = extractPropertyValue(props['핵심패턴']);
			const LaTeX예시 = extractPropertyValue(props['LaTeX예시']);
			// 실제 필드명 사용
			const 개념연결 = extractPropertyValue(props['개념연결']);
			const 후행개념 = extractPropertyValue(props['후행개념']);
			const 선행개념 = extractPropertyValue(props['선행개념']);
			
			const pageErrors = [];
			const pageWarnings = [];
			
			// 1. 필수 필드 완전성 검사
			const requiredCheck = checkRequiredFields(page);
			pageErrors.push(...requiredCheck.errors);
			pageWarnings.push(...requiredCheck.warnings);
			
			// 2. LaTeX 수식 검사
			const latexFields = [핵심패턴, LaTeX예시, 개념연결, 후행개념, 선행개념, 핵심개념];
			for (const field of latexFields) {
				if (field) {
					const latexCheck = checkLaTeXSyntax(field);
					if (!latexCheck.valid) {
						pageErrors.push(...latexCheck.errors.map(e => `LaTeX 오류: ${e}`));
					}
				}
			}
			
			// 3. 주제 일관성 검사
			const topicCheck = checkTopicConsistency(대단원, 중단원, 소단원, 핵심개념, 문제구조);
			pageErrors.push(...topicCheck.errors);
			pageWarnings.push(...topicCheck.warnings);
			
			// 4. 문제-해설 일관성 검사
			const 문제 = 핵심패턴 || LaTeX예시 || '';
			const 해설 = [개념연결, 후행개념, 선행개념, 핵심개념].filter(h => h);
			const problemSolutionCheck = checkProblemSolutionConsistency(문제, 해설, 문제구조, 핵심개념);
			pageErrors.push(...problemSolutionCheck.errors);
			pageWarnings.push(...problemSolutionCheck.warnings);
			
			// 5. 수학적 논리 검사
			const mathLogicCheck = checkMathLogic(문제, 해설, 핵심개념, 문제구조);
			pageErrors.push(...mathLogicCheck.errors);
			pageWarnings.push(...mathLogicCheck.warnings);
			
			// 6. 필드 간 상호 참조 일관성 검사
			const consistencyCheck = checkFieldConsistency(page);
			pageErrors.push(...consistencyCheck.errors);
			pageWarnings.push(...consistencyCheck.warnings);
			
			if (pageErrors.length > 0 || pageWarnings.length > 0) {
				pageReports.push({
					문제ID: 문제ID || page.id.substring(0, 8),
					errors: pageErrors,
					warnings: pageWarnings
				});
				
				allErrors.push(...pageErrors.map(e => `[${문제ID || page.id.substring(0, 8)}] ${e}`));
				allWarnings.push(...pageWarnings.map(w => `[${문제ID || page.id.substring(0, 8)}] ${w}`));
			}
			
			if ((i + 1) % 50 === 0) {
				console.log(`  ${i + 1}/${allPages.length} 페이지 검토 완료...`);
			}
		}
		
		// 결과 출력
		console.log('\n' + '='.repeat(80));
		console.log('[검토 결과 요약]');
		console.log('='.repeat(80));
		console.log(`총 페이지 수: ${allPages.length}개`);
		console.log(`오류가 있는 페이지: ${pageReports.length}개`);
		console.log(`총 오류 수: ${allErrors.length}개`);
		console.log(`총 경고 수: ${allWarnings.length}개`);
		
		if (allErrors.length > 0) {
			console.log('\n' + '='.repeat(80));
			console.log('[오류 목록]');
			console.log('='.repeat(80));
			allErrors.slice(0, 50).forEach((error, i) => {
				console.log(`${i + 1}. ${error}`);
			});
			if (allErrors.length > 50) {
				console.log(`\n... 외 ${allErrors.length - 50}개 오류`);
			}
		}
		
		if (allWarnings.length > 0) {
			console.log('\n' + '='.repeat(80));
			console.log('[경고 목록] (상위 50개)');
			console.log('='.repeat(80));
			allWarnings.slice(0, 50).forEach((warning, i) => {
				console.log(`${i + 1}. ${warning}`);
			});
			if (allWarnings.length > 50) {
				console.log(`\n... 외 ${allWarnings.length - 50}개 경고`);
			}
		}
		
		// 카테고리별 통계
		console.log('\n' + '='.repeat(80));
		console.log('[카테고리별 통계]');
		console.log('='.repeat(80));
		
		const errorCategories = {
			'LaTeX 오류': allErrors.filter(e => e.includes('LaTeX')).length,
			'필드 불일치': allErrors.filter(e => e.includes('불일치')).length,
			'필수 필드 누락': allWarnings.filter(w => w.includes('필수 필드')).length,
			'주제 일관성': allWarnings.filter(w => w.includes('일관성') || w.includes('불일치')).length,
			'문제-해설 일관성': allWarnings.filter(w => w.includes('해설') || w.includes('문제에 언급')).length,
			'수학적 논리': allWarnings.filter(w => w.includes('언급 없음') || w.includes('확인')).length
		};
		
		Object.entries(errorCategories).forEach(([category, count]) => {
			if (count > 0) {
				console.log(`${category}: ${count}개`);
			}
		});
		
		console.log('\n' + '='.repeat(80));
		console.log('✅ 검토 완료!');
		console.log('='.repeat(80));
		
	} catch (error) {
		console.error('\n❌ 검토 중 오류 발생:', error.message);
		if (error.code) {
			console.error(`   코드: ${error.code}`);
		}
		console.error(error.stack);
	}
}

async function main() {
	try {
		await comprehensiveReview();
	} catch (error) {
		console.error('\n❌ 실행 중 오류 발생:', error);
		process.exit(1);
	}
}

main();
