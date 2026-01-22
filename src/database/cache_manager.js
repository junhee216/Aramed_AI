// src/database/cache_manager.js
// TTL(Time To Live) 기능이 있는 캐시 매니저
// 비용 0원 로직의 핵심: 이미 처리된 문제는 재처리하지 않음

import fs from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';
import logger from '../middleware/logger.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const CACHE_DIR = path.join(__dirname, '../../data');
const CACHE_FILE = path.join(CACHE_DIR, 'cache_store.json');

/**
 * 캐시 항목 구조
 */
class CacheItem {
	constructor(key, value, ttl = null) {
		this.key = key;
		this.value = value;
		this.createdAt = Date.now();
		this.ttl = ttl; // 밀리초 단위, null이면 만료 없음
		this.accessedAt = this.createdAt;
		this.accessCount = 0;
	}

	/**
	 * 만료되었는지 확인
	 */
	isExpired() {
		if (this.ttl === null) return false;
		const age = Date.now() - this.createdAt;
		return age > this.ttl;
	}

	/**
	 * 접근 기록 업데이트
	 */
	access() {
		this.accessedAt = Date.now();
		this.accessCount++;
	}

	/**
	 * 직렬화 가능한 객체로 변환
	 */
	toJSON() {
		return {
			key: this.key,
			value: this.value,
			createdAt: this.createdAt,
			ttl: this.ttl,
			accessedAt: this.accessedAt,
			accessCount: this.accessCount,
		};
	}

	/**
	 * JSON에서 CacheItem 복원
	 */
	static fromJSON(json) {
		const item = new CacheItem(json.key, json.value, json.ttl);
		item.createdAt = json.createdAt;
		item.accessedAt = json.accessedAt;
		item.accessCount = json.accessCount;
		return item;
	}
}

/**
 * 캐시 매니저 클래스
 */
export class CacheManager {
	constructor(cacheFile = CACHE_FILE, defaultTTL = null) {
		this.cacheFile = cacheFile;
		this.defaultTTL = defaultTTL; // 기본 TTL (밀리초), null이면 만료 없음
		this.cache = new Map(); // 메모리 캐시
		this.initialized = false;
		this.stats = {
			hits: 0,
			misses: 0,
			saves: 0,
			evictions: 0,
		};
	}

	/**
	 * 초기화 - 파일에서 캐시 로드
	 */
	async init() {
		if (this.initialized) return;

		try {
			// 캐시 디렉토리 확인
			try {
				await fs.access(CACHE_DIR);
			} catch {
				await fs.mkdir(CACHE_DIR, { recursive: true });
			}

			// 캐시 파일 읽기
			try {
				const data = await fs.readFile(this.cacheFile, 'utf-8');
				const cacheData = JSON.parse(data);
				
				// 만료된 항목 제외하고 로드
				for (const itemData of cacheData.items || []) {
					const item = CacheItem.fromJSON(itemData);
					if (!item.isExpired()) {
						this.cache.set(item.key, item);
					}
				}

				this.stats = cacheData.stats || this.stats;
				await logger.info('CACHE', `캐시 로드 완료: ${this.cache.size}개 항목`);
			} catch (error) {
				if (error.code !== 'ENOENT') {
					await logger.warn('CACHE', `캐시 파일 로드 실패: ${error.message}`);
				}
			}

			this.initialized = true;
		} catch (error) {
			await logger.error('CACHE', `캐시 초기화 실패: ${error.message}`);
			throw error;
		}
	}

	/**
	 * 캐시 파일에 저장
	 */
	async save() {
		await this.init();

		try {
			const cacheData = {
				items: Array.from(this.cache.values()).map(item => item.toJSON()),
				stats: this.stats,
				lastSaved: Date.now(),
			};

			await fs.writeFile(this.cacheFile, JSON.stringify(cacheData, null, 2), 'utf-8');
		} catch (error) {
			await logger.error('CACHE', `캐시 저장 실패: ${error.message}`);
			throw error;
		}
	}

	/**
	 * 만료된 항목 제거
	 */
	async cleanup() {
		await this.init();

		let evicted = 0;
		for (const [key, item] of this.cache.entries()) {
			if (item.isExpired()) {
				this.cache.delete(key);
				evicted++;
			}
		}

		if (evicted > 0) {
			this.stats.evictions += evicted;
			await logger.info('CACHE', `만료된 항목 ${evicted}개 제거`);
			await this.save();
		}
	}

	/**
	 * 캐시에서 값 가져오기
	 * @param {string} key - 캐시 키
	 * @returns {any|null} - 캐시된 값 또는 null
	 */
	async get(key) {
		await this.init();

		// 정기적으로 만료된 항목 제거 (10% 확률로)
		if (Math.random() < 0.1) {
			await this.cleanup();
		}

		const item = this.cache.get(key);

		if (!item) {
			this.stats.misses++;
			await logger.cache('MISS', key, { stats: this.getStats() });
			return null;
		}

		// 만료 확인
		if (item.isExpired()) {
			this.cache.delete(key);
			this.stats.misses++;
			this.stats.evictions++;
			await logger.cache('EXPIRED', key, { stats: this.getStats() });
			return null;
		}

		// 접근 기록
		item.access();
		this.stats.hits++;
		await logger.cache('HIT', key, { 
			accessCount: item.accessCount,
			age: Date.now() - item.createdAt,
			stats: this.getStats()
		});

		return item.value;
	}

	/**
	 * 캐시에 값 저장
	 * @param {string} key - 캐시 키
	 * @param {any} value - 저장할 값
	 * @param {number|null} ttl - TTL (밀리초), null이면 defaultTTL 사용
	 */
	async set(key, value, ttl = null) {
		await this.init();

		const itemTTL = ttl !== null ? ttl : this.defaultTTL;
		const item = new CacheItem(key, value, itemTTL);
		
		this.cache.set(key, item);
		this.stats.saves++;

		await logger.cache('SET', key, { 
			ttl: itemTTL,
			stats: this.getStats()
		});

		// 주기적으로 파일에 저장 (10번 저장마다)
		if (this.stats.saves % 10 === 0) {
			await this.save();
		}
	}

	/**
	 * 캐시에서 항목 제거
	 */
	async delete(key) {
		await this.init();

		const deleted = this.cache.delete(key);
		if (deleted) {
			await logger.cache('DELETE', key);
			await this.save();
		}
		return deleted;
	}

	/**
	 * 캐시에 키가 있는지 확인 (만료되지 않은 경우만)
	 */
	async has(key) {
		await this.init();

		const item = this.cache.get(key);
		if (!item) return false;
		
		if (item.isExpired()) {
			this.cache.delete(key);
			this.stats.evictions++;
			return false;
		}

		return true;
	}

	/**
	 * 캐시 비우기
	 */
	async clear() {
		await this.init();

		const size = this.cache.size;
		this.cache.clear();
		this.stats = {
			hits: 0,
			misses: 0,
			saves: 0,
			evictions: 0,
		};

		await logger.info('CACHE', `캐시 비우기: ${size}개 항목 제거`);
		await this.save();
	}

	/**
	 * 캐시 통계 가져오기
	 */
	getStats() {
		const hitRate = this.stats.hits + this.stats.misses > 0
			? ((this.stats.hits / (this.stats.hits + this.stats.misses)) * 100).toFixed(2)
			: 0;

		return {
			...this.stats,
			size: this.cache.size,
			hitRate: `${hitRate}%`,
		};
	}

	/**
	 * 캐시 키 생성 (문제 ID 기반)
	 */
	generateKey(problemId, studentLevel = null, stage = null) {
		const parts = [problemId];
		if (studentLevel !== null) parts.push(`level_${studentLevel}`);
		if (stage !== null) parts.push(`stage_${stage}`);
		return parts.join('::');
	}

	/**
	 * 강제 저장 (즉시 파일에 쓰기)
	 */
	async forceSave() {
		await this.save();
	}
}

// 싱글톤 인스턴스
const cacheManager = new CacheManager(CACHE_FILE, 7 * 24 * 60 * 60 * 1000); // 기본 TTL: 7일

// 기본 export
export default cacheManager;
