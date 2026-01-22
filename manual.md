# 📘 Project Aramed: Digital Socrates Math System - 개발 매뉴얼

**작성일:** 2026-01-12  
**프로젝트 버전:** 2.0 (Ultimate Edition)  
**마지막 업데이트:** 2026-01-12 13:06:22

---

## 📋 목차

1. [프로젝트 개요](#프로젝트-개요)
2. [시스템 아키텍처](#시스템-아키텍처)
3. [작성된 코드 파일 목록](#작성된-코드-파일-목록)
4. [코드 상세 설명](#코드-상세-설명)
5. [폴더 구조](#폴더-구조)
6. [사용 가이드](#사용-가이드)
7. [Aramed 특허 전략: 지식재산권 보호](#🛡️-aramed-특허-전략-지식재산권-보호)
8. [구글 시트 가공 및 노션 업로드 전략](#📊-구글-시트-가공-및-노션-업로드-전략)

---

## 🎯 프로젝트 개요

### 프로젝트 철학
- **Digital Socrates:** 정답 제공이 아닌, '질문형 힌트'를 통한 사고 확장
- **Zero-Cost First:** API 호출 전 로컬 캐시 및 노션 메타데이터 우선 활용 (비용 99% 절감)
- **Transparency:** AI의 기술적 한계와 비용 발생을 사용자에게 솔직히 고지

### 프로젝트 목적
수학 학습자를 위한 지능형 힌트 시스템 구축. Notion 데이터베이스와 연동하여 대량의 수학 문제 데이터를 효율적으로 관리하고, PDF 형식의 수학 문제집을 체계적으로 정리하는 시스템.

---

## 🏗️ 시스템 아키텍처

### 4단계 처리 레벨

```
Level 0 (Local Filter)
  ↓ $0
Level 1 (Cache Hit)
  ↓ $0  
Level 2 (Template Engine)
  ↓ $0
Level 3 (AI Invocation)
  ↓ 비용 발생
```

1. **Level 0 (Local Filter):** 학생 입력 분석 및 기본 템플릿 응답 ($0)
2. **Level 1 (Cache Hit):** `data/cache_store.json`에서 기존 답변 재사용 ($0)
3. **Level 2 (Template Engine):** Notion `Hint_Stage_N` 메타데이터 조합 ($0)
4. **Level 3 (AI Invocation):** 해결 불가 시 최종적으로 OpenAI/Claude 호출 (비용 발생)

### 핵심 설계 원칙
- **비용 최적화:** 캐시 우선, API 호출 최소화
- **확장성:** 13만 개 이상의 대량 데이터 처리 가능
- **안정성:** Rate Limiting, 재시도 로직, 오류 처리
- **유지보수성:** 모듈화된 구조, 명확한 책임 분리

---

## 📁 작성된 코드 파일 목록

### JavaScript/Node.js 파일 (Aramed_AI 시스템)

| 파일명 | 경로 | 작성일 | 용도 |
|--------|------|--------|------|
| `rate_limiter.js` | `src/middleware/` | 2026-01-12 | API 호출 속도 제한 미들웨어 |
| `batch_upload.js` | 루트 | 2026-01-12 | Notion 대량 데이터 배치 업로드 |
| `cache_manager.js` | `src/database/` | (기존) | 로컬 캐시 관리 시스템 |
| `logger.js` | `src/middleware/` | (기존) | 로깅 시스템 |
| `thinking.js` | `src/logic/` | (기존) | 힌트 단계 결정 알고리즘 |
| `read_notion_database.js` | 루트 | (기존) | Notion 데이터베이스 읽기 |
| `save_progress.js` | 루트 | (기존) | 진행 상황 Notion 저장 |

### Python 파일 (PDF 처리)

| 파일명 | 경로 | 작성일 | 용도 |
|--------|------|--------|------|
| `pdf_math_extractor.py` | 루트 | 2026-01-12 | PDF 수학 문제집 단원별 텍스트 추출 |
| `organize_pdf.py` | 루트 | 2026-01-12 | PDF 파일 정리 및 분할 도구 |

---

## 💻 코드 상세 설명

### 1. `src/middleware/rate_limiter.js` ⏱️

**용도:** API 호출 간 지연을 적용하여 Rate Limit 초과를 방지하는 미들웨어

**주요 기능:**
- 1초 지연 기본값 (유동적 설정 가능)
- 초당 최대 요청 수 제한 옵션
- 통계 정보 제공
- 여러 RateLimiter 인스턴스 생성 가능

**핵심 코드 구조:**
```javascript
export class RateLimiter {
  constructor(delayMs = 1000, maxRequestsPerSecond = null)
  async waitIfNeeded()  // 지연 시간 계산 및 대기
  setDelay(newDelayMs)  // 지연 시간 동적 변경
  getStats()  // 통계 정보 반환
}
```

**사용 예시:**
```javascript
import { createRateLimiter } from './src/middleware/rate_limiter.js';
const rateLimiter = createRateLimiter(1000); // 1초 지연
await rateLimiter.waitIfNeeded(); // 다음 요청 전 대기
```

**적용 위치:**
- `batch_upload.js` - Notion API 호출 제한
- `read_notion_database.js` - 대량 데이터 조회 시 제한

---

### 2. `batch_upload.js` 📤

**용도:** 13만 개 이상의 대량 데이터를 Notion 데이터베이스에 효율적으로 업로드

**주요 기능:**
- 배치 단위 처리 (BATCH_SIZE = 50)
- 1초 지연 적용 (rate_limiter 사용)
- 재시도 로직 (최대 3회, 지수 백오프)
- 진행 상황 추적 및 로깅
- 오류 처리 및 통계 리포트

**핵심 함수:**
- `convertItemToProperties()` - 데이터를 Notion 속성 형식으로 변환
- `createPageWithRetry()` - 재시도 로직이 포함된 페이지 생성
- `uploadBatch()` - 배치 단위 업로드 메인 함수
- `main()` - 실행 함수

**설정 값:**
```javascript
BATCH_SIZE = 50          // 배치 크기
MAX_RETRIES = 3          // 최대 재시도 횟수
RETRY_DELAY_MS = 2000    // 재시도 대기 시간
```

**사용 방법:**
```bash
node batch_upload.js
# 또는 코드에서 import하여 사용
import { uploadBatch } from './batch_upload.js';
```

**처리 흐름:**
1. 데이터 배열을 50개씩 배치로 분할
2. 각 항목마다 1초 지연 적용
3. Notion API 호출 (재시도 로직 포함)
4. 진행 상황 로깅
5. 결과 통계 출력

---

### 3. `pdf_math_extractor.py` 📄

**용도:** PDF 수학 문제집에서 단원별로 문제를 추출하여 텍스트로 변환

**주요 기능:**
- PDF 텍스트 추출 (PyPDF2/pdfplumber/pymupdf 지원)
- 단원 패턴 자동 감지 (제N단원, Unit N 등)
- 문제 번호 인식 (1번, 1., 1), ①② 등)
- 하위 문제 추출 (가), 나), 다))
- JSON 또는 텍스트 파일로 저장

**핵심 클래스:**
```python
class PDFMathExtractor:
  def extract_text()  # PDF 텍스트 추출
  def detect_unit_patterns()  # 단원 패턴 감지
  def detect_problem_patterns()  # 문제 번호 인식
  def process()  # 전체 처리
  def save_to_json()  # JSON 형식으로 저장
  def save_to_text_files()  # 텍스트 파일로 저장
```

**사용 방법:**
```bash
# JSON 출력
python pdf_math_extractor.py 수학문제집.pdf

# 텍스트 파일 출력
python pdf_math_extractor.py 수학문제집.pdf text
```

**출력 형식:**
- JSON: 단원별 문제 구조화된 데이터
- 텍스트: 단원별로 분리된 `.txt` 파일

---

### 4. `organize_pdf.py` 📁

**용도:** PDF 파일을 6개 폴더(수1, 수2, 미적분, 확률, 통계, 기하)로 분류하고, 파일명 표준화 및 15MB 초과 파일을 10MB 단위로 분할

**주요 기능:**
- **6개 대분류 폴더만 사용** (수1, 수2, 미적분, 확률, 통계, 기하 + 미분류)
- 파일명 표준화: `[과목]_[교재명]_[파트].pdf` 형식
- 전체 페이지 수 계산 및 CSV 기록
- 15MB 초과 파일을 10MB 단위로 자동 분할
- 경로 고정: `C:\Users\a\Documents\MathPDF`
- 처리 결과를 `file_list.csv`로 저장

**핵심 클래스:**
```python
class PDFOrganizer:
  def extract_subject()  # 6개 폴더 중 하나로 과목 추출
  def get_total_pages()  # PDF 전체 페이지 수 계산
  def standardize_filename()  # 파일명 표준화
  def split_pdf()  # PDF 분할
  def organize_file()  # 단일 파일 정리
  def process_all()  # 모든 파일 처리
  def save_file_list()  # CSV로 저장 (페이지 수 포함)
```

**인식 키워드 (6개 폴더):**
- **수1:** 수1, 수학1, 수학 1, 수i, -수1-
- **수2:** 수2, 수학2, 수학 2, 수ii, -수2-
- **미적분:** 미적분, 미적, 미분, 적분, calculus
- **확률:** 확률, 확률과통계, 확통
- **통계:** 통계
- **기하:** 기하, 공간도형, 벡터, geometry
- **미분류:** 위 키워드에 해당하지 않을 경우

**폴더 구조 (단순화):**
```
C:\Users\a\Documents\MathPDF\
└── organized/
    ├── 수1/
    │   └── 수1_교재명_P1.pdf
    ├── 수2/
    ├── 미적분/
    ├── 확률/
    ├── 통계/
    ├── 기하/
    └── 미분류/
```

**사용 방법:**
```bash
# 경로가 고정되어 있어서 인자 없이 실행
python organize_pdf.py
```

**분할 기준:**
- 15MB 초과 → 자동 분할
- 10MB 단위로 분할
- `파일명_P1.pdf`, `파일명_P2.pdf` 형식 (파트 번호)

**CSV 기록 항목:**
- 원본파일명
- 표준화파일명
- 과목 (6개 폴더)
- 크기(MB)
- **전체페이지수** (새로 추가됨)
- 상태
- 새위치
- 분할개수
- 처리일시

---

## 📂 폴더 구조

```
Aramed_AI/
├── src/                          # 소스 코드
│   ├── ai/                       # AI 클라이언트
│   │   ├── gpt_client.js         # GPT 클라이언트 (구현 예정)
│   │   └── prompts.js            # 프롬프트 관리
│   ├── config/                   # 설정
│   │   └── constants.js          # 상수 정의
│   ├── database/                 # 데이터베이스
│   │   └── cache_manager.js      # 캐시 관리 (TTL 지원)
│   ├── logic/                    # 비즈니스 로직
│   │   └── thinking.js           # 힌트 단계 결정 알고리즘
│   ├── middleware/               # 미들웨어
│   │   ├── logger.js             # 로깅 시스템
│   │   └── rate_limiter.js       # Rate Limiting ⭐ 신규
│   └── README.md                 # src 폴더 설명
│
├── data/                         # 데이터 파일
│   ├── cache_store.json          # 캐시 저장소
│   └── templates.json            # 템플릿 데이터
│
├── logs/                         # 로그 파일
│   └── access.log                # 접속 로그
│
├── batch_upload.js               # 배치 업로드 스크립트 ⭐ 신규
├── organize_pdf.py               # PDF 정리 도구 ⭐ 신규
├── pdf_math_extractor.py         # PDF 추출 도구 ⭐ 신규
├── read_notion_database.js       # Notion DB 읽기
├── save_progress.js              # 진행 상황 저장
├── server.js                     # 서버 메인 파일
├── package.json                  # Node.js 패키지 정보
├── requirements.txt              # Python 라이브러리 목록 ⭐ 신규
├── manual.md                     # 본 문서 ⭐ 신규
├── README_PDF_EXTRACTOR.md       # PDF 추출 가이드 ⭐ 신규
├── README_PDF_ORGANIZER.md       # PDF 정리 가이드 ⭐ 신규
└── .env                          # 환경변수 (gitignore)
```

---

## 🚀 사용 가이드

### 환경 설정

#### 1. Node.js 환경 설정
```bash
# 패키지 설치
npm install

# 환경변수 설정 (.env 파일)
NOTION_API_KEY=secret_xxx
NOTION_DATABASE_ID=xxx
NOTION_PAGE_ID=xxx
```

#### 2. Python 환경 설정 (PDF 처리용)
```bash
# Python 라이브러리 설치
pip install PyPDF2
# 또는
pip install -r requirements.txt
```

### 주요 스크립트 실행

#### Notion 관련

**1. 데이터베이스 읽기:**
```bash
node read_notion_database.js
```
- Notion 데이터베이스 조회
- Rate Limiting 적용 (초당 3회)
- 페이지네이션 처리

**2. 배치 업로드:**
```bash
node batch_upload.js
```
- 대량 데이터 업로드
- 1초 지연 적용
- 배치 단위 처리

**3. 진행 상황 저장:**
```bash
node save_progress.js
```
- 세션 요약 및 진행 상황을 Notion에 저장

#### PDF 처리

**1. PDF 단원별 추출:**
```bash
python pdf_math_extractor.py 수학문제집.pdf
```
- PDF에서 단원별 문제 추출
- JSON 또는 텍스트 파일로 저장

**2. PDF 파일 정리:**
```bash
python organize_pdf.py
```
- 경로 고정: `C:\Users\a\Documents\MathPDF`
- 6개 폴더 분류 (수1, 수2, 미적분, 확률, 통계, 기하 + 미분류)
- 파일명 표준화: `[과목]_[교재명]_[파트].pdf`
- 전체 페이지 수 계산 및 CSV 기록
- 대용량 파일(15MB 초과) 자동 분할 (10MB 단위)

---

## 📊 시스템 통합 구조

### 데이터 흐름

```
PDF 파일
  ↓ (organize_pdf.py)
정리된 PDF 폴더
  ↓ (pdf_math_extractor.py)
구조화된 JSON 데이터
  ↓ (batch_upload.js)
Notion 데이터베이스
  ↓ (cache_manager.js)
로컬 캐시
  ↓ (thinking.js)
사용자에게 힌트 제공
```

### 컴포넌트 간 의존성

```
batch_upload.js
  ├── src/middleware/rate_limiter.js
  └── src/middleware/logger.js

read_notion_database.js
  ├── @notionhq/client
  └── rate_limiter (내장)

thinking.js
  ├── src/database/cache_manager.js
  └── src/middleware/logger.js

cache_manager.js
  └── src/middleware/logger.js
```

---

## 🔧 주요 설정 값

### Rate Limiting
- **기본 지연:** 1000ms (1초)
- **Notion API 제한:** 초당 3회 (read_notion_database.js)

### 배치 처리
- **배치 크기:** 50개
- **최대 재시도:** 3회
- **재시도 지연:** 2000ms (지수 백오프)

### PDF 분할
- **분할 기준:** 15MB 초과 파일
- **분할 단위:** 10MB
- **분할 파일명:** `[과목]_[교재명]_P1.pdf`, `P2.pdf`, ...

### 캐시
- **캐시 파일:** `data/cache_store.json`
- **TTL 지원:** 있음

---

## 📝 개발 히스토리

### 2026-01-12
- ✅ `src/middleware/rate_limiter.js` 작성
  - 1초 지연 기본값 설정
  - 유동적 설정 가능하도록 구현
  - 마스터플랜 V2.0 요구사항 반영

- ✅ `batch_upload.js` 작성
  - 13만 개 데이터 기준 처리
  - 배치 단위 처리 (50개씩)
  - 1초 지연 적용
  - 재시도 로직 구현
  - 진행 상황 추적 및 로깅

- ✅ `pdf_math_extractor.py` 작성
  - PDF 단원별 텍스트 추출
  - 다중 PDF 라이브러리 지원
  - JSON/텍스트 출력 형식

- ✅ `organize_pdf.py` 작성
  - PDF 파일 자동 정리
  - 과목/년도/중단원별 분류
  - 대용량 파일 자동 분할
  - CSV 결과 저장

- ✅ `requirements.txt` 작성
- ✅ `README_PDF_EXTRACTOR.md` 작성
- ✅ `README_PDF_ORGANIZER.md` 작성
- ✅ `manual.md` 작성 (본 문서)

---

## 🎓 코딩 스타일 및 규칙

### JavaScript
- ES6+ 모듈 시스템 사용 (`import`/`export`)
- ESM 형식 (`"type": "module"` in package.json)
- Node.js 18 이상 필요
- 비동기 처리: `async/await` 사용

### Python
- Python 3.7 이상
- 타입 힌트 사용 (선택적)
- docstring 포함
- 에러 처리: try-except 사용

### 공통
- 명확한 함수/클래스 이름
- 주석 및 문서화
- 오류 처리 포함
- 로깅 시스템 활용

---

## ⚠️ 주의사항

1. **환경변수 보안**
   - `.env` 파일을 git에 커밋하지 않기
   - `.gitignore`에 `.env` 추가

2. **Rate Limiting**
   - Notion API 제한 준수 (초당 3회)
   - 대량 데이터 처리 시 반드시 rate_limiter 사용

3. **PDF 처리**
   - 스캔된 이미지 PDF는 OCR 필요할 수 있음
   - 텍스트 추출 가능한 PDF 권장

4. **메모리 관리**
   - 대량 데이터 처리 시 배치 크기 조정
   - PDF 분할 시 파일 크기 모니터링

---

## 🛡️ Aramed 특허 전략: 지식재산권 보호

### 핵심 기술명

**AI-Human 하이브리드 수학 교육 데이터 정제 및 자기진화 시스템**

### 기술적 차별점

본 프로젝트의 핵심 기술은 다음과 같은 차별화된 요소들을 포함합니다:

1. **로컬 파이썬을 활용한 데이터 전처리 및 물리적 주소 지정 기술**
   - Python 기반 PDF 파일 자동 분류 및 표준화 시스템
   - 파일명 표준화 알고리즘: `[과목]_[교재명]_[파트].pdf` 형식
   - 물리적 주소 기반 체계적 데이터 구조화
   - 대용량 파일 자동 분할 기술 (15MB 초과 → 10MB 단위)
   - 구현 파일: `organize_pdf.py`

2. **LLM 기반 3단계 소크라테스식 질문 해설 생성 엔진**
   - Level 0: 로컬 필터 및 기본 템플릿 응답
   - Level 1: 캐시 히트 (기존 답변 재사용)
   - Level 2: Notion 메타데이터 기반 템플릿 엔진
   - Level 3: AI 호출 (최종 단계)
   - 정답 제공이 아닌 질문형 힌트를 통한 사고 확장
   - 구현 파일: `src/logic/thinking.js`

3. **인간 검수 결과의 피드백 루프를 통한 생성 품질 고도화 알고리즘**
   - 사용자 피드백을 통한 지속적 학습 메커니즘
   - 캐시 시스템을 통한 검증된 답변 축적
   - TTL(Time To Live) 기반 캐시 관리 시스템
   - 구현 파일: `src/database/cache_manager.js`

### 데이터 보호: Database Right 확보 전략

**13만 개의 라벨링된 메타데이터 DB권(Database Right) 확보 방안:**

1. **데이터 구조화 및 메타데이터 관리**
   - Notion 데이터베이스에 체계적으로 구조화된 메타데이터 저장
   - 파일명 표준화를 통한 일관된 데이터 라벨링
   - 페이지 수, 파일 크기, 분류 정보 등 상세 메타데이터 기록

2. **물리적 주소 기반 데이터 관리**
   - 고정된 물리적 경로: `C:\Users\a\Documents\MathPDF`
   - 체계적인 폴더 구조 (6개 대분류 폴더)
   - CSV 파일을 통한 메타데이터 백업 및 추적

3. **데이터베이스 권리(Database Right) 확보**
   - 자체 생성 및 구조화된 데이터베이스
   - 13만 개 이상의 체계적 라벨링된 메타데이터
   - 독창적인 분류 체계 및 표준화 알고리즘
   - 지속적인 데이터 축적 및 관리 시스템

4. **지식재산권 보호 전략**
   - 핵심 알고리즘의 코드 레벨 보호
   - 데이터 구조 및 분류 체계의 독창성
   - 하이브리드 시스템(인간+AI)의 창의적 접근
   - 지속적 개선을 통한 기술 고도화

### 특허 출원 고려사항

1. **기술의 신규성 및 진보성**
   - AI-Human 하이브리드 방식의 수학 교육 데이터 정제
   - 자기진화 알고리즘을 통한 지속적 품질 향상
   - 3단계 소크라테스식 질문 생성 시스템

2. **산업상 이용 가능성**
   - 온라인 교육 플랫폼
   - 개인화 학습 시스템
   - AI 기반 교육 콘텐츠 생성 도구

3. **보호 범위**
   - 알고리즘 및 시스템 아키텍처
   - 데이터 분류 및 표준화 방법
   - 피드백 루프를 통한 품질 향상 메커니즘

---

## 📊 구글 시트 가공 및 노션 업로드 전략

### 개요

PDF 파일을 난이도별로 분류하고 구조화된 데이터로 변환하여 Notion에 일괄 업로드하기 위한 워크플로우입니다. Claude AI를 활용한 데이터 추출 및 구글 시트를 통한 검수 과정을 포함합니다.

### 1. Claude AI를 통한 PDF 분석 및 데이터 추출

#### Claude 업로드용 프롬프트

PDF를 Claude에 업로드한 후 아래 프롬프트를 사용하세요:

```
너는 대한민국 최고의 수학 교육 데이터 분석가야. 지금 업로드한 PDF의 [N페이지]를 분석해서, 나중에 내가 '구글 시트'에 붙여넣고 '노션'으로 일괄 업로드할 수 있도록 아래 규칙에 맞춰 정리해줘.

[데이터 추출 및 라벨링 규칙]
1. 문제 ID: 파일명_페이지_문항번호 (예: 수1_현우진_P5_12_01)
2. 출처(Labeling): [년도]_[월]_[시행기관]_[학년]_[번호]. (정보 없으면 '자체교재')
3. 대단원: (수1, 수2, 미적분, 확률, 통계, 기하) 중 하나 선택.
4. 중/소단원: 수능/내신 분류 체계에 따른 정밀 단원명.
5. 난이도: 하, 중, 상, 최상 중 선택.
6. 핵심개념: 문제 풀이의 핵심 공식.
7. 3단계 힌트: 학생의 사고를 유도하는 질문형 (힌트1, 힌트2, 힌트3).
8. LaTeX 수식: 모든 수식은 반드시 $...$ 형식을 사용.

[구글 시트 복사 전용 출력 가이드]
- Markdown 표(Table) 형식으로 출력해줘.
- 힌트 1, 2, 3은 각각 별도의 열(Column)로 나누어줘.
- 수식이나 텍스트 안에 쉼표(,)가 있다면 노션 업로드 시 칸이 밀릴 수 있으니, 표의 각 셀 내용을 출력할 때 큰따옴표(")로 감싸지 말고 텍스트 그대로 깔끔하게 출력해줘.

이제 분석을 시작하고 표를 그려줘.
```

#### 데이터 추출 규칙 상세

1. **문제 ID 형식**
   - 패턴: `파일명_페이지_문항번호`
   - 예시: `수1_현우진_P5_12_01` (수1_현우진_P5 파일의 12페이지 1번 문제)

2. **출처(Labeling) 형식**
   - 패턴: `[년도]_[월]_[시행기관]_[학년]_[번호]`
   - 정보 없을 경우: `자체교재`
   - 예시: `2024_03_수능_고3_21`

3. **대단원 분류**
   - 선택지: 수1, 수2, 미적분, 확률, 통계, 기하
   - `organize_pdf.py`의 6개 폴더 분류와 일치

4. **중/소단원**
   - 수능/내신 분류 체계에 따른 정밀 단원명
   - 예: 삼각함수, 수열, 극한, 미분법 등

5. **난이도 분류**
   - 하, 중, 상, 최상 (4단계)

6. **핵심개념**
   - 문제 풀이의 핵심 공식 또는 개념

7. **3단계 힌트**
   - 학생의 사고를 유도하는 질문형 힌트
   - 힌트1, 힌트2, 힌트3을 각각 별도 열로 구분
   - Digital Socrates 철학 반영

8. **LaTeX 수식**
   - 모든 수식은 `$...$` 형식 사용
   - 예: `$x^2 + y^2 = r^2$`

### 2. 구글 시트를 통한 검수 및 가공

#### 구글 시트 설정

1. **첫 줄 고정 (헤더 설정)**
   ```
   문제ID | 출처 | 대단원 | 중/소단원 | 난이도 | 핵심개념 | 힌트1 | 힌트2 | 힌트3 | LaTeX수식
   ```

2. **값만 붙여넣기**
   - Claude가 생성한 표를 복사
   - 구글 시트에서 `Ctrl + Shift + V` (값만 붙여넣기)
   - 서식 없이 깔끔한 텍스트만 입력

#### 검수 체크리스트

**Human-in-the-Loop 검수 과정:**

1. **단원 분류 검토**
   - Claude가 대단원/중소단원을 잘못 분류한 경우 수정
   - `organize_pdf.py`의 6개 폴더 분류와 일치하는지 확인

2. **수식 깨짐 확인**
   - LaTeX 수식이 올바르게 표시되는지 확인
   - `$...$` 형식이 유지되는지 검증

3. **라벨링 검토**
   - 출처(Labeling) 정보가 정확한지 확인
   - 문제 ID 형식이 일관된지 검증

4. **힌트 품질 검토**
   - 3단계 힌트가 질문형으로 작성되었는지 확인
   - 학생의 사고를 유도하는지 검증

5. **난이도 일관성**
   - 난이도 분류가 일관된 기준으로 적용되었는지 확인

### 3. Notion 일괄 업로드

#### 업로드 전 준비사항

1. **구글 시트 최종 검수 완료**
   - 모든 데이터가 정확히 입력되었는지 확인
   - 빈 셀이 없는지 확인

2. **Notion 데이터베이스 구조 확인**
   - 구글 시트의 컬럼과 Notion 속성이 일치하는지 확인
   - 필요한 속성(문제ID, 출처, 대단원, 중소단원, 난이도, 핵심개념, 힌트1, 힌트2, 힌트3, LaTeX수식)이 모두 있는지 확인

3. **배치 업로드 실행**
   - `batch_upload.js` 사용
   - 구글 시트 데이터를 JSON 형식으로 변환 후 업로드

#### 업로드 시 주의사항

- **쉼표(,) 처리**: 구글 시트에서 Notion으로 복사 시 쉼표가 포함된 텍스트는 셀 구분자로 인식될 수 있으므로 주의
- **수식 보존**: LaTeX 수식의 `$...$` 형식이 Notion에서도 올바르게 표시되는지 확인
- **대량 업로드**: 13만 개 이상의 데이터는 `batch_upload.js`의 배치 처리 기능 활용

### 4. 워크플로우 요약

```
PDF 파일 (organize_pdf.py로 분류)
  ↓
Claude AI 분석 (프롬프트 사용)
  ↓
구글 시트에 붙여넣기 (Ctrl + Shift + V)
  ↓
Human-in-the-Loop 검수
  ↓
Notion 일괄 업로드 (batch_upload.js)
  ↓
13만 개 데이터베이스 완성
```

### 5. 핵심 원칙

1. **Human-in-the-Loop**
   - AI가 생성한 데이터는 반드시 인간이 검수
   - 편의점 업무 중에도 슥 보면서 수정 가능한 구조

2. **일관성 유지**
   - 문제 ID, 출처, 단원 분류 등 일관된 형식 유지
   - `organize_pdf.py`의 분류 체계와 일치

3. **확장성**
   - 한 줄씩 완성하여 13만 개로 확장
   - 배치 업로드로 대량 처리 가능

---

## 📚 참고 자료

### 프로젝트 문서
- `src/README.md` - 프로젝트 개요 및 아키텍처
- `README_PDF_EXTRACTOR.md` - PDF 추출 도구 사용법
- `README_PDF_ORGANIZER.md` - PDF 정리 도구 사용법
- `COST_OPTIMIZATION_GUIDE.md` - 비용 최적화 가이드

### 외부 라이브러리
- [Notion API](https://developers.notion.com/)
- [PyPDF2](https://pypdf2.readthedocs.io/)
- [pdfplumber](https://github.com/jsvine/pdfplumber)
- [PyMuPDF](https://pymupdf.readthedocs.io/)

---

## 🔄 업데이트 로그

### Version 2.0 (2026-01-12)
- Rate Limiter 미들웨어 추가
- 배치 업로드 시스템 구축
- PDF 처리 도구 추가
- 문서화 완료

---

**작성자:** Auto (Cursor AI Assistant)  
**최종 수정:** 2026-01-12 13:06:22

---

*본 프로젝트는 편의점 카운터의 극한 환경에서 탄생한 고밀도 경영 자산입니다.*