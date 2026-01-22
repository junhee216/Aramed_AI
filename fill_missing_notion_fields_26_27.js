// fill_missing_notion_fields_26_27.js
// 노션 데이터베이스에서 비어있는 26번(원리공유문제), 27번(오답시나리오) 필드 채우기
// 개선: 공통 유틸리티 사용, 에러 처리 및 로깅 개선

import 'dotenv/config';
import { Client, collectPaginatedAPI } from '@notionhq/client';
import { createRateLimiter } from './src/middleware/rate_limiter.js';
import { extractPropertyValue, extractProblemData, createRichTextProperty, createProblemIdFilter } from './src/utils/notion_utils.js';
import { extractMathPrinciple, findPrincipleSharedProblems, generateErrorScenario } from './src/utils/math_principle_utils.js';
import logger from './src/middleware/logger.js';

const notionApiKey = process.env.NOTION_API_KEY;
const databaseId = process.env.NOTION_DATABASE_ID;

if (!notionApiKey || !databaseId) {
	console.error('❌ .env 설정 오류');
	process.exit(1);
}

const notion = new Client({ auth: notionApiKey });
const rateLimiter = createRateLimiter(333); // 초당 3회 요청 (1000ms / 3 ≈ 333ms)

async function fillMissingFields() {
	const startTime = Date.now();
	console.log('='.repeat(80));
	console.log('비어있는 26번(원리공유문제), 27번(오답시나리오) 필드 채우기');
	console.log('='.repeat(80));
	
	await logger.init();
	await logger.info('FILL_FIELDS', '작업 시작');
	
	try {
		// 모든 페이지 가져오기 (수1, 수2, 미적분, 확통 포함)
		const problemIdPatterns = ['수1_2025', '수2_2025', '미적분_2025', '확통_2024'];
		const filter = createProblemIdFilter(problemIdPatterns);
		
		await logger.info('FILL_FIELDS', `페이지 조회 시작: ${problemIdPatterns.join(', ')}`);
		
		const allPages = await collectPaginatedAPI(notion.databases.query, {
			database_id: databaseId,
			filter
		});
		
		console.log(`\n📖 총 ${allPages.length}개 페이지 발견\n`);
		await logger.info('FILL_FIELDS', `총 ${allPages.length}개 페이지 발견`);
		
		// 문제 데이터 구조화
		const problems = [];
		for (const page of allPages) {
			try {
				const problem = extractProblemData(page);
				problem.원리공유문제 = extractPropertyValue(page.properties['원리공유문제']);
				problem.오답시나리오 = extractPropertyValue(page.properties['오답시나리오']);
				problems.push(problem);
			} catch (error) {
				await logger.warn('FILL_FIELDS', `페이지 데이터 추출 실패: ${page.id}`, { error: error.message });
			}
		}
		
		// 비어있는 필드가 있는 문제 찾기
		const needsUpdate = problems.filter(p => {
			const 원리공유문제Empty = !p.원리공유문제 || String(p.원리공유문제).trim() === '';
			const 오답시나리오Empty = !p.오답시나리오 || String(p.오답시나리오).trim() === '';
			return 원리공유문제Empty || 오답시나리오Empty;
		});
		
		console.log(`📝 업데이트 필요한 페이지: ${needsUpdate.length}개\n`);
		await logger.info('FILL_FIELDS', `업데이트 필요한 페이지: ${needsUpdate.length}개`);
		
		// 각 문제에 대해 필드 채우기
		let updatedCount = 0;
		let errorCount = 0;
		
		for (let i = 0; i < needsUpdate.length; i++) {
			const problem = needsUpdate[i];
			const progress = `[${i + 1}/${needsUpdate.length}]`;
			
			try {
				const updateProps = {};
				
				// 원리공유문제가 비어있으면 생성
				if (!problem.원리공유문제 || String(problem.원리공유문제).trim() === '') {
					const sharedProblems = findPrincipleSharedProblems(problem, problems);
					let 원리공유문제;
					
					if (sharedProblems.length > 0) {
						// 원리 공유 문제 ID를 줄바꿈으로 구분
						원리공유문제 = sharedProblems.slice(0, 5).join('\n');
					} else {
						// 원리 공유 문제가 없으면 핵심 원리 추출
						const principle = extractMathPrinciple(
							problem.question || '',
							problem.topic || '',
							problem.핵심개념 || '',
							problem.중단원 || ''
						);
						
						if (principle) {
							// 세미콜론으로 구분된 여러 항목을 줄바꿈으로 표시
							const principleLines = principle.split(';').map(p => p.trim()).filter(p => p !== '');
							원리공유문제 = principleLines.join('\n');
						} else {
							원리공유문제 = '해당 문제와 본질적으로 같은 원리를 공유하는 다른 문제를 찾을 수 없습니다.';
						}
					}
					
					updateProps['원리공유문제'] = createRichTextProperty(원리공유문제);
				}
				
				// 오답시나리오가 비어있으면 생성 (항상 다시 생성하여 줄바꿈 문제 해결)
				if (!problem.오답시나리오 || String(problem.오답시나리오).trim() === '') {
					const 오답시나리오 = generateErrorScenario(
						problem.question || '',
						problem.함정설계 || '',
						problem.실수포인트 || '',
						problem.핵심개념 || '',
						problem.중단원 || ''
					);
					
					if (오답시나리오) {
						// 노션 API는 \n을 줄바꿈으로 인식하므로 하나의 text 객체에 포함
						const scenarioLines = 오답시나리오.split('\n').filter(line => line.trim() !== '');
						const formattedScenario = scenarioLines.join('\n');
						updateProps['오답시나리오'] = createRichTextProperty(formattedScenario);
					} else {
						updateProps['오답시나리오'] = createRichTextProperty('가장 빠지기 쉬운 논리적 함정을 식별할 수 없습니다.');
					}
				}
				
				// 업데이트 실행
				if (Object.keys(updateProps).length > 0) {
					await rateLimiter.waitIfNeeded();
					await notion.pages.update({
						page_id: problem.id,
						properties: updateProps
					});
					
					updatedCount++;
					const updatedFields = Object.keys(updateProps).join(', ');
					console.log(`${progress} ✅ ${problem.문제ID || problem.id.substring(0, 8)}... [${updatedFields}] 업데이트 완료`);
					await logger.info('FILL_FIELDS', `업데이트 완료: ${problem.문제ID}`, { fields: updatedFields });
				}
			} catch (error) {
				errorCount++;
				const errorMsg = `${progress} ❌ ${problem.문제ID || problem.id.substring(0, 8)}... 업데이트 실패: ${error.message}`;
				console.error(errorMsg);
				await logger.error('FILL_FIELDS', `업데이트 실패: ${problem.문제ID}`, { 
					error: error.message,
					code: error.code,
					stack: error.stack
				});
				
				// 연속 에러가 많으면 잠시 대기
				if (errorCount > 0 && errorCount % 10 === 0) {
					console.log('⚠️  연속 에러 발생. 5초 대기 후 계속...');
					await new Promise(resolve => setTimeout(resolve, 5000));
				}
			}
		}
		
		const elapsedTime = ((Date.now() - startTime) / 1000).toFixed(2);
		console.log(`\n✅ 총 ${updatedCount}개 페이지 업데이트 완료 (소요 시간: ${elapsedTime}초)`);
		if (errorCount > 0) {
			console.log(`⚠️  ${errorCount}개 페이지 업데이트 실패`);
		}
		
		// 업데이트 후 통계 확인 (기존 데이터 사용)
		const empty원리공유문제 = problems.filter(p => !p.원리공유문제 || String(p.원리공유문제).trim() === '').length;
		const empty오답시나리오 = problems.filter(p => !p.오답시나리오 || String(p.오답시나리오).trim() === '').length;
		
		console.log('\n' + '='.repeat(80));
		console.log('[최종 통계]');
		console.log('='.repeat(80));
		console.log(`총 페이지 수: ${problems.length}개`);
		console.log(`원리공유문제 비어있음: ${empty원리공유문제}개`);
		console.log(`오답시나리오 비어있음: ${empty오답시나리오}개`);
		console.log(`업데이트 완료: ${updatedCount}개`);
		console.log(`업데이트 실패: ${errorCount}개`);
		console.log(`소요 시간: ${elapsedTime}초`);
		
		await logger.info('FILL_FIELDS', '작업 완료', {
			total: problems.length,
			updated: updatedCount,
			errors: errorCount,
			empty원리공유문제,
			empty오답시나리오,
			elapsedTime: `${elapsedTime}초`
		});
		
	} catch (error) {
		const elapsedTime = ((Date.now() - startTime) / 1000).toFixed(2);
		console.error('\n❌ 필드 채우기 오류:', error.message);
		if (error.code) {
			console.error(`   코드: ${error.code}`);
		}
		console.error(error.stack);
		
		await logger.error('FILL_FIELDS', '작업 실패', {
			error: error.message,
			code: error.code,
			elapsedTime: `${elapsedTime}초`,
			stack: error.stack
		});
		
		throw error;
	}
}

async function main() {
	const startTime = Date.now();
	
	try {
		await fillMissingFields();
		
		const totalTime = ((Date.now() - startTime) / 1000).toFixed(2);
		console.log('\n' + '='.repeat(80));
		console.log('✅ 작업 완료!');
		console.log(`총 소요 시간: ${totalTime}초`);
		console.log('='.repeat(80));
		
		process.exit(0);
		
	} catch (error) {
		const totalTime = ((Date.now() - startTime) / 1000).toFixed(2);
		console.error('\n❌ 실행 중 오류 발생:', error);
		console.error(`소요 시간: ${totalTime}초`);
		
		await logger.error('MAIN', '프로그램 실행 실패', {
			error: error.message,
			elapsedTime: `${totalTime}초`
		});
		
		process.exit(1);
	}
}

main();
