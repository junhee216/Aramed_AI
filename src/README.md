# 📘 Project Aramed: Digital Socrates Math System
**Version:** 2.0 (Ultimate Edition)
**Last Updated:** 2026-01-11

## 1. 프로젝트 철학 (Philosophy)
- **Digital Socrates:** 정답 제공이 아닌, '질문형 힌트'를 통한 사고 확장.
- **Zero-Cost First:** API 호출 전 로컬 캐시 및 노션 메타데이터 우선 활용 (비용 99% 절감).
- **Transparency:** AI의 기술적 한계와 비용 발생을 사용자에게 솔직히 고지.

## 2. 시스템 아키텍처 (Architecture)


1. **Level 0 (Local Filter):** 학생 입력 분석 및 기본 템플릿 응답 ($0)
2. **Level 1 (Cache Hit):** `data/cache_store.json`에서 기존 답변 재사용 ($0)
3. **Level 2 (Template Engine):** Notion `Hint_Stage_N` 메타데이터 조합 ($0)
4. **Level 3 (AI Invocation):** 해결 불가 시 최종적으로 OpenAI/Claude 호출 (비용 발생)

## 3. 폴더 및 파일 구조 (Directory Structure)
- `src/database/`: Notion API 연동 및 Cache 관리
- `src/logic/`: 힌트 단계 결정 알고리즘 (`thinking.js`)
- `src/middleware/`: Rate Limiter 및 로깅 시스템
- `data/`: 로컬 캐시 및 반응형 멘트 템플릿
- `logs/`: 접속 로그, 비용 추적, 에러 리포트

## 4. 실행 가이드 (Quick Start)
- **DB 연결 확인:** `node read_notion_database.js`
- **프로그레스 저장:** `node save_progress.js`
- **배치 업로드:** `node batch_upload.js` (준비 중)

---
*본 프로젝트는 편의점 카운터의 극한 환경에서 탄생한 고밀도 경영 자산입니다.*

