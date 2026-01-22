# convert_su2_p5_solution_latex.py
# 수2 드릴 P5 해설 LaTeX를 딥시크용 CSV로 변환

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

\\newunicodechar{□}{\\ifmmode\\square\\else{$\\square$}\\fi}

\\begin{document}
\\captionsetup{singlelinecheck=false}
\\section*{Drill. 1 정적분을 포함한 함수}
$f(x)=g(x)+\\int_{a}^{b} f(t) d t$ 와 같이 정적분을 포함한 함수는 상수 $k$ 에 대하여 $\\int_{a}^{b} f(t) d t=k$ 로 놓으면 $f(x)=g(x)+k$ 이므로 $\\int_{a}^{b}\\{g(x)+k\\} d x=k$ 에서 $k$ 를 구하는 방법으로 다룰 수 있다.

\\section*{Drill. 2 우함수와 기함수의 정적분}
적분 구간이 대칭으로 나타날 때, 그래프의 대칭성 확인은 매우 중요하다. $\\int_{-a}^{a}$ 에서 우함수인지 기함수인지 체크하는 것은 기본이고, $\\int_{0}^{a}, \\int_{a}^{0}$ 등과 같이 적분 구간의 한쪽 끝이 0 인 경우에도 그래프의 대칭성과 밀접한 관련이 있을 수 있으므로 이에 주목하도록 한다.

\\begin{enumerate}
  \\item 우함수의 정적분
\\end{enumerate}

모든 실수 $x$ 에 대하여 $f(-x)=f(x)$ 일 때

$$
\\int_{-a}^{a} f(x) d x=2 \\int_{0}^{a} f(x) d x
$$

\\begin{enumerate}
  \\setcounter{enumi}{1}
  \\item 기함수의 정적분
\\end{enumerate}

모든 실수 $x$ 에 대하여 $f(-x)=-f(x)$ 일 때

$$
\\int_{-a}^{a} f(x) d x=0
$$

앞의 문제는 $\\int_{0}^{1} x^{4} f(t) d t$ 에서 변수와 상수를 구별해서 정리하고 시작해야 한다. 적분 구간이 서로 다른 정적분이 둘 이상 포함되면 각각 다른 미지수로 잡기도 하지만 앞의 문제에서 과연 두 정적분의 값을 각각 다른 미지수로 잡아야 할까? 여러 정적분이 함께 등장할 때는 정적분의 성질의 이용 여부와 그래프의 대칭의 확인은 필수다.

Drill 정적분은 상수이다\\\\
정적분 $\\int_{a}^{b} \\square d x$ 에서 □ 의 식에 $x$ 가 아닌 변수가 포함되지 않으면 $\\int_{a}^{b} \\square d x$ 는 상수로 취급하는 당연한 기본 인식이 은근히 중요할 때가 있다. 앞의 문제는\\\\
$f(x) \\geq f\\left(\\int_{0}^{1} f(t) d t\\right)$ 에서 $\\int_{0}^{1} f(t) d t$ 를 상수 $k$ 로 보면 $f(x) \\geq f(k)$, 즉 $f(x)$ 가 $x=k$ 에서 최솟값을 갖는다는 것으로 해석하고 풀어 가면 된다.

\\section*{Comment}
\\section*{Drill 도함수의 정적분}
정적분의 정의에서

$$
\\int_{a}^{b} f^{\\prime}(x) d x=f(b)-f(a)
$$

를 다음과 같이 이해할 수 있다.\\\\
(1) $f^{\\prime}(x)$ 의 정적분의 값은 $f(x)$ 의 함숫값의 차이다.\\\\
(2) $f(x)$ 의 함숫값의 차는 $f^{\\prime}(x)$ 의 정적분의 값이다.

그림과 같이 $f^{\\prime}(x)$ 의 그래프와 $x$ 축으로 둘러싸인 부분의 넓이 $S_{1}, S_{2}, S_{3}$ 은 각 구간의 양 끝에서 $f(x)$ 의 함숫값의 차와 같다.\\\\
\\includegraphics[max width=\\textwidth, center]{b49952d3-dc53-4e18-8e36-780a28bfe257-03_443_502_1235_1036}\\\\
$f(x)$ 를 위치, $f^{\\prime}(x)$ 를 속도로 보면 $a<b$ 일 때

$$
\\int_{a}^{b}\\left|f^{\\prime}(x)\\right| d x
$$

는 구간 $[a, b]$ 에서 곡선 $y=f(x)$ 위를 움직이는 점에서\\\\
$y$ 축에 내린 수선의 발이 움직인 거리\\\\
로 볼 수 있다.\\\\
앞의 문제의 조건 (가)에서 얻은 결과와 함께 삼차함수의 그래프의 비율 관계를 감안하여 조건 (나)를 이렇게 보면 삼차함수 $y=f(x)$ 의 그래프가 구간 ( 1,2 )에서 $x$ 축에 접한다는 것, 점 $(1, f(1))$ 이 변곡점이라는 것을 쉽게 알고 $f(x)$ 의 식을 곧바로 쓸 수 있다.

\\section*{Drill. 1 정적분을 부호를 가진 넓이로}
큰 틀에서 정적분을 다루는 두 가지 방법은 부정적분의 함숫값의 차로 계산하는 것과 부호를 가진 넓이로 다루는 것이다. 앞의 문제는 주어진 등식의 우변의 변수 구분에 주의하여 양변에 $k=0$ 을 대입해 보면 $f(x)$ 가 이차함수라는 것만으로 ㄱ을 쉽게 판단할 수 있다.\\\\
ㄴ은 ㄱ에서 확인한 $f(0)=0$ 또는 $\\int_{0}^{1} f(x) d x=0$ 이라는 확실한 결과를 케이스 구분의 기준 으로 이용할 생각만 하면 역시 이차함수 $f(x)$ 의 최고차항의 계수가 양수라는 것으로 그리 어렵지 않게 판단할 수 있다.\\\\
ㄷ에서는 ㄱ, ㄴ에서의 확인 과정과 결과를 적절히 끌어다 이용하는 센스를 잘 발휘하면 된다. $k=-1$ 일 때의 방정식을 정적분의 성질을 이용하여 정리한 두 가지 결과에서 모두 방정식 $f(x)=0$ 이 음의 실근을 갖는다. 그리고 $1 \\in A$ 이다. ㄴ에서 확인한 것을 그대로 이용할 수 있다. $f(x)$ 의 식을 쓰고 이 두 가지 결과 중 올바른 하나를 선별하여 계산하고 마무리하면 된다.\\\\
다항함수에 관한 합답형 문항이 그래프를 이용한 기하적 판단뿐인 경우도 없지는 않지만 앞의 문제의 ㄷ에서처럼 함수의 식의 결정, 함수의 식을 이용한 계산이 어디에선가 필요한 경우가 훨씬 많다.

\\section*{Comment}
\\section*{Drill 2 적분방향과 넓이}
$\\int_{a}^{b} f(x) d x=-\\int_{b}^{a} f(x) d x$ 이므로 $a$ 에서 $b$ 까지의 정적분과 $b$ 에서 $a$ 까지의 정적분의 부호가 반대이다. 따라서 함숫값의 부호와 함께 적분방향까지 고려하면\\\\
$a<b$ 이고 $f(x) \\geq 0$ 일 때

$$
\\int_{a}^{b} f(x) d x=+(\\text { 넓이 }), \\int_{b}^{a} f(x) d x=-(\\text { 넓이 })
$$

$a<b$ 이고 $f(x) \\leq 0$ 일 때

$$
\\int_{a}^{b} f(x) d x=-(\\text { 넓이 }), \\int_{b}^{a} f(x) d x=+(\\text { 넓이 })
$$

이므로 다음과 같이 정리해 볼 수 있다.\\\\
적분방향 + , 함숫값 + (정적분) $=+$ (넓이)\\\\
적분방향 - , 함숫값 $+\\Rightarrow$ (정적분) $=-$ (넓이)\\\\
적분방향 + , 함숫값 $-\\Rightarrow($ 정적분 $)=-($ 넓이 $)$\\\\
적분방향 - , 함숫값 $-\\Rightarrow($ 정적분 $)=+($ 넓이 $)$\\\\
\\includegraphics[max width=\\textwidth, center]{b49952d3-dc53-4e18-8e36-780a28bfe257-05_228_319_1450_1048}

$$
\\int_{a}^{b} f(x) d x>0
$$

\\begin{center}
\\includegraphics[max width=\\textwidth]{b49952d3-dc53-4e18-8e36-780a28bfe257-05_223_317_1810_1048}
\\end{center}

$$
\\int_{a}^{b} f(x) d x<0
$$

\\begin{center}
\\includegraphics[max width=\\textwidth]{b49952d3-dc53-4e18-8e36-780a28bfe257-05_223_324_1450_1421}
\\end{center}

$$
\\int_{b}^{a} f(x) d x<0
$$

\\begin{center}
\\includegraphics[max width=\\textwidth]{b49952d3-dc53-4e18-8e36-780a28bfe257-05_227_318_1810_1421}
\\end{center}

$$
\\int_{b}^{a} f(x) d x>0
$$

Drill 부정적분 $\\int_{a}^{x} f(t) d t$ 를 포함한 항등식\\\\
부정적분 $\\int_{a}^{x} f(t) d t$ 를 포함한 항등식을 다루는 기본적인 방법은 다음과 같다.\\\\
(1) 양변을 $x$ 에 대하여 미분하고 새로운 항등식을 얻는다. (항등식은 미분해도 항등식이다.)\\\\
(2) 양변에 $x=a$ 를 대입하고 $\\int_{a}^{a} f(t) d t=0$ 임을 이용하여 함숫값 또는 미지수의 값을 얻는다.\\\\
(항등식의 양변에 임의의 값을 대입할 수 있다.)

\\section*{2024학년도 9월 평가원 공통 22번}
두 다항함수 $f(x), g(x)$ 에 대하여 $f(x)$ 의 한 부정적분을 $F(x)$ 라 하고 $g(x)$ 의 한 부정적분을 $G(x)$ 라 할 때, 이 함수들은 모든 실수 $x$ 에 대하여 다음 조건을 만족시킨다.\\\\
(가) $\\int_{1}^{x} f(t) d t=x f(x)-2 x^{2}-1$\\\\
(나) $f(x) G(x)+F(x) g(x)=8 x^{3}+3 x^{2}+1$\\\\
$\\int_{1}^{3} g(x) d x$ 의 값을 구하시오. [4점]\\\\
답 10

\\section*{Comment}
Drill 부정적분 $\\int_{a}^{x} f(t) d t$ 를 포함한 항등식\\\\
부정적분 $\\int_{a}^{x} f(t) d t$ 를 포함한 항등식의 기본 접근법과 함께 다음과 같은 접근법도 반드시 고려해야 한다.\\\\
(1) 정적분의 정의를 적용할 수 있다. 특히 $f^{\\prime}(x)$ 에 대한 부정적분에서

$$
\\int_{a}^{x} f^{\\prime}(t) d t=f(x)-f(a)
$$

(2) 양변에 $x=b(a \\neq b)$ 를 대입하여 $\\int_{a}^{b} f(t) d t$ 의 값에 관해 다룰 수 있다.

\\section*{Drill 부정적분으로 정의된 함수}
함수 $g(x)=\\int_{a}^{x} f(t) d t$ 가 등장할 때 미분하고 대입할 수도 있으나 다음과 같은 그래프에 관한 기하적 관점이 필요할 때가 많다.\\\\
(1) $g(x)$ 의 도함수 $f(x)$ 의 그래프를 이용하여 $g(x)$ 의 그래프의 개형을 추론할 수 있다. 반대로 $g(x)$ 의 그래프를 이용하여 $g(x)$ 의 도함수 $f(x)$ 의 그래프의 개형을 추론할 수 있다.\\\\
(2) $g(a)=0$ 이므로 $g(x)$ 의 그래프는 점 $(a, 0)$ 을 지난다.

이때 $g(x)$ 의 함숫값은 $g(b)=\\int_{a}^{b} f(t) d t$ 와 같이 정적분의 값으로 계산하게 되는데, $f(x)$ 의 그래프가 직선 등으로 간단히 주어질 때는 넓이의 관점으로 다루는 것이 편리하다.

\\section*{Drill. 1 부정적분으로 정의된 함수}
앞의 문제에서는 $f(x)$ 가 이차함수이므로 부정적분인 삼차함수 $\\int_{1}^{x} f(t) d t$ 에 대한 파악부터 시작해야 한다. $\\int_{1}^{x} f(t) d t$ 에 자연스럽게 $x=1$ 을 대입해 보면 $\\int_{1}^{4} f(x) d x=0$ 인 조건과 함께 인수 2 개를 쉽게 구할 수 있다.\\\\
조건 (가)에서 $x-1$ 의 부호에 따라 케이스를 나누어 삼차함수의 그래프의 개형을 파악하고, 최고차항의 계수만 미지수로 잡아 식을 쓰고, 미분해서 $f(x)$ 의 식을 구하고, $f(x)$ 의 식의 형태에서 곡선 $y=f(x)$ 와 직선 $y=3 x-12$ 의 접점 $(4,0)$ 을 잡아내고 마무리하는 것까지 모든 과정이 막힘없이 쭉쭉 이어져야 한다.

\\section*{Drill. 2 함수에 대한 부등식의 조건}
어떤 구간에서 항상 성립하는 함수에 대한 부등식의 조건이 주어진다면 그래프가 접하는 상황일 가능성이 매우 높다. 예를 들어 어떤 구간에서 $f(x) \\geq g(x)$ 가 항상 성립한다는 조건 에서 곡선 $y=f(x)$ 가 곡선 $y=g(x)$ 보다 위쪽에 있을 뿐 서로 만나지 않는다면 별 쓸모없는 부등식이 돼버리고, 두 곡선의 교점이 존재하고 이 교점이 접점이 아니라면 교점의 좌우에서 상하 관계가 바뀌어 부등식이 성립하지 않게 된다.

\\section*{Connment}
\\section*{Drill 사차함수의 그래프의 특징의 이해}
앞의 문제에서 $f(x)$ 가 삼차함수이므로 부정적분인 $\\int_{a}^{x} f(t) d t$, 즉 $|g(x)|$ 는 사차함수이다. $g(x)$ 의 그래프의 $g(x)<0$ 인 부분을 $x$ 축에 대하여 대칭이동한 $|g(x)|$ 의 그래프가 사차 함수의 그래프라는 것이고 진작부터 $x=a$ 를 대입해놔서 $g(a)=0$ 인 것도 알고 있다. $|g(x)|$ 의 그래프가 $x$ 축과 점 $(a, 0)$ 에서 만난다는 것인데 여기서 무슨 일이? $|g(x)|$ 가 사차함수이므로 미분가능하다는 기본 인식이 매우 중요하다. 점 $(a, 0)$ 뿐만 아니라 $|g(x)|$ 의 그래프가 $x$ 축과 만나는 모든 점은 접점이어야 한다. $g(x)$ 가 오직 하나의 극값을 갖는 것에서 사차함수의 그래프의 개형을 잡는 것은 그리 어렵지 않다. 당연히 특수한 경우 부터! 사차함수의 그래프의 특징에 대한 이해가 확실하다면 $|g(x)|$ 의 도함수인 $f(x)$ 의 식을 인수분해해서 $|g(x)|$ 가 극값을 갖는 $x$ 의 값의 차의 대소 비교로부터 자연스럽게 마무리할 수 있다.\\\\
최고차항의 계수가 양수인 사차함수의 극댓값과 극솟값이 모두 존재할 때, 극값을 갖는 $x$ 의 값의 차의 대소 관계에 따른 다음의 그래프의 개형을 반드시 확인해두자.

\\begin{figure}[h]
\\begin{center}
  \\includegraphics[max width=\\textwidth]{b49952d3-dc53-4e18-8e36-780a28bfe257-10_473_302_1467_752}
\\captionsetup{labelformat=empty}
\\caption{$b-a=c-b$}
\\end{center}
\\end{figure}

\\begin{figure}[h]
\\begin{center}
  \\includegraphics[max width=\\textwidth]{b49952d3-dc53-4e18-8e36-780a28bfe257-10_561_300_1442_1120}
\\captionsetup{labelformat=empty}
\\caption{$b-a>c-b$}
\\end{center}
\\end{figure}

\\begin{figure}[h]
\\begin{center}
  \\includegraphics[max width=\\textwidth]{b49952d3-dc53-4e18-8e36-780a28bfe257-10_502_312_1505_1488}
\\captionsetup{labelformat=empty}
\\caption{$b-a<c-b$}
\\end{center}
\\end{figure}

\\section*{Comment}
Drill. $1 \\int_{a}^{x} f(t) d t$ 와 $\\int_{b}^{x} f(t) d t$ 의 관계\\\\
$a \\neq b$ 일 때, 두 부정적분 $\\int_{a}^{x} f(t) d t, \\int_{b}^{x} f(t) d t$ 는 한 함수 $f(x)$ 에 대한 부정적분이므로 서로 같은 함수일 수도 있지만 서로 다른 함수일 수도 있다. 두 부정적분이 서로 다른 함수인 경우 에는 적분상수만 서로 다르고, 정적분의 정의를 이용하여 다음과 같이 한 함수로 나타낼 수 있다.\\\\
$g(x)=\\int_{a}^{x} f(t) d t$ 라 하면 $\\int_{b}^{x} f(t) d t=g(x)-g(b)$\\\\
앞의 문제는 두 부정적분 $\\int_{0}^{x} f(t) d t, \\int_{1}^{x} f(t) d t$ 를 하나의 함수로 나타낼 수 있다는 인식에서 출발한다. $g(x)=\\int_{0}^{x} f(t) d t, \\int_{1}^{x} f(t) d t=g(x)-g(1)$ 과 같이 나타내고 시작해야 한다.

\\section*{Drill. 2 부등식 풀이의 기본 원리}
$a<b$ 일 때, 이차부등식 $(x-a)(x-b) \\leq 0$ 의 해가 $a \\leq x \\leq b$ 인 것은 $x \\geq a, x \\leq b$ 또는 $x \\leq a$, $x \\geq b$ 를 풀어서 나온 결과를, 이차부등식 $(x-a)(x-b) \\geq 0$ 의 해가 $x \\leq a$ 또는 $x \\geq b$ 인 것은 $x \\geq a, x \\geq b$ 또는 $x \\leq a, x \\leq b$ 를 풀어서 나온 결과를 기억하고 활용하는 것이다.\\\\
앞의 문제에서 $g(x)=\\int_{0}^{x} f(t) d t$ 로 고친 부등식 $g(x)\\{g(x)+x-1-g(1)\\} \\leq 0$ 을 $g(x)$ 에 대한 부등식으로 보았을 때, 해의 경계에 해당하는 0 과 $-x+1+g(1)$ 의 대소 관계가 정해 지지 않은 것에서 부등식 풀이의 기본으로 돌아가 $g(x) \\geq 0, g(x) \\leq-x+1+g(1)$ 또는 $g(x) \\leq 0, g(x) \\geq-x+1+g(1)$ 로 다루겠다고 판단할 수 있어야 한다.\\\\
$0 \\leq-x+1+g(1)$ 인 경우에 $0 \\leq g(x) \\leq-x+1+g(1),-x+1+g(1) \\leq 0$ 인 경우에 $-x+1+g(1) \\leq g(x) \\leq 0$ 으로 케이스를 구분해 봐도 좋다.\\\\
이어서 당연히 원점을 지나는 삼차함수 $y=g(x)$ 의 그래프와 $x$ 축, 직선 $y=-x+1+g(1)$ 의 관계를 파악해 보려 할 텐데, 부등식의 해가 $-1 \\leq x \\leq 3$ 인 것에서 $y=g(x)$ 의 그래프를 어떻게 잡아보기 시작할지 정하는 센스도 중요하다. 부등식의 해의 경계, 방정식의 실근, 그래프의 교점의 $x$ 좌표는 필요에 따라 언제든 오가며 바꾸어볼 수 있어야 한다.

\\section*{Drill 적분 변수를 구별해서 잘 정리하기만 하면}
앞의 문제는 적분 변수부터 구별하여 정리하고 양변을 미분하여 얻은 $h^{\\prime}(x)=f^{\\prime}(x) \\int_{k}^{x} g(t) d t$ 부터 시작하면 된다. $f(x), g(x)$ 가 모두 이차함수이므로 $f^{\\prime}(x)$ 는 일차함수, $\\int_{k}^{x} g(t) d t$ 는 삼차함수, $h^{\\prime}(x)$ 는 사차함수이다. $h(x)$ 가 오차함수인 것에 관심을 가질 필요는 전혀 없다. $h(x)$ 가 극값을 갖지 않아야 하므로 최고차항의 계수가 양수인 사차 함수 $h^{\\prime}(x)$ 가 모든 실수 $x$ 에 대하여 $h^{\\prime}(x) \\geq 0$ 이어야 한다. 사차함수 $h^{\\prime}(x)$ 에 집중!\\\\
$h^{\\prime}(k)=0$ 이므로 $x=k$ 의 좌우에서 $h^{\\prime}(x)>0$ 이어야 한다. 점 $(k, 0)$ 이 사차함수 $y=h^{\\prime}(x)$ 의 그래프와 $x$ 축의 접점이고 극소인 점이라는 것이다. 이러한 $k$ 의 값이 $a, a+3$ 뿐이라니 $h^{\\prime}(x)$ 의 식도 쉽게 쓸 수 있다. 이제 $f^{\\prime}(x), \\int_{k}^{x} g(t) d t$ 의 인수를 구성하고 마무리하면 된다.

\\section*{Connment}
\\section*{Drill 두 곡선 $y=f(x)$ 와 $y=f^{-1}(x)$ 로 둘러싸인 부분의 넓이}
$f(x)$ 가 증가하는 연속함수일 때, 두 곡선 $y=f(x), y=f^{-1}(x)$ 로 둘러싸인 부분의 넓이는

$$
2 \\int_{a}^{b}|f(x)-x| d x
$$

\\begin{center}
\\includegraphics[max width=\\textwidth]{b49952d3-dc53-4e18-8e36-780a28bfe257-13_450_494_915_1042}
\\end{center}

두 곡선 $y=f(x)$ 와 $y=f^{-1}(x)$ 사이의 관계는 일반적으로 곡선 $y=f(x)$ 와 직선 $y=x$ 사이의 관계로 다룬다. 앞의 문제에서는 삼차함수 $f(x)$ 와 그 역함수 $g(x)$ 의 차 $f(x)-g(x)$ 의 등장에서 $h(x)$ 에 대한 조건들을 곡선 $y=f(x)$ 와 직선 $y=x$ 의 교점의 좌표와 $y=f(x)$ 의 그래프의 대칭을 파악하고 식을 작성하는 데 이용할 수 있어야 한다. 마무리 단계에서 삼차 함수가 역함수를 갖기 위한 조건의 이용을 떠올리지 못하는 슬픈 일도 없어야…


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
        
        concepts_in_solutions = set()
        for sol in solutions:
            content = sol.get('content', '')
            if '정적분' in content or '\\int' in content:
                concepts_in_solutions.add('정적분')
            if '함수' in content and ('f(x)' in content or 'g(x)' in content):
                concepts_in_solutions.add('함수 관계')
        
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
    print("[수2 드릴 P5 해설 LaTeX → CSV 변환]")
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
    problems_path = Path(r'C:\Users\a\Documents\MathPDF\organized\현우진\수2_2005학년도_현우진_드릴\수2_2025학년도_현우진_드릴_P5_문제_deepseek.json')
    compare_with_problems(solutions, problems_path)
    
    # 5단계: 저장
    print("\n[4단계] 딥시크용 파일 저장 중...")
    base_dir = Path(r'C:\Users\a\Documents\MathPDF\organized\현우진\수2_2005학년도_현우진_드릴')
    base_filename = "수2_2025학년도_현우진_드릴_P5_해설"
    csv_path, json_path = save_for_deepseek(solutions, base_dir, base_filename)
    
    print("\n" + "=" * 60)
    print("[완료] 딥시크가 읽을 수 있는 형태로 저장되었습니다.")
    print("=" * 60)
    print(f"저장 위치: {base_dir}")
    print(f"  - CSV: {csv_path.name}")
    print(f"  - JSON: {json_path.name}")


if __name__ == '__main__':
    main()
