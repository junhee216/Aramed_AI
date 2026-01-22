// review_and_fill_haktong_p7_notion.js
// 확통_2024학년도_현우진_드릴_P7 Notion 필드 검토 및 26, 27번 필드 채우기

import 'dotenv/config';
import { Client, collectPaginatedAPI } from '@notionhq/client';
import { createRateLimiter } from './src/middleware/rate_limiter.js';
import { extractPropertyValue, extractProblemData, createRichTextProperty, createProblemIdFilter } from './src/utils/notion_utils.js';
import { extractMathPrinciple, findPrincipleSharedProblems, generateErrorScenario } from './src/utils/math_principle_utils.js';
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
		'확통_2005학년도_현우진_드릴', '확통_2024학년도_현우진_드릴_P7_문제_deepseek.json'
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
		'확통_2024학년도_현우진_드릴', '확통_2024학년도_현우진_드릴_P7_해설_deepseek_r1.md'
	);
	
	try {
		return fs.readFileSync(solutionPath, 'utf-8');
	} catch (error) {
		console.error(`❌ 해설 파일 읽기 실패: ${error.message}`);
		return '';
	}
}

// 수학적 논리 검증
function validateMathLogic(notionPage, problems, solution) {
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
	
	// 1. 중단원과 문제 내용 일치 확인
	if (중단원 === '통계') {
		const question = 핵심패턴 || LaTeX예시 || '';
		if (question) {
			const has통계 = question.includes('정규분포') || 
			               question.includes('표본평균') || 
			               question.includes('신뢰구간') ||
			               question.includes('확률변수') ||
			               question.includes('확률밀도함수');
			
			if (!has통계) {
				warnings.push('중단원이 "통계"인데 문제에 통계 관련 내용이 명시되지 않음');
			}
		}
	}
	
	// 2. 핵심개념 검증
	if (핵심개념 && solution) {
		const 핵심개념List = 핵심개념.split(/[,;]/).map(c => c.trim()).filter(c => c);
		const solutionLower = solution.toLowerCase();
		
		for (const concept of 핵심개념List) {
			const conceptLower = concept.toLowerCase();
			const hasInSolution = solutionLower.includes(conceptLower) || 
			                     solution.includes(concept);
			
			if (!hasInSolution && concept.length > 2) {
				warnings.push(`핵심개념 "${concept}"이 해설에 명시적으로 다뤄지지 않음`);
			}
		}
	}
	
	// 3. 표본평균 관련 공식 검증
	if (solution) {
		// 표본평균의 분산 공식 확인
		if (solution.includes('표본평균') || solution.includes('\\bar{X}')) {
			const hasVarianceFormula = solution.includes('\\frac{\\sigma^{2}}{n}') ||
			                          solution.includes('σ²/n') ||
			                          solution.includes('V(\\bar{X})');
			
			if (!hasVarianceFormula) {
				warnings.push('표본평균의 분산 공식이 해설에 명시되지 않음');
			}
		}
		
		// 신뢰구간 공식 확인
		if (solution.includes('신뢰구간') || solution.includes('신뢰도')) {
			const hasConfidenceFormula = solution.includes('1.96') || 
			                            solution.includes('2.58') ||
			                            solution.includes('\\frac{\\sigma}{\\sqrt{n}}');
			
			if (!hasConfidenceFormula) {
				warnings.push('신뢰구간 공식이 해설에 명시되지 않음');
			}
		}
	}
	
	// 4. 문제와 해설의 수학적 일관성
	if (problems && problems.length > 0 && solution) {
		// 문제에 나온 수식이 해설에 있는지 확인
		for (const problem of problems) {
			if (problem.question) {
				// 정규분포 표기 확인
				if (problem.question.includes('N(') || problem.question.includes('\\mathrm{N}')) {
					if (!solution.includes('정규분포') && !solution.includes('N(')) {
						warnings.push('문제의 정규분포 표기가 해설에 일치하지 않음');
					}
				}
			}
		}
	}
	
	return { errors, warnings };
}

async function reviewAndFillHaktongP7() {
	const startTime = Date.now();
	console.log('='.repeat(80));
	console.log('확통_2024학년도_현우진_드릴_P7 Notion 필드 검토 및 26, 27번 필드 채우기');
	console.log('='.repeat(80));
	
	await logger.init();
	await logger.info('REVIEW_P7', '작업 시작');
	
	// 문제와 해설 파일 로드
	console.log('\n📖 문제 및 해설 파일 로드 중...');
	const problems = loadProblems();
	const solution = loadSolution();
	
	console.log(`  - 문제: ${problems.length}개 발견`);
	console.log(`  - 해설: ${solution.length > 0 ? '로드 완료' : '로드 실패'}\n`);
	
	try {
		// Notion에서 P7 문제 찾기
		const filter = {
			property: '문제ID',
			title: {
				contains: '확통_2024'
			}
		};
		
		const allPages = await collectPaginatedAPI(notion.databases.query, {
			database_id: databaseId,
			filter
		});
		
		// P7 문제만 필터링
		const p7Pages = allPages.filter(page => {
			const 문제ID = extractPropertyValue(page.properties['문제ID']);
			return 문제ID && 문제ID.includes('P7');
		});
		
		console.log(`📋 Notion에서 P7 문제 ${p7Pages.length}개 발견\n`);
		await logger.info('REVIEW_P7', `P7 문제 ${p7Pages.length}개 발견`);
		
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
		
		// 각 P7 문제 검토 및 업데이트
		for (let i = 0; i < p7Pages.length; i++) {
			const page = p7Pages[i];
			const 문제ID = extractPropertyValue(page.properties['문제ID']);
			const progress = `[${i + 1}/${p7Pages.length}]`;
			
			console.log(`\n${progress} 📄 처리 중: ${문제ID}`);
			
			try {
				const problem = extractProblemData(page);
				problem.원리공유문제 = extractPropertyValue(page.properties['원리공유문제']);
				problem.오답시나리오 = extractPropertyValue(page.properties['오답시나리오']);
				
				// 수학적 논리 검증
				const validation = validateMathLogic(page, problems, solution);
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
				
				// 원리공유문제 (26번)
				if (!problem.원리공유문제 || String(problem.원리공유문제).trim() === '') {
					const sharedProblems = findPrincipleSharedProblems(problem, allProblems);
					let 원리공유문제;
					
					if (sharedProblems.length > 0) {
						원리공유문제 = sharedProblems.slice(0, 5).join('\n');
					} else {
						const principle = extractMathPrinciple(
							problem.question || '',
							problem.topic || '',
							problem.핵심개념 || '',
							problem.중단원 || ''
						);
						
						if (principle) {
							const principleLines = principle.split(';').map(p => p.trim()).filter(p => p !== '');
							원리공유문제 = principleLines.join('\n');
						} else {
							원리공유문제 = '표본평균, 정규분포, 신뢰구간 등 통계의 핵심 개념을 공유하는 문제들';
						}
					}
					
					updateProps['원리공유문제'] = createRichTextProperty(원리공유문제);
					needsUpdate = true;
					console.log(`  📝 26번 필드(원리공유문제) 생성`);
				}
				
				// 오답시나리오 (27번)
				if (!problem.오답시나리오 || String(problem.오답시나리오).trim() === '') {
					const 오답시나리오 = generateErrorScenario(
						problem.question || '',
						problem.함정설계 || '',
						problem.실수포인트 || '',
						problem.핵심개념 || '',
						problem.중단원 || ''
					);
					
					if (오답시나리오) {
						const scenarioLines = 오답시나리오.split('\n').filter(line => line.trim() !== '');
						const formattedScenario = scenarioLines.join('\n');
						updateProps['오답시나리오'] = createRichTextProperty(formattedScenario);
					} else {
						// 해설과 문제를 참고하여 오답시나리오 생성
						let customScenario = '가장 빠지기 쉬운 오류:\n';
						if (solution.includes('표본평균')) {
							customScenario += '1. 표본평균의 분산 공식을 잘못 적용: V(\\bar{X}) = σ²/n을 V(\\bar{X}) = σ²로 착각\n';
						}
						if (solution.includes('신뢰구간')) {
							customScenario += '2. 신뢰구간 공식에서 표준편차와 표준오차를 혼동\n';
							customScenario += '3. 신뢰상수 1.96과 2.58을 잘못 선택\n';
						}
						if (solution.includes('정규분포')) {
							customScenario += '4. 정규분포의 표준화 과정에서 부호 실수\n';
						}
						updateProps['오답시나리오'] = createRichTextProperty(customScenario);
					}
					
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
					await logger.info('REVIEW_P7', `업데이트 완료: ${문제ID}`, { fields: updatedFields });
				} else if (!needsUpdate) {
					console.log(`  ℹ️  26, 27번 필드가 이미 채워져 있음`);
				}
				
			} catch (error) {
				const errorMsg = `${progress} ❌ ${문제ID} 처리 실패: ${error.message}`;
				console.error(`  ${errorMsg}`);
				await logger.error('REVIEW_P7', `처리 실패: ${문제ID}`, {
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
		console.log(`총 P7 문제 수: ${p7Pages.length}개`);
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
		
		await logger.info('REVIEW_P7', '작업 완료', {
			total: p7Pages.length,
			updated: updatedCount,
			errors: allErrors.length,
			warnings: allWarnings.length,
			elapsedTime: `${elapsedTime}초`
		});
		
	} catch (error) {
		const elapsedTime = ((Date.now() - startTime) / 1000).toFixed(2);
		console.error('\n❌ 작업 실패:', error.message);
		console.error(error.stack);
		
		await logger.error('REVIEW_P7', '작업 실패', {
			error: error.message,
			code: error.code,
			elapsedTime: `${elapsedTime}초`
		});
		
		throw error;
	}
}

async function main() {
	try {
		await reviewAndFillHaktongP7();
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
