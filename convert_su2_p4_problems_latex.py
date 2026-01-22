# convert_su2_p4_problems_latex.py
# 수2 드릴 P4 문제 LaTeX를 딥시크용 CSV로 변환

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
\\section*{Chapter 2 \\
 미분}
최고차항의 계수가 양수인 삼차함수 $f(x)$ 와 공차가 $d(d>0)$ 인 등차수열 $\\left\\{a_{n}\\right\\}$ 이 있다. 두 집합 $A, B$ 가

$$
\\begin{aligned}
& A=\\left\\{f^{\\prime}(n) \\mid 1 \\leq n \\leq 5, n \\text { 은 자연수 }\\right\\}, \\\\
& B=\\left\\{\\left.\\frac{f(n)}{d} \\right\\rvert\\, 1 \\leq n \\leq 5, n \\text { 은 자연수 }\\right\\}
\\end{aligned}
$$

이고, 자연수 $m$ 에 대하여

$$
A-B=\\left\\{a_{12}\\right\\}, \\quad A \\cap B=\\left\\{0, a_{6}\\right\\}, \\quad B-A=\\left\\{a_{m}\\right\\}
$$

이다. $f(m)$ 의 값을 구하시오. [4점]

\\section*{Chapter 2}
미분

함수 $f(x)=2 x^{3}-k x^{2}+9(k>0)$ 와 상수 $a, b$ 에 대하여 함수 $g(x)$ 를

$$
g(x)= \\begin{cases}f(x) & (x<b) \\\\ 2 a-f(x) & (x \\geq b)\\end{cases}
$$

라 하자. 함수 $g(x)$ 가 실수 전체의 집합에서 미분가능하고 극댓값이 10 일 때, $k+a+b$ 의 값은? [4점]\\\\
(1) 10\\\\
(2) 11\\\\
(3) 12\\\\
(4) 13\\\\
(5) 14

\\section*{Chapter 2 미분}
최고차항의 계수가 음수인 삼차함수 $f(x)$ 에 대하여 실수 전체의 집합에서 연속인 함수 $g(x)$ 가 모든 실수 $x$ 에 대하여

$$
\\{g(x)-f(x)\\}\\{g(x)-x-f(0)\\}=0
$$

이고，다음 조건을 만족시킨다．\\\\
（가） $\\lim _{h \\rightarrow 0+} \\frac{g(\\alpha+h)-g(\\alpha)}{h}=0$ 을 만족시키는 $\\alpha$ 는 존재하지 않는다．\\\\
（나）함수 $g(x)$ 가 $x=\\beta$ 에서 미분가능하지 않으면 $\\lim _{h \\rightarrow 0} \\frac{g(\\beta+h)-g(\\beta-h)}{h}=0$ 이다．

함수 $g(x)$ 가 극솟값 $f(0)-2$ 를 가질 때，〈보기〉에서 옳은 것만을 있는 대로 고른 것은？［4점］

\\section*{〈보기〉}
ㄱ．$f^{\\prime}(-2)=-1$\\\\
ᄂ．함수 $g(x)$ 가 $x=k(k>0)$ 에서 극댓값 $3 f(0)$ 을 가지면 $k+f^{\\prime}(k)=f(0)$ 이다．\\\\
ᄃ．모든 실수 $x$ 에 대하여 $\\{g(x)\\}^{2} \\geq f(x) g(x)$ 이면 $f(1) \\geq \\frac{3}{2}$ 이다．\\\\
（1）ᄀ\\\\
（2）ᄀ，ᄂ\\\\
（3）ᄀ，ᄃ\\\\
（4）ᄂ，ᄃ\\\\
（5）ᄀ，ᄂ，ᄃ

\\section*{Chapter 2}
\\section*{미분}
삼차함수 $f(x)=-x^{2}(x-a)(a>0)$ 와 실수 $t$ 에 대하여 곡선 $y=f(x)$ 위의 점 $(t, f(t))$ 에서 $x$ 축까지의 거리와 $y$ 축까지의 거리 중 크지 않은 값을 $g(t)$ 라 하자. 함수 $g(t)$ 가 세 점에서만 미분가능하지 않도록 하는 $a$ 의 최댓값은? [4점]\\\\
(1) 1\\\\
(2) $\\sqrt{2}$\\\\
(3) $\\sqrt{3}$\\\\
(4) 2\\\\
(5) $\\sqrt{5}$

\\section*{Chapter 2 미분}
최고차항의 계수가 양수인 삼차함수 $f(x)$ 에 대하여 함수 $g(x)$ 를

$$
g(x)= \\begin{cases}|f(x)| & (x<1) \\\\ f(x)-3 x+5 & (x \\geq 1)\\end{cases}
$$

라 하자. 함수 $g(x)$ 가 실수 전체의 집합에서 미분가능하고, $g(0)=0$ 일 때, $g(2)$ 의 값은? [4점]\\\\
(1) 7\\\\
(2) 8\\\\
(3) 9\\\\
(4) 10\\\\
(5) 11

\\section*{Chapter 2}
\\section*{미분}
최고차항의 계수가 1 인 삼차함수 $f(x)$ 에 대하여

$$
g(x)= \\begin{cases}|f(x)-2| & (x<0) \\\\ |f(x)+6| & (x \\geq 0)\\end{cases}
$$

이라 하자. 함수 $g(x)$ 가 실수 전체의 집합에서 미분가능할 때, $f(4)$ 의 최댓값 $M$, 최솟값 $m$ 에 대하여 $M+m$ 의 값은? [4점]\\\\
(1) 120\\\\
(2) 122\\\\
(3) 124\\\\
(4) 126\\\\
(5) 128

\\section*{Chapter 2 미분}
최고차항의 계수가 -1 인 삼차함수 $f(x)$ 에 대하여 함수

$$
g(x)= \\begin{cases}|f(x)|-4 & (x<0) \\\\ f(x)+4 & (x \\geq 0)\\end{cases}
$$

가 다음 조건을 만족시킨다.\\\\
(가) 함수 $g(x)$ 는 $x=0$ 에서 미분가능하다.\\\\
(나) 함수 $g(x)$ 는 $x=\\alpha$ 에서 극소이고 $x=\\beta$ 에서 극대이다.\\\\
$g(\\alpha)+g(\\beta)=0, \\alpha \\beta<0$ 일 때, $f(\\alpha-1)$ 의 값을 구하시오. [4점]

\\section*{Chapter 2}
미분

최고차항의 계수가 1 인 이차함수 $f(x)$ 에 대하여 함수

$$
g(x)=3 x^{3}-\\left|\\int_{a}^{x} f(t) d t\\right|
$$

가 다음 조건을 만족시키도록 하는 정수 $a$ 의 개수는? [4점]\\\\
(가) 함수 $g(x)$ 는 실수 전체의 집합에서 미분가능하다.\\\\
(나) $x>-2$ 에서 함수 $g(x)$ 가 극값을 갖는 $x$ 의 개수는 2 이다.\\\\
(1) 6\\\\
(2) 7\\\\
(3) 8\\\\
(4) 9\\\\
(5) 10

\\section*{Chapter 2}
미분

최고차항의 계수가 1 인 삼차함수 $f(x)$ 와 함수

$$
g(x)= \\begin{cases}-x-2 & (x<-1) \\\\ |x| & (x \\geq-1)\\end{cases}
$$

가 있다. 함수 $h(x)=g(x)|f(x)|$ 가 실수 전체의 집합에서 미분가능할 때, $f(2)$ 의 최댓값은? [4점]\\\\
(1) 12\\\\
(2) 18\\\\
(3) 24\\\\
(4) 30\\\\
(5) 36

\\section*{Chapter 2 미분}
최고차항의 계수가 3 인 삼차함수 $f(x)$ 에 대하여 실수 전체의 집합에서 연속인 함수

$$
g(x)= \\begin{cases}f(x) & (x<1) \\\\ \\int_{a}^{x}\\left|f^{\\prime}(t)\\right| d t & (x \\geq 1)\\end{cases}
$$

가 있다. 실수 $k$ 에 대하여 함수 $|g(x)-k|$ 가 미분가능하지 않은 점의 개수를 $h(k)$ 라 할 때, 함수 $h(k)$ 는 $k=b$ 에서 최솟값 1 을 갖는다. $g(a)=b$ 이고

$$
h(48) \\neq \\lim _{k \\rightarrow 48+} h(k)=4
$$

일 때, $g(-4 a)$ 의 값을 구하시오. (단, $a, b$ 는 상수이다.) [4점]


\\end{document}"""


def extract_problems_from_latex(latex_content, debug=False):
    """LaTeX에서 문제 추출 (최적화 버전)"""
    problems = []
    
    # 본문 추출
    body = extract_body(latex_content)
    
    # 사전 컴파일된 정규식
    point_pattern = re.compile(r'\[4점\]|\[3점\]|［4점］|［3점］')
    options_pattern = re.compile(r'\([1-5]\)|（[1-5]）|①|②|③|④|⑤')
    
    # 점수 마커 찾기
    markers = []
    for match in point_pattern.finditer(body):
        point = 4 if '[4점]' in match.group() or '［4점］' in match.group() else 3
        markers.append((match.start(), point))
    
    if debug:
        print(f"[디버깅] 점수 마커 발견: {len(markers)}개")
    
    # 섹션 헤더 위치 찾기
    section_pattern = re.compile(r'\\section\*?\{[^}]*\}')
    sections = []
    for match in section_pattern.finditer(body):
        sections.append(match.start())
    
    # 각 점수 마커 주변에서 문제 추출
    for i, (pos, point) in enumerate(markers, 1):
        # 문제 시작: 이전 마커 이후 또는 문서 시작
        if i > 1:
            prev_pos = markers[i-2][0]
            # 이전 마커의 끝 찾기
            prev_marker_end = prev_pos
            prev_match = point_pattern.search(body[prev_pos:prev_pos+50])
            if prev_match:
                prev_marker_end = prev_pos + prev_match.end()
            problem_start = prev_marker_end + 50
        else:
            problem_start = 0
        
        # 현재 마커 이전의 마지막 섹션 찾기
        for sec_pos in reversed(sections):
            if sec_pos < pos and sec_pos >= problem_start:
                # 섹션 헤더 끝 찾기
                section_end = body.find('}', sec_pos)
                if section_end != -1:
                    problem_start = section_end + 1
                break
        
        # 문제 끝: 다음 마커 이전 또는 문서 끝
        if i < len(markers):
            next_pos = markers[i][0]
            problem_end = next_pos - 50
        else:
            problem_end = len(body)
        
        problem_text_raw = body[problem_start:problem_end].strip()
        
        # 점수 마커를 기준으로 문제와 선택지 분리
        point_match_in_text = point_pattern.search(problem_text_raw)
        if not point_match_in_text:
            continue
        
        question_part = problem_text_raw[:point_match_in_text.start()].strip()
        options_part = problem_text_raw[point_match_in_text.start():].strip()
        
        # 텍스트 정리
        question = clean_latex_text(question_part)
        
        # 섹션 헤더 제거 (문제 본문에 포함되지 않도록)
        question = re.sub(r'\\section\*?\{[^}]*\}', '', question)
        question = re.sub(r'Chapter 2[^가-힣]*미분', '', question)
        question = question.strip()
        
        # 문제 시작 부분이 잘린 경우 복구 시도
        # "}+9(k>0)$" 같은 패턴이 시작 부분에 있으면 이전 부분 찾기
        if question.startswith('}+') or question.startswith('}$') or question.startswith('ction*'):
            # 이전 텍스트에서 문제 시작 찾기
            search_back = body[max(0, problem_start - 200):problem_start]
            # 함수 정의 패턴 찾기
            func_patterns = [
                r'함수 \$f\(x\)=[^$]+',
                r'삼차함수 \$f\(x\)=[^$]+',
                r'다항함수 \$f\(x\)',
                r'이차함수 \$f\(x\)',
            ]
            for pattern in func_patterns:
                match = re.search(pattern, search_back)
                if match:
                    # 찾은 부분부터 현재까지
                    full_question = search_back[match.start():] + question_part
                    question = clean_latex_text(full_question)
                    question = re.sub(r'\\section\*?\{[^}]*\}', '', question)
                    question = question.strip()
                    break
        
        # 주제 판단
        topic = "미분"  # 기본값
        
        # 선택지 추출
        options = []
        has_options = bool(options_pattern.search(options_part))
        
        if has_options:
            # '〈보기〉'가 포함된 문제 처리
            if '〈보기〉' in options_part or '보기' in question or '\\section\\*\\{〈보기〉' in options_part:
                # 보기 내용 추출 (섹션 헤더 포함)
                boogi_patterns = [
                    r'\\section\*\{〈보기〉\}(.*?)(?=（[1-5]）|$|\\section)',
                    r'〈보기〉(.*?)(?=（[1-5]）|$|\\section)',
                ]
                boogi_content = ""
                for pattern in boogi_patterns:
                    boogi_match = re.search(pattern, options_part, re.DOTALL)
                    if boogi_match:
                        boogi_content = clean_latex_text(boogi_match.group(1))
                        question += f" 〈보기〉 {boogi_content}"
                        break
                
                # 선택지 (1)~(5) 추출 (전각 괄호 우선)
                for opt_num in range(1, 6):
                    # 전각 괄호: （1）~（5）
                    pattern1 = rf'（{opt_num}）\s*([^（]+?)(?=（[1-5]）|$|\\section|\\end)'
                    # 반각 괄호: (1)~(5)
                    pattern2 = rf'\({opt_num}\)\s*([^(]+?)(?=\([1-5]\)|$|\\section|\\end)'
                    
                    match = re.search(pattern1, options_part) or re.search(pattern2, options_part)
                    if match:
                        option_text = clean_latex_text(match.group(1))
                        # 보기 내용이 선택지에 포함되지 않도록 확인
                        if '〈보기〉' not in option_text and 'ㄱ' not in option_text and 'ㄴ' not in option_text and 'ㄷ' not in option_text:
                            options.append(f"{['①', '②', '③', '④', '⑤'][opt_num-1]} {option_text}")
            else:
                # 일반 객관식 문제
                options = extract_options_generic(options_part, num_options=5)
        
        # 문제 추가
        if len(question) > 30:  # 최소 길이 필터링
            problem_entry = {
                "index": f"{i:02d}",
                "page": (i // 2) + 1,
                "topic": topic,
                "question": question,
                "point": point,
                "answer_type": "multiple_choice" if has_options else "short_answer"
            }
            if has_options:
                problem_entry["options"] = options
            problems.append(problem_entry)
    
    return problems


def main():
    print("=" * 60)
    print("[수2 드릴 P4 문제 LaTeX → CSV 변환]")
    print("=" * 60)
    
    # 1단계: LaTeX 읽기
    print(f"\n[1단계] LaTeX 내용 읽기 완료 ({len(latex_content)}자)")
    
    # 2단계: 문제 추출
    print("\n[2단계] 문제 추출 중...")
    problems = extract_problems_from_latex(latex_content, debug=True)
    print(f"[완료] {len(problems)}개 문제 추출됨")
    
    # 3단계: 검토 (수학적 논리 포함)
    print("\n[3단계] 문제 검토 중...")
    is_valid = review_problems(problems)
    
    # 4단계: 저장
    print("\n[4단계] 딥시크용 파일 저장 중...")
    base_dir = Path(r'C:\Users\a\Documents\MathPDF\organized\현우진\수2_2005학년도_현우진_드릴')
    base_filename = "수2_2025학년도_현우진_드릴_P4_문제"
    csv_path, json_path = save_for_deepseek(problems, base_dir, base_filename)
    
    print("\n" + "=" * 60)
    print("[완료] 딥시크가 읽을 수 있는 형태로 저장되었습니다.")
    print("=" * 60)
    print(f"저장 위치: {base_dir}")
    print(f"  - CSV: {csv_path.name}")
    print(f"  - JSON: {json_path.name}")


if __name__ == '__main__':
    main()
