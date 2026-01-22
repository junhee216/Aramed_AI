// src/logic/thinking.js
// 노션에서 가져온 Stage 1, 2, 3 힌트를 학생 단계에 맞춰서 골라주는 로직
// 비용 0원 로직의 핵심: 캐시를 활용하여 이미 처리된 문제는 재처리하지 않음

import cacheManager from '../database/cache_manager.js';
import logger from '../middleware/logger.js';

/**
 * 학생 레벨 정의
 */
export const StudentLevel = {
	BEGINNER: 1,    // 초급
	INTERMEDIATE: 2, // 중급
	ADVANCED: 3,     // 고급
};

/**
 * Stage 정의 (힌트 단계)
 */
export const HintStage = {
	STAGE_1: 1, // 첫 번째 힌트 (가장 큰 힌트)
	STAGE_2: 2, // 두 번째 힌트 (중간 힌트)
	STAGE_3: 3, // 세 번째 힌트 (가장 작은 힌트)
};

/**
 * 학생 레벨에 따른 Stage 선택 로직
 * - 초급(BEGINNER): Stage 1 → Stage 2 → Stage 3 순서
 * - 중급(INTERMEDIATE): Stage 2 → Stage 3 순서 (Stage 1 건너뜀)
 * - 고급(ADVANCED): Stage 3만 제공
 */
export function getAvailableStages(studentLevel) {
	switch (studentLevel) {
		case StudentLevel.BEGINNER:
			return [HintStage.STAGE_1, HintStage.STAGE_2, HintStage.STAGE_3];
		case StudentLevel.INTERMEDIATE:
			return [HintStage.STAGE_2, HintStage.STAGE_3];
		case StudentLevel.ADVANCED:
			return [HintStage.STAGE_3];
		default:
			// 기본값: 초급
			return [HintStage.STAGE_1, HintStage.STAGE_2, HintStage.STAGE_3];
	}
}

/**
 * 힌트 데이터 구조 (노션에서 가져온 데이터)
 */
export class HintData {
	constructor(problemId, hints) {
		this.problemId = problemId;
		this.hints = hints; // { stage_1: "힌트1", stage_2: "힌트2", stage_3: "힌트3" }
		this.createdAt = Date.now();
	}

	/**
	 * 특정 Stage의 힌트 가져오기
	 */
	getHint(stage) {
		const key = `stage_${stage}`;
		return this.hints[key] || null;
	}

	/**
	 * 학생 레벨에 맞는 힌트들 가져오기
	 */
	getHintsForLevel(studentLevel) {
		const availableStages = getAvailableStages(studentLevel);
		const hints = {};

		for (const stage of availableStages) {
			const hint = this.getHint(stage);
			if (hint) {
				hints[`stage_${stage}`] = hint;
			}
		}

		return hints;
	}
}

/**
 * Thinking 로직 클래스
 */
export class ThinkingLogic {
	constructor() {
		this.cacheManager = cacheManager;
	}

	/**
	 * 학생 레벨에 맞는 힌트 선택
	 * @param {string} problemId - 문제 ID
	 * @param {number} studentLevel - 학생 레벨 (1: 초급, 2: 중급, 3: 고급)
	 * @param {Object} notionHints - 노션에서 가져온 힌트 데이터 { stage_1: "...", stage_2: "...", stage_3: "..." }
	 * @returns {Object} 선택된 힌트들
	 */
	async selectHints(problemId, studentLevel, notionHints) {
		await logger.thinking('SELECT_HINTS_START', studentLevel, null, {
			problemId,
			notionHints: Object.keys(notionHints),
		});

		// 캐시 키 생성
		const cacheKey = this.cacheManager.generateKey(problemId, studentLevel);

		// 캐시에서 먼저 확인 (비용 0원 로직의 핵심)
		const cached = await this.cacheManager.get(cacheKey);
		if (cached !== null) {
			await logger.thinking('SELECT_HINTS_CACHE_HIT', studentLevel, null, {
				problemId,
				cacheKey,
			});
			await logger.api('CACHE_HIT', `thinking/${problemId}`, {
				cost: 0,
				studentLevel,
			});
			return cached;
		}

		// 캐시에 없으면 힌트 선택 로직 실행
		await logger.thinking('SELECT_HINTS_CACHE_MISS', studentLevel, null, {
			problemId,
			cacheKey,
		});

		// HintData 객체 생성
		const hintData = new HintData(problemId, notionHints);

		// 학생 레벨에 맞는 힌트 선택
		const selectedHints = hintData.getHintsForLevel(studentLevel);

		// 사용 가능한 Stage 목록
		const availableStages = getAvailableStages(studentLevel);

		// 결과 구조
		const result = {
			problemId,
			studentLevel,
			availableStages,
			hints: selectedHints,
			timestamp: Date.now(),
		};

		// 캐시에 저장 (비용 0원 로직: 다음에 같은 요청이 오면 캐시에서 반환)
		await this.cacheManager.set(cacheKey, result);
		await this.cacheManager.forceSave(); // 즉시 저장

		await logger.thinking('SELECT_HINTS_COMPLETE', studentLevel, null, {
			problemId,
			selectedStages: availableStages,
			hintCount: Object.keys(selectedHints).length,
		});

		// 비용 0원 로직이므로 API 호출 비용은 0
		await logger.api('CACHE_SAVE', `thinking/${problemId}`, {
			cost: 0,
			studentLevel,
			nextCallCost: 0, // 다음 호출은 캐시에서 가져오므로 비용 0
		});

		return result;
	}

	/**
	 * 특정 Stage의 힌트만 가져오기
	 * @param {string} problemId - 문제 ID
	 * @param {number} studentLevel - 학생 레벨
	 * @param {number} stage - Stage (1, 2, 3)
	 * @param {Object} notionHints - 노션에서 가져온 힌트 데이터
	 * @returns {string|null} 힌트 텍스트 또는 null
	 */
	async getHintByStage(problemId, studentLevel, stage, notionHints) {
		await logger.thinking('GET_HINT_BY_STAGE', studentLevel, stage, {
			problemId,
		});

		// 학생 레벨에 사용 가능한 Stage 확인
		const availableStages = getAvailableStages(studentLevel);
		if (!availableStages.includes(stage)) {
			await logger.warn('THINKING', `학생 레벨 ${studentLevel}에서는 Stage ${stage}를 사용할 수 없습니다`, {
				problemId,
				studentLevel,
				stage,
				availableStages,
			});
			return null;
		}

		// 캐시 키 생성
		const cacheKey = this.cacheManager.generateKey(problemId, studentLevel, stage);

		// 캐시에서 확인
		const cached = await this.cacheManager.get(cacheKey);
		if (cached !== null) {
			await logger.thinking('GET_HINT_CACHE_HIT', studentLevel, stage, {
				problemId,
			});
			return cached;
		}

		// 캐시에 없으면 힌트 선택
		const hintData = new HintData(problemId, notionHints);
		const hint = hintData.getHint(stage);

		if (!hint) {
			await logger.warn('THINKING', `Stage ${stage} 힌트가 없습니다`, {
				problemId,
				stage,
			});
			return null;
		}

		// 캐시에 저장
		await this.cacheManager.set(cacheKey, hint);
		await this.cacheManager.forceSave();

		await logger.thinking('GET_HINT_COMPLETE', studentLevel, stage, {
			problemId,
			hintLength: hint.length,
		});

		return hint;
	}

	/**
	 * 학생 레벨 검증
	 */
	validateStudentLevel(level) {
		const validLevels = Object.values(StudentLevel);
		if (!validLevels.includes(level)) {
			throw new Error(`유효하지 않은 학생 레벨: ${level}. 유효한 값: ${validLevels.join(', ')}`);
		}
		return true;
	}

	/**
	 * Stage 검증
	 */
	validateStage(stage) {
		const validStages = Object.values(HintStage);
		if (!validStages.includes(stage)) {
			throw new Error(`유효하지 않은 Stage: ${stage}. 유효한 값: ${validStages.join(', ')}`);
		}
		return true;
	}

	/**
	 * 캐시 통계 가져오기
	 */
	async getCacheStats() {
		return this.cacheManager.getStats();
	}
}

// 싱글톤 인스턴스
const thinkingLogic = new ThinkingLogic();

// 기본 export
export default thinkingLogic;
