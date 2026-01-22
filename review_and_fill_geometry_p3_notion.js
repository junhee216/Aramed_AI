// review_and_fill_geometry_p3_notion.js
// 기하_2024학년도_현우진_드릴_P3 Notion 필드 검토 및 26, 27번 필드 채우기

import 'dotenv/config';
import { Client, collectPaginatedAPI } from '@notionhq/client';
import { createRateLimiter } from './src/middleware/rate_limiter.js';
import { extractPropertyValue, extractProblemData, createRichTextProperty, createProblemIdFilter } from './src/utils/notion_utils.js';
import { extractMathPrinciple, findPrincipleSharedProblems, generateErrorScenario, extractGeometryPrinciple, generateGeometryErrorScenario } from './src/utils/math_principle_utils.js';
import logger from './src/middleware/logger.js';
import fs from 'fs';
import path from 'path';

const notionApiKey = process.env.NOTION_API_KEY;
const databaseId = process.env.NOTION_DATABASE_ID;

if (!notionApiKey || !databaseId) {
	console.error('❌ .env 설정 오류');
	process.exit(1);
}

const notion = new Client({ auth: notionApiKey });
const rateLimiter = createRateLimiter(333);

// 문제 파일 읽기
function loadProblems() {
	const problemPath = path.join(
		'C:', 'Users', 'a', 'Documents', 'MathPDF', 'organized', '현우진',
		'기하_2024학년도_현우진_드릴', '기하_2024학년도_현우진_드릴_P3_문제_deepseek.json'
	);
	
	try {
		const content = fs.readFileSync(problemPath, 'utf-8');
		return JSON.parse(content);
	} catch (error) {
		console.error(`❌ 문제 파일 읽기 실패: ${error.message}`);
		return [];
	}
}

// 해설 파일 읽기
function loadSolution() {
	const solutionPath = path.join(
		'C:', 'Users', 'a', 'Documents', 'MathPDF', 'organized', '현우진',
		'기하_2024학년도_현우진_드릴', '기하_2024학년도_현우진_드릴_P3_해설_deepseek_r1.md'
	);
	
	try {
		return fs.readFileSync(solutionPath, 'utf-8');
	} catch (error) {
		console.error(`❌ 해설 파일 읽기 실패: ${error.message}`);
		return '';
	}
}

// 문제 유형 판별
function detectProblemType(question, 핵심개념, 중단원) {
	const q = (question || '').toLowerCase();
	const h = (핵심개념 || '').toLowerCase();
	
	if (q.includes('타원') || h.includes('타원')) {
		return '타원';
	}
	if (q.includes('쌍곡선') || h.includes('쌍곡선')) {
		return '쌍곡선';
	}
	if (q.includes('포물선') || h.includes('포물선')) {
		return '포물선';
	}
	if (q.includes('벡터') || h.includes('벡터') || q.includes('\\overrightarrow') || q.includes('\\vec')) {
		return '벡터';
	}
	if (q.includes('원') && (q.includes('^{2}') || q.includes('^2'))) {
		return '원';
	}
	if (중단원 === '이차곡선') {
		return '이차곡선';
	}
	return '기타';
}

// 수학적 논리 검증 (개선 버전)
function validateMathLogic(notionPage, problems, solution, problemData) {
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
	const 함정설계 = extractPropertyValue(props['함정설계']);
	const 실수포인트 = extractPropertyValue(props['실수포인트']);
	
	// 문제 유형 판별
	const question = 핵심패턴 || LaTeX예시 || problemData?.question || '';
	const problemType = detectProblemType(question, 핵심개념, 중단원);
	
	// 1. 중단원과 문제 내용 일치 확인
	if (중단원 === '이차곡선') {
		if (question) {
			const has이차곡선 = question.includes('포물선') || 
			                   question.includes('타원') || 
			                   question.includes('쌍곡선') ||
			                   question.includes('초점') ||
			                   question.includes('준선');
			
			if (!has이차곡선) {
				warnings.push('중단원이 "이차곡선"인데 문제에 이차곡선 관련 내용이 명시되지 않음');
			}
		}
	}
	
	// 2. 핵심개념 검증 (유형별로 필터링)
	if (핵심개념 && solution) {
		const 핵심개념List = 핵심개념.split(/[,;]/).map(c => c.trim()).filter(c => c);
		const solutionLower = solution.toLowerCase();
		
		for (const concept of 핵심개념List) {
			// 문제 유형과 관련된 개념만 검증
			const conceptLower = concept.toLowerCase();
			const isRelevant = 
				(problemType === '타원' && (conceptLower.includes('타원') || conceptLower.includes('초점') || conceptLower.includes('장축'))) ||
				(problemType === '쌍곡선' && (conceptLower.includes('쌍곡선') || conceptLower.includes('초점') || conceptLower.includes('주축'))) ||
				(problemType === '포물선' && (conceptLower.includes('포물선') || conceptLower.includes('초점') || conceptLower.includes('준선'))) ||
				(problemType === '벡터' && (conceptLower.includes('벡터') || conceptLower.includes('무게중심') || conceptLower.includes('위치벡터'))) ||
				(problemType === '원' && conceptLower.includes('원')) ||
				problemType === '기타';
			
			if (isRelevant) {
				const hasInSolution = solutionLower.includes(conceptLower) || 
				                     solution.includes(concept);
				
				if (!hasInSolution && concept.length > 2) {
					warnings.push(`핵심개념 "${concept}"이 해설에 명시적으로 다뤄지지 않음`);
				}
			}
		}
	}
	
	// 3. 문제 유형별 검증 (해당 유형만)
	if (problemType === '타원' && solution) {
		// 타원 정의 확인
		const hasEllipseDefinition = solution.includes('PF') && 
		                           (solution.includes('PF\'') || solution.includes('PF\'')) &&
		                           (solution.includes('2a') || solution.includes('2b'));
		
		if (!hasEllipseDefinition && question.includes('타원')) {
			warnings.push('타원의 정의(PF + PF\' = 2a)가 해설에 명시되지 않음');
		}
		
		// 타원 관련 확인
		if (question.includes('장축')) {
			if (!solution.includes('장축')) {
				warnings.push('문제의 타원 관련 내용이 해설에 일치하지 않음');
			}
		}
	}
	
	if (problemType === '쌍곡선' && solution) {
		// 쌍곡선 정의 확인
		const hasHyperbolaDefinition = solution.includes('PF') && 
		                              (solution.includes('PF\'') || solution.includes('PF\'')) &&
		                              (solution.includes('2a') || solution.includes('2b') || solution.includes('주축'));
		
		if (!hasHyperbolaDefinition && question.includes('쌍곡선')) {
			warnings.push('쌍곡선의 정의(|PF - PF\'| = 2a)가 해설에 명시되지 않음');
		}
		
		// 쌍곡선 관련 확인
		if (question.includes('주축') || question.includes('점근선')) {
			if (!solution.includes('주축') && !solution.includes('점근선')) {
				warnings.push('문제의 쌍곡선 관련 내용이 해설에 일치하지 않음');
			}
		}
	}
	
	if (problemType === '포물선' && solution) {
		// 포물선 정의 확인
		const hasParabolaDefinition = solution.includes('PF') && 
		                            (solution.includes('PI') || solution.includes('AH') || solution.includes('접선'));
		
		if (!hasParabolaDefinition && question.includes('포물선')) {
			warnings.push('포물선의 정의(PF = PI)가 해설에 명시되지 않음');
		}
	}
	
	if (problemType === '벡터' && solution) {
		// 벡터 관련 확인
		if (question.includes('\\overrightarrow') || question.includes('\\vec')) {
			if (!solution.includes('\\overrightarrow') && !solution.includes('\\vec') && !solution.includes('벡터')) {
				warnings.push('문제의 벡터 표기가 해설에 일치하지 않음');
			}
		}
	}
	
	// 4. 문제와 해설의 수학적 일관성 (해당 문제만)
	if (problemData && problemData.question && solution) {
		const problemQuestion = problemData.question;
		
		// 타원 방정식 확인
		if (problemType === '타원' && (problemQuestion.includes('\\frac{x^{2}') || problemQuestion.includes('x^2'))) {
			if (!solution.includes('x^{2}') && !solution.includes('x^2')) {
				warnings.push('문제의 타원 방정식이 해설에 일치하지 않음');
			}
		}
		
		// 쌍곡선 방정식 확인
		if (problemType === '쌍곡선' && (problemQuestion.includes('\\frac{x^{2}') || problemQuestion.includes('x^2'))) {
			if (!solution.includes('x^{2}') && !solution.includes('x^2')) {
				warnings.push('문제의 쌍곡선 방정식이 해설에 일치하지 않음');
			}
		}
		
		// 포물선 방정식 확인
		if (problemType === '포물선' && (problemQuestion.includes('y^{2}') || problemQuestion.includes('y^2'))) {
			if (!solution.includes('y^{2}') && !solution.includes('y^2')) {
				warnings.push('문제의 포물선 방정식이 해설에 일치하지 않음');
			}
		}
	}
	
	return { errors, warnings };
}

// 원리공유문제 생성 (개선 버전)
function generatePrincipleSharedProblems(problem, allProblems, solution) {
	const problemType = detectProblemType(problem.question || '', problem.핵심개념 || '', problem.중단원 || '');
	
	// 문제 유형별 특화 내용
	const typeSpecificPrinciples = {
		'타원': [
			'타원의 정의(PF + PF\' = 2a)를 활용하는 문제들',
			'타원 위의 점에서 두 초점까지의 거리의 합이 일정함을 이용하는 문제들',
			'타원의 대칭성을 이용하는 문제들',
			'타원의 초점을 지나는 직선 문제',
			'타원의 접선 방정식을 이용하는 문제들'
		],
		'쌍곡선': [
			'쌍곡선의 정의(|PF - PF\'| = 2a)를 활용하는 문제들',
			'쌍곡선 위의 점에서 두 초점까지의 거리의 차가 일정함을 이용하는 문제들',
			'쌍곡선의 점근선을 이용하는 문제들',
			'쌍곡선의 초점을 지나는 직선 문제',
			'쌍곡선의 접선 방정식을 이용하는 문제들'
		],
		'포물선': [
			'포물선의 정의(PF = PI)를 활용하는 문제들',
			'포물선 위의 점에서 초점과 준선까지의 거리가 같음을 이용하는 문제들',
			'포물선의 초점을 지나는 직선 문제',
			'포물선의 접선 성질을 이용하는 문제들'
		],
		'벡터': [
			'벡터의 연산을 이용하는 문제들',
			'무게중심과 위치벡터를 이용하는 문제들',
			'벡터의 내적을 이용하는 문제들',
			'한 점을 지나고 주어진 벡터에 평행한 직선의 방정식 문제들'
		],
		'이차곡선': [
			'이차곡선의 정의와 성질을 활용하는 문제들',
			'초점과 준선을 이용하는 문제들',
			'이차곡선과 직선의 교점 문제',
			'이차곡선의 접선 문제'
		]
	};
	
	// 해설에서 관련 내용 추출
	const solutionPrinciples = [];
	if (solution) {
		if (problemType === '타원' && solution.includes('타원')) {
			if (solution.includes('접선')) {
				solutionPrinciples.push('타원의 접선 방정식을 이용하는 문제');
			}
			if (solution.includes('대칭')) {
				solutionPrinciples.push('타원의 대칭성을 이용하는 문제');
			}
		}
		if (problemType === '쌍곡선' && solution.includes('쌍곡선')) {
			if (solution.includes('접선')) {
				solutionPrinciples.push('쌍곡선의 접선 방정식을 이용하는 문제');
			}
			if (solution.includes('점근선')) {
				solutionPrinciples.push('쌍곡선의 점근선을 이용하는 문제');
			}
		}
		if (problemType === '포물선' && solution.includes('포물선')) {
			if (solution.includes('접선')) {
				solutionPrinciples.push('포물선의 접선 성질을 이용하는 문제');
			}
		}
		if (problemType === '벡터' && (solution.includes('벡터') || solution.includes('무게중심'))) {
			if (solution.includes('무게중심')) {
				solutionPrinciples.push('무게중심과 위치벡터를 이용하는 문제');
			}
			if (solution.includes('평행') || solution.includes('방정식')) {
				solutionPrinciples.push('벡터를 이용한 직선의 방정식 문제');
			}
		}
		if (solution.includes('직각삼각형') && solution.includes('닮음')) {
			solutionPrinciples.push('직각삼각형의 닮음을 이용하는 문제');
		}
		if (solution.includes('이등변삼각형') && solution.includes('닮음')) {
			solutionPrinciples.push('이등변삼각형의 닮음을 이용하는 문제');
		}
		if (solution.includes('원') && solution.includes('내접')) {
			solutionPrinciples.push('원에 내접하는 사각형을 이용하는 문제');
		}
	}
	
	// 공유 문제 찾기
	const sharedProblems = findPrincipleSharedProblems(problem, allProblems);
	
	if (sharedProblems.length > 0) {
		return sharedProblems.slice(0, 3).join('\n');
	}
	
	// 타입별 특화 내용 사용
	const principles = typeSpecificPrinciples[problemType] || typeSpecificPrinciples['이차곡선'];
	const selectedPrinciples = [...principles, ...solutionPrinciples].slice(0, 5);
	
	return selectedPrinciples.join('\n');
}

// 오답시나리오 생성 (개선 버전)
function generateErrorScenarioImproved(problem, solution) {
	const problemType = detectProblemType(problem.question || '', problem.핵심개념 || '', problem.중단원 || '');
	
	let customScenario = '가장 빠지기 쉬운 오류:\n';
	
	// 문제 유형별 특화 오류
	if (problemType === '타원') {
		customScenario += '1. 타원의 정의를 잘못 적용: PF + PF\' = 2a를 PF + PF\' = a로 착각\n';
		customScenario += '2. 장축과 단축을 혼동하여 초점의 위치를 잘못 계산\n';
		customScenario += '3. 타원 위의 점에서 두 초점까지의 거리의 합을 구할 때 부호 실수\n';
		if (solution && solution.includes('접선')) {
			customScenario += '4. 타원의 접선 방정식을 구할 때 기울기 조건을 놓침\n';
		}
	}
	
	if (problemType === '쌍곡선') {
		customScenario += '1. 쌍곡선의 정의를 잘못 적용: |PF - PF\'| = 2a를 PF - PF\' = 2a로 착각\n';
		customScenario += '2. 주축과 단축을 혼동하여 초점의 위치를 잘못 계산\n';
		customScenario += '3. 쌍곡선 위의 점에서 두 초점까지의 거리의 차를 구할 때 절댓값 처리 실수\n';
		if (solution && solution.includes('접선')) {
			customScenario += '4. 쌍곡선의 접선 방정식을 구할 때 기울기 조건(a²m² - b² > 0)을 놓침\n';
		}
		if (solution && solution.includes('점근선')) {
			customScenario += '5. 쌍곡선의 점근선 방정식을 잘못 적용: y = ±(b/a)x를 y = ±(a/b)x로 착각\n';
		}
	}
	
	if (problemType === '포물선') {
		customScenario += '1. 포물선의 정의를 잘못 적용: PF = PI를 PF = PI/2로 착각\n';
		customScenario += '2. 준선의 위치를 잘못 파악하여 거리 계산 실수\n';
		if (solution && solution.includes('접선')) {
			customScenario += '3. 포물선의 접선 성질을 잘못 적용\n';
		}
	}
	
	if (problemType === '벡터') {
		customScenario += '1. 벡터의 연산에서 부호 실수\n';
		customScenario += '2. 무게중심의 위치벡터 공식을 잘못 적용\n';
		if (solution && solution.includes('평행')) {
			customScenario += '3. 벡터의 평행 조건을 잘못 적용\n';
		}
		if (solution && solution.includes('내적')) {
			customScenario += '4. 벡터의 내적 계산 실수\n';
		}
	}
	
	// 공통 오류
	if (solution && solution.includes('직각삼각형') && solution.includes('닮음')) {
		customScenario += `${customScenario.split('\n').length}. 직각삼각형의 닮음을 체크할 때 대응하는 각을 잘못 매칭\n`;
	}
	if (solution && solution.includes('이등변삼각형') && solution.includes('닮음')) {
		customScenario += `${customScenario.split('\n').length}. 이등변삼각형의 닮음을 체크할 때 대응하는 변을 잘못 매칭\n`;
	}
	if (solution && solution.includes('원') && solution.includes('내접')) {
		customScenario += `${customScenario.split('\n').length}. 원에 내접하는 사각형의 성질을 놓침\n`;
	}
	
	// 기존 함수도 시도
	const generated = generateGeometryErrorScenario(
		problem.question || '',
		problem.함정설계 || '',
		problem.실수포인트 || '',
		problem.핵심개념 || '',
		problem.중단원 || ''
	);
	
	if (generated && generated.length > customScenario.length) {
		return generated;
	}
	
	return customScenario;
}

async function reviewAndFillGeometryP3() {
	const startTime = Date.now();
	console.log('='.repeat(80));
	console.log('기하_2024학년도_현우진_드릴_P3 Notion 필드 검토 및 26, 27번 필드 채우기');
	console.log('='.repeat(80));
	
	await logger.init();
	await logger.info('REVIEW_GEOMETRY_P3', '작업 시작');
	
	// 문제와 해설 파일 로드
	console.log('\n📖 문제 및 해설 파일 로드 중...');
	const problems = loadProblems();
	const solution = loadSolution();
	
	console.log(`  - 문제: ${problems.length}개 발견`);
	console.log(`  - 해설: ${solution.length > 0 ? '로드 완료' : '로드 실패'}\n`);
	
	// 문제 인덱스 맵 생성 (문제ID로 빠른 검색)
	const problemMap = {};
	for (const problem of problems) {
		const index = problem.index || problem.index;
		if (index) {
			problemMap[index] = problem;
		}
	}
	
	try {
		// Notion에서 P3 문제 찾기
		const filter = {
			property: '문제ID',
			title: {
				contains: '기하_2024'
			}
		};
		
		const allPages = await collectPaginatedAPI(notion.databases.query, {
			database_id: databaseId,
			filter
		});
		
		// P3 문제만 필터링
		const p3Pages = allPages.filter(page => {
			const 문제ID = extractPropertyValue(page.properties['문제ID']);
			return 문제ID && 문제ID.includes('P3');
		});
		
		console.log(`📋 Notion에서 P3 문제 ${p3Pages.length}개 발견\n`);
		await logger.info('REVIEW_GEOMETRY_P3', `P3 문제 ${p3Pages.length}개 발견`);
		
		const allErrors = [];
		const allWarnings = [];
		let updatedCount = 0;
		
		// 모든 문제 데이터 구조화 (26, 27번 필드 생성용)
		const allProblems = [];
		for (const page of allPages) {
			try {
				const problem = extractProblemData(page);
				problem.원리공유문제 = extractPropertyValue(page.properties['원리공유문제']);
				problem.오답시나리오 = extractPropertyValue(page.properties['오답시나리오']);
				allProblems.push(problem);
			} catch (error) {
				// 무시
			}
		}
		
		// 각 P3 문제 검토 및 업데이트
		for (let i = 0; i < p3Pages.length; i++) {
			const page = p3Pages[i];
			const 문제ID = extractPropertyValue(page.properties['문제ID']);
			const progress = `[${i + 1}/${p3Pages.length}]`;
			
			console.log(`\n${progress} 📄 처리 중: ${문제ID}`);
			
			try {
				const problem = extractProblemData(page);
				problem.원리공유문제 = extractPropertyValue(page.properties['원리공유문제']);
				problem.오답시나리오 = extractPropertyValue(page.properties['오답시나리오']);
				
				// 문제ID에서 인덱스 추출 (예: P3_01 -> 01)
				const indexMatch = 문제ID.match(/P3[_-]?(\d+)/);
				const problemIndex = indexMatch ? indexMatch[1] : null;
				const problemData = problemIndex ? problemMap[problemIndex] : null;
				
				// 수학적 논리 검증 (개선 버전)
				const validation = validateMathLogic(page, problems, solution, problemData);
				allErrors.push(...validation.errors.map(e => `[${문제ID}] ${e}`));
				allWarnings.push(...validation.warnings.map(w => `[${문제ID}] ${w}`));
				
				if (validation.errors.length > 0 || validation.warnings.length > 0) {
					console.log(`  ⚠️  검토 결과:`);
					validation.errors.forEach(e => console.log(`    ❌ ${e}`));
					validation.warnings.forEach(w => console.log(`    ⚠️  ${w}`));
				} else {
					console.log(`  ✅ 수학적/논리적 오류 없음`);
				}
				
				// 26, 27번 필드 채우기
				const updateProps = {};
				let needsUpdate = false;
				
				// 원리공유문제 (26번) - 개선 버전
				if (!problem.원리공유문제 || String(problem.원리공유문제).trim() === '') {
					let 원리공유문제;
					
					// 기하 전용 원리 추출 시도
					const geometryPrinciple = extractGeometryPrinciple(
						problem.question || '',
						problem.topic || '',
						problem.핵심개념 || '',
						problem.중단원 || ''
					);
					
					if (geometryPrinciple) {
						const principleLines = geometryPrinciple.split(';').map(p => p.trim()).filter(p => p !== '');
						원리공유문제 = principleLines.join('\n');
					} else {
						// 공유 문제 찾기
						const sharedProblems = findPrincipleSharedProblems(problem, allProblems);
						if (sharedProblems.length > 0) {
							원리공유문제 = sharedProblems.slice(0, 3).join('\n');
						} else {
							// 타입별 특화 내용
							원리공유문제 = generatePrincipleSharedProblems(problem, allProblems, solution);
						}
					}
					
					updateProps['원리공유문제'] = createRichTextProperty(원리공유문제);
					needsUpdate = true;
					console.log(`  📝 26번 필드(원리공유문제) 생성`);
				}
				
				// 오답시나리오 (27번) - 개선 버전
				if (!problem.오답시나리오 || String(problem.오답시나리오).trim() === '') {
					const 오답시나리오 = generateErrorScenarioImproved(problem, solution);
					const scenarioLines = 오답시나리오.split('\n').filter(line => line.trim() !== '');
					const formattedScenario = scenarioLines.join('\n');
					updateProps['오답시나리오'] = createRichTextProperty(formattedScenario);
					needsUpdate = true;
					console.log(`  📝 27번 필드(오답시나리오) 생성`);
				}
				
				// Notion 업데이트
				if (needsUpdate && Object.keys(updateProps).length > 0) {
					await rateLimiter.waitIfNeeded();
					await notion.pages.update({
						page_id: page.id,
						properties: updateProps
					});
					
					updatedCount++;
					const updatedFields = Object.keys(updateProps).join(', ');
					console.log(`  ✅ ${updatedFields} 업데이트 완료`);
					await logger.info('REVIEW_GEOMETRY_P3', `업데이트 완료: ${문제ID}`, { fields: updatedFields });
				} else if (!needsUpdate) {
					console.log(`  ℹ️  26, 27번 필드가 이미 채워져 있음`);
				}
				
			} catch (error) {
				const errorMsg = `${progress} ❌ ${문제ID} 처리 실패: ${error.message}`;
				console.error(`  ${errorMsg}`);
				await logger.error('REVIEW_GEOMETRY_P3', `처리 실패: ${문제ID}`, {
					error: error.message,
					code: error.code
				});
			}
		}
		
		// 최종 결과 출력
		const elapsedTime = ((Date.now() - startTime) / 1000).toFixed(2);
		console.log('\n' + '='.repeat(80));
		console.log('[최종 결과]');
		console.log('='.repeat(80));
		console.log(`총 P3 문제 수: ${p3Pages.length}개`);
		console.log(`업데이트 완료: ${updatedCount}개`);
		console.log(`수학적 오류: ${allErrors.length}개`);
		console.log(`경고: ${allWarnings.length}개`);
		console.log(`소요 시간: ${elapsedTime}초`);
		
		if (allErrors.length > 0) {
			console.log('\n❌ 발견된 오류:');
			allErrors.slice(0, 10).forEach(e => console.log(`  - ${e}`));
			if (allErrors.length > 10) {
				console.log(`  ... 외 ${allErrors.length - 10}개`);
			}
		}
		
		if (allWarnings.length > 0) {
			console.log('\n⚠️  발견된 경고:');
			allWarnings.slice(0, 10).forEach(w => console.log(`  - ${w}`));
			if (allWarnings.length > 10) {
				console.log(`  ... 외 ${allWarnings.length - 10}개`);
			}
		}
		
		await logger.info('REVIEW_GEOMETRY_P3', '작업 완료', {
			total: p3Pages.length,
			updated: updatedCount,
			errors: allErrors.length,
			warnings: allWarnings.length,
			elapsedTime: `${elapsedTime}초`
		});
		
	} catch (error) {
		const elapsedTime = ((Date.now() - startTime) / 1000).toFixed(2);
		console.error('\n❌ 작업 실패:', error.message);
		console.error(error.stack);
		
		await logger.error('REVIEW_GEOMETRY_P3', '작업 실패', {
			error: error.message,
			code: error.code,
			elapsedTime: `${elapsedTime}초`
		});
		
		throw error;
	}
}

async function main() {
	try {
		await reviewAndFillGeometryP3();
		console.log('\n' + '='.repeat(80));
		console.log('✅ 작업 완료!');
		console.log('='.repeat(80));
		process.exit(0);
	} catch (error) {
		console.error('\n❌ 실행 중 오류 발생:', error);
		process.exit(1);
	}
}

main();
