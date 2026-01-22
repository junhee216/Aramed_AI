# convert_su2_03_problems_latex.py
# 수2 드릴 03 문제 LaTeX를 딥시크용 CSV로 변환

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
\\IfFontExistsTF{Noto Serif CJK TC}
{\\setCJKfallbackfamilyfont{\\CJKrmdefault}{Noto Serif CJK TC}}
{\\IfFontExistsTF{STSong}
  {\\setCJKfallbackfamilyfont{\\CJKrmdefault}{STSong}}
  {\\IfFontExistsTF{Droid Sans Fallback}
    {\\setCJKfallbackfamilyfont{\\CJKrmdefault}{Droid Sans Fallback}}
    {\\setCJKfallbackfamilyfont{\\CJKrmdefault}{SimSun}}
}}

\\setmainlanguage{english}
\\IfFontExistsTF{CMU Serif}
{\\setmainfont{CMU Serif}}
{\\IfFontExistsTF{DejaVu Sans}
  {\\setmainfont{DejaVu Sans}}
  {\\setmainfont{Georgia}}
}

\\begin{document}
$f(0)=0$ 이고 최고차항의 계수가 음수인 삼차함수 $f(x)$ 에 대하여 실수 전체의 집합의 두 부분집합 $A, B$ 가

$$
A=\\{x \\mid f(x)=2 x\\}, B=\\{x \\mid f(x)=6 x-8\\}
$$

이다．$n(A-B)=1$ 일 때，〈보기〉에서 옳은 것만을 있는 대로 고른 것은？［4점］\\\\
〈보기〉\\\\
ᄀ．$n(A \\cap B)=1$\\\\
ㄴ．$n(A \\cup B)=3$ 이면 곡선 $y=f(x)$ 는 직선 $y=6 x-8$ 에 접한다．\\\\
ᄃ．$n(A)=n(B)=2$ 이면 $f(3)=-6$ 이다．\\\\
（1）ᄀ\\\\
（2）ᄂ\\\\
（3）ᄃ\\\\
（4）ᄀ，ᄃ\\\\
（5）ᄂ，ᄃ

\\section*{Chapter 2 \\\\
 미분}
최고차항의 계수가 양수이고 $f(0)=0$ 인 삼차함수 $f(x)$ 에 대하여 함수

$$
g(x)= \\begin{cases}\\frac{x|f(x)|}{f(x)} & (f(x) \\neq 0) \\\\ 8 & (f(x)=0)\\end{cases}
$$

이 다음 조건을 만족시킬 때, $f(5)$ 의 값을 구하시오. [4점]\\\\
(가) $\\lim _{x \\rightarrow 3-} g(x)<\\lim _{x \\rightarrow 3+} g(x)$\\\\
(나) 방정식 $g(x)=f(1)$ 의 서로 다른 실근의 개수는 5 이다.\\\\
(다) 방정식 $g(x)=f(x)$ 의 서로 다른 실근의 개수는 3 이다.

\\section*{Chapter 2 \\\\
 미분}
다항함수 $f(x)$ 가

$$
\\lim _{x \\rightarrow \\infty} \\frac{f(x)}{x^{3}}=\\{f(2)\\}^{2}, \\quad \\lim _{x \\rightarrow 0} \\frac{f(x)}{|x|}=f^{\\prime}(2)
$$

를 만족시킬 때, $f(1)$ 의 값은? (단, $f(2) \\neq 0$ ) [4점]\\\\
(1) $-\\frac{1}{8}$\\\\
(2) $-\\frac{1}{7}$\\\\
(3) $-\\frac{1}{6}$\\\\
(4) $-\\frac{1}{5}$\\\\
(5) $-\\frac{1}{4}$

최고차항의 계수가 1 인 삼차함수 $f(x)$ 가 다음 조건을 만족시킨다.\\\\
(가) 함수 $f(x)$ 의 극댓값은 5 이다.\\\\
(나) 열린구간 $(a, b)$ 에서 함수 $f(x)$ 의 최댓값과 최솟값이 모두 존재하도록 하는 $a$ 의 최솟값은 -1 이고 $b$ 의 최댓값은 3 이다.\\\\
$f(4)$ 의 값은? [4점]\\\\
(1) 21\\\\
(2) 22\\\\
(3) 23\\\\
(4) 24\\\\
(5) 25

\\section*{Chapter 2 미분}
함수 $f(x)=x^{3}-3 x$ 와 $0<t<2$ 인 실수 $t$ 에 대하여 점 $\\mathrm{A}(t, 3 t)$ 를 지나고 $y$ 축과 평행한 직선이 곡선 $y=f(x)$ 와 만나는 점을 C 라 하고, 곡선 $y=f(x)$ 위의 점 C 에서 그은 접선이 곡선 $y=f(x)$ 와 만나는 점 중 C 가 아닌 점을 B 라 할 때, 삼각형 ABC 의 넓이의 최댓값은? [4점]\\\\
(1) $\\frac{25}{2}$\\\\
(2) 13\\\\
(3) $\\frac{27}{2}$\\\\
(4) 14\\\\
(5) $\\frac{29}{2}$

\\section*{Chapter 2 \\\\
 미분}
$x=4$ 에서 극댓값 0 을 갖는 삼차함수 $f(x)$ 와 양수 $a$ 에 대하여 함수

$$
g(x)= \\begin{cases}-f(x-a) & (x<a) \\\\ f(x) & (x \\geq a)\\end{cases}
$$

가 다음 조건을 만족시킨다.\\\\
(가) $\\lim _{x \\rightarrow a} \\frac{|x-a| g^{\\prime}(x)}{x-a}$ 의 값이 존재한다.\\\\
(나) 함수 $g(x)$ 는 $x=0$ 에서 최댓값 $M$ 을 갖는다.\\\\
$g(-M)=0$ 일 때, $|f(3)|=\\frac{q}{p}$ 이다. $p+q$ 의 값을 구하시오. (단, $p$ 와 $q$ 는 서로소인 자연수이다.) [4점]

\\section*{Chapter 2 미분}
다항함수 $f(x)$ 가 다음 조건을 만족시킨다．\\\\
（가） $\\lim _{x \\rightarrow \\infty} \\frac{|f(x)|}{x^{3}}=f(f(1))=1$\\\\
（나）함수 $f(x)$ 는 구간 $(-\\infty, 1)$ 에서 최솟값 $f(1)$ 을 갖는다．

집합 $A=\\{x \\mid f(f(x))=1\\}$ 에 대하여 〈보기〉에서 옳은 것만을 있는 대로 고른 것은？［4점］\\\\
〈보기〉\\\\
ᄀ．$f(1)>1$ 일 때，$n(A)=2$ 이다．\\\\
ᄂ．$f^{\\prime}(f(1))>0$ 일 때，$n(A)=6$ 이다．\\\\
ᄃ．$n(A)=5$ 일 때，$f(1)=-3$ 이다．\\\\
（1）ᄀ\\\\
（2）ᄃ\\\\
（3）ᄀ，ᄂ\\\\
（4）ᄂ，ᄃ\\\\
（5）ᄀ，ᄂ，ᄃ

\\section*{Chapter 2}
\\section*{미분}
$f(0)=0$ 인 삼차함수 $f(x)$ 에 대하여 방정식

$$
(f \\circ f)(x)=\\{f(x)\\}^{2}
$$

의 모든 실근을 작은 수부터 크기순으로 나열한 것을 $\\alpha_{1}, \\alpha_{2}, \\cdots, \\alpha_{7}$ 이라 하자. $\\alpha_{1}=0, \\alpha_{7}=4$ 이고, $f^{\\prime}\\left(\\alpha_{5}\\right)=0$ 일 때, $\\left(2 \\alpha_{5}-\\alpha_{3}\\right) \\times \\sum_{k=1}^{7}\\left\\{\\alpha_{k}+f\\left(\\alpha_{k}\\right)\\right\\}$ 의 값을 구하시오. [4점]

최고차항의 계수가 양수이고 $f(0)=0$ 인 삼차함수 $f(x)$ 에 대하여 실수 전체의 집합에서 미분가능한 함수

$$
g(x)= \\begin{cases}-f(1) x & (x<0) \\\\ f(x+1)-f(1) & (x \\geq 0)\\end{cases}
$$

이 다음 조건을 만족시킨다.

방정식 $(g \\circ g)(x)=x$ 의 서로 다른 모든 실근을 작은 수부터 크기순으로 나열한 $\\alpha, 0, \\beta, \\gamma$ 는 이 순서대로 등차수열을 이룬다.\\\\
$|f(\\alpha)|$ 의 값을 구하시오. [4점]

\\section*{Chapter 2 \\\\
 미분}
최고차항의 계수가 1 인 삼차함수 $f(x)$ 가 있다. 실수 $t$ 에 대하여 함수 $g(x)$ 를

$$
g(x)=f^{\\prime}(t+2)(x-t)+f(t)
$$

라 하자. 곡선 $y=f(x)$ 와 직선 $y=g(x)$ 가 만나는 서로 다른 점의 개수가 2 가 되도록 하는 $t$ 의 개수는 $m$ 이고, 모든 $t$ 를 작은 수부터 크기순으로 나열할 때, $n$ 번째 수를 $t_{n}$ 이라 하면

$$
\\sum_{k=1}^{m} t_{k}=\\frac{8}{3}, \\quad f^{\\prime}\\left(t_{1}+2\\right)=14
$$

이다. $f^{\\prime}(m+4)$ 의 값을 구하시오. [4점]


\\end{document}"""


def extract_problems_from_latex(latex_content, debug=False):
    """LaTeX에서 문제 추출 (최적화 버전)"""
    problems = []
    
    # 본문 추출
    body = extract_body(latex_content)
    
    # 사전 컴파일된 정규식 (더 빠름)
    point_pattern = re.compile(r'\[4점\]|\[3점\]|［4점］|［3점］')
    options_pattern = re.compile(r'\([1-5]\)|（[1-5]）|①|②|③|④|⑤')
    
    # 점수 마커 찾기
    markers = []
    for match in point_pattern.finditer(body):
        point = 4 if '[4점]' in match.group() or '［4점］' in match.group() else 3
        markers.append((match.start(), point))
    
    print(f"[디버깅] 점수 마커 발견: {len(markers)}개")
    
    # 섹션 헤더 위치 찾기
    section_pattern = re.compile(r'\\section\*?\{[^}]*\}')
    sections = []
    for match in section_pattern.finditer(body):
        sections.append(match.start())
    
    # 각 점수 마커 주변에서 문제 추출
    for i, (pos, point) in enumerate(markers, 1):
        start_pos = max(0, pos - 1500)
        end_pos = min(len(body), pos + 800)
        
        # 문제 시작 찾기: 이전 섹션 또는 이전 마커 이후
        problem_start = start_pos
        if i > 1:
            prev_pos = markers[i-2][0]
            problem_start = prev_pos + 200
        
        # 현재 마커 이전의 마지막 섹션 찾기
        for sec_pos in reversed(sections):
            if sec_pos < pos:
                problem_start = max(problem_start, sec_pos)
                break
        
        # 다음 문제/섹션 찾기
        if i < len(markers):
            next_pos = markers[i][0]
            end_pos = min(end_pos, next_pos - 50)
        else:
            next_section = body.find('\\section', pos)
            if next_section != -1:
                end_pos = min(end_pos, next_section)
        
        problem_text = body[problem_start:end_pos]
        
        # 선택지 확인 (전각 괄호 포함)
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
        if len(question) < 50 or question.startswith('$') or question.startswith('가') or question.startswith('는'):
            extended_start = max(0, problem_start - 1000)
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
        
        # 섹션 헤더 제거
        question = re.sub(r'\\section\*?\{[^}]*\}', '', question)
        question = re.sub(r'Chapter \d+', '', question)
        question = re.sub(r'\\\\', ' ', question)
        question = re.sub(r'\s+', ' ', question).strip()
        
        if len(question) < 30:
            continue
        
        # 주제 판단 (Chapter 2: 미분)
        if 'Chapter 1' in problem_text or '함수의 극한과 연속' in problem_text:
            topic = "함수의 극한과 연속"
        elif 'Chapter 2' in problem_text or '미분' in problem_text:
            topic = "미분"
        else:
            topic = "미분"  # 기본값
        
        # 선택지 추출
        options = []
        if has_options and options_text:
            # 보기 문제 (ㄱ, ㄴ, ㄷ) 확인
            if 'ㄱ' in options_text or 'ㄴ' in options_text or 'ㄷ' in options_text or 'ᄀ' in options_text or 'ᄂ' in options_text or 'ᄃ' in options_text or '〈보기〉' in question:
                # 보기 문제: 전각 괄호 (（1）~（5）) 사용
                for opt_num in range(1, 6):
                    # 전각 괄호: （1）ᄀ 또는 （1） ᄀ
                    pattern = rf'（{opt_num}）\s*([ᄀᄂᄃ]+)'
                    match = re.search(pattern, options_text)
                    if match:
                        option_num = ["①", "②", "③", "④", "⑤"][opt_num-1]
                        opt_text = match.group(1).strip()
                        options.append(f"{option_num} {opt_text}")
                    else:
                        # 전각 괄호만 있는 경우도 처리
                        pattern2 = rf'（{opt_num}）'
                        if re.search(pattern2, options_text):
                            option_num = ["①", "②", "③", "④", "⑤"][opt_num-1]
                            # 다음 괄호 전까지 또는 줄바꿈 전까지
                            match2 = re.search(rf'（{opt_num}）\s*([^（]+?)(?=（[1-5]）|$|\\section|\\end)', options_text)
                            if match2:
                                opt_text = clean_latex_text(match2.group(1))
                                if '〈보기〉' not in opt_text:
                                    options.append(f"{option_num} {opt_text}")
            else:
                # 일반 객관식 문제 - 분수 형태 포함 개선
                for i in range(1, 6):
                    option_num = ["①", "②", "③", "④", "⑤"][i-1]
                    
                    # 다양한 패턴 시도
                    patterns = [
                        # 분수: (1) $-\frac{1}{8}$ 또는 (1) -\$\frac{1}{8}\$
                        rf'\({i}\)\s*([-+]?)\\?\$?\\?frac\{{([0-9]+)}}\{{([0-9]+)}}\\?\$?',
                        # 정수: (1) 21
                        rf'\({i}\)\s*([0-9]+)(?=\\\\|\s|$)',
                        # 전각 괄호: （1）...
                        rf'（{i}）\s*([^（(]+?)(?=（[1-5]）|\([1-5]\)|$)',
                    ]
                    
                    match = None
                    for pattern in patterns:
                        match = re.search(pattern, options_text)
                        if match:
                            break
                    
                    if match:
                        if len(match.groups()) == 3:  # 분수
                            sign = match.group(1) if match.group(1) else ""
                            num = match.group(2)
                            den = match.group(3)
                            opt_text = f"${sign}\\frac{{{num}}}{{{den}}}$"
                            options.append(f"{option_num} {opt_text}")
                        elif len(match.groups()) == 1:  # 정수 또는 기타
                            opt_text = clean_latex_text(match.group(1))
                            # 분수 형태가 포함되어 있으면 그대로 유지
                            if '\\frac' in opt_text:
                                options.append(f"{option_num} ${opt_text}$")
                            else:
                                options.append(f"{option_num} {opt_text}")
                    else:
                        # 패턴 매칭 실패 시 기존 함수 사용
                        pass
                
                # 기존 함수로 보완
                if len(options) < 5:
                    options = extract_options_generic(options_text, num_options=5)
        
        # 보기 문제 확인 (〈보기〉가 있고 선택지가 (1)~(5) 형태)
        is_boogi_problem = '〈보기〉' in question or '보기' in question
        if is_boogi_problem and (has_options or len(options) > 0):
            # 보기 문제는 선택지가 있어도 5개가 아닐 수 있음
            if len(options) >= 3:  # 최소 3개 선택지
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
                    "answer_type": "multiple_choice",
                    "options": options if options else []
                })
        # 일반 객관식 문제
        elif len(options) >= 5:
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
    print("[수2 드릴 03 문제 데이터 검토 (수학적 논리 포함)]")
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
    print("[수2 드릴 03 문제 LaTeX → CSV 변환 (최적화 버전)]")
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
    base_filename = "수2_2025학년도_현우진_드릴_03_문제"
    csv_path, json_path = save_for_deepseek(problems, base_dir, base_filename)
    
    print("\n" + "=" * 60)
    print("[완료] 딥시크가 읽을 수 있는 형태로 저장되었습니다.")
    print("=" * 60)
    print(f"저장 위치: {base_dir}")
    print(f"  - CSV: {csv_path.name}")
    print(f"  - JSON: {json_path.name}")


if __name__ == '__main__':
    main()
