// src/utils/math_principle_utils.js
// 수학 원리 추출 및 오답 시나리오 생성 유틸리티

/**
 * 수학적 원리 추출 함수 (확통 포함)
 * @param {string} question - 문제 내용
 * @param {string} topic - 주제/중단원
 * @param {string} 핵심개념 - 핵심 개념
 * @param {string} 중단원 - 중단원
 * @returns {string|null} 추출된 원리 (세미콜론으로 구분)
 */
export function extractMathPrinciple(question, topic = '', 핵심개념 = '', 중단원 = '') {
	const principles = [];
	const q = question || '';
	const t = topic || '';
	const h = 핵심개념 || '';
	const z = 중단원 || '';
	
	// 확통 관련
	if (q.includes('경우의 수') || q.includes('순열') || q.includes('조합')) {
		if (q.includes('원순열') || q.includes('원형')) {
			principles.push('원순열 (회전하여 일치하는 것은 같은 것으로 봄)');
		}
		if (q.includes('이웃') || q.includes('이웃하지')) {
			principles.push('이웃하는 것/이웃하지 않는 것의 배열');
		}
		if (q.includes('부정방정식') || q.includes('음이 아닌 정수')) {
			principles.push('부정방정식의 정수해 (중복조합)');
		}
		if (q.includes('여사건') || q.includes('드모르간')) {
			principles.push('여사건의 이용 (드모르간의 법칙)');
		}
		if (q.includes('순서가 정해진') || q.includes('≤')) {
			principles.push('순서가 정해진 배열 (중복조합)');
		}
	}
	
	// 극한 관련
	if (q.includes('\\lim') || q.includes('극한')) {
		if (q.includes('\\frac') && q.includes('|x|')) {
			principles.push('극한 존재 조건 (인수분해 필요)');
		} else if (q.includes('\\infty')) {
			principles.push('무한대 극한 (최고차항 계수)');
		}
	}
	
	// 미분 관련
	if (q.includes('미분가능') || q.includes('f\'') || q.includes('도함수')) {
		if (q.includes('\\begin{cases}')) {
			principles.push('구간별 함수의 미분가능성 (연속성 + 미분계수 일치)');
		} else if (q.includes('|f(x)|')) {
			principles.push('절댓값 함수의 미분가능성 (접점/교점 판단)');
		}
	}
	
	// 삼차함수 관련
	if (q.includes('삼차함수') || h.includes('삼차함수')) {
		if (q.includes('비율') || h.includes('비율')) {
			principles.push('삼차함수 비율 관계 (2:1, 1:2, 1:√3)');
		}
		if (q.includes('변곡점') || h.includes('변곡점')) {
			principles.push('삼차함수 변곡점 대칭성');
		}
		if (q.includes('접선') || h.includes('접선')) {
			principles.push('삼차함수 접선의 비율 관계');
		}
	}
	
	// 집합 관련
	if (q.includes('A=') && q.includes('B=')) {
		principles.push('집합 연산과 함수의 교점/접점 관계');
	}
	
	// 합성함수 관련
	if (q.includes('f(f(x))') || q.includes('합성함수')) {
		principles.push('합성함수 방정식의 대응 관계');
	}
	
	// 적분 관련
	if (q.includes('\\int') || q.includes('적분')) {
		if (q.includes('|f\'')) {
			principles.push('절댓값 도함수의 정적분');
		}
		if (q.includes('넓이') || q.includes('정적분')) {
			principles.push('정적분과 넓이의 관계');
		}
	}
	
	return principles.length > 0 ? principles.join('; ') : null;
}

/**
 * 원리 공유 문제 찾기 (개선: 유사도 기반)
 * @param {Object} currentProblem - 현재 문제 객체
 * @param {Array<Object>} allProblems - 모든 문제 배열
 * @returns {Array<string>} 원리 공유 문제 ID 배열
 */
export function findPrincipleSharedProblems(currentProblem, allProblems) {
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

/**
 * 오답 시나리오 생성 (확통 포함)
 * @param {string} question - 문제 내용
 * @param {string} 함정설계 - 함정 설계 내용
 * @param {string} 실수포인트 - 실수 포인트 내용
 * @param {string} 핵심개념 - 핵심 개념
 * @param {string} 중단원 - 중단원
 * @returns {string|null} 생성된 오답 시나리오 (줄바꿈으로 구분)
 */
export function generateErrorScenario(question = '', 함정설계 = '', 실수포인트 = '', 핵심개념 = '', 중단원 = '') {
	const scenarios = [];
	const q = (question || '').toLowerCase();
	
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
	
	// 확통 관련 오답 시나리오
	if (q.includes('원순열') || q.includes('원형')) {
		scenarios.push('[오답] 원순열에서 회전하여 일치하는 경우를 중복 계산');
		scenarios.push('[오답] 원순열에서 무엇 하나라도 배치하고 나면 순열로 바뀌는 것을 놓침');
		scenarios.push('[오답] 원순열의 경우를 구별하는 기준이 자리의 위치가 아니라 관계임을 놓침');
	}
	
	if (q.includes('이웃') || q.includes('이웃하지')) {
		scenarios.push('[오답] 이웃하지 않는 것의 여사건을 잘못 적용 (3개 이상일 때 주의)');
		scenarios.push('[오답] 이웃하는 것과 이웃하지 않는 것의 계산 원칙 혼동');
		scenarios.push('[오답] 서로 다른 것과 서로 같은 것의 이웃 계산 방법 혼동');
	}
	
	if (q.includes('부정방정식') || q.includes('음이 아닌 정수') || q.includes('중복조합')) {
		scenarios.push('[오답] 자연수 조건을 음이 아닌 정수로 치환할 때 범위 오류');
		scenarios.push('[오답] 새로운 미지수로 치환 후 제외할 경우를 놓침');
		scenarios.push('[오답] 부정방정식의 정수해에 대한 조건을 새로운 미지수로 치환할 때 범위 설정 오류');
	}
	
	if (q.includes('여사건') || q.includes('드모르간')) {
		scenarios.push('[오답] 드모르간의 법칙 적용 시 합집합과 교집합 혼동');
		scenarios.push('[오답] 여사건 계산 시 중복 제거를 놓침');
		scenarios.push('[오답] (A ∪ B)^C = A^C ∩ B^C, (A ∩ B)^C = A^C ∪ B^C를 잘못 적용');
	}
	
	if (q.includes('순서가 정해진') || q.includes('≤') || q.includes('대소 관계')) {
		scenarios.push('[오답] 순서가 정해진 배열에서 순서 부여를 중복 계산');
		scenarios.push('[오답] 부등식에 등호가 있을 때와 없을 때의 차이를 놓침');
		scenarios.push('[오답] 대소 관계의 조건을 차로 새로운 미지수로 잡을 때 음이 아닌 정수/자연수 구분 오류');
	}
	
	if (q.includes('함수') && (q.includes('개수') || q.includes('경우의 수'))) {
		scenarios.push('[오답] 함수의 개수 계산 시 조건을 제대로 적용하지 않음');
		scenarios.push('[오답] 치역의 조건이 있는 함수의 개수에서 정의역의 원소에 치역의 원소가 대응하는 경우의 수 계산 오류');
		scenarios.push('[오답] 순서가 정해진 배열(중복조합)과 일대일대응(순열)의 구분 오류');
	}
	
	// 확률 관련
	if (q.includes('독립') || q.includes('종속')) {
		scenarios.push('[오답] 사건의 독립 확인 시 P(A ∩ B) = P(A)P(B)를 확인하지 않고 주관적으로 판단');
		scenarios.push('[오답] 이중분할표에서 비의 일치를 확인하지 않고 독립이라고 잘못 판단');
		scenarios.push('[오답] P(A|B) = P(A)와 P(B|A) = P(B)를 혼동하거나 하나만 확인하고 독립이라고 판단');
	}
	
	if (q.includes('시행') && (q.includes('반복') || q.includes('번 던져') || q.includes('번 반복'))) {
		scenarios.push('[오답] 독립시행의 상황임을 인지하지 못해 풀이의 방향을 잡지 못함');
		scenarios.push('[오답] 독립시행에서 ${}_n C_r$가 아닌 다른 경우의 수가 필요한 상황을 놓침');
		scenarios.push('[오답] 매회의 시행에서 사건이 일어날 확률 p가 일정하다는 것을 확인하지 않음');
	}
	
	if (q.includes('조건부') || (q.includes('일 때') && q.includes('확률은'))) {
		scenarios.push('[오답] 조건부확률에서 표본공간이 축소된다는 것을 고려하지 않음');
		scenarios.push('[오답] P(B|A) 계산 시 분모를 전체 표본공간으로 잘못 계산');
		scenarios.push('[오답] 축소된 표본공간의 케이스가 나누어질 때 확률의 덧셈정리로 잘못 계산: P(B|A) ≠ P(B|A₁) + P(B|A₂)');
		scenarios.push('[오답] 조건부확률에서 이중분할표를 활용하지 않아 계산이 복잡해짐');
	}
	
	// 통계 관련
	if (q.includes('확률변수') || q.includes('확률질량함수') || q.includes('확률밀도함수')) {
		scenarios.push('[오답] 확률질량함수의 성질 ∑p_i = 1을 확인하지 않음');
		scenarios.push('[오답] 확률밀도함수에서 f(x)의 함숫값이 확률이 아니라는 것을 놓침');
		scenarios.push('[오답] 연속확률변수에서 P(X=c) = 0임을 고려하지 않음');
	}
	
	if (q.includes('이항분포') || (q.includes('독립시행') && q.includes('확률'))) {
		scenarios.push('[오답] 이항분포의 상황임을 인지하지 못함');
		scenarios.push('[오답] E(X) = np, V(X) = npq 공식을 잘못 적용');
		scenarios.push('[오답] 확률변수의 변환 Y = aX + b에서 분산 계산 오류');
	}
	
	if (q.includes('정규분포') || q.includes('표준정규분포')) {
		scenarios.push('[오답] 정규분포를 표준정규분포로 변환할 때 (X-m)/σ 변환 오류');
		scenarios.push('[오답] 표준정규분포표에서 z 값의 의미를 잘못 해석');
		scenarios.push('[오답] P(a ≤ X ≤ b) 계산 시 구간 설정 오류');
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
	
	if (question?.includes('적분') && question.includes('넓이')) {
		scenarios.push('[오답] 정적분과 넓이의 관계에서 부호 처리 오류');
		scenarios.push('[오답] 넓이 계산 시 구간 분할을 놓침');
	}
	
	return scenarios.length > 0 ? scenarios.join('\n') : null;
}

/**
 * 기하 문제의 수학적 원리 추출 (기하 전용)
 * @param {string} question - 문제 내용
 * @param {string} topic - 주제/중단원
 * @param {string} 핵심개념 - 핵심 개념
 * @param {string} 중단원 - 중단원
 * @returns {string|null} 추출된 원리
 */
export function extractGeometryPrinciple(question, topic = '', 핵심개념 = '', 중단원 = '') {
	const principles = [];
	const q = question || '';
	const h = 핵심개념 || '';
	const z = 중단원 || '';
	
	// 포물선 관련
	if (q.includes('포물선') || h.includes('포물선')) {
		if (q.includes('초점') && q.includes('준선')) {
			principles.push('포물선의 정의: 초점과 준선까지의 거리가 같음 (PF = PI)');
		}
		if (q.includes('y^{2}') || q.includes('y^2')) {
			principles.push('포물선 방정식: y² = 4ax (초점: (a, 0), 준선: x = -a)');
		}
		if (q.includes('직각사다리꼴') || q.includes('사다리꼴')) {
			principles.push('직각사다리꼴을 이용한 포물선 문제');
		}
		if (q.includes('초점을 지나는') || q.includes('초점과')) {
			principles.push('포물선의 초점을 지나는 직선 문제');
		}
	}
	
	// 타원 관련
	if (q.includes('타원') || h.includes('타원')) {
		if (q.includes('초점') && (q.includes('장축') || q.includes('2a'))) {
			principles.push('타원의 정의: 두 초점까지의 거리의 합이 일정 (PF + PF\' = 2a)');
		}
		if (q.includes('장축')) {
			principles.push('타원의 장축과 단축을 이용하는 문제');
		}
		if (q.includes('초점') && q.includes('원')) {
			principles.push('타원의 두 초점을 지름의 양 끝으로 하는 원 문제');
		}
	}
	
	// 쌍곡선 관련
	if (q.includes('쌍곡선') || h.includes('쌍곡선')) {
		if (q.includes('초점')) {
			principles.push('쌍곡선의 정의: 두 초점까지의 거리의 차가 일정');
		}
		if (q.includes('점근선')) {
			principles.push('쌍곡선의 점근선 방정식');
		}
	}
	
	// 원 관련
	if (q.includes('원') && (q.includes('^{2}') || q.includes('^2'))) {
		if (q.includes('내접') || q.includes('외접')) {
			principles.push('원에 내접/외접하는 도형 문제');
		}
		if (q.includes('원주각') || q.includes('중심각')) {
			principles.push('원주각과 중심각의 관계 (중심각 = 2 × 원주각)');
		}
		if (q.includes('접선') || q.includes('접점')) {
			principles.push('원과 직선의 접점 문제');
		}
	}
	
	// 직각삼각형 관련
	if (q.includes('직각삼각형') || q.includes('닮음')) {
		principles.push('직각삼각형의 닮음을 이용하는 문제');
	}
	
	if (principles.length === 0) {
		return null;
	}
	
	return principles.join('; ');
}

/**
 * 기하 문제의 오답 시나리오 생성 (기하 전용)
 * @param {string} question - 문제 내용
 * @param {string} 함정설계 - 함정 설계
 * @param {string} 실수포인트 - 실수 포인트
 * @param {string} 핵심개념 - 핵심 개념
 * @param {string} 중단원 - 중단원
 * @returns {string} 오답 시나리오
 */
export function generateGeometryErrorScenario(question, 함정설계 = '', 실수포인트 = '', 핵심개념 = '', 중단원 = '') {
	const scenarios = [];
	const q = question || '';
	const h = 핵심개념 || '';
	
	// 포물선 관련 오류
	if (q.includes('포물선') || h.includes('포물선')) {
		scenarios.push('1. 포물선의 정의를 잘못 적용: PF = PI를 PF = PI\'로 착각하거나 준선까지의 거리를 잘못 계산');
		scenarios.push('2. 포물선 방정식에서 초점의 위치를 잘못 파악: y² = 4ax에서 초점이 (a, 0)임을 (0, a)로 착각');
		scenarios.push('3. 포물선 위의 점의 좌표를 방정식에 대입할 때 부호 실수');
		
		if (q.includes('직각사다리꼴') || q.includes('사다리꼴')) {
			scenarios.push('4. 직각사다리꼴에서 두 밑변의 길이의 차를 구할 때 부호 실수');
		}
		if (q.includes('x_{1}') || q.includes('x_1')) {
			scenarios.push('5. 포물선 위의 점의 x좌표에 p를 더하는 과정에서 부호 실수');
		}
	}
	
	// 타원 관련 오류
	if (q.includes('타원') || h.includes('타원')) {
		scenarios.push('1. 타원의 정의를 잘못 적용: PF + PF\' = 2a를 PF + PF\' = a로 착각');
		scenarios.push('2. 장축과 단축을 혼동하여 초점의 위치를 잘못 계산');
		scenarios.push('3. 타원 위의 점에서 두 초점까지의 거리의 합을 구할 때 부호 실수');
		
		if (q.includes('장축')) {
			scenarios.push('4. 장축의 길이 2a와 반장축의 길이 a를 혼동');
		}
	}
	
	// 쌍곡선 관련 오류
	if (q.includes('쌍곡선') || h.includes('쌍곡선')) {
		scenarios.push('1. 쌍곡선의 정의를 잘못 적용: |PF - PF\'| = 2a를 PF - PF\' = 2a로 착각');
		scenarios.push('2. 쌍곡선의 점근선 방정식을 잘못 적용');
	}
	
	// 원 관련 오류
	if (q.includes('원') && (q.includes('^{2}') || q.includes('^2'))) {
		scenarios.push('1. 원의 방정식에서 중심과 반지름을 잘못 파악');
		scenarios.push('2. 원과 직선의 접점을 구할 때 판별식을 잘못 적용');
		
		if (q.includes('원주각') || q.includes('중심각')) {
			scenarios.push('3. 원주각과 중심각의 관계를 잘못 적용: 중심각 = 2 × 원주각임을 잊음');
		}
	}
	
	// 직각삼각형 관련 오류
	if (q.includes('직각삼각형') || q.includes('닮음')) {
		scenarios.push('직각삼각형의 닮음을 체크할 때 대응하는 각을 잘못 매칭');
	}
	
	if (scenarios.length === 0) {
		return '이차곡선의 정의와 성질을 적용할 때 주의해야 할 오류들';
	}
	
	return '가장 빠지기 쉬운 오류:\n' + scenarios.join('\n');
}
