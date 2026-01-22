// fix_haktong_p3_notion_concepts.js
// 확통_2024학년도_현우진_드릴_P3 노션 핵심개념 필드 수정

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

// 문제 내용 기반 핵심개념 추출
function extractCoreConcept(problem, solution) {
	const concepts = [];
	
	if (!problem) return null;
	
	const question = problem.question || '';
	const solutionContent = solution?.content || '';
	const topic = problem.topic || '';
	
	// 대소 관계의 조건 (중복조합)
	if (question.includes('≤') || question.includes('≥') || question.includes('<') || question.includes('>')) {
		if (question.includes('자연수') || question.includes('정수')) {
			concepts.push('대소 관계의 조건');
			concepts.push('중복조합');
			if (question.includes('차') || question.includes('최댓값') || question.includes('최솟값')) {
				concepts.push('차를 새로운 미지수로 잡기');
			}
		}
	}
	
	// 함수의 개수
	if (question.includes('함수') && question.includes('개수')) {
		concepts.push('함수의 개수');
		if (question.includes('집합') && question.includes('→')) {
			if (question.includes('치역')) {
				concepts.push('치역의 조건이 있는 함수의 개수');
			}
			if (question.includes('≤') || question.includes('≥')) {
				concepts.push('순서가 정해진 배열');
				concepts.push('중복조합');
			}
			if (question.includes('≠') || question.includes('일대일')) {
				concepts.push('일대일함수');
				concepts.push('순열');
			}
		}
	}
	
	// 이항정리
	if (question.includes('다항식') && question.includes('전개식')) {
		concepts.push('이항정리');
		concepts.push('이항계수');
		if (question.includes('유리수') || question.includes('무리수')) {
			concepts.push('계수가 유리수/무리수인 항의 판별');
		}
	}
	
	// 확률
	if (question.includes('확률') || topic === '확률') {
		concepts.push('수학적 확률');
		if (question.includes('근원사건') || question.includes('표본공간')) {
			concepts.push('근원사건');
		}
		if (question.includes('여사건') || question.includes('드모르간')) {
			concepts.push('여사건의 활용');
		}
		if (question.includes('곱이') && (question.includes('짝수') || question.includes('홀수'))) {
			concepts.push('곱이 짝수/홀수');
			concepts.push('여사건');
		}
	}
	
	// 해설 내용 기반 보완
	if (solutionContent) {
		if (solutionContent.includes('중복조합') || solutionContent.includes('H_')) {
			if (!concepts.includes('중복조합')) {
				concepts.push('중복조합');
			}
		}
		if (solutionContent.includes('이항정리')) {
			if (!concepts.includes('이항정리')) {
				concepts.push('이항정리');
			}
		}
		if (solutionContent.includes('함수의 개수')) {
			if (!concepts.includes('함수의 개수')) {
				concepts.push('함수의 개수');
			}
		}
	}
	
	return concepts.length > 0 ? concepts.join(', ') : null;
}

// 문제구조 추출
function extractProblemStructure(problem) {
	if (!problem) return null;
	
	const question = problem.question || '';
	const answerType = problem.answer_type || '';
	
	const structures = [];
	
	if (answerType === 'multiple_choice') {
		structures.push('객관식');
		structures.push('5지선다');
	}
	
	if (answerType === 'short_answer') {
		structures.push('주관식');
		structures.push('서술형');
	}
	
	// 조건 개수 확인
	const conditionCount = (question.match(/\(가\)|\(나\)|\(다\)/g) || []).length;
	if (conditionCount > 0) {
		structures.push(`조건 ${conditionCount}개`);
	}
	
	// 문제 유형
	if (question.includes('함수') && question.includes('개수')) {
		structures.push('함수의 개수');
	}
	if (question.includes('다항식') && question.includes('전개식')) {
		structures.push('이항정리');
	}
	if (question.includes('확률')) {
		structures.push('확률 계산');
	}
	
	return structures.length > 0 ? structures.join(', ') : null;
}

async function fixHaktongP3Concepts() {
	console.log('='.repeat(80));
	console.log('확통_2024학년도_현우진_드릴_P3 노션 핵심개념 필드 수정');
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
		
		// 문제 번호 매핑 (문제 index와 노션 문제 번호 매칭)
		// 문제 JSON의 index: "18", "02", "03", "04", "05", "23", "20", "11", "12"
		// 노션 문제ID: P3_01, P3_02, P3_03, P3_04, P3_05, P3_06, P3_07, P3_08, P3_09
		const problemMapping = {
			'01': 0,  // 문제 18
			'02': 1,  // 문제 02
			'03': 2,  // 문제 03
			'04': 3,  // 문제 04
			'05': 4,  // 문제 05
			'06': 5,  // 문제 23
			'07': 6,  // 문제 20
			'08': 7,  // 문제 11
			'09': 8   // 문제 12
		};
		
		let updatedCount = 0;
		
		for (const page of allPages) {
			const props = page.properties;
			const 문제ID = extractPropertyValue(props['문제ID']);
			
			console.log(`\n📄 처리 중: ${문제ID}`);
			
			// 문제 번호 추출
			const problemMatch = 문제ID.match(/P3[_\s]?(\d+)/);
			if (!problemMatch) {
				console.log(`  ⚠️  문제 번호를 찾을 수 없음: ${문제ID}`);
				continue;
			}
			
			const problemNum = problemMatch[1];
			const problemIndex = problemMapping[problemNum];
			
			if (problemIndex === undefined || problemIndex < 0 || problemIndex >= problems.length) {
				console.log(`  ⚠️  문제 인덱스 범위 초과: ${problemNum}`);
				continue;
			}
			
			const problem = problems[problemIndex];
			const solution = solutions[problemIndex] || solutions[problemIndex % solutions.length];
			
			// 현재 노션 필드
			const 현재핵심개념 = extractPropertyValue(props['핵심개념']);
			const 현재문제구조 = extractPropertyValue(props['문제구조']);
			const 현재중단원 = extractPropertyValue(props['중단원']);
			
			// 새로운 핵심개념 추출
			const 새로운핵심개념 = extractCoreConcept(problem, solution);
			const 새로운문제구조 = extractProblemStructure(problem);
			
			// 중단원 확인 및 수정
			const 새로운중단원 = problem.topic || 현재중단원;
			
			const updateProps = {};
			let needsUpdate = false;
			
			// 핵심개념 수정
			if (새로운핵심개념 && 새로운핵심개념 !== 현재핵심개념) {
				updateProps['핵심개념'] = {
					rich_text: [
						{
							text: {
								content: 새로운핵심개념
							}
						}
					]
				};
				needsUpdate = true;
				console.log(`  ✅ 핵심개념 수정: "${현재핵심개념}" → "${새로운핵심개념}"`);
			}
			
			// 문제구조 수정
			if (새로운문제구조 && 새로운문제구조 !== 현재문제구조) {
				updateProps['문제구조'] = {
					rich_text: [
						{
							text: {
								content: 새로운문제구조
							}
						}
					]
				};
				needsUpdate = true;
				console.log(`  ✅ 문제구조 수정: "${현재문제구조 || '(비어있음)'}" → "${새로운문제구조}"`);
			}
			
			// 중단원 수정 (필요한 경우)
			if (새로운중단원 && 새로운중단원 !== 현재중단원) {
				// 중단원이 select 타입인지 확인
				const 중단원Prop = props['중단원'];
				if (중단원Prop && 중단원Prop.type === 'select') {
					updateProps['중단원'] = {
						select: {
							name: 새로운중단원
						}
					};
					needsUpdate = true;
					console.log(`  ✅ 중단원 수정: "${현재중단원}" → "${새로운중단원}"`);
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
				console.log(`  ℹ️  업데이트 불필요 (이미 올바름)`);
			}
		}
		
		// 결과 요약
		console.log('\n' + '='.repeat(80));
		console.log('[수정 결과 요약]');
		console.log('='.repeat(80));
		console.log(`총 페이지 수: ${allPages.length}개`);
		console.log(`수정된 페이지: ${updatedCount}개`);
		console.log('\n✅ 작업 완료!');
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
		await fixHaktongP3Concepts();
	} catch (error) {
		console.error('\n❌ 실행 중 오류 발생:', error);
		process.exit(1);
	}
}

main();
