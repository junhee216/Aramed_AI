// review_and_fill_haktong_p3_notion.js
// 확통_2024학년도_현우진_드릴_P3 노션 데이터 검토 및 26번, 27번 필드 채우기

import 'dotenv/config';
import { Client, collectPaginatedAPI } from '@notionhq/client';
import fs from 'fs';
import path from 'path';

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

// JSON 파일 로드
function loadJSONFile(filePath) {
	try {
		const fullPath = path.resolve(filePath);
		const content = fs.readFileSync(fullPath, 'utf-8');
		return JSON.parse(content);
	} catch (error) {
		console.error(`❌ JSON 파일 읽기 오류 (${filePath}): ${error.message}`);
		return null;
	}
}

// 수학적 원리 추출 (확통 특화)
function extractMathPrinciple(question, topic, 핵심개념, 중단원) {
	const principles = [];
	
	if (!question) return principles;
	
	const q = question.toLowerCase();
	
	// 대소 관계의 조건 (중복조합)
	if (q.includes('≤') || q.includes('≥') || q.includes('<') || q.includes('>')) {
		if (q.includes('자연수') || q.includes('정수')) {
			principles.push('대소 관계의 조건을 차를 새로운 미지수로 잡아 중복조합으로 다룰 수 있음');
			if (q.includes('≤') && q.includes('<')) {
				principles.push('등호가 일부 포함된 부등식에서 음이 아닌 정수와 자연수를 섞어서 미지수 설정');
			}
		}
	}
	
	// 함수의 개수
	if (q.includes('함수') && q.includes('개수')) {
		if (q.includes('집합') && q.includes('→')) {
			principles.push('함수의 개수: 모든 함수는 중복순열, 일대일함수는 순열, 순서가 정해진 배열은 조합/중복조합');
		}
		if (q.includes('치역')) {
			principles.push('치역의 조건이 있는 함수의 개수: 치역의 원소를 먼저 선택하고 정의역의 원소에 대응하는 경우의 수');
		}
	}
	
	// 이항정리
	if (q.includes('다항식') && q.includes('전개식')) {
		principles.push('이항정리: $(a+b)^n$의 전개식에서 $a^r b^{n-r}$의 계수는 ${}_n C_r$');
		if (q.includes('유리수') || q.includes('무리수')) {
			principles.push('이항정리에서 계수가 유리수/무리수인 항의 판별');
		}
	}
	
	// 확률
	if (q.includes('확률') || topic === '확률') {
		principles.push('수학적 확률: P(A) = n(A)/n(S), 근원사건을 제대로 파악하는 것이 중요');
		if (q.includes('여사건') || q.includes('드모르간')) {
			principles.push('여사건의 활용: 조건이 복잡할 때 반대 조건을 생각');
		}
		if (q.includes('곱이') && (q.includes('짝수') || q.includes('홀수'))) {
			principles.push('곱이 짝수/홀수: 여사건인 곱이 홀수/짝수를 이용');
		}
	}
	
	// 순서가 정해진 배열
	if (q.includes('순서') || q.includes('≤') || q.includes('≥')) {
		if (q.includes('함수') && (q.includes('≤') || q.includes('≥'))) {
			principles.push('순서가 정해진 배열: $x_1 < x_2$이면 $f(x_1) ≤ f(x_2)$인 함수는 중복조합');
		}
	}
	
	// 핵심개념 기반
	if (핵심개념) {
		const 핵심개념List = 핵심개념.split(/[,;]/).map(c => c.trim());
		for (const concept of 핵심개념List) {
			if (concept.includes('중복조합') || concept.includes('H_')) {
				principles.push('중복조합: 부정방정식의 정수해, 대소 관계의 조건');
			}
			if (concept.includes('이항정리') || concept.includes('이항계수')) {
				principles.push('이항정리와 이항계수의 성질');
			}
			if (concept.includes('함수') && concept.includes('개수')) {
				principles.push('함수의 개수: 조건에 따른 경우의 수 계산');
			}
		}
	}
	
	return principles.length > 0 ? principles.join('; ') : null;
}

// 오답 시나리오 생성 (확통 특화)
function generateErrorScenario(question, 함정설계, 실수포인트, 핵심개념, 중단원) {
	const scenarios = [];
	
	if (!question) return null;
	
	const q = question.toLowerCase();
	
	// 대소 관계의 조건 관련 오류
	if (q.includes('≤') || q.includes('≥') || q.includes('<') || q.includes('>')) {
		if (q.includes('자연수') || q.includes('정수')) {
			scenarios.push('대소 관계의 조건에서 음이 아닌 정수와 자연수를 구분하지 못해 중복조합 계산 오류');
			scenarios.push('등호가 일부 포함된 부등식에서 미지수 설정 시 $x_2+1$과 같은 변환을 놓침');
		}
	}
	
	// 함수의 개수 관련 오류
	if (q.includes('함수') && q.includes('개수')) {
		scenarios.push('함수의 개수에서 모든 함수($b^a$), 일대일함수($_b P_a$), 순서가 정해진 배열($_b C_a$ 또는 $_b H_a$)을 혼동');
		if (q.includes('치역')) {
			scenarios.push('치역의 조건이 있는 함수의 개수에서 정의역의 모든 원소에 치역의 1개 또는 2개의 원소만 대응하는 경우를 빼지 않음');
		}
	}
	
	// 이항정리 관련 오류
	if (q.includes('다항식') && q.includes('전개식')) {
		scenarios.push('이항정리에서 계수와 이항계수를 혼동: 이항계수는 ${}_n C_r$, 계수는 이항계수 × 각 항의 계수');
		if (q.includes('유리수') || q.includes('무리수')) {
			scenarios.push('이항정리에서 계수가 유리수/무리수인 항의 판별 시 $\sqrt[3]{2}$와 같은 무리수 계수를 고려하지 않음');
		}
	}
	
	// 확률 관련 오류
	if (q.includes('확률') || 중단원 === '확률') {
		scenarios.push('수학적 확률에서 근원사건을 제대로 파악하지 못해 분모(전체 경우의 수) 계산 오류');
		if (q.includes('여사건')) {
			scenarios.push('여사건을 이용할 때 드모르간의 법칙 적용 오류 또는 여사건이 더 복잡한 경우를 고려하지 않음');
		}
		if (q.includes('곱이') && (q.includes('짝수') || q.includes('홀수'))) {
			scenarios.push('곱이 짝수/홀수 문제에서 여사건인 곱이 홀수/짝수를 이용하지 않고 직접 계산하여 복잡해짐');
		}
	}
	
	// 순서가 정해진 배열 관련 오류
	if (q.includes('순서') || (q.includes('함수') && (q.includes('≤') || q.includes('≥')))) {
		scenarios.push('순서가 정해진 배열에서 조합과 중복조합을 혼동: $<$는 조합, $≤$는 중복조합');
	}
	
	// 함정설계 기반
	if (함정설계) {
		const 함정Keywords = 함정설계.split(/[1-9]\./).filter(p => p.trim()).slice(0, 3);
		for (const keyword of 함정Keywords) {
			if (keyword.trim() && keyword.trim().length > 5) {
				scenarios.push(`함정: ${keyword.trim().substring(0, 50)}`);
			}
		}
	}
	
	// 실수포인트 기반
	if (실수포인트) {
		const 실수Keywords = 실수포인트.split(/[1-9]\./).filter(p => p.trim()).slice(0, 3);
		for (const keyword of 실수Keywords) {
			if (keyword.trim() && keyword.trim().length > 5) {
				scenarios.push(`실수: ${keyword.trim().substring(0, 50)}`);
			}
		}
	}
	
	return scenarios.length > 0 ? scenarios.join('\n') : null;
}

// 수학적 논리 검증
function validateMathLogic(problem, solution, notionPage) {
	const errors = [];
	const warnings = [];
	
	const props = notionPage.properties;
	const 문제ID = extractPropertyValue(props['문제ID']);
	const 대단원 = extractPropertyValue(props['대단원']);
	const 중단원 = extractPropertyValue(props['중단원']);
	const 핵심개념 = extractPropertyValue(props['핵심개념']);
	const 문제구조 = extractPropertyValue(props['문제구조']);
	const 핵심패턴 = extractPropertyValue(props['핵심패턴']);
	const LaTeX예시 = extractPropertyValue(props['LaTeX예시']);
	
	// 문제와 노션 필드 일치 확인
	const question = problem?.question || '';
	const notionQuestion = 핵심패턴 || LaTeX예시 || '';
	
	// 핵심개념이 문제/해설과 일치하는지 확인
	if (핵심개념 && solution) {
		const solutionText = solution.content || '';
		const 핵심개념List = 핵심개념.split(/[,;]/).map(c => c.trim());
		
		for (const concept of 핵심개념List) {
			if (concept && !solutionText.includes(concept) && !question.includes(concept)) {
				warnings.push(`핵심개념 "${concept}"이 해설에 명시적으로 다뤄지지 않음`);
			}
		}
	}
	
	// 중단원과 문제 내용 일치 확인
	if (중단원 === '경우의 수') {
		if (question.includes('확률') && !question.includes('경우의 수')) {
			warnings.push('중단원이 "경우의 수"인데 문제에 확률 관련 내용 포함');
		}
	}
	
	if (중단원 === '확률') {
		if (!question.includes('확률') && !question.includes('확률은')) {
			warnings.push('중단원이 "확률"인데 문제에 확률 관련 내용이 명시되지 않음');
		}
	}
	
	// 문제구조와 실제 문제 유형 일치 확인
	if (문제구조) {
		const isMultipleChoice = problem?.answer_type === 'multiple_choice';
		const isShortAnswer = problem?.answer_type === 'short_answer';
		
		if (isMultipleChoice && !문제구조.includes('객관식') && !문제구조.includes('선택형')) {
			warnings.push('문제가 객관식인데 문제구조에 객관식 언급 없음');
		}
		
		if (isShortAnswer && !문제구조.includes('주관식') && !문제구조.includes('서술형')) {
			warnings.push('문제가 주관식인데 문제구조에 주관식 언급 없음');
		}
	}
	
	return { errors, warnings };
}

async function reviewAndFillHaktongP3() {
	console.log('='.repeat(80));
	console.log('확통_2024학년도_현우진_드릴_P3 노션 데이터 검토 및 26번, 27번 필드 채우기');
	console.log('='.repeat(80));
	
	try {
		// JSON 파일 로드
		const problemsPath = path.resolve('C:\\Users\\a\\Documents\\MathPDF\\organized\\현우진\\확통_2005학년도_현우진_드릴\\확통_2024학년도_현우진_드릴_P3_문제_deepseek.json');
		const solutionsPath = path.resolve('C:\\Users\\a\\Documents\\MathPDF\\organized\\현우진\\확통_2005학년도_현우진_드릴\\확통_2024학년도_현우진_드릴_P3_해설_deepseek.json');
		
		const problems = loadJSONFile(problemsPath);
		const solutions = loadJSONFile(solutionsPath);
		
		if (!problems || !solutions) {
			console.error('❌ JSON 파일을 읽을 수 없습니다.');
			return;
		}
		
		console.log(`\n📖 문제 수: ${problems.length}개`);
		console.log(`📖 해설 수: ${solutions.length}개\n`);
		
		// 노션에서 P3 관련 페이지 찾기
		const allPages = await collectPaginatedAPI(notion.databases.query, {
			database_id: databaseId,
			filter: {
				property: '문제ID',
				title: {
					contains: '확통_2024학년도_현우진_드릴_P3'
				}
			}
		});
		
		console.log(`📖 노션에서 발견된 P3 페이지: ${allPages.length}개\n`);
		
		if (allPages.length === 0) {
			console.log('⚠️  노션에 P3 관련 페이지가 없습니다.');
			return;
		}
		
		// 각 페이지 검토 및 업데이트
		let updatedCount = 0;
		const allErrors = [];
		const allWarnings = [];
		
		for (const page of allPages) {
			const props = page.properties;
			const 문제ID = extractPropertyValue(props['문제ID']);
			
			console.log(`\n📄 처리 중: ${문제ID}`);
			
			// 문제 번호 추출 (예: P3_01, P3_02 등)
			const problemMatch = 문제ID.match(/P3[_\s]?(\d+)/);
			if (!problemMatch) {
				console.log(`  ⚠️  문제 번호를 찾을 수 없음: ${문제ID}`);
				continue;
			}
			
			const problemNum = parseInt(problemMatch[1]);
			const problemIndex = problemNum - 1;
			
			if (problemIndex < 0 || problemIndex >= problems.length) {
				console.log(`  ⚠️  문제 인덱스 범위 초과: ${problemNum} (총 ${problems.length}개)`);
				continue;
			}
			
			const problem = problems[problemIndex];
			const solution = solutions[problemIndex] || solutions[problemIndex % solutions.length];
			
			// 노션 필드 추출
			const 대단원 = extractPropertyValue(props['대단원']);
			const 중단원 = extractPropertyValue(props['중단원']);
			const 핵심개념 = extractPropertyValue(props['핵심개념']);
			const 문제구조 = extractPropertyValue(props['문제구조']);
			const 함정설계 = extractPropertyValue(props['함정설계']);
			const 실수포인트 = extractPropertyValue(props['실수포인트']);
			const 원리공유문제 = extractPropertyValue(props['원리공유문제']);
			const 오답시나리오 = extractPropertyValue(props['오답시나리오']);
			
			// 수학적 논리 검증
			const validation = validateMathLogic(problem, solution, page);
			allErrors.push(...validation.errors);
			allWarnings.push(...validation.warnings);
			
			if (validation.errors.length > 0 || validation.warnings.length > 0) {
				console.log(`  ⚠️  검토 결과:`);
				validation.errors.forEach(e => console.log(`    ❌ ${e}`));
				validation.warnings.forEach(w => console.log(`    ⚠️  ${w}`));
			}
			
			// 26번, 27번 필드 채우기
			const updateProps = {};
			let needsUpdate = false;
			
			// 원리공유문제 (26번)
			if (!원리공유문제 || 원리공유문제.trim() === '') {
				const principle = extractMathPrinciple(
					problem.question,
					problem.topic,
					핵심개념,
					중단원
				);
				
				if (principle) {
					updateProps['원리공유문제'] = {
						rich_text: [
							{
								text: {
									content: principle
								}
							}
						]
					};
					needsUpdate = true;
					console.log(`  ✅ 원리공유문제 생성: ${principle.substring(0, 50)}...`);
				}
			}
			
			// 오답시나리오 (27번)
			if (!오답시나리오 || 오답시나리오.trim() === '') {
				const scenario = generateErrorScenario(
					problem.question,
					함정설계,
					실수포인트,
					핵심개념,
					중단원
				);
				
				if (scenario) {
					updateProps['오답시나리오'] = {
						rich_text: [
							{
								text: {
									content: scenario
								}
							}
						]
					};
					needsUpdate = true;
					console.log(`  ✅ 오답시나리오 생성: ${scenario.substring(0, 50)}...`);
				}
			}
			
			// 업데이트 실행
			if (needsUpdate) {
				await rateLimiter.waitIfNeeded();
				await notion.pages.update({
					page_id: page.id,
					properties: updateProps
				});
				updatedCount++;
				console.log(`  ✅ 업데이트 완료`);
			} else {
				console.log(`  ℹ️  업데이트 불필요 (이미 채워져 있음)`);
			}
		}
		
		// 결과 요약
		console.log('\n' + '='.repeat(80));
		console.log('[작업 결과 요약]');
		console.log('='.repeat(80));
		console.log(`총 페이지 수: ${allPages.length}개`);
		console.log(`업데이트된 페이지: ${updatedCount}개`);
		console.log(`총 오류: ${allErrors.length}개`);
		console.log(`총 경고: ${allWarnings.length}개`);
		
		if (allErrors.length > 0) {
			console.log('\n[오류 목록]');
			allErrors.forEach((error, i) => {
				console.log(`${i + 1}. ${error}`);
			});
		}
		
		if (allWarnings.length > 0) {
			console.log('\n[경고 목록] (상위 10개)');
			allWarnings.slice(0, 10).forEach((warning, i) => {
				console.log(`${i + 1}. ${warning}`);
			});
			if (allWarnings.length > 10) {
				console.log(`... 외 ${allWarnings.length - 10}개 경고`);
			}
		}
		
		console.log('\n' + '='.repeat(80));
		console.log('✅ 작업 완료!');
		console.log('='.repeat(80));
		
	} catch (error) {
		console.error('\n❌ 작업 중 오류 발생:', error.message);
		if (error.code) {
			console.error(`   코드: ${error.code}`);
		}
		console.error(error.stack);
	}
}

async function main() {
	try {
		await reviewAndFillHaktongP3();
	} catch (error) {
		console.error('\n❌ 실행 중 오류 발생:', error);
		process.exit(1);
	}
}

main();
