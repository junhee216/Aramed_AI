# Aramed_AI

Mathpix 및 Notion 업무 자동화 프로젝트

## 프로젝트 개요

LaTeX 수학 문제를 Deepseek R1-70B가 읽을 수 있는 형식으로 변환하고, Notion 데이터베이스와 연동하여 문제 검토 및 필드 자동 채우기를 수행하는 프로젝트입니다.

## 주요 기능

1. **LaTeX 변환**: Mathpix로 변환된 LaTeX를 Deepseek R1-70B용 마크다운/JSON으로 변환
2. **수학적 검증**: 문제와 해설의 수학적 오류 및 논리적 일관성 검증
3. **Notion 연동**: Notion API를 통한 문제 데이터 관리 및 자동 필드 채우기

## 프로젝트 구조

```
Aramed_AI/
├── src/                    # 소스 코드
│   ├── middleware/         # 미들웨어 (rate_limiter, logger)
│   └── utils/              # 유틸리티 함수
├── convert_*.py           # LaTeX 변환 스크립트
├── review_and_fill_*.js  # Notion 검토 및 필드 채우기 스크립트
├── .env                    # 환경 변수 (Git에 포함되지 않음)
├── .env.example           # 환경 변수 템플릿
└── .gitignore             # Git 제외 파일 목록
```

## 설치 및 설정

### 1. 의존성 설치

**Python:**
```bash
pip install -r requirements.txt
```

**Node.js:**
```bash
npm install
```

### 2. 환경 변수 설정

`.env.example`을 참고하여 `.env` 파일을 생성하고 필요한 값들을 입력하세요:

```bash
cp .env.example .env
# .env 파일 편집
```

필수 환경 변수:
- `NOTION_API_KEY`: Notion API 키
- `NOTION_DATABASE_ID`: Notion 데이터베이스 ID

## 사용 방법

### LaTeX 변환

```bash
# 기하 P5 문제 변환
python convert_geometry_p5_problems_deepseek.py

# 기하 P5 해설 변환
python convert_geometry_p5_solution_deepseek.py
```

### Notion 필드 검토 및 채우기

```bash
# 기하 P5 Notion 필드 검토 및 26, 27번 필드 채우기
node review_and_fill_geometry_p5_notion.js
```

## Windows ↔ Linux 동기화

Git을 사용하여 Windows 노트북과 Linux 데스크탑 간 코드를 동기화할 수 있습니다.

자세한 내용은 `GIT_SETUP_GUIDE.md`를 참고하세요.

## 주요 스크립트

### 문제 변환
- `convert_geometry_p*_problems_deepseek.py`: 기하 문제 LaTeX → JSON/Markdown 변환
- `convert_geometry_p*_solution_deepseek.py`: 기하 해설 LaTeX → Markdown 변환

### Notion 연동
- `review_and_fill_geometry_p*_notion.js`: Notion 필드 검토 및 자동 채우기

## 개선사항

최근 개선사항은 다음 문서를 참고하세요:
- `IMPROVEMENTS_MATHPIX_NOTION.md`: 전체 개선사항
- `IMPROVEMENTS_MATHPIX_NOTION_V2.md`: 최신 개선사항 (P3, P4 작업 후)
- `IMPROVEMENTS_SUMMARY.md`: 개선사항 요약

## 주의사항

1. **.env 파일은 절대 Git에 커밋하지 마세요**
2. **API 키 보안**: `.env` 파일을 안전하게 관리하세요
3. **Rate Limiting**: Notion API 호출 시 rate limiter가 적용됩니다

## 라이선스

프로젝트 내부 사용 목적
