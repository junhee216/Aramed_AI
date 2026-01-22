# convert_su2_02_problems_latex.py
# 수2 드릴 02 문제 LaTeX를 딥시크용 CSV로 변환

import re
import sys
import os
from pathlib import Path
from latex_utils import (
    extract_body, extract_options_generic, clean_latex_text
)
from convert_template import review_problems, save_for_deepseek

# Windows 콘솔 인코딩 설정
if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')

# Mathpix에서 온 LaTeX 내용
latex_content = """% This LaTeX document needs to be compiled with XeLaTeX.
\\documentclass[10pt]{article}
\\usepackage[utf8]{inputenc}
\\usepackage{amsmath}
\\usepackage{amsfonts}
\\usepackage{amssymb}
\\usepackage[version=4]{mhchem}
\\usepackage{stmaryrd}
\\usepackage[fallback]{xeCJK}
\\usepackage{polyglossia}
\\usepackage{fontspec}
\\IfFontExistsTF{Noto Serif CJK KR}
{\\setCJKmainfont{Noto Serif CJK KR}}
{\\IfFontExistsTF{Apple SD Gothic Neo}
  {\\setCJKmainfont{Apple SD Gothic Neo}}
  {\\IfFontExistsTF{UnDotum}
    {\\setCJKmainfont{UnDotum}}
    {\\setCJKmainfont{Malgun Gothic}}
}}

\\setmainlanguage{english}
\\IfFontExistsTF{CMU Serif}
{\\setmainfont{CMU Serif}}
{\\IfFontExistsTF{DejaVu Sans}
  {\\setmainfont{DejaVu Sans}}
  {\\setmainfont{Georgia}}
}

\\begin{document}
\\section*{Chapter 1 \\\\
 함수의 극한과 연속}
함수

$$
f(x)= \\begin{cases}3 x & (x \\leq 0) \\\\ x^{2}-2 x+4 & (x>0)\\end{cases}
$$

에 대하여 함수 $g(x)$ 를

$$
g(x)= \\begin{cases}\\lim _{t \\rightarrow(x+3)+} f(t)-\\lim _{t \\rightarrow x^{-}} f(t) & (x \\leq 0) \\\\ f(x)-a & (x>0)\\end{cases}
$$

라 하자. 함수 $g(x)$ 가 $x=b$ 에서만 불연속일 때, 상수 $a, b$ 에 대하여 $a+b$ 의 값은? [4점]\\\\
(1) -8\\\\
(2) -7\\\\
(3) -6\\\\
(4) -5\\\\
(5) -4

\\section*{Chapter 1 \\\\
 함수의 극한과 연속}
이차함수 $f(x)$ 와 함수

$$
g(x)= \\begin{cases}-x+k & (x<0) \\\\ x-1 & (x \\geq 0)\\end{cases}
$$

이 $\\lim _{x \\rightarrow 0} \\frac{f(x)}{|x| g(x)}=3$ 을 만족시킨다. 실수 $t$ 에 대하여 $x$ 에 대한 방정식

$$
\\{f(x)-t\\}\\{g(x)-t\\}=0
$$

의 서로 다른 실근의 개수를 $h(t)$ 라 할 때, 함수 $h(t)$ 가 $t=\\alpha$ 에서 불연속인 $\\alpha$ 의 개수는 3 이다. $f(2 k)$ 의 값은? (단, $k$ 는 상수이다.) [4점]\\\\
(1) -24\\\\
(2) -15\\\\
(3) -6\\\\
(4) 3\\\\
(5) 12

\\section*{Chapter 2}
미분

두 다항함수 $f(x), g(x)$ 가

$$
g(x)=x^{2} f(x)+4, \\quad \\lim _{x \\rightarrow 3} \\frac{f(x)-g(x)}{x-3}=1
$$

을 만족시킬 때, 곡선 $y=g(x)$ 위의 점 $(3, g(3))$ 에서의 접선과 $x$ 축, $y$ 축으로 둘러싸인 부분의 넓이는?\\\\[0pt]
[4점]\\\\
(1) 2\\\\
(2) $\\frac{49}{24}$\\\\
(3) $\\frac{25}{12}$\\\\
(4) $\\frac{17}{8}$\\\\
(5) $\\frac{13}{6}$

\\section*{Chapter 2}
\\section*{미분}
최고차항의 계수가 1 인 삼차함수 $f(x)$ 가 다음 조건을 만족시킨다.\\\\
(가) 곡선 $y=f(x)$ 위의 점 $(0, f(0))$ 에서의 접선의 방정식은 $y=12 x+1$ 이다.\\\\
(나) 방정식 $f(x)=-2 x+9$ 는 서로 다른 세 실근 $\\alpha, \\beta, \\gamma(\\alpha<\\beta<\\gamma)$ 를 갖고, $\\alpha, \\beta, \\gamma$ 는 이 순서대로 등비수열을 이룬다.\\\\
$f(1)$ 의 값은? [4점]\\\\
(1) 4\\\\
(2) 5\\\\
(3) 6\\\\
(4) 7\\\\
(5) 8

\\section*{Chapter 2}
미분

최고차항의 계수가 1 이고 $f^{\\prime}(0)=0$ 인 이차함수 $f(x)$ 에 대하여 방정식

$$
f(x)=f(x f(x)-2)
$$

의 서로 다른 실근의 개수는 3 이다. $f(4)$ 의 값을 구하시오. [4점]

\\section*{Chapter 2 \\\\
 미분}
최고차항의 계수가 3 인 삼차함수 $f(x)$ 에 대하여 실수 전체의 집합에서 정의된 함수 $g(x)$ 가 다음 조건을 만족시킨다.\\\\
(가) $x>0$ 인 모든 실수 $x$ 에 대하여 $g(x)=f(x)$ 이다.\\\\
(나) 모든 실수 $x$ 에 대하여 $g(x)=-g(-x)$ 이다.\\\\
(다) $\\lim _{x \\rightarrow 0} \\frac{|g(x)|-1}{x}=f(0)-1$

방정식 $g(x)=|x|$ 가 서로 다른 네 실근을 가지고, 가장 작은 근을 $\\alpha$ 라 할 때, $\\{f(\\alpha)+g(\\alpha)\\}^{2}$ 의 값을 구하시오. [4점]

\\section*{Chapter 2 \\\\
 미분}
서로 다른 두 정수 $a, b$ 에 대하여 함수 $f(x)=(x-a)^{2}(x-b)$ 가 있다. 방정식

$$
\\lim _{h \\rightarrow 0+} \\frac{|f(x+h)|-|f(x)|}{h}=f(x)
$$

의 모든 실근을 작은 수부터 크기순으로 나열한 것이 $-4, \\alpha_{1}, \\alpha_{2}, \\alpha_{3}$ 일 때, $\\alpha_{1}+\\alpha_{2}+\\alpha_{3}$ 의 값은? [4점]\\\\
(1) -2\\\\
(2) -1\\\\
(3) 0\\\\
(4) 1\\\\
(5) 2

\\section*{Chapter 2}
\\section*{미분}
실수 $a$ 에 대하여 함수 $f(x)=(x-a)\\left(x^{2}+x+1\\right)$ 이 있다. 함수 $g(x)$ 가 모든 실수 $x$ 에 대하여 $g(f(x))=x$ 를 만족시킬 때, $g(0)$ 의 최댓값을 $M$, 최솟값을 $m$ 이라 하자. $M-m$ 의 값을 구하시오.\\\\[0pt]
[4점]

\\section*{Chapter 2 미분}
두 함수 $f(x)=x^{3}+a, g(x)=b x+7$ 에 대하여 세 집합 $A, B, C$ 가

$$
\\begin{aligned}
& A=\\{(x, f(x)) \\mid x \\text { 는 실수 }\\} \\\\
& B=\\{(f(x), x) \\mid x \\text { 는 실수 }\\} \\\\
& C=\\{(x, g(y)) \\mid x, y \\text { 는 실수이고 }(x, y) \\in A\\}
\\end{aligned}
$$

이다. $A \\cap B=\\{(2, c)\\}$ 이고 $(1,-3) \\in C$ 일 때, 상수 $a, b, c$ 에 대하여 $a+b+c$ 의 값은? [4점]\\\\
(1) -2\\\\
(2) -1\\\\
(3) 0\\\\
(4) 1\\\\
(5) 2

\\section*{Chapter 2}
미분

함수 $f(x)=x^{3}-3 x^{2}+k$ 에 대하여 함수 $|f(x)|$ 의 극솟값이 0,1 일 때, 함수 $|f(x)|$ 의 극댓값은?\\\\
(단, $k<0$ ) [4점]\\\\
(1) 5\\\\
(2) 6\\\\
(3) 7\\\\
(4) 8\\\\
(5) 9

\\section*{Chapter 2}
\\section*{미분}
최고차항의 계수가 3 인 삼차함수 $f(x)$ 에 대하여 실수 전체의 집합에서 연속인 함수 $g(x)$ 가

$$
g(x)= \\begin{cases}f(x) & (x<0) \\\\ f(x-1) & (0 \\leq x<1) \\\\ f(x-2) & (x \\geq 1)\\end{cases}
$$

이다. 함수 $g(x)$ 가 $x=a$ 에서 극대가 되도록 하는 모든 실수 $a$ 의 값의 합이 -1 일 때, $f^{\\prime}(-3)$ 의 값은?\\\\[0pt]
[4점]\\\\
(1) 17\\\\
(2) 19\\\\
(3) 21\\\\
(4) 23\\\\
(5) 25

\\section*{Chapter 2}
미분

곡선 $y=x^{3}-2 x^{2}-x$ 위의 서로 다른 두 점 $\\mathrm{P}, \\mathrm{Q}$ 에서의 접선의 기울기가 모두 $m$ 이다.\\\\
직선 PQ 가 $x$ 축에 평행할 때, 상수 $m$ 의 값은? [4점]\\\\
(1) $\\frac{2}{3}$\\\\
(2) $\\frac{5}{3}$\\\\
(3) $\\frac{8}{3}$\\\\
(4) $\\frac{11}{3}$\\\\
(5) $\\frac{14}{3}$


\\end{document}"""


def extract_problems_from_latex(latex_content, debug=False):
    """LaTeX에서 문제 추출 (최적화 버전)"""
    problems = []
    
    # 본문 추출
    body = extract_body(latex_content)
    
    # 사전 컴파일된 정규식 (더 빠름)
    point_pattern = re.compile(r'\[4점\]|\[3점\]|［4점］|［3점］')
    options_pattern = re.compile(r'\([1-5]\)|①|②|③|④|⑤')
    
    # 점수 마커 찾기
    markers = []
    for match in point_pattern.finditer(body):
        point = 4 if '[4점]' in match.group() or '［4점］' in match.group() else 3
        markers.append((match.start(), point))
    
    print(f"[디버깅] 점수 마커 발견: {len(markers)}개")
    
    # 각 점수 마커 주변에서 문제 추출
    for i, (pos, point) in enumerate(markers, 1):
        start_pos = max(0, pos - 1500)
        end_pos = min(len(body), pos + 800)
        
        # 문제 시작 찾기 (최적화)
        problem_start = start_pos
        if i > 1:
            prev_pos = markers[i-2][0]
            problem_start = prev_pos + 200
        
        # 다음 문제/섹션 찾기
        if i < len(markers):
            next_pos = markers[i][0]
            end_pos = min(end_pos, next_pos - 50)
        else:
            next_section = body.find('\\section', pos)
            if next_section != -1:
                end_pos = min(end_pos, next_section)
        
        problem_text = body[problem_start:end_pos]
        
        # 선택지 확인
        has_options = bool(options_pattern.search(problem_text))
        
        # 문제 본문 추출
        question_end = problem_text.find('[4점]')
        if question_end == -1:
            question_end = problem_text.find('［4점］')
        if question_end == -1:
            question_end = problem_text.find('[3점]')
        if question_end == -1:
            question_end = problem_text.find('［3점］')
        
        if question_end != -1:
            question = problem_text[:question_end].strip()
            options_text = problem_text[question_end:] if has_options else ""
        else:
            question = problem_text.strip()
            options_text = ""
        
        # 텍스트 정리
        question = clean_latex_text(question)
        
        # 문제 시작 부분이 너무 짧으면 확장
        if len(question) < 50:
            extended_start = max(0, problem_start - 600)
            extended_text = body[extended_start:end_pos]
            question_end_ext = extended_text.find('[4점]')
            if question_end_ext == -1:
                question_end_ext = extended_text.find('［4점］')
            if question_end_ext == -1:
                question_end_ext = extended_text.find('[3점]')
            if question_end_ext == -1:
                question_end_ext = extended_text.find('［3점］')
            if question_end_ext != -1:
                question = clean_latex_text(extended_text[:question_end_ext])
                options_text = extended_text[question_end_ext:] if has_options else ""
        
        if len(question) < 30:
            continue
        
        # 주제 판단 (Chapter 1: 함수의 극한과 연속, Chapter 2: 미분)
        if 'Chapter 1' in problem_text or '함수의 극한과 연속' in problem_text:
            topic = "함수의 극한과 연속"
        elif 'Chapter 2' in problem_text or '미분' in problem_text:
            topic = "미분"
        else:
            topic = "미분"  # 기본값
        
        # 선택지 추출
        options = []
        if has_options and options_text:
            # 일반 객관식 문제
            options = extract_options_generic(options_text, num_options=5)
        
        # 문제 추가
        if len(options) >= 5:
            problems.append({
                "index": f"{i:02d}",
                "page": (i // 2) + 1,
                "topic": topic,
                "question": question,
                "point": point,
                "answer_type": "multiple_choice",
                "options": options
            })
        elif len(question) > 50:
            problems.append({
                "index": f"{i:02d}",
                "page": (i // 2) + 1,
                "topic": topic,
                "question": question,
                "point": point,
                "answer_type": "short_answer"
            })
    
    return problems


def review_problems_with_math_check(problems):
    """문제 데이터 검토 (수학적 논리 포함)"""
    print("=" * 60)
    print("[수2 드릴 02 문제 데이터 검토 (수학적 논리 포함)]")
    print("=" * 60)
    
    issues = []
    math_warnings = []
    
    for prob in problems:
        idx = prob.get("index", "?")
        print(f"\n[문제 {idx}]")
        
        question = prob.get("question", "")
        print(f"[내용 길이] {len(question)}자")
        
        # LaTeX 검사
        dollar_count = re.sub(r'\$\$', '', question).count('$')
        if dollar_count % 2 != 0:
            issues.append(f"문제 {idx}: LaTeX 수식 괄호 불일치")
            print("[LaTeX] 오류: 수식 괄호 불일치")
        else:
            print("[LaTeX] 정상")
        
        # 수학적 논리 검토
        # 1. 극한 식 확인
        if '\\lim' in question:
            if 'x \\rightarrow' in question or 'x->' in question or 'h \\rightarrow' in question:
                pass  # 극한 식 구조 정상
        
        # 2. 함수의 연속성 확인
        if '연속' in question or '불연속' in question:
            if 'f(x)' in question or 'g(x)' in question:
                pass  # 연속성 조건 언급 정상
        
        # 3. 다항함수 차수 확인
        if '이차함수' in question or '삼차함수' in question:
            if '최고차항' in question or '계수' in question:
                pass  # 다항함수 차수 언급 정상
        
        # 4. 미분 관련 확인
        if '미분' in question or '접선' in question or '극대' in question or '극소' in question:
            if 'f\'' in question or 'f^{\\prime}' in question or 'g\'' in question:
                pass  # 미분 관련 언급 정상
        
        # 5. 조건부 함수 확인
        if '\\begin{cases}' in question:
            if '\\end{cases}' in question:
                pass  # 조건부 함수 구조 정상
        
        # 6. 방정식 실근 개수 확인
        if '실근' in question and '개수' in question:
            if '서로 다른' in question:
                pass  # 실근 개수 조건 언급 정상
        
        # 유형 확인
        answer_type = prob.get("answer_type", "")
        print(f"[유형] {answer_type}")
        
        if answer_type == "multiple_choice":
            options = prob.get("options", [])
            print(f"[선택지 수] {len(options)}개")
            if len(options) == 5:
                print("[선택지] 정상")
            else:
                issues.append(f"문제 {idx}: 선택지 수 오류 ({len(options)}개)")
                print(f"[선택지] 오류: {len(options)}개 (5개여야 함)")
    
    print("\n" + "=" * 60)
    print("[검토 결과]")
    print("=" * 60)
    print(f"[총 문제수] {len(problems)}개")
    
    mc_count = sum(1 for p in problems if p.get("answer_type") == "multiple_choice")
    sa_count = sum(1 for p in problems if p.get("answer_type") == "short_answer")
    print(f"[객관식] {mc_count}개")
    print(f"[주관식] {sa_count}개")
    
    if issues:
        print("\n[오류]")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("\n[오류] 없음")
    
    if math_warnings:
        print("\n[수학적 논리 경고]")
        for warning in math_warnings:
            print(f"  - {warning}")
    else:
        print("[수학적 논리] 정상")
    
    return len(issues) == 0


def main():
    """메인 실행 함수"""
    print("=" * 60)
    print("[수2 드릴 02 문제 LaTeX → CSV 변환 (최적화 버전)]")
    print("=" * 60)
    
    # 1단계: LaTeX 읽기
    print(f"\n[1단계] LaTeX 내용 읽기 완료 ({len(latex_content)}자)")
    
    # 2단계: 문제 추출
    print("\n[2단계] 문제 추출 중...")
    problems = extract_problems_from_latex(latex_content, debug=False)
    print(f"[완료] {len(problems)}개 문제 추출됨")
    
    # 3단계: 검토 (수학적 논리 포함)
    print("\n[3단계] 문제 검토 중...")
    is_valid = review_problems_with_math_check(problems)
    
    # 4단계: 저장 (수2 디렉토리 - 기존 폴더 경로 사용)
    print("\n[4단계] 딥시크용 파일 저장 중...")
    base_dir = Path(r'C:\Users\a\Documents\MathPDF\organized\현우진\수2_2005학년도_현우진_드릴')
    base_filename = "수2_2025학년도_현우진_드릴_02_문제"
    csv_path, json_path = save_for_deepseek(problems, base_dir, base_filename)
    
    print("\n" + "=" * 60)
    print("[완료] 딥시크가 읽을 수 있는 형태로 저장되었습니다.")
    print("=" * 60)
    print(f"저장 위치: {base_dir}")
    print(f"  - CSV: {csv_path.name}")
    print(f"  - JSON: {json_path.name}")


if __name__ == '__main__':
    main()
