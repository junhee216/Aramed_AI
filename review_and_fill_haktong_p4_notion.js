// review_and_fill_haktong_p4_notion.js
// 확통_2024학년도_현우진_드릴_P4 노션 데이터 검토 및 26번, 27번 필드 채우기

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

// 수학적 원리 추출 (확통 P4 특화 - 확률 중심)
function extractMathPrinciple(question, topic, 핵심개념, 중단원) {
	const principles = [];
	
	if (!question) return principles;
	
	const q = question.toLowerCase();
	
	// 사건의 독립
	if (q.includes('독립') || q.includes('종속')) {
		principles.push('사건의 독립: P(B|A) = P(B) 또는 P(A|B) = P(A), P(A ∩ B) = P(A)P(B)');
		principles.push('이중분할표에서 비의 일치로 독립 확인 가능');
	}
	
	// 독립시행
	if (q.includes('시행') && (q.includes('반복') || q.includes('번 던져') || q.includes('번 반복'))) {
		principles.push('독립시행: 동일한 조건에서 시행을 되풀이할 때 각 시행의 결과가 다른 시행에 영향을 주지 않음');
		principles.push('독립시행에서 사건 A가 r회 일어날 확률: ${}_n C_r p^r (1-p)^{n-r}$');
	}
	
	// 조건부확률
	if (q.includes('조건부') || q.includes('일 때') || q.includes('일 확률은')) {
		if (q.includes('확률은') && q.includes('일 때')) {
			principles.push('조건부확률: P(B|A) = P(A ∩ B)/P(A) = n(A ∩ B)/n(A)');
			principles.push('조건부확률에서 표본공간이 축소됨: 전사건이 주어지고 그 일부에 대해 다루면 표본공간을 축소');
		}
	}
	
	// 여사건
	if (q.includes('여사건') || q.includes('적어도') || q.includes('아닐 확률')) {
		principles.push('여사건의 활용: 조건이 복잡할 때 반대 조건을 생각');
		principles.push('조건부확률에서 여사건: P(B|A) = 1 - P(B^C|A), 단 축소된 표본공간을 벗어나지 말아야 함');
	}
	
	// 축소된 표본공간
	if (q.includes('일 때') && q.includes('확률은')) {
		principles.push('축소된 표본공간: 조건부확률에서 전사건이 주어지고 그 일부에 대해 다룰 때 표본공간을 축소');
		principles.push('축소된 표본공간의 케이스가 나누어질 때: P(B|A) = (n(B₁) + n(B₂))/(n(A₁) + n(A₂)), 덧셈정리로 잘못 다루지 않도록 주의');
	}
	
	// 함수의 대응 관계
	if (q.includes('함수') && (q.includes('치역') || q.includes('합성함수'))) {
		principles.push('함수의 대응 관계: 정의역의 원소와 공역의 원소 사이의 대응 관계를 그려보는 것이 도움');
		principles.push('함수의 치역과 합성함수의 치역이 같으면 일대일대응이어야 함');
	}
	
	// 경우의 수에 의한 확률
	if (q.includes('확률') && (q.includes('경우의 수') || q.includes('개수'))) {
		principles.push('경우의 수에 의한 확률: 모든 대상은 같은 확률을 가지는 서로 다른 것으로 봄');
		principles.push('순서는 분모와 분자에 모두 고려하거나 모두 고려하지 않음');
	}
	
	// 핵심개념 기반
	if (핵심개념) {
		const 핵심개념List = 핵심개념.split(/[,;]/).map(c => c.trim());
		for (const concept of 핵심개념List) {
			if (concept.includes('독립') || concept.includes('종속')) {
				principles.push('사건의 독립과 종속의 확인 방법');
			}
			if (concept.includes('조건부확률')) {
				principles.push('조건부확률의 체크리스트: 상황 파악, 경우의 수/확률 선택, 케이스 구분, 발생 순서, 이중분할표 활용');
			}
			if (concept.includes('여사건')) {
				principles.push('여사건의 활용과 축소된 표본공간의 주의점');
			}
		}
	}
	
	return principles.length > 0 ? principles.join('; ') : null;
}

// 오답 시나리오 생성 (확통 P4 특화 - 확률 중심)
function generateErrorScenario(question, 함정설계, 실수포인트, 핵심개념, 중단원) {
	const scenarios = [];
	
	if (!question) return null;
	
	const q = question.toLowerCase();
	
	// 사건의 독립 관련 오류
	if (q.includes('독립') || q.includes('종속')) {
		scenarios.push('[오답] 사건의 독립 확인 시 P(A ∩ B) = P(A)P(B)를 확인하지 않고 주관적으로 판단');
		scenarios.push('[오답] 이중분할표에서 비의 일치를 확인하지 않고 독립이라고 잘못 판단');
		scenarios.push('[오답] P(A|B) = P(A)와 P(B|A) = P(B)를 혼동하거나 하나만 확인하고 독립이라고 판단');
	}
	
	// 독립시행 관련 오류
	if (q.includes('시행') && (q.includes('반복') || q.includes('번 던져') || q.includes('번 반복'))) {
		scenarios.push('[오답] 독립시행의 상황임을 인지하지 못해 풀이의 방향을 잡지 못함');
		scenarios.push('[오답] 독립시행에서 ${}_n C_r$가 아닌 다른 경우의 수가 필요한 상황을 놓침');
		scenarios.push('[오답] 매회의 시행에서 사건이 일어날 확률 p가 일정하다는 것을 확인하지 않음');
	}
	
	// 조건부확률 관련 오류
	if (q.includes('조건부') || (q.includes('일 때') && q.includes('확률은'))) {
		scenarios.push('[오답] 조건부확률에서 표본공간이 축소된다는 것을 고려하지 않음');
		scenarios.push('[오답] P(B|A) 계산 시 분모를 전체 표본공간으로 잘못 계산');
		scenarios.push('[오답] 축소된 표본공간의 케이스가 나누어질 때 확률의 덧셈정리로 잘못 계산: P(B|A) ≠ P(B|A₁) + P(B|A₂)');
		scenarios.push('[오답] 조건부확률에서 이중분할표를 활용하지 않아 계산이 복잡해짐');
	}
	
	// 여사건 관련 오류
	if (q.includes('여사건') || q.includes('적어도') || q.includes('아닐 확률')) {
		scenarios.push('[오답] 여사건을 이용할 때 축소된 표본공간을 벗어나 P(B^C)를 구하는 실수');
		scenarios.push('[오답] 조건부확률에서 여사건 이용 시 P(A ∩ B^C)를 구해야 하는데 P(B^C)를 구함');
		scenarios.push('[오답] 여사건이 더 복잡한 경우를 고려하지 않고 무조건 여사건을 이용');
	}
	
	// 함수의 대응 관계 관련 오류
	if (q.includes('함수') && (q.includes('치역') || q.includes('합성함수'))) {
		scenarios.push('[오답] 함수의 치역과 합성함수의 치역이 같다는 것의 의미를 대응 관계로 파악하지 못함');
		scenarios.push('[오답] 치역의 원소의 개수에 따라 케이스를 구분하지 않고 한 번에 계산하려고 시도');
	}
	
	// 경우의 수에 의한 확률 관련 오류
	if (q.includes('확률') && (q.includes('경우의 수') || q.includes('개수'))) {
		scenarios.push('[오답] 경우의 수로 확률을 계산할 때 순서를 분모와 분자에 다르게 고려');
		scenarios.push('[오답] 모든 대상이 같은 확률을 가지는 서로 다른 것으로 보지 않고 중복을 허용');
		scenarios.push('[오답] 주어진 조건 이외의 경우의 수를 분모와 분자에서 다르게 계산');
	}
	
	// 함정설계 기반
	if (함정설계) {
		// 숫자. 패턴으로 분리 (예: "1. 내용 2. 내용")
		// 정규식으로 "숫자. " 패턴을 찾아서 분리
		const 함정Parts = [];
		const matches = 함정설계.matchAll(/\d+\.\s*([^\d]+?)(?=\d+\.|$)/g);
		for (const match of matches) {
			const part = match[1].trim();
			if (part && part.length > 0) {
				함정Parts.push(part);
			}
		}
		
		for (let i = 0; i < Math.min(함정Parts.length, 5); i++) {
			const part = 함정Parts[i].trim();
			if (part && part.length > 0) {
				// 전체 내용을 포함 (길이 제한 없음)
				scenarios.push(`[함정] ${part}`);
			}
		}
	}
	
	// 실수포인트 기반
	if (실수포인트) {
		// 숫자. 패턴으로 분리 (예: "1. $\sin x$ 부호 변화 무시 2. 연결부 불연속 간과 3. 수열 대입 실수 과 0")
		// 공백이 없을 수도 있으므로 \s* 대신 더 유연한 패턴 사용
		// 예: "1. 내용1 2. 내용2 3. 내용3" 또는 "1.내용1 2.내용2 3.내용3" -> ["내용1", "내용2", "내용3"]
		const 실수Parts = [];
		// 숫자. 다음에 오는 내용을 다음 숫자. 또는 끝까지 추출
		const matches = 실수포인트.matchAll(/\d+\.\s*([^\d]+?)(?=\s*\d+\.|$)/g);
		for (const match of matches) {
			const part = match[1].trim();
			if (part && part.length > 0) {
				실수Parts.push(part);
			}
		}
		
		// 매칭이 실패하면 더 단순한 방법 시도
		if (실수Parts.length === 0) {
			const parts = 실수포인트.split(/\d+\./).map(p => p.trim()).filter(p => p !== '');
			실수Parts.push(...parts);
		}
		
		// 각 항목을 별도 줄로 추가 (전체 내용 포함, 길이 제한 없음)
		for (let i = 0; i < Math.min(실수Parts.length, 10); i++) {
			const part = 실수Parts[i].trim();
			if (part && part.length > 0) {
				// 전체 내용을 포함 (길이 제한 없음)
				scenarios.push(`[실수] ${part}`);
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
	
	// 문제와 노션 필드 일치 확인
	const question = problem?.question || '';
	
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
	if (중단원 === '확률') {
		if (!question.includes('확률') && !question.includes('확률은') && !question.includes('시행')) {
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

async function reviewAndFillHaktongP4() {
	console.log('='.repeat(80));
	console.log('확통_2024학년도_현우진_드릴_P4 노션 데이터 검토 및 26번, 27번 필드 채우기');
	console.log('='.repeat(80));
	
	try {
		// JSON 파일 로드
		const problemsPath = path.resolve('C:\\Users\\a\\Documents\\MathPDF\\organized\\현우진\\확통_2005학년도_현우진_드릴\\확통_2024학년도_현우진_드릴_P4_문제_deepseek.json');
		const solutionsPath = path.resolve('C:\\Users\\a\\Documents\\MathPDF\\organized\\현우진\\확통_2005학년도_현우진_드릴\\확통_2024학년도_현우진_드릴_P4_해설_deepseek.json');
		
		const problems = loadJSONFile(problemsPath);
		const solutions = loadJSONFile(solutionsPath);
		
		if (!problems || !solutions) {
			console.error('❌ JSON 파일을 읽을 수 없습니다.');
			return;
		}
		
		console.log(`\n📖 문제 수: ${problems.length}개`);
		console.log(`📖 해설 수: ${solutions.length}개\n`);
		
		// 노션에서 P4 관련 페이지 찾기
		const allPages = await collectPaginatedAPI(notion.databases.query, {
			database_id: databaseId,
			filter: {
				property: '문제ID',
				title: {
					contains: '확통_2024학년도_현우진_드릴_P4'
				}
			}
		});
		
		console.log(`📖 노션에서 발견된 P4 페이지: ${allPages.length}개\n`);
		
		if (allPages.length === 0) {
			console.log('⚠️  노션에 P4 관련 페이지가 없습니다.');
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
			
			// 문제 번호 추출 (예: P4_03, P4_06 등)
			const problemMatch = 문제ID.match(/P4[_\s]?(\d+)/);
			if (!problemMatch) {
				console.log(`  ⚠️  문제 번호를 찾을 수 없음: ${문제ID}`);
				continue;
			}
			
			const problemNum = parseInt(problemMatch[1]);
			
			// 노션의 문제 내용 가져오기
			const notionQuestion = extractPropertyValue(props['핵심패턴']) || 
			                      extractPropertyValue(props['LaTeX예시']) || '';
			
			// 문제 번호와 내용으로 매칭
			let problem = null;
			let problemIndex = -1;
			
			// 먼저 문제 내용으로 매칭 시도 (가장 정확)
			if (notionQuestion && notionQuestion.trim() !== '') {
				for (let i = 0; i < problems.length; i++) {
					const probQuestion = problems[i].question;
					// 문제 내용의 핵심 키워드로 매칭
					const probKeywords = probQuestion.substring(0, 80).replace(/\$/g, '').replace(/\\/g, '');
					const notionKeywords = notionQuestion.substring(0, 80).replace(/\$/g, '').replace(/\\/g, '');
					
					// 공통 키워드 찾기
					const probWords = probKeywords.split(/\s+/).filter(w => w.length > 2);
					const notionWords = notionKeywords.split(/\s+/).filter(w => w.length > 2);
					const commonWords = probWords.filter(w => notionWords.includes(w));
					
					if (commonWords.length >= 3 || probKeywords.includes(notionKeywords.substring(0, 30)) || 
					    notionKeywords.includes(probKeywords.substring(0, 30))) {
						problem = problems[i];
						problemIndex = i;
						console.log(`  ✅ 문제 내용으로 매칭: 인덱스 ${i} (공통 키워드: ${commonWords.slice(0, 3).join(', ')})`);
						break;
					}
				}
			}
			
			// 내용 매칭 실패 시 index로 매칭 시도
			if (!problem) {
				for (let i = 0; i < problems.length; i++) {
					if (parseInt(problems[i].index) === problemNum) {
						problem = problems[i];
						problemIndex = i;
						console.log(`  ✅ 문제 번호로 매칭: 인덱스 ${i} (번호: ${problemNum})`);
						break;
					}
				}
			}
			
			if (!problem) {
				console.log(`  ⚠️  문제를 찾을 수 없음: ${문제ID} (번호: ${problemNum})`);
				console.log(`     노션 문제 내용: ${notionQuestion.substring(0, 50)}...`);
				continue;
			}
			
			// 해설 매칭 (해설은 문제 순서대로 있으므로 인덱스 사용)
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
			
			// 원리공유문제 (26번) - 이미 채워져 있어도 다시 생성하여 줄바꿈 문제 해결
			if (!원리공유문제 || 원리공유문제.trim() === '') {
				const principle = extractMathPrinciple(
					problem.question,
					problem.topic,
					핵심개념,
					중단원
				);
				
				if (principle) {
					// 원리공유문제는 세미콜론으로 구분된 여러 항목을 줄바꿈으로 표시
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
				problem.question,
				함정설계,
				실수포인트,
				핵심개념,
				중단원
			);
			
			if (scenario) {
				// 노션 API는 \n을 줄바꿈으로 인식하므로 하나의 text 객체에 포함
				// 모든 줄이 표시되도록 보장하기 위해 각 줄을 확인
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
		await reviewAndFillHaktongP4();
	} catch (error) {
		console.error('\n❌ 실행 중 오류 발생:', error);
		process.exit(1);
	}
}

main();
