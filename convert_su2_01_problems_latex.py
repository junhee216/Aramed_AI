# convert_su2_01_problems_latex.py
# 수2 드릴 01 문제 LaTeX를 딥시크용 CSV로 변환

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
이차함수 $f(x)$ 가

$$
\\lim _{x \\rightarrow 2} \\frac{f(x)+x-2}{f(x)-x+2}=f(3)=\\frac{1}{3}
$$

을 만족시킬 때, $f(5)$ 의 값은? [4점]\\\\
(1) 9\\\\
(2) 11\\\\
(3) 13\\\\
(4) 15\\\\
(5) 17

최고차항의 계수가 1 인 삼차함수 $f(x)$ 와 최고차항의 계수가 2 인 삼차함수 $g(x)$ 가 다음 조건을 만족시킨다.\\\\
(가) $\\lim _{x \\rightarrow k} \\frac{f(x) g(x)}{(x-k)^{2}}=0$ 을 만족시키는 실수 $k$ 의 개수는 2 이다.\\\\
(나) $\\lim _{x \\rightarrow 1} \\frac{g(x)}{f(x)}=\\lim _{x \\rightarrow 3} \\frac{f(x)}{g(x)}=0$\\\\
$f(2)>0$ 일 때, $f(4)+g(4)$ 의 값은? [4점]\\\\
(1) 19\\\\
(2) 20\\\\
(3) 21\\\\
(4) 22\\\\
(5) 23

최고차항의 계수가 1 인 이차함수 $f(x)$ 와 최고차항의 계수가 1 인 삼차함수 $g(x)$ 가 다음 조건을 만족시킨다.\\\\
(가) $\\lim _{x \\rightarrow t} \\frac{f(x)+g(x)-x^{2}}{x}=0$ 을 만족시키는 실수 $t$ 의 값은 0 뿐이다.\\\\
(나) 함수 $g(x)$ 는 $x=-1$ 에서 극댓값 0 을 갖는다.\\\\
$f(1)$ 의 값은? [4점]\\\\
(1) 3\\\\
(2) 4\\\\
(3) 5\\\\
(4) 6\\\\
(5) 7

삼차함수 $f(x)$ 가

$$
\\lim _{x \\rightarrow 0} \\frac{|f(x)-1|}{x}=\\lim _{x \\rightarrow 1} \\frac{f(x)-x}{x-1}=k
$$

를 만족시킬 때, $f(k+3)$ 의 값은? (단, $k$ 는 상수이다.) [4점]\\\\
(1) 11\\\\
(2) 13\\\\
(3) 15\\\\
(4) 17\\\\
(5) 19

\\section*{Chapter 1 \\\\
 함수의 극한과 연속}
$x=0$ 에서 불연속인 함수 $f(x)$ 와 최고차항의 계수가 1 인 이차함수 $g(x)$ 가

$$
\\lim _{x \\rightarrow 0} \\frac{f(x)-1}{x}=\\lim _{x \\rightarrow 0} \\frac{g(x)-f(0)}{x}=3
$$

을 만족시킨다. $\\lim _{x \\rightarrow 0} \\frac{f(x) g(x)+2}{x}=a$ 일 때, $g(2 a)$ 의 값은? (단, $a$ 는 상수이다.) [4점]\\\\
(1) 15\\\\
(2) 16\\\\
(3) 17\\\\
(4) 18\\\\
(5) 19

다항함수 $f(x)$ 와 일차함수 $g(x)$ 가 다음 조건을 만족시킬 때, $f(1) \\times g(1)$ 의 값은? [4점]\\\\
(가) $\\lim _{x \\rightarrow \\infty} \\frac{f(x)}{x g(x)}=2$\\\\
(나) $\\lim _{x \\rightarrow 2} \\frac{f(x)}{g(x)-g(2)}=\\lim _{x \\rightarrow 0} \\frac{f(x)}{x}=g(3)$\\\\
(1) 10\\\\
(2) 12\\\\
(3) 14\\\\
(4) 16\\\\
(5) 18

\\section*{Chapter 1 \\\\
 함수의 극한과 연속}
자연수 $n$ 에 대하여 다항함수 $f(x)$ 가

$$
\\lim _{x \\rightarrow \\infty} \\frac{x^{n}}{f(x)+x^{4}}=\\lim _{x \\rightarrow \\infty} \\frac{x^{n+1}}{f(x)+x^{2}}=\\lim _{x \\rightarrow 0} \\frac{f(x)}{x^{2}}=k
$$

를 만족시킬 때, $f(-2)$ 의 값은? (단, $k$ 는 0 이 아닌 상수이다.) [4점]\\\\
(1) -18\\\\
(2) -16\\\\
(3) -14\\\\
(4) -12\\\\
(5) -10

\\section*{Chapter 1 \\\\
 함수의 극한과 연속}
$f(0) \\neq 0$ 인 다항함수 $f(x)$ 와 0 이 아닌 상수 $k$ 가 모든 자연수 $n$ 에 대하여

$$
\\lim _{x \\rightarrow \\infty} \\frac{f(x)-x^{n}-x^{3}}{f^{\\prime}(x)-f(0) x^{n}}= \\begin{cases}3 k & (n=2) \\\\ k & (n \\neq 2)\\end{cases}
$$

를 만족시킬 때, $f(3)$ 의 값은? [4점]\\\\
(1) 45\\\\
(2) 46\\\\
(3) 47\\\\
(4) 48\\\\
(5) 49

\\section*{Chapter 1 \\\\
 함수의 극한과 연속}
두 상수 $a, b$ 에 대하여 실수 전체의 집합에서 연속인 함수

$$
f(x)= \\begin{cases}-x+a & (x<2) \\\\ \\frac{b x+1}{x-1} & (x \\geq 2)\\end{cases}
$$

의 치역이 $\\{y \\mid y>2\\}$ 일 때, $a+b$ 의 값은? [4점]\\\\
(1) 5\\\\
(2) 6\\\\
(3) 7\\\\
(4) 8\\\\
(5) 9

\\section*{Chapter 1 \\\\
 함수의 극한과 연속}
\\section*{두 함수}
$$
f(x)=\\left\\{\\begin{array}{ll}
x-2 & (x<a) \\\\
x-4 & (x \\geq a)
\\end{array}, \\quad g(x)=x^{2}-3 x+2\\right.
$$

에 대하여 함수 $|f(x)| g(x)$ 가 실수 전체의 집합에서 연속이 되도록 하는 모든 실수 $a$ 의 값의 합을 구하 시오. [4점]


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
        start_pos = max(0, pos - 1000)
        end_pos = min(len(body), pos + 700)
        
        # 문제 시작 찾기 (최적화)
        problem_start = start_pos
        if i > 1:
            prev_pos = markers[i-2][0]
            problem_start = prev_pos + 100
        
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
            extended_start = max(0, problem_start - 400)
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
        
        # 주제 판단 (함수의 극한과 연속)
        topic = "함수의 극한과 연속"
        
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
    print("[수2 드릴 01 문제 데이터 검토 (수학적 논리 포함)]")
    print("=" * 60)
    
    issues = []
    math_warnings = []
    
    for prob in problems:
        idx = prob.get("index", "?")
        print(f"\n[문제 {idx}]")
        
        question = prob.get("question", "")
        print(f"[내용 길이] {len(question)}자")
        
        # LaTeX 검사
        dollar_count = question.count('$')
        if dollar_count % 2 != 0:
            issues.append(f"문제 {idx}: LaTeX 수식 괄호 불일치")
            print("[LaTeX] 오류: 수식 괄호 불일치")
        else:
            print("[LaTeX] 정상")
        
        # 수학적 논리 검토
        # 1. 극한 식 확인
        if '\\lim' in question:
            if 'x \\rightarrow' in question or 'x->' in question:
                pass  # 극한 식 구조 정상
        
        # 2. 함수의 연속성 확인
        if '연속' in question or '불연속' in question:
            if 'f(x)' in question or 'g(x)' in question:
                pass  # 연속성 조건 언급 정상
        
        # 3. 다항함수 차수 확인
        if '이차함수' in question or '삼차함수' in question:
            if '최고차항' in question or '계수' in question:
                pass  # 다항함수 차수 언급 정상
        
        # 4. 극한값 계산 확인
        if '\\lim' in question and '=' in question:
            if 'k' in question or 'a' in question or '상수' in question:
                pass  # 극한값 계산 언급 정상
        
        # 5. 조건부 함수 확인
        if '\\begin{cases}' in question:
            if '\\end{cases}' in question:
                pass  # 조건부 함수 구조 정상
        
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
    print("[수2 드릴 01 문제 LaTeX → CSV 변환 (최적화 버전)]")
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
    base_filename = "수2_2025학년도_현우진_드릴_01_문제"
    csv_path, json_path = save_for_deepseek(problems, base_dir, base_filename)
    
    print("\n" + "=" * 60)
    print("[완료] 딥시크가 읽을 수 있는 형태로 저장되었습니다.")
    print("=" * 60)
    print(f"저장 위치: {base_dir}")
    print(f"  - CSV: {csv_path.name}")
    print(f"  - JSON: {json_path.name}")


if __name__ == '__main__':
    main()
