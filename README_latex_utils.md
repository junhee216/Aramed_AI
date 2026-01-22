# LaTeX 변환 유틸리티 사용 가이드

## 개요
`latex_utils.py`와 `convert_template.py`는 LaTeX 파일을 딥시크용 CSV/JSON으로 변환하는 작업을 빠르게 수행하기 위한 재사용 가능한 유틸리티입니다.

## 주요 기능

### 1. `latex_utils.py` - 핵심 유틸리티 함수들

#### `extract_body(latex_content)`
- LaTeX 본문만 추출 (`\begin{document}` ~ `\end{document}`)

#### `diagnose_latex_structure(body, max_chars=500)`
- LaTeX 본문 구조를 진단하여 디버깅에 도움
- 백슬래시, 달러 기호, 전각/반각 문자, 줄바꿈 패턴 확인

#### `extract_options_generic(options_text, num_options=5)`
- 일반적인 선택지 추출 (분수, 정수, 제곱근 등)
- 다양한 패턴을 자동으로 시도

#### `extract_problem_with_options(body, question_pattern, boundary_pattern, ...)`
- 문제와 선택지를 함께 추출하는 범용 함수

#### `test_pattern(pattern, body, context_chars=100)`
- 패턴 테스트 및 매칭 결과 출력

### 2. `convert_template.py` - 변환 템플릿

#### 사용 방법:
1. `extract_problems_from_latex()` 함수를 각 파일에 맞게 수정
2. `main()` 함수 호출

## 사용 예시

```python
from convert_template import main
from latex_utils import extract_body, diagnose_latex_structure

# LaTeX 내용
latex_content = """..."""

# 초기 진단 (디버깅)
body = extract_body(latex_content)
diagnose_latex_structure(body)  # 구조 확인

# 변환 실행
output_dir = r"C:\Users\a\Documents\MathPDF-현우진-수1_2025학년도_현우진_드릴"
base_filename = "수1_2025학년도_현우진_드릴_P2_문제"
main(latex_content, output_dir, base_filename, debug=True)
```

## 개선 사항

### 이전 문제점:
1. 매번 LaTeX 구조를 수동으로 확인
2. 패턴을 처음부터 작성
3. 디버깅 코드를 매번 추가

### 개선 후:
1. **초기 진단 자동화**: `diagnose_latex_structure()`로 즉시 구조 파악
2. **재사용 가능한 패턴**: `extract_options_generic()` 등 범용 함수 사용
3. **템플릿 기반 작업**: `convert_template.py`를 복사하여 수정만 하면 됨

## 다음 작업 시 절차

1. **새 파일 변환 시**:
   ```python
   # convert_new_file.py 생성
   from convert_template import main, extract_problems_from_latex
   from latex_utils import *
   
   # extract_problems_from_latex() 함수만 수정
   # 각 문제의 패턴만 정의하면 됨
   ```

2. **디버깅이 필요할 때**:
   ```python
   diagnose_latex_structure(body)  # 구조 확인
   test_pattern(pattern, body)      # 패턴 테스트
   ```

3. **선택지 추출이 어려울 때**:
   ```python
   options = extract_options_generic(options_text)  # 자동으로 다양한 패턴 시도
   ```

## 주의사항

- 각 LaTeX 파일의 구조가 다를 수 있으므로, `extract_problems_from_latex()` 함수는 파일별로 수정 필요
- 하지만 공통 부분(본문 추출, 검토, 저장)은 재사용 가능
- 디버깅 함수를 활용하면 문제 원인을 빠르게 파악 가능
