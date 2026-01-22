// batch_upload.js
// 배치 업로드 스크립트 - 대량 데이터를 Notion 데이터베이스에 효율적으로 업로드
// 마스터플랜 V2.0: 13만 개 데이터 기준, 유동적 양 대응, 1초 지연, 효율적 배치 처리
// Node >= 18, ESM("type": "module") 환경 기준

import 'dotenv/config';
import { Client } from '@notionhq/client';
import { createRateLimiter } from './src/middleware/rate_limiter.js';
import logger from './src/middleware/logger.js';

// ✅ 1. 환경변수 읽기
const notionApiKey = process.env.NOTION_API_KEY;
const databaseId = process.env.NOTION_DATABASE_ID;

if (!notionApiKey || !databaseId) {
	console.error('❌ .env 설정 오류: NOTION_API_KEY 또는 NOTION_DATABASE_ID 가 없습니다.');
	process.exit(1);
}

// ✅ 2. Notion 클라이언트 생성
const notion = new Client({ auth: notionApiKey });

// ✅ 3. Rate Limiter 생성 (1초 지연)
const rateLimiter = createRateLimiter(1000); // 1초 지연

console.log('✅ ENV LOADED:', {
	keyPrefix: notionApiKey.slice(0, 8) + '...',
	databaseId,
});

/**
 * ✅ 4. 배치 업로드 설정
 */
const BATCH_SIZE = 50; // 한 번에 처리할 배치 크기 (메모리 효율성을 위해 적절한 크기)
const MAX_RETRIES = 3; // 최대 재시도 횟수
const RETRY_DELAY_MS = 2000; // 재시도 전 대기 시간 (밀리초)

/**
 * ✅ 5. 데이터 항목을 Notion 페이지 속성으로 변환
 * @param {Object} item - 업로드할 데이터 항목
 * @param {string} titlePropertyName - 제목 속성 이름 (기본값: '마스터 프로토콜 v1.0')
 * @returns {Object} Notion 페이지 속성 객체
 */
function convertItemToProperties(item, titlePropertyName = '마스터 프로토콜 v1.0') {
	const properties = {};

	// 제목 속성 (필수)
	if (item.title !== undefined) {
		properties[titlePropertyName] = {
			title: [
				{
					text: {
						content: String(item.title || '(제목 없음)'),
					},
				},
			],
		};
	}

	// 추가 속성들 변환 (item의 다른 필드들을 Notion 속성으로 매핑)
	// 실제 사용 시 데이터 구조에 맞게 수정 필요
	if (item.properties) {
		Object.assign(properties, item.properties);
	}

	return properties;
}

/**
 * ✅ 6. 재시도 로직이 포함된 단일 페이지 생성
 * @param {Object} item - 업로드할 데이터 항목
 * @param {number} retryCount - 현재 재시도 횟수
 * @returns {Promise<Object>} 생성된 페이지
 */
async function createPageWithRetry(item, retryCount = 0) {
	try {
		// Rate Limiter 적용 (1초 지연)
		await rateLimiter.waitIfNeeded();

		const properties = convertItemToProperties(item);
		
		const newPage = await notion.pages.create({
			parent: {
				database_id: databaseId,
			},
			properties: properties,
		});

		return newPage;
	} catch (error) {
		// Rate Limit 오류 또는 일시적 오류인 경우 재시도
		const isRetryable = 
			error.code === 'rate_limited' ||
			error.status === 429 ||
			error.status === 500 ||
			error.status === 503;

		if (isRetryable && retryCount < MAX_RETRIES) {
			const delay = RETRY_DELAY_MS * (retryCount + 1); // 지수 백오프
			await logger.warn('BATCH_UPLOAD', `재시도 대기 (${delay}ms): ${item.title || '제목 없음'}`, {
				retryCount: retryCount + 1,
				maxRetries: MAX_RETRIES,
				error: error.message,
			});

			await new Promise((resolve) => setTimeout(resolve, delay));
			return createPageWithRetry(item, retryCount + 1);
		}

		// 재시도 불가능한 오류이거나 최대 재시도 횟수 초과
		throw error;
	}
}

/**
 * ✅ 7. 배치 단위로 데이터 업로드
 * @param {Array} items - 업로드할 데이터 배열
 * @param {Function} progressCallback - 진행 상황 콜백 함수
 * @returns {Promise<Object>} 업로드 결과 통계
 */
async function uploadBatch(items, progressCallback = null) {
	const totalItems = items.length;
	let successCount = 0;
	let failCount = 0;
	const errors = [];

	await logger.info('BATCH_UPLOAD', `배치 업로드 시작: 총 ${totalItems}개 항목`, {
		totalItems,
		batchSize: BATCH_SIZE,
		delayMs: rateLimiter.delayMs,
	});

	const startTime = Date.now();

	// 효율적인 반복문: 배치 단위로 처리
	for (let i = 0; i < totalItems; i += BATCH_SIZE) {
		const batch = items.slice(i, i + BATCH_SIZE);
		const batchNumber = Math.floor(i / BATCH_SIZE) + 1;
		const totalBatches = Math.ceil(totalItems / BATCH_SIZE);

		await logger.info('BATCH_UPLOAD', `배치 ${batchNumber}/${totalBatches} 처리 중 (${batch.length}개 항목)`, {
			batchNumber,
			totalBatches,
			batchSize: batch.length,
			currentIndex: i,
			totalItems,
		});

		// 배치 내 항목들을 순차적으로 처리 (병렬 처리 시 Rate Limit 위험)
		for (let j = 0; j < batch.length; j++) {
			const item = batch[j];
			const currentIndex = i + j + 1;

			try {
				await createPageWithRetry(item);
				successCount++;

				// 진행 상황 콜백 호출 (100개마다 또는 마지막 항목)
				if (progressCallback && (currentIndex % 100 === 0 || currentIndex === totalItems)) {
					progressCallback({
						current: currentIndex,
						total: totalItems,
						success: successCount,
						failed: failCount,
						percentage: ((currentIndex / totalItems) * 100).toFixed(2),
					});
				}
			} catch (error) {
				failCount++;
				errors.push({
					index: currentIndex,
					item: item.title || '제목 없음',
					error: error.message || error.toString(),
				});

				await logger.error('BATCH_UPLOAD', `항목 업로드 실패: ${item.title || '제목 없음'}`, {
					index: currentIndex,
					error: error.message,
					code: error.code,
					status: error.status,
				});
			}
		}

		// 배치 간 짧은 대기 (선택사항, 시스템 부하 분산)
		if (i + BATCH_SIZE < totalItems) {
			await new Promise((resolve) => setTimeout(resolve, 100));
		}
	}

	const endTime = Date.now();
	const duration = ((endTime - startTime) / 1000).toFixed(2);
	const avgTimePerItem = (duration / totalItems).toFixed(3);

	await logger.info('BATCH_UPLOAD', '배치 업로드 완료', {
		totalItems,
		successCount,
		failCount,
		duration: `${duration}초`,
		avgTimePerItem: `${avgTimePerItem}초/항목`,
	});

	return {
		total: totalItems,
		success: successCount,
		failed: failCount,
		duration: `${duration}초`,
		avgTimePerItem: `${avgTimePerItem}초/항목`,
		errors: errors.length > 0 ? errors : null,
	};
}

/**
 * ✅ 8. 샘플 데이터 생성 (테스트용)
 * 실제 사용 시 데이터 소스에서 가져오거나 파일에서 읽어와야 함
 * @param {number} count - 생성할 데이터 개수
 * @returns {Array} 샘플 데이터 배열
 */
function generateSampleData(count) {
	const items = [];
	for (let i = 1; i <= count; i++) {
		items.push({
			title: `배치 업로드 테스트 항목 #${i}`,
			// 추가 속성들...
		});
	}
	return items;
}

/**
 * ✅ 9. 메인 실행 함수
 * @param {Array} dataItems - 업로드할 데이터 배열 (없으면 샘플 데이터 생성)
 */
async function main(dataItems = null) {
	try {
		// 데이터 준비
		let items = dataItems;

		if (!items || items.length === 0) {
			console.log('⚠️ 업로드할 데이터가 제공되지 않았습니다.');
			console.log('💡 사용법: node batch_upload.js [데이터 파일 경로]');
			console.log('💡 또는 코드에서 dataItems 배열을 직접 전달하세요.');
			
			// 예시: 샘플 데이터 생성 (실제 사용 시 제거)
			const useSample = process.env.USE_SAMPLE_DATA === 'true';
			if (useSample) {
				const sampleCount = parseInt(process.env.SAMPLE_COUNT || '10', 10);
				console.log(`📝 샘플 데이터 ${sampleCount}개 생성 중...`);
				items = generateSampleData(sampleCount);
			} else {
				console.log('❌ 업로드할 데이터가 없습니다. 종료합니다.');
				process.exit(1);
			}
		}

		console.log(`\n📊 총 ${items.length}개 항목 업로드 준비 완료\n`);

		// 진행 상황 콜백
		const progressCallback = ({ current, total, success, failed, percentage }) => {
			console.log(
				`📈 진행 상황: ${current}/${total} (${percentage}%) | 성공: ${success} | 실패: ${failed}`
			);
		};

		// 배치 업로드 실행
		const result = await uploadBatch(items, progressCallback);

		// 결과 출력
		console.log('\n' + '='.repeat(50));
		console.log('✅ 배치 업로드 완료!');
		console.log('='.repeat(50));
		console.log(`📊 총 항목: ${result.total}`);
		console.log(`✅ 성공: ${result.success}`);
		console.log(`❌ 실패: ${result.failed}`);
		console.log(`⏱️  소요 시간: ${result.duration}`);
		console.log(`⚡ 평균 처리 시간: ${result.avgTimePerItem}초/항목`);

		if (result.errors && result.errors.length > 0) {
			console.log(`\n⚠️  오류 발생 항목 (최대 10개 표시):`);
			result.errors.slice(0, 10).forEach((err) => {
				console.log(`  - 항목 #${err.index}: ${err.item} - ${err.error}`);
			});
			if (result.errors.length > 10) {
				console.log(`  ... 외 ${result.errors.length - 10}개 오류`);
			}
		}

		console.log('\n');

	} catch (error) {
		console.error('\n❌ 배치 업로드 실행 중 오류 발생:');
		console.error(error);
		await logger.error('BATCH_UPLOAD', '배치 업로드 실행 오류', {
			error: error.message,
			stack: error.stack,
		});
		process.exit(1);
	}
}

// 직접 실행 시에만 main 함수 실행
if (import.meta.url.endsWith(process.argv[1].replace(/\\/g, '/'))) {
	main();
}

// 다른 파일에서 import 시 사용할 수 있도록 export
export { uploadBatch, createPageWithRetry, convertItemToProperties };