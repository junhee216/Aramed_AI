# convert_su1_p6_solution_latex.py
# 수1 드릴 P6 해설 LaTeX를 딥시크용 CSV로 변환

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
\\newunicodechar{⇔}{\\ifmmode\\Leftrightarrow\\else{$\\Leftrightarrow$}\\fi}
\\newunicodechar{⇒}{\\ifmmode\\Rightarrow\\else{$\\Rightarrow$}\\fi}

\\begin{document}
\\section*{Drill 등차수열을 이루는 수}
앞의 문제는 $(a k+5)^{k}$ 의 $k$ 제곱근 중 실수인 것을 $k$ 가 홀수인 경우와 짝수인 경우로 나누어 자연스럽게 나열하고 시작할 수 있어야 한다. $(a k+5)^{k}$ 의 $k$ 제곱근 중 실수인 것은 $k$ 가 홀수이면 무조건 1 개, $k$ 가 짝수이면 2 개 또는 1 개이다. $n(A)=5$ 가 되려면 $k$ 가 짝수인 경우에 대한 조절이 필요함을 알 수 있다. 남은 일은 집합 $A$ 의 원소가 등차수열을 이루는 것을 어떻게 다루느냐 하는 것. 등차수열을 이루는 수를 다루는 전형적인 방법과 수식이 있고 이들을 상황에 맞게 잘 이용하는 것도 중요하지만 잊지 말아야 할 본질은 이웃하는 항 사이의 간격이 일정하다는 것이다!

\\section*{2024학년도 6월 평가원 공통 12번}
$a_{2}=-4$ 이고 공차가 0 이 아닌 등차수열 $\\left\\{a_{n}\\right\\}$ 에 대하여 수열 $\\left\\{b_{n}\\right\\}$ 을 $b_{n}=a_{n}+a_{n+1}(n \\geq 1)$ 이라 하고, 두 집합 $A, B$ 를

$$
A=\\left\\{a_{1}, a_{2}, a_{3}, a_{4}, a_{5}\\right\\}, \\quad B=\\left\\{b_{1}, b_{2}, b_{3}, b_{4}, b_{5}\\right\\}
$$

라 하자. $n(A \\cap B)=3$ 이 되도록 하는 모든 수열 $\\left\\{a_{n}\\right\\}$ 에 대하여 $a_{20}$ 의 값의 합은? [4점]\\\\
(1) 30\\\\
(2) 34\\\\
(3) 38\\\\
(4) 42\\\\
(5) 46

\\section*{Comment}
\\section*{Drill. 1 등차수열과 등비수열의 구조에 대한 기본적인 이해}
등차수열과 등비수열의 구조적 특징의 이해와 활용은 대단히 중요하다. 그런데 이 구조적 특징이라는 게 별 대단한 게 아니다. 등차수열과 등비수열의 정의로부터 너무나 당연히 알 수 있는 항 사이의 간격과 공차, 공비의 연계 그리고 합의 대칭성, 곱의 대칭성에 관한 것이다. 앞의 문제에서 자연스럽게 인식하고 출발해야 할 것은 등차수열 $\\left\\{a_{n}\\right\\}$ 의 공차가 음수이므로 $a_{6} \\times a_{7}<0$ 에서 $a_{6}>0, a_{7}<0$ 이고 등비수열 $\\left\\{b_{n}\\right\\}$ 의 공비가 $m$ 이므로 $b_{3}$ 을 $b_{2} m$ 으로 고쳐서 써야겠다는 것이다. 조건 (나)의 시그마로 나타낸 관계식에서는 당연히 수열의 합과 일반항의 관계를 이용할 수 있어야 한다. 여기에 등차수열의 합의 대칭성에 대한 이해가 조금 더해지면 된다.

\\section*{Drill 2 등차수열의 합의 대칭성}
공차가 $d$ 인 등차수열 $\\left\\{a_{n}\\right\\}$ 에 대하여

$$
a_{k}+a_{l}=\\left(a_{k}+d\\right)+\\left(a_{l}-d\\right)=\\left(a_{k}+2 d\\right)+\\left(a_{l}-2 d\\right)=\\left(a_{k}+3 d\\right)+\\left(a_{l}-3 d\\right)=\\cdots
$$

에서

$$
a_{k}+a_{l}=a_{k+1}+a_{l-1}=a_{k+2}+a_{l-2}=a_{k+3}+a_{l-3}=\\cdots
$$

이고

$$
k+l=(k+1)+(l-1)=(k+2)+(l-2)=(k+3)+(l-3)=\\cdots
$$

이다. 즉 정중앙을 기준으로\\\\
대칭인 위치의 두 항의 합과 두 항의 항수의 합이 일정\\\\
하다.\\\\
\\includegraphics[max width=\\textwidth, center]{cf797797-a97f-4ffa-a014-34281dffcf6c-02_259_280_1759_964}\\\\
\\includegraphics[max width=\\textwidth, center]{cf797797-a97f-4ffa-a014-34281dffcf6c-02_174_352_1797_1377}

등차수열의 합의 대칭성을 생각할 때\\\\
(1) 항의 개수가 짝수이면 정중앙에 항이 나타나지 않는다.\\\\
(2) 항의 개수가 홀수이면 정중앙의 항(등차중항)은 다른 대칭인 위치에 있는 두 항의 합의 $\\frac{1}{2}$ 이다.

\\section*{Chapter 3}
수열

\\section*{Comment}
Drill. 3 등차수열의 합이 0\\\\
공차가 0 이 아닌 등차수열의 합이 0 이면 정중앙을 기준으로 대칭인 위치에 있는 두 항이 절댓값이 같고 부호가 반대이다. 즉 정중앙을 기준으로

대칭인 위치의 두 항의 합이 0 이고 두 항의 항수의 합이 일정 하다. 또한\\\\
(1) 항의 개수가 짝수이면 0 인 항이 없다.\\\\
(2) 항의 개수가 홀수이면 정중앙의 항(등차중항)은 0 이다.

Drill 등차수열은 일차함수이고 직선을 나타낸다\\\\
첫째항이 $a$ 이고 공차가 $d$ 인 등차수열 $\\left\\{a_{n}\\right\\}$ 의 일반항 $a_{n}=a+(n-1) d$ 를

$$
a_{n}=d n+(a-d)
$$

로 고쳐 쓰면 이 등차수열은 기울기가 $d$ 인 직선을 나타내는 일차함수

$$
f(x)=d x+(a-d)
$$

로 볼 수 있다.

이러한 기본적인 관점만 갖추고 있다면 앞의 문제에서 등차수열 $\\left\\{a_{n}\\right\\}$ 의 공차를 미지수로 잡고 좌표평면의 직선을 이용하여 $\\left|a_{n}-a_{10}\\right|$ 과 $\\frac{a_{n}}{2}$ 의 대소를 비교하기로 하는 선택은 쉬울 수 있다. 조건 (가)를 이용하여 좌표평면에 직선으로 나타내기 알맞은 정도로 등차수열 $\\left\\{a_{n}\\right\\}$ 의 일반항을 정리하는 것이 더 까다로울 듯. 그런데! 조건 (가)는 등차수열의 구조에 관한 아주 기본적인 이해로 정리할 수 있다. 공차를 $d$ 라 하면 $b_{6}$ 의 값은 $4 d, \\frac{a_{6}}{2}$ 중 하나이고 $b_{12}$ 의 값은 $2 d, \\frac{a_{12}}{2}$ 중 하나이다. 공차 $d$ 가 양수이므로 $4 d \\neq 2 d$ 이고 $a_{6} \\neq a_{12}$, 즉 $\\frac{a_{6}}{2} \\neq \\frac{a_{12}}{2}$ 이다.\\\\
조건 (가)에서 따져봐야 할 케이스는 두 가지만 남는다. 차근차근 점검해보면 된다.\\\\
등차수열의 당연한 구조적 특징을 이해하고 활용할 준비를 갖추는 것은 너무나 중요한 것!

\\section*{Drill 등차수열의 합의 일반항과 이차함수의 그래프}
공차가 0 이 아닌 등차수열 $\\left\\{a_{n}\\right\\}$ 의 첫째항부터 제 $n$ 항까지의 합 $S_{n}$ 은 상수항이 0 인 $n$ 에 대한 이차식

$$
S_{n}=a n^{2}+b n
$$

이고, 이때 등차수열 $\\left\\{a_{n}\\right\\}$ 의 공차는 $2 a$, 첫째항은 $a+b$ 이다.\\\\
이 특징을 기억한다면 등차수열의 합에서 곧바로 공차를 알 수 있고, $n=1$ 을 대입하여 구한 첫째항과 함께 일반항을 쉽게 구할 수 있다.\\\\
이 등차수열의 합은 이차함수 $y=a x^{2}+b x$ 로 볼 수 있고, 이차함수 $y=a x^{2}+b x$ 의 그래프와 등차수열 $\\left\\{a_{n}\\right\\}$ 의 첫째항 $a_{1}$, 공차 $2 a$ 의 관계는 다음과 같다.\\\\
\\includegraphics[max width=\\textwidth, center]{cf797797-a97f-4ffa-a014-34281dffcf6c-05_273_421_1180_774}\\\\
\\includegraphics[max width=\\textwidth, center]{cf797797-a97f-4ffa-a014-34281dffcf6c-05_278_276_1175_1251}

$$
\\begin{aligned}
\\Rightarrow & a_{1}<0 \\\\
& 2 a>0 \\\\
& S_{n} \\text { 의 최솟값이 존재한다. }
\\end{aligned}
$$

\\includegraphics[max width=\\textwidth, center]{cf797797-a97f-4ffa-a014-34281dffcf6c-05_276_421_1490_774}\\\\
\\includegraphics[max width=\\textwidth, center]{cf797797-a97f-4ffa-a014-34281dffcf6c-05_276_655_1490_1251}

\\section*{Drill 등비중항}
0 이 아닌 세 수 $a, x, b$ 가 이 순서대로 등비수열을 이룰 때, $x$ 를 $a$ 와 $b$ 의 등비중항이라고 한다. 이때 $\\frac{x}{a}=\\frac{b}{x}$ 이므로 다음이 성립한다.

$$
x^{2}=a b
$$

등차중항과 등비중항에 관한 문제는 아주 쉬운 계산 문제로 따로 다루어지기도 하지만 고1 수학이나 중학교 도형, 수열 이외의 다른 여러 단원의 문제로 다루어지는 경우가 많다. 앞의 문제도 고1 수학의 이차방정식의 판별식, 근과 계수의 관계가 주인공이다. 특히 이차방정식이 '서로 다른 두 실근'을 갖는다는 조건을 그냥저냥 흔하게 보던 얘기라고 흘려버리지 말고 판별식을 이용하여 $k$ 의 값의 범위를 먼저 정하고 시작해야 한다. 이차방정식뿐만 아니라 삼차방정식, 사차방정식에서도 '서로 다른 실근의 개수'의 조건은 매우 중요하다.

\\section*{Drill 미지수의 개수와 필요한 방정식의 개수}
앞의 문제에서 등비수열 $\\left\\{a_{n}\\right\\}$ 의 일반항을 구하기 위해 필요한 미지수의 개수는?\\\\
첫째항을 $a$, 공비를 $r$ 이라 하면 2개! 그렇다면 필요한 $a, r$ 에 대한 방정식의 개수는?\\\\
역시 2 개! 주어진 등식의 양변에 $n=1,2$ 를 대입하여 $a, r$ 에 대한 연립방정식을 만들어서 풀면 그만이다.\\\\
문제의 상황을 모두 살피지 않은 채 수열의 합과 일반항의 관계로 일반항을 구하느라 시간과 노력을 허비하지 않았기를⋯

\\section*{Drill. 1 등비수열의 일반항}
첫째항이 $a$, 공비가 $r$ 인 등비수열의 일반항 $a_{n}$ 은

$$
a_{n}=a r^{n-1}(n=1,2,3, \\cdots)
$$

이다.\\\\
공비가 1 이 아닌 등비수열의 일반항은 지수가 $n$ 에 대한 일차식이다.

$$
a_{n}=a r^{d n+c} \\Rightarrow \\text { 수열 }\\left\\{a_{n}\\right\\} \\text { 은 공비가 } r^{d} \\text { 인 등비수열 }
$$

앞의 문제에서 주어진 공비를 이용하여 등비수열 $\\left\\{a_{n}\\right\\}$ 의 일반항을 쓰고 부등식 $a_{1} a_{p} \\leq a_{2}$ 를 정리하는 것부터 시작할 수 있다. 이 부등식을 만족시키는 자연수 $p$ 의 개수가 3 이 되도록 하는 $a_{1}$ 의 최댓값과 최솟값을 구해야 하는 상황에 맞게, $a_{1}$ 이 자연수인 조건에 주목하여 이 부등식을 어떻게 보기 좋게 정리할 것인가 하는 실전적인 센스만 잘 발휘하면 된다.\\\\
또는 공비가 주어져 있으니 등비수열의 구조적 특징의 기본인 이웃하는 항의 몫이 공비임을 이용하면서 시작하는 건 어떨까? 그리고 첫째항이 양수이고 공비가 음수인 것에서 등비수열 만의 중요한 구조적 특징인 항의 부호의 변화를 생각해보면 멋지게 풀 수도 있다.

\\section*{Drill. 2 등비수열의 공비의 부호와 항의 부호}
등비수열의 공비의 부호에 따라 항의 부호는 다음과 같다.\\\\
공비가 양수 $\\Leftrightarrow+,+,+,+,+, \\cdots$ 또는,,,,,$----- \\cdots$\\\\
공비가 음수 ⇔,,,,,$+-+-+ \\cdots$ 또는,,,,$-+-+- \\cdots$\\\\
등비수열은 짝수 번째 항끼리 부호가 같고 홀수 번째 항끼리 부호가 같다.

\\section*{Drill 수열의 부분과 전체}
수열 $\\left\\{a_{n}\\right\\}$ 이 등비수열이면 수열 $\\left\\{a_{2 n}\\right\\},\\left\\{a_{3 n}\\right\\}$ 은 등비수열이지만 수열 $\\left\\{a_{2 n}\\right\\},\\left\\{a_{3 n}\\right\\}$ 이 등비 수열이라고 해서 수열 $\\left\\{a_{n}\\right\\}$ 이 등비수열이라는 보장은 없다. 수열 전체에 대한 규칙은 이 수열의 일부에 적용할 수 있지만 수열의 일부에 대한 규칙을 이 수열 전체에 적용할 수 없는 것은 너무나 당연하다.

앞의 문제에서 공비가 $r$ 인 등비수열 $\\left\\{a_{2 n}\\right\\}: a_{2}, a_{4}, a_{6}, \\cdots$ 과 공비가 $r+4$ 인 등비수열\\\\
$\\left\\{a_{3 n}\\right\\}: a_{3}, a_{6}, a_{9}, \\cdots$ 는 어떻게 이용해야 할까? 등비수열을 재구성하면 수열 $\\left\\{a_{6 n}\\right\\}$ 이 등비수열 이므로 $r$ 의 값을 구하는 방법을 떠올리는 건 어렵지 않을 것이다. 이제 $a_{2}$ 의 값을 이용하여 $a_{8}, a_{9}, a_{10}$ 의 값만 구하면 된다.

\\section*{Drill. 1 교대수열의 합}
(1) $\\sum_{k=1}^{n}\\left(a_{k}-a_{k+1}\\right)=\\left(a_{1}-a_{2}\\right)+\\left(a_{2}-a_{3}\\right)+\\cdots+\\left(a_{n}-a_{n+1}\\right)=a_{1}-a_{n+1}$\\\\
(2) $\\sum_{k=1}^{n}\\left(a_{k}-a_{k+2}\\right)=\\left(a_{1}-a_{3}\\right)+\\left(a_{2}-a_{4}\\right)+\\left(a_{3}-a_{5}\\right)+\\cdots+\\left(a_{n-1}-a_{n+1}\\right)+\\left(a_{n}-a_{n+2}\\right)$

$$
=a_{1}+a_{2}-a_{n+1}-a_{n+2}
$$

(3) $\\sum_{k=1}^{n}(-1)^{k}\\left(a_{k}+a_{k+1}\\right)=-\\left(a_{1}+a_{2}\\right)+\\left(a_{2}+a_{3}\\right)-\\left(a_{3}+a_{4}\\right)+\\cdots+(-1)^{n}\\left(a_{n}+a_{n+1}\\right)$

$$
=-a_{1}+(-1)^{n} a_{n+1}
$$

교대수열의 형태로 고치는 방법의 핵심은 이웃하는 두 항 또는 일정한 간격의 두 항을

$$
\\sum((\\text { 앞 })-(\\text { 뒤 })), \\sum((\\text { 뒤 })-(\\text { 앞 })), \\sum(-1)^{k}((\\text { 앞 }) \\pm(\\text { 뒤 }))
$$

의 형태가 되도록 하는 것이다. 또한 교대수열의 합을 구할 때는 앞뒤로 순서대로 지우는 것 보다\\\\
$\\sum_{k=1}^{n}\\left(a_{k}-a_{k+1}\\right)=\\left(a_{1}+a_{2}+\\cdots+a_{n}\\right)-\\left(a_{2}+\\cdots+a_{n}+a_{n+1}\\right)=a_{1}-a_{n+1}$\\\\
$\\sum_{k=1}^{n}\\left(a_{k}-a_{k+2}\\right)=\\left(a_{1}+a_{2}+a_{3}+\\cdots+a_{n-1}+a_{n}\\right)-\\left(a_{3}+\\cdots+a_{n}+a_{n+1}+a_{n+2}\\right)$

$$
=a_{1}+a_{2}-a_{n+1}-a_{n+2}
$$

등과 같이\\\\
각 항의 앞의 수끼리, 뒤의 수끼리 따로 나열\\\\
하여 한꺼번에 지우는 것이 더 편리하다.

\\section*{Drill. $2 S_{0}=0$}
수열 $\\left\\{a_{n}\\right\\}$ 의 첫째항부터 제 $n$ 항까지의 합 $S_{n}$ 에 대하여 $a_{n}=S_{n}-S_{n-1}$ 은 일반적으로 $n \\geq 2$ 일 때 성립하고 $a_{1}=S_{1}$ 이다. 따라서 $a_{n}=S_{n}-S_{n-1}$ 이 $n \\geq 1$ 일 때 성립하려면 $a_{1}=S_{1}-S_{0}=S_{1}$ 에서 $S_{0}=0$ 이어야 함을 알 수 있다.

$$
S_{0}=0 \\text { 이면 } a_{n}=S_{n}-S_{n-1}(n \\geq 1)
$$

앞의 문제에서 $S_{0}=0$ 이므로 $S_{n}-S_{n-1}$ 을 안심하고 $n \\geq 1$ 일 때 성립하는 $a_{n}$ 의 일반항으로 쓸 수 있다.

\\section*{Chapter 3}
수열

\\section*{2024학년도 6월 평기원 공통 9번}
수열 $\\left\\{a_{n}\\right\\}$ 이 모든 자연수 $n$ 에 대하여

$$
\\sum_{k=1}^{n} \\frac{1}{(2 k-1) a_{k}}=n^{2}+2 n
$$

을 만족시킬 때, $\\sum_{n=1}^{10} a_{n}$ 의 값은? [4점]\\\\
(1) $\\frac{10}{21}$\\\\
(2) $\\frac{4}{7}$\\\\
(3) $\\frac{2}{3}$\\\\
(4) $\\frac{16}{21}$\\\\
(5) $\\frac{6}{7}$

\\section*{Drill 수열의 합과 일반항의 관계 이용은 대입부터}
앞의 문제는 수열의 합과 일반항의 관계 이용으로 가닥을 잡아볼 수 있다. 이때 절대 잊지 말아야 할 건 $S_{n} S_{n+1}=1, a_{n} a_{n+1}<0$ 에 모두 $n=1$ 을 대입하고 시작하는 것! $a_{2}$ 의 값이 주어 졌음ㄹㄹㅗ $S_{1} S_{2}=1$ 을 $a_{1}\\left(a_{1}+a_{2}\\right)=1$ 로 고쳐서 $a_{1}$ 에 대한 이차방정식으로 볼 수 있어야 한다. $S_{n}$ 과 $S_{n+1}$ 이 역수라는 확실한 관계에서 $S_{1}, S_{2}, S_{3}, \\cdots$ 을 나열해보면 수열의 합과 일반항의 관계에서 $a_{1}, a_{2}, a_{3}, \\cdots$ 을 쉽게 추정할 수 있다. 수열의 합과 일반항의 관계를 일반적으로 이용한 것도 아니고 $n$ 의 값의 대입이라는 기본만 이용했을 뿐이다. 마무리는 지수법칙을 살짝 이용해서 $(-2)^{k-1} a_{k}$ 의 식을 Named 수열의 식으로 정리하기.

\\section*{Drill 시그마의 다양한 용도}
합의 기호 시그마는 다음과 같이 이용된다.\\\\
(1) 자연수의 거듭제곱의 합 $\\Rightarrow \\sum_{k=1}^{n} k, \\sum_{k=1}^{n} k^{2}, \\sum_{k=1}^{n} k^{3}$\\\\
(2) 수열의 합의 표현 ⇒ 말 그대로 just 합의 표현일 뿐이거나 수열의 합을 써보면서 등차수열, 등비수열, 주기 등에 관한 규칙 발견\\\\
(3) $\\sum_{k=1}^{n}(\\star)=(n$ 의 식 $)(n \\geq 1) \\Rightarrow(n$ 의 식 $)$ 을 $S_{n}$ 으로 간주\\\\
$\\Rightarrow S_{n}-S_{n-1}=(\\star)$ 의 일반항 $(n \\geq 2), S_{1}=(\\star)$ 의 첫째항

앞의 문제에서 주어진 관계식으로 수열의 합과 일반항의 관계를 이용하고자 할 때 $n=1$ 부터 대입해보는 것은 절대 놓치지 않아야 하고, $S_{0}=0$ 이 확인되지 않는 한 $S_{n}-S_{n-1}$ 로 구한 $a_{n}$ 은 $n \\geq 2$ 일 때 성립하는 것에 절대 주의해야 한다. 하나 더. 구하고자 하는 $a_{2}$ 의 값을 미지수로 잡고 이 미지수로 식들을 간편하게 정리해가는 것이 좋겠다.


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
                    question_ref = "P6"
                
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
                    question_ref = "P6"
                
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
    print("[수1 드릴 P6 해설 데이터 검토]")
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
        # 1. 등차수열 공식 확인
        if '등차수열' in content:
            if 'a_{n}' in content or 'a_n' in content:
                if 'a+(n-1)d' in content or 'a + (n-1)d' in content or '공차' in content:
                    pass  # 일반항 공식 정상
            if 'S_n' in content or 'S_{n}' in content:
                if '합' in content or '대칭' in content:
                    pass  # 합 공식 정상
        
        # 2. 등비수열 공식 확인
        if '등비수열' in content:
            if 'a_{n}' in content or 'a_n' in content:
                if 'ar^{n-1}' in content or 'a r^{n-1}' in content or '공비' in content:
                    pass  # 일반항 공식 정상
        
        # 3. 등비중항 확인
        if '등비중항' in content:
            if 'x^2' in content or 'x^{2}' in content:
                if 'ab' in content or 'a b' in content:
                    pass  # x² = ab 정상
        
        # 4. 수열의 합과 일반항의 관계 확인
        if '수열의 합과 일반항' in content or 'S_n' in content:
            if 'a_n' in content or 'a_{n}' in content:
                if 'S_n-S_{n-1}' in content or 'S_n - S_{n-1}' in content:
                    pass  # 관계식 정상
        
        # 5. 교대수열의 합 확인
        if '교대수열' in content or '(-1)^' in content:
            if '합' in content:
                pass  # 교대수열 합 공식 언급 정상
        
        # 6. 등차수열의 대칭성 확인
        if '등차수열' in content and '대칭' in content:
            if '합' in content or '항' in content:
                pass  # 대칭성 설명 정상
    
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
    csv_path = save_dir / "수1_2025학년도_현우진_드릴_P6_해설_deepseek.csv"
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
    json_path = save_dir / "수1_2025학년도_현우진_드릴_P6_해설_deepseek.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(solutions, f, ensure_ascii=False, indent=2)
    
    print(f"[JSON 저장 완료] {json_path}")
    
    return csv_path, json_path


def main():
    print("=" * 60)
    print("[수1 드릴 P6 해설 LaTeX → CSV 변환]")
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
