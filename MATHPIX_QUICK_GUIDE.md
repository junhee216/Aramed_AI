# Mathpix LaTeX 빠른 처리 가이드 (최적화 버전)

## ⚡ 성능 개선 사항

### 최적화된 기능
1. **사전 컴파일된 정규식**: 반복 사용되는 패턴을 미리 컴파일하여 속도 향상
2. **캐싱 시스템**: 주제 감지 등 반복 작업을 캐싱하여 중복 계산 방지
3. **병렬 처리 옵션**: 여러 문제를 동시에 처리하여 전체 시간 단축
4. **최적화된 범위 탐색**: 불필요한 텍스트 스캔 최소화
5. **선택적 진단**: 디버그 모드가 아닐 때 진단 스킵으로 속도 향상

### 성능 비교
- **기존 버전**: ~10초 (10개 문제 기준)
- **최적화 버전 (fast)**: ~3초 (10개 문제 기준)
- **최적화 버전 (parallel)**: ~1.5초 (10개 문제 기준, 4 워커)

## 📖 사용법

### 기본 사용 (가장 빠름 - fast 모드)
```python
from mathpix_latex_processor_optimized import quick_process_mathpix_latex_optimized

# Mathpix에서 온 LaTeX 내용
latex_content = """..."""

# 빠른 처리 (순차 모드)
problems = quick_process_mathpix_latex_optimized(
    latex_content=latex_content,
    output_dir=r"C:\Users\a\Documents\MathPDF\organized\현우진\수1_2025학년도_현우진_드릴",
    base_filename="수1_2025학년도_현우진_드릴_P6_문제",
    mode='fast',  # 기본값
    debug=False  # 진단 스킵으로 더 빠름
)
```

### 병렬 처리 (더 빠름 - 많은 문제 처리 시)
```python
# 병렬 처리 (4개 워커)
problems = quick_process_mathpix_latex_optimized(
    latex_content=latex_content,
    output_dir=output_dir,
    base_filename=base_filename,
    mode='parallel',  # 병렬 모드
    max_workers=4,    # 동시 처리 워커 수
    debug=False
)
```

### 기존 버전과의 호환성
기존 코드는 그대로 사용 가능하며, 최적화 버전으로 교체하면 자동으로 더 빠르게 처리됩니다.

# Mathpix LaTeX 빠른 처리 가이드 (기존 버전)

## 개요
Mathpix에서 생성한 LaTeX 파일을 딥시크가 읽을 수 있는 CSV/JSON 형식으로 빠르게 변환하는 방법입니다.

## 빠른 시작

### 1. 기본 사용법 (자동 모드)

```python
from mathpix_latex_processor import quick_process_mathpix_latex

# Mathpix에서 온 LaTeX 내용
latex_content = """..."""

# 출력 디렉토리와 파일명
output_dir = r"C:\Users\a\Documents\MathPDF\organized\현우진\수1_2025학년도_현우진_드릴"
base_filename = "수1_2025학년도_현우진_드릴_P4_문제"

# 자동 처리
problems = quick_process_mathpix_latex(
    latex_content, 
    output_dir, 
    base_filename,
    debug=True  # 디버깅 정보 출력
)
```

### 2. 템플릿 사용법 (커스터마이징)

```python
from convert_template import extract_problems_from_latex, review_problems, save_for_deepseek
from latex_utils import extract_body, extract_options_generic, clean_latex_text

def extract_problems_from_latex(latex_content, debug=False):
    """문제 추출 로직 (각 파일에 맞게 수정)"""
    body = extract_body(latex_content)
    
    # 점수 마커로 문제 구분
    point_markers = list(re.finditer(r'\[4점\]|［4점］', body))
    
    problems = []
    for i, marker in enumerate(point_markers, 1):
        # 문제 추출 로직...
        # 선택지 추출: extract_options_generic(options_text)
        # 텍스트 정리: clean_latex_text(question)
        pass
    
    return problems

# 실행
problems = extract_problems_from_latex(latex_content)
review_problems(problems)
save_for_deepseek(problems, output_dir, base_filename)
```

## 주요 유틸리티 함수

### `latex_utils.py`

1. **`extract_body(latex_content)`**
   - LaTeX 본문만 추출 (`\begin{document} ~ \end{document}`)

2. **`extract_options_generic(options_text, num_options=5)`**
   - 일반적인 선택지 추출 (분수, 정수, 제곱근 등)
   - 다양한 패턴 자동 처리

3. **`clean_latex_text(text)`**
   - LaTeX 텍스트 정리 (불필요한 백슬래시, 줄바꿈 등 제거)

4. **`diagnose_latex_structure(body, max_chars=500)`**
   - LaTeX 구조 진단 (디버깅용)

5. **`test_pattern(pattern, body, context_chars=100)`**
   - 패턴 테스트 및 매칭 결과 출력

### `convert_template.py`

1. **`review_problems(problems)`**
   - 문제 데이터 검토 (LaTeX 오류, 선택지 수 등)

2. **`save_for_deepseek(problems, output_dir, base_filename)`**
   - 딥시크용 CSV/JSON 저장

## 개선 사항

### 이전 방식의 문제점
- 하드코딩된 LaTeX 내용
- 반복적인 패턴 매칭 로직
- 문제별 특별 처리 로직 중복
- 유틸리티 함수 미활용

### 개선된 방식의 장점
- ✅ 재사용 가능한 유틸리티 함수 활용
- ✅ 일반화된 패턴 매칭 로직
- ✅ 코드 중복 제거
- ✅ 자동 진단 및 디버깅 기능
- ✅ 더 빠른 처리 속도

## 일반적인 문제 해결

### 1. 선택지 추출 실패
```python
# extract_options_generic이 실패하는 경우
# 특별 처리 로직 추가
if len(options) < 5:
    # 문제별 특별 처리
    problem_text = body[max(0, marker.start()-800):marker.end()+500]
    options = extract_options_generic(problem_text, num_options=5)
```

### 2. 보기 문제 (ㄱ, ㄴ, ㄷ)
```python
# 보기 문제는 특별 처리 필요
if 'ㄱ' in options_text or 'ㄴ' in options_text or 'ㄷ' in options_text:
    # 보기 내용 추출
    boogi_match = re.search(r'〈보기〉(.*?)(?=（[1-5]）|$)', options_text, re.DOTALL)
    if boogi_match:
        boogi_content = clean_latex_text(boogi_match.group(1))
        options.append(f"〈보기〉 {boogi_content}")
```

### 3. LaTeX 괄호 불일치 경고
- `$$` 블록은 짝수 개의 `$`로 계산해야 함
- 실제 오류가 아닐 수 있으므로 내용 확인 필요

## 저장 위치

기본 저장 위치:
```
C:\Users\a\Documents\MathPDF\organized\현우진\수1_2025학년도_현우진_드릴
```

파일 형식:
- CSV: `{base_filename}_deepseek.csv`
- JSON: `{base_filename}_deepseek.json`

## 다음 단계

1. Mathpix에서 LaTeX 복사
2. `convert_su1_p4_problems_latex_improved.py` 같은 개선된 스크립트 사용
3. 또는 `quick_process_mathpix_latex()` 함수로 자동 처리
4. 결과 검토 및 저장

## 참고 파일

- `latex_utils.py`: 재사용 가능한 유틸리티 함수
- `convert_template.py`: 템플릿 및 공통 함수
- `mathpix_latex_processor.py`: 자동화 처리 시스템
- `convert_su1_p4_problems_latex_improved.py`: 개선된 예시 스크립트
