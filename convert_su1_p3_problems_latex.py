# convert_su1_p3_problems_latex.py
# 수1 드릴 P3 문제 LaTeX를 딥시크용 CSV로 변환

import re
import csv
import sys
import os
from pathlib import Path
from datetime import datetime
import json

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
\\usepackage{graphicx}
\\usepackage[export]{adjustbox}
\\graphicspath{ {./images/} }
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
$a>0,0<b<\\frac{1}{2}$ 인 상수 $a, b$ 에 대하여 닫힌구간 $[0,1]$ 에서 정의된 함수

$$
y=a \\sin (\\pi x+b \\pi)
$$

의 최댓값이 4 , 최솟값이 -2 일 때, $\\frac{a}{b}$ 의 값은? [4점]\\\\
(1) 20\\\\
(2) 24\\\\
(3) 28\\\\
(4) 32\\\\
(5) 36

\\section*{Chapter 2}
\\section*{삼각함수}
$0 \\leq x \\leq 5$ 일 때, $\\frac{1}{2}(a \\sin \\pi x+5)$ 의 값이 정수가 되도록 하는 모든 실수 $x$ 의 값의 합을 $S(a)$ 라 하자.\\
$25 \\leq S(a) \\leq 75$ 를 만족시키는 정수 $a$ 의 개수를 구하시오. [4점]

닫힌구간 $[0,2 \\pi]$ 에서 정의된 두 함수

$$
f(x)=\\cos x, \\quad g(x)=a \\sin x(a>0)
$$

에 대하여 두 곡선 $y=f(x), y=g(x)$ 의 교점 중 $y$ 좌표가 양수인 점 A 를 지나는 직선 $y=k$ 가 있다. 직선 $y=k$ 가 두 곡선 $y=f(x), y=g(x)$ 와 만나는 점 중 A 가 아닌 점을 각각 $\\mathrm{B}, \\mathrm{C}$ 라 하자. $\\overline{\\mathrm{AC}}: \\overline{\\mathrm{BC}}=2: 3$ 일 때, $a+k$ 의 값은? (단, $k$ 는 상수이다.) [4점]\\\\
(1) $\\sqrt{3}$\\\\
(2) $\\frac{3 \\sqrt{3}}{2}$\\\\
(3) $2 \\sqrt{3}$\\\\
(4) $\\frac{5 \\sqrt{3}}{2}$\\\\
(5) $3 \\sqrt{3}$

\\section*{Chapter 2 삼각함수}
그림과 같이 곡선 $y=\\sin \\frac{\\pi x}{2}(0 \\leq x \\leq 5)$ 와 직선 $y=k(0<k<1)$ 가 만나는 세 점 $\\mathrm{A}, \\mathrm{B}, \\mathrm{C}$ 의 $x$ 좌표를 각각 $a, b, c$ 라 할 때, $a<b<c$ 이다. 두 삼각형 $\\mathrm{OBA}, \\mathrm{OCB}$ 의 넓이를 각각 $S_{1}, S_{2}$ 라 할 때, $S_{1}: S_{2}=1: 5$ 이다. $S_{1} \\times S_{2}$ 의 값은? (단, O 는 원점이다.) [4점]\\\\
\\includegraphics[max width=\\textwidth, center]{436b503b-64e4-4f3d-8d2f-8a11b9d7fe99-04_348_714_934_824}\\\\
(1) $\\frac{1}{12}$\\\\
(2) $\\frac{1}{6}$\\\\
(3) $\\frac{1}{4}$\\\\
(4) $\\frac{1}{3}$\\\\
(5) $\\frac{5}{12}$

양수 $a$ 에 대하여 집합 $\\left\\{x \\left\\lvert\\, 0<x<\\frac{3}{2 a}\\right., x \\neq \\frac{1}{2 a}\\right\\}$ 에서 정의된 함수 $f(x)=\\tan (a \\pi x)$ 가 있다. 곡선 $y=f(x)$ 가 $x$ 축과 만나는 점을 A 라 하고, 점 A 를 지나고 기울기가 음수인 직선이 곡선 $y=f(x)$ 와 만나는 점 중 A 가 아닌 점을 $\\mathrm{P}, y$ 축과 만나는 점을 Q 라 하자. $\\overline{\\mathrm{AP}}: \\overline{\\mathrm{PQ}}=3: 1$ 이고 두 삼각형 $\\mathrm{OAP}, \\mathrm{OPQ}$ 의 넓이의 차가 $\\frac{1}{6}$ 일 때, $a$ 의 값은? (단, O 는 원점이다.) [4점]\\\\
(1) $\\frac{7}{4}$\\\\
(2) 2\\\\
(3) $\\frac{9}{4}$\\\\
(4) $\\frac{5}{2}$\\\\
(5) $\\frac{11}{4}$\\\\
\\includegraphics[max width=\\textwidth, center]{436b503b-64e4-4f3d-8d2f-8a11b9d7fe99-05_536_435_1169_968}\\\\
$a>1, b>0$ 인 상수 $a, b$ 에 대하여 집합 $\\{x \\mid-b \\leq x \\leq b\\}$ 에서 정의된 함수

$$
f(x)=a \\sin \\frac{\\pi x}{b}
$$

가 있다. 곡선 $y=f(x)$ 가 직선 $y=1$ 과 만나는 두 점을 각각 $\\mathrm{A}, \\mathrm{B}$ 라 하고, 직선 OB 가 곡선 $y=f(x)$ 와 제 3 사분면에서 만나는 점을 C 라 하자. 직선 AC 의 기울기가 직선 BC 의 기울기의 $\\frac{3}{2}$ 배이고, $\\overline{\\mathrm{AC}}=2 \\sqrt{3}$ 일 때, $a b$ 의 값은? (단, O 는 원점이고, 점 A 의 $x$ 좌표는 점 B 의 $x$ 좌표보다 작다.) [4점]\\\\
(1) $2 \\sqrt{2}$\\\\
(2) 4\\\\
(3) $2 \\sqrt{6}$\\\\
(4) $4 \\sqrt{2}$\\\\
(5) $2 \\sqrt{10}$\\\\
\\includegraphics[max width=\\textwidth, center]{436b503b-64e4-4f3d-8d2f-8a11b9d7fe99-06_407_724_1203_820}

함수 $f(x)=\\cos \\pi x$ 에 대하여 곡선 $y=f(x)$ 와 직선 $y=k(0<k<1)$ 가 만나는 점 중 $x$ 좌표가 양수인 모든 점의 $x$ 좌표를 작은 수부터 크기순으로 나열할 때, $n$ 번째 수를 $a_{n}$ 이라 하자. 함수 $g(x)$ 가

$$
g(x)=\\sin \\frac{\\pi\\left(x-a_{1}\\right)}{a_{2}-a_{1}}+k
$$

일 때, $f\\left(a_{5}\\right)=g\\left(a_{5}\\right)$ 이다. $g\\left(a_{4}\\right)$ 의 값은? [4점]\\\\
(1) $\\frac{3}{4}$\\\\
(2) 1\\\\
(3) $\\frac{5}{4}$\\\\
(4) $\\frac{3}{2}$\\\\
(5) $\\frac{7}{4}$

1 보다 큰 실수 $a$ 와 양수 $b$ 에 대하여 함수

$$
f(x)=a \\sin (b x)-1
$$

이 있다. 구간 $(0, \\infty)$ 에서 방정식 $|f(x)|=2$ 의 모든 실근을 작은 수부터 크기순으로 나열할 때, $k$ 번째 수를 $\\alpha_{k}$ 라 하자. 수열 $\\left\\{\\alpha_{2 n}+\\alpha_{2 n+3}\\right\\}$ 이 공차가 $6 \\alpha_{1}$ 인 등차수열일 때, $a^{2}$ 의 값은? [4점]\\\\
(1) 8\\\\
(2) 9\\\\
(3) 10\\\\
(4) 11\\\\
(5) 12\\\\
$0<\\theta<2 \\pi$ 일 때, 함수 $f(x)=-x^{2}-(\\sin \\theta+\\cos \\theta) x$ 에 대하여 집합 $\\{x \\mid f(f(x))=x\\}$ 의 원소의 개수가 1 이 되도록 하는 모든 $\\theta$ 의 값의 합은 $\\frac{q}{p} \\pi$ 이다. $p+q$ 의 값을 구하시오.\\
(단, $p$ 와 $q$ 는 서로소인 자연수이다.) [4점]

실수 $k$ 에 대하여 집합 $A$ 를

$$
A=\\left\\{x \\left\\lvert\\, \\cos ^{2} \\frac{\\pi x}{4}-\\frac{1}{2} \\sin \\frac{\\pi x}{4}=k\\right., 0 \\leq x \\leq 8\\right\\}
$$

이라 하자. $A \\neq \\varnothing$ 일 때, 집합 $A$ 의 모든 원소의 합을 $f(k)$ 라 하면, $f(k)=24$ 를 만족시키는 모든 $k$ 의 값의 범위는 $a \\leq k<b, f(k)=10$ 을 만족시키는 $k$ 의 값은 $c$ 이다. $80 \\times(a+b+c)$ 의 값을 구하시오. [4점]


\\end{document}"""

def extract_problems_from_latex(latex_content):
    """LaTeX에서 문제 추출"""
    problems = []
    
    # 본문만 추출
    begin_match = re.search(r'\\begin\{document\}', latex_content)
    end_match = re.search(r'\\end\{document\}', latex_content)
    if begin_match and end_match:
        body = latex_content[begin_match.end():end_match.start()]
    else:
        body = latex_content
    
    # 점수 마커로 문제 구분 (더 안정적인 방법)
    point_markers = list(re.finditer(r'\[4점\]', body))
    print(f"[디버깅] [4점] 마커 발견: {len(point_markers)}개")
    
    # 문제 2번 특별 처리: "정수 a의 개수" 또는 "구하시오" + "Chapter 2" 섹션 전
    problem_02_pattern = r'(\$0.*?정수.*?개수.*?구하시오\. \[4점\])'
    p2_match = re.search(problem_02_pattern, body, re.DOTALL)
    if p2_match:
        question_02 = p2_match.group(1).strip()
        question_02 = re.sub(r'\\\\', ' ', question_02)
        question_02 = re.sub(r'\$\$', ' ', question_02)
        question_02 = re.sub(r'\s+', ' ', question_02)
        if len(question_02) > 50:
            problems.append({
                "index": "02",
                "page": 2,
                "topic": "삼각함수",
                "question": question_02,
                "point": 4,
                "answer_type": "short_answer"
            })
            print("[디버깅] 문제 2번 특별 추출 완료")
    
    # 각 점수 마커 주변에서 문제 추출
    for i, marker in enumerate(point_markers, 1):
        start_pos = max(0, marker.start() - 800)  # 앞으로 800자
        end_pos = min(len(body), marker.end() + 500)  # 뒤로 500자
        context = body[start_pos:end_pos]
        
        # 문제 시작 찾기 (역방향으로 문장 시작 찾기)
        problem_start = start_pos
        for j in range(marker.start(), max(0, marker.start() - 800), -1):
            if j > 0:
                # 이전 문제의 끝이나 섹션 시작 찾기
                if body[j-1] == '\n' and (body[j:j+10].startswith('$') or 
                    body[j:j+20].find('함수') != -1 or 
                    body[j:j+20].find('그림') != -1 or
                    body[j:j+30].find('닫힌구간') != -1 or
                    body[j:j+30].find('양수') != -1 or
                    body[j:j+30].find('실수') != -1):
                    problem_start = j
                    break
                # 이전 문제의 [4점] 찾기
                if j > 50 and body[j-50:j].find('[4점]') != -1:
                    prev_marker = body.rfind('[4점]', max(0, j-500), j)
                    if prev_marker != -1:
                        problem_start = prev_marker + 100  # 이전 문제 다음부터
                    break
        
        # 문제 끝 찾기
        problem_end = marker.end() + 300
        next_section = body.find('\\section', marker.end())
        if next_section != -1:
            problem_end = min(problem_end, next_section)
        next_problem = body.find('[4점]', marker.end() + 50)
        if next_problem != -1:
            problem_end = min(problem_end, next_problem - 50)
        
        problem_text = body[problem_start:problem_end]
        
        # 선택지 확인
        has_options = bool(re.search(r'\([1-5]\)|①|②|③|④|⑤', problem_text))
        
        # 문제 본문 추출
        question_end = problem_text.find('[4점]')
        if question_end != -1:
            question = problem_text[:question_end].strip()
            options_text = problem_text[question_end:] if has_options else ""
        else:
            question = problem_text.strip()
            options_text = ""
        
        # 정리
        question = re.sub(r'\\\\', ' ', question)
        question = re.sub(r'\\includegraphics.*?}', '', question)
        question = re.sub(r'\$\$', ' ', question)  # $$ 블록 제거
        question = re.sub(r'\s+', ' ', question)
        
        # 문제 시작 부분이 너무 짧으면 이전 문제의 일부일 수 있음
        # 문제 시작 키워드 확인
        if len(question) < 50:
            # 이전 문제의 끝 부분일 가능성 - 더 앞으로 확장
            extended_start = max(0, problem_start - 200)
            extended_text = body[extended_start:problem_end]
            question_end_ext = extended_text.find('[4점]')
            if question_end_ext != -1:
                question = extended_text[:question_end_ext].strip()
                question = re.sub(r'\\\\', ' ', question)
                question = re.sub(r'\\includegraphics.*?}', '', question)
                question = re.sub(r'\$\$', ' ', question)
                question = re.sub(r'\s+', ' ', question)
                options_text = extended_text[question_end_ext:] if has_options else ""
        
        # 문제 2번은 "구하시오"로 끝나는 주관식 문제
        # 문제 2번 특별 처리: "구하시오"가 있고 "Chapter 2" 섹션 전
        is_problem_02 = '구하시오' in question and 'Chapter 2' not in body[max(0, marker.start()-500):marker.start()]
        
        if len(question) < 30 and not is_problem_02:  # 문제 2번은 예외
            continue
        
        # 선택지 추출
        options = []
        if has_options and options_text:
            for opt_num in range(1, 6):
                # body에서는 $ 형태 (백슬래시 없음) 또는 \\$ 형태
                patterns = [
                    rf'\({opt_num}\)\s*\$\$?frac{{([0-9]+)}}\{{([0-9]+)}}\$',  # (1) $\frac{1}{2}$ 또는 (1) $$frac{1}{2}$
                    rf'\({opt_num}\)\s*\$\$?sqrt{{([0-9]+)}}\$',                # (1) $\sqrt{3}$
                    rf'\({opt_num}\)\s*\$\$?([0-9]+) \\sqrt{{([0-9]+)}}\$',     # (1) $2 \sqrt{3}$
                    rf'\({opt_num}\)\s*\$\$?\\frac{{([0-9]+) \\sqrt{{([0-9]+)}}}}\{{([0-9]+)}}\$',  # (1) $\frac{3\sqrt{3}}{2}$
                    rf'\({opt_num}\)\s*([0-9]+)(?=\\\\\\\\)',                    # (1) 20\\
                    rf'\({opt_num}\)\s*([0-9]+)(?=\\\\|\s|$)',                  # (1) 20
                ]
                match = None
                for pattern in patterns:
                    match = re.search(pattern, options_text)
                    if match:
                        break
                
                if match:
                    option_num = ["①", "②", "③", "④", "⑤"][opt_num-1]
                    if len(match.groups()) == 2 and match.group(1).isdigit() and match.group(2).isdigit():
                        # 분수
                        opt_text = f"\\frac{{{match.group(1)}}}{{{match.group(2)}}}"
                        options.append(f"{option_num} ${opt_text}$")
                    elif len(match.groups()) == 1 and match.group(1).isdigit():
                        # 정수 또는 제곱근
                        if 'sqrt' in pattern:
                            opt_text = f"\\sqrt{{{match.group(1)}}}"
                            options.append(f"{option_num} ${opt_text}$")
                        else:
                            options.append(f"{option_num} {match.group(1)}")
                    elif len(match.groups()) == 2:
                        # 숫자와 제곱근
                        opt_text = f"{match.group(1)} \\sqrt{{{match.group(2)}}}"
                        options.append(f"{option_num} ${opt_text}$")
                    elif len(match.groups()) == 3:
                        # 분수와 제곱근
                        opt_text = f"\\frac{{{match.group(1)} \\sqrt{{{match.group(2)}}}}}{{{match.group(3)}}}"
                        options.append(f"{option_num} ${opt_text}$")
        
        # 문제 추가
        # 인덱스는 점수 마커 순서대로 (1부터 10까지)
        # 단, 문제 2번은 이미 특별 추출했으므로 스킵
        is_problem_02 = '정수.*개수' in question or ('구하시오' in question and 'Chapter 2' not in body[max(0, marker.start()-500):marker.start()] and i == 2)
        
        # 문제 2번은 이미 추가했으므로 스킵
        if is_problem_02 and any(p.get("index") == "02" for p in problems):
            continue
        
        if len(options) == 5:
            # 문제 2번이 이미 있으면 인덱스 조정
            if any(p.get("index") == "02" for p in problems) and i == 2:
                problem_idx = "03"
            elif any(p.get("index") == "02" for p in problems) and i > 2:
                problem_idx = f"{i:02d}"
            else:
                problem_idx = f"{i:02d}"
            problems.append({
                "index": problem_idx,
                "page": (i // 2) + 1,
                "topic": "삼각함수",
                "question": question,
                "point": 4,
                "answer_type": "multiple_choice",
                "options": options
            })
        elif len(question) > 50:
            # 문제 2번이 이미 있으면 인덱스 조정
            if any(p.get("index") == "02" for p in problems) and i == 2:
                problem_idx = "03"
            elif any(p.get("index") == "02" for p in problems) and i > 2:
                problem_idx = f"{i:02d}"
            else:
                problem_idx = f"{i:02d}"
            problems.append({
                "index": problem_idx,
                "page": (i // 2) + 1,
                "topic": "삼각함수",
                "question": question,
                "point": 4,
                "answer_type": "short_answer"
            })
    
    # 기존 패턴 기반 추출 코드는 제거하고 위의 점수 마커 기반 추출만 사용
    return problems

def review_problems(problems):
    """문제 데이터 검토"""
    print("=" * 60)
    print("[수1 드릴 P3 문제 데이터 검토]")
    print("=" * 60)
    
    issues = []
    
    for prob in problems:
        idx = prob.get("index", "?")
        print(f"\n[문제 {idx}]")
        
        question = prob.get("question", "")
        if '$' in question and question.count('$') % 2 != 0:
            issues.append(f"문제 {idx}: LaTeX 수식 괄호 불일치")
            print("[LaTeX] 오류: 수식 괄호 불일치")
        else:
            print("[LaTeX] 정상")
        
        print(f"[내용 길이] {len(question)}자")
        
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
    
    return len(issues) == 0

def save_for_deepseek(problems):
    """딥시크용 CSV 저장"""
    base_dir = Path(r'C:\Users\a\Documents\MathPDF\organized\현우진\수1_2025학년도_현우진_드릴')
    save_dir = base_dir
    save_dir.mkdir(parents=True, exist_ok=True)
    
    # CSV 저장
    csv_path = save_dir / "수1_2025학년도_현우진_드릴_P3_문제_deepseek.csv"
    with open(csv_path, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['index', 'page', 'topic', 'question', 'options', 'answer_type', 'point'])
        for problem in problems:
            options_str = ', '.join(problem.get('options', [])) if problem.get('options') else ''
            writer.writerow([
                problem.get('index', ''),
                problem.get('page', ''),
                problem.get('topic', ''),
                problem.get('question', ''),
                options_str,
                problem.get('answer_type', ''),
                problem.get('point', '')
            ])
    
    print(f"\n[CSV 저장 완료] {csv_path}")
    
    # JSON 저장
    json_path = save_dir / "수1_2025학년도_현우진_드릴_P3_문제_deepseek.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(problems, f, ensure_ascii=False, indent=2)
    
    print(f"[JSON 저장 완료] {json_path}")
    
    return csv_path, json_path

def main():
    print("=" * 60)
    print("[수1 드릴 P3 문제 LaTeX → CSV 변환]")
    print("=" * 60)
    
    # 1단계: LaTeX 읽기
    print(f"\n[1단계] LaTeX 내용 읽기 완료 ({len(latex_content)}자)")
    
    # 2단계: 문제 추출
    print("\n[2단계] 문제 추출 중...")
    problems = extract_problems_from_latex(latex_content)
    print(f"[완료] {len(problems)}개 문제 추출됨")
    
    # 3단계: 검토
    print("\n[3단계] 문제 검토 중...")
    is_valid = review_problems(problems)
    
    # 4단계: 저장
    print("\n[4단계] 딥시크용 파일 저장 중...")
    csv_path, json_path = save_for_deepseek(problems)
    
    print("\n" + "=" * 60)
    print("[완료] 딥시크가 읽을 수 있는 형태로 저장되었습니다.")
    print("=" * 60)
    base_dir = Path(r'C:\Users\a\Documents\MathPDF\organized\현우진\수1_2025학년도_현우진_드릴')
    print(f"저장 위치: {base_dir}")
    print(f"  - CSV: {csv_path.name}")
    print(f"  - JSON: {json_path.name}")

if __name__ == '__main__':
    main()
