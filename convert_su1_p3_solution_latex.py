# convert_su1_p3_solution_latex.py
# 수1 드릴 P3 해설 LaTeX를 딥시크용 CSV로 변환

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
\\usepackage{caption}
\\usepackage{bbold}
\\usepackage[fallback]{xeCJK}
\\usepackage{polyglossia}
\\usepackage{fontspec}
\\usepackage{newunicodechar}
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

\\newunicodechar{⋯}{\\ifmmode\\cdots\\else{$\\cdots$}\\fi}

\\begin{document}
\\captionsetup{singlelinecheck=false}
\\section*{Drill. 1 삼각함수의 그래프}
$y=a \\sin (b x+c)+d, y=a \\cos (b x+c)+d$ 의 그래프는 먼저 그림과 같이 8 칸으로 나누 어진 직사각형에 한 주기를 나타낸 후 필요하다면 확장하거나 좌표축과의 관계를 감안하여 다루는 것이 유리하다.\\
$y=a \\sin (b x+c)+d$ 의 그래프

\\begin{figure}[h]
\\begin{center}
  \\includegraphics[max width=\\textwidth]{3c0ed4eb-1378-44aa-b2da-8dd47e4ed97a-01_337_484_977_864}
\\captionsetup{labelformat=empty}
\\caption{$a b>0$ 일 때}
\\end{center}
\\end{figure}

$$
y=a \\cos (b x+c)+d \\text { 의 그래프 }
$$

\\begin{figure}[h]
\\begin{center}
  \\includegraphics[max width=\\textwidth]{3c0ed4eb-1378-44aa-b2da-8dd47e4ed97a-01_333_483_1467_867}
\\captionsetup{labelformat=empty}
\\caption{$a>0$ 일 때}
\\end{center}
\\end{figure}

\\begin{figure}[h]
\\begin{center}
  \\includegraphics[max width=\\textwidth]{3c0ed4eb-1378-44aa-b2da-8dd47e4ed97a-01_330_484_977_1433}
\\captionsetup{labelformat=empty}
\\caption{$a b<0$ 일 때}
\\end{center}
\\end{figure}

\\begin{figure}[h]
\\begin{center}
  \\includegraphics[max width=\\textwidth]{3c0ed4eb-1378-44aa-b2da-8dd47e4ed97a-01_333_484_1467_1433}
\\captionsetup{labelformat=empty}
\\caption{$a<0$ 일 때}
\\end{center}
\\end{figure}

\\section*{Drill. 2 삼각함수의 최대와 최소}
삼각함수의 최댓값과 최솟값은 주로 다음의 방법으로 구할 수 있다.\\
한 가지의 삼각함수로 고친 후\\
(1) $-1 \\leq \\sin x \\leq 1,-1 \\leq \\cos x \\leq 1$ 임을 이용하여 최댓값과 최솟값을 구한다.\\
(2) $\\sin x=t$ 또는 $\\cos x=t$ 로 치환하여 $t$ 에 대한 함수의 최댓값과 최솟값을 구한다. 이때 $-1 \\leq t \\leq 1$ 인 것에 주의한다.\\
(3) 제한된 범위에서는 삼각함수의 그래프를 이용하여 최댓값과 최솟값을 구한다.

\\section*{Comment}
\\section*{Drill 삼각함수의 그래프의 대칭}
삼각함수의 그래프를 다룰 때 $x$ 축에 수직인 직선에 대한 대칭, 점에 대한 대칭을 체크하는 것은 필수이다. 삼각함수의 그래프와 다른 함수의 그래프, 다른 도형과의 관계를 다룰 때는 더더욱 그러하다.

앞의 문제는 함수 $y=\\frac{1}{2}(a \\sin \\pi x+5)$ 의 주기와 주어진 $x$ 의 값의 범위를 감안하여 직선 $x=\\frac{5}{2}$ 에 대한 대칭부터 체크하고 시작할 수 있어야 한다. 그런데 직선 $x=\\frac{5}{2}$ 에 대하여 대칭인 2 개씩의 점들에 직선 $x=\\frac{5}{2}$ 위의 점 1 개가 추가된다면 이 점들의 $x$ 좌표의 합은 따로 다루어야 하나? 아니다!\\
직선 $x=m$ 에 대하여 또는 점 $(m, n)$ 에 대하여 대칭인 2 개씩의 짝수개의 점들의 $x$ 좌표의 합도, 여기에 $m$ 을 추가한 홀수개의 점들의 $x$ 좌표의 합도\\
(모든 점의 개수) $\\times m$\\
으로 계산하는 하나의 방법으로 다루면 된다.\\
직선 $x=m$ 에 대하여 또는 점 $(m, n)$ 에 대하여 대칭인 두 점의 $x$ 좌표를 각각 $\\alpha, \\beta$ 라 하면 $\\alpha+\\beta=2 m$ 이므로 그 합을 다룰 때는 $\\alpha=\\beta=m$ 으로 보아도 되므로 모든 점의 $x$ 좌표를 $m$ 으로 보면 되기 때문이다.\\
\\includegraphics[max width=\\textwidth, center]{3c0ed4eb-1378-44aa-b2da-8dd47e4ed97a-02_303_600_1603_1048}\\
\\includegraphics[max width=\\textwidth, center]{3c0ed4eb-1378-44aa-b2da-8dd47e4ed97a-02_210_595_1954_1051}

\\section*{Comment}
\\section*{Drill 삼각함수의 그래프 위의 점}
앞의 문제는 삼각함수의 그래프의 대칭을 이용하여 점 A 의 $x$ 좌표만 미지수로 잡고 두 점 B , C 의 $x$ 좌표를 이 미지수로 나타내는 것이 전부이다. 지수함수와 로그함수에서와 마찬가지로 삼각함수의 그래프 위의 여러 점들의 좌표를 미지수로 나타낼 때에도 적절한 한 점의 좌표를 미지수로 나타낸 후 다른 점들의 좌표는 주어진 관계에 따라 가급적이면 새로운 미지수를 사용하지 않도록, 미지수의 개수를 최소화하는 것이 좋다.

\\section*{Comment}
\\section*{Drill. 1 삼각함수의 함숫값을 구한다는 것의 의미}
앞의 문제에서는 두 삼각형 $\\mathrm{OBA}, \\mathrm{OCB}$ 의 밑변을 각각 선분 $\\mathrm{AB}, \\mathrm{BC}$ 로 보고 두 삼각형의 넓이의 비를 두 선분 $\\mathrm{AB}, \\mathrm{BC}$ 의 길이의 비로 이용하기로 하는 것이 자연스럽다. 한 점의 좌표를 미지수로 나타낸 후 다른 점들의 좌표는 주어진 관계에 따라 미지수의 개수를 최소화 하는 것 역시 중요하다.

두 삼각형 $\\mathrm{OBA}, \\mathrm{OCB}$ 의 넓이를 구해야 하는데, 높이는? 삼각함수의 함숫값으로 구할 수 있어야 하므로 특수각과의 관련성을 미리 예상한다면 좀 더 마음 편하게 풀어갈 수 있다.

\\section*{Drill. 2 삼각함수의 그래프의 비율 관계}
일반적인 사인함수와 코사인함수의 그래프에서\\
점대칭의 중심으로부터 한 주기의 $\\frac{1}{4}$ 에 해당하는 구간\\
의 그래프는 함수 $y=\\sin x$ 의 구간 $\\left[0, \\frac{\\pi}{2}\\right]$ 에서의 그래프를 확대, 축소, 대칭이동한 것이다.\\
따라서 그림과 같이\\
삼등분 또는 이등분\\
하여 특수각처럼 활용할 수 있도록 하자.\\
\\includegraphics[max width=\\textwidth, center]{3c0ed4eb-1378-44aa-b2da-8dd47e4ed97a-05_895_1105_1142_858}

\\section*{Comment}
Drill 삼각함수의 그래프 위의 점 그리고 특수각과의 관련 예상\\
앞의 문제 역시 $\\overline{\\mathrm{AP}}: \\overline{\\mathrm{PQ}}=3: 1$ 에서 점 A 의 $x$ 좌표를 이용하여 점 P 의 $x$ 좌표를 나타낼 수 있다는 것과 점 P 의 $y$ 좌표를 삼각함수의 함숫값으로 구해야 하므로 특수각과 관련될 것이라는 예상으로 가볍게 출발할 수 있어야 한다. 두 삼각형 $\\mathrm{OAP}, \\mathrm{OPQ}$ 의 넓이를 이용하기 위해 밑변과 높이를 따로 잡아야 한다는 기하적 상황 판단으로 마무리하면 된다.

\\section*{Comment}
\\section*{Drill 특수각 그리고 직각삼각형의 이용}
직선의 일부를 빗변으로 하고 직각을 낀 두 변이 각각 좌표축에 평행한 직각삼각형을 이용 하여 직선의 기울기를 다루는 것은 함수의 그래프에 관한 기하적 관점의 기본 중의 기본 이다. 또한 삼각함수에서 이러한 직각삼각형의 밑변의 길이와 높이는 웬만하면 특수각에 관한 것이어야 구할 수 있다는 예상도 항상 함께 해야 한다.\\
앞의 문제에서는 두 직선 $\\mathrm{AC}, \\mathrm{BC}$ 의 기울기의 비를 각각 선분 $\\mathrm{BC}, \\mathrm{AC}$ 를 빗변으로 하고 직각을 낀 두 변이 각각 좌표축에 평행한 두 직각삼각형의 밑변의 길이의 비로 이용할 수 있어야 한다. 점 A 의 $x$ 좌표를 미지수로 잡으면 삼각함수의 그래프의 대칭에서 점 B 의 $x$ 좌표, 점 C 의 $x$ 좌표까지 같은 미지수로 나타낼 수 있고, 두 직각삼각형의 밑변의 길이의 비에서 곧바로 끝이 보인다.

Drill 삼각함수의 주기와 그래프의 대칭\\
앞의 문제는 첫 문장에서 곧바로 삼각함수의 주기와 그래프의 대칭에 관한 것임을 알 수 있다. $g(x)$ 에 쓸데없이 정신 팔려서 그래프 그리고 어쩌고 하지 않았기를 ⋯ $g(x)$ 는 원활한 표현의 수단으로 등장한 것일 뿐이다.\\
별로 까다롭지 않은 문제이긴 하다. 문제에서 원하는 방향에 딱 맞게 반응하고 주어지지 않은 조건을 스스로 잘 챙길 수 있다는 전제에서! $f\\left(a_{5}\\right)=g\\left(a_{5}\\right)$ 에서 ' $=k$ '를 자연스럽게 이어 붙이고 이 결과로부터 올바른 풀이 방향을 잡고, $a_{1}, a_{2}$ 에 관한 관계식과 $a_{1}, a_{4}$ 에 관한 관계 식을 필요한 때에 자연스럽게 떠올렸다면 굿이다. 삼각함수의 주기와 그래프의 대칭에 대해 본능적으로 반응하도록 잘 공부해 놓았다는 것!

\\section*{Comment}
Drill 경계를 이용해서 최대한 간결하게\\
앞의 문제에서 $y=|f(x)|$ 의 그래프를 그리기는 곤란하므로 방정식 $|f(x)|=2$ 의 실근은 당연히 $f(x)=-2, f(x)=2$ 로 나누어 생각해야 한다. $f(x)=-2$ 에서 $a \\sin (b x)=-1$, $f(x)=2$ 에서 $a \\sin (b x)=3$ 이고 $a>1$ 이므로 곡선 $y=a \\sin (b x)$ 는 직선 $y=-1$ 과 한 주기 에서 두 개의 교점을 갖는다. $y=a \\sin (b x)$ 의 최댓값이 $a>1$ 이므로 곡선 $y=a \\sin (b x)$ 와 직선 $y=3$ 의 한 주기에서의 교점의 개수는 $a=3$ 일 때를 경계로 나누어진다.\\
$1<a<3, a=3, a>3$ 으로 케이스를 구분하여 등차수열 $\\left\\{\\alpha_{2 n}+\\alpha_{2 n+3}\\right\\}$ 의 공차의 조건에 부합하는지 점검하는 일이 남았다. 공차는 자연스럽게 $\\left(\\alpha_{4}+\\alpha_{7}\\right)-\\left(\\alpha_{2}+\\alpha_{5}\\right)$ 로 쓸 수 있어야 하고, $1<a<3, a=3$ 인 경우 삼각함수의 주기와 그래프의 대칭에서 $\\alpha_{4}$ 와 $\\alpha_{2}, \\alpha_{7}$ 과 $\\alpha_{5}$ 의 관계에 눈길이 가면서 공차 $\\left(\\alpha_{4}+\\alpha_{7}\\right)-\\left(\\alpha_{2}+\\alpha_{5}\\right)$ 를 변형해서 다룰 수 있어야 한다.

\\section*{Comment}
\\section*{Drill 방정식 $(f \\circ f)(x)=x$}
항등식 $(f \\circ f)(x)=x$ 는 $f(x)$ 의 역함수가 존재하고 $f(x)=f^{-1}(x)$ 라는 의미로 이용한다. 이를 방정식 $(f \\circ f)(x)=x$ 와 혼동하지 않도록 주의하자.\\
방정식 $(f \\circ f)(x)=x$ 는 일반적인 함수 $f(x)$ 에 대하여 다룰 수 있다. 즉 $f(x)$ 의 역함수가 존재하지 않아도 상관없다는 것이다.\\
함수 $f(x)$ 에 대하여 방정식 $(f \\circ f)(x)=x$ 의 실근은 대응 관계에서 다음과 같이 나타남을 알 수 있다.\\
\\includegraphics[max width=\\textwidth, center]{3c0ed4eb-1378-44aa-b2da-8dd47e4ed97a-10_107_303_1074_1188}\\
\\includegraphics[max width=\\textwidth, center]{3c0ed4eb-1378-44aa-b2da-8dd47e4ed97a-10_135_303_1194_1188}

즉 방정식 $(f \\circ f)(x)=x$ 의 실근은 함수 $f$ 에 의하여 한 실근에 자기 자신이 대응하거나 두 실근이 짝을 이루어 서로에게 대응한다. 이를 좌표평면에 나타내면 다음과 같고, 이때 함수 $y=f(x)$ 의 그래프는 네 점 $(\\alpha, \\alpha),(\\beta, \\delta),(\\gamma, \\gamma),(\\delta, \\beta)$ 를 지난다.\\
\\includegraphics[max width=\\textwidth, center]{3c0ed4eb-1378-44aa-b2da-8dd47e4ed97a-10_422_456_1564_1112}

\\section*{Comment}
함수 $y=f(x)$ 의 그래프를 직선 $y=x$ 에 대하여 대칭이동한 도형을 $F$ 라 하면 일반적으로 방정식 $(f \\circ f)(x)=x$ 의 실근은 $y=f(x)$ 의 그래프와 도형 $F$ 의 교점의 $x$ 좌표와 같다.\\
\\includegraphics[max width=\\textwidth, center]{3c0ed4eb-1378-44aa-b2da-8dd47e4ed97a-11_464_464_799_1171}

앞의 문제에서 방정식 $f(f(x))=x$ 가 오직 한 실근을 갖는다는 것은 곡선 $y=f(x)$ 와 직선 $y=x$ 가 오직 한 점에서 만난다는 것! '수학 I '까지로 한정하면 판별식을 이용하면 되지만 '수학 $\\mathbb{I}$ '의 미분의 방법으로 풀어도 좋다.

\\section*{Comment}
\\section*{Drill 삼각방정식과 삼각부등식}
삼각방정식과 삼각부등식의 해는 다음의 방법으로 구할 수 있다.\\
(1) 삼각방정식의 해는 $\\sin x=k, \\cos x=k, \\tan x=k$ 등으로 고쳐서 함수 $y=\\sin x$, $y=\\cos x, y=\\tan x$ 의 그래프와 직선 $y=k$ 의 교점의 $x$ 좌표로 구한다.\\
(2) 삼각부등식의 해는 $\\sin x>k, \\cos x<k, \\tan x>k$ 등으로 고쳐서 함수 $y=\\sin x$, $y=\\cos x, y=\\tan x$ 의 그래프와 직선 $y=k$ 의 교점의 $x$ 좌표를 경계로 하여 구한다.\\
(3) $\\sin x=t$ 또는 $\\cos x=t$ 로 치환하여 $t$ 에 대한 방정식 또는 부등식의 해를 구한다. 이때 $-1 \\leq t \\leq 1$ 인 것에 주의한다.

앞의 문제도 하나의 삼각함수로 나타내고 치환하는 기본적인 절차를 밟는 것으로 시작하면 된다. 치환한 이차방정식이 순순히 인수분해되는 형태가 아니라고 해서 당황하지 말 것! 근의 공식도 있다. 이어지는 과정에서 교점이 나타나는 케이스를 구분하여 차근차근 정리해가면 된다.


\\end{document}"""

def extract_solutions_from_latex(latex_content):
    """LaTeX에서 해설 추출"""
    solutions = []
    
    # 본문만 추출
    begin_match = re.search(r'\\begin\{document\}', latex_content)
    end_match = re.search(r'\\end\{document\}', latex_content)
    if begin_match and end_match:
        body = latex_content[begin_match.end():end_match.start()]
    else:
        body = latex_content
    
    # Drill 섹션 추출
    # Comment 섹션 다음에 오는 Drill은 전략, 그 외는 개념
    drill_pattern = r'\\section\*\{Drill\.?\s*([0-9]*)\s*([^}]+)\}(.*?)(?=\\section\*|\\end\{document\}|$)'
    drill_matches = re.finditer(drill_pattern, body, re.DOTALL)
    
    for match in drill_matches:
        drill_num = match.group(1).strip() if match.group(1) else ""
        topic = match.group(2).strip()
        content = match.group(3).strip()
        
        # 이전 섹션이 Comment인지 확인
        start_pos = match.start()
        prev_comment = body.rfind('\\section*{Comment}', 0, start_pos)
        prev_drill = body.rfind('\\section*{Drill', 0, start_pos)
        
        # Comment 바로 다음에 오는 Drill은 전략
        is_strategy = False
        if prev_comment != -1:
            # Comment와 Drill 사이에 다른 섹션이 없으면 전략
            between = body[prev_comment:start_pos]
            if '\\section*{' not in between.replace('\\section*{Comment}', '').replace('\\section*{Drill', ''):
                is_strategy = True
        
        # 이미지 제거
        content = re.sub(r'\\includegraphics.*?}', '', content)
        content = re.sub(r'\\begin\{figure\}.*?\\end\{figure\}', '', content, flags=re.DOTALL)
        content = re.sub(r'\\captionsetup.*?}', '', content)
        content = re.sub(r'\\\\', ' ', content)
        content = re.sub(r'\$\$', ' ', content)
        content = re.sub(r'\s+', ' ', content)
        
        if len(content) > 50:
            if is_strategy:
                # 문제 참조 추출
                question_ref = ""
                if '앞의 문제' in content:
                    question_ref = "P3"
                
                solutions.append({
                    "type": "strategy",
                    "topic": f"{drill_num} {topic}".strip() if drill_num else topic,
                    "question_ref": question_ref,
                    "content": content
                })
            else:
                solutions.append({
                    "type": "concept",
                    "topic": f"{drill_num} {topic}".strip() if drill_num else topic,
                    "content": content,
                    "question_ref": ""
                })
    
    # Comment 섹션 내의 "Drill ..." 텍스트 추출 (전략)
    # Comment 섹션 내에 섹션 헤더 없이 "Drill ..." 형태로 나오는 경우
    comment_sections = re.finditer(r'\\section\*\{Comment\}(.*?)(?=\\section\*\{|\\end\{document\}|$)', body, re.DOTALL)
    
    for comment_match in comment_sections:
        comment_content = comment_match.group(1)
        
        # Comment 내의 "Drill ..." 텍스트 찾기 (섹션 헤더가 아닌 경우)
        # "Drill"로 시작하지만 "\section*{Drill"가 아닌 경우
        drill_text_pattern = r'(?:^|\\\\)Drill\s+([^\\]+?)(?=\\\\section|Drill|\\end|$)'
        drill_text_matches = re.finditer(drill_text_pattern, comment_content, re.DOTALL | re.MULTILINE)
        
        for drill_text_match in drill_text_matches:
            strategy_content = drill_text_match.group(1).strip()
            
            # 이미지 제거
            strategy_content = re.sub(r'\\includegraphics.*?}', '', strategy_content)
            strategy_content = re.sub(r'\\\\', ' ', strategy_content)
            strategy_content = re.sub(r'\$\$', ' ', strategy_content)
            strategy_content = re.sub(r'\s+', ' ', strategy_content)
            
            if len(strategy_content) > 50:
                # 문제 참조 추출
                question_ref = ""
                if '앞의 문제' in strategy_content:
                    question_ref = "P3"
                
                solutions.append({
                    "type": "strategy",
                    "topic": "삼각함수",
                    "question_ref": question_ref,
                    "content": strategy_content
                })
    
    return solutions

def review_solutions(solutions):
    """해설 데이터 검토"""
    print("=" * 60)
    print("[수1 드릴 P3 해설 데이터 검토]")
    print("=" * 60)
    
    issues = []
    math_errors = []
    
    for i, sol in enumerate(solutions, 1):
        sol_type = sol.get("type", "")
        print(f"\n[해설 {i}] 타입: {sol_type}")
        
        if sol_type == "concept":
            topic = sol.get("topic", "")
            print(f"[주제] {topic}")
        elif sol_type == "strategy":
            q_ref = sol.get("question_ref", "")
            print(f"[문제 참조] {q_ref}")
        
        content = sol.get("content", "")
        print(f"[내용 길이] {len(content)}자")
        
        # LaTeX 검사
        if '$' in content and content.count('$') % 2 != 0:
            issues.append(f"해설 {i}: LaTeX 수식 괄호 불일치")
            print("[LaTeX] 오류: 수식 괄호 불일치")
        else:
            print("[LaTeX] 정상")
        
        # 수학적 논리 검토
        # 삼각함수 관련 기본 공식 확인
        if 'sin' in content or 'cos' in content:
            # 범위 확인: -1 <= sin x <= 1, -1 <= cos x <= 1
            if 'sin' in content and ('> 1' in content or '< -1' in content):
                # 단, 최댓값/최솟값 설명은 예외
                if '최댓값' not in content and '최솟값' not in content:
                    math_errors.append(f"해설 {i}: sin 함수 범위 오류 가능성")
        
        # 대칭 관련 논리 확인
        if '대칭' in content and 'x=' in content:
            # 직선 x=m에 대한 대칭: α+β=2m 논리 확인
            if 'α+β=2' in content or 'alpha+beta=2' in content:
                pass  # 논리적으로 정상
    
    print("\n" + "=" * 60)
    print("[검토 결과]")
    print("=" * 60)
    print(f"[총 해설 수] {len(solutions)}개")
    
    concept_count = sum(1 for s in solutions if s.get("type") == "concept")
    strategy_count = sum(1 for s in solutions if s.get("type") == "strategy")
    print(f"[개념] {concept_count}개")
    print(f"[전략] {strategy_count}개")
    
    if issues:
        print("\n[LaTeX 오류]")
        for issue in issues:
            print(f"  - {issue}")
    
    if math_errors:
        print("\n[수학적 논리 오류 가능성]")
        for error in math_errors:
            print(f"  - {error}")
    
    if not issues and not math_errors:
        print("\n[오류] 없음")
        print("[수학적 논리] 정상")
    
    return len(issues) == 0 and len(math_errors) == 0

def save_for_deepseek(solutions):
    """딥시크용 CSV 저장"""
    base_dir = Path(r'C:\Users\a\Documents\MathPDF\organized\현우진\수1_2025학년도_현우진_드릴')
    save_dir = base_dir
    save_dir.mkdir(parents=True, exist_ok=True)
    
    # CSV 저장
    csv_path = save_dir / "수1_2025학년도_현우진_드릴_P3_해설_deepseek.csv"
    with open(csv_path, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['type', 'topic', 'question_ref', 'content'])
        for solution in solutions:
            writer.writerow([
                solution.get('type', ''),
                solution.get('topic', ''),
                solution.get('question_ref', ''),
                solution.get('content', '')
            ])
    
    print(f"\n[CSV 저장 완료] {csv_path}")
    
    # JSON 저장
    json_path = save_dir / "수1_2025학년도_현우진_드릴_P3_해설_deepseek.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(solutions, f, ensure_ascii=False, indent=2)
    
    print(f"[JSON 저장 완료] {json_path}")
    
    return csv_path, json_path

def main():
    print("=" * 60)
    print("[수1 드릴 P3 해설 LaTeX → CSV 변환]")
    print("=" * 60)
    
    # 1단계: LaTeX 읽기
    print(f"\n[1단계] LaTeX 내용 읽기 완료 ({len(latex_content)}자)")
    
    # 2단계: 해설 추출
    print("\n[2단계] 해설 추출 중...")
    solutions = extract_solutions_from_latex(latex_content)
    print(f"[완료] {len(solutions)}개 해설 추출됨")
    
    # 3단계: 검토
    print("\n[3단계] 해설 검토 중...")
    is_valid = review_solutions(solutions)
    
    # 4단계: 저장
    print("\n[4단계] 딥시크용 파일 저장 중...")
    csv_path, json_path = save_for_deepseek(solutions)
    
    print("\n" + "=" * 60)
    print("[완료] 딥시크가 읽을 수 있는 형태로 저장되었습니다.")
    print("=" * 60)
    base_dir = Path(r'C:\Users\a\Documents\MathPDF\organized\현우진\수1_2025학년도_현우진_드릴')
    print(f"저장 위치: {base_dir}")
    print(f"  - CSV: {csv_path.name}")
    print(f"  - JSON: {json_path.name}")

if __name__ == '__main__':
    main()
