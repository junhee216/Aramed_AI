// test_thinking_logic.js
// Thinking 로직 및 캐시 매니저 테스트

import thinkingLogic, { StudentLevel, HintStage } from './src/logic/thinking.js';
import cacheManager from './src/database/cache_manager.js';
import logger from './src/middleware/logger.js';

/**
 * 테스트 실행
 */
async function testThinkingLogic() {
	console.log('🧪 Thinking 로직 테스트 시작\n');

	try {
		// 1. 캐시 초기화
		await cacheManager.init();
		console.log('✅ 캐시 초기화 완료\n');

		// 2. 테스트 데이터
		const problemId = 'test_problem_001';
		const notionHints = {
			stage_1: '첫 번째 힌트: 문제를 단계별로 나누어 생각해보세요.',
			stage_2: '두 번째 힌트: 특정 패턴을 찾아보세요.',
			stage_3: '세 번째 힌트: 공식을 적용해보세요.',
		};

		// 3. 초급 학생 테스트
		console.log('📚 초급 학생 (BEGINNER) 테스트');
		const beginnerResult = await thinkingLogic.selectHints(
			problemId,
			StudentLevel.BEGINNER,
			notionHints
		);
		console.log('선택된 힌트:', beginnerResult.hints);
		console.log('사용 가능한 Stage:', beginnerResult.availableStages);
		console.log('');

		// 4. 중급 학생 테스트
		console.log('📚 중급 학생 (INTERMEDIATE) 테스트');
		const intermediateResult = await thinkingLogic.selectHints(
			problemId + '_intermediate',
			StudentLevel.INTERMEDIATE,
			notionHints
		);
		console.log('선택된 힌트:', intermediateResult.hints);
		console.log('사용 가능한 Stage:', intermediateResult.availableStages);
		console.log('');

		// 5. 고급 학생 테스트
		console.log('📚 고급 학생 (ADVANCED) 테스트');
		const advancedResult = await thinkingLogic.selectHints(
			problemId + '_advanced',
			StudentLevel.ADVANCED,
			notionHints
		);
		console.log('선택된 힌트:', advancedResult.hints);
		console.log('사용 가능한 Stage:', advancedResult.availableStages);
		console.log('');

		// 6. 캐시 테스트 (비용 0원 로직)
		console.log('💰 캐시 테스트 (비용 0원 로직)');
		console.log('동일한 문제를 다시 요청하면 캐시에서 가져옵니다...\n');
		
		const cachedResult = await thinkingLogic.selectHints(
			problemId,
			StudentLevel.BEGINNER,
			notionHints
		);
		console.log('캐시에서 가져온 결과:', cachedResult.hints);
		console.log('');

		// 7. 캐시 통계
		const stats = await thinkingLogic.getCacheStats();
		console.log('📊 캐시 통계:');
		console.log(JSON.stringify(stats, null, 2));
		console.log('');

		// 8. 특정 Stage 힌트 가져오기
		console.log('🎯 특정 Stage 힌트 가져오기 테스트');
		const stage2Hint = await thinkingLogic.getHintByStage(
			problemId + '_stage2',
			StudentLevel.INTERMEDIATE,
			HintStage.STAGE_2,
			notionHints
		);
		console.log('Stage 2 힌트:', stage2Hint);
		console.log('');

		console.log('✅ 모든 테스트 완료!\n');
		console.log('📝 로그 파일 확인: logs/access.log');
		console.log('💾 캐시 파일 확인: data/cache_store.json');

	} catch (error) {
		console.error('❌ 테스트 실패:', error);
		await logger.error('TEST', `테스트 실패: ${error.message}`, { error: error.stack });
		process.exit(1);
	}
}

// 테스트 실행
testThinkingLogic();
