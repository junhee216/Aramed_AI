# Mathpix LaTeX 빠른 처리 가이드

## 개요
Mathpix에서 온 LaTeX 파일을 빠르게 처리하기 위한 워크플로우입니다.

## 기본 사용법

### 1. 자동 모드 (가장 빠름)
```python
from mathpix_latex_processor import quick_process_mathpix_latex

# Mathpix에서 온 LaTeX 내용
latex_content = """..."""

# 처리
problems = quick_process_mathpix_latex(
    latex_content=latex_content,
    output_dir=r"C:\Users\a\Documents\MathPDF-현우진-수1_2025학년도_현우진_드릴",
    base_filename="수1_2025학년도_현우진_드릴_P2_문제",
    debug=True  # 자동 진단 활성화
)
```

### 2. 커스텀 추출기 사용 (문제 패턴이 특수한 경우)
```python
from mathpix_latex_processor import quick_process_mathpix_latex
from latex_utils import extract_options_generic, clean_latex_text
import re

def custom_extractor(body):
    """커스텀 문제 추출 함수"""
    problems = []
    
    # 문제 1번 추출 예시
    p1_match = re.search(r'(문제 시작 패턴.*?\[4점\])(.*?)(?=\\section)', body, re.DOTALL)
    if p1_match:
        question = clean_latex_text(p1_match.group(1))
        options_text = p1_match.group(2) if p1_match.lastindex >= 2 else ""
        options = extract_options_generic(options_text)
        
        problems.append({
            "index": "01",
            "page": 1,
            "topic": "주제",
            "question": question,
            "point": 4,
            "answer_type": "multiple_choice" if len(options) == 5 else "short_answer",
            "options": options
        })
    
    # 문제 2번, 3번... 추가
    
    return problems

# 처리
problems = quick_process_mathpix_latex(
    latex_content=latex_content,
    output_dir=output_dir,
    base_filename=base_filename,
    custom_extractor=custom_extractor
)
```

## 워크플로우

### Step 1: Mathpix LaTeX 받기
```
사용자: "Mathpix에서 온 LaTeX입니다"
```

### Step 2: 자동 진단 실행
```python
processor = MathpixLatexProcessor(latex_content, output_dir, base_filename)
# 자동으로 구조 진단 실행됨
```

**자동으로 확인되는 것:**
- 백슬래시 이스케이프 패턴 (`\$`, `\\` 등)
- 전각/반각 문자 (`［`, `[` 등)
- 섹션 구조 (`\section*{...}`)
- 이미지 포함 여부
- 키워드 위치 (보기, section, Chapter 등)

### Step 3: 문제 추출

#### 옵션 A: 자동 추출 (스마트 모드)
```python
processor.process(mode='auto')
```
- 점수 마커(`[4점]`, `［4점］`)를 기준으로 자동으로 문제 구분
- 선택지 자동 감지 및 추출
- **장점**: 빠름, 대부분의 경우 작동
- **단점**: 복잡한 구조에서는 수정 필요

#### 옵션 B: 커스텀 추출
```python
def my_extractor(body):
    # 각 문제별 패턴 정의
    problems = []
    # 문제 1, 2, 3... 추출
    return problems

processor.process(mode='custom', custom_extractor=my_extractor)
```

### Step 4: 검토 및 저장
- 자동으로 LaTeX 오류 검사
- 선택지 수 확인
- CSV/JSON 자동 저장

## 빠른 문제 해결

### 문제 1: 패턴 매칭 실패
```python
from latex_utils import test_pattern

# 패턴 테스트
test_pattern(r'패턴', body)
# 결과: 매칭 성공/실패 + 주변 텍스트 출력
```

### 문제 2: 선택지 추출 실패
```python
from latex_utils import extract_options_generic, diagnose_latex_structure

# 구조 확인
diagnose_latex_structure(body)

# 선택지 텍스트만 따로 추출
options = extract_options_generic(options_text)
```

### 문제 3: 문제 경계 찾기 어려움
```python
from latex_utils import find_keyword_positions

# 키워드 위치 확인
find_keyword_positions(body, ['section', 'Chapter', '문제'])
```

## 체크리스트

Mathpix LaTeX 처리 시 확인할 것:

- [ ] 자동 진단 실행 (`auto_diagnose=True`)
- [ ] 백슬래시 이스케이프 패턴 확인 (`\$` vs `$`)
- [ ] 전각/반각 문자 확인 (`［` vs `[`)
- [ ] 줄바꿈 패턴 확인 (`\n` vs `\\`)
- [ ] 선택지 패턴 확인 (`(1)` vs `①`)
- [ ] 문제 경계 확인 (`\section` 위치)

## 예시: 실제 사용

```python
# convert_su1_p3_problems.py
from mathpix_latex_processor import quick_process_mathpix_latex
from latex_utils import *
import re

# Mathpix LaTeX 내용
latex_content = """..."""

def extract_p3_problems(body):
    problems = []
    
    # 문제 1번
    p1 = extract_problem_with_options(
        body,
        r'(\\?\$a>1\\?\$.*?\[4점\])',
        r'(\\section|\\end)',
        options_extractor=extract_options_generic
    )
    if p1 and len(p1['options']) == 5:
        problems.append({
            "index": "01", "page": 1, "topic": "지수함수와 로그함수",
            "question": p1['question'], "point": 4,
            "answer_type": "multiple_choice", "options": p1['options']
        })
    
    # 문제 2번, 3번... 추가
    
    return problems

# 실행
quick_process_mathpix_latex(
    latex_content,
    r"C:\Users\a\Documents\MathPDF-현우진-수1_2025학년도_현우진_드릴",
    "수1_2025학년도_현우진_드릴_P3_문제",
    custom_extractor=extract_p3_problems
)
```

## 주의사항

1. **항상 자동 진단 먼저 실행**: 구조를 파악한 후 패턴 작성
2. **패턴 테스트 활용**: `test_pattern()`으로 매칭 확인
3. **재사용 가능한 함수 사용**: `extract_options_generic()` 등 활용
4. **디버깅 정보 확인**: 문제 발생 시 진단 결과 확인

## 다음 단계

Mathpix LaTeX를 받으면:
1. `quick_process_mathpix_latex()` 실행
2. 자동 진단 결과 확인
3. 필요시 커스텀 추출기 작성
4. 검토 및 저장

**이제 훨씬 빠르게 처리할 수 있습니다!**
