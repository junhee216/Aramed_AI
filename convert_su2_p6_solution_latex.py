# convert_su2_p6_solution_latex.py
# 수2 드릴 P6 해설 LaTeX를 딥시크용 CSV로 변환

import re
import sys
import os
import json
from pathlib import Path
from latex_utils import extract_body, clean_latex_text

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
\\section*{Drill 우함수와 기함수의 미분과 적분}
$(\\text { 우함수 })^{\\prime}=($ 기함수 $),(\\text { 기함수 })^{\\prime}=($ 우함수 $)$

$$
\\int(\\text { 기함수 })=(\\text { 우함수 }), \\int(\\text { 우함수 }) \\neq(\\text { 기함수 })
$$

우함수 $f^{\\prime}(x)$ 에 대하여 $f(x)$ 를 기함수라고 단정할 수 없지만 그래프의 대칭성이 완전히 사라지는 것은 아니다. 함수 $y=f(x)$ 의 그래프는 점 $(0, f(0))$ 에 대하여 대칭이다. $f(0)=0$ 일 때, $f(x)$ 가 기함수가 되는 것이다.

앞의 문제에서 다항함수 $f(x)$ 는 기함수이므로 $f^{\\prime}(x)$ 는 우함수이다. 함수 $g(x)$ 가 미분가능 하므로 연결 지점인 $x=0$ 의 좌우의 $g^{\\prime}(x)$ 의 함숫값이 같아야 하고, $y=g^{\\prime}(x)$ 의 그래프는 $y=f^{\\prime}(x)$ 의 그래프를 $x$ 축에 대하여 대칭이동한 $y=-f^{\\prime}(x)$ 의 그래프와 $y=f^{\\prime}(x)$ 의\\\\
그래프의 연결이다. 그래프의 상황을 살짝만 떠올려보면 $f^{\\prime}(0)=0$ 임을 알 수 있다. $g^{\\prime}(x)$ 는 기함수이고 기함수를 적분한 $g(x)$ 는 확실히 우함수라는 것!\\\\
두 곡선 $y=f(x), y=g(x)$ 가 서로 만나지 않도록 그래프의 개형을 간단히 그리고 둘러싸인 부분의 넓이의 계산으로 마무리하면 된다.

\\section*{Drill. 1 이차함수와 넓이}
이차함수 $f(x)$ 에 대하여 곡선 $y=f(x)$ 위의 두 점 $\\mathrm{A}, \\mathrm{B}$ 의 $x$ 좌표가 각각 $\\alpha, \\beta(\\alpha \\neq \\beta)$ 일 때, 곡선 $y=f(x)$ 와 직선 AB 로 둘러싸인 부분의 넓이는 직선 $x=\\frac{\\alpha+\\beta}{2}$ 에 의하여 이등분된다.\\\\
\\includegraphics[max width=\\textwidth, center]{775fe3b4-ce19-4ec2-82de-69f83888df16-02_364_304_903_913}\\\\
\\includegraphics[max width=\\textwidth, center]{775fe3b4-ce19-4ec2-82de-69f83888df16-02_367_304_900_1361}

\\section*{Drill. 2 이차함수와 넓이 그리고 삼차함수의 그래프의 비율 관계}
삼차함수 $y=f(x)$ 의 그래프의 접선, 변곡점을 지나는 직선에 관한 비율 관계와 이차함수 $y=f^{\\prime}(x)$ 의 그래프와 $x$ 축으로 둘러싸인 부분의 넓이 사이의 관계는 그림과 같다.\\\\
\\includegraphics[max width=\\textwidth, center]{775fe3b4-ce19-4ec2-82de-69f83888df16-02_549_405_1526_1108}

\\section*{Comment}
\\section*{Drill 이차함수와 넓이}
(1) 이차함수 $y=a x^{2}+b x+c$ 의 그래프와 직선 $y=m x+n$ 의 교점의 $x$ 좌표를 $\\alpha, \\beta$ 라 하면 이차함수의 그래프와 직선으로 둘러싸인 부분의 넓이 $S$ 는

$$
\\begin{aligned}
S & =\\int_{\\alpha}^{\\beta}\\left|a x^{2}+b x+c-(m x+n)\\right| d x \\\\
& =\\left|\\frac{a}{6}(\\beta-\\alpha)^{3}\\right|
\\end{aligned}
$$

\\includegraphics[max width=\\textwidth, center]{775fe3b4-ce19-4ec2-82de-69f83888df16-03_350_528_744_1340}\\\\
(2) 두 이차함수 $y=a x^{2}+b x+c$,\\\\
$y=a^{\\prime} x^{2}+b^{\\prime} x+c^{\\prime}\\left(a \\neq a^{\\prime}\\right)$ 의 그래프의 교점의 $x$ 좌표를 $\\alpha, \\beta$ 라 하면 두 곡선으로 둘러싸인 부분의 넓이 $S$ 는

$$
\\begin{aligned}
S & =\\int_{\\alpha}^{\\beta}\\left|a x^{2}+b x+c-\\left(a^{\\prime} x^{2}+b^{\\prime} x+c^{\\prime}\\right)\\right| d x \\\\
& =\\left|\\frac{a-a^{\\prime}}{6}(\\beta-\\alpha)^{3}\\right|
\\end{aligned}
$$

\\begin{center}
\\includegraphics[max width=\\textwidth]{775fe3b4-ce19-4ec2-82de-69f83888df16-03_371_471_1129_1397}
\\end{center}

\\section*{Drill 이차함수와 넓이 그리고 넓이 사이의 관계}
이차함수, 삼차함수, 사차함수에 관한 넓이의 공식은 선택이 아니라 필수이다. 반드시 알아 두고 적극적으로 활용하도록 하자. 또한 두 부분의 넓이가 함께 등장할 때는 두 넓이 사이의 관계를 우선 파악해 봐야 한다. 앞의 문제에서도 $S_{1}, S_{2}$ 의 관계를 이차함수에 관한 넓이의 공식과 어떻게 연결 지을지 생각하기 시작하면 아주 쉽게 풀이 방향을 잡을 수 있다.

\\section*{Comment}
\\section*{Drill 삼차함수와 넓이}
(1) 삼차함수 $y=a(x-\\alpha)^{2}(x-\\beta)$ 의 그래프와 $x$ 축으로 둘러싸인 부분의 넓이 $S$ 는

$$
S=\\left|\\frac{a}{12}(\\beta-\\alpha)^{4}\\right|
$$

\\includegraphics[max width=\\textwidth, center]{775fe3b4-ce19-4ec2-82de-69f83888df16-05_323_365_898_926}\\\\
\\includegraphics[max width=\\textwidth, center]{775fe3b4-ce19-4ec2-82de-69f83888df16-05_321_367_900_1357}\\\\
(2) 최고차항의 계수가 $a$ 인 삼차함수 $y=f(x)$ 의 그래프와 차수가 2 이하인 다항함수 $y=g(x)$ 의 그래프가 $x$ 좌표가 $\\alpha$ 인 점에서 접하고 $x$ 좌표가 $\\beta$ 인 점에서 만날 때, 두 함수 $y=f(x), y=g(x)$ 의 그래프로 둘러싸인 부분의 넓이 $S$ 는

$$
S=\\left|\\frac{a}{12}(\\beta-\\alpha)^{4}\\right|
$$

이고, $y=g(x)$ 가 최고차항의 계수가 $a^{\\prime}\\left(a^{\\prime} \\neq a\\right)$ 인 삼차함수일 때, 두 함수 $y=f(x)$, $y=g(x)$ 의 그래프로 둘러싸인 부분의 넓이 $S$ 는

$$
S=\\left|\\frac{a-a^{\\prime}}{12}(\\beta-\\alpha)^{4}\\right|
$$

\\includegraphics[max width=\\textwidth, center]{775fe3b4-ce19-4ec2-82de-69f83888df16-05_358_417_1713_571}\\\\
\\includegraphics[max width=\\textwidth, center]{775fe3b4-ce19-4ec2-82de-69f83888df16-05_356_424_1713_1019}\\\\
\\includegraphics[max width=\\textwidth, center]{775fe3b4-ce19-4ec2-82de-69f83888df16-05_356_409_1713_1476}

앞의 문제에서 곡선 $y=g(x)$ 와 직선 $y=\\frac{x}{3}$ 로 둘러싸인 부분의 넓이는 모두 직선 $y=x$ 에 대하여 대칭이동한 곡선 $y=f(x)$ 와 직선 $y=3 x$ 로 둘러싸인 부분의 넓이로 계산해야 하고, 삼차함수에 관한 넓이이므로 넓이의 공식을 이용할 상황인지 우선 점검해 봐야 한다. 교점의 상태에 대한 점점이므로 인수정리와 조립제법을 이용한 $f(x)-3 x$ 의 인수분해로!

\\section*{Drill 삼차함수와 넓이}
삼차함수의 그래프의 변곡점에 관한 다음의 넓이의 공식도 기억하고 이를 이용할 상황인지 항상 점검해 보도록 하자.

최고차항의 계수가 $a$ 인 삼차함수 $y=f(x)$ 의 그래프의 변곡점의 $x$ 좌표가 $\\alpha$ 이고 점 $(\\alpha, f(\\alpha))$ 를 지나는 직선 $l$ 이 $y=f(x)$ 의 그래프와 $x$ 좌표가 $\\beta$ 인 점에서 만날 때, $y=f(x)$ 의 그래프와 직선 $l$ 로 둘러싸인 두 부분의 넓이는 서로 같고, 각각의 넓이 $S$ 는

$$
S=\\left|\\frac{a}{4}(\\beta-\\alpha)^{4}\\right|
$$

\\includegraphics[max width=\\textwidth, center]{775fe3b4-ce19-4ec2-82de-69f83888df16-06_339_346_1180_913}\\\\
\\includegraphics[max width=\\textwidth, center]{775fe3b4-ce19-4ec2-82de-69f83888df16-06_341_348_1180_1321}

\\section*{Comment}
\\section*{Drill. 1 그래프의 기하적 상황의 추정과 확인}
앞의 문제는 그래프의 기하적 상황의 추정과 확인의 방법으로 풀어가야 한다.\\\\
조건 (나)의 항등식을 $f(x+2)=-f(x)+4$ 로 고쳐서 $0 \\leq x<2$ 에서의 $y=f(x)$ 의 그래프를 $x$ 축에 대하여 대칭이동한 후 $x$ 축의 방향으로 2 만큼, $y$ 축의 방향으로 4 만큼 평행이동한 것이 $2 \\leq x<4$ 에서의 $y=f(x)$ 의 그래프이고, 이를 반복하면 $f(x)$ 가 주기를 갖는다는 것까지 쭉 알아낼 수 있어야 한다. 마무리 단계의 정적분의 계산도 $y=f(x)$ 의 그래프의 대칭과 주기의 특징을 이용하여 최대한 간단하게!

\\section*{Drill. 2 선대칭, 점대칭과 정적분}
그래프가 선대칭, 점대칭인 함수의 정적분은 보통 그래프를 이용하여 기하적으로 다루는 것이 편리하고, 이러한 의도를 가진 문제에 빠르게 반응하는 것이 중요한 경우가 많다.

\\begin{figure}[h]
\\begin{center}
  \\includegraphics[max width=\\textwidth]{775fe3b4-ce19-4ec2-82de-69f83888df16-07_309_392_1309_850}
\\captionsetup{labelformat=empty}
\\caption{선대칭}
\\end{center}
\\end{figure}

\\begin{figure}[h]
\\begin{center}
  \\includegraphics[max width=\\textwidth]{775fe3b4-ce19-4ec2-82de-69f83888df16-07_329_393_1298_1323}
\\captionsetup{labelformat=empty}
\\caption{점대칭}
\\end{center}
\\end{figure}

특히 점대칭의 경우 함수 $y=f(x)$ 의 그래프가 점 $(a, b)$ 에 대하여 대칭일 때 항상

$$
\\int_{a-p}^{a+p} f(x) d x=2 p \\times b
$$

이다. 기하적으로는 그림과 같이 가로의 길이가 $2 p$, 세로의 길이가 $|b|$ 인 $x$ 축에 한 변이 놓인 직사각형의 넓이에서 $b$ 의 부호까지 감안한 것이라고 생각하면 된다.\\\\
\\includegraphics[max width=\\textwidth, center]{775fe3b4-ce19-4ec2-82de-69f83888df16-07_333_1274_1998_592}

\\section*{Drill. 1 그래프의 기하적 상황의 추정과 확인}
앞의 문제에서는 조건 (가), (나)를 보자마자 항등식에 $x=-1$ 을 대입하고 싶어져야 한다. 항등식을 이용하는 기본 중 하나는 적절한 값을 대입해 보는 것. 두 조건 (가), (나)에서 $f(2 k-1)=0$ ( $k$ 는 정수)이라는 괜찮은 결과를 얻고, 그래프의 기하적 상황도 짐작할 수 있다. $-1 \\leq x \\leq 1$ 에서 $y$ 축에 대하여 대칭인 $y=f(x)$ 의 그래프를 $x$ 축의 방향으로 2 만큼 평행이동 하고 $x$ 축을 기준으로 $y$ 축의 방향으로 2 배한 것이 $1 \\leq x \\leq 3$ 에서의 $y=f(x)$ 의 그래프이고, 반대로 $-1 \\leq x \\leq 1$ 에서의 $f(x)$ 의 그래프를 $x$ 축의 방향으로 -2 만큼 평행이동하고 $x$ 축을 기준으로 $y$ 축의 방향으로 $\\frac{1}{2}$ 배한 것이 $-3 \\leq x \\leq-1$ 에서의 $y=f(x)$ 의 그래프이다. 반복\\~{} 각 구간에서의 $y=f(x)$ 의 그래프의 대칭도 확인했을 테니 ㄴㄷㅗ 가볍게 판단할 수 있다. 점 $(6,0)$ 에 대한 대칭과 직선 $x=6$ 에 대한 대칭의 곱에서 점 $(6,0)$ 에 대한 대칭 확인!\\\\
ᄃ에서는 ᄀ, ㄴ에서 확인한 것을 그대로 받아 이용하면 된다. 적분 구간을 $5,7,9, \\cdots, 15$ 로 모두 자르고, 각 구간에서 그래프가 점대칭이 되도록 곱해진 일차함수의 상수항을 조절 하고, 남은 정적분은 다음 구간으로 넘어가면서 넓이가 2 배가 되는 것으로 찬찬히 계산해서 마무리하면 된다.\\\\
이 정도는 모든 과정이 매끄럽게 이어질 수 있도록 해야 한다.

\\section*{Drill. 2 선대칭과 점대칭의 곱의 연산 결과}
직선 $x=k$ 에 대하여 대칭인 함수를 '선대칭', 점 $(k, 0)$ 에 대하여 대칭인 함수를 '점대칭'으로 나타내면 그 곱의 연산 결과는 다음과 같다.\\\\
$($ 선대칭 $) \\times($ 선대칭 $)=($ 선대칭 $),($ 선대칭 $) \\times($ 점대칭 $)=($ 점대칭 $)$,\\\\
$($ 점대칭 $) \\times($ 점대칭 $)=($ 선대칭 $)$\\\\
직선 $x=k$ 에 대하여 대칭인 함수와 점 $(k, c)(c \\neq 0)$ 에 대하여 대칭인 함수의 곱에서는 일반 적으로 대칭이 나타나지 않지만, 점 $(k, c)$ 에 대하여 대칭인 함수를 '점대칭 $+c$ '로 나타내면\\\\
$($ 선대칭 $) \\times($ 점대칭 $+c)=($ 선대칭 $) \\times($ 점대칭 $)+c \\times($ 선대칭 $)=($ 점대칭 $)+($ 선대칭 $)$ 으로 구분하여 다룰 수 있다.

\\section*{Drill. 1 알아야 할 것은 제대로 알아야}
앞의 문제에서 $f^{\\prime}(0)=0$ 이므로 이차함수 $f(x)$ 의 그래프는 $y$ 축, 즉 직선 $x=0$ 에 대하여 대칭 이고, $g(x)$ 의 도함수 $f(x-a)+b$ 의 그래프는 직선 $x=a$ 에 대하여 대칭이므로 삼차함수 $g(x)$ 의 그래프는 점 $(a, g(a))$ 에 대하여 대칭이다. ㄱㅇㅢ 판단은 이렇게 자연스럽게\\~{} 이어서 ㄴ. 방정식 $g(g(x))=x$ 의 실근은 곡선 $y=g(x)$ 와 직선 $y=x$ 의 교점의 $x$ 좌표 또는 곡선 $y=g(x)$ 위의 직선 $y=x$ 에 대하여 대칭인 점들의 $x$ 좌표로 이루어진 것을 알고 있어야 한다. $A=B$ 이고 집합 $B$ 의 원소의 개수는 많아봐야 3 이라는 판단과 함께 진작 구해 둔 $g(2 a)=0$ 을 이용하여 $g(0)=2 a, g(a)=a$ 의 확인으로 가닥을 잡아야 한다.\\\\
여기까지 정리했으면 ㄷ은 그리 어렵지 않다. 그래프의 대칭과 정적분에 대한 반응. 이 역시 알고 있다는 전제에서 ⋯\\\\
이 모든 과정은 알아야 할 것은 제대로 알고 있는 준비 태세와 그래프의 특수한 상태에 대한 충분한 경험이 있어야 가능하다!

\\section*{Drill. 2 도함수의 그래프의 대칭}
\\begin{center}
\\begin{tabular}{|c|c|c|}
\\hline
$f^{\\prime}(x)$ & 점 $(0,0)$ 대칭 $(\\text { 기함수 })$ & 직선 $x=0$ 대칭 $(\\text { 우함수 })$ \\\\
\\hline
$f(x)$ & 직선 $x=0$ 대칭 $(\\text { 우함수 })$ & 점 $(0, f(0))$ 대칭 \\\\
\\hline
\\end{tabular}
\\end{center}

\\begin{center}
\\begin{tabular}{|c|c|c|}
\\hline
$f^{\\prime}(x)$ & 점 $(k, 0)$ 대칭 & 직선 $x=k$ 대칭 \\\\
\\hline
$f(x)$ & 직선 $x=k$ 대칭 & 점 $(k, f(k))$ 대칭 \\\\
\\hline
\\end{tabular}
\\end{center}

기함수, 우함수인 $f^{\\prime}(x)$ 의 그래프와 $f(x)$ 의 그래프를 $x$ 축의 방향으로 $k$ 만큼 평행이동하면 점 $(k, 0)$ 대칭, 직선 $x=k$ 대칭인 $f^{\\prime}(x)$ 의 그래프와 $f(x)$ 의 그래프에 대해 생각할 수 있다. 참고로 $f^{\\prime}(x)$ 의 그래프가 $y$ 좌표가 0 이 아닌 점에 대하여 대칭일 때는 일반적으로 $f(x)$ 의 그래프의 대칭이 나타나지 않는다.

\\section*{Drill. 1 함수의 식이 주어지지 않은 구간에서의 그래프}
앞의 문제에서 우선 눈여겨봐야 할 것은 $0<x<2$ 에서 $g(x)$ 가 주어지지 않았다는 것이다. 경험이 충분하다면 $0<x<2$ 에서 $g(x)$ 의 그래프는 직선의 일부일 가능성이 매우 높다는 것과 조건 (가)에서 이 직선의 기울기까지 예상하고 확인하는 것으로 풀이의 방향을 잡을 수 있다. $g(0)=1$ 이고 조건 (다)에서 $g(2)=3$ 이므로 거의 확인 끝! $0<x<2$ 에서 $g(x)$ 의 그래프가 두 점 $(0,1),(2,3)$ 을 지나는 직선의 일부가 아닌 그래프 하나만 슥 그려보면 조건 (가)에 어긋나는 것은 쉽게 알 수 있다.\\\\
이어서 두 조건 (나), (다)에서 $g(x)$ 의 그래프의 점대칭과 $f(x)$ 의 그래프의 점대칭을 파악 하고 $g(x)$ 의 연결 지점에서의 미분가능으로 $f(x)$ 의 식을 구하는 것은 그리 어렵지 않다. 정적분의 계산은 점대칭인 함수의 정적분으로 계산할 구간과 $f(x)$ 의 적분이 필요한 구간을 구분하고, $f(x)$ 의 적분이 필요한 구간도 그래프와 적분 구간의 이동으로 최대한 간단하게 마무리할 수 있어야 한다.

\\section*{Comment}
\\section*{Drill. 2 그래프와 적분 구간의 이동}
(1) $\\int_{a}^{b} f(x+m) d x=\\int_{a+m}^{b+m} f(x) d x \\Rightarrow x$ 축의 방향으로 $m$ 만큼 평행이동\\\\
\\includegraphics[max width=\\textwidth, center]{775fe3b4-ce19-4ec2-82de-69f83888df16-11_261_684_858_1053}\\\\
(2) $\\int_{a}^{b} f(-x) d x=\\int_{-b}^{-a} f(x) d x \\Rightarrow y$ 축에 대하여 대칭이동\\\\
\\includegraphics[max width=\\textwidth, center]{775fe3b4-ce19-4ec2-82de-69f83888df16-11_310_684_1285_1053}\\\\
(3) $\\int_{-a}^{a} f(-x) d x=\\int_{-a}^{a} f(x) d x \\Rightarrow y$ 축에 대하여 대칭이동\\\\
\\includegraphics[max width=\\textwidth, center]{775fe3b4-ce19-4ec2-82de-69f83888df16-11_286_316_1755_1040}\\\\
\\includegraphics[max width=\\textwidth, center]{775fe3b4-ce19-4ec2-82de-69f83888df16-11_284_321_1755_1433}


\\end{document}"""


def extract_solutions_from_latex(latex_content):
    """LaTeX에서 해설 추출"""
    solutions = []
    
    # 본문 추출
    body = extract_body(latex_content)
    
    # 섹션 헤더 패턴
    section_pattern = re.compile(r'\\section\*\{([^}]+)\}')
    
    # Comment, Connment 섹션 찾기 (전략 해설)
    comment_sections = []
    for match in section_pattern.finditer(body):
        title = match.group(1)
        if 'Comment' in title or 'Connment' in title:
            comment_sections.append(match.start())
    
    # Drill 섹션 찾기 (개념 해설)
    drill_sections = []
    for match in section_pattern.finditer(body):
        title = match.group(1)
        if 'Drill' in title:
            drill_sections.append((match.start(), title))
    
    # 각 섹션에서 해설 추출
    all_sections = sorted([(pos, 'drill', title) for pos, title in drill_sections] + 
                          [(pos, 'comment', 'Comment') for pos in comment_sections])
    
    for i, (pos, section_type, title) in enumerate(all_sections):
        # 섹션 내용 추출
        if i < len(all_sections) - 1:
            next_pos = all_sections[i+1][0]
            section_content = body[pos:next_pos]
        else:
            section_content = body[pos:]
        
        # 섹션 헤더 제거
        section_content = re.sub(r'\\section\*\{[^}]*\}', '', section_content, count=1)
        
        # 이미지 제거
        section_content = re.sub(r'\\includegraphics[^}]*\{[^}]+\}', '', section_content)
        section_content = re.sub(r'\\begin\{figure\}.*?\\end\{figure\}', '', section_content, flags=re.DOTALL)
        section_content = re.sub(r'\\begin\{center\}.*?\\end\{center\}', '', section_content, flags=re.DOTALL)
        section_content = re.sub(r'\\begin\{enumerate\}.*?\\end\{enumerate\}', '', section_content, flags=re.DOTALL)
        section_content = re.sub(r'\\begin\{tabular\}.*?\\end\{tabular\}', '', section_content, flags=re.DOTALL)
        section_content = re.sub(r'\\caption\{[^}]+\}', '', section_content)
        
        # 텍스트 정리
        solution_text = clean_latex_text(section_content)
        
        # 빈 해설 제외
        if len(solution_text.strip()) < 50:
            continue
        
        # 해설 타입 판단
        solution_type = "strategy" if section_type == 'comment' else "concept"
        
        solutions.append({
            "index": f"{len(solutions)+1:02d}",
            "solution_type": solution_type,
            "title": title if section_type == 'drill' else "Comment",
            "content": solution_text.strip()
        })
    
    return solutions


def review_solutions(solutions):
    """해설 검토 (수학적 논리 포함)"""
    print("=" * 60)
    print("[해설 데이터 검토]")
    print("=" * 60)
    
    errors = []
    warnings = []
    
    for sol in solutions:
        content = sol.get('content', '')
        
        # LaTeX 괄호 검사
        dollar_count = content.count('$') - content.count('\\$')
        if dollar_count % 2 != 0:
            errors.append(f"해설 {sol['index']}: LaTeX 수식 괄호 불일치 ($ 개수: {dollar_count})")
        
        # 수학적 논리 검사 (적분 관련)
        if '적분' in content:
            # 정적분 정의 확인
            if '\\int_{a}^{b}' in content and 'f(b)-f(a)' not in content and 'f(a)-f(b)' not in content:
                if '도함수' in content or 'f\'' in content:
                    warnings.append(f"해설 {sol['index']}: 정적분과 도함수 관계 언급 가능")
        
        # 내용 길이 확인
        if len(content) < 100:
            warnings.append(f"해설 {sol['index']}: 내용이 짧음 ({len(content)}자)")
    
    print(f"\n[총 해설수] {len(solutions)}개")
    print(f"[개념 해설] {sum(1 for s in solutions if s['solution_type'] == 'concept')}개")
    print(f"[전략 해설] {sum(1 for s in solutions if s['solution_type'] == 'strategy')}개")
    
    if errors:
        print(f"\n[오류] {len(errors)}개")
        for err in errors:
            print(f"  - {err}")
    
    if warnings:
        print(f"\n[경고] {len(warnings)}개")
        for warn in warnings:
            print(f"  - {warn}")
    
    if not errors and not warnings:
        print("\n[오류] 없음")
    
    return len(errors) == 0


def compare_with_problems(solutions, problems_path):
    """문제 파일과 해설 비교 검토"""
    print("\n" + "=" * 60)
    print("[문제-해설 비교 검토]")
    print("=" * 60)
    
    try:
        with open(problems_path, 'r', encoding='utf-8') as f:
            problems = json.load(f)
        
        print(f"\n[문제 수] {len(problems)}개")
        print(f"[해설 수] {len(solutions)}개")
        
        # 주제 일치 확인
        problem_topics = set(p.get('topic', '') for p in problems)
        solution_topics = set()
        for sol in solutions:
            if '적분' in sol.get('content', ''):
                solution_topics.add('적분')
        
        if problem_topics & solution_topics:
            print(f"\n[주제 일치] 확인됨: {problem_topics & solution_topics}")
        else:
            print(f"\n[경고] 주제 일치 확인 필요")
            print(f"  문제 주제: {problem_topics}")
            print(f"  해설 주제: {solution_topics}")
        
        # 수학적 개념 일치 확인
        print("\n[수학적 개념 확인]")
        concepts_in_problems = set()
        for p in problems:
            q = p.get('question', '')
            if '\\int' in q:
                concepts_in_problems.add('정적분')
            if 'f(x)' in q and 'g(x)' in q:
                concepts_in_problems.add('함수 관계')
            if '넓이' in q or '넓이를' in q:
                concepts_in_problems.add('넓이')
            if '대칭' in q or '기함수' in q or '우함수' in q:
                concepts_in_problems.add('대칭성')
        
        concepts_in_solutions = set()
        for sol in solutions:
            content = sol.get('content', '')
            if '정적분' in content or '\\int' in content:
                concepts_in_solutions.add('정적분')
            if '함수' in content and ('f(x)' in content or 'g(x)' in content):
                concepts_in_solutions.add('함수 관계')
            if '넓이' in content:
                concepts_in_solutions.add('넓이')
            if '대칭' in content or '기함수' in content or '우함수' in content:
                concepts_in_solutions.add('대칭성')
        
        if concepts_in_problems & concepts_in_solutions:
            print(f"  확인된 개념: {concepts_in_problems & concepts_in_solutions}")
        else:
            print(f"  [경고] 개념 일치 확인 필요")
        
    except FileNotFoundError:
        print(f"\n[경고] 문제 파일을 찾을 수 없습니다: {problems_path}")
    except Exception as e:
        print(f"\n[오류] 비교 중 오류 발생: {e}")


def save_for_deepseek(solutions, base_dir, base_filename):
    """딥시크용 파일 저장"""
    base_dir = Path(base_dir)
    base_dir.mkdir(parents=True, exist_ok=True)
    
    # CSV 저장
    csv_path = base_dir / f"{base_filename}_deepseek.csv"
    with open(csv_path, 'w', encoding='utf-8-sig', newline='') as f:
        f.write("index,solution_type,title,content\n")
        for sol in solutions:
            index = sol['index']
            sol_type = sol['solution_type']
            title = sol.get('title', '').replace(',', '，').replace('\n', ' ')
            content = sol['content'].replace(',', '，').replace('\n', ' ')
            f.write(f"{index},{sol_type},{title},{content}\n")
    
    # JSON 저장
    json_path = base_dir / f"{base_filename}_deepseek.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(solutions, f, ensure_ascii=False, indent=2)
    
    print(f"\n[CSV 저장 완료] {csv_path}")
    print(f"[JSON 저장 완료] {json_path}")
    
    return csv_path, json_path


def main():
    print("=" * 60)
    print("[수2 드릴 P6 해설 LaTeX → CSV 변환]")
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
    
    # 4단계: 문제와 비교
    problems_path = Path(r'C:\Users\a\Documents\MathPDF\organized\현우진\수2_2005학년도_현우진_드릴\수2_2025학년도_현우진_드릴_P6_문제_deepseek.json')
    compare_with_problems(solutions, problems_path)
    
    # 5단계: 저장
    print("\n[4단계] 딥시크용 파일 저장 중...")
    base_dir = Path(r'C:\Users\a\Documents\MathPDF\organized\현우진\수2_2005학년도_현우진_드릴')
    base_filename = "수2_2025학년도_현우진_드릴_P6_해설"
    csv_path, json_path = save_for_deepseek(solutions, base_dir, base_filename)
    
    print("\n" + "=" * 60)
    print("[완료] 딥시크가 읽을 수 있는 형태로 저장되었습니다.")
    print("=" * 60)
    print(f"저장 위치: {base_dir}")
    print(f"  - CSV: {csv_path.name}")
    print(f"  - JSON: {json_path.name}")


if __name__ == '__main__':
    main()
