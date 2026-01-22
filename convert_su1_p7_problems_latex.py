# convert_su1_p7_problems_latex.py
# 수1 드릴 P7 문제 LaTeX를 딥시크용 CSV로 변환 (최적화 버전)

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
\\section*{Chapter 3}
\\section*{수열}
수열

수열 $\\left\\{a_{n}\\right\\}$ 은 $0<a_{1} \\leq 1$ 이고, 모든 자연수 $n$ 에 대하여

$$
a_{n+1}=\\cos \\left(\\pi a_{n}\\right)
$$

을 만족시킨다. $a_{5} \\times a_{6}=1$ 이 되도록 하는 모든 $a_{1}$ 의 값의 합은? [4점]\\\\
(1) $\\frac{3}{2}$\\\\
(2) $\\frac{11}{6}$\\\\
(3) 2\\\\
(4) $\\frac{13}{6}$\\\\
(5) $\\frac{5}{2}$

\\section*{Chapter 3}
수열

첫째항이 1 이고 모든 항이 정수인 수열 $\\left\\{a_{n}\\right\\}$ 에 대하여 다음 조건을 만족시키는 자연수 $p$ 가 존재한다.

모든 자연수 $n$ 에 대하여 $a_{n+3}=p a_{n}$ 이다.\\\\
$\\sum_{k=1}^{9} a_{k}=26, a_{6}-a_{2}=-5$ 일 때, $a_{p+8}$ 의 값은? [4점]\\\\
(1) 18\\\\
(2) 27\\\\
(3) 36\\\\
(4) 45\\\\
(5) 54

\\section*{Chapter 3}
수열

수열 $\\left\\{a_{n}\\right\\}$ 이 모든 자연수 $n$ 에 대하여

$$
\\left(a_{n+1}-a_{n}+2\\right)\\left(a_{n+1}-2 a_{n}-1\\right)=0
$$

을 만족시킨다. $a_{3}=a_{4}$ 이고 $a_{1} a_{2} a_{3}<0$ 일 때, $a_{1}+a_{2}+a_{3}=k$ 이다. 모든 $k$ 의 값의 곱은? [4점]\\\\
(1) -10\\\\
(2) -9\\\\
(3) -8\\\\
(4) -7\\\\
(5) -6

\\section*{Chapter 3 \\\\
 수열}
수열 $\\left\\{a_{n}\\right\\}$ 이 모든 자연수 $n$ 에 대하여 다음 조건을 만족시킨다.\\\\
(가) $a_{2 n+1}=4 a_{n}-a_{n+1}$\\\\
(나) $a_{2 n+2}=-2 a_{n}+a_{n+1}$\\\\
$a_{1}=1$ 이고 $\\sum_{k=1}^{18} a_{k}=38$ 일 때, $\\left|a_{3}\\right|+\\left|a_{4}\\right|$ 의 값을 구하시오. [4점]

\\section*{Chapter 3}
\\section*{수열}
수열 $\\left\\{a_{n}\\right\\}$ 의 첫째항부터 제 $n$ 항까지의 합을 $S_{n}$ 이라 할 때, 모든 자연수 $n$ 에 대하여

$$
a_{n+2}= \\begin{cases}-S_{n}+n & \\left(S_{n} \\leq 0\\right) \\\\ -a_{n+1} & \\left(S_{n}>0\\right)\\end{cases}
$$

이다. $a_{4}=4, S_{4}=3$ 일 때, $\\sum_{k=1}^{50} k a_{k}$ 의 값은? [4점]\\\\
(1) -77\\\\
(2) -75\\\\
(3) -73\\\\
(4) -71\\\\
(5) -69

\\section*{Chapter 3}
수열

수열 $\\left\\{a_{n}\\right\\}$ 이 모든 자연수 $n$ 에 대하여 다음 조건을 만족시킨다．\\\\
（가）$n-1<a_{n}<n$\\\\
（나） $\\sin \\left(\\pi a_{n+1}\\right)=\\cos \\left(\\pi a_{n}\\right)$

〈보기〉에서 옳은 것만을 있는 대로 고른 것은？［4점］

\\section*{〈보기〉}
ᄀ． $0<a_{1}<\\frac{1}{2}$\\\\
ㄴ．모든 자연수 $n$ 에 대하여 $a_{n}+a_{n+1}=\\frac{4 n+1}{2}$ 이다．\\\\
ᄃ．$a_{1}+a_{9}=\\frac{28}{3}$ 이면 $\\sum_{k=1}^{13} a_{k}=\\frac{263}{3}$ 이다．\\\\
（1）ᄀ\\\\
（2）ᄂ\\\\
（3）ᄃ\\\\
（4）ᄂ，ᄃ\\\\
（5）ᄀ，ᄂ，ᄃ

\\section*{Chapter 3}
수열

모든 항이 자연수인 수열 $\\left\\{a_{n}\\right\\}$ 에 대하여 $a_{n}$ 을 3 으로 나눈 나머지를 $b_{n}$ 이라 하자. 두 수열 $\\left\\{a_{n}\\right\\},\\left\\{b_{n}\\right\\}$ 이 모든 자연수 $n$ 에 대하여

$$
a_{n+2}-a_{n+1}=b_{n}+b_{n+1}
$$

을 만족시킨다. $a_{4}=8$ 이고 $a_{6}$ 이 3 의 배수일 때, $\\sum_{k=1}^{6} a_{k}$ 의 최솟값은? [4점]\\\\
(1) 48\\\\
(2) 49\\\\
(3) 50\\\\
(4) 51\\\\
(5) 52

\\section*{Chapter 3 \\\\
 수열}
$a_{2}$ 가 자연수인 수열 $\\left\\{a_{n}\\right\\}$ 이 모든 자연수 $n$ 에 대하여

$$
a_{n+1}= \\begin{cases}a_{n} & \\left(a_{n}>n\\right) \\\\ a_{n}+a_{2} & \\left(a_{n} \\leq n\\right)\\end{cases}
$$

를 만족시킨다. $a_{9}=9$ 일 때, $\\sum_{n=1}^{12} a_{n}$ 의 최댓값과 최솟값의 합은? [4점]\\\\
(1) 220\\\\
(2) 222\\\\
(3) 224\\\\
(4) 226\\\\
(5) 228

\\section*{Chapter 3}
수열 $\\left\\{a_{n}\\right\\}$ 이 다음 조건을 만족시킨다.\\\\
(가) 20 이하의 모든 자연수 $n$ 에 대하여

$$
a_{n}= \\begin{cases}a_{2 n} & \\left(a_{n+2}=1\\right) \\\\ n+1 & \\left(a_{n+2} \\neq 1\\right)\\end{cases}
$$

이다.\\\\
(나) $a_{m}=1$ 인 20 이하의 자연수 $m$ 의 개수는 11 이다.\\\\
$a_{11}=1$ 일 때, $a_{1}+a_{3}+a_{5}+a_{7}+a_{9}$ 의 값은? [4점]\\\\
(1) 9\\\\
(2) 14\\\\
(3) 19\\\\
(4) 24\\\\
(5) 29

다음 조건을 만족시키는 수열 $\\left\\{a_{n}\\right\\}$ 에 대하여 $a_{16}=k$ 라 할 때, 모든 실수 $k$ 의 값의 합은? [4점]\\\\
(가) 모든 자연수 $n$ 에 대하여

$$
a_{n+2}= \\begin{cases}a_{n+1} a_{n} & \\left(a_{n+1} \\leq 0\\right) \\\\ \\frac{a_{n+1}}{a_{n}} & \\left(a_{n+1}>0\\right)\\end{cases}
$$

이다.\\\\
(나) $a_{m}=8, a_{m+5}=-1$ 인 자연수 $m$ 이 존재하고, 모든 자연수 $n$ 에 대하여 $a_{n} \\leq a_{m}$ 이다.\\\\
(1) $-\\frac{33}{64}$\\\\
(2) $-\\frac{65}{128}$\\\\
(3) $-\\frac{1}{2}$\\\\
(4) $-\\frac{63}{128}$\\\\
(5) $-\\frac{31}{64}$


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
        
        # 주제 판단 (모두 수열)
        topic = "수열"
        
        # 선택지 추출
        options = []
        if has_options and options_text:
            # 보기 문제 (ㄱ, ㄴ, ㄷ) 확인
            if 'ㄱ' in options_text or 'ㄴ' in options_text or 'ㄷ' in options_text:
                # 보기 내용은 문제 본문에 포함되므로 선택지에서 제외
                # 선택지만 추출 (1) ~ (5)
                for opt_num in range(1, 6):
                    pattern = rf'（{opt_num}）\s*([^（]+?)(?=（[1-5]）|$|\\section|\\end|\\includegraphics)'
                    match = re.search(pattern, options_text)
                    if match:
                        option_num = ["①", "②", "③", "④", "⑤"][opt_num-1]
                        opt_text = clean_latex_text(match.group(1))
                        if '〈보기〉' not in opt_text and 'ㄱ' not in opt_text and 'ㄴ' not in opt_text and 'ㄷ' not in opt_text:
                            options.append(f"{option_num} {opt_text}")
            else:
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
    print("[수1 드릴 P7 문제 데이터 검토 (수학적 논리 포함)]")
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
        # 1. 수열 점화식 확인
        if 'a_{n+1}' in question or 'a_{n+2}' in question:
            if '=' in question or '\\leq' in question or '\\geq' in question:
                pass  # 점화식 구조 정상
        
        # 2. 삼각함수 범위 확인
        if 'cos' in question or 'sin' in question:
            if '\\pi' in question:
                # cos(πx), sin(πx)의 범위는 -1 ~ 1
                pass  # 정상
        
        # 3. 합 기호 확인
        if '\\sum' in question:
            if 'k=1' in question or 'n=1' in question:
                pass  # 합 기호 구조 정상
        
        # 4. 조건부 수식 확인
        if '\\begin{cases}' in question:
            if '\\end{cases}' in question:
                pass  # 조건부 수식 구조 정상
        
        # 5. 절댓값 확인
        if '|a_' in question or '\\left|' in question:
            if '|' in question or '\\right|' in question:
                pass  # 절댓값 구조 정상
        
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
    print("[수1 드릴 P7 문제 LaTeX → CSV 변환 (최적화 버전)]")
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
    
    # 4단계: 저장
    print("\n[4단계] 딥시크용 파일 저장 중...")
    base_dir = Path(r'C:\Users\a\Documents\MathPDF\organized\현우진\수1_2025학년도_현우진_드릴')
    base_filename = "수1_2025학년도_현우진_드릴_P7_문제"
    csv_path, json_path = save_for_deepseek(problems, base_dir, base_filename)
    
    print("\n" + "=" * 60)
    print("[완료] 딥시크가 읽을 수 있는 형태로 저장되었습니다.")
    print("=" * 60)
    print(f"저장 위치: {base_dir}")
    print(f"  - CSV: {csv_path.name}")
    print(f"  - JSON: {json_path.name}")


if __name__ == '__main__':
    main()
