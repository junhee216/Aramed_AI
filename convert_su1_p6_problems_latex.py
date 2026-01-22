# convert_su1_p6_problems_latex.py
# 수1 드릴 P6 문제 LaTeX를 딥시크용 CSV로 변환

import re
import sys
import os
from pathlib import Path
from latex_utils import (
    extract_body, extract_options_generic, clean_latex_text,
    diagnose_latex_structure
)
from convert_template import review_problems, save_for_deepseek
# 최적화 버전 사용 가능 (선택사항)
# from mathpix_latex_processor_optimized import quick_process_mathpix_latex_optimized

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
\\section*{Chapter 3}
수열

실수 전체의 집합의 부분집합 $A$ 가

$$
A=\\left\\{x \\mid x \\text { 는 }(a k+5)^{k} \\text { 의 } k \\text { 제곱근, } k=2,3,4,5\\right\\}
$$

이다. 집합 $A$ 가 다음 조건을 만족시키도록 하는 모든 실수 $a$ 의 값의 합은? [4점]\\\\
(가) $n(A)=5$\\\\
(나) 집합 $A$ 의 모든 원소를 작은 수부터 크기순으로 나열하면 이 순서대로 등차수열을 이룬다.\\\\
(1) $-\\frac{13}{4}$\\\\
(2) -3\\\\
(3) $-\\frac{11}{4}$\\\\
(4) $-\\frac{5}{2}$\\\\
(5) $-\\frac{9}{4}$

1 보다 큰 자연수 $m$ 에 대하여 공차가 $-m$ 인 등차수열 $\\left\\{a_{n}\\right\\}$ 과 모든 항이 자연수이고 공비가 $m$ 인 등비수열 $\\left\\{b_{n}\\right\\}$ 이 다음 조건을 만족시킨다.\\\\
(가) $a_{6} \\times a_{7}<0, b_{1}>1$\\\\
(나) $\\sum_{n=1}^{b_{2}} a_{n}=\\sum_{n=1}^{b_{3}} a_{n}$\\\\
$\\sum_{n=1}^{2 m}\\left(a_{n}+b_{n}\\right)$ 의 값을 구하시오. [4점]

\\section*{Chapter 3 \\\\
 수열}
공차가 양수인 등차수열 $\\left\\{a_{n}\\right\\}$ 에 대하여 $\\left|a_{n}-a_{10}\\right|$ 과 $\\frac{a_{n}}{2}$ 중 작지 않은 값을 $b_{n}$ 이라 하자.\\\\
$b_{n}$ 이 다음 조건을 만족시킬 때, $\\sum_{n=1}^{20} b_{n}$ 의 값은? [4점]\\\\
(가) $b_{6}=b_{12}$\\\\
(나) $b_{n}$ 의 최솟값은 10 이다.\\\\
(1) 530\\\\
(2) 540\\\\
(3) 550\\\\
(4) 560\\\\
(5) 570

\\section*{Chapter 3}
수열

첫째항이 자연수인 등차수열 $\\left\\{a_{n}\\right\\}$ 에 대하여 $2 a_{1}-3 a_{2}=0$ 이고,

$$
\\sum_{k=1}^{m} a_{k} \\geq a_{3}+2
$$

를 만족시키는 모든 자연수 $m$ 의 값의 합이 14 일 때, $a_{10}$ 의 값은? [4점]\\\\
(1) -5\\\\
(2) -4\\\\
(3) -3\\\\
(4) -2\\\\
(5) -1

\\section*{Chapter 3}
수열\\\\
$x$ 에 대한 이차방정식

$$
x^{2}-2 k x+k^{2}+2 k=0
$$

이 서로 다른 두 실근 $\\alpha, \\beta$ 를 갖는다. 세 수 $\\alpha, 4 \\sqrt{3}, \\beta$ 가 이 순서대로 등비수열을 이룰 때, $\\alpha+\\beta$ 의 값은?\\\\
(단, $k$ 는 상수이다.) [4점]\\\\
(1) -16\\\\
(2) -9\\\\
(3) -2\\\\
(4) 5\\\\
(5) 12

\\section*{Chapter 3 수열}
등비수열 $\\left\\{a_{n}\\right\\}$ 의 첫째항부터 제 $n$ 항까지의 합을 $S_{n}$ 이라 하자. 모든 자연수 $n$ 에 대하여

$$
a_{n+1} \\times S_{n}=9^{n}-3^{n}
$$

일 때, $\\left(a_{3}\\right)^{2}$ 의 값은? [4점]\\\\
(1) 138\\\\
(2) 144\\\\
(3) 150\\\\
(4) 156\\\\
(5) 162

\\section*{Chapter 3}
수열

첫째항이 자연수이고 공비가 $-\\frac{1}{2}$ 인 등비수열 $\\left\\{a_{n}\\right\\}$ 에 대하여

$$
a_{1} a_{p} \\leq a_{2}
$$

를 만족시키는 자연수 $p$ 의 개수가 3 일 때, $a_{1}$ 의 최댓값을 $M$, 최솟값을 $m$ 이라 하자.\\\\
$M-m$ 의 값을 구하시오. [4점]

\\section*{Chapter 3}
수열

수열 $\\left\\{a_{n}\\right\\}$ 이 다음 조건을 만족시킨다.\\\\
(가) 두 수열 $\\left\\{a_{2 n}\\right\\},\\left\\{a_{3 n}\\right\\}$ 은 각각 공비가 $r, r+4$ 인 등비수열이다.\\\\
(나) $a_{2}=1, \\sum_{k=1}^{7} a_{k}=-100$\\\\
$\\sum_{k=1}^{10} a_{k}$ 의 값을 구하시오. (단, $r \\neq 0$ ) [4점]

\\section*{Chapter 3}
수열

수열 $\\left\\{a_{n}\\right\\}$ 의 첫째항부터 제 $n$ 항까지의 합을 $S_{n}$ 이라 하자. 모든 자연수 $n$ 에 대하여

$$
S_{n}=\\sqrt{n^{2}+n}
$$

일 때, $\\sum_{k=1}^{8} \\frac{a_{k}}{\\sqrt{k}}$ 의 값은? [3점]\\\\
(1) $\\sqrt{2}+1$\\\\
(2) $\\sqrt{2}+2$\\\\
(3) $2 \\sqrt{2}$\\\\
(4) $2 \\sqrt{2}+1$\\\\
(5) $2 \\sqrt{2}+2$

\\section*{Chapter 3}
\\section*{수열}
$a_{2}=-\\frac{3}{2}$ 인 수열 $\\left\\{a_{n}\\right\\}$ 의 첫째항부터 제 $n$ 항까지의 합을 $S_{n}$ 이라 하자. 모든 자연수 $n$ 에 대하여

$$
S_{n} S_{n+1}=1, \\quad a_{n} a_{n+1}<0
$$

일 때, $\\sum_{k=1}^{8}(-2)^{k-1} a_{k}$ 의 값을 구하시오. [4점]

\\section*{Chapter 3 \\\\
 수열}
수열 $\\left\\{a_{n}\\right\\}$ 이 $a_{1}=10$ 이고, 모든 자연수 $n$ 에 대하여

$$
a_{n+2}+a_{n+1}=\\sum_{k=1}^{n} a_{k}
$$

를 만족시킨다. $\\sum_{k=1}^{5} a_{3 k}=175$ 일 때, $a_{2}$ 의 값을 구하시오. [4점]


\\end{document}"""


def extract_problems_from_latex(latex_content, debug=False):
    """LaTeX에서 문제 추출"""
    problems = []
    
    # 본문 추출
    body = extract_body(latex_content)
    
    if debug:
        print("[LaTeX 구조 진단]")
        diagnose_latex_structure(body, max_chars=300)
    
    # 점수 마커로 문제 구분 ([4점] 또는 [3점])
    point_markers = list(re.finditer(r'\[4점\]|\[3점\]|［4점］|［3점］', body))
    print(f"[디버깅] 점수 마커 발견: {len(point_markers)}개")
    
    # 각 점수 마커 주변에서 문제 추출
    for i, marker in enumerate(point_markers, 1):
        start_pos = max(0, marker.start() - 1500)
        end_pos = min(len(body), marker.end() + 800)
        
        # 문제 시작 찾기
        problem_start = start_pos
        for j in range(marker.start(), max(0, marker.start() - 1500), -1):
            if j > 0:
                # 이전 문제의 끝 또는 섹션 시작 찾기
                if j > 100:
                    prev_marker = body.rfind('[4점]', max(0, j-800), j)
                    if prev_marker == -1:
                        prev_marker = body.rfind('［4점］', max(0, j-800), j)
                    if prev_marker == -1:
                        prev_marker = body.rfind('[3점]', max(0, j-800), j)
                    if prev_marker == -1:
                        prev_marker = body.rfind('［3점］', max(0, j-800), j)
                    if prev_marker != -1:
                        problem_start = prev_marker + 200
                        break
                # 섹션 시작 찾기
                if body[j:j+10].find('\\section') != -1:
                    problem_start = j
                    break
        
        # 문제 끝 찾기
        problem_end = marker.end() + 500
        next_section = body.find('\\section', marker.end())
        if next_section != -1:
            problem_end = min(problem_end, next_section)
        next_problem = body.find('[4점]', marker.end() + 50)
        if next_problem == -1:
            next_problem = body.find('［4점］', marker.end() + 50)
        if next_problem == -1:
            next_problem = body.find('[3점]', marker.end() + 50)
        if next_problem == -1:
            next_problem = body.find('［3점］', marker.end() + 50)
        if next_problem != -1:
            problem_end = min(problem_end, next_problem - 50)
        
        problem_text = body[problem_start:problem_end]
        
        # 점수 추출
        point_match = re.search(r'\[([34])점\]|［([34])점］', problem_text)
        point = int(point_match.group(1) or point_match.group(2)) if point_match else 4
        
        # 선택지 확인
        has_options = bool(re.search(r'\([1-5]\)|①|②|③|④|⑤', problem_text))
        
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
            extended_start = max(0, problem_start - 500)
            extended_text = body[extended_start:problem_end]
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


def main():
    """메인 실행 함수"""
    print("=" * 60)
    print("[수1 드릴 P6 문제 LaTeX → CSV 변환]")
    print("=" * 60)
    
    # 1단계: LaTeX 읽기
    print(f"\n[1단계] LaTeX 내용 읽기 완료 ({len(latex_content)}자)")
    
    # 2단계: 문제 추출
    print("\n[2단계] 문제 추출 중...")
    problems = extract_problems_from_latex(latex_content, debug=False)
    print(f"[완료] {len(problems)}개 문제 추출됨")
    
    # 3단계: 검토
    print("\n[3단계] 문제 검토 중...")
    is_valid = review_problems(problems)
    
    # 4단계: 저장
    print("\n[4단계] 딥시크용 파일 저장 중...")
    base_dir = Path(r'C:\Users\a\Documents\MathPDF\organized\현우진\수1_2025학년도_현우진_드릴')
    base_filename = "수1_2025학년도_현우진_드릴_P6_문제"
    csv_path, json_path = save_for_deepseek(problems, base_dir, base_filename)
    
    print("\n" + "=" * 60)
    print("[완료] 딥시크가 읽을 수 있는 형태로 저장되었습니다.")
    print("=" * 60)
    print(f"저장 위치: {base_dir}")
    print(f"  - CSV: {csv_path.name}")
    print(f"  - JSON: {json_path.name}")


if __name__ == '__main__':
    main()
