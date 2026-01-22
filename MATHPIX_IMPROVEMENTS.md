# Mathpix 처리 시스템 개선 사항

## 🎯 개선 완료 (2026-01-13)

### 1. 자동 저장 기능 추가
- **기존**: 사용자 입력 대기 (`input()`)
- **개선**: `auto_save=True` 옵션으로 자동 저장
- **효과**: 배치 처리 및 자동화 가능

### 2. 공통 유틸리티 함수 분리
- **새 파일**: `mathpix_utils.py`
- **기능**:
  - `detect_problem_type()`: 문제 유형 자동 감지
  - `detect_topic_from_content()`: 주제 자동 감지
  - `extract_point_value()`: 점수 추출
  - `find_problem_boundaries()`: 문제 경계 찾기 (최적화)
  - `clean_problem_text()`: 문제 텍스트 정리
  - `validate_problem_structure()`: 문제 구조 검증
  - `auto_save_path()`: 자동 저장 경로 생성

### 3. 성능 최적화
- **사전 컴파일된 정규식**: 반복 사용 패턴 미리 컴파일
- **최적화된 경계 탐색**: 불필요한 텍스트 스캔 최소화

### 4. 에러 처리 개선
- **구조 검증**: 문제 데이터 구조 자동 검증
- **명확한 에러 메시지**: 문제 발생 시 구체적인 오류 정보 제공

## 📝 사용법

### 기본 사용 (자동 저장)
```python
from mathpix_latex_processor import quick_process_mathpix_latex

problems = quick_process_mathpix_latex(
    latex_content=latex_content,
    output_dir=output_dir,
    base_filename=base_filename,
    debug=False,      # 진단 스킵
    auto_save=True    # 자동 저장 (기본값)
)
```

### 공통 유틸리티 사용
```python
from mathpix_utils import (
    detect_problem_type,
    detect_topic_from_content,
    auto_save_path
)

# 문제 유형 감지
problem_type = detect_problem_type(body_snippet)

# 주제 감지
topic = detect_topic_from_content(body_snippet)

# 자동 저장 경로 생성
save_dir, filename = auto_save_path(
    subject="수1",
    year="2025",
    book_name="현우진_드릴",
    part_name="P7",
    problem_or_solution="문제"
)
```

## 🔄 기존 코드 호환성

기존 코드는 그대로 작동하며, 자동 저장 기능이 기본으로 활성화됩니다.

### 변경 전
```python
# 사용자 입력 대기
if is_valid or input("\n저장하시겠습니까? (y/n): ").lower() == 'y':
    save_for_deepseek(...)
```

### 변경 후
```python
# 자동 저장 (auto_save=True일 때)
if is_valid or len(self.problems) > 0:
    save_for_deepseek(...)
```

## 📊 개선 효과

1. **자동화 가능**: 배치 처리 및 스크립트 자동 실행 가능
2. **코드 재사용성 향상**: 공통 유틸리티 함수로 중복 코드 제거
3. **성능 향상**: 사전 컴파일된 정규식으로 처리 속도 개선
4. **유지보수성 향상**: 공통 기능을 한 곳에서 관리

## 🚀 다음 단계

1. 모든 변환 스크립트에 공통 유틸리티 적용
2. 자동 저장 경로 생성 기능 통합
3. 에러 로깅 시스템 추가
4. 배치 처리 스크립트 생성
