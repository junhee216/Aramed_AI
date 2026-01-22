// progress_tracker.js
// 진행 상황 추적 및 재개(Resume) 기능 - 파일 기반 저장
// Node.js 환경에서 사용 (localStorage 대신 파일 사용)

import fs from 'fs/promises';
import path from 'path';

/**
 * 진행 상황 추적 및 재개(Resume) 기능 - 파일 기반
 * 13만 개의 문제 처리 시 중단 후 재개 가능
 */
export class ProgressTracker {
	constructor(filePath = 'progress.json') {
		this.filePath = filePath;
		this.progress = {
			processed: 0,
			total: 0,
			lastProcessedId: null,
			lastProcessedIndex: 0,
			timestamp: Date.now(),
			errors: [],
			metadata: {},
		};
	}

	/**
	 * 파일에서 진행 상황 로드
	 */
	async load() {
		try {
			const data = await fs.readFile(this.filePath, 'utf-8');
			this.progress = JSON.parse(data);
			console.log(`✅ 진행 상황 로드 완료: ${this.progress.processed}/${this.progress.total} 처리됨`);
			return true;
		} catch (err) {
			if (err.code === 'ENOENT') {
				// 파일이 없으면 새로 시작
				console.log('📝 새로운 진행 상황 시작');
				return false;
			}
			console.warn('⚠️ 진행 상황 로드 실패:', err.message);
			return false;
		}
	}

	/**
	 * 진행 상황을 파일에 저장
	 */
	async save() {
		try {
			this.progress.timestamp = Date.now();
			await fs.writeFile(this.filePath, JSON.stringify(this.progress, null, 2), 'utf-8');
			return true;
		} catch (err) {
			console.warn('⚠️ 진행 상황 저장 실패:', err.message);
			return false;
		}
	}

	/**
	 * 진행 상황 업데이트
	 */
	async update(processed, lastProcessedId = null, lastProcessedIndex = null) {
		this.progress.processed = processed;
		if (lastProcessedId) {
			this.progress.lastProcessedId = lastProcessedId;
		}
		if (lastProcessedIndex !== null) {
			this.progress.lastProcessedIndex = lastProcessedIndex;
		}
		await this.save();
	}

	/**
	 * 총 개수 설정
	 */
	async setTotal(total) {
		this.progress.total = total;
		await this.save();
	}

	/**
	 * 에러 추가
	 */
	async addError(error, itemId = null, itemIndex = null) {
		this.progress.errors.push({
			timestamp: Date.now(),
			error: error.message || String(error),
			itemId,
			itemIndex,
		});
		// 최근 100개 에러만 유지 (메모리 절약)
		if (this.progress.errors.length > 100) {
			this.progress.errors = this.progress.errors.slice(-100);
		}
		await this.save();
	}

	/**
	 * 메타데이터 저장 (추가 정보)
	 */
	async setMetadata(key, value) {
		this.progress.metadata[key] = value;
		await this.save();
	}

	/**
	 * 메타데이터 가져오기
	 */
	getMetadata(key) {
		return this.progress.metadata[key];
	}

	/**
	 * 진행 상황 리셋
	 */
	async reset() {
		this.progress = {
			processed: 0,
			total: 0,
			lastProcessedId: null,
			lastProcessedIndex: 0,
			timestamp: Date.now(),
			errors: [],
			metadata: {},
		};
		await this.save();
	}

	/**
	 * 진행 상황 상태 가져오기
	 */
	getStatus() {
		const percentage =
			this.progress.total > 0
				? ((this.progress.processed / this.progress.total) * 100).toFixed(2)
				: 0;
		return {
			...this.progress,
			percentage: parseFloat(percentage),
			remaining: this.progress.total - this.progress.processed,
		};
	}

	/**
	 * 처리된 항목인지 확인 (재개 시 사용)
	 */
	isProcessed(itemId) {
		// 간단한 체크: lastProcessedId까지 처리되었는지 확인
		// 실제 구현은 더 정교한 로직 필요 (예: Set 사용)
		return false; // 기본값: 모든 항목 처리 필요
	}

	/**
	 * 처리되지 않은 항목만 필터링
	 */
	filterUnprocessedItems(items, getId = (item) => item.id) {
		if (this.progress.lastProcessedIndex === null) {
			return items;
		}

		// 마지막 처리된 인덱스 이후의 항목만 반환
		return items.slice(this.progress.lastProcessedIndex + 1);
	}
}
