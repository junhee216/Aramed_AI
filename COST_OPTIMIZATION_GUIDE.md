# 비용 최적화 가이드

## 📊 현재 코드 분석 결과

### ✅ 개선 완료된 항목

1. **Notion API 페이지네이션 처리**
   - ✅ `read_notion_database.js`에 페이지네이션 로직 추가
   - ✅ 13만 개의 데이터도 전체 조회 가능
   - ✅ Rate Limiting 구현 (초당 3회 제한 준수)

2. **비용 최적화 유틸리티 생성**
   - ✅ `cost_optimization_utils.js`: Rate Limiter, 재시도 로직, 배치 처리, 캐싱
   - ✅ `progress_tracker.js`: 진행 상황 추적 및 재개 기능

### ⚠️ 발견된 문제점

#### 1. **Notion API Over-fetching 문제**

**현재 상태**: ✅ **문제 없음**
- Notion API는 필요한 필드만 반환 (Over-fetching 없음)
- `page_size: 100` 사용 (최적화된 배치 크기)

**개선 사항**:
- 페이지네이션 처리 추가 완료
- Rate Limiting 추가 완료

#### 2. **OpenAI API 호출 최소화**

**현재 상태**: ⚠️ **아직 OpenAI API 호출 없음**
- 현재 코드베이스에 OpenAI API 통합 없음
- 13만 개 문제 처리 시 비용 폭탄 가능성 높음

**필요한 로직** (지금 단계에서 추가해야 할 것):

1. **배치 처리** ✅
   - 여러 문제를 한 번에 처리 (예: 10-20개씩)
   - OpenAI API는 배치 요청 지원 (일부 모델)
   - 또는 여러 문제를 하나의 프롬프트로 묶어서 처리

2. **캐싱 시스템** ✅
   - 이미 처리된 문제는 재처리하지 않음
   - 동일한 입력에 대한 중복 호출 방지
   - `cost_optimization_utils.js`의 `SimpleCache` 사용

3. **스마트 필터링** ⚠️
   - 처리할 필요가 없는 항목 사전 제외
   - 예: 이미 처리된 문제, 중복 문제, 빈 항목 등

4. **진행 상황 저장 및 재개** ✅
   - 중단 후 재개 가능
   - `progress_tracker.js` 사용

5. **비용 예측 및 모니터링** ⚠️
   - 예상 토큰 사용량 계산
   - 실시간 비용 추적
   - 예산 초과 시 중단

6. **재시도 로직** ✅
   - Exponential Backoff 구현
   - 일시적 오류 처리
   - `cost_optimization_utils.js`의 `retryWithBackoff` 사용

## 🎯 13만 개 문제 처리 시 비용 폭탄 방지 전략

### 1. **예상 비용 계산**

```
가정:
- 문제당 평균 토큰: 입력 500 + 출력 200 = 700 토큰
- GPT-4 가격: 입력 $0.03/1K 토큰, 출력 $0.06/1K 토큰
- 13만 개 문제 처리 시

비용 = 130,000 × (500 × $0.03/1000 + 200 × $0.06/1000)
     = 130,000 × ($0.015 + $0.012)
     = 130,000 × $0.027
     = $3,510

배치 처리 (10개씩) 적용 시:
- API 호출: 13,000회로 감소
- 오버헤드 비용 감소
- 예상 절감: 5-10%
```

### 2. **필수 구현 항목 (지금 단계)**

#### A. OpenAI API 통합 시 필수 사항

```javascript
// 예시: OpenAI API 호출 최소화 예시
import { OpenAIOptimizer, ProgressTracker } from './cost_optimization_utils.js';
import { ProgressTracker } from './progress_tracker.js';

const optimizer = new OpenAIOptimizer({
  batchSize: 10, // 10개씩 배치 처리
  enableCache: true,
  progressTracker: new ProgressTracker('openai_progress.json')
});

// 처리할 항목 필터링 (캐시된 항목 제외)
const itemsToProcess = optimizer.filterUnprocessedItems(allItems);

// 배치 처리
await optimizer.processBatch(itemsToProcess, async (batch) => {
  // OpenAI API 호출 (배치 단위)
  return await openaiApiCall(batch);
});
```

#### B. 진행 상황 저장 및 재개

```javascript
const tracker = new ProgressTracker('processing_progress.json');
await tracker.load(); // 이전 진행 상황 로드

// 재개 가능한 처리
const unprocessedItems = tracker.filterUnprocessedItems(allItems);

for (let i = 0; i < unprocessedItems.length; i++) {
  try {
    await processItem(unprocessedItems[i]);
    await tracker.update(i + tracker.progress.processed, unprocessedItems[i].id, i);
  } catch (error) {
    await tracker.addError(error, unprocessedItems[i].id, i);
    // 에러 발생 시에도 다음 항목 계속 처리
  }
}
```

#### C. 비용 모니터링

```javascript
// 예상 비용 계산 함수
function estimateCost(itemCount, avgTokensPerItem = 700) {
  const totalTokens = itemCount * avgTokensPerItem;
  const costPer1KTokens = 0.027; // GPT-4 예시
  return (totalTokens / 1000) * costPer1KTokens;
}

// 비용 제한 설정
const MAX_COST = 100; // $100
const estimatedCost = estimateCost(130000);
if (estimatedCost > MAX_COST) {
  console.warn(`⚠️ 예상 비용($${estimatedCost.toFixed(2)})이 제한($${MAX_COST})을 초과합니다.`);
}
```

### 3. **추가 권장 사항**

1. **테스트 단계**
   - 소량 데이터로 먼저 테스트 (예: 100개)
   - 실제 비용 측정
   - 최적 배치 크기 확인

2. **점진적 확장**
   - 1,000개 → 10,000개 → 100,000개 단계별 확장
   - 각 단계에서 비용 및 성능 평가

3. **대안 모델 고려**
   - GPT-3.5-turbo: 더 저렴하지만 품질 낮음
   - Claude, Gemini 등 다른 모델 비교

4. **로컬 모델 활용**
   - Ollama, LM Studio 등 로컬 LLM 사용 검토
   - 완전 무료 (하드웨어 비용 제외)

## 📝 체크리스트

- [x] Notion API 페이지네이션 처리
- [x] Rate Limiting 구현
- [x] 재시도 로직 구현
- [x] 진행 상황 추적 시스템
- [x] 캐싱 시스템
- [x] 배치 처리 유틸리티
- [ ] OpenAI API 통합 시 비용 최적화 적용
- [ ] 비용 모니터링 시스템
- [ ] 테스트 단계 실행

## 🔗 관련 파일

- `read_notion_database.js`: 페이지네이션 및 Rate Limiting 구현
- `cost_optimization_utils.js`: 비용 최적화 유틸리티 함수들
- `progress_tracker.js`: 진행 상황 추적 및 재개 기능
