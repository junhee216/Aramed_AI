// review_and_fill_geometry_p1_notion_improved.js
// 기하_2024학년도_현우진_드릴_P1 Notion 필드 검토 및 26, 27번 필드 채우기 (개선 버전)

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
		'기하_2024학년도_현우진_드릴', '기하_2024학년도_현우진_드릴_P1_문제_deepseek.json'
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
		'기하_2024학년도_현우진_드릴', '기하_2024학년도_현우진_드릴_P1_해설_deepseek_r1.md'
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
	
	if (q.includes('포물선') || h.includes('포물선')) {
		return '포물선';
	}
	if (q.includes('타원') || h.includes('타원')) {
		return '타원';
	}
	if (q.includes('쌍곡선') || h.includes('쌍곡선')) {
		return '쌍곡선';
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
				(problemType === '포물선' && (conceptLower.includes('포물선') || conceptLower.includes('초점') || conceptLower.includes('준선'))) ||
				(problemType === '타원' && (conceptLower.includes('타원') || conceptLower.includes('초점') || conceptLower.includes('장축'))) ||
				(problemType === '쌍곡선' && (conceptLower.includes('쌍곡선') || conceptLower.includes('초점'))) ||
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
	if (problemType === '포물선' && solution) {
		// 포물선 정의 확인
		if (solution.includes('PF') && solution.includes('PI')) {
			// 포물선 정의 언급됨 ✓
		} else if (question.includes('포물선')) {
			warnings.push('포물선의 정의(PF = PI)가 해설에 명시되지 않음');
		}
		
		// 포물선 방정식 확인
		if (question.includes('y^{2}') || question.includes('y^2')) {
			if (!solution.includes('y^{2}') && !solution.includes('y^2')) {
				warnings.push('문제의 포물선 방정식이 해설에 일치하지 않음');
			}
		}
	}
	
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
	
	// 4. 문제와 해설의 수학적 일관성 (해당 문제만)
	if (problemData && problemData.question && solution) {
		const problemQuestion = problemData.question;
		
		// 포물선 방정식 확인
		if (problemType === '포물선' && (problemQuestion.includes('y^{2}=4') || problemQuestion.includes('y^{2}=8'))) {
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
		'포물선': [
			'포물선의 정의(PF = PI)를 활용하는 문제들',
			'포물선 위의 점에서 초점과 준선까지의 거리가 같음을 이용하는 문제들',
			'포물선의 초점을 지나는 직선과 포물선의 교점 문제',
			'포물선과 원의 교점 문제',
			'직각사다리꼴을 이용한 포물선 문제'
		],
		'타원': [
			'타원의 정의(PF + PF\' = 2a)를 활용하는 문제들',
			'타원 위의 점에서 두 초점까지의 거리의 합이 일정함을 이용하는 문제들',
			'타원과 직선의 교점 문제',
			'타원의 두 초점을 지름의 양 끝으로 하는 원 문제',
			'타원의 장축과 단축을 이용하는 문제'
		],
		'원': [
			'원의 방정식을 이용하는 문제들',
			'원과 직선의 접점 문제',
			'원에 내접하는 사각형 문제',
			'원주각과 중심각의 관계를 이용하는 문제'
		],
		'이차곡선': [
			'이차곡선의 정의와 성질을 활용하는 문제들',
			'초점과 준선을 이용하는 문제들',
			'이차곡선과 직선의 교점 문제'
		]
	};
	
	// 해설에서 관련 내용 추출
	const solutionPrinciples = [];
	if (solution) {
		if (problemType === '포물선' && solution.includes('포물선')) {
			if (solution.includes('직각사다리꼴')) {
				solutionPrinciples.push('직각사다리꼴을 이용한 포물선 문제');
			}
			if (solution.includes('초점을 지나는 직선')) {
				solutionPrinciples.push('포물선의 초점을 지나는 직선 문제');
			}
		}
		if (problemType === '타원' && solution.includes('타원')) {
			if (solution.includes('장축')) {
				solutionPrinciples.push('타원의 장축을 이용하는 문제');
			}
			if (solution.includes('초점')) {
				solutionPrinciples.push('타원의 두 초점을 이용하는 문제');
			}
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
	if (problemType === '포물선') {
		customScenario += '1. 포물선의 정의를 잘못 적용: PF = PI를 PF = PI\'로 착각하거나 준선까지의 거리를 잘못 계산\n';
		customScenario += '2. 포물선 방정식에서 초점의 위치를 잘못 파악: y² = 4ax에서 초점이 (a, 0)임을 (0, a)로 착각\n';
		customScenario += '3. 포물선 위의 점의 좌표를 방정식에 대입할 때 부호 실수\n';
		
		if (solution && solution.includes('직각사다리꼴')) {
			customScenario += '4. 직각사다리꼴에서 두 밑변의 길이의 차를 구할 때 부호 실수\n';
		}
		if (solution && solution.includes('x_{1}+p')) {
			customScenario += '5. 포물선 위의 점의 x좌표에 p를 더하는 과정에서 부호 실수\n';
		}
	}
	
	if (problemType === '타원') {
		customScenario += '1. 타원의 정의를 잘못 적용: PF + PF\' = 2a를 PF + PF\' = a로 착각\n';
		customScenario += '2. 장축과 단축을 혼동하여 초점의 위치를 잘못 계산\n';
		customScenario += '3. 타원 위의 점에서 두 초점까지의 거리의 합을 구할 때 부호 실수\n';
		
		if (solution && solution.includes('장축')) {
			customScenario += '4. 장축의 길이 2a와 반장축의 길이 a를 혼동\n';
		}
	}
	
	if (problemType === '원') {
		customScenario += '1. 원의 방정식에서 중심과 반지름을 잘못 파악\n';
		customScenario += '2. 원과 직선의 접점을 구할 때 판별식을 잘못 적용\n';
		
		if (solution && solution.includes('원주각')) {
			customScenario += '3. 원주각과 중심각의 관계를 잘못 적용: 중심각 = 2 × 원주각임을 잊음\n';
		}
	}
	
	// 공통 오류
	if (solution && solution.includes('직각삼각형') && solution.includes('닮음')) {
		customScenario += `${customScenario.split('\n').length}. 직각삼각형의 닮음을 체크할 때 대응하는 각을 잘못 매칭\n`;
	}
	
	// 기존 함수도 시도
	const generated = generateErrorScenario(
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

async function reviewAndFillGeometryP1() {
	const startTime = Date.now();
	console.log('='.repeat(80));
	console.log('기하_2024학년도_현우진_드릴_P1 Notion 필드 검토 및 26, 27번 필드 채우기 (개선 버전)');
	console.log('='.repeat(80));
	
	await logger.init();
	await logger.info('REVIEW_GEOMETRY_P1', '작업 시작');
	
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
		// Notion에서 P1 문제 찾기
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
		
		// P1 문제만 필터링
		const p1Pages = allPages.filter(page => {
			const 문제ID = extractPropertyValue(page.properties['문제ID']);
			return 문제ID && 문제ID.includes('P1');
		});
		
		console.log(`📋 Notion에서 P1 문제 ${p1Pages.length}개 발견\n`);
		await logger.info('REVIEW_GEOMETRY_P1', `P1 문제 ${p1Pages.length}개 발견`);
		
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
		
		// 각 P1 문제 검토 및 업데이트
		for (let i = 0; i < p1Pages.length; i++) {
			const page = p1Pages[i];
			const 문제ID = extractPropertyValue(page.properties['문제ID']);
			const progress = `[${i + 1}/${p1Pages.length}]`;
			
			console.log(`\n${progress} 📄 처리 중: ${문제ID}`);
			
			try {
				const problem = extractProblemData(page);
				problem.원리공유문제 = extractPropertyValue(page.properties['원리공유문제']);
				problem.오답시나리오 = extractPropertyValue(page.properties['오답시나리오']);
				
				// 문제ID에서 인덱스 추출 (예: P1_02 -> 02)
				const indexMatch = 문제ID.match(/P1[_-]?(\d+)/);
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
					let 오답시나리오;
					
					// 기하 전용 오답 시나리오 시도
					오답시나리오 = generateGeometryErrorScenario(
						problem.question || '',
						problem.함정설계 || '',
						problem.실수포인트 || '',
						problem.핵심개념 || '',
						problem.중단원 || ''
					);
					
					// 해설에서 추가 정보 추출
					if (solution) {
						const problemType = detectProblemType(problem.question || '', problem.핵심개념 || '', problem.중단원 || '');
						
						if (problemType === '포물선' && solution.includes('직각사다리꼴')) {
							오답시나리오 += '\n6. 직각사다리꼴에서 두 밑변의 길이의 차를 구할 때 부호 실수';
						}
						if (problemType === '타원' && solution.includes('장축')) {
							오답시나리오 += '\n5. 장축의 길이 2a와 반장축의 길이 a를 혼동';
						}
					}
					
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
					await logger.info('REVIEW_GEOMETRY_P1', `업데이트 완료: ${문제ID}`, { fields: updatedFields });
				} else if (!needsUpdate) {
					console.log(`  ℹ️  26, 27번 필드가 이미 채워져 있음`);
				}
				
			} catch (error) {
				const errorMsg = `${progress} ❌ ${문제ID} 처리 실패: ${error.message}`;
				console.error(`  ${errorMsg}`);
				await logger.error('REVIEW_GEOMETRY_P1', `처리 실패: ${문제ID}`, {
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
		console.log(`총 P1 문제 수: ${p1Pages.length}개`);
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
		
		await logger.info('REVIEW_GEOMETRY_P1', '작업 완료', {
			total: p1Pages.length,
			updated: updatedCount,
			errors: allErrors.length,
			warnings: allWarnings.length,
			elapsedTime: `${elapsedTime}초`
		});
		
	} catch (error) {
		const elapsedTime = ((Date.now() - startTime) / 1000).toFixed(2);
		console.error('\n❌ 작업 실패:', error.message);
		console.error(error.stack);
		
		await logger.error('REVIEW_GEOMETRY_P1', '작업 실패', {
			error: error.message,
			code: error.code,
			elapsedTime: `${elapsedTime}초`
		});
		
		throw error;
	}
}

async function main() {
	try {
		await reviewAndFillGeometryP1();
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
