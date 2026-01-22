// review_and_fill_haktong_p5_notion.js
// 확통_2024학년도_현우진_드릴_P5 노션 데이터 검토 및 26번, 27번 필드 채우기

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

// 수학적 원리 추출 (확통 일반)
function extractMathPrinciple(question, 핵심개념, 중단원, 개념연결, 후행개념) {
	const principles = [];
	
	if (!question) {
		// 노션 필드에서 추출
		question = 개념연결 || 후행개념 || '';
	}
	
	const q = question.toLowerCase();
	
	// 확통 관련 원리
	if (중단원 === '경우의 수' || q.includes('경우의 수') || q.includes('순열') || q.includes('조합')) {
		if (q.includes('원순열') || q.includes('원형')) {
			principles.push('원순열: 회전하여 일치하는 것은 같은 것으로 봄, (n-1)!');
		}
		if (q.includes('이웃') || q.includes('이웃하지')) {
			principles.push('이웃하는 것/이웃하지 않는 것의 배열: 이웃하는 것은 묶어서, 이웃하지 않는 것은 여사건 활용');
		}
		if (q.includes('부정방정식') || q.includes('음이 아닌 정수')) {
			principles.push('부정방정식의 정수해: 중복조합 ${}_n H_r$로 계산');
		}
		if (q.includes('여사건') || q.includes('드모르간')) {
			principles.push('여사건의 이용: 드모르간의 법칙, (A∪B)^C = A^C∩B^C');
		}
		if (q.includes('순서가 정해진') || q.includes('≤')) {
			principles.push('순서가 정해진 배열: 중복조합으로 계산');
		}
		if (q.includes('함수') && q.includes('개수')) {
			principles.push('함수의 개수: 모든 함수는 중복순열, 일대일함수는 순열, 순서가 정해진 배열은 조합/중복조합');
		}
	}
	
	if (중단원 === '확률' || q.includes('확률')) {
		principles.push('수학적 확률: P(A) = n(A)/n(S), 근원사건을 제대로 파악하는 것이 중요');
		if (q.includes('여사건') || q.includes('드모르간')) {
			principles.push('여사건의 활용: 조건이 복잡할 때 반대 조건을 생각');
		}
		if (q.includes('독립')) {
			principles.push('사건의 독립: P(A∩B) = P(A)P(B) 또는 P(B|A) = P(B)');
		}
		if (q.includes('조건부확률')) {
			principles.push('조건부확률: P(B|A) = P(A∩B)/P(A), 축소된 표본공간');
		}
		if (q.includes('독립시행')) {
			principles.push('독립시행: 동일 조건 반복, 각 시행 결과 독립, ${}_n C_r p^r (1-p)^{n-r}$');
		}
	}
	
	// 핵심개념 기반
	if (핵심개념) {
		const 핵심개념List = 핵심개념.split(/[,;]/).map(c => c.trim());
		for (const concept of 핵심개념List) {
			if (concept.includes('원순열')) {
				principles.push('원순열: 무엇 하나라도 배치하고 나면 순열로 바뀜');
			}
			if (concept.includes('이항정리')) {
				principles.push('이항정리: $(a+b)^n$의 전개식에서 $a^r b^{n-r}$의 계수는 ${}_n C_r$');
			}
		}
	}
	
	return principles.length > 0 ? principles.join('; ') : null;
}

// 오답 시나리오 생성 (확통 일반)
function generateErrorScenario(question, 함정설계, 실수포인트, 핵심개념, 중단원) {
	const scenarios = [];
	
	if (!question) return null;
	
	const q = question.toLowerCase();
	
	// 확통 관련 오답 시나리오
	if (중단원 === '경우의 수' || q.includes('경우의 수') || q.includes('순열') || q.includes('조합')) {
		if (q.includes('원순열') || q.includes('원형')) {
			scenarios.push('[오답] 원순열에서 회전하여 일치하는 경우를 중복 계산');
			scenarios.push('[오답] 원순열에서 무엇 하나라도 배치하고 나면 순열로 바뀌는 것을 놓침');
		}
		if (q.includes('이웃') || q.includes('이웃하지')) {
			scenarios.push('[오답] 이웃하지 않는 것의 여사건을 잘못 적용 (3개 이상일 때 주의)');
			scenarios.push('[오답] 이웃하는 것과 이웃하지 않는 것의 계산 원칙 혼동');
		}
		if (q.includes('부정방정식') || q.includes('음이 아닌 정수')) {
			scenarios.push('[오답] 자연수 조건을 음이 아닌 정수로 치환할 때 범위 오류');
			scenarios.push('[오답] 새로운 미지수로 치환 후 제외할 경우를 놓침');
		}
		if (q.includes('여사건') || q.includes('드모르간')) {
			scenarios.push('[오답] 드모르간의 법칙 적용 시 합집합과 교집합 혼동');
			scenarios.push('[오답] 여사건 계산 시 중복 제거를 놓침');
		}
		if (q.includes('함수') && q.includes('개수')) {
			scenarios.push('[오답] 함수의 개수에서 모든 함수($b^a$), 일대일함수($_b P_a$), 순서가 정해진 배열($_b C_a$ 또는 $_b H_a$)을 혼동');
		}
	}
	
	if (중단원 === '확률' || q.includes('확률')) {
		scenarios.push('[오답] 수학적 확률에서 근원사건을 제대로 파악하지 못해 분모(전체 경우의 수) 계산 오류');
		if (q.includes('여사건')) {
			scenarios.push('[오답] 여사건을 이용할 때 드모르간의 법칙 적용 오류 또는 여사건이 더 복잡한 경우를 고려하지 않음');
		}
		if (q.includes('독립')) {
			scenarios.push('[오답] 사건의 독립 판단 오류: P(A∩B) = P(A)P(B) 조건을 확인하지 않고 독립으로 간주');
		}
		if (q.includes('조건부확률')) {
			scenarios.push('[오답] 조건부확률에서 축소된 표본공간을 잘못 설정하거나, P(A∩B) 대신 P(B)를 분자에 사용');
		}
		if (q.includes('독립시행')) {
			scenarios.push('[오답] 독립시행 문제에서 ${}_n C_r$을 누락하거나, 각 시행의 확률 p를 잘못 계산');
		}
	}
	
	// 함정설계 기반
	if (함정설계) {
		const 함정Parts = [];
		const matches = 함정설계.matchAll(/\d+\.\s*([^\d]+?)(?=\d+\.|$)/g);
		for (const match of matches) {
			const part = match[1].trim();
			if (part && part.length > 0) {
				함정Parts.push(part);
			}
		}
		
		if (함정Parts.length === 0) {
			const parts = 함정설계.split(/\d+\./).map(p => p.trim()).filter(p => p !== '');
			함정Parts.push(...parts);
		}
		
		for (let i = 0; i < Math.min(함정Parts.length, 5); i++) {
			const part = 함정Parts[i].trim();
			if (part && part.length > 0) {
				scenarios.push(`[함정] ${part}`);
			}
		}
	}
	
	// 실수포인트 기반
	if (실수포인트) {
		const 실수Parts = [];
		const matches = 실수포인트.matchAll(/\d+\.\s*([^\d]+?)(?=\s*\d+\.|$)/g);
		for (const match of matches) {
			const part = match[1].trim();
			if (part && part.length > 0) {
				실수Parts.push(part);
			}
		}
		
		if (실수Parts.length === 0) {
			const parts = 실수포인트.split(/\d+\./).map(p => p.trim()).filter(p => p !== '');
			실수Parts.push(...parts);
		}
		
		for (let i = 0; i < Math.min(실수Parts.length, 10); i++) {
			const part = 실수Parts[i].trim();
			if (part && part.length > 0) {
				scenarios.push(`[실수] ${part}`);
			}
		}
	}
	
	return scenarios.length > 0 ? scenarios.join('\n') : null;
}

// 수학적 논리 검증
function validateMathLogic(notionPage) {
	const errors = [];
	const warnings = [];
	
	const props = notionPage.properties;
	const 문제ID = extractPropertyValue(props['문제ID']);
	const 대단원 = extractPropertyValue(props['대단원']);
	const 중단원 = extractPropertyValue(props['중단원']);
	const 핵심개념 = extractPropertyValue(props['핵심개념']);
	const 문제구조 = extractPropertyValue(props['문제구조']);
	const 개념연결 = extractPropertyValue(props['개념연결']);
	const 후행개념 = extractPropertyValue(props['후행개념']);
	const 선행개념 = extractPropertyValue(props['선행개념']);
	
	// 대단원-중단원 일치 확인
	if (대단원 && 중단원) {
		if (대단원 === '확률과 통계' && !['경우의 수', '확률', '통계'].includes(중단원)) {
			warnings.push(`대단원이 "확률과 통계"인데 중단원이 "${중단원}"으로 일치하지 않음`);
		}
	}
	
	// 핵심개념-해설 일치 확인
	if (핵심개념 && (개념연결 || 후행개념 || 선행개념)) {
		const 해설Text = `${개념연결 || ''} ${후행개념 || ''} ${선행개념 || ''}`;
		const 핵심개념List = 핵심개념.split(/[,;]/).map(c => c.trim());
		
		for (const concept of 핵심개념List) {
			if (concept && concept.length > 3 && !해설Text.includes(concept.substring(0, 5))) {
				warnings.push(`핵심개념 "${concept}"이 해설에 명시적으로 다뤄지지 않음`);
			}
		}
	}
	
	return { errors, warnings };
}

async function reviewAndFillHaktongP5() {
	console.log('='.repeat(80));
	console.log('확통_2024학년도_현우진_드릴_P5 노션 데이터 검토 및 26번, 27번 필드 채우기');
	console.log('='.repeat(80));
	
	try {
		// 노션에서 P5 관련 페이지 찾기
		const allPages = await collectPaginatedAPI(notion.databases.query, {
			database_id: databaseId,
			filter: {
				property: '문제ID',
				title: {
					contains: '확통_2024학년도_현우진_드릴_P5'
				}
			}
		});
		
		console.log(`\n📖 노션에서 발견된 P5 페이지: ${allPages.length}개\n`);
		
		if (allPages.length === 0) {
			console.log('⚠️  노션에 P5 관련 페이지가 없습니다.');
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
			
			// 노션 필드 추출
			const 대단원 = extractPropertyValue(props['대단원']);
			const 중단원 = extractPropertyValue(props['중단원']);
			const 핵심개념 = extractPropertyValue(props['핵심개념']);
			const 문제구조 = extractPropertyValue(props['문제구조']);
			const 함정설계 = extractPropertyValue(props['함정설계']);
			const 실수포인트 = extractPropertyValue(props['실수포인트']);
			const 원리공유문제 = extractPropertyValue(props['원리공유문제']);
			const 오답시나리오 = extractPropertyValue(props['오답시나리오']);
			const 개념연결 = extractPropertyValue(props['개념연결']);
			const 후행개념 = extractPropertyValue(props['후행개념']);
			const LaTeX예시 = extractPropertyValue(props['LaTeX예시']);
			const 핵심패턴 = extractPropertyValue(props['핵심패턴']);
			
			// 문제 내용 추출 (LaTeX예시 또는 핵심패턴 사용)
			const question = LaTeX예시 || 핵심패턴 || 개념연결 || 후행개념 || '';
			
			// 수학적 논리 검증
			const validation = validateMathLogic(page);
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
					question,
					핵심개념,
					중단원,
					개념연결,
					후행개념
				);
				
				if (principle) {
					const principleLines = principle.split(';').map(p => p.trim()).filter(p => p !== '');
					const formattedPrinciple = principleLines.join('\n');
					
					updateProps['원리공유문제'] = {
						rich_text: [
							{
								text: {
									content: formattedPrinciple
								}
							}
						]
					};
					needsUpdate = true;
					console.log(`  ✅ 원리공유문제 생성: ${principleLines.length}개 항목`);
				}
			}
			
			// 오답시나리오 (27번) - 항상 다시 생성하여 줄바꿈 문제 해결
			const scenario = generateErrorScenario(
				question,
				함정설계,
				실수포인트,
				핵심개념,
				중단원
			);
			
			if (scenario) {
				const scenarioLines = scenario.split('\n').filter(line => line.trim() !== '');
				const formattedScenario = scenarioLines.join('\n');
				
				updateProps['오답시나리오'] = {
					rich_text: [
						{
							text: {
								content: formattedScenario
							}
						}
					]
				};
				needsUpdate = true;
				console.log(`  ✅ 오답시나리오 생성/업데이트: ${scenarioLines.length}개 항목`);
				if (scenarioLines.length > 0) {
					console.log(`     첫 항목: ${scenarioLines[0].substring(0, 60)}...`);
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
		await reviewAndFillHaktongP5();
	} catch (error) {
		console.error('\n❌ 실행 중 오류 발생:', error);
		process.exit(1);
	}
}

main();
