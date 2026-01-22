// src/utils/geometry_principle_utils.js
// 기하 문제 전용 원리 추출 및 오답 시나리오 생성 유틸리티

/**
 * 기하 문제의 수학적 원리 추출
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
 * 기하 문제의 오답 시나리오 생성
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
