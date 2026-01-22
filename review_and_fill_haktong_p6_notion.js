// review_and_fill_haktong_p6_notion.js
// 확통_2024학년도_현우진_드릴_P6 노션 필드 검토 및 26, 27번 필드 채우기

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
		default:
			return null;
	}
}

// 수학적 원리 추출 (확통 P6 특화 - 통계 중심)
function extractMathPrinciple(question, topic, 핵심개념, 중단원) {
	const principles = [];
	
	if (!question) return null;
	
	const q = question.toLowerCase();
	
	// 문제별 특수 패턴 인식
	// P6_01: P(X>n+1)={P(X>n)}² 패턴
	if (q.includes('p(x>n+1)') || (q.includes('p(x>') && q.includes('n+1') && q.includes('²'))) {
		principles.push('재귀적 확률 관계: P(X>n+1) = {P(X>n)}²를 이용한 확률 계산');
		principles.push('P(X=1)이 주어지면 P(X>1) = 1 - P(X=1)을 이용하여 P(X>2), P(X>3) 계산');
		principles.push('P(X>3) = P(X=4)이므로 모든 확률을 구할 수 있음');
	}
	
	// P6_02: 이차방정식 x²-x-a_k=0의 실근
	if (q.includes('x²-x-a') || q.includes('x^2-x-a') || 
	    (q.includes('이차방정식') && q.includes('x_{2k-1}') && q.includes('x_{2k}'))) {
		principles.push('이차방정식의 실근과 확률변수: x²-x-a_k=0의 두 실근을 확률변수의 값으로 사용');
		principles.push('모든 값에 대해 동일한 확률: P(X=x_m) = P(X=x_n)일 때 각 확률은 1/20');
		principles.push('근과 계수의 관계: 이차방정식의 두 실근의 합은 1 (x₁+x₂ = 1)');
		principles.push('∑a_k = 10 조건을 이용하여 분산 계산');
	}
	
	// P6_03: 주머니에서 공 꺼내기, 25번 반복
	if ((q.includes('주머니') && q.includes('공') && q.includes('꺼내')) ||
	    (q.includes('공을') && q.includes('확인') && q.includes('시행'))) {
		principles.push('독립시행의 반복: 주머니에서 공을 꺼내는 시행을 반복할 때 각 시행은 독립');
		principles.push('25번 반복 시행: 각 시행의 기댓값과 분산을 구한 후 25배하여 전체 확률변수의 기댓값과 분산 계산');
		principles.push('E(X²) 계산: E(X²) = V(X) + {E(X)}²');
	}
	
	// P6_04: 주사위를 던져 공을 주머니에 넣기
	if (q.includes('주사위') && q.includes('공을') && q.includes('주머니에 넣는')) {
		principles.push('이항분포와 확률변수의 변환: 첫 번째 시행 결과에 따라 이후 시행이 달라지는 경우의 케이스 구분');
		principles.push('첫 번째 시행에서 1개 또는 2개 넣는 확률에 따라 이후 시행 패턴이 달라지는 경우');
		principles.push('확률변수의 변환: Y = aX + b일 때 E(Y) = aE(X) + b');
	}
	
	// P6_05: 연속확률변수, 확률밀도함수, 역함수
	if (q.includes('연속확률변수') && q.includes('확률밀도함수') && q.includes('역함수')) {
		principles.push('연속확률변수의 확률밀도함수: f(x) ≥ 0, ∫[0 to a] f(x)dx = 1');
		principles.push('확률밀도함수의 정적분: P(a ≤ X ≤ b) = ∫[a to b] f(x)dx');
		principles.push('Y의 확률밀도함수가 f(x)의 역함수일 때 변환 관계');
		principles.push('P(f(1/3) ≤ Y ≤ f(5/3)) = 7/9 조건을 이용한 k, a 결정');
	}
	
	// P6_06: 정규분포, f(k) 최댓값
	if (q.includes('정규분포') && q.includes('f(k)') && q.includes('최댓값')) {
		principles.push('정규분포 N(m, σ²): 표준정규분포로 변환하여 확률 계산');
		principles.push('f(k) = P(X≤k) + P(Y≥k)의 최댓값 조건: (a+b)/2 = m일 때 최대');
		principles.push('최댓값이 1.6826이라는 조건으로 m 결정');
	}
	
	// P6_07: 정규분포, f(x) = P(X≤x) 또는 P(Y≥x+2)
	if (q.includes('정규분포') && q.includes('f(x)=') && 
	    q.includes('p(x≤x)') && q.includes('p(y≥x+2)')) {
		principles.push('정규분포 N(m₁,2²), N(m₂,2²): 표준편차가 2로 동일');
		principles.push('f(4) + P(Y≥2) = 1 조건으로 평균 결정');
		principles.push('f(-2) = P(X≤-2) 계산');
	}
	
	// 확률질량함수 관련
	if (q.includes('이산확률변수') || q.includes('확률질량함수') || 
	    (q.includes('확률변수') && (q.includes('p(x=') || q.includes('p(x>') || q.includes('p(x =')))) {
		principles.push('이산확률변수의 확률질량함수: P(X=x_i) = p_i, ∑p_i = 1');
		principles.push('확률질량함수의 성질: 0 ≤ p_i ≤ 1, ∑p_i = 1');
		if (q.includes('p(x>n+1)') || (q.includes('p(x>') && (q.includes('²') || q.includes('^2')))) {
			principles.push('조건부 확률 관계: P(X>n+1) = {P(X>n)}²와 같은 재귀적 관계를 이용한 확률 계산');
			principles.push('재귀적 확률 계산: P(X>2) = {P(X>1)}², P(X>3) = {P(X>2)}² = {P(X>1)}⁴');
			principles.push('P(X=1)이 주어지면 P(X>1) = 1 - P(X=1)을 이용하여 모든 확률 계산 가능');
		}
		if (q.includes('대칭') || q.includes('합의 대칭') || 
		    (q.includes('x₁+x_n') && q.includes('p₁=p_n'))) {
			principles.push('확률변수의 합의 대칭과 확률의 대칭: x₁+x_n = x₂+x_{n-1}이고 p₁=p_n이면 E(X) = (x₁+x_n)/2');
		}
		if (q.includes('a₁+p₁') || (q.includes('등차수열') && q.includes('공차')) ||
		    (q.includes('a_1+p_1') || q.includes('a_2') || q.includes('a_3'))) {
			principles.push('확률질량함수와 등차수열: a_i가 등차수열이고 E(X)=a₂일 때의 관계');
			principles.push('E(X) = a₁p₁ + a₂p₂ + a₃p₃ = a₂ 조건과 V(X) = E(X²) - {E(X)}² = 2 조건을 이용한 계산');
			principles.push('a₁+p₁ = 5/4 조건과 a₁, a₂, a₃가 공차 2인 등차수열 조건을 이용한 연립방정식');
		}
	}
	
	// 분산 계산 관련
	if (q.includes('분산') || q.includes('v(x)') || q.includes('e(x²)')) {
		principles.push('분산의 계산: V(X) = E(X²) - {E(X)}² = ∑(x_i - E(X))²p_i');
		principles.push('분산 계산 방법 선택: (편차)²의 평균 또는 (제곱의 평균) - (평균의 제곱)');
	}
	
	// 이항분포 관련
	if (q.includes('이항분포') || (q.includes('독립시행') && q.includes('확률')) ||
	    (q.includes('시행') && q.includes('반복') && q.includes('확률변수')) ||
	    (q.includes('시행') && q.includes('번 반복') && q.includes('확률변수')) ||
	    ((q.includes('주머니') || q.includes('공')) && q.includes('시행') && q.includes('반복'))) {
		principles.push('이항분포 B(n,p): 독립시행에서 사건의 발생 횟수가 확률변수');
		principles.push('이항분포의 평균과 분산: E(X) = np, V(X) = npq (q = 1-p)');
		if ((q.includes('주머니') && q.includes('공') && (q.includes('반복') || q.includes('시행'))) ||
		    (q.includes('공을') && (q.includes('꺼내') || q.includes('확인')) && q.includes('시행'))) {
			principles.push('독립시행의 반복: 주머니에서 공을 꺼내는 시행을 반복할 때 각 시행은 독립');
			principles.push('E(X²) 계산: E(X²) = V(X) + {E(X)}² = npq + (np)²');
			if (q.includes('25 번') || q.includes('75 개') || q.includes('25번')) {
				principles.push('25번 반복 시행: 각 시행의 기댓값과 분산을 구한 후 25배하여 전체 확률변수의 기댓값과 분산 계산');
			}
		}
		if (q.includes('변환') || q.includes('y = ax + b') || q.includes('e(2x)') || q.includes('e(2 x)') ||
		    q.includes('e(2x)') || q.includes('e(2 x)')) {
			principles.push('확률변수의 변환: Y = aX + b일 때 E(Y) = aE(X) + b, V(Y) = a²V(X)');
		}
		if ((q.includes('주사위') && q.includes('공을') && q.includes('넣는')) ||
		    (q.includes('주사위') && q.includes('공을 주머니에 넣는')) ||
		    (q.includes('주사위') && q.includes('공을') && q.includes('주머니'))) {
			principles.push('이항분포와 확률변수의 변환: 첫 번째 시행 결과에 따라 이후 시행이 달라지는 경우의 케이스 구분');
			principles.push('첫 번째 시행에서 1개 또는 2개 넣는 확률에 따라 이후 시행 패턴이 달라지는 경우');
		}
	}
	
	// 확률밀도함수 관련
	if (q.includes('연속확률변수') || q.includes('확률밀도함수')) {
		principles.push('연속확률변수의 확률밀도함수: f(x) ≥ 0, ∫f(x)dx = 1');
		principles.push('확률밀도함수의 정적분: P(a ≤ X ≤ b) = ∫[a to b] f(x)dx');
		principles.push('연속확률변수에서 P(X=c) = 0 (c는 상수)');
		if (q.includes('역함수')) {
			principles.push('확률밀도함수의 역함수: Y의 확률밀도함수가 f(x)의 역함수일 때 변환 관계');
		}
	}
	
	// 정규분포 관련
	if (q.includes('정규분포') || q.includes('n(')) {
		principles.push('정규분포 N(m, σ²): 표준정규분포로 변환하여 확률 계산');
		principles.push('표준정규분포표 이용: P(x₁ ≤ X ≤ x₂) = P((x₁-m)/σ ≤ Z ≤ (x₂-m)/σ)');
		if (q.includes('최댓값') || q.includes('최대')) {
			principles.push('정규분포에서 확률의 최댓값: b-a가 일정하면 (a+b)/2 = m일 때 최대');
		}
		if (q.includes('합동') || q.includes('교점')) {
			principles.push('정규분포 확률밀도함수의 합동: 표준편차가 같으면 평균에 관계없이 합동, 교점은 (m₁+m₂)/2');
		}
		if (q.includes('높이') || q.includes('표준편차')) {
			principles.push('정규분포 확률밀도함수의 높이: 표준편차가 커지면 높이 작아지고, 작아지면 높이 커짐');
		}
	}
	
	// 표본평균 관련
	if (q.includes('표본평균') || q.includes('x̄') || q.includes('\\bar{x}')) {
		principles.push('표본평균의 분산: V(Ẋ) = V(X)/n (n은 표본 크기)');
		principles.push('표본평균의 확률분포: 모집단이 정규분포이면 표본평균도 정규분포');
	}
	
	// 신뢰구간 관련
	if (q.includes('신뢰구간') || q.includes('신뢰도')) {
		principles.push('모평균의 신뢰구간: x̄ ± z_(α/2) × (σ/√n)');
		principles.push('신뢰구간의 길이: 2 × z_(α/2) × (σ/√n), 표본 크기가 커지면 길이 감소');
	}
	
	return principles.length > 0 ? principles.join('; ') : null;
}

// 원리 공유 문제 찾기 (확통 P6 특화)
function findPrincipleSharedProblems(currentProblem, allProblems) {
	const currentPrinciple = extractMathPrinciple(
		currentProblem.question || '',
		currentProblem.topic || '',
		currentProblem.핵심개념 || '',
		currentProblem.중단원 || ''
	);
	
	if (!currentPrinciple) return [];
	
	const shared = [];
	const currentPrincipleList = currentPrinciple.split(';').map(p => p.trim());
	
	for (const prob of allProblems) {
		if (prob.id === currentProblem.id) continue;
		
		const otherPrinciple = extractMathPrinciple(
			prob.question || '',
			prob.topic || '',
			prob.핵심개념 || '',
			prob.중단원 || ''
		);
		
		if (!otherPrinciple) continue;
		
		// 정확히 일치하는 경우
		if (otherPrinciple === currentPrinciple) {
			shared.push(prob.문제ID || prob.id);
			continue;
		}
		
		// 부분 일치 확인 (하나 이상의 원리가 공유되는 경우)
		const otherPrincipleList = otherPrinciple.split(';').map(p => p.trim());
		const commonPrinciples = currentPrincipleList.filter(p => 
			otherPrincipleList.some(op => 
				op.includes(p) || p.includes(op) || 
				// 유사도 체크: 핵심 키워드가 공통되는 경우
				(p.length > 10 && op.length > 10 && 
				 (p.substring(0, 10) === op.substring(0, 10) || 
				  p.includes(op.substring(0, Math.min(15, op.length))) ||
				  op.includes(p.substring(0, Math.min(15, p.length)))))
			)
		);
		
		if (commonPrinciples.length > 0) {
			shared.push(prob.문제ID || prob.id);
		}
	}
	
	// 중단원이나 핵심개념이 같은 경우 우선순위 부여
	const prioritized = shared.sort((a, b) => {
		const probA = allProblems.find(p => (p.문제ID || p.id) === a);
		const probB = allProblems.find(p => (p.문제ID || p.id) === b);
		
		const scoreA = (probA?.중단원 === currentProblem.중단원 ? 2 : 0) +
		              (probA?.핵심개념 === currentProblem.핵심개념 ? 1 : 0);
		const scoreB = (probB?.중단원 === currentProblem.중단원 ? 2 : 0) +
		              (probB?.핵심개념 === currentProblem.핵심개념 ? 1 : 0);
		
		return scoreB - scoreA;
	});
	
	return prioritized;
}

// 오답 시나리오 생성 (확통 P6 특화 - 통계 중심)
function generateErrorScenario(question, 함정설계, 실수포인트, 핵심개념, 중단원) {
	const scenarios = [];
	
	if (!question) return null;
	
	const q = question.toLowerCase();
	
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
	
	// 확률질량함수 관련 오류
	if (q.includes('이산확률변수') || q.includes('확률질량함수')) {
		scenarios.push('[오답] 확률질량함수의 성질 ∑p_i = 1을 확인하지 않음');
		scenarios.push('[오답] P(x_i ≤ X ≤ x_j) = ∑p_k 계산 시 구간 설정 오류');
		if (q.includes('대칭')) {
			scenarios.push('[오답] 확률변수의 합의 대칭 조건을 제대로 확인하지 않고 E(X) = (x₁+x_n)/2를 적용');
		}
	}
	
	// 분산 계산 관련 오류
	if (q.includes('분산') || q.includes('v(x)') || q.includes('e(x²)')) {
		scenarios.push('[오답] 분산 계산 시 V(X) = E(X²) - {E(X)}² 공식을 잘못 적용');
		scenarios.push('[오답] 분산 계산 방법 선택 오류: (편차)²의 평균과 (제곱의 평균)-(평균의 제곱) 중 어느 것이 유리한지 판단 실패');
		scenarios.push('[오답] E(X²) 계산 시 확률을 제대로 적용하지 않음');
	}
	
	// 이항분포 관련 오류
	if (q.includes('이항분포') || (q.includes('독립시행') && q.includes('확률'))) {
		scenarios.push('[오답] 이항분포의 상황임을 인지하지 못함');
		scenarios.push('[오답] E(X) = np, V(X) = npq 공식을 잘못 적용');
		if (q.includes('변환') || q.includes('y = ax + b')) {
			scenarios.push('[오답] 확률변수의 변환 Y = aX + b에서 분산 계산 오류: V(Y) = a²V(X)를 놓침');
			scenarios.push('[오답] 확률변수의 변환에서 평균과 분산의 변환 관계 혼동');
		}
	}
	
	// 확률밀도함수 관련 오류
	if (q.includes('연속확률변수') || q.includes('확률밀도함수')) {
		scenarios.push('[오답] 확률밀도함수에서 f(x)의 함숫값이 확률이 아니라는 것을 놓침');
		scenarios.push('[오답] 연속확률변수에서 P(X=c) = 0임을 고려하지 않음');
		scenarios.push('[오답] 확률밀도함수의 정적분 조건 ∫f(x)dx = 1을 확인하지 않음');
		if (q.includes('역함수')) {
			scenarios.push('[오답] 확률밀도함수의 역함수 변환 관계를 잘못 적용');
			scenarios.push('[오답] Y의 확률밀도함수가 f(x)의 역함수일 때 변환 관계 오류');
		}
	}
	
	// 정규분포 관련 오류
	if (q.includes('정규분포') || q.includes('n(')) {
		scenarios.push('[오답] 정규분포를 표준정규분포로 변환할 때 (X-m)/σ 변환 오류');
		scenarios.push('[오답] 표준정규분포표에서 z 값의 의미를 잘못 해석');
		scenarios.push('[오답] P(a ≤ X ≤ b) 계산 시 구간 설정 오류');
		if (q.includes('최댓값') || q.includes('최대')) {
			scenarios.push('[오답] 정규분포에서 확률의 최댓값 조건 (a+b)/2 = m을 놓침');
		}
		if (q.includes('합동') || q.includes('교점')) {
			scenarios.push('[오답] 정규분포 확률밀도함수의 합동 조건(표준편차가 같아야 함)을 확인하지 않음');
			scenarios.push('[오답] 두 정규분포의 확률밀도함수 교점의 x 좌표 (m₁+m₂)/2를 놓침');
		}
		if (q.includes('높이') || q.includes('표준편차')) {
			scenarios.push('[오답] 정규분포 확률밀도함수의 높이와 표준편차의 관계를 역으로 이해');
		}
	}
	
	// 표본평균 관련 오류
	if (q.includes('표본평균') || q.includes('x̄') || q.includes('\\bar{x}')) {
		scenarios.push('[오답] 표본평균의 분산 V(Ẋ) = V(X)/n 공식을 잘못 적용');
		scenarios.push('[오답] 표본평균의 확률분포가 정규분포임을 인지하지 못함');
		scenarios.push('[오답] 표본 크기 n과 분산의 관계를 잘못 이해');
	}
	
	// 신뢰구간 관련 오류
	if (q.includes('신뢰구간') || q.includes('신뢰도')) {
		scenarios.push('[오답] 신뢰구간 공식 x̄ ± z_(α/2) × (σ/√n)를 잘못 적용');
		scenarios.push('[오답] 신뢰도와 z_(α/2) 값의 대응 관계 오류');
		scenarios.push('[오답] 표본 크기가 커질 때 신뢰구간의 길이 변화를 잘못 이해');
		scenarios.push('[오답] 두 표본의 신뢰구간 관계에서 표본평균과 표본 크기의 관계를 놓침');
	}
	
	return scenarios.length > 0 ? scenarios.join('\n') : null;
}

async function reviewAndFillHaktongP6() {
	console.log('='.repeat(80));
	console.log('확통_2024학년도_현우진_드릴_P6 노션 필드 검토 및 26, 27번 필드 채우기');
	console.log('='.repeat(80));
	
	try {
		// P6 문제만 가져오기
		const pages = await collectPaginatedAPI(notion.databases.query, {
			database_id: databaseId,
			filter: {
				property: '문제ID',
				title: {
					contains: '확통_2024학년도_현우진_드릴_P6'
				}
			}
		});
		
		console.log(`\n📖 총 ${pages.length}개 페이지 발견\n`);
		
		if (pages.length === 0) {
			console.log('❌ P6 문제를 찾을 수 없습니다.');
			return;
		}
		
		// 모든 문제 가져오기 (원리 공유 문제 찾기용)
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
					},
					{
						property: '문제ID',
						title: {
							contains: '확통_2024'
						}
					}
				]
			}
		});
		
		// 모든 문제 데이터 구조화
		const allProblems = [];
		for (const page of allPages) {
			const props = page.properties;
			allProblems.push({
				id: page.id,
				문제ID: extractPropertyValue(props['문제ID']),
				question: extractPropertyValue(props['핵심패턴']) || extractPropertyValue(props['LaTeX예시']) || '',
				topic: extractPropertyValue(props['중단원']) || extractPropertyValue(props['대단원']) || '',
				핵심개념: extractPropertyValue(props['핵심개념']) || '',
				중단원: extractPropertyValue(props['중단원']) || '',
			});
		}
		
		let updatedCount = 0;
		
		// 각 P6 문제에 대해 검토 및 필드 채우기
		for (const page of pages) {
			const props = page.properties;
			const 문제ID = extractPropertyValue(props['문제ID']);
			const question = extractPropertyValue(props['핵심패턴']) || extractPropertyValue(props['LaTeX예시']) || '';
			const 핵심개념 = extractPropertyValue(props['핵심개념']) || '';
			const 중단원 = extractPropertyValue(props['중단원']) || '';
			const 함정설계 = extractPropertyValue(props['함정설계']) || '';
			const 실수포인트 = extractPropertyValue(props['실수포인트']) || '';
			// 해설 필드 찾기 (여러 가능한 필드 이름 확인)
			let 해설 = extractPropertyValue(props['해설']) || 
			           extractPropertyValue(props['25']) || 
			           extractPropertyValue(props['소단원']) || 
			           '';
			
			// 해설이 비어있으면 긴 텍스트가 있는 필드 찾기
			if (!해설 || 해설.trim() === '') {
				for (const [fieldName, prop] of Object.entries(props)) {
					const value = extractPropertyValue(prop);
					// 해설일 가능성이 있는 긴 텍스트 필드 (200자 이상)
					if (value && typeof value === 'string' && value.length > 200) {
						// 해설 관련 키워드가 포함되어 있으면 해설로 간주
						if (value.includes('해설') || value.includes('풀이') || 
						    value.includes('계산') || value.includes('확률') ||
						    value.includes('분산') || value.includes('기댓값') ||
						    value.includes('정규분포') || value.includes('이항분포')) {
							해설 = value;
							console.log(`  📖 해설 필드 발견: ${fieldName} (${해설.length}자)`);
							break;
						}
					}
				}
			}
			const 원리공유문제 = extractPropertyValue(props['원리공유문제']);
			const 오답시나리오 = extractPropertyValue(props['오답시나리오']);
			
			console.log(`\n📝 ${문제ID} 검토 중...`);
			
			// 25번 필드(해설) 수학적 논리 검토
			const mathErrors = [];
			const mathWarnings = [];
			
			if (해설) {
				console.log(`  📖 해설 필드 확인됨 (${해설.length}자)`);
				
				// LaTeX 수식 괄호 검사
				const dollarCount = (해설.match(/\$/g) || []).length;
				const dollarBlockCount = (해설.match(/\$\$/g) || []).length;
				const singleDollarCount = dollarCount - dollarBlockCount * 2;
				
				if (singleDollarCount % 2 !== 0) {
					mathErrors.push('❌ LaTeX 수식 괄호 불일치: $ 기호가 홀수 개');
				}
				
				// 확률질량함수 검토
				if (해설.includes('확률질량함수') || 해설.includes('이산확률변수')) {
					if (!해설.includes('∑') && !해설.includes('합') && !해설.includes('확률의 합') && !해설.includes('= 1')) {
						mathWarnings.push('⚠️ 확률질량함수의 성질 ∑p_i = 1 확인 필요');
					}
					if (해설.includes('P(X>n+1)') && 해설.includes('{P(X>n)}²')) {
						// 재귀적 확률 관계 검토
						if (!해설.includes('P(X>1)') && !해설.includes('P(X=1)')) {
							mathWarnings.push('⚠️ P(X>n+1) = {P(X>n)}² 관계에서 초기값 P(X=1) 또는 P(X>1) 필요');
						}
					}
				}
				
				// 분산 계산 검토
				if (해설.includes('분산') || 해설.includes('V(X)')) {
					if (해설.includes('E(X²)') && !해설.includes('E(X)') && !해설.includes('E(X)²')) {
						mathWarnings.push('⚠️ 분산 계산 시 V(X) = E(X²) - {E(X)}² 공식에서 E(X) 필요');
					}
					if (해설.includes('V(X) =') && !해설.includes('E(X²)') && !해설.includes('E(X)')) {
						mathWarnings.push('⚠️ 분산 계산 방법이 명확하지 않음');
					}
				}
				
				// 정규분포 변환 검토
				if (해설.includes('정규분포') && 해설.includes('N(')) {
					if (해설.includes('표준정규분포표') || 해설.includes('표준정규분포')) {
						if (!해설.includes('(X-m)/σ') && !해설.includes('변환') && !해설.includes('표준화')) {
							mathWarnings.push('⚠️ 정규분포를 표준정규분포로 변환하는 과정 명시 필요');
						}
					}
				}
				
				// 이항분포 검토
				if (해설.includes('이항분포') || (해설.includes('독립시행') && 해설.includes('확률'))) {
					if (해설.includes('E(X)') && !해설.includes('np') && !해설.includes('n×p')) {
						mathWarnings.push('⚠️ 이항분포의 기댓값 E(X) = np 언급 필요');
					}
					if (해설.includes('V(X)') && !해설.includes('npq') && !해설.includes('np(1-p)')) {
						mathWarnings.push('⚠️ 이항분포의 분산 V(X) = npq 언급 필요');
					}
				}
				
				// 확률밀도함수 검토
				if (해설.includes('확률밀도함수') || 해설.includes('연속확률변수')) {
					if (해설.includes('∫') && !해설.includes('= 1') && !해설.includes('정규화')) {
						mathWarnings.push('⚠️ 확률밀도함수의 정규화 조건 ∫f(x)dx = 1 확인 필요');
					}
				}
				
				// 수식 일관성 검토
				if (해설.includes('=') && 해설.includes('≠')) {
					// 등식과 부등식이 혼재되어 있는 경우 일관성 확인
				}
				
			} else {
				mathWarnings.push('⚠️ 해설 필드가 비어있음');
			}
			
			// 문제 자체의 수학적 논리 검토
			if (question.includes('이산확률변수') || question.includes('확률질량함수')) {
				if (!question.includes('∑') && !question.includes('합') && !question.includes('확률의 합')) {
					// 확률의 합이 1인지 확인하는 내용이 없으면 경고
					// (문제에 명시되어 있을 수도 있으므로 경고만)
				}
			}
			
			if (mathErrors.length > 0) {
				console.log(`  ❌ 수학적 논리 오류:`);
				mathErrors.forEach(err => console.log(`     ${err}`));
			}
			
			if (mathWarnings.length > 0) {
				console.log(`  ⚠️ 수학적 논리 경고:`);
				mathWarnings.forEach(warn => console.log(`     ${warn}`));
			}
			
			if (mathErrors.length === 0 && mathWarnings.length === 0 && 해설) {
				console.log(`  ✅ 수학적 논리 검토 통과`);
			}
			
			const updateProps = {};
			let needsUpdate = false;
			
			// 원리공유문제 (26번) - 항상 다시 생성하여 정확한 내용으로 업데이트
			const currentProblem = {
				id: page.id,
				문제ID: 문제ID,
				question: question,
				topic: 중단원,
				핵심개념: 핵심개념,
				중단원: 중단원,
			};
			
			const sharedProblems = findPrincipleSharedProblems(currentProblem, allProblems);
			let 원리공유문제Text;
			
			if (sharedProblems.length > 0) {
				// 원리 공유 문제 ID를 줄바꿈으로 구분
				원리공유문제Text = sharedProblems.slice(0, 5).join('\n');
				console.log(`  ✅ 원리공유문제: ${sharedProblems.length}개 문제 발견 (${sharedProblems.slice(0, 3).join(', ')}...)`);
			} else {
				// 원리 공유 문제가 없으면 핵심 원리 추출
				const principle = extractMathPrinciple(
					question,
					중단원,
					핵심개념,
					중단원
				);
				
				if (principle) {
					// 세미콜론으로 구분된 여러 항목을 줄바꿈으로 표시
					const principleLines = principle.split(';').map(p => p.trim()).filter(p => p !== '');
					원리공유문제Text = principleLines.join('\n');
					console.log(`  ✅ 원리공유문제: 핵심 원리 ${principleLines.length}개 추출`);
				} else {
					원리공유문제Text = '해당 문제와 본질적으로 같은 원리를 공유하는 다른 문제를 찾을 수 없습니다.';
					console.log(`  ⚠️  원리공유문제: 원리 추출 실패`);
				}
			}
			
			// 함정설계 내용이 포함되어 있으면 제거
			if (원리공유문제Text.includes('함정') || 원리공유문제Text.includes('실수') || 
			    원리공유문제Text.includes('1.') && 원리공유문제Text.includes('2.')) {
				// 함정설계 형식이면 원리로 다시 추출
				const principle = extractMathPrinciple(
					question,
					중단원,
					핵심개념,
					중단원
				);
				if (principle) {
					const principleLines = principle.split(';').map(p => p.trim()).filter(p => p !== '');
					원리공유문제Text = principleLines.join('\n');
					console.log(`  🔄 원리공유문제: 함정설계 내용 제거 후 원리로 재생성`);
				}
			}
			
			updateProps['원리공유문제'] = {
				rich_text: [
					{
						text: {
							content: 원리공유문제Text
						}
					}
				]
			};
			needsUpdate = true;
			
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
		console.log(`총 페이지 수: ${pages.length}개`);
		console.log(`업데이트 완료: ${updatedCount}개`);
		console.log('='.repeat(80));
		
	} catch (error) {
		console.error('\n❌ 오류 발생:', error.message);
		if (error.code) {
			console.error(`   코드: ${error.code}`);
		}
		console.error(error.stack);
	}
}

async function main() {
	try {
		await reviewAndFillHaktongP6();
		
		console.log('\n' + '='.repeat(80));
		console.log('✅ 작업 완료!');
		console.log('='.repeat(80));
		
	} catch (error) {
		console.error('\n❌ 실행 중 오류 발생:', error);
		process.exit(1);
	}
}

main();
