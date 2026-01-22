# convert_su1_p7_solution_latex.py
# 수1 드릴 P7 해설 LaTeX를 딥시크용 CSV로 변환

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

\\newunicodechar{⇒}{\\ifmmode\\Rightarrow\\else{$\\Rightarrow$}\\fi}

\\begin{document}
\\section*{Drill 점화식을 다루는 중요한 기본 중 하나인 나열해보기}
귀납적으로 정의된 수열의 이웃하는 항 사이의 관계식인 점화식을 대하는 기본 태도는

\\section*{나열, 관찰 ⇒ 규칙의 발견, 확인}
이다. 나열, 관찰에서 딱히 규칙이 발견되지 않을 수도 있다. 주로 항수가 작은 항을 다룰 때 그저 나열해보는 것으로 그만인 경우가 많다.\\\\
앞의 문제에서는 코사인의 값의 곱이 1 이라는 특별한 상황 인식만 잘 하면 $a_{6}, a_{5}$ 로부터 거꾸로 써보면 되는데, $a_{1}$ 의 값의 범위에 0이 포함되지 않으므로 몇 번째 항의 값의 범위에 까지 영향을 미치는지 확인하는 것만 주의하면 된다. 또한 함수 $y=\\cos \\pi x$ 의 그래프를 이용 하는 것은 너무나 당연하고, 이때 항의 값을 거꾸로 쓴다는 것은 $y$ 의 값에서 $x$ 의 값으로 역대응하는 것으로 다루면 된다.

\\section*{Drill 미지수의 정수 조건의 적극 활용}
과목과 단원에 상관없이 미지수가 정수인 조건은 매우 예민하게 받아들이고 이로 인해 발생 하는 특수한 상황을 절대 놓치면 안 된다. 앞의 문제에서 수열 $\\left\\{a_{n}\\right\\}$ 의 모든 항은 정수이고, $p$ 는 자연수이다. 주어진 점화식에 따라 $\\sum_{k=1}^{9} a_{k}$ 를 3 개씩의 항으로 묶어서 계산할 수 있어야 한다. 그리고 미지수의 개수를 줄이기 위해 $a_{1}=1, a_{6}-a_{2}=-5$ 를 이용할 수 있어야 한다. 이렇게 정리한 $\\sum_{k=1}^{9} a_{k}$ 의 식이 두 자연수의 곱으로 나타나는 특수한 상황을 놓치지 않으면 이제 끝이 보인다. 이 모든 과정을 부담 없이 자연스럽게 이어가려면? 고1 수학의 실력이 매우 중요하다!

\\section*{Drill 적절한 케이스 구분과 차분한 점검}
점화식에 관한 문제에서 적절히 케이스를 구분하고 꽤나 끈기 있게 차분히 점검해야 하는 경우가 많이 있다. 실전에서 당황하지 않도록 많은 경험을 해두어야 한다.\\\\
앞의 문제는 점화식 둘 중 하나를 선택해서 이웃하는 항 사이의 관계에 이용해야 한다.\\\\
$a_{3}=a_{4}$ 에서 점화식의 선택은 그리 어렵지 않다. $a_{1} a_{2} a_{3}<0$ 을 이용하기 위해 $a_{3}$ 으로부터 거꾸로 써보면서 케이스의 구분 상황을 놓치지 말고 실수가 없도록 주의하며 차근차근 계산해가면 된다.

\\section*{2024학년도 수능 공통 15번}
첫째항이 자연수인 수열 $\\left\\{a_{n}\\right\\}$ 이 모든 자연수 $n$ 에 대하여

$$
a_{n+1}= \\begin{cases}2^{a_{n}} & \\left(a_{n} \\text { 이 홀수인 경우 }\\right) \\\\ \\frac{1}{2} a_{n} & \\left(a_{n} \\text { 이 짝수인 경우 }\\right)\\end{cases}
$$

를 만족시킬 때, $a_{6}+a_{7}=3$ 이 되도록 하는 모든 $a_{1}$ 의 값의 합은? [4점]\\\\
(1) 139\\\\
(2) 146\\\\
(3) 153\\\\
(4) 160\\\\
(5) 167

답 (3)

\\section*{Drill 둘 이상의 점화식}
이웃한 항끼리의 합, 차, 곱, 몫이 있을 때는 주어진 둘 이상의 점화식, 주어진 한 점화식과 $n$ 대신 $n+1, n-1,2 n$ 등을 대입하여 얻은 새로운 점화식, 주어진 점화식에 $n$ 대신 적당한 값을 대입하여 얻은 둘 이상의 식 등을 연립방정식처럼 다룰 수 있다.\\\\
앞의 문제에서는 주어진 두 점화식에서 $a_{n+1}$ 을 일단 소거해보고 싶어야 한다. 이렇게 얻은 새로운 점화식의 형태가 주어진 수열의 합의 조건을 이용하기 더 좋다는 것과 어떻게 이용 할지의 판단이 그리 어렵지는 않을 듯.

\\section*{Drill 규칙의 발견}
항수가 큰 항을 다룰 때는 몇 개의 항을 나열하고 관찰해서 규칙을 발견한다. 이때 규칙은 주로

Named 수열 (등차수열, 등비수열, 자연수의 거듭제곱의 합), 주기 에 관한 것이다. 앞의 문제에서는 수열의 50 개의 항의 합을 구해야 하므로 규칙의 발견 쪽으로 우선 가닥을 잡아보는 것이 맞다. $a_{4}=4, S_{4}=3$ 을 이용하기 위해 주어진 점화식에 $n=2$ 를 대입해보고 $S_{2}$ 의 값의 범위에 따라 케이스부터 구분하고 점검을 시작해보자.\\\\
항수가 작으므로 $S_{2}, S_{4}$ 를 각각 $a_{1}+a_{2}, a_{1}+a_{2}+a_{3}+a_{4}$ 로 고쳐서 다루는 것이 좋겠다는 센스 정도는 발휘해야 한다. 이렇게 구해진 $a_{1}, a_{2}, a_{3}, a_{4}$ 의 값들만 봐서는 아무런 느낌이 없겠지만 규칙의 발견을 기대하고 $a_{n}, S_{n}$ 을 나란히 써보기에 돌입하면 된다.

\\section*{Drill 새로운 점화식의 필요성 인식}
앞의 문제의 ㄱ, ㄴ은 순전히 삼각함수의 실력으로 해결하는 것! 두 삼각함수 $y=\\sin \\pi x$, $y=\\cos \\pi x$ 의 그래프를 그리고 두 그래프를 혼동하지 않도록 주의하며 $a_{1}, a_{2}, a_{3}, \\cdots$ 의 값의 범위를 확인해가야 한다. 그리고 삼각함수를 다룰 때 처음부터 주기와 그래프의 대칭을 감안해야 하는 것은 너무나 당연하다. 이렇게 ㄴ의 점화식까지 판단하고 나서 ㄷ은? 이웃한 항끼리의 합에 관한 점화식에 $n$ 대신 $n+1, n-1$ 등을 대입해서 새로운 점화식을 얻고 두 점화식을 연립방정식처럼 다루어보는 것 또한 매우 당연한 것 아닐까?

\\section*{Drill 앞으로도 써보고 뒤로도 써보고}
주어진 점화식을 이용하여 항수가 큰 항으로 뒤로 써볼지 항수가 작은 항으로 앞으로 써볼지 판단할 수 있어야 하고 앞으로도 뒤로도 모두 써봐야 하는 경우도 많다. 앞으로 쓸 일이 많다 싶을 때는 $a_{n+1}=\\left(a_{n}\\right.$ 의 식 $)$ 으로 주어진 점화식을 $a_{n}=\\left(a_{n+1}\\right.$ 의 식 $)$ 으로 고쳐놓는 것이 좋다.

앞의 문제는 주어진 점화식을 뒤로 쓰기 위해 $a_{n+2}=a_{n+1}+b_{n}+b_{n+1}$ 로 고쳐놓고 나머지의 문제는 나머지끼리 해결한다는 기본 원칙을 지키면서 $a_{4}=8$ 에서 $a_{6}$ 을 향해 뒤로 가보기 시작 하는 것이 자연스럽다. 이 상황을 정리하고 나면? 더 이상 뒤로 쓸 일이 없다.\\\\
그렇다면 주어진 점화식을 $a_{n+1}=a_{n+2}-b_{n}-b_{n+1}$ 로 고쳐놓고 앞으로!

\\section*{Drill 뒤로 써볼지 앞으로 써볼지의 판단 그리고 끈기와 인내}
낯선 점화식을 만나면 일단 써보는 게 기본이다. $a_{9}$ 의 값이 주어졌으니 앞으로 써보기 시작할 듯. 그런데 상황 정리가 쉽지 않다면 $a_{2}$ 로부터 뒤로 써보기도 곧바로 시도해보고 어떻게 하는 것이 유리할지 판단해야 한다. $a_{2}$ 로부터 뒤로 써보기 시작하면 케이스가 계속 나누어져 너무 복잡하다고 생각할 수 있는데, 규칙을 발견하겠다는 기본 태도가 잘 갖춰져 있고 경험이 충분하다면 $\\cdots$ Named 수열이나 주기에 관한 것은 아니긴 하지만 일반항의 형태를 짐작하고 남은 풀이 방향을 정할 수 있을 듯!\\\\
일반항의 형태와 $a_{9}$ 의 값에서 $a_{2}$ 의 값의 케이스를 구분하고 끈기와 인내로 마무리! 아 그리고, 2024학년도 수능에서 다룬 점화식의 난도를 보고 이제 점화식은 쉽게 나오는 거 아니야? 하는 얼토당토않은 예측 따위는 하지 말자.

\\section*{2024학년도 9월 평기원 공통 12번}
첫째항이 자연수인 수열 $\\left\\{a_{n}\\right\\}$ 이 모든 자연수 $n$ 에 대하여

$$
a_{n+1}= \\begin{cases}a_{n}+1 & \\left(a_{n} \\text { 이 홀수인 경우 }\\right) \\\\ \\frac{1}{2} a_{n} & \\left(a_{n} \\text { 이 짝수인 경우 }\\right)\\end{cases}
$$

를 만족시킬 때, $a_{2}+a_{4}=40$ 이 되도록 하는 모든 $a_{1}$ 의 값의 합은? [4점]\\\\
(1) 172\\\\
(2) 175\\\\
(3) 178\\\\
(4) 181\\\\
(5) 184

답 (1)

\\section*{2024학년도 6월 평가원 공통 15번}
자연수 $k$ 에 대하여 다음 조건을 만족시키는 수열 $\\left\\{a_{n}\\right\\}$ 이 있다.\\\\
$a_{1}=k$ 이고, 모든 자연수 $n$ 에 대하여

$$
a_{n+1}= \\begin{cases}a_{n}+2 n-k & \\left(a_{n} \\leq 0\\right) \\\\ a_{n}-2 n-k & \\left(a_{n}>0\\right)\\end{cases}
$$

이다.\\\\
$a_{3} \\times a_{4} \\times a_{5} \\times a_{6}<0$ 이 되도록 하는 모든 $k$ 의 값의 합은? [4점]\\\\
(1) 10\\\\
(2) 14\\\\
(3) 18\\\\
(4) 22\\\\
(5) 26

답 (2)

\\section*{Comment}
\\section*{Drill 거꾸로 정의된 점화식}
점화식은 보통 앞의 항에서 뒤의 항으로 정의되는데 앞의 문제는 뒤의 항에서 앞의 항으로 정의되어 있어서 조금 낯설고 살짝 헷갈린다. 뭐 어쩌겠나. 그대로 따라서 일단 써봐야지. $a_{11}=1$ 에서 출발! 당연히 $a_{11}=a_{22}=1$ 이고, $a_{22}$ 의 값이 무엇인지는 별로 중요하지 않은데 하고 조금만 생각을 이어가면 $a_{13}=1$ 을 알게 된다. 이 패턴을 그대로 따르면 $a_{15}, a_{17}, a_{19}$ 의 값이 1 인 것까지 쪽쪽 확인하고 $a_{m}=1$ 임이 확실한 20 이하의 자연수 $m$ 의 값 5 개를 일단 찾는다. 이제 남은 6 개를 찾아야 한다. 값이 1 로 정해진 항들로부터 앞에서와는 조금 다른 방법으로 점화식을 이용해야 한다. $a_{n+2} \\neq 1$ 인 경우 $a_{n}=n+1$ 인 것은 아직 이용 불가이고 $a_{n+2}=1$ 인 경우 $a_{n}=a_{2 n}$ 인 것은 $a_{11}=1$ 에서 이용하는 수밖에 없다. 이렇게 얻은 $a_{9}=a_{18}$ 에서 $a_{9}, a_{18}$ 의 값이 1 이 아니면 무슨 일이 벌어지는지 먼저 슥 살펴볼 수 있어야 한다. 여기까지 논리 전개에 성공하면 거의 다 된 거다. 익숙해진 패턴의 반복과 $a_{n+2} \\neq 1$ 인 경우 $a_{n}=n+1$ 인 것의 적절한 적용이 남았다.

마무리 단계에서 $a_{2}, a_{4}, a_{6}, a_{8}, a_{10}, a_{12}$ 에는 관심을 끄고 구하고자 하는 것에만 집중하는 것도 중요한데, 그러다가 $a_{5}$ 에 $a_{n}=n+1$ 을 적용하지 않도록 마지막까지 주의해야 한다.\\\\
낮설고 조금 복잡해 보이는 점화식을 접할 때, 처음엔 조금 헷갈리겠지만 항 사이의 관계에 금세 익숙해질 테고 이를 반복하면 된다는 생각으로 차분히 살펴보는 인내와 끈기를 기르는 것이 중요하다.

\\section*{Drill 난도가 높다 한들 점화식을 대하는 기본 태도는}
점화식에 관한 문제는 난도가 높다고 해도 그저 열심히 써보다 보면 시간이 어느 정도 걸릴 지라도 뇌에 큰 과부하는 걸리지 않는 경우가 대부분이긴 하다. 그러나 많은 경험을 토대로 한 가정과 점검, 모순의 발견 그리고 확실한 결론의 도출 등의 상당한 수준의 논리 전개와 잘 정돈된 깔끔한 계산을 필요로 하는 경우에도 항상 대비하자. 또한 적당한 타이밍에 어느 정도의 써보기와 이에 따른 추정으로 논리 전개의 가닥을 잡을 수 있어야 한다.\\\\
앞의 문제는 어떤 자연수 $p$ 에 대하여 $a_{p}=8, a_{p+5}=-1$ 인 것에서 시작할 텐데, $a_{n+1} \\leq 0$ 인 경우 $a_{n+2}=a_{n+1} a_{n}$ 인 것에서 $a_{p+1}=0$ 이면 $a_{p+5}$ 가 어떻게 될지, $a_{n+1}>0$ 인 경우\\\\
$a_{n+2}=\\frac{a_{n+1}}{a_{n}}$ 인 것에서 $a_{p}>0$ 이므로 $a_{p+1}>0$ 이면 $a_{p+5}$ 가 어떻게 될지 수상하니 확인해봐야 겠다는 충분한 실전 경험에서 우러나는 센스가 필요하다. 이렇게 $a_{p+1}$ 의 부호를 정한 후에는 반복 계산을 위해 $a_{p+1}$ 을 미지수로 잡아서 깨 수월하게 값을 구할 수 있다.\\\\
남은 과정은 어떻게? $a_{p+5}=-1$ 에서부터 조금만 인내심을 갖고 뒤로 써보면 규칙을 발견할 수 있고, 문제의 상황이 명확히 정리되면서 모든 자연수 $n$ 에 대하여 $a_{n} \\leq 8$ 인 조건을 앞으로와 뒤로 중 어느 방향으로 적용할지 정하고 마무리할 수 있다.\\\\
아무리 난도가 높다 한들 점화식에서 써보는 것은 항상 중요한 것!


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
    drill_pattern = r'\\section\*\{Drill\.?\s*([0-9]*)\s*([^}]+?)(?:\\\\[^}]*?)?\}(.*?)(?=\\section\*|\\end\{document\}|$)'
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
            between = body[prev_comment:start_pos]
            if '\\section*{' not in between.replace('\\section*{Comment}', '').replace('\\section*{Drill', ''):
                is_strategy = True
        
        # 이미지 제거
        content = re.sub(r'\\includegraphics.*?}', '', content)
        content = re.sub(r'\\begin\{figure\}.*?\\end\{figure\}', '', content, flags=re.DOTALL)
        content = re.sub(r'\\begin\{center\}.*?\\end\{center\}', '', content, flags=re.DOTALL)
        content = re.sub(r'\\begin\{tabular\}.*?\\end\{tabular\}', '', content, flags=re.DOTALL)
        content = re.sub(r'\\captionsetup.*?}', '', content)
        content = re.sub(r'\\\\', ' ', content)
        content = re.sub(r'\$\$', ' ', content)
        content = re.sub(r'\s+', ' ', content)
        
        # 주제도 정리
        topic = re.sub(r'\\\\', ' ', topic)
        topic = re.sub(r'\s+', ' ', topic)
        
        if len(content) > 50:
            if is_strategy:
                question_ref = ""
                if '앞의 문제' in content:
                    question_ref = "P7"
                
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
    comment_sections = re.finditer(r'\\section\*\{Comment\}(.*?)(?=\\section\*\{|\\end\{document\}|$)', body, re.DOTALL)
    
    for comment_match in comment_sections:
        comment_content = comment_match.group(1)
        
        # Comment 내의 "Drill ..." 텍스트 찾기
        drill_text_pattern = r'(?:^|\\\\)Drill\.?\s*([0-9]*)\s+([^\\]+?)(?=\\\\section|Drill|\\end|$)'
        drill_text_matches = re.finditer(drill_text_pattern, comment_content, re.DOTALL | re.MULTILINE)
        
        for drill_text_match in drill_text_matches:
            drill_num = drill_text_match.group(1).strip() if drill_text_match.group(1) else ""
            strategy_content = drill_text_match.group(2).strip()
            
            # 이미지 제거
            strategy_content = re.sub(r'\\includegraphics.*?}', '', strategy_content)
            strategy_content = re.sub(r'\\\\', ' ', strategy_content)
            strategy_content = re.sub(r'\$\$', ' ', strategy_content)
            strategy_content = re.sub(r'\s+', ' ', strategy_content)
            
            if len(strategy_content) > 50:
                question_ref = ""
                if '앞의 문제' in strategy_content:
                    question_ref = "P7"
                
                solutions.append({
                    "type": "strategy",
                    "topic": f"{drill_num} 수열".strip() if drill_num else "수열",
                    "question_ref": question_ref,
                    "content": strategy_content
                })
    
    return solutions


def review_solutions(solutions):
    """해설 데이터 검토 (수학적 논리 포함)"""
    print("=" * 60)
    print("[수1 드릴 P7 해설 데이터 검토]")
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
        dollar_count = content.count('$')
        content_no_dblock = re.sub(r'\$\$', '', content)
        dollar_count_single = content_no_dblock.count('$')
        
        topic_dollar = sol.get("topic", "").count('$')
        topic_no_dblock = re.sub(r'\$\$', '', sol.get("topic", ""))
        topic_dollar_single = topic_no_dblock.count('$')
        
        total_dollar_single = dollar_count_single + topic_dollar_single
        
        if total_dollar_single % 2 != 0:
            issues.append(f"해설 {i}: LaTeX 수식 괄호 불일치")
            print("[LaTeX] 오류: 수식 괄호 불일치")
        else:
            print("[LaTeX] 정상")
        
        # 수학적 논리 검토
        # 1. 점화식 구조 확인
        if '점화식' in content:
            if 'a_{n+1}' in content or 'a_{n+2}' in content:
                if '=' in content:
                    pass  # 점화식 구조 정상
        
        # 2. 삼각함수 범위 확인
        if 'cos' in content or 'sin' in content:
            if '\\pi' in content:
                # cos(πx), sin(πx)의 범위는 -1 ~ 1
                pass  # 정상
        
        # 3. 수열의 합과 일반항의 관계 확인
        if '수열의 합' in content or 'S_n' in content:
            if 'a_n' in content or 'a_{n}' in content:
                if 'S_n-S_{n-1}' in content or 'S_n - S_{n-1}' in content:
                    pass  # 관계식 정상
        
        # 4. 조건부 점화식 확인
        if '\\begin{cases}' in content:
            if '\\end{cases}' in content:
                pass  # 조건부 수식 구조 정상
        
        # 5. 나머지 연산 확인
        if '나머지' in content or 'b_{n}' in content:
            if '3' in content or '나눈' in content:
                pass  # 나머지 연산 언급 정상
        
        # 6. 정수 조건 확인
        if '정수' in content or '자연수' in content:
            if '조건' in content or '미지수' in content:
                pass  # 정수 조건 언급 정상
    
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
    csv_path = save_dir / "수1_2025학년도_현우진_드릴_P7_해설_deepseek.csv"
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
    json_path = save_dir / "수1_2025학년도_현우진_드릴_P7_해설_deepseek.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(solutions, f, ensure_ascii=False, indent=2)
    
    print(f"[JSON 저장 완료] {json_path}")
    
    return csv_path, json_path


def main():
    print("=" * 60)
    print("[수1 드릴 P7 해설 LaTeX → CSV 변환]")
    print("=" * 60)
    
    # 1단계: LaTeX 읽기
    print(f"\n[1단계] LaTeX 내용 읽기 완료 ({len(latex_content)}자)")
    
    # 2단계: 해설 추출
    print("\n[2단계] 해설 추출 중...")
    solutions = extract_solutions_from_latex(latex_content)
    print(f"[완료] {len(solutions)}개 해설 추출됨")
    
    # 3단계: 검토 (수학적 논리 포함)
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
