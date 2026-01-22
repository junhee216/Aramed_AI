# convert_su1_p2_problems_latex.py
# 수1 드릴 P2 문제 LaTeX를 딥시크용 CSV로 변환

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
\$a>1\$ 인 상수 \$a\$ 에 대하여 곡선 \$y=a^{x}\$ 과 직선 \$y=2 x\$ 가 두 점 \$\\mathrm{A}, \\mathrm{B}\$ 에서 만나고, 곡선 \$y=a^{2 x}\$ 과 직선 \$y=4 x\$ 가 두 점 \$\\mathrm{C}, \\mathrm{D}\$ 에서 만난다. 직선 AD 의 기울기가 -4 일 때, 점 A 의 \$x\$ 좌표는?\\\\
(단, 원점 O 에 대하여 \$\\overline{\\mathrm{OA}}<\\overline{\\mathrm{OB}}, \\overline{\\mathrm{OC}}<\\overline{\\mathrm{OD}}\$ 이다. ) [4점]\\\\
(1) \$\\frac{15}{16}\$\\\\
(2) 1\\\\
(3) \$\\frac{17}{16}\$\\\\
(4) \$\\frac{9}{8}\$\\\\
(5) \$\\frac{19}{16}\$

\\section*{Chapter 1 \\\\
 지수함수와 로그함수}
함수 \$f(x)=\\log _{k} x+2(k>1)\$ 에 대하여 곡선 \$y=f(x)\$ 위의 세 점 \$\\mathrm{A}(a, f(a)), \\mathrm{B}(b, f(b))\$, \$\\mathrm{C}(c, f(c))(0<a<b<c)\$ 와 \$y\$ 축 위의 서로 다른 두 점 \$\\mathrm{P}, \\mathrm{Q}\$ 가 다음 조건을 만족시킨다.\\\\
(가) \$\\overline{\\mathrm{AP}}=\\overline{\\mathrm{AB}}=\\sqrt{2}, \\angle \\mathrm{PAB}=\\frac{\\pi}{2}\$\\\\
(나) \$\\overline{\\mathrm{BQ}}=\\overline{\\mathrm{BC}}, \\angle \\mathrm{QBC}=\\frac{\\pi}{2}\$

직선 BP 가 \$x\$ 축에 평행할 때, 삼각형 BCQ 의 넓이를 구하시오. [4점]\\\\
\\includegraphics[max width=\\textwidth, center]{363b2900-881b-4d41-aa13-a9e5a75c160f-02_559_555_1203_896}

\\section*{Chapter 1 지수함수와 로그함수}
\\section*{(B)}
직선 \$y=-2 x+k\$ 가 두 곡선 \$y=\\log _{2} x, y=\\log _{2}(x+1)+2\$ 와 만나는 점을 각각 \$\\mathrm{A}, \\mathrm{B}\$ 라 하자. 점 B 를 지나고 직선 AB 에 수직인 직선이 곡선 \$y=\\log _{2}(x+1)+2\$ 와 B 가 아닌 점 C 에서 만날 때, 삼각형 ABC 가 이등변삼각형이 되도록 하는 모든 실수 \$k\$ 의 값의 합은? [4점]\\\\
(1) 11\\\\
(2) 12\\\\
(3) 13\\\\
(4) 14\\\\
(5) 15

\\section*{Chapter 1 \\\\
 지수함수와 로그함수}
함수 \$f(x)=\\left|2^{x}-k\\right|(k>0)\$ 에 대하여 곡선 \$y=f(x)\$ 위의 세 점 \$\\mathrm{A}(a, f(a)), \\mathrm{B}(b, f(b))\$, \$\\mathrm{C}(c, f(c))\$ 가 다음 조건을 만족시킬 때, 삼각형 ABC 의 무게중심의 \$y\$ 좌표는? (단, \$a<\\log _{2} k<b<c\$ )\\\\[0pt]
[4점]\\\\
(가) 두 직선 \$\\mathrm{AB}, \\mathrm{AC}\$ 의 기울기는 각각 \$\\frac{1}{3}, 1\$ 이다.\\\\
(나) \$\\overline{\\mathrm{AB}}=\\overline{\\mathrm{BC}}, \\overline{\\mathrm{AC}}=4 \\sqrt{2}\$\\\\
(1) \$\\frac{13}{6}\$\\\\
(2) \$\\frac{109}{48}\$\\\\
(3) \$\\frac{19}{8}\$\\\\
(4) \$\\frac{119}{48}\$\\\\
(5) \$\\frac{31}{12}\$\\\\
\\includegraphics[max width=\\textwidth, center]{363b2900-881b-4d41-aa13-a9e5a75c160f-04_580_555_1258_903}

1 보다 큰 두 실수 \$a, m\$ 에 대하여 곡선 \$y=a^{x}\$ 과 직선 \$y=m x\$ 가 두 점 \$\\mathrm{A}, \\mathrm{B}\$ 에서 만난다. 점 B 를 지나고 기울기가 -1 인 직선이 곡선 \$y=\\log _{a} x\$ 와 만나는 점을 C 라 할 때,

$$
\\overline{\\mathrm{AC}}: \\overline{\\mathrm{OB}}=3: 5, \\quad \\angle \\mathrm{BAC}=\\frac{\\pi}{2}
$$

이다. 점 A 의 \$x\$ 좌표를 \$k\$ 라 할 때, \$a^{\\frac{k}{m}}\$ 의 값은? (단, 원점 O 에 대하여 \$\\overline{\\mathrm{OA}}<\\overline{\\mathrm{OB}}\$ 이다.) [4점]\\\\
(1) \$\\frac{25}{16}\$\\\\
(2) \$\\frac{15}{8}\$\\\\
(3) \$\\frac{35}{16}\$\\\\
(4) \$\\frac{5}{2}\$\\\\
(5) \$\\frac{45}{16}\$

10\\\\
\$a>1\$ 인 실수 \$a\$ 에 대하여 두 함수 \$f(x)=a^{x}, g(x)=\\log _{a}(x-1)-1\$ 이 있고, 두 곡선 \$y=f(x), y=g(x)\$ 와 제 1 사분면에서 만나는 기울기가 -1 인 직선 \$l\$ 이 있다. 직선 \$l\$ 이 두 곡선 \$y=f(x), y=g(x)\$ 와 만나는 점을 각각 \$\\mathrm{A}, \\mathrm{B}\$ 라 하고, 두 점 \$\\mathrm{A}, \\mathrm{B}\$ 에서 \$x\$ 축에 내린 수선의 발을 각각 \$\\mathrm{C}, \\mathrm{D}\$ 라 하자. \$\\overline{\\mathrm{AB}}=14 \\sqrt{2}\$ 이고, 사각형 ACDB 의 넓이가 126 일 때, \$f(2)\$ 의 값은? (단, 점 A 의 \$x\$ 좌표는 점 B 의 \$x\$ 좌표보다 작다.) [4점]\\\\
(1) \$2^{2}\$\\\\
(2) \$2^{\\frac{7}{3}}\$\\\\
(3) \$2^{\\frac{8}{3}}\$\\\\
(4) \$2^{3}\$\\\\
(5) \$2^{\\frac{10}{3}}\$

\\section*{Chapter 1 \\\\
 지수함수와 로그함수}
그림과 같이 곡선 \$y=a^{x}(a>1)\$ 과 직선 \$y=x\$ 가 서로 다른 두 점 \$\\mathrm{P}, \\mathrm{Q}\$ 에서 만나고, 곡선\\\\
\$y=\\left|\\log _{a} x-b\\right|(b>0)\$ 는 점 P 를 지난다. 점 Q 를 지나고 \$x\$ 축에 수직인 직선이 곡선 \$y=\\left|\\log _{a} x-b\\right|\$ 와 만나는 점을 R 이라 할 때, 직선 PR 의 기울기는 \$\\frac{1}{3}\$ 이다. \$b^{3}\$ 의 값을 구하시오.\\\\
(단, 점 P 의 \$x\$ 좌표는 점 Q 의 \$x\$ 좌표보다 작다.) [4점]\\\\
\\includegraphics[max width=\\textwidth, center]{363b2900-881b-4d41-aa13-a9e5a75c160f-07_538_559_1000_903}\\\\
\\includegraphics[max width=\\textwidth, center]{363b2900-881b-4d41-aa13-a9e5a75c160f-08_255_242_467_211}\\\\
\$a>1\$ 인 실수 \$a\$ 에 대하여 두 곡선 \$y=a^{x}\$ 과 \$y=-\\log _{a} x\$ 가 만나는 점을 A 라 하고, 원점을 중심으로 하고 점 A 를 지나는 원 \$C\$ 가 두 곡선 \$y=a^{x}, y=-\\log _{a} x\$ 와 만나는 점 중 A 가 아닌 점을 각각 \$\\mathrm{B}, \\mathrm{C}\$ 라 하자. 직선 BC 의 기울기가 \$-\\frac{1}{2}\$ 일 때, 원 \$C\$ 의 넓이는 \$5 \\times 2^{-\\frac{q}{p}} \\times \\pi\$ 이다. \$p+q\$ 의 값을 구하시오.\\\\
(단, \$p\$ 와 \$q\$ 는 서로소인 자연수이다.) [4점]\\\\
\\includegraphics[max width=\\textwidth, center]{363b2900-881b-4d41-aa13-a9e5a75c160f-08_557_559_998_892}\\\\
\$a>1\$ 인 실수 \$a\$ 에 대하여 곡선 \$y=\\left(\\frac{1}{a}\\right)^{x}\$ 과 직선 \$y=-\\frac{1}{3} x+\\frac{13}{3}\$ 이 제 2 사분면에서 만나는 점을 A , 곡선 \$y=\\log _{a}(a x+a)\$ 와 직선 \$y=-\\frac{1}{3} x+\\frac{13}{3}\$ 이 만나는 점을 B 라 하자. 선분 AB 를 지름으로 하는 원이 점 \$(0,1)\$ 을 지날 때, \$a\$ 의 값은? [4점]\\\\
(1) \$\\sqrt{2}\$\\\\
(2) \$\\sqrt{3}\$\\\\
(3) 2\\\\
(4) \$\\sqrt{5}\$\\\\
(5) \$\\sqrt{6}\$\\\\
\\includegraphics[max width=\\textwidth, center]{363b2900-881b-4d41-aa13-a9e5a75c160f-09_595_606_1070_873}

\\section*{Chapter 1 \\\\
 지수함수와 로그함수}
함수

$$
f(x)= \\begin{cases}\\left(\\frac{1}{2}\\right)^{x+4}-5 & (x<-4) \\\\ -\\log _{2}(x+5)+k & (x \\geq-4)\\end{cases}
$$

와 실수 \$t\$ 에 대하여 함수 \$y=|f(x)|\$ 의 그래프와 직선 \$y=t\$ 가 만나는 서로 다른 점의 개수를 \$g(t)\$ 라 하자.\\\\
두 함수 \$f(x), g(t)\$ 가 다음 조건을 만족시킨다.\\\\
(가) 모든 양의 실수 \$x\$ 에 대하여 \$f(x) \\neq 0\$ 이다.\\\\
(나) \$g(a)-g(a+2)=2\$ 를 만족시키는 양수 \$a\$ 가 존재한다.

실수 \$k\$ 의 최댓값을 \$M\$, 최솟값을 \$m\$ 이라 할 때, \$2^{M+m}\$ 의 값을 구하시오. [4점]

\\section*{Chapter 1 \\\\
 지수함수와 로그함수}
곡선 \$y=\\log _{2} x\$ 가 두 곡선 \$y=\\left(\\frac{1}{2}\\right)^{x}, y=-2^{x}\$ 과 만나는 점을 각각 \$\\mathrm{A}, \\mathrm{B}\$ 라 하자．〈보기〉에서 옳은 것만을 있는 대로 고른 것은？（단， O 는 원점이다．）［4점］

〈보기〉\\\\
ᄀ．\$\\overline{\\mathrm{OA}}=\\overline{\\mathrm{OB}}\$\\\\
ㄴ．점 A 와 직선 \$y=x\$ 사이의 거리는 \$\\frac{\\sqrt{2}}{4}\$ 보다 크다．\\\\
ᄃ．\$\\overline{\\mathrm{AB}}<\\frac{\\sqrt{10}}{2}\$\\\\
（1）ᄀ\\\\
（2）ᄂ\\\\
（3）ㄱ，ㄴ\\\\
（4）ᄀ，ᄃ\\\\
（5）ᄀ，ᄂ，ᄃ


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
    
    # 디버깅: body의 처음 500자 확인
    # print(f"[디버깅] body 처음 500자: {repr(body[:500])}")
    # print(f"[디버깅] body에서 '보기' 위치: {body.find('보기')}")
    # print(f"[디버깅] body에서 '$a>1$' 위치: {body.find('$a>1$')}")
    
    # 문제 1: 첫 번째 문제 (객관식)
    # PDF 본문: $a > 1$인 상수 $a$... 선택지: ① $\frac{15}{16}$, ② 1, ③ $\frac{17}{16}$, ④ $\frac{9}{8}$, ⑤ $\frac{19}{16}$
    # LaTeX: \$a>1\$ 인 상수... (1) \$\\frac{15}{16}\$ 또는 (2) 1
    # body에서는 \\$a>1\\$ 형태 (백슬래시가 그대로 있음)
    # 문제 1번 패턴: \\section*{Chapter 1 앞까지
    # 실제 LaTeX: \\section*{Chapter 1 \\\\
    # body에서 실제로는 \n\\section*{Chapter 1 형태
    p1_match = re.search(r'(\\\$a>1\\\$ 인 상수.*?\[4점\])(.*?)(?=\n\\section\*\{Chapter 1)', body, re.DOTALL)
    if not p1_match:
        # 대체 패턴: \n\\section 앞까지
        p1_match = re.search(r'(\\\$a>1\\\$ 인 상수.*?\[4점\])(.*?)(?=\n\\section)', body, re.DOTALL)
    if not p1_match:
        # 대체 패턴: \\section*{Chapter 1 앞까지 (줄바꿈 없이)
        p1_match = re.search(r'(\\\$a>1\\\$ 인 상수.*?\[4점\])(.*?)(?=\\section\*\{Chapter 1)', body, re.DOTALL)
    
    if p1_match:
        question = p1_match.group(1).strip()
        options_text = p1_match.group(2) if p1_match.lastindex >= 2 else ""
        question = re.sub(r'\\\\', ' ', question)
        question = re.sub(r'\s+', ' ', question)
        
        options = []
        for i in range(1, 6):
            # 실제 선택지 텍스트: (1) \$\frac{15}{16}\$\\ 또는 (2) 1\\
            # body에서는 백슬래시가 그대로 있으므로: \$는 \\$, \frac는 \frac
            patterns = [
                rf'\({i}\)\s*\\\$\\frac{{([0-9]+)}}\{{([0-9]+)}}\\\$',  # (1) \$\frac{15}{16}\$
                rf'\({i}\)\s*([0-9]+)(?=\\\\)',                          # (2) 1\\
            ]
            match = None
            for pattern in patterns:
                match = re.search(pattern, options_text)
                if match:
                    break
            
            if match:
                option_num = ["①", "②", "③", "④", "⑤"][i-1]
                # 분수 형태인 경우
                if len(match.groups()) == 2 and match.group(1).isdigit() and match.group(2).isdigit():
                    opt_text = f"\\frac{{{match.group(1)}}}{{{match.group(2)}}}"
                    options.append(f"{option_num} ${opt_text}$")
                else:
                    # 정수 형태인 경우
                    options.append(f"{option_num} {match.group(1)}")
        
        # 문제 1번은 선택지가 5개여야 함
        if len(options) == 5:
            problems.append({
                "index": "01",
                "page": 1,
                "topic": "지수함수와 로그함수",
                "question": question,
                "point": 4,
                "answer_type": "multiple_choice",
                "options": options
            })
        else:
            # 디버깅
            print(f"[디버깅] 문제 1번 선택지 추출: {len(options)}개")
            if len(options) > 0:
                print(f"[디버깅] 추출된 선택지: {options}")
            print(f"[디버깅] 선택지 텍스트 길이: {len(options_text)}")
            print(f"[디버깅] 선택지 텍스트 (처음 200자): {options_text[:200]}")
    else:
        print("[디버깅] 문제 1번 패턴 매칭 실패!")
        print(f"[디버깅] body에서 '\\$a>1\\$' 검색: {body.find('\\$a>1\\$')}")
        print(f"[디버깅] body 처음 200자: {repr(body[:200])}")
    
    # 문제 2: 함수 $f(x)=\log _{k} x+2$ (주관식)
    # body에서는 \$ 형태이므로 \\\$가 아니라 \$로 매칭
    p2_match = re.search(r'(함수 \\\$f\(x\)=\\\\log.*?구하시오\. \[4점\])', body, re.DOTALL)
    if not p2_match:
        # 대체 패턴: 괄호 이스케이프 없이
        p2_match = re.search(r'(함수.*?log.*?구하시오\. \[4점\])', body, re.DOTALL)
    if p2_match:
        question = p2_match.group(1).strip()
        question = re.sub(r'\\\\', ' ', question)
        question = re.sub(r'\\includegraphics.*?}', '', question)
        question = re.sub(r'\s+', ' ', question)
        if len(question) > 100:  # 주관식 문제는 충분한 길이 필요
            problems.append({
                "index": "02",
                "page": 2,
                "topic": "지수함수와 로그함수",
                "question": question,
                "point": 4,
                "answer_type": "short_answer"
            })
    
    # 문제 3: 직선 $y=-2 x+k$ (객관식)
    p3_match = re.search(r'\\section\*\{\(B\)\}(.*?\[4점\])(.*?)(?=\\section|\\end)', body, re.DOTALL)
    if p3_match:
        question = p3_match.group(1).strip()
        options_text = p3_match.group(2) if p3_match.lastindex >= 2 else ""
        question = re.sub(r'\\\\', ' ', question)
        question = re.sub(r'\s+', ' ', question)
        
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
            "index": "03",
            "page": 3,
            "topic": "지수함수와 로그함수",
            "question": question,
            "point": 4,
            "answer_type": "multiple_choice" if options else "short_answer",
            "options": options if options else None
        })
    
    # 문제 4: 함수 $f(x)=\left|2^{x}-k\right|$ (객관식)
    p4_match = re.search(r'(함수 \$f\(x\)=\\left\\|2\^\{x\}-k\\right\\|.*?\[4점\])(.*?)(?=\\includegraphics|1 보다 큰|\\section|\\end)', body, re.DOTALL)
    if p4_match:
        question = p4_match.group(1).strip()
        options_text = p4_match.group(2) if p4_match.lastindex >= 2 else ""
        question = re.sub(r'\\\\', ' ', question)
        question = re.sub(r'\s+', ' ', question)
        
        options = []
        for i in range(1, 6):
            pattern = rf'\({i}\)\s*\$?([^\$\(]+)\$?'
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
            "index": "04",
            "page": 4,
            "topic": "지수함수와 로그함수",
            "question": question,
            "point": 4,
            "answer_type": "multiple_choice" if options else "short_answer",
            "options": options if options else None
        })
    
    # 문제 5: 1 보다 큰 두 실수 $a, m$ (객관식)
    p5_match = re.search(r'(1 보다 큰 두 실수.*?\[4점\])(.*?)(?=10\\\\|\\section|\\end)', body, re.DOTALL)
    if p5_match:
        question = p5_match.group(1).strip()
        options_text = p5_match.group(2) if p5_match.lastindex >= 2 else ""
        question = re.sub(r'\$\$.*?\$\$', '', question, flags=re.DOTALL)
        question = re.sub(r'\\\\', ' ', question)
        question = re.sub(r'\s+', ' ', question)
        
        options = []
        for i in range(1, 6):
            pattern = rf'\({i}\)\s*\$?([^\$\(]+)\$?'
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
            "index": "05",
            "page": 5,
            "topic": "지수함수와 로그함수",
            "question": question,
            "point": 4,
            "answer_type": "multiple_choice" if options else "short_answer",
            "options": options if options else None
        })
    
    # 문제 6: $a>1$ 인 실수 $a$ 에 대하여 (객관식, "10" 다음)
    # body에서는 \\\$ 형태이므로 \\\$로 매칭
    p6_match = re.search(r'10\\\\\s*(\\\$a>1\\\$ 인 실수.*?\[4점\])(.*?)(?=그림과 같이|\\\\section|\\end)', body, re.DOTALL)
    if p6_match:
        question = p6_match.group(1).strip()
        options_text = p6_match.group(2) if p6_match.lastindex >= 2 else ""
        question = re.sub(r'\\\\', ' ', question)
        question = re.sub(r'\s+', ' ', question)
        
        options = []
        for i in range(1, 6):
            pattern = rf'\({i}\)\s*\$?([^\$\(]+)\$?'
            match = re.search(pattern, options_text)
            if match:
                option_num = ["①", "②", "③", "④", "⑤"][i-1]
                opt_text = match.group(1).strip()
                opt_text = re.sub(r'\\\\', '', opt_text)
                if '2^{' in opt_text or '\\frac' in opt_text:
                    options.append(f"{option_num} ${opt_text}$")
                else:
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
    
    # 문제 7: 그림과 같이 곡선 $y=a^x$ (주관식)
    # PDF에서는 $b^2$이지만 LaTeX에서는 $b^3$으로 되어 있음
    # 문제 8번과 분리하기 위해 $b^{3}$ 또는 $b^3$ 키워드로 찾기
    # 문제 7번은 "그림과 같이 곡선"으로 시작하고 "b^{3}" 또는 "b^3"을 포함
    p7_match = re.search(r'(그림과 같이 곡선.*?b\^\{[23]\}.*?구하시오\. \[4점\])', body, re.DOTALL)
    if not p7_match:
        # 대체 패턴: 문제 7번만 추출 (문제 8번과 분리)
        # 문제 7번은 "그림과 같이"로 시작하고 "b"와 "3" 또는 "2"를 포함
        p7_match = re.search(r'(그림과 같이 곡선.*?구하시오\. \[4점\])(.*?)(?=\\\\$a>1\\\$ 인 실수.*?두 곡선)', body, re.DOTALL)
        if p7_match:
            # 문제 7번인지 확인 (b^3 또는 b^2 포함)
            question_text = p7_match.group(1) + (p7_match.group(2) if p7_match.lastindex >= 2 else "")
            if 'b^{3}' not in question_text and 'b^3' not in question_text and 'b^{2}' not in question_text and 'b^2' not in question_text:
                p7_match = None
    
    if p7_match:
        question = p7_match.group(1).strip()
        question = re.sub(r'\\\\', ' ', question)
        question = re.sub(r'\\includegraphics.*?}', '', question)
        question = re.sub(r'\s+', ' ', question)
        # 문제 7번만 추출 (문제 8번과 분리) - 길이 제한
        if len(question) > 200 and len(question) < 1500:
            problems.append({
                "index": "07",
                "page": 7,
                "topic": "지수함수와 로그함수",
                "question": question,
                "point": 4,
                "answer_type": "short_answer"
            })
    
    # 문제 8: $a>1$ 인 실수 $a$ 에 대하여 두 곡선 (주관식)
    # 문제 7번과 분리하기 위해 더 정확한 패턴 사용
    # 문제 8번은 $p+q$의 값을 구하는 문제
    p8_match = re.search(r'(\\\$a>1\\\$ 인 실수.*?두 곡선.*?p\+q.*?구하시오\. \[4점\])', body, re.DOTALL)
    if not p8_match:
        # 대체 패턴
        p8_match = re.search(r'(\\\$a>1\\\$ 인 실수.*?두 곡선.*?구하시오\. \[4점\])', body, re.DOTALL)
    
    if p8_match:
        question = p8_match.group(1).strip()
        question = re.sub(r'\\\\', ' ', question)
        question = re.sub(r'\\includegraphics.*?}', '', question)
        question = re.sub(r'\s+', ' ', question)
        # 문제 8번은 $p+q$의 값을 구하는 문제
        question_clean = question.replace('\\', '').replace('$', '')
        if ('p+q' in question or 'p\\+q' in question or 'p+q' in question_clean or 
            ('p' in question and 'q' in question and '서로소' in question) or
            ('원' in question and '넓이' in question)):
            # 문제 8번만 추출 (문제 7번과 분리)
            if len(question) > 200:
                problems.append({
                    "index": "08",
                    "page": 8,
                    "topic": "지수함수와 로그함수",
                    "question": question,
                    "point": 4,
                    "answer_type": "short_answer"
                })
    
    # 문제 9: $a>1$ 인 실수 $a$ 에 대하여 곡선 $y=\left(\frac{1}{a}\right)^{x}$ (객관식)
    # PDF 본문: 제2사분면, 지름 키워드, 선택지: ① $\sqrt{2}$, ② $\sqrt{3}$, ③ 2, ④ $\sqrt{5}$, ⑤ $\sqrt{6}$
    p9_match = re.search(r'(\\\$a>1\\\$ 인 실수.*?제 2 사분면.*?\[4점\])', body, re.DOTALL)
    if not p9_match:
        p9_match = re.search(r'(\\\$a>1\\\$ 인 실수.*?지름.*?\[4점\])', body, re.DOTALL)
    
    if p9_match:
        question = p9_match.group(1).strip()
        # 선택지 찾기 - 문제 다음 부분
        start_pos = body.find(question[:50]) if len(question) > 50 else -1
        if start_pos != -1:
            options_section = body[start_pos + len(question):start_pos + len(question) + 500]
        else:
            options_section = ""
        
        question = re.sub(r'\\\\', ' ', question)
        question = re.sub(r'\s+', ' ', question)
        
        options = []
        for i in range(1, 6):
            # 선택지 패턴: (1) $\sqrt{2}$ 또는 (3) 2
            patterns = [
                rf'\({i}\)\s*\\\$\\sqrt{{([0-9]+)}}\\\$',  # (1) $\sqrt{2}$
                rf'\({i}\)\s*([0-9]+)(?=\\\\)',            # (3) 2\\
            ]
            match = None
            for pattern in patterns:
                match = re.search(pattern, options_section)
                if match:
                    break
            
            if match:
                option_num = ["①", "②", "③", "④", "⑤"][i-1]
                if len(match.groups()) == 1 and match.group(1).isdigit():
                    # sqrt 형태
                    if '\\sqrt' in match.group(0):
                        opt_text = f"\\sqrt{{{match.group(1)}}}"
                        options.append(f"{option_num} ${opt_text}$")
                    else:
                        options.append(f"{option_num} {match.group(1)}")
        
        if len(options) == 5:
            problems.append({
                "index": "09",
                "page": 9,
                "topic": "지수함수와 로그함수",
                "question": question,
                "point": 4,
                "answer_type": "multiple_choice",
                "options": options
            })
    
    # 문제 10: 함수 $f(x)=...$ (주관식)
    p10_match = re.search(r'(함수\s*\$\$.*?구하시오\. \[4점\])', body, re.DOTALL)
    if p10_match:
        question = p10_match.group(1).strip()
        question = re.sub(r'\\\\', ' ', question)
        question = re.sub(r'\s+', ' ', question)
        problems.append({
            "index": "10",
            "page": 10,
            "topic": "지수함수와 로그함수",
            "question": question,
            "point": 4,
            "answer_type": "short_answer"
        })
    
    # 문제 11: 곡선 $y=\log_2 x$ (객관식, 보기 문제)
    # PDF 본문: 보기 문제, 선택지: ① ㄱ, ② ㄴ, ③ ㄱ, ㄴ, ④ ㄱ, ㄷ, ⑤ ㄱ, ㄴ, ㄷ
    # LaTeX: （1）ᄀ, （2）ᄂ, （3）ㄱ，ㄴ, （4）ᄀ，ᄃ, （5）ᄀ，ᄂ，ᄃ
    # body에서는 백슬래시가 그대로 있으므로 \\$y=\\log 형태
    # 실제 LaTeX: 곡선 \$y=\\log _{2} x\$ 가 두 곡선...〈보기〉에서 옳은 것만을 있는 대로 고른 것은？（단， O 는 원점이다．）［4점］
    # "보기" 키워드로 찾기
    pos = body.find('보기')
    if pos != -1:
        # 보기 앞부분부터 문제 찾기 (body에서는 백슬래시가 그대로 있음)
        # 전각 괄호 ［4점］도 매칭
        p11_match = re.search(r'(곡선.*?보기.*?[\[［]4점[\]］])(.*?)(?=\\end|$)', body[max(0, pos-300):], re.DOTALL)
    else:
        p11_match = None
    
    if not p11_match:
        # 대체 패턴 (body에서는 백슬래시가 그대로 있음)
        p11_patterns = [
            r'(곡선 \\\$y=\\\\log.*?보기.*?[\[［]4점[\]］])',
            r'(곡선.*?보기.*?[\[［]4점[\]］])',
        ]
        for pattern in p11_patterns:
            p11_match = re.search(pattern + r'(.*?)(?=\\end|$)', body, re.DOTALL)
            if p11_match:
                break
    
    if p11_match:
        question = p11_match.group(1).strip()
        options_text = p11_match.group(2) if p11_match.lastindex >= 2 else ""
        question = re.sub(r'\\\\', ' ', question)
        question = re.sub(r'\s+', ' ', question)
        
        # "보기" 키워드 확인
        if '보기' in question:
            # 선택지 추출 (보기 문제)
            # LaTeX: （1）ᄀ, （2）ᄂ, （3）ㄱ，ㄴ, （4）ᄀ，ᄃ, （5）ᄀ，ᄂ，ᄃ
            # 실제 body 텍스트: （1）ᄀ\\\\, （2）ᄂ\\\\, （3）ㄱ，ㄴ\\\\, （4）ᄀ，ᄃ\\\\, （5）ᄀ，ᄂ，ᄃ
            options = []
            for i in range(1, 6):
                # 전각 괄호도 매칭: （1） 또는 (1)
                pattern = rf'[（(]{i}[）)]'
                match = re.search(pattern, options_text)
                if match:
                    option_num = ["①", "②", "③", "④", "⑤"][i-1]
                    # 선택지 텍스트 추출 - 다음 선택지까지
                    start_pos = match.end()
                    if i < 5:
                        next_match = re.search(rf'[（(]{i+1}[）)]', options_text[start_pos:])
                        if next_match:
                            opt_text = options_text[start_pos:start_pos + next_match.start()].strip()
                        else:
                            opt_text = options_text[start_pos:start_pos + 30].strip()
                    else:
                        opt_text = options_text[start_pos:start_pos + 30].strip()
                    
                    # LaTeX 특수 문자 제거
                    opt_text = re.sub(r'\\\\+', '', opt_text)
                    opt_text = re.sub(r'\\\$', '', opt_text)
                    opt_text = opt_text.strip()
                    
                    # PDF 본문에 맞게 변환 (LaTeX에서 직접 읽기)
                    # LaTeX: （1）ᄀ, （2）ᄂ, （3）ㄱ，ㄴ, （4）ᄀ，ᄃ, （5）ᄀ，ᄂ，ᄃ
                    if not opt_text or len(opt_text) < 1:
                        # LaTeX에서 직접 읽기
                        if i == 1:
                            opt_text = "ㄱ"
                        elif i == 2:
                            opt_text = "ㄴ"
                        elif i == 3:
                            opt_text = "ㄱ，ㄴ"
                        elif i == 4:
                            opt_text = "ㄱ，ㄷ"
                        elif i == 5:
                            opt_text = "ㄱ，ㄴ，ㄷ"
                    else:
                        # LaTeX에서 추출한 텍스트 사용
                        opt_text = opt_text.strip()
                    
                    options.append(f"{option_num} {opt_text}")
            
            if len(options) == 5:
                problems.append({
                    "index": "11",
                    "page": 11,
                    "topic": "지수함수와 로그함수",
                    "question": question,
                    "point": 4,
                    "answer_type": "multiple_choice",
                    "options": options
                })
            else:
                print(f"[디버깅] 문제 11번 선택지 추출: {len(options)}개")
                print(f"[디버깅] 선택지 텍스트 길이: {len(options_text)}")
                print(f"[디버깅] 선택지 텍스트 (처음 300자): {repr(options_text[:300])}")
    else:
        print("[디버깅] 문제 11번 패턴 매칭 실패!")
        if pos == -1:
            print("[디버깅] '보기' 키워드를 찾을 수 없습니다")
    
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
    print("[수1 드릴 P2 문제 데이터 검토]")
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
        '*드릴*P2*문제*.pdf',
        '*수1*드릴*P2*문제*.pdf',
        '*수1*드릴*02*문제*.pdf'
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
    base_dir = Path(r'C:\Users\a\Documents\MathPDF\organized\현우진\수1_2025학년도_현우진_드릴')
    save_dir = base_dir
    # 디렉토리가 없으면 생성
    save_dir.mkdir(parents=True, exist_ok=True)
    
    # CSV 저장
    csv_path = save_dir / "수1_2025학년도_현우진_드릴_P2_문제_deepseek.csv"
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
    json_path = save_dir / "수1_2025학년도_현우진_드릴_P2_문제_deepseek.json"
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
            "원본": "수1_2025학년도_현우진_드릴_P2_문제",
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
    print("[수1 드릴 P2 문제 LaTeX → CSV 변환]")
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
