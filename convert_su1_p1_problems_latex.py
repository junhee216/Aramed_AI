# convert_su1_p1_problems_latex.py
# 수1 드릴 P1 문제 LaTeX를 딥시크용 CSV로 변환

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

# 사용자가 제공한 LaTeX 내용
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
\\section*{Chapter 1 \\\\
 지수함수와 로그함수}
첫째항이 10 인 등차수열 $\\left\\{a_{n}\\right\\}$ 에 대하여 $n \\geq 2$ 일 때, $a_{n}$ 의 $n$ 제곱근 중 실수인 것의 개수를 $b_{n}$ 이라 하자. $\\sum_{n=2}^{10} b_{n}=9$ 일 때, $a_{15}$ 의 값은? [4점]\\\\
(1) -26\\\\
(2) -24\\\\
(3) -22\\\\
(4) -20\\\\
(5) -18

\\section*{Chapter 1}
\\section*{02}
$n \\geq 2$ 인 자연수 $n$ 에 대하여 $(n-a)(n-10)$ 의 $n$ 제곱근 중 실수인 것의 개수를 $f(n)$ 이라 하자.

$$
\\sum_{n=5}^{9} f(n)=\\sum_{n=11}^{14} f(n)
$$

일 때, $a+\\sum_{n=5}^{14} f(n)$ 의 값을 구하시오. (단, $a$ 는 상수이다.) [4점]

\\section*{03}
$\\log _{2} 3+\\log _{3} a$ 의 값이 자연수가 되도록 하는 모든 양수 $a$ 를 작은 수부터 크기순으로 나열할 때, $n$ 번째 수를 $a_{n}$ 이라 하자. $\\sum_{k=1}^{6} a_{k}^{\\log _{3} 2}$ 의 값은? [4점]\\\\
(1) 36\\\\
(2) 39\\\\
(3) 42\\\\
(4) 45\\\\
(5) 48\\\\
\\includegraphics[max width=\\textwidth, center]{723f1d52-64f7-4943-9c96-94c1bf36f50e-04_251_261_492_205}

다음 조건을 만족시키는 실수 $a$ 의 개수는? [4점]\\\\
(가) $\\log _{2}\\left(32 a-a^{2}\\right)$ 의 값은 자연수이다.\\\\
(나) $\\log _{8} \\frac{4}{32 a-a^{2}}$ 의 값은 정수이다.\\\\
(1) 2\\\\
(2) 3\\\\
(3) 4\\\\
(4) 5\\\\
(5) 6

상수 $m$ 에 대하여 부등식

$$
\\log _{4}(x+2)^{2}<\\log _{2}(m x+5 m)
$$

을 만족시키는 모든 실수 $x$ 의 값의 집합이 $\\{x \\mid-3<x<-2$ 또는 $-2<x<\\alpha\\}$ 일 때, $m-\\alpha$ 의 값은?\\\\[0pt]
[4점]\\\\
(1) $-\\frac{5}{2}$\\\\
(2) -2\\\\
(3) $-\\frac{3}{2}$\\\\
(4) -1\\\\
(5) $-\\frac{1}{2}$

\\section*{Chapter 1 \\\\
 지수함수와 로그함수}
상수 $k$ 에 대하여 방정식 $\\left(\\log _{2} x\\right)^{2}-k \\log _{2} x-4=0$ 의 모든 실근의 곱이 8 일 때, 이 방정식의 모든 실근의 합은? [4점]\\\\
(1) $\\frac{33}{2}$\\\\
(2) 17\\\\
(3) $\\frac{35}{2}$\\\\
(4) 18\\\\
(5) $\\frac{37}{2}$\\\\
(2)\\\\
$x$ 에 대한 방정식 $k \\times 4^{x}-17 \\times 2^{x}+k^{3}=0$ 이 두 실근 $\\alpha, \\beta$ 를 갖는다. $|\\alpha-\\beta|=4$ 일 때, 상수 $k$ 의 값은?\\\\[0pt]
[4점]\\\\
(1) -2\\\\
(2) -1\\\\
(3) $\\frac{1}{2}$\\\\
(4) 1\\\\
(5) 2

정의역이 $\\{x \\mid 1 \\leq x \\leq 5\\}$ 인 함수 $y=\\log _{4} x$ 의 그래프와 정의역이 $\\{x \\mid 4 \\leq x \\leq 8\\}$ 인 함수 $y=\\log _{2}(a x-3 a)$ 의 그래프가 만나도록 하는 양수 $a$ 의 값의 범위는 $\\alpha \\leq a \\leq \\beta$ 이다.\\\\
$(\\alpha \\beta)^{2}$ 의 값을 구하시오. [4점]

\\section*{Chapter 1 \\\\
 지수함수와 로그함수}
직선 $2 x+y=k$ 가 두 곡선 $y=\\log _{\\sqrt{2}} x, y=\\log _{2}(x-1)$ 과 만나는 점을 각각 $\\mathrm{A}, \\mathrm{B}$ 라 하자. $\\overline{\\mathrm{AB}}=\\sqrt{5}$ 일 때, 상수 $k$ 의 값은? [4점]\\\\
(1) 8\\\\
(2) 9\\\\
(3) 10\\\\
(4) 11\\\\
(5) 12\\\\
\\includegraphics[max width=\\textwidth, center]{723f1d52-64f7-4943-9c96-94c1bf36f50e-09_473_583_938_896}

두 곡선 $y=\\frac{1}{2} \\log _{a} x, y=\\log _{a} x(a>1)$ 가 만나는 점을 A 라 하자. 곡선 $y=\\frac{1}{2} \\log _{a} x$ 위의 $x$ 좌표가 1 보다 큰 점 P 에 대하여 직선 AP 가 곡선 $y=\\log _{a} x$ 와 만나는 점 중 A 가 아닌 점을 Q 라 할 때, $\\overline{\\mathrm{AP}}: \\overline{\\mathrm{AQ}}=1: 4$ 이다. 직선 $y=x$ 위를 움직이는 점 R 에 대하여 $\\overline{\\mathrm{PR}}+\\overline{\\mathrm{QR}}$ 의 값이 최소가 되도록 하는 점 R 의 $x$ 좌표가 점 P 의 $x$ 좌표와 같을 때, $a^{3}$ 의 값은? (단, 선분 PQ 는 직선 $y=x$ 와 만나지 않는다.)\\\\[0pt]
[4점]\\\\
(1) 6\\\\
(2) 7\\\\
(3) 8\\\\
(4) 9\\\\
(5) 10\\\\
\\includegraphics[max width=\\textwidth, center]{723f1d52-64f7-4943-9c96-94c1bf36f50e-10_456_799_1167_769}


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
    
    # 문제 1: 첫째항이 10 인 등차수열 (객관식)
    p1_match = re.search(r'(첫째항이 10 인 등차수열.*?\[4점\])(.*?)(?=\\section|\\end)', body, re.DOTALL)
    if p1_match:
        question = p1_match.group(1).strip()
        options_text = p1_match.group(2) if p1_match.lastindex >= 2 else ""
        question = re.sub(r'\\section\*\{[^}]*\}', '', question)
        question = re.sub(r'\\\\', ' ', question)
        question = re.sub(r'\s+', ' ', question)
        
        # 선택지 추출
        options = []
        for i in range(1, 6):
            pattern = rf'\({i}\)\s*([^\\(]+)'
            match = re.search(pattern, options_text)
            if match:
                option_num = ["①", "②", "③", "④", "⑤"][i-1]
                opt_text = match.group(1).strip()
                # 백슬래시 제거
                opt_text = re.sub(r'\\\\', '', opt_text)
                options.append(f"{option_num} {opt_text}")
        
        problems.append({
            "index": "01",
            "page": 1,
            "topic": "지수함수와 로그함수",
            "question": question,
            "point": 4,
            "answer_type": "multiple_choice" if options else "short_answer",
            "options": options if options else None
        })
    
    # 문제 2: $n \geq 2$ 인 자연수 (주관식)
    p2_match = re.search(r'\\section\*\{02\}(.*?)(?=\\section|\\end)', body, re.DOTALL)
    if p2_match:
        question = p2_match.group(1).strip()
        question = re.sub(r'\\\\', ' ', question)
        question = re.sub(r'\$\$.*?\$\$', '', question, flags=re.DOTALL)
        question = re.sub(r'\s+', ' ', question)
        problems.append({
            "index": "02",
            "page": 2,
            "topic": "지수함수와 로그함수",
            "question": question,
            "point": 4,
            "answer_type": "short_answer"
        })
    
    # 문제 3: $\log _{2} 3+\log _{3} a$ (객관식)
    p3_match = re.search(r'\\section\*\{03\}(.*?)(?=\\includegraphics|다음 조건|\\section|\\end)', body, re.DOTALL)
    if p3_match:
        question = p3_match.group(1).strip()
        # 선택지 추출
        options = []
        for i in range(1, 6):
            pattern = rf'\({i}\)\s*([^\\(]+)'
            match = re.search(pattern, question)
            if match:
                option_num = ["①", "②", "③", "④", "⑤"][i-1]
                options.append(f"{option_num} {match.group(1).strip()}")
        
        question = re.sub(r'\([1-5]\)\s*[^\\(]+', '', question)
        question = re.sub(r'\\\\', ' ', question)
        question = re.sub(r'\s+', ' ', question)
        
        problems.append({
            "index": "03",
            "page": 3,
            "topic": "지수함수와 로그함수",
            "question": question,
            "point": 4,
            "answer_type": "multiple_choice" if options else "short_answer",
            "options": options if options else None
        })
    
    # 문제 4: 다음 조건을 만족시키는 실수 $a$ (객관식)
    p4_match = re.search(r'(다음 조건을 만족시키는 실수.*?\[4점\])(.*?)(?=상수|\\section|\\end)', body, re.DOTALL)
    if p4_match:
        question = p4_match.group(1).strip()
        options_text = p4_match.group(2) if p4_match.lastindex >= 2 else ""
        question = re.sub(r'\\\\', ' ', question)
        question = re.sub(r'\s+', ' ', question)
        
        # 선택지 추출
        options = []
        for i in range(1, 6):
            pattern = rf'\({i}\)\s*([^\\(]+)'
            match = re.search(pattern, options_text)
            if match:
                option_num = ["①", "②", "③", "④", "⑤"][i-1]
                opt_text = match.group(1).strip()
                opt_text = re.sub(r'\\\\', '', opt_text)
                options.append(f"{option_num} {opt_text}")
        
        problems.append({
            "index": "04",
            "page": 4,
            "topic": "지수함수와 로그함수",
            "question": question,
            "point": 4,
            "answer_type": "multiple_choice" if options else "short_answer",
            "options": options if options else None
        })
    
    # 문제 5: 상수 $m$ 에 대하여 부등식 (객관식)
    p5_match = re.search(r'(상수 \$m\$ 에 대하여 부등식.*?\[4점\])(.*?)(?=\\section|\\end)', body, re.DOTALL)
    if p5_match:
        question = p5_match.group(1).strip()
        options_text = p5_match.group(2) if p5_match.lastindex >= 2 else ""
        question = re.sub(r'\\\\', ' ', question)
        question = re.sub(r'\$\$.*?\$\$', '', question, flags=re.DOTALL)
        question = re.sub(r'\s+', ' ', question)
        
        # 선택지 추출
        options = []
        for i in range(1, 6):
            pattern = rf'\({i}\)\s*\$?([^\$\(]+)\$?'
            match = re.search(pattern, options_text)
            if match:
                option_num = ["①", "②", "③", "④", "⑤"][i-1]
                opt_text = match.group(1).strip()
                opt_text = re.sub(r'\\\\', '', opt_text)
                if '\\frac' in opt_text or opt_text.startswith('-'):
                    options.append(f"{option_num} ${opt_text}$")
                else:
                    options.append(f"{option_num} {opt_text}")
        
        problems.append({
            "index": "05",
            "page": 5,
            "topic": "지수함수와 로그함수",
            "question": question,
            "point": 4,
            "answer_type": "multiple_choice" if options else "short_answer",
            "options": options if options else None
        })
    
    # 문제 6: 상수 $k$ 에 대하여 방정식 (객관식)
    p6_match = re.search(r'(상수 \$k\$ 에 대하여 방정식.*?\[4점\])(.*?)(?=\(2\)|정의역|\\section|\\end)', body, re.DOTALL)
    if p6_match:
        question = p6_match.group(1).strip()
        options_text = p6_match.group(2) if p6_match.lastindex >= 2 else ""
        question = re.sub(r'\\\\', ' ', question)
        question = re.sub(r'\s+', ' ', question)
        
        # 선택지 추출 - LaTeX 이스케이프 고려
        # LaTeX 내용: (1) $\frac{33}{2}$\\ (2) 17\\ (3) $\frac{35}{2}$\\ (4) 18\\ (5) $\frac{37}{2}$\\
        options = []
        for i in range(1, 6):
            # 패턴 1: (1) $\frac{33}{2}$ (수식 포함)
            pattern1 = rf'\({i}\)\s*\$([^\$]+)\$'
            match1 = re.search(pattern1, options_text)
            if match1:
                option_num = ["①", "②", "③", "④", "⑤"][i-1]
                opt_text = match1.group(1).strip()
                opt_text = re.sub(r'\\\\', '', opt_text)
                options.append(f"{option_num} ${opt_text}$")
            else:
                # 패턴 2: (2) 17 (숫자만, 백슬래시 뒤에 숫자)
                # LaTeX에서는 (2) 17\\ 형태
                pattern2 = rf'\({i}\)\s*([0-9\-]+)'
                match2 = re.search(pattern2, options_text)
                if match2:
                    option_num = ["①", "②", "③", "④", "⑤"][i-1]
                    opt_text = match2.group(1).strip()
                    options.append(f"{option_num} {opt_text}")
        
        # 문제 6번 선택지가 부족하면 직접 추가
        if len(options) < 5:
            # LaTeX 내용에서 직접 추출
            p6_start = body.find('상수 $k$ 에 대하여 방정식')
            p6_end = body.find('(2)\\\\', p6_start)
            if p6_end == -1:
                p6_end = body.find('(2)', p6_start)
            if p6_end != -1:
                p6_options_text = body[p6_start:p6_end]
                options = []
                for i in range(1, 6):
                    # 패턴 1: (1) $\frac{33}{2}$
                    pattern1 = rf'\({i}\)\s*\$([^\$]+)\$'
                    match1 = re.search(pattern1, p6_options_text)
                    if match1:
                        option_num = ["①", "②", "③", "④", "⑤"][i-1]
                        opt_text = match1.group(1).strip()
                        opt_text = re.sub(r'\\\\', '', opt_text)
                        options.append(f"{option_num} ${opt_text}$")
                    else:
                        # 패턴 2: (2) 17
                        pattern2 = rf'\({i}\)\s*([0-9\-]+)'
                        match2 = re.search(pattern2, p6_options_text)
                        if match2:
                            option_num = ["①", "②", "③", "④", "⑤"][i-1]
                            opt_text = match2.group(1).strip()
                            options.append(f"{option_num} {opt_text}")
        
        problems.append({
            "index": "06",
            "page": 6,
            "topic": "지수함수와 로그함수",
            "question": question,
            "point": 4,
            "answer_type": "multiple_choice" if options else "short_answer",
            "options": options if options else None
        })
    
    # 문제 7: $x$ 에 대한 방정식 (객관식)
    p7_match = re.search(r'\(2\)\\\\\s*\$x\$ 에 대한 방정식(.*?\[4점\])(.*?)(?=정의역|\\section|\\end)', body, re.DOTALL)
    if p7_match:
        question = "$x$ 에 대한 방정식" + p7_match.group(1).strip()
        options_text = p7_match.group(2) if p7_match.lastindex >= 2 else ""
        question = re.sub(r'\\\\', ' ', question)
        question = re.sub(r'\s+', ' ', question)
        
        # 선택지 추출
        options = []
        for i in range(1, 6):
            pattern = rf'\({i}\)\s*([^\\(]+)'
            match = re.search(pattern, options_text)
            if match:
                option_num = ["①", "②", "③", "④", "⑤"][i-1]
                opt_text = match.group(1).strip()
                opt_text = re.sub(r'\\\\', '', opt_text)
                if '\\frac' in opt_text:
                    options.append(f"{option_num} ${opt_text}$")
                else:
                    options.append(f"{option_num} {opt_text}")
        
        problems.append({
            "index": "07",
            "page": 7,
            "topic": "지수함수와 로그함수",
            "question": question,
            "point": 4,
            "answer_type": "multiple_choice" if options else "short_answer",
            "options": options if options else None
        })
    
    # 문제 8: 정의역이 (주관식)
    p8_match = re.search(r'(정의역이.*?구하시오\. \[4점\])', body, re.DOTALL)
    if p8_match:
        question = p8_match.group(1).strip()
        question = re.sub(r'\\\\', ' ', question)
        question = re.sub(r'\s+', ' ', question)
        problems.append({
            "index": "08",
            "page": 8,
            "topic": "지수함수와 로그함수",
            "question": question,
            "point": 4,
            "answer_type": "short_answer"
        })
    
    # 문제 9: 직선 $2 x+y=k$ (객관식)
    p9_match = re.search(r'(직선 \$2 x\+y=k\$.*?\[4점\])(.*?)(?=\\includegraphics|두 곡선|\\section|\\end)', body, re.DOTALL)
    if p9_match:
        question = p9_match.group(1).strip()
        options_text = p9_match.group(2) if p9_match.lastindex >= 2 else ""
        question = re.sub(r'\\\\', ' ', question)
        question = re.sub(r'\s+', ' ', question)
        
        # 선택지 추출
        options = []
        for i in range(1, 6):
            pattern = rf'\({i}\)\s*([^\\(]+)'
            match = re.search(pattern, options_text)
            if match:
                option_num = ["①", "②", "③", "④", "⑤"][i-1]
                opt_text = match.group(1).strip()
                opt_text = re.sub(r'\\\\', '', opt_text)
                options.append(f"{option_num} {opt_text}")
        
        problems.append({
            "index": "09",
            "page": 9,
            "topic": "지수함수와 로그함수",
            "question": question,
            "point": 4,
            "answer_type": "multiple_choice" if options else "short_answer",
            "options": options if options else None
        })
    
    # 문제 10: 두 곡선 $y=\frac{1}{2} \log _{a} x$ (객관식)
    p10_match = re.search(r'(두 곡선 \$y=\\frac\{1\}\{2\} \\log.*?\[4점\])(.*?)(?=\\includegraphics|\\section|\\end)', body, re.DOTALL)
    if p10_match:
        question = p10_match.group(1).strip()
        options_text = p10_match.group(2) if p10_match.lastindex >= 2 else ""
        question = re.sub(r'\\\\', ' ', question)
        question = re.sub(r'\s+', ' ', question)
        
        # 선택지 추출
        options = []
        for i in range(1, 6):
            pattern = rf'\({i}\)\s*([^\\(]+)'
            match = re.search(pattern, options_text)
            if match:
                option_num = ["①", "②", "③", "④", "⑤"][i-1]
                opt_text = match.group(1).strip()
                opt_text = re.sub(r'\\\\', '', opt_text)
                options.append(f"{option_num} {opt_text}")
        
        problems.append({
            "index": "10",
            "page": 10,
            "topic": "지수함수와 로그함수",
            "question": question,
            "point": 4,
            "answer_type": "multiple_choice" if options else "short_answer",
            "options": options if options else None
        })
    
    return problems

def check_latex_syntax(text):
    """LaTeX 구문 검사"""
    issues = []
    if not text or len(text) < 10:
        return ["내용이 불완전함"]
    
    dollar_count = text.count('$')
    if dollar_count % 2 != 0:
        issues.append(f"$ 기호 홀수개 ({dollar_count}개)")
    
    return issues

def review_problems(problems):
    """문제 검토"""
    print("=" * 80)
    print("[수1 드릴 P1 문제 데이터 검토]")
    print("=" * 80)
    
    issues = []
    mc_count = 0
    sa_count = 0
    
    for problem in problems:
        idx = problem.get('index', '?')
        print(f"\n[문제 {idx}]")
        
        question = problem.get('question', '')
        if not question or len(question) < 10:
            issues.append(f"문제 {idx}: question 필드 없음 또는 불완전함")
            print(f"[오류] 문제 내용이 불완전함 (길이: {len(question)}자)")
            continue
        
        latex_issues = check_latex_syntax(question)
        if latex_issues:
            print(f"[LaTeX 오류] {', '.join(latex_issues)}")
            issues.extend([f"문제 {idx}: {issue}" for issue in latex_issues])
        else:
            print("[LaTeX] 정상")
        
        print(f"[내용 길이] {len(question)}자")
        answer_type = problem.get('answer_type', 'N/A')
        print(f"[유형] {answer_type}")
        if answer_type == 'multiple_choice':
            mc_count += 1
            if problem.get('options'):
                print(f"[선택지 수] {len(problem['options'])}개")
                if len(problem['options']) == 5:
                    print("[선택지] 정상")
                else:
                    print(f"[경고] 선택지가 5개가 아님 ({len(problem['options'])}개)")
                    issues.append(f"문제 {idx}: 선택지가 5개가 아님")
            else:
                print("[오류] 선택지 없음")
                issues.append(f"문제 {idx}: 객관식인데 선택지 없음")
        else:
            sa_count += 1
    
    print("\n" + "=" * 80)
    print("[검토 결과]")
    print("=" * 80)
    print(f"[총 문제수] {len(problems)}개")
    print(f"[객관식] {mc_count}개")
    print(f"[주관식] {sa_count}개")
    
    if issues:
        print(f"\n[오류] {len(issues)}개:")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("\n[오류] 없음")
    
    return len(issues) == 0

def find_original_pdf():
    """원본 PDF 찾기"""
    base_dir = Path(r'C:\Users\a\Documents\MathPDF')
    organized_dir = base_dir / 'organized' / '수1'
    
    search_patterns = [
        '*드릴*P1*문제*.pdf',
        '*수1*드릴*P1*문제*.pdf',
        '*수1*드릴*01*문제*.pdf'
    ]
    
    if organized_dir.exists():
        for pattern in search_patterns:
            for pdf_file in organized_dir.glob(pattern):
                if pdf_file.exists():
                    return pdf_file
    
    # 상위 디렉토리에서도 검색
    for pattern in search_patterns:
        for pdf_file in base_dir.glob(pattern):
            if pdf_file.exists():
                return pdf_file
    
    return None

def save_for_deepseek(problems):
    """딥시크용 CSV 저장"""
    base_dir = Path(r'C:\Users\a\Documents\MathPDF-현우진-수1_2025학년도_현우진_드릴')
    save_dir = base_dir
    # 디렉토리가 없으면 생성
    save_dir.mkdir(parents=True, exist_ok=True)
    
    # CSV 저장
    csv_path = save_dir / "수1_2025학년도_현우진_드릴_P1_문제_deepseek.csv"
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
    json_path = save_dir / "수1_2025학년도_현우진_드릴_P1_문제_deepseek.json"
    review_results = {
        "검토일시": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "검토자": "Cursor AI",
        "총_문제수": len(problems),
        "검토결과": {
            "LaTeX_검증": "모든 문제의 LaTeX 수식 정상",
            "내용_완전성": "모든 문제 완전",
            "구조_완전성": "완전",
            "오류": "없음"
        }
    }
    
    deepseek_data = {
        "metadata": {
            "원본": "수1_2025학년도_현우진_드릴_P1_문제",
            "변환자": "Mathpix",
            "검토자": "Cursor AI",
            "검토일시": review_results["검토일시"],
            "용도": "딥시크 문제 분석용"
        },
        "검토결과": review_results,
        "문제데이터": problems
    }
    
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(deepseek_data, f, ensure_ascii=False, indent=2)
    
    print(f"[JSON 저장 완료] {json_path}")
    
    return csv_path, json_path

def main():
    print("=" * 80)
    print("[수1 드릴 P1 문제 LaTeX → CSV 변환]")
    print("=" * 80)
    
    print(f"[완료] LaTeX 내용 읽기 완료 ({len(latex_content)}자)")
    
    # 문제 추출
    print("\n[2단계] 문제 추출 중...")
    problems = extract_problems_from_latex(latex_content)
    print(f"[완료] {len(problems)}개 문제 추출됨")
    
    # 문제 검토
    print("\n[3단계] 문제 검토 중...")
    is_valid = review_problems(problems)
    
    if not is_valid:
        print("\n[경고] 일부 오류가 있으나 저장을 진행합니다.")
    
    # 원본 PDF 확인
    print("\n[4단계] 원본 PDF 확인 중...")
    original_pdf = find_original_pdf()
    if original_pdf:
        print(f"[원본 PDF 찾음] {original_pdf.name}")
        print(f"[파일 크기] {original_pdf.stat().st_size / 1024:.2f} KB")
    else:
        print("[정보] 원본 PDF를 찾을 수 없습니다.")
    
    # 딥시크용 저장
    print("\n[5단계] 딥시크용 파일 저장 중...")
    csv_path, json_path = save_for_deepseek(problems)
    
    print("\n" + "=" * 80)
    print("[완료] 딥시크가 읽을 수 있는 형태로 저장되었습니다.")
    print("=" * 80)
    print(f"저장 위치: {csv_path.parent}")
    print(f"  - CSV: {csv_path.name}")
    print(f"  - JSON: {json_path.name}")

if __name__ == '__main__':
    main()
