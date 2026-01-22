# convert_su1_p2_solution_latex.py
# 수1 드릴 P2 해설 LaTeX를 딥시크용 CSV로 변환

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

\\newunicodechar{⋯}{\\ifmmode\\cdots\\else{$\\cdots$}\\fi}

\\begin{document}
\\captionsetup{singlelinecheck=false}
Drill $y=f(a x), a y=f(x)$ 의 그래프\\
(1) $y=f(a x)$ 의 그래프 $\\Rightarrow x$ 대신 $a x$ 를 대입\\
$a>0$ 이면 $y=f(x)$ 의 그래프를 $y$ 축을 기준으로 $x$ 축의 방향으로 $\\frac{1}{a}$ 배한 것과 같고,\\
$a<0$ 이면 $y=f(x)$ 의 그래프를 $y$ 축에 대하여 대칭이동한 후 $x$ 축의 방향으로 $\\frac{1}{|a|}$ 배한 것과 같다.\\
(2) $a y=f(x)$ 의 그래프, 즉 $y=\\frac{1}{a} f(x)$ 의 그래프 $\\Rightarrow y$ 대신 $a y$ 를 대입\\
$a>0$ 이면 $y=f(x)$ 의 그래프를 $x$ 축을 기준으로 $y$ 축의 방향으로 $\\frac{1}{a}$ 배한 것과 같고,\\
$a<0$ 이면 $y=f(x)$ 의 그래프를 $x$ 축에 대하여 대칭이동한 후 $y$ 축의 방향으로 $\\frac{1}{|a|}$ 배한 것과 같다.\\
$y=a^{x}$ 과 $y=b^{x}$ 을 각각 $y=f(x)$ 와 $y=f\\left(\\log _{a} b \\times x\\right)$ 로 볼 수 있고,\\
$y=\\log _{a} x$ 와 $y=\\log _{b} x$ 를 각각 $y=f(x)$ 와 $y=\\log _{b} a \\times f(x)$,\\
즉 $y=f(x)$ 와 $\\log _{a} b \\times y=f(x)$ 로 볼 수 있다.

앞의 문제는 이러한 관점 없이도 해결할 수 있긴 하지만 곡선 $y=a^{2 x}$ 과 직선 $y=4 x$ 가 각각 곡선 $y=a^{x}$ 과 직선 $y=2 x$ 를 $y$ 축을 기준으로 $x$ 축의 방향으로 $\\frac{1}{2}$ 배한 것임을 알면 두 선분 $\\mathrm{AC}, \\mathrm{BD}$ 가 $x$ 축에 평행하다는 것, 직선 AD 의 기울기의 조건에서 삼각형 ADC 가 이등변 삼각형인 것을 파악하고 좀 더 가벼운 마음으로 풀어갈 수 있다.

\\section*{Drill 직각삼각형과 특수각 그리고 좌표축에 내린 수선}
지수함수와 로그함수의 그래프에 관한 문제에서는 삼각형, 원의 기본 성질과 특수한 기하적 상황 등을 제대로 이용하지 못하면 곤란해지는 경우가 많다. 앞의 문제에서도 직각이등변 삼각형의 등장에 주목해야 하고 또한 이와 연계하기 위해 좌표축 또는 좌표축에 평행한 직선에 적절히 수선을 내려 봐야 한다. 그저 계산만 한다면… 슬퍼진다. 지수함수와 로그함수의 그래프 위의 여러 점이 등장하면 언제든 좌표축 또는 좌표축에 평행한 직선에 수선을 내릴 마음의 준비를 하도록!

\\section*{Drill 평행이동의 이해}
도형 $F$ 를 $x$ 축의 방향으로 $m$ 만큼, $y$ 축의 방향으로 $n$ 만큼 평행이동한 도형을 $G$ 라 하자.\\
도형 $F$ 위의 점 P 가 도형 $G$ 위의 점 Q 로 옮겨지고, 도형 $F$ 위의 점 R 이 도형 $G$ 위의 점 S 로 옮겨질 때,\\
(1) 두 직선 PQ 와 RS 의 기울기는 $\\frac{n}{m}$ 으로 일정하다.\\
(2) 직각삼각형에서 $\\overline{\\mathrm{PQ}}=\\overline{\\mathrm{RS}}=\\sqrt{m^{2}+n^{2}}$\\
\\includegraphics[max width=\\textwidth, center]{2c5d93e2-5ebf-4fab-a449-00b7e61650ae-03_350_443_752_1476}

앞의 문제에서 가장 중요한 판단은 곡선 $y=\\log _{2}(x+1)+2$ 가 곡선 $y=\\log _{2} x$ 를 $x$ 축의 방향 으로 -1 만큼, $y$ 축의 방향으로 2 만큼 평행이동한 것이고 직선 $y=-2 x+k$ 의 기울기가 -2 이므로 $k$ 의 값에 관계없이 점 A 를 $x$ 축의 방향으로 -1 만큼, $y$ 축의 방향으로 2 만큼 평행 이동한 것이 점 B 라는 것이다. 삼각형 ABC 가 직각이등변삼각형이 되려면 점 C 는 점 B 를 어떻게 평행이동한 것인지 케이스를 두 가지로 구분하면 된다. 두 케이스는 두 점 $\\mathrm{B}, \\mathrm{C}$ 를 서로 맞바꾼 것일 뿐이라고 센스 있게 판단하면 한 케이스의 계산만으로 끝낼 수도 있다.

\\section*{Comment}
\\section*{Drill 직사각형, 직각삼각형의 꼭짓점의 좌표}
좌표평면의 직사각형, 직각삼각형의 꼭짓점의 좌표는 다음의 예와 같이 직각삼각형의 합동, 닮음을 이용하여 평행이동의 관계로 나타낼 수 있다.

\\begin{figure}[h]
\\begin{center}
  \\includegraphics[max width=\\textwidth]{2c5d93e2-5ebf-4fab-a449-00b7e61650ae-04_314_583_858_1048}
\\captionsetup{labelformat=empty}
\\caption{정사각형 / 직각이등변삼각형}
\\end{center}
\\end{figure}

\\begin{figure}[h]
\\begin{center}
  \\includegraphics[max width=\\textwidth]{2c5d93e2-5ebf-4fab-a449-00b7e61650ae-04_331_608_1279_1021}
\\captionsetup{labelformat=empty}
\\caption{직사각형 / 직각삼각형}
\\end{center}
\\end{figure}

앞의 문제에서는 직선 AC 의 기울기가 1 이고 $\\overline{\\mathrm{AC}}=4 \\sqrt{2}$ 라는 것에서 선분 AC 를 빗변으로 하는 직각이등변삼각형을 곧바로 그리고 시작해야 한다. 직선 AB 의 기울기가 $\\frac{1}{3}$ 인 것은 선분 AB 를 빗변으로 하는 직각삼각형의 남은 두 변의 길이의 비를 알려준 것이고, $\\overline{\\mathrm{AB}}=\\overline{\\mathrm{BC}}$ 에서 선분 BC 를 빗변으로 하는 직각삼각형의 남은 두 변의 길이의 비도 알 수 있다.\\
중학교 도형은 알아야 할 것은 제대로 알고 언제든 이용할 준비가 되어 있어야 한다.

\\section*{Comment}
\\section*{Drill 지수함수와 로그함수의 역함수 관계}
지수함수와 로그함수가 함께 등장할 때는 서로 역함수 관계인지 체크하는 것은 필수! 서로 역함수 관계라면 그래프가 직선 $y=x$ 에 대하여 대칭인 기하적 관점과 역함수의 성질을 이용할 준비 태세를 갖추어야 한다.\\
(1) 지수함수 $y=a^{x} \\stackrel{\\text { 역함수 }}{\\longleftrightarrow}$ 로그함수 $y=\\log _{a} x$\\
(2) 함수 $y=a^{x-m}+n \\stackrel{\\text { 역함수 }}{\\longleftrightarrow}$ 함수 $y=\\log _{a}(x-n)+m$

앞의 문제에서는 $\\overline{\\mathrm{AC}}: \\overline{\\mathrm{OB}}$ 를 $\\overline{\\mathrm{AC}}: \\overline{\\mathrm{OC}}$ 로 보고 원점 O 와 함께 한 직선 위에 있는 곡선 $y=a^{x}$ 위의 두 점 $\\mathrm{A}, \\mathrm{B}$ 의 좌표를 적절하게 미지수로 잡기 시작하면 갈 길이 훤히 보일 것이다.

\\section*{Comment}
\\section*{Drill 밑이 같은 지수함수와 로그함수}
밑이 같은 지수함수와 로그함수가 함께 등장할 때에는 서로 역함수 관계가 아니더라도 한 함수의 그래프를 어떤 이동에 의해 다른 함수의 그래프로 옮길 수 있는지 기하적 측면을 살펴 보는 것이 좋다.\\
앞의 문제에서 $y=g(x)$ 의 그래프를 $x$ 축의 방향으로 -1 만큼, $y$ 축의 방향으로 1 만큼 평행 이동하면 $y=f(x)$ 의 역함수의 그래프가 된다. 이때 점 B 를 함께 평행이동한 점과 $y=f(x)$ 의 그래프 위의 점 A 의 관계를 살피는 것이 가장 효율적인 방법이다.

\\section*{Drill 역함수를 이용해도 좋고 그저 그냥 좌표 계산도 좋고}
앞의 문제에서 $y=a^{x}$ 의 역함수인 $y=\\log _{a} x$ 로부터 곡선 $y=\\log _{a} x$ 를 $y$ 축의 방향으로 $-b$ 만큼 평행이동한 곡선 $y=\\log _{a} x-b$, 곡선 $y=\\log _{a} x-b$ 를 $x$ 축에 대하여 대칭이동한 곡선 $y=-\\log _{a} x+b$ 의 관계를 이용하기로 한다면 기하적 관점이 잘 잡혀있는 것.\\
또는 점 P 에서 직선 QR 에 수선을 내리고 선분 PQ 를 빗변으로 하는 직각이등변삼각형과 선분 PR 을 빗변으로 하는 직각삼각형에서 직선 PR 의 기울기 $\\frac{1}{3}$ 을 이용하여 세 점 $\\mathrm{P}, \\mathrm{R}$, Q 의 좌표를 그저 그냥 미지수로 잡고 계산하는 것도 괜찮다. 역함수에 관한 기하적 관점 없이도 상관없는데 뭘⋯ 하지 말고 스스로 떠올리지 못한 조금이라도 나은 방법이 있다면 쪽쭉 받아들여서 자기 것으로 만들어야 한다.

\\section*{Comment}
\\section*{Drill 원점을 중심으로 한 회전}
$x$ 축, $y$ 축, 직선 $y=x$, 직선 $y=-x$ 중 서로 다른 두 직선에 대한 두 번의 대칭이동은 원점을 중심으로 시계 방향으로 $90^{\\circ}, 180^{\\circ}, 270^{\\circ}$ 만큼 회전한 것과 같다.\\
점을 원점을 중심으로 회전한 예는 다음과 같다.\\
점 $\\mathrm{P}(m, n)$ 을 $x$ 축에 대하여 대칭이동한 후 $y$ 축에 대하여 대칭이동한 점 $\\mathrm{Q}(-m,-n)$ 은 점 P 를 원점을 중심으로 시계 방향으로 $180^{\\circ}$ 만큼 회전한 것과 같다.\\
점 $\\mathrm{P}(m, n)$ 을 직선 $y=x$ 에 대하여 대칭이동한 후 $x$ 축에 대하여 대칭이동한\\
점 $\\mathrm{R}(n,-m)$ 은 점 P 를 원점을 중심으로 시계 방향으로 $90^{\\circ}$ 만큼 회전한 것과 같다.\\
점 $\\mathrm{P}(m, n)$ 을 $y$ 축에 대하여 대칭이동한 후 직선 $y=-x$ 에 대하여 대칭이동한\\
점 $\\mathrm{S}(-n, m)$ 은 점 P 를 원점을 중심으로 시계 방향으로 $270^{\\circ}$ (시계 반대 방향으로 $90^{\\circ}$ )\\
만큼 회전한 것과 같다.

지수함수의 그래프를 원점을 중심으로 회전한 예는 다음과 같다.\\
$y=a^{x}$ 의 그래프를 $x$ 축에 대하여 대칭이동한 후 $y$ 축에 대하여 대칭이동한 $y=-a^{-x}$ 의 그래프는 $y=a^{x}$ 의 그래프를 원점을 중심으로 시계 방향으로 $180^{\\circ}$ 만큼 회전한 것과 같다.\\
$y=a^{x}$ 의 그래프를 직선 $y=x$ 에 대하여 대칭이동한 후 $x$ 축에 대하여 대칭이동한 $y=-\\log _{a} x$ 의 그래프는\\
\\includegraphics[max width=\\textwidth, center]{2c5d93e2-5ebf-4fab-a449-00b7e61650ae-08_403_466_1321_1459}\\
$y=a^{x}$ 의 그래프를 원점을 중심으로 시계 방향으로 $90^{\\circ}$ 만큼 회전한 것과 같다.\\
$y-a^{x}$ 의 그래프를 $y$ 축에 대하여 대칭이동한 후 직선 $y=-x$ 에 대하여 대칭이동한\\
$y=\\log _{a}(-x)$ 의 그래프는 $y=a^{x}$ 의 그래프를 원점을 중심으로 시계 방향으로 $270^{\\circ}$ (시계 반대 방향으로 $90^{\\circ}$ )만큼 회전한 것과 같다.\\
지수함수와 로그함수의 그래프를 원점을 중심으로 회전한 것은 그리 어렵지 않게 파악할 수 있으므로 밑이 같은 지수함수와 로그함수가 함께 등장할 때는 서로 역함수 관계인지 확인하는 것에 더해서 이러한 그래프의 회전까지 확인해보도록 하자.

\\section*{Drill 밑이 같은 지수함수와 로그함수의 기하적 관계}
앞의 문제에서 밑이 같은 지수함수와 로그함수가 등장하고 선분 AB 를 지름으로 하는 원과 두 곡선 $y=\\left(\\frac{1}{a}\\right)^{x}, y=\\log _{a}(a x+a)$ 가 모두 점 $(0,1)$ 을 지나는 것에서 뭔가 특별함을 느껴야 하지 않을까?\\
곡선 $y=\\log _{a}(a x+a)$ 는 곡선 $y=\\log _{a} x$ 를 평행이동한 것. 곡선 $y=\\log _{a} x$ 는 곡선 $y=\\left(\\frac{1}{a}\\right)^{x}$ 을 원점을 중심으로 시계 방향으로 $90^{\\circ}$ 만큼 회전한 것. 지수함수와 로그함수의 그래프를 다룰 때 당연히 주목해야 할 점 $(0,1)$, 점 $(1,0)$ 까지 쪽 살피다보면 세 점 $\\mathrm{A}, \\mathrm{B}$, $(0,1)$ 을 꼭짓점으로 하는 삼각형이 어떤 직각삼각형인지 쉽게 파악할 수 있다.\\
계산만 남았다. 경험만 충분하다면 이러한 기하적 상황이 한눈에 들어왔을 테고 확인하는 과정도 그리 어렵지 않았을 것!

\\section*{Comment}
\\section*{Drill 경계의 이용}
그래프의 변화 관찰의 기본은 적절한 경계를 이용하는 것.\\
앞의 문제에서는 확정된 함수 $y=\\left(\\frac{1}{2}\\right)^{x+4}-5$ 의 $x=-4$ 에서의 함숫값을 경계로 이용할 수 있어야 한다. 함수 $y=-\\log _{2}(x+5)+k$ 의 $x=-4$ 에서의 함숫값이 $k$ 인 것도 한눈에 들어 온다. 조건 (가)를 이용하려면 곡선 $y=-\\log _{2}(x+5)+k$ 의 $y$ 절편의 경계도 함께 고려해야 한다는 것과 $y=f(x)$ 의 그래프가 아닌 $y=|f(x)|$ 의 그래프를 다루는 것에 주의하면서 조건 (나)를 만족시키는 상태를 파악해가면 된다. 끝까지 경계의 이용!\\
지수함수와 로그함수에 관한 문제에서는 점근선, 증가와 감소, 위로 볼록과 아래로 볼록 등의 그래프의 특징을 잘 알고 상황에 맞게 유연하게 적용할 수 있어야 하고, 점근선의 움직임도 중요한 판단 근거가 되는 경우가 많다. 다음의 기출 문제를 확인해두자.

\\section*{Chapter 1 지수함수와 로그함수}
\\section*{2024학년도 9월 평가원 공통 14번}
두 자연수 $a, b$ 에 대하여 함수

$$
f(x)= \\begin{cases}2^{x+a}+b & (x \\leq-8) \\\\ -3^{x-3}+8 & (x>-8)\\end{cases}
$$

이 다음 조건을 만족시킬 때, $a+b$ 의 값은? [4점]

집합 $\\{f(x) \\mid x \\leq k\\}$ 의 원소 중 정수인 것의 개수가 2 가 되도록 하는 모든 실수 $k$ 의 값의 범위는 $3 \\leq k<4$ 이다.\\
(1) 11\\
(2) 13\\
(3) 15\\
(4) 17\\
(5) 19

답 (2)

\\section*{2024학년도 수능 공통 21번}
양수 $a$ 에 대하여 $x \\geq-1$ 에서 정의된 함수 $f(x)$ 는

$$
f(x)= \\begin{cases}-x^{2}+6 x & (-1 \\leq x<6) \\\\ a \\log _{4}(x-5) & (x \\geq 6)\\end{cases}
$$

이다. $t \\geq 0$ 인 실수 $t$ 에 대하여 닫힌구간 $[t-1, t+1]$ 에서의 $f(x)$ 의 최댓값을 $g(t)$ 라 하자. 구간 $[0, \\infty)$ 에서 함수 $g(t)$ 의 최솟값이 5 가 되도록 하는 양수 $a$ 의 최솟값을 구하시오. [4점]

답 10

\\section*{Comment}
\\section*{Drill 격자점을 경계로 이용}
다항함수，지수함수，로그함수，삼각함수 중 서로 다른 종류의 두 함수 $y=f(x), y=g(x)$ 의 그래프의 교점의 $x$ 좌표，즉 방정식 $f(x)=g(x)$ 의 실근을 구하는 일반적인 방법은 없다． 그럼에도 불구하고 이들 함수 사이의 관계가 자주 다루어진다．이때는 그래프에서 적절한 격자점을 경계로 이용하는 방법을 우선 고려해야 한다．그러나 무조건 그래프를 그려서 그림으로 해결한다는 고정관념도 위험하다는 기！어느 정도 식을 이용한 계산이 필요할 수도 있고 식을 이용한 계산이 더 유리할 수도 있다．빠르게 판단하고 최소한의 시행착오로 효율 적인 방향을 잡을 수 있도록 충분히 연습하자．

앞의 문제의 가장 중요한 출발점은 세 곡선 $y=\\log _{2} x, y=\\left(\\frac{1}{2}\\right)^{x}, y=-2^{x}$ 사이의 특별한 기하적 관계를 자연스럽게 인식하고 좌표가 명확한 점 $\\left(1, \\frac{1}{2}\\right)$ 을 경계로 이용하기로 하는 것．

\\section*{2024학년도 6월 평기원 공통 21번}
실수 $t$ 에 대하여 두 곡선 $y=t-\\log _{2} x$ 와 $y=2^{x-t}$ 이 만나는 점의 $x$ 좌표를 $f(t)$ 라 하자．\\
〈보기〉의 각 명제에 대하여 다음 규칙에 따라 $A, B, C$ 의 값을 정할 때，$A+B+C$ 의 값을 구하시오．\\
（단，$A+B+C \\neq 0$ ）［4점］\\
－명제 ㄱㅇㅣ 참이면 $A=100$ ，거짓이면 $A=0$ 이다．\\
－명제 ㄴㅇㅣ 참이면 $B=10$ ，거짓이면 $B=0$ 이다．\\
－명제 ᄃ이 참이면 $C=1, \\quad$ 거짓이면 $C=0$ 이다．\\
〈보기〉\\
ㄱ．$f(1)=1$ 이고 $f(2)=2$ 이다．\\
ᄂ．실수 $t$ 의 값이 증가하면 $f(t)$ 의 값도 증가한다．\\
ᄃ．모든 양의 실수 $t$ 에 대하여 $f(t) \\geq t$ 이다．


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
    
    # Drill 섹션 추출 (개념)
    drill_pattern = r'\\section\*\{Drill ([^}]+)\}(.*?)(?=\\section\*|\\end\{document\}|$)'
    drill_matches = re.finditer(drill_pattern, body, re.DOTALL)
    
    for i, match in enumerate(drill_matches, 1):
        topic = match.group(1).strip()
        content = match.group(2).strip()
        
        # 이미지 제거
        content = re.sub(r'\\includegraphics.*?}', '', content)
        content = re.sub(r'\\begin\{figure\}.*?\\end\{figure\}', '', content, flags=re.DOTALL)
        content = re.sub(r'\\\\', ' ', content)
        content = re.sub(r'\s+', ' ', content)
        
        if len(content) > 50:  # 최소 길이 확인
            solutions.append({
                "type": "concept",
                "topic": topic,
                "content": content,
                "question_ref": ""
            })
    
    # 기출 문제 추출
    problem_pattern = r'\\section\*\{([0-9]{4}학년도[^}]+)\}(.*?)(?=\\section\*|\\end\{document\}|$)'
    problem_matches = re.finditer(problem_pattern, body, re.DOTALL)
    
    for match in problem_matches:
        problem_id = match.group(1).strip()
        content = match.group(2).strip()
        
        # 답 추출
        answer_match = re.search(r'답\s*\(?([0-9]+)\)?', content)
        answer = answer_match.group(1) if answer_match else ""
        
        # 문제 내용 정리
        content = re.sub(r'\\includegraphics.*?}', '', content)
        content = re.sub(r'\\\\', ' ', content)
        content = re.sub(r'\s+', ' ', content)
        
        if len(content) > 50:
            solutions.append({
                "type": "problem",
                "topic": "지수함수와 로그함수",
                "question_ref": problem_id,
                "content": content,
                "answer": answer
            })
    
    return solutions

def review_solutions(solutions):
    """해설 데이터 검토"""
    print("=" * 60)
    print("[수1 드릴 P2 해설 데이터 검토]")
    print("=" * 60)
    
    issues = []
    
    for i, sol in enumerate(solutions, 1):
        sol_type = sol.get("type", "")
        print(f"\n[해설 {i}] 타입: {sol_type}")
        
        if sol_type == "concept":
            topic = sol.get("topic", "")
            print(f"[주제] {topic}")
        elif sol_type == "problem":
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
    
    print("\n" + "=" * 60)
    print("[검토 결과]")
    print("=" * 60)
    print(f"[총 해설 수] {len(solutions)}개")
    
    concept_count = sum(1 for s in solutions if s.get("type") == "concept")
    problem_count = sum(1 for s in solutions if s.get("type") == "problem")
    print(f"[개념] {concept_count}개")
    print(f"[기출 문제] {problem_count}개")
    
    if issues:
        print("\n[오류]")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("\n[오류] 없음")
    
    return len(issues) == 0

def save_for_deepseek(solutions):
    """딥시크용 CSV 저장"""
    base_dir = Path(r'C:\Users\a\Documents\MathPDF\organized\현우진\수1_2025학년도_현우진_드릴')
    save_dir = base_dir
    save_dir.mkdir(parents=True, exist_ok=True)
    
    # CSV 저장
    csv_path = save_dir / "수1_2025학년도_현우진_드릴_P2_해설_deepseek.csv"
    with open(csv_path, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['type', 'topic', 'question_ref', 'content', 'answer'])
        for solution in solutions:
            writer.writerow([
                solution.get('type', ''),
                solution.get('topic', ''),
                solution.get('question_ref', ''),
                solution.get('content', ''),
                solution.get('answer', '')
            ])
    
    print(f"\n[CSV 저장 완료] {csv_path}")
    
    # JSON 저장
    json_path = save_dir / "수1_2025학년도_현우진_드릴_P2_해설_deepseek.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(solutions, f, ensure_ascii=False, indent=2)
    
    print(f"[JSON 저장 완료] {json_path}")
    
    return csv_path, json_path

def main():
    print("=" * 60)
    print("[수1 드릴 P2 해설 LaTeX → CSV 변환]")
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
    print(f"저장 위치: {base_dir}")
    print(f"  - CSV: {csv_path.name}")
    print(f"  - JSON: {json_path.name}")

if __name__ == '__main__':
    main()
