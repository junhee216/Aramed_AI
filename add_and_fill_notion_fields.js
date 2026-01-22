// add_and_fill_notion_fields.js
// 노션 데이터베이스에 두 필드 추가 및 기존 문제 데이터 분석하여 채우기

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
		default:
			return null;
	}
}

// 수학적 원리 추출 함수
function extractMathPrinciple(question, topic, 핵심개념) {
	const principles = [];
	
	// 극한 관련
	if (question.includes('\\lim') || question.includes('극한')) {
		if (question.includes('\\frac') && question.includes('|x|')) {
			principles.push('극한 존재 조건 (인수분해 필요)');
		} else if (question.includes('\\infty')) {
			principles.push('무한대 극한 (최고차항 계수)');
		}
	}
	
	// 미분 관련
	if (question.includes('미분가능') || question.includes('f\'') || question.includes('도함수')) {
		if (question.includes('\\begin{cases}')) {
			principles.push('구간별 함수의 미분가능성 (연속성 + 미분계수 일치)');
		} else if (question.includes('|f(x)|')) {
			principles.push('절댓값 함수의 미분가능성 (접점/교점 판단)');
		}
	}
	
	// 삼차함수 관련
	if (question.includes('삼차함수') || 핵심개념?.includes('삼차함수')) {
		if (question.includes('비율') || 핵심개념?.includes('비율')) {
			principles.push('삼차함수 비율 관계 (2:1, 1:2, 1:√3)');
		}
		if (question.includes('변곡점') || 핵심개념?.includes('변곡점')) {
			principles.push('삼차함수 변곡점 대칭성');
		}
		if (question.includes('접선') || 핵심개념?.includes('접선')) {
			principles.push('삼차함수 접선의 비율 관계');
		}
	}
	
	// 집합 관련
	if (question.includes('A=') && question.includes('B=')) {
		principles.push('집합 연산과 함수의 교점/접점 관계');
	}
	
	// 합성함수 관련
	if (question.includes('f(f(x))') || question.includes('합성함수')) {
		principles.push('합성함수 방정식의 대응 관계');
	}
	
	// 적분 관련
	if (question.includes('\\int') || question.includes('적분')) {
		if (question.includes('|f\'')) {
			principles.push('절댓값 도함수의 정적분');
		}
	}
	
	return principles.length > 0 ? principles.join('; ') : null;
}

// 원리 공유 문제 찾기
function findPrincipleSharedProblems(currentProblem, allProblems) {
	const currentPrinciple = extractMathPrinciple(
		currentProblem.question || '',
		currentProblem.topic || '',
		currentProblem.핵심개념 || ''
	);
	
	if (!currentPrinciple) return [];
	
	const shared = [];
	for (const prob of allProblems) {
		if (prob.id === currentProblem.id) continue;
		
		const otherPrinciple = extractMathPrinciple(
			prob.question || '',
			prob.topic || '',
			prob.핵심개념 || ''
		);
		
		if (otherPrinciple && otherPrinciple === currentPrinciple) {
			shared.push(prob.문제ID || prob.id);
		}
	}
	
	return shared;
}

// 오답 시나리오 생성
function generateErrorScenario(question, 함정설계, 실수포인트, 핵심개념) {
	const scenarios = [];
	
	// 함정설계 기반
	if (함정설계) {
		scenarios.push(`[함정] ${함정설계}`);
	}
	
	// 실수포인트 기반
	if (실수포인트) {
		const points = 실수포인트.split(/[1-9]\./).filter(p => p.trim());
		points.forEach((point, i) => {
			if (point.trim()) {
				scenarios.push(`[실수 ${i+1}] ${point.trim()}`);
			}
		});
	}
	
	// 문제 유형별 일반적 오답 시나리오
	if (question?.includes('미분가능')) {
		if (question.includes('\\begin{cases}')) {
			scenarios.push('[오답] 연결 지점에서 함숫값 일치를 확인하지 않고 미분계수만 확인');
		}
		if (question.includes('|f(x)|')) {
			scenarios.push('[오답] f(x)=0인 점에서 |f(x)|의 미분가능성을 접점 여부로 판단하지 않음');
		}
	}
	
	if (question?.includes('극한') && question.includes('\\frac')) {
		scenarios.push('[오답] 분모가 0이 되는 경우를 고려하지 않고 바로 대입');
	}
	
	if (question?.includes('삼차함수') && question.includes('비율')) {
		scenarios.push('[오답] 비율 관계를 적용할 때 내분점/외분점 위치를 잘못 판단');
	}
	
	if (question?.includes('합성함수')) {
		scenarios.push('[오답] f(x)=t 치환 후 t와 x의 관계를 혼동');
	}
	
	return scenarios.length > 0 ? scenarios.join('\\n') : null;
}

async function addFieldsToDatabase() {
	console.log('='.repeat(80));
	console.log('노션 데이터베이스에 필드 추가');
	console.log('='.repeat(80));
	
	try {
		await rateLimiter.waitIfNeeded();
		
		// 데이터베이스 정보 가져오기
		const db = await notion.databases.retrieve({
			database_id: databaseId
		});
		
		// 이미 필드가 있는지 확인
		const existingProps = db.properties;
		const has원리공유문제 = '원리공유문제' in existingProps;
		const has오답시나리오 = '오답시나리오' in existingProps;
		
		if (has원리공유문제 && has오답시나리오) {
			console.log('✅ 필드가 이미 존재합니다.');
			return true;
		}
		
		// 새 속성 추가
		const newProperties = {};
		
		if (!has원리공유문제) {
			newProperties['원리공유문제'] = {
				rich_text: {}
			};
		}
		
		if (!has오답시나리오) {
			newProperties['오답시나리오'] = {
				rich_text: {}
			};
		}
		
		if (Object.keys(newProperties).length > 0) {
			await rateLimiter.waitIfNeeded();
			await notion.databases.update({
				database_id: databaseId,
				properties: newProperties
			});
			
			console.log('✅ 필드 추가 완료:');
			Object.keys(newProperties).forEach(field => {
				console.log(`  - ${field}`);
			});
		}
		
		return true;
		
	} catch (error) {
		console.error('❌ 필드 추가 오류:', error.message);
		if (error.code === 'validation_error') {
			console.error('   필드명이 이미 존재하거나 형식이 올바르지 않습니다.');
		}
		return false;
	}
}

async function fillFieldsForProblems() {
	console.log('\n' + '='.repeat(80));
	console.log('기존 문제 데이터 분석 및 필드 채우기');
	console.log('='.repeat(80));
	
	try {
		// 모든 페이지 가져오기 (미적분, 수1, 수2 P4까지)
		const allPages = await collectPaginatedAPI(notion.databases.query, {
			database_id: databaseId,
			filter: {
				or: [
					{
						property: '문제ID',
						title: {
							contains: '수1_2025'
						}
					},
					{
						property: '문제ID',
						title: {
							contains: '수2_2025'
						}
					},
					{
						property: '문제ID',
						title: {
							contains: '미적분_2025'
						}
					}
				]
			}
		});
		
		console.log(`\n📖 총 ${allPages.length}개 페이지 발견\n`);
		
		// 문제 데이터 구조화
		const problems = [];
		for (const page of allPages) {
			const props = page.properties;
			const problem = {
				id: page.id,
				문제ID: extractPropertyValue(props['문제ID']),
				question: extractPropertyValue(props['핵심패턴']) || extractPropertyValue(props['LaTeX예시']) || '',
				topic: extractPropertyValue(props['중단원']) || extractPropertyValue(props['대단원']) || '',
				핵심개념: extractPropertyValue(props['핵심개념']) || '',
				함정설계: extractPropertyValue(props['함정설계']) || '',
				실수포인트: extractPropertyValue(props['실수포인트']) || '',
			};
			problems.push(problem);
		}
		
		// 각 문제에 대해 필드 채우기
		let updatedCount = 0;
		
		for (const problem of problems) {
			// 원리공유문제 찾기
			const sharedProblems = findPrincipleSharedProblems(problem, problems);
			const 원리공유문제 = sharedProblems.length > 0 
				? sharedProblems.slice(0, 3).join(', ') 
				: null;
			
			// 오답시나리오 생성
			const 오답시나리오 = generateErrorScenario(
				problem.question,
				problem.함정설계,
				problem.실수포인트,
				problem.핵심개념
			);
			
			// 업데이트할 속성 준비
			const updateProps = {};
			
			if (원리공유문제) {
				updateProps['원리공유문제'] = {
					rich_text: [
						{
							text: {
								content: 원리공유문제
							}
						}
					]
				};
			}
			
			if (오답시나리오) {
				updateProps['오답시나리오'] = {
					rich_text: [
						{
							text: {
								content: 오답시나리오
							}
						}
					]
				};
			}
			
			// 업데이트 실행
			if (Object.keys(updateProps).length > 0) {
				await rateLimiter.waitIfNeeded();
				await notion.pages.update({
					page_id: problem.id,
					properties: updateProps
				});
				
				updatedCount++;
				console.log(`✅ ${problem.문제ID || problem.id.substring(0, 8)}... 업데이트 완료`);
			}
		}
		
		console.log(`\n✅ 총 ${updatedCount}개 페이지 업데이트 완료`);
		
	} catch (error) {
		console.error('\n❌ 필드 채우기 오류:', error.message);
		if (error.code) {
			console.error(`   코드: ${error.code}`);
		}
	}
}

async function main() {
	try {
		// 1단계: 필드 추가
		const success = await addFieldsToDatabase();
		
		if (!success) {
			console.error('❌ 필드 추가 실패. 작업을 중단합니다.');
			return;
		}
		
		// 2단계: 필드 채우기
		await fillFieldsForProblems();
		
		console.log('\n' + '='.repeat(80));
		console.log('✅ 작업 완료!');
		console.log('='.repeat(80));
		
	} catch (error) {
		console.error('\n❌ 실행 중 오류 발생:', error);
		process.exit(1);
	}
}

main();
