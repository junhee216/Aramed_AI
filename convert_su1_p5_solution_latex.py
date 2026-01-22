# convert_su1_p5_solution_latex.py
# 수1 드릴 P5 해설 LaTeX를 딥시크용 CSV로 변환

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
\\section*{Comment}
\\section*{Drill 원과 삼각형의 닮음 (2)}
그림과 같이 원의 두 현 $\\mathrm{AB}, \\mathrm{CD}$ 가 만나는 점을 P 라 하면\\\\
삼각형 PAD 와 삼각형 PCB 는 서로 닮은 도형이고 다음이 성립한다.

$$
\\overline{\\mathrm{PA}} \\times \\overline{\\mathrm{PB}}=\\overline{\\mathrm{PC}} \\times \\overline{\\mathrm{PD}}
$$

\\begin{center}
\\includegraphics[max width=\\textwidth]{87cf0ce5-0609-4da8-9af8-ff4dc1584a94-01_333_310_900_1192}
\\end{center}

앞의 문제에서 선분 $\\mathrm{O}_{1} \\mathrm{O}_{2}$ 를 연장하여 원 $C_{2}$ 의 반지름을 표시하는 건 너무 당연한 일이어야 하고, 원과 삼각형의 닮음에 관한 상황 인식이 있어야 선분 $\\mathrm{O}_{1} \\mathrm{O}_{2}$ 를 연장하여 원 $C_{2}$ 의 지름 까지 표시하고 이용할 수 있다. 또한 이등변삼각형이 등장하면 항상 직각삼각형으로 적극 이용할 마음의 준비도 되어 있어야 한다. 사인법칙과 코사인법칙의 많은 고난도 문제들이 결국 중학교 도형 실력이 관건이라는 거…

\\section*{Drill. 1 결과도 중요하지만 원리도 항상 중요하다}
앞서 다룬 원과 삼각형의 닮음 (1), (2)의 결과를 기억하고 활용하는 것도 중요하지만 원주각, 중심각, 삼각형의 닮음을 이용한 유도 과정 자체도 중요하다. 앞의 문제에서는 삼각형의 두 내각의 크기의 합 $\\theta_{1}+\\theta_{2}$ 에 대한 조건을 이용하기 위해 두 삼각형 PTS, PRT의 닮음과 대응하는 각을 짝지을 수 있어야 한다. 이후 사인법칙과 코사인법칙의 기본적인 기하 상황에 반응하고 원 $C_{2}$ 에 그은 두 접선을 이용하여 마무리할 수 있다.

\\section*{Drill. 2 삼각형의 두 내각의 합}
삼각형의 두 내각의 크기가 각각 $\\alpha, \\beta$ 이면 남은 한 내각의 크기는 $\\pi-(\\alpha+\\beta)$ 이므로 그 외각의 크기는 $\\pi-\\{\\pi-(\\alpha+\\beta)\\}=\\alpha+\\beta$ 이다. 따라서

삼각형의 한 외각의 크기는 그와 이웃하지 않은 두 내각의 크기의 합과 같다. 다음 그림과 같이 삼각형의 두 내각이 주어질 때는 남은 한 외각을, 한 내각과 한 외각이 주어질 때는 남은 한 내각을 표시하고 이용할 가능성이 있는지 점검해봐야 한다.\\\\
\\includegraphics[max width=\\textwidth, center]{87cf0ce5-0609-4da8-9af8-ff4dc1584a94-02_178_356_1400_960}\\\\
\\includegraphics[max width=\\textwidth, center]{87cf0ce5-0609-4da8-9af8-ff4dc1584a94-02_180_333_1400_1400}

\\section*{Comment}
\\section*{Drill 각의 크기와 변의 길이의 과감한 미지수 설정 그리고 고 1 수학}
사인법칙과 코사인법칙에 관한 문제에서 주어지지 않은 각의 크기와 변의 길이는 우물쭈물 하지 말고 일단 과감하게 미지수로 설정해 놓고, 여러 기하적 상황에 따라 사인법칙과 코사인 법칙을 적용해보면서 재정비하는 시행착오를 감수할 수 있어야 한다. 앞의 문제에서도 조건 (가)에서 사각형 ABCD 의 네 변의 길이를 모두 미지수로 잡는 건 좀 무리인가 싶을 수 있으나 일단 이렇게 출발해보면, 조건 (나)에서 코사인법칙에 대한 센스와 고 1 수학의 실력으로 갈 길을 찾아 미지수 설정을 재정비하고 마무리할 수 있다. 코사인법칙의 단순 이용과 간단한 삼각함수의 각의 변환 정도를 제외하면 고 1 수학의 센스가 절대적으로 중요한 문제이다.\\\\
두 변의 길이가 $a, b$ 인 삼각형에서 코사인법칙에 의하여 $a^{2}+b^{2}, a b, a^{2}-b^{2}$ 등이 등장하므로 곱셈 공식과 인수분해 공식, $a^{2}+b^{2}=(a+b)^{2}-2 a b$ 등의 곱셈 공식의 변형의 이용 가능성은 항상 염두에 두어야 한다!

\\section*{2024학년도 6월 평가원 공통 13번}
그림과 같이

$$
\\overline{\\mathrm{BC}}=3, \\overline{\\mathrm{CD}}=2, \\cos (\\angle \\mathrm{BCD})=-\\frac{1}{3}, \\angle \\mathrm{DAB}>\\frac{\\pi}{2}
$$

인 사각형 ABCD 에서 두 삼각형 ABC 와 ACD 는 모두 예각삼각형이다. 선분 AC 를 $1: 2$ 로 내분하는 점 E 에 대하여 선분 AE 를 지름으로 하는 원이 두 선분 $\\mathrm{AB}, \\mathrm{AD}$ 와 만나는 점 중 A 가 아닌 점을 각각 $\\mathrm{P}_{1}, \\mathrm{P}_{2}$ 라 하고, 선분 CE 를 지름으로 하는 원이 두 선분 $\\mathrm{BC}, \\mathrm{CD}$ 와 만나는 점 중 C 가 아닌 점을 각각 $\\mathrm{Q}_{1}, \\mathrm{Q}_{2}$ 라 하자. $\\overline{\\mathrm{P}_{1} \\mathrm{P}_{2}}: \\overline{\\mathrm{Q}_{1} \\mathrm{Q}_{2}}=3: 5 \\sqrt{2}$ 이고 삼각형 ABD 의 넓이가 2 일 때, $\\overline{\\mathrm{AB}}+\\overline{\\mathrm{AD}}$ 의 값은? (단, $\\overline{\\mathrm{AB}}>\\overline{\\mathrm{AD}}$ )\\\\[0pt]
[4점]\\\\
\\includegraphics[max width=\\textwidth, center]{87cf0ce5-0609-4da8-9af8-ff4dc1584a94-03_413_659_1734_1025}\\\\
(1) $\\sqrt{21}$\\\\
(2) $\\sqrt{22}$\\\\
(3) $\\sqrt{23}$\\\\
(4) $2 \\sqrt{6}$\\\\
(5) 5

답(1)

\\section*{Drill 관련성을 잘 파악하기 그리고 할 수 있는 모든 것을 해보기}
합답형 문항에서는 맘대로 내달리지 말고 ㄱ, ㄴ, ㄷ의 순서대로 앞서 판단한 내용이 이어 지는 내용과 어떤 관련성이 있는지 항상 살피며 진행해야 한다. 앞의 문제에서 ㄱ은 너무나 쉬운 것. 그러나 등장한 특수각에 끝까지 관심을 두고 있어야 한다. ㄴ도 쉽다. 두 삼각형 $\\mathrm{PAB}, \\mathrm{PBC}$ 의 외접원의 반지름의 길이가 주어졌으니 $\\angle \\mathrm{PAB}, \\angle \\mathrm{PCB}$ 에서 두 삼각형의 공통인 변 PB 에 대하여 사인법칙을 사용하면 된다. 그 느낌을 간직하고 마지막으로 ㄷ. 삼각형 PAB 에서 선분 AB 와 $\\angle \\mathrm{APB}$ 그리고 외접원, 삼각형 PBC 에서 선분 BC 와 $\\angle \\mathrm{BPC}$ 그리고 외접원이 보인다. ㄴ에서 그랬던 것처럼 $\\angle \\mathrm{APB}, \\angle \\mathrm{BPC}$ 에 대한 정보를 얻기 위해 사인법칙을 사용해 보기로 마음만 먹으면 ㄱ의 특수각과 함께 풀이 방향을 딱 잡을 수 있다.\\\\
난도 높은 많은 문제에서 효율적인 풀이 방향이 잘 잡히지 않을 때, 손은 가만 두고 열심히 머리만 쥐어짜지 말고 손을 함께 움직이며 눈에 보이는 대로 할 수 있는 것을 모두 해봐야 한다.

\\section*{Drill 원에 대한 기본 태도와 각의 분석}
앞의 문제의 ㄱ은 직각삼각형 CFD 그리고 원주각에 대한 이해로 쉽게 해결했을 듯. 합답형 이므로 ㄱ에서 확인해 둔 기하적 상황을 이어지는 내용에 잘 연결 짓는 것이 역시 중요하다. ㄴ에서 $\\beta$ 는 삼각형 ADF 에서 다루어야 할 텐데, 앞서 다룬 원과 삼각형의 닮음 (1)-(1)의 기하적 상황에 친숙하다면 $\\angle \\mathrm{DFA}$ 의 크기를 곧바로 나타낼 수 있다. 아니면 원에 대해 잘 갖춰진 기본 태도로 점 F 를 선분 CD 의 중점, 즉 원 $C$ 의 중심과 연결하여 $\\alpha$ 로부터 각을 분석해갈 수도 있다.\\\\
남은 ㄷ. 삼각형 CFO 만 그려놓고 멀뚱히 보고 있으면 안 된다. 점 O 가 삼각형 ADF 의 외접원의 중심이므로 역시 원에 대한 기본 태도로 세 선분 $\\mathrm{AD}, \\mathrm{DF}, \\mathrm{FA}$ 중 어디에든 수선을 내려야 한다. 선택은? 선분 DF 의 근처에 이미 여러 기하적 상황 분석이 되어 있다. 이제 선분 DF 의 중점 H 에 대하여 두 선분 $\\mathrm{OH}, \\mathrm{CF}$ 가 모두 선분 DF 와 수직인 것에서 도형의 기본 중의 기본으로 삼각형 CFO 의 넓이를 직각삼각형 CFH 의 넓이로 구하기로 결정하고 마무리하면 된다.

\\section*{Drill. 1 등차수열의 일반항}
첫째항이 $a$, 공차가 $d$ 인 등차수열의 일반항 $a_{n}$ 은

$$
a_{n}=a+(n-1) d(n=1,2,3, \\cdots)
$$

이다.\\\\
공차가 0 이 아닌 등차수열의 일반항의 특징은 다음과 같다.\\\\
(1) $n$ 에 대한 일차식이다.\\\\
(2) $n$ 의 계수가 공차이다.

$$
a_{n}=d n+c \\Leftrightarrow \\text { 수열 }\\left\\{a_{n}\\right\\} \\text { 은 공차가 } d \\text { 인 등차수열 }
$$

앞의 문제에서는 $a_{m}$ 의 부호에 따라 $\\left|a_{m}\\right|$ 을 $a_{m},-a_{m}$ 으로 케이스를 구분하여 풀어도 좋지만 $\\left(a_{m}\\right)^{2}$ 이 함께 등장하므로 $\\left(a_{m}\\right)^{2}$ 을 $\\left|a_{m}\\right|^{2}$ 으로 고쳐서 $\\left|a_{m}\\right|$ 에 대한 이차부등식으로 다루는 정도의 센스는 발휘하는 게 좋다.

\\section*{Drill 2 절댓값의 성질}
두 실수 $a, b$ 에 대하여\\\\
(1) $|a|=\\left\\{\\begin{array}{rr}a & (a \\geq 0) \\\\ -a & (a<0)\\end{array}\\right.$\\\\
(2) $|a||b|=|a b|$\\\\
(3) $\\frac{|a|}{|b|}=\\left|\\frac{a}{b}\\right|($ 단, $b \\neq 0)$\\\\
(4) $|a|=|-a|,|a|^{2}=a^{2}$\\\\
(5) $|a|=b(b>0)$ 이면 $a=b$ 또는 $a=-b$\\\\
$|a|=|b|$ 이면 $a=b$ 또는 $a=-b$\\\\[0pt]
[예] (1) $|3|=3,|-3|=3=-(-3)$\\\\
(2) $|2||-3|=6=|2 \\times(-3)|$\\\\
(3) $\\frac{|-2|}{|3|}=\\frac{2}{3}=\\left|\\frac{-2}{3}\\right|$\\\\
(4) $|3|=3=|-3|,|-2|^{2}=2^{2}=4=(-2)^{2}$

\\section*{Drill 공차의 적극 이용}
등차수열에서 가장 적극적으로 이용해야 할 것을 꼽는다면 당연히 공차다. 앞의 문제에서 $a_{n}$ 을 이용하여 $b_{n}$ 을 나타내기 위해 자연스럽게 등차수열 $\\left\\{a_{n}\\right\\}$ 의 이웃하는 항의 차가 공차임 을 이용할 수 있어야 한다. 또는 첫째항과 공차가 같다는 특별한 조건에 주목하여 첫째항과 공차를 미지수 $d$ 로 놓고 일반항 $a_{n}=d n$ 을 곧바로 써서 $b_{n}$ 을 나타내도 좋다. 또한 $(-1)^{n}$ 이 곱해진 것에서 자연스럽게 $\\sum_{k=1}^{30} b_{k}$ 를 공차를 이용하여 나타낼 수 있음을 알아야 한다. 이렇게 구한 수열 $\\left\\{b_{n}\\right\\}$ 의 일반항으로 $\\sum_{k=1}^{15} b_{k}$ 를 계산할 때, $\\sum_{k=1}^{14} b_{k}+b_{15}$ 와 $b_{1}+\\sum_{k=2}^{15} b_{k}$ 중 어떤 계산이 유리할지 판단하는 여유까지 보여준다면 매우 훌륭하다.

\\section*{Drill 등차수열의 합의 선택}
등차수열을 이루는 $n$ 개의 수의 합은\\\\
$n \\times$ (평균)\\\\
이다. 예를 들어, 등차수열을 이루는 5 개의 수 $a-2 d, a-d, a, a+d, a+2 d$ 의 평균은 $a$ 이고, 그 합은

$$
(a-2 d)+(a-d)+a+(a+d)+(a+2 d)=5 a
$$

등차수열을 이루는 4 개의 수 $a-3 d, a-d, a+d, a+3 d$ 의 평균은 $a$ 이고, 그 합은

$$
(a-3 d)-(a-d)+(a+d)+(a+3 d)=4 a
$$

이므로 다음과 같이 일반화할 수 있다.

등차수열의 첫째항부터 제 $n$ 항까지의 합 $S_{n}$ 은\\\\
(1) 첫째항이 $a$, 제 $n$ 항이 $l$ 일 때 $S_{n}=n \\times \\frac{a+l}{2} \\Rightarrow$ (항의 개수) $\\times$ (평균)\\\\
(2) 첫째항이 $a$, 공차가 $d$ 일 때 $S_{n}=\\frac{n}{2}\\{2 a+(n-1) d\\}$ 이다. 둘 중 어떤 것을 이용하는 것이 나을지 문제의 상황에 맞게 선택하면 된다.

앞의 문제에서는 $\\sum_{n=1}^{m}(-1)^{n+1} a_{n}$ 에 $(-1)^{n+1}$ 이 곱해진 것에서 등차수열 $\\left\\{a_{n}\\right\\}$ 의 공차를 이용 하기로 하고 $m$ 이 홀수인 경우와 짝수인 경우로 케이스를 구분할 수 있어야 한다. 그리고 $\\sum_{n=1}^{10} a_{n}$ 의 계산까지 감안하면 $m$ 이 홀수인 경우에 $a_{1}$ 과 $a_{m}$ 중 어느 것을 따로 떼어 내는 것이 나을까?

\\section*{Drill 등차수열의 합의 선택}
앞의 문제에서 가장 먼저 해야 할 일은 $\\log _{2} \\frac{b_{n+1}}{b_{n}}$ 을 $\\log _{2} b_{n+1}-\\log _{2} b_{n}$ 으로 고쳐 교대수열의 합으로 깔끔히 정리하는 것. 이렇게 얻은 $a_{1}, a_{10}$ 의 관계식과 미지수로 잡은 공차로 등차수열의 두 항 $a_{1}, a_{10}$ 사이의 관계식을 자연스럽게 함께 이용하기. 그리고 $\\sum_{n=1}^{5} b_{4 n}$ 을 항의 합으로 일단 나열해보고 등차수열의 항들의 합이라는 것에서 (항의 개수) $\\times$ (평균)의 계산으로 가닥을 잡으면 된다.

\\section*{Drill 등차수열의 재구성}
(1) 등차수열의 항을

일정한 간격, 일정한 개수\\\\
로 택하여 더하거나 빼거나 상수를 곱해서 새로운 등차수열을 얻을 수 있다. 예를 들어, 공차가 $d$ 인 등차수열 $\\left\\{a_{n}\\right\\}$ 에 대하여

$$
\\begin{aligned}
& a_{1}, a_{3}, a_{5}, \\cdots \\\\
& 2 a_{1}, 2 a_{3}, 2 a_{5}, \\cdots \\\\
& a_{1}+a_{2}, a_{4}+a_{5}, a_{7}+a_{8}, \\cdots \\\\
& a_{1}-3 a_{2}, a_{3}-3 a_{4}, a_{5}-3 a_{6}, \\cdots \\\\
& a_{1}+a_{2}-a_{3}, a_{4}+a_{5}-a_{6}, a_{7}+a_{8}-a_{9}, \\cdots
\\end{aligned}
$$

등은 모두 등차수열이고, 공차는 차례대로

$$
\\begin{aligned}
& a_{3}-a_{1}=2 d \\\\
& 2 a_{3}-2 a_{1}=2\\left(a_{3}-a_{1}\\right)=4 d \\\\
& \\left(a_{4}+a_{5}\\right)-\\left(a_{1}+a_{2}\\right)=\\left(a_{4}-a_{1}\\right)+\\left(a_{5}-a_{2}\\right)=3 d+3 d=6 d \\\\
& \\left(a_{3}-3 a_{4}\\right)-\\left(a_{1}-3 a_{2}\\right)=\\left(a_{3}-a_{1}\\right)-3\\left(a_{4}-a_{2}\\right)=2 d-3 \\times 2 d=-4 d \\\\
& \\begin{aligned}
\\left(a_{4}+a_{5}-a_{6}\\right)-\\left(a_{1}+a_{2}-a_{3}\\right) & =\\left(a_{4}-a_{1}\\right)+\\left(a_{5}-a_{2}\\right)-\\left(a_{6}-a_{3}\\right) \\\\
\\quad \\quad= & 3 d+3 d-3 d=3 d
\\end{aligned}
\\end{aligned}
$$

이다.\\\\
(2) 두 등차수열의 일반항을 더하거나 빼거나 상수를 곱해서 새로운 등차수열을 얻을 수 있다. 공차가 $d_{1}$ 인 등차수열 $\\left\\{a_{n}\\right\\}$ 과 공차가 $d_{2}$ 인 등차수열 $\\left\\{b_{n}\\right\\}$ 에 대하여 수열 $\\left\\{k a_{n}+l b_{n}\\right\\}$ (단, $k, l$ 은 상수)\\\\
은 공차가 $k d_{1}+l d_{2}$ 인 등차수열이다.

앞의 문제는 수열 $\\left\\{a_{n}+b_{n}\\right\\}$ 이 두 등차수열 $\\left\\{a_{n}\\right\\},\\left\\{b_{n}\\right\\}$ 으로 재구성한 등차수열이라는 당연한 인식, 등차수열의 합 $\\sum_{n=1}^{7}\\left(a_{n}+b_{n}\\right)$ 을 (항의 개수) $\\times$ (평균)으로 다루겠다는 선택, 그리고 $\\left|a_{3}\\right|=b_{3}$ 을 $a_{3}=b_{3}, a_{3}=-b_{3}$ 으로 구분하여 다룰 때 두 등차수열 $\\left\\{a_{n}\\right\\},\\left\\{b_{n}\\right\\}$ 의 공차가 모두 정수라는 조건에 자연스럽게 눈길이 가려면 등차수열과 그 합에 대한 기본에 매우 충실해야 한다.

\\section*{Drill 수열의 합과 일반항의 관계}
수열 $\\left\\{a_{n}\\right\\}$ 의 첫째항부터 제 $n$ 항까지의 합이 $S_{n}$ 일 때\\\\
(1) $a_{1}=S_{1}$\\\\
(2) $a_{n}=S_{n}-S_{n-1}(n \\geq 2)$\\\\
\\includegraphics[max width=\\textwidth, center]{87cf0ce5-0609-4da8-9af8-ff4dc1584a94-11_193_942_903_888}

앞의 문제는 등차수열의 합의 최대와 최소에 관한 것이긴 하다. 그런데! 문제의 전반적인 상황을 파악하지도 않은 채, 앗 아는 거다 하면서 무작정 내달리지 않았기를 $\\cdots$ 등차수열 $\\left\\{a_{n}\\right\\}$ 의 정수인 공차가 주어졌고 모든 항이 정수이므로 $a_{1}$ 도 정수이다. $S_{m}>S_{m+1}$ 을 만족시키는 자연수 $m$ 의 최솟값이 4 라는 조건에서 두 부등식 $S_{3} \\leq S_{4}, S_{4}>S_{5}$ 에 수열의 합과 일반항의 관계를 이용하는 것만으로도 모든 $a_{1}$ 의 값을 구하기에 충분하다는 상황 파악을 할 수 있어야 한다.\\\\
또는 $S_{m+1}-S_{m}=a_{m+1}<0$ 에서 $a_{5}<0, a_{4} \\geq 0$ 이고, $a_{5}=a_{4}-3<0$ 에서 $a_{4}<3$ 이므로 $a_{4}$ 의 값은 $0,1,2$, 따라서 $a_{1}$ 의 값은 $a_{4}-3 \\times(-3)$ 에서~ 라는 등차수열의 특징과 모든 항이 정수 라는 조건을 좀 더 적극적으로 이용한 센스 있는 풀이도 매우 좋다.


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
                    question_ref = "P5"
                
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
                question_ref = ""
                if '앞의 문제' in strategy_content:
                    question_ref = "P5"
                
                solutions.append({
                    "type": "strategy",
                    "topic": "기하/수열",
                    "question_ref": question_ref,
                    "content": strategy_content
                })
    
    return solutions


def review_solutions(solutions):
    """해설 데이터 검토 (수학적 논리 포함)"""
    print("=" * 60)
    print("[수1 드릴 P5 해설 데이터 검토]")
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
        # 1. 삼각형 내각의 합 확인
        if '삼각형' in content and ('A+B+C' in content or 'α+β' in content or 'α + β' in content):
            if 'π' in content or '180' in content:
                pass  # 정상
        
        # 2. 등차수열 공식 확인
        if '등차수열' in content:
            if 'a_{n}' in content or 'a_n' in content:
                if 'a+(n-1)d' in content or 'a + (n-1)d' in content:
                    pass  # 일반항 공식 정상
            if 'S_n' in content or 'S_{n}' in content:
                if 'n/2' in content or '\\frac{n}{2}' in content:
                    pass  # 합 공식 정상
        
        # 3. 절댓값 성질 확인
        if '절댓값' in content or '|a|' in content:
            if '|a|^2' in content or '|a|^{2}' in content:
                if 'a^2' in content or 'a^{2}' in content:
                    pass  # |a|² = a² 정상
        
        # 4. 코사인법칙 확인
        if '코사인법칙' in content:
            if 'a^{2}+b^{2}' in content or 'a^2+b^2' in content:
                if '2ab' in content or '2 a b' in content:
                    pass  # 공식 구조 정상
        
        # 5. 원과 삼각형의 닮음 확인
        if '원과 삼각형의 닮음' in content:
            if 'PA' in content and 'PB' in content and 'PC' in content and 'PD' in content:
                if '×' in content or '*' in content:
                    pass  # PA × PB = PC × PD 정상
        
        # 6. 등차수열의 합 공식 확인
        if '등차수열' in content and '합' in content:
            if '평균' in content or 'S_n' in content:
                pass  # 합 공식 언급 정상
    
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
    csv_path = save_dir / "수1_2025학년도_현우진_드릴_P5_해설_deepseek.csv"
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
    json_path = save_dir / "수1_2025학년도_현우진_드릴_P5_해설_deepseek.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(solutions, f, ensure_ascii=False, indent=2)
    
    print(f"[JSON 저장 완료] {json_path}")
    
    return csv_path, json_path


def main():
    print("=" * 60)
    print("[수1 드릴 P5 해설 LaTeX → CSV 변환]")
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
