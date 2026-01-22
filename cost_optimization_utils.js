// cost_optimization_utils.js
// 대량 데이터 처리 시 비용 최적화를 위한 유틸리티 함수들

/**
 * Rate Limiter - API 호출 횟수 제한
 * Notion API: 초당 3회 제한
 * OpenAI API: 토큰 기반 요금제에 따라 다름
 */
export class RateLimiter {
	constructor(maxRequestsPerSecond = 3) {
		this.maxRequests = maxRequestsPerSecond;
		this.requests = [];
	}

	async waitIfNeeded() {
		const now = Date.now();
		// 1초 이상 지난 요청 제거
		this.requests = this.requests.filter((time) => now - time < 1000);

		// 초당 제한에 도달했으면 대기
		if (this.requests.length >= this.maxRequests) {
			const oldestRequest = Math.min(...this.requests);
			const waitTime = 1000 - (now - oldestRequest) + 10; // 10ms 여유
			if (waitTime > 0) {
				await new Promise((resolve) => setTimeout(resolve, waitTime));
			}
		}

		this.requests.push(Date.now());
	}

	reset() {
		this.requests = [];
	}
}

/**
 * 재시도 로직 - Exponential Backoff
 */
export async function retryWithBackoff(
	fn,
	maxRetries = 3,
	baseDelay = 1000,
	onRetry = null
) {
	let lastError;

	for (let attempt = 0; attempt < maxRetries; attempt++) {
		try {
			return await fn();
		} catch (error) {
			lastError = error;

			// 마지막 시도가 아니면 재시도
			if (attempt < maxRetries - 1) {
				const delay = baseDelay * Math.pow(2, attempt); // Exponential backoff
				if (onRetry) {
					onRetry(attempt + 1, maxRetries, delay, error);
				}
				await new Promise((resolve) => setTimeout(resolve, delay));
			}
		}
	}

	throw lastError;
}

/**
 * 배치 처리 - 배열을 청크로 나누어 처리
 * OpenAI API 호출 최소화: 여러 항목을 한 번에 처리
 */
export function chunkArray(array, chunkSize) {
	const chunks = [];
	for (let i = 0; i < array.length; i += chunkSize) {
		chunks.push(array.slice(i, i + chunkSize));
	}
	return chunks;
}

/**
 * 진행 상황 추적 및 재개(Resume) 기능
 */
export class ProgressTracker {
	constructor(storageKey = 'progress') {
		this.storageKey = storageKey;
		this.progress = {
			processed: 0,
			total: 0,
			lastProcessedId: null,
			timestamp: Date.now(),
			errors: [],
		};
	}

	load() {
		try {
			const stored = localStorage.getItem(this.storageKey);
			if (stored) {
				this.progress = JSON.parse(stored);
				return true;
			}
		} catch (err) {
			console.warn('진행 상황 로드 실패:', err);
		}
		return false;
	}

	save() {
		try {
			this.progress.timestamp = Date.now();
			localStorage.setItem(this.storageKey, JSON.stringify(this.progress));
			return true;
		} catch (err) {
			console.warn('진행 상황 저장 실패:', err);
			return false;
		}
	}

	update(processed, lastProcessedId = null) {
		this.progress.processed = processed;
		if (lastProcessedId) {
			this.progress.lastProcessedId = lastProcessedId;
		}
		this.save();
	}

	addError(error, itemId = null) {
		this.progress.errors.push({
			timestamp: Date.now(),
			error: error.message || String(error),
			itemId,
		});
		this.save();
	}

	reset() {
		this.progress = {
			processed: 0,
			total: 0,
			lastProcessedId: null,
			timestamp: Date.now(),
			errors: [],
		};
		this.save();
	}

	getStatus() {
		const percentage =
			this.progress.total > 0
				? ((this.progress.processed / this.progress.total) * 100).toFixed(2)
				: 0;
		return {
			...this.progress,
			percentage,
			remaining: this.progress.total - this.progress.processed,
		};
	}
}

/**
 * 캐싱 시스템 - 중복 API 호출 방지
 * OpenAI API 호출 최소화: 이미 처리된 항목은 재처리하지 않음
 */
export class SimpleCache {
	constructor(ttl = 24 * 60 * 60 * 1000) {
		// 기본 TTL: 24시간
		this.cache = new Map();
		this.ttl = ttl;
	}

	get(key) {
		const item = this.cache.get(key);
		if (!item) return null;

		// TTL 체크
		if (Date.now() - item.timestamp > this.ttl) {
			this.cache.delete(key);
			return null;
		}

		return item.value;
	}

	set(key, value) {
		this.cache.set(key, {
			value,
			timestamp: Date.now(),
		});
	}

	has(key) {
		const item = this.cache.get(key);
		if (!item) return false;

		// TTL 체크
		if (Date.now() - item.timestamp > this.ttl) {
			this.cache.delete(key);
			return false;
		}

		return true;
	}

	clear() {
		this.cache.clear();
	}

	size() {
		return this.cache.size;
	}
}

/**
 * OpenAI API 호출 최소화 전략
 * 
 * 1. 배치 처리: 여러 항목을 한 번에 처리
 * 2. 캐싱: 동일한 입력은 재처리하지 않음
 * 3. 스마트 필터링: 처리할 필요가 없는 항목 제외
 * 4. 진행 상황 저장: 중단 후 재개 가능
 */
export class OpenAIOptimizer {
	constructor(options = {}) {
		this.cache = options.cache || new SimpleCache();
		this.batchSize = options.batchSize || 10; // 한 번에 처리할 항목 수
		this.enableCache = options.enableCache !== false;
		this.progressTracker = options.progressTracker || null;
	}

	/**
	 * 항목의 고유 키 생성 (캐싱용)
	 */
	getItemKey(item) {
		// 항목의 고유 ID를 기반으로 키 생성
		return item.id || JSON.stringify(item);
	}

	/**
	 * 처리할 항목 필터링 (캐시에 있는 항목 제외)
	 */
	filterUnprocessedItems(items) {
		if (!this.enableCache) {
			return items;
		}

		return items.filter((item) => {
			const key = this.getItemKey(item);
			return !this.cache.has(key);
		});
	}

	/**
	 * 항목들을 배치로 나누어 처리
	 */
	async processBatch(items, processFn, options = {}) {
		const { onProgress = null, onError = null } = options;

		// 캐시에서 제외된 항목만 필터링
		const unprocessedItems = this.filterUnprocessedItems(items);
		const batches = chunkArray(unprocessedItems, this.batchSize);

		console.log(
			`📊 처리 계획: 총 ${items.length}개 항목 중 ${unprocessedItems.length}개 미처리, ${batches.length}개 배치로 처리`
		);

		let processedCount = 0;
		const results = [];

		for (let i = 0; i < batches.length; i++) {
			const batch = batches[i];
			try {
				// 배치 처리 (OpenAI API 호출 최소화)
				const batchResults = await processFn(batch);

				// 결과 캐싱
				batch.forEach((item, index) => {
					const key = this.getItemKey(item);
					const result = batchResults[index];
					this.cache.set(key, result);
				});

				results.push(...batchResults);
				processedCount += batch.length;

				// 진행 상황 업데이트
				if (this.progressTracker) {
					this.progressTracker.update(processedCount);
				}

				if (onProgress) {
					onProgress({
						processed: processedCount,
						total: items.length,
						currentBatch: i + 1,
						totalBatches: batches.length,
					});
				}
			} catch (error) {
				if (onError) {
					onError(error, batch, i);
				} else {
					console.error(`배치 ${i + 1} 처리 실패:`, error);
				}
				throw error;
			}
		}

		return results;
	}
}
