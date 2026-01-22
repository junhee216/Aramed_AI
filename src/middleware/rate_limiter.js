// src/middleware/rate_limiter.js
// Rate Limiting 미들웨어 - API 호출 속도 제한
// 마스터플랜 V2.0: 1초 지연 기본값, 유동적 설정 가능

/**
 * Rate Limiter 클래스
 * API 호출 간 적절한 지연을 적용하여 Rate Limit 초과를 방지합니다.
 */
export class RateLimiter {
	/**
	 * @param {number} delayMs - 각 요청 사이의 지연 시간 (밀리초), 기본값 1000ms (1초)
	 * @param {number} maxRequestsPerSecond - 초당 최대 요청 수 (참고용, delayMs가 우선 적용됨)
	 */
	constructor(delayMs = 1000, maxRequestsPerSecond = null) {
		this.delayMs = delayMs;
		this.maxRequestsPerSecond = maxRequestsPerSecond;
		this.lastRequestTime = 0;
		this.requestCount = 0;
		this.requestTimestamps = []; // 요청 타임스탬프 배열 (maxRequestsPerSecond 사용 시)
	}

	/**
	 * 다음 요청을 위해 필요한 지연 시간 계산 및 대기
	 * @returns {Promise<void>}
	 */
	async waitIfNeeded() {
		const now = Date.now();
		const timeSinceLastRequest = now - this.lastRequestTime;

		// delayMs 만큼 시간이 지나지 않았다면 대기
		if (timeSinceLastRequest < this.delayMs) {
			const waitTime = this.delayMs - timeSinceLastRequest;
			await new Promise((resolve) => setTimeout(resolve, waitTime));
		}

		// maxRequestsPerSecond가 설정된 경우 추가 체크
		if (this.maxRequestsPerSecond) {
			const nowAfterWait = Date.now();
			
			// 1초 이내의 요청만 유지
			this.requestTimestamps = this.requestTimestamps.filter(
				(timestamp) => nowAfterWait - timestamp < 1000
			);

			// 초당 제한에 도달했으면 추가 대기
			if (this.requestTimestamps.length >= this.maxRequestsPerSecond) {
				const oldestRequest = Math.min(...this.requestTimestamps);
				const waitTime = 1000 - (nowAfterWait - oldestRequest) + 10; // 10ms 여유
				
				if (waitTime > 0) {
					await new Promise((resolve) => setTimeout(resolve, waitTime));
				}
			}

			this.requestTimestamps.push(Date.now());
		}

		this.lastRequestTime = Date.now();
		this.requestCount++;
	}

	/**
	 * 지연 시간 동적 변경
	 * @param {number} newDelayMs - 새로운 지연 시간 (밀리초)
	 */
	setDelay(newDelayMs) {
		this.delayMs = newDelayMs;
	}

	/**
	 * 통계 정보 반환
	 * @returns {Object} 통계 정보
	 */
	getStats() {
		return {
			delayMs: this.delayMs,
			totalRequests: this.requestCount,
			maxRequestsPerSecond: this.maxRequestsPerSecond,
		};
	}

	/**
	 * 통계 초기화
	 */
	reset() {
		this.requestCount = 0;
		this.requestTimestamps = [];
		this.lastRequestTime = 0;
	}
}

/**
 * 기본 Rate Limiter 인스턴스 (1초 지연)
 * 다른 파일에서 import하여 사용 가능
 */
export const defaultRateLimiter = new RateLimiter(1000);

/**
 * Rate Limiter 팩토리 함수
 * @param {number} delayMs - 지연 시간 (밀리초)
 * @returns {RateLimiter} RateLimiter 인스턴스
 */
export function createRateLimiter(delayMs = 1000) {
	return new RateLimiter(delayMs);
}

// 기본 export
export default defaultRateLimiter;