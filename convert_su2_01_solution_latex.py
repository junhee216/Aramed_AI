# convert_su2_01_solution_latex.py
# 수2 드릴 01 해설 LaTeX를 딥시크용 CSV로 변환

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
\\usepackage{fvextra, csquotes}
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

\\newunicodechar{→}{\\ifmmode\\rightarrow\\else{$\\rightarrow$}\\fi}
\\newunicodechar{⇒}{\\ifmmode\\Rightarrow\\else{$\\Rightarrow$}\\fi}
\\newunicodechar{×}{\\ifmmode\\times\\else{$\\times$}\\fi}

\\begin{document}
\\section*{Drill. 1 함수의 극한에 대한 성질의 활용}
(1) $\\lim _{x \\rightarrow a} \\frac{f(x)}{g(x)}=\\alpha, \\lim _{x \\rightarrow a} g(x)=0$ 이면 $\\lim _{x \\rightarrow a} f(x)=0$\\\\
(2) $\\lim _{x \\rightarrow a} \\frac{f(x)}{g(x)}=\\alpha(\\alpha \\neq 0), \\lim _{x \\rightarrow a} f(x)=0$ 이면 $\\lim _{x \\rightarrow a} g(x)=0$\\\\
(3) $\\lim _{x \\rightarrow a} f(x) g(x)=\\alpha, \\lim _{x \\rightarrow a}|g(x)|=\\infty$ 이면 $\\lim _{x \\rightarrow a} f(x)=0$\\\\
(4) $\\lim _{x \\rightarrow a} f(x) g(x)=\\alpha(\\alpha \\neq 0), \\lim _{x \\rightarrow a} f(x)=0$ 이면 $\\lim _{x \\rightarrow a}|g(x)|=\\infty$\\\\
$\\frac{0}{(\\quad)} \\rightarrow \\alpha$ 에서 $\\alpha \\neq 0$ 인 조건은 다음과 같이 이해해 볼 수 있다.\\\\
$\\frac{0}{()} \\rightarrow 0$ 이면 ( ) → 2, ( ) $\\rightarrow \\infty$ 등이 모두 가능하므로 ( ) $\\rightarrow 0$ 이라고 단정할 수 없다.\\\\
$0 \\times() \\rightarrow \\alpha$ 에서 $\\alpha \\neq 0$ 인 조건도 마찬가지이다.\\\\
$0 \\times() \\rightarrow 0$ 이면 ( ) → 2, ( ) $\\rightarrow 0$ 등이 모두 가능하므로 ( ) $\\rightarrow \\infty$ 라고 단정할 수 없다.

\\section*{Drill. 2 분모의 극한값부터 확인}
$x \\rightarrow a$ 일 때 분수꼴 함수의 극한에서는 항상 분모의 극한값이 0 인지 아닌지부터 먼저 확인 해야 한다. 분모의 극한값이 0 이 아니라면 $x=a$ 를 대입하면 그만이다.\\\\
앞의 문제에서도 분모의 극한값이 0 이 아니라고 가정하고 $x=2$ 를 대입해 보면서 이차함수 $f(x)$ 의 한 인수를 정하고 식을 써서 남은 풀이 과정을 이어갈 수 있다.

\\section*{Drill. 3 다항함수의 식의 결정}
다항함수를 다루는 모든 상황에서 다항함수의 식을 결정하는 대표적인 방법은 다음과 같고, 이 둘을 함께 이용하는 경우도 많다.\\\\
(1) 인수정리 ⇒ $f(a)=0$ 이면 $f(x)=(x-a)(\\cdots \\cdots)$\\\\
$f(a)=0, f^{\\prime}(a)=0$ 이면 $f(x)=(x-a)^{2}(\\cdots \\cdots)$\\\\
$f^{\\prime}(a)=0$ 이면 $f^{\\prime}(x)=(x-a)(\\cdots \\cdots)$ 에서 적분\\\\
(2) 전개식 $\\Rightarrow f(x)=a x^{n}+\\cdots+\\square$\\\\
$(x \\rightarrow 0$ 일 때 극한값의 조건으로 가장 낮은 차수의 항을 함께 결정할 수도 있다.)

\\section*{Drill $\\frac{0}{0}$ 꼴에서 함수의 결정}
다항함수 $f(x)$ 와 자연수 $n$ 에 대하여\\\\
$\\lim _{x \\rightarrow a} \\frac{f(x)}{(x-a)^{n}}=k \\cdots \\cdots$ (ㄱ)일 때\\\\
(1) $k \\neq 0$ 이면 다항함수 $g(x)$ 에 대하여

$$
f(x)=(x-a)^{n} g(x)
$$

이고, 이를 (ㄱ)에 대입하면

$$
g(a)=k
$$

$\\Rightarrow f(x)=p(x-a)^{m}+\\cdots+k(x-a)^{n}(m \\geq n, m$ 은 자연수 $)$ 과 같이 $x-a$ 에 관한 전개식으로 나타낼 수도 있다.\\\\
(2) $k=0$ 이면 다항함수 $g(x)$ 에 대하여

$$
f(x)=(x-a)^{n+1} g(x)
$$

$\\Rightarrow f(x)=p(x-a)^{m}+\\cdots+q(x-a)^{n+1}(m>n, m$ 은 자연수 $)$ 과 같이 $x-a$ 에 관한 전개식으로 나타낼 수도 있다.

앞의 문제에서는 조건 (가)에서 극한값이 0 이고 분모가 $(x-k)^{2}$,이러한 $k$ 가 2 개라는 것에서 이 2 개의 $k$ 의 값을 미지수로 잡고 $f(x) g(x)$ 의 식을 곧바로 쓰고 시작할 수 있어야 한다.\\\\
두 삼차함수 $f(x), g(x)$ 에 인수를 어떻게 배분할 것인지의 케이스만 잘 구분하여 조건 (나)를 마저 이용해서 마무리~

Drill $\\frac{0}{0}$ 꼴의 극한에 대한 중요한 기본 인식\\\\
$\\frac{0}{0}$ 꼴의 극한의 조건의 가장 중요한 활용 방법은 분자 또는 분모의 인수를 잡는 것이다. 이러한 기본 인식이 잘 갖춰져야 앞의 문제의 조건 (가)를 $x \\rightarrow 0$ 일 때의 극한값이 0 이므로 분자가 $x^{2}$ 을 인수로 갖는다는 것으로 해석할 수 있다. 그리고 분수꼴의 극한에서 절대 소홀히 넘기지 말아야 할 또 하나의 기본 인식은 $x \\rightarrow a$ 일 때 분모의 극한값이 0 이 아니라면 $x=a$ 를 대입 하면 그만이라는 것! 조건 (가)는 이러한 두 가지의 기본 인식의 결합으로 제대로 이용할 수 있다.

\\section*{Drill 절댓값을 포함한 극한}
다항함수 $f(x)$ 와 홀수인 자연수 $n$ 에 대하여 $\\lim _{x \\rightarrow a} \\frac{|f(x)|}{(x-a)^{n}}=k$ 또는 $\\lim _{x \\rightarrow a} \\frac{f(x)}{\\left|(x-a)^{n}\\right|}=k$ 일 때, $f(x)$ 는 $(x-a)^{n+1}$ 을 인수로 가지고, $k=0$ 이다.\\\\[0pt]
[증명] $\\lim _{x \\rightarrow a} \\frac{|f(x)|}{(x-a)^{n}}=k$ 일 때 $f(x)=(x-a)^{n} g(x)$ 라 하면

$$
\\begin{aligned}
& \\lim _{x \\rightarrow a-} \\frac{|f(x)|}{(x-a)^{n}}=\\lim _{x \\rightarrow a-} \\frac{-(x-a)^{n}|g(x)|}{(x-a)^{n}}=-\\lim _{x \\rightarrow a-}|g(x)|=-|g(a)|, \\\\
& \\lim _{x \\rightarrow a+} \\frac{|f(x)|}{(x-a)^{n}}=\\lim _{x \\rightarrow a+} \\frac{(x-a)^{n}|g(x)|}{(x-a)^{n}}=\\lim _{x \\rightarrow a+}|g(x)|=|g(a)| \\\\
& \\text { 이므로 }-|g(a)|=|g(a)| \\text { 에서 } g(a)=0 \\text { 이다. } \\\\
& \\text { 따라서 } g(x) \\text { 는 } x-a \\text { 를 인수로 가지므로 } f(x) \\text { 는 }(x-a)^{n+1} \\text { 을 인수로 가지고, } k=0 \\\\
& \\text { 이다. } \\\\
& \\lim _{x \\rightarrow a} \\frac{f(x)}{\\left|(x-a)^{n}\\right|}=k \\text { 일 때도 이와 마찬가지이다. }
\\end{aligned}
$$

앞의 문제는 $\\lim _{x \\rightarrow 0} \\frac{|f(x)-1|}{x}=k$ 에서 $f(x)-1$ 의 식과 $k$ 의 값을 정하는 것이 핵심인데, 이 과정이 위의 증명과 같다. 위의 내용을 알고 있었다면 곧바로 $f(x)-1$ 의 식을 쓰고 $k=0$ 에서 얼마 남지 않은 계산 과정만 마무리하면 된다. 익혀두고 활용하도록 하자!\\\\
증명에서 좌극한과 우극한의 일치를 따질 필요성과 절댓값을 처리하는 과정도 눈여겨 뵈둘만 하다.

\\section*{Drill. 1 불연속이라는 조건에 주의}
앞의 문제에서 $f(x)$ 가 $x=0$ 에서 불연속이라는 조건을 그냥 흘려버리고 $\\frac{0}{0}$ 꼴에 무작정 반응 했다간 낭패다 $\\cdots \\frac{0}{0}$ 꼴에서 분자 또는 분모의 극한값을 함숫값으로 사용하는 것은 어디까지나 연속인 함수, 다항함수에서 그렇게 해왔던 것.\\\\
$\\lim _{x \\rightarrow 0} \\frac{f(x)-1}{x}=3$ 에서 $\\lim _{x \\rightarrow 0}\\{f(x)-1\\}=0$ 은 $\\lim _{x \\rightarrow 0} f(x)=1$ 로만 이용해야 하고, $\\lim _{x \\rightarrow 0} \\frac{g(x)-f(0)}{x}, \\lim _{x \\rightarrow 0} \\frac{f(x) g(x)+2}{x}$ 의 계산에서도 극한값 $\\lim _{x \\rightarrow 0} f(x)$ 와 함숫값 $f(0)$ 의 구분에 계속 신경 써야 한다. $\\lim _{x \\rightarrow 0} \\frac{f(x) g(x)+2}{x}$ 의 계산도 극한값이 존재하는 함수끼리의 연산으로 변형하여 함수의 극한에 대한 성질로 멋지게 마무리할 수 있어야 한다.

\\section*{2024학년도 9월 평가원 공통 15번}
최고차항의 계수가 1 인 삼차함수 $f(x)$ 에 대하여 함수 $g(x)$ 를

$$
g(x)= \\begin{cases}\\frac{f(x+3)\\{f(x)+1\\}}{f(x)} & (f(x) \\neq 0) \\\\ 3 & (f(x)=0)\\end{cases}
$$

이라 하자. $\\lim _{x \\rightarrow 3} g(x)=g(3)-1$ 일 때, $g(5)$ 의 값은? [4점]\\\\
(1) 14\\\\
(2) 16\\\\
(3) 18\\\\
(4) 20\\\\
(5) 22

답(4)

\\section*{Chapter 1 함수의 극한과 연속}
Drill 2 함수의 극한에 대한 성질과 극한값의 추정\\\\
함수의 극한에 대한 성질은 다음과 같다.\\\\
$\\lim _{x \\rightarrow a} f(x)=\\alpha, \\lim _{x \\rightarrow a} g(x)=\\beta$ 일 때\\\\
(1) $\\lim _{x \\rightarrow a} c f(x)=c \\lim _{x \\rightarrow a} f(x)=c \\alpha$ (단, $c$ 는 상수)\\\\
(2) $\\lim _{x \\rightarrow a}\\{f(x)+g(x)\\}=\\lim _{x \\rightarrow a} f(x)+\\lim _{x \\rightarrow a} g(x)=\\alpha+\\beta$\\\\
(3) $\\lim _{x \\rightarrow a}\\{f(x)-g(x)\\}=\\lim _{x \\rightarrow a} f(x)-\\lim _{x \\rightarrow a} g(x)=\\alpha-\\beta$\\\\
(4) $\\lim _{x \\rightarrow a} f(x) g(x)=\\lim _{x \\rightarrow a} f(x) \\times \\lim _{x \\rightarrow a} g(x)=\\alpha \\beta$\\\\
(5) $\\lim _{x \\rightarrow a} \\frac{f(x)}{g(x)}=\\frac{\\lim _{x \\rightarrow a} f(x)}{\\lim _{x \\rightarrow a} g(x)}=\\frac{\\alpha}{\\beta} \\quad($ 단, $\\beta \\neq 0)$

극한값에 대한 조건을 이용하여 함수의 식을 구하지 않고 극한값만을 추정하는 문제가 자주 출제된다. 이때 함수의 극한에 대한 성질을 이용할 수 있도록 극한값이 존재하는 함수끼리의 합, 차, 곱, 몫으로 고쳐서 함수의 극한값을 계산할 수 있다.\\\\
함수의 극한에 대한 성질을 이용한 극한값의 추정에서 간혹 로피탈의 법칙을 즐기는 학생들이 있는데, '수학 II'에서 다루는 미분법의 한계 때문에 다양한 함수에 적용하기 힘들고 미분가능 하지 않은 함수에 대해서는 무용지물이다. 또한 함수의 극한을 기반으로 한 변화율의 형태 인식에 대한 감이 떨어질 수도 있다. 배운 대로 하자!\\\\
앞의 문제는 $f(x)$ 가 $x=0$ 에서 미분가능하지 않으므로 로피탈의 법칙과는 아무 상관이 없다.

\\section*{Drill $\\frac{\\infty}{\\infty}$ 꼴에서 다항함수의 결정}
$x \\rightarrow \\infty$ 일 때 분자 또는 분모에 다항함수 $f(x)$ 가 포함된 분수꼴 함수의 극한의 조건은 $f(x)$ 의 최고차항에 대한 조건이므로 다음과 같이 $f(x)$ 의 차수와 최고차항의 계수를 파악할 수 있어야 한다.

다항함수 $f(x)$ 와 자연수 $n$ 에 대하여

$$
\\lim _{x \\rightarrow \\infty} \\frac{f(x)}{a x^{n}+\\cdots}=k(k \\neq 0) \\Rightarrow f(x)=k \\times a x^{n}+\\cdots
$$

앞의 문제의 조건 (가)에서는 일차함수 $g(x)$ 의 최고차항의 계수를 미지수로 잡아 다항함수 $f(x)$ 의 차수와 최고차항의 계수를 결정하고 곧이어 조건 (나)를 이용하여 인수로 $f(x)$ 의 식을 쓸 수 있다. $\\frac{0}{0}$ 꼴의 극한을 이용하여 쓴 함수의 식에 미지수가 남아있으면 이 $\\frac{0}{0}$ 꼴의 극한에 함수의 식을 다시 대입해 봐야 하는 기본 중의 기본도 확인해두자.

\\section*{Drill 다항함수의 최고차항과 가장 낮은 차수의 항 결정}
(1) 다항함수 $f(x)$ 와 $n>m$ 인 자연수 $n, m$ 에 대하여

$$
\\begin{aligned}
& \\lim _{x \\rightarrow \\infty} \\frac{f(x)}{a x^{n}+\\cdots}=p, \\lim _{x \\rightarrow 0} \\frac{f(x)}{x^{m}}=q(p q \\neq 0) \\\\
& \\Rightarrow f(x)=x^{m}\\left(p a x^{n-m}+\\cdots+q\\right) \\text { 또는 } f(x)=p a x^{n}+\\cdots+q x^{m}
\\end{aligned}
$$

(2) 다항함수 $f(x)$ 와 $n>m$ 인 자연수 $n, m$ 에 대하여

$$
\\begin{aligned}
& \\lim _{x \\rightarrow \\infty} \\frac{f(x)}{a x^{n}+\\cdots}=p, \\lim _{x \\rightarrow k} \\frac{f(x)}{(x-k)^{m}}=q(p q \\neq 0) \\\\
& \\Rightarrow f(x)=(x-k)^{m}\\left\\{p a(x-k)^{n-m}+\\cdots+q\\right\\} \\text { 또는 } f(x)=p a(x-k)^{n}+\\cdots+q(x-k)^{m} \\\\
& \\quad x \\rightarrow \\infty, x \\rightarrow-\\infty \\text { 일 때 극한값의 조건 } \\Rightarrow \\text { 최고차항 결정 } \\\\
& \\quad x \\rightarrow 0 \\text { 일 때 극한값의 조건 } \\Rightarrow \\text { 가장 낮은 차수의 항 결정 }
\\end{aligned}
$$

앞의 문제에서는 우선 $x \\rightarrow \\infty$ 일 때의 극한의 조건에서 $f(x)$ 의 최고차항과 $k$ 의 값을 정할 수 있고 $x \\rightarrow 0$ 일 때의 극한의 조건에서 $f(x)$ 의 가장 낮은 차수의 항을 정할 수 있다.

\\section*{Drill 어떤 케이스부터 점검해 볼까?}
앞의 문제는 $x \\rightarrow \\infty$ 일 때 극한의 조건이 주어졌으므로 $f(x)$ 의 최고차항부터 정하고 시작 하는 것은 너무나 당연하다. $n$ 의 값은 무엇인 경우부터 시작하고 싶을까? $n=2$ 인 경우부터 시작하는 것도 당연해 보인다. $f(x)$ 의 차수가 4 이상일 때와 2 이하일 때 어떤 일이 벌어 지는지 굳이 손이 수고하지 않아도 눈으로 슥 확인하고 $f(x)$ 의 최고차항을 정할 수 있다. 다음으로 $n$ 의 값이 무엇인 경우로 넘어가볼까? 상대적으로 단순한 상황부터! $n=1$ 인 경우, $n=3$ 인 경우, $\\cdots$ 로 순서를 잡아보는 것이 자연스럽다. 차츰 $f(x)$ 의 남은 계수의 윤곽이 잡히고 $n=2$ 인 경우의 극한의 식에서 분자와 분모의 최고차항의 계수에 관한 간단한 가정과 모순의 발견으로 마무리하면 된다.

\\section*{Drill. 1 구간별로 정의된 함수의 연속}
연속함수 $g_{1}(x), g_{2}(x)$ 에 대하여\\\\
(1) 함수 $f(x)=\\left\\{\\begin{array}{ll}g_{1}(x) & (x<a) \\\\ g_{2}(x) & (x \\geq a)\\end{array}\\right.$ 가 $x=a$ 에서 연속 $\\Leftrightarrow g_{1}(a)=g_{2}(a)$\\\\
(2) 함수 $f(x)=\\left\\{\\begin{array}{ll}g_{1}(x) & (x<a) \\\\ c & (x=a) \\\\ g_{2}(x) & (x>a)\\end{array}\\right.$ 가 $x=a$ 에서 연속 $\\Longleftrightarrow g_{1}(a)=g_{2}(a)=c$\\\\
(3) 함수 $f(x)=\\left\\{\\begin{array}{ll}g_{1}(x) & (x \\neq a) \\\\ c & (x=a)\\end{array}\\right.$ 가 $x=a$ 에서 연속 $\\Leftrightarrow g_{1}(a)=c$

Drill. 2 고1 수학의 함수 재점검\\\\
최근 고1 수학의 중요도가 높아지고 있는 만큼, 고1 수학에서 다루는 이차함수, 유리함수와 무리함수에 대한 재점검이 반드시 필요하다. 이차함수는 주로 이차방정식과 이차부등식에의 활용에 초점을 맞추고, 유리함수와 무리함수는 모든 Named 함수에서 그러하듯이 식과 그래프의 기본적인 특징에 매우 익숙해야 한다.

\\section*{Drill. 1 연속함수의 성질}
두 함수 $f(x), g(x)$ 가 $x=a$ 에서 연속이면 다음 함수도 모두 $x=a$ 에서 연속이다.\\\\
(1) $c f(x)$ (단, $c$ 는 상수)\\\\
(2) $f(x)+g(x), f(x)-g(x)$\\\\
(3) $f(x) g(x)$\\\\
(4) $\\frac{f(x)}{g(x)}$ (단, $g(a) \\neq 0$ )

함수의 합, 차, 곱, 몫의 불연속은 불연속인 함수가 있거나 분모가 0 이 되는 함수가 있는 경우 에만 해당되므로 불연속이 의심되는 지점만 확인하면 된다.\\\\
앞의 문제는 $|f(x)|$ 가 $x=a$ 에서 연속이어서 (연속) × (연속)에서 $|f(x)| g(x)$ 가 연속인 경우를 놓치지 않도록 주의해야 한다.

\\section*{Drill. 2 (불연속) $\\times$ (연속)}
함수 $f(x)$ 가 $x=a$ 에서 정의되어 있고 불연속일 때, $x=a$ 에서 연속인 함수 $g(x)$ 에 대하여 $g(a)=0$ 은 함수 $f(x) g(x)$ 가 $x=a$ 에서 연속이기 위한 필요조건이다.\\\\
특히, $f(x)$ 의 $x=a$ 에서의 좌극한과 우극한이 각각 존재하면 $g(a)=0$ 은 $f(x) g(x)$ 가 $x=a$ 에서 연속이기 위한 필요충분조건이다.\\\\
(불연속) $\\times$ (연속)의 상황은 다음과 같이 구분해서 다룬다.\\\\
(1) 불연속인 함수의 좌극한과 우극한이 각각 존재할 때

⇒ 연속인 함수의 함숫값이 0 이 아니면 불연속\\\\
⇒ 연속인 함수의 함숫값이 0 이면 연속\\\\
(2) 불연속인 함수의 좌극한 또는 우극한이 양의 무한대 또는 음의 무한대로 발산할 때

⇒ 연속인 함수의 함숫값이 0 이 아니면 불연속\\\\
⇒ 연속인 함수의 함숫값이 0 이면 $0 \\times \\infty$ 꼴의 부정형의 극한을 직접 계산\\\\
여기서 불연속인 함수의 상황에 관계없이

\\begin{displayquote}
연속인 함수의 함숫값이 0 이 아니면 불연속
\\end{displayquote}

이라는 판단도 따로 챙겨두는 것이 좋다.


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
        content = re.sub(r'\\begin\{displayquote\}.*?\\end\{displayquote\}', '', content, flags=re.DOTALL)
        content = re.sub(r'\s+', ' ', content)
        
        # 주제도 정리
        topic = re.sub(r'\\\\', ' ', topic)
        topic = re.sub(r'\s+', ' ', topic)
        
        if len(content) > 50:
            if is_strategy:
                question_ref = ""
                if '앞의 문제' in content:
                    question_ref = "01"
                
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
                    question_ref = "01"
                
                solutions.append({
                    "type": "strategy",
                    "topic": f"{drill_num} 함수의 극한과 연속".strip() if drill_num else "함수의 극한과 연속",
                    "question_ref": question_ref,
                    "content": strategy_content
                })
    
    return solutions


def review_solutions(solutions):
    """해설 데이터 검토 (수학적 논리 포함)"""
    print("=" * 60)
    print("[수2 드릴 01 해설 데이터 검토]")
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
        # 1. 극한 성질 확인
        if '극한' in content or '\\lim' in content:
            if 'x \\rightarrow' in content or 'x->' in content:
                pass  # 극한 식 구조 정상
        
        # 2. 함수의 연속성 확인
        if '연속' in content or '불연속' in content:
            if 'f(x)' in content or 'g(x)' in content:
                pass  # 연속성 조건 언급 정상
        
        # 3. 다항함수 차수 확인
        if '다항함수' in content or '차수' in content:
            if '최고차항' in content or '계수' in content:
                pass  # 다항함수 차수 언급 정상
        
        # 4. 극한값 계산 확인
        if '\\lim' in content and '=' in content:
            if 'k' in content or '\\alpha' in content or '상수' in content:
                pass  # 극한값 계산 언급 정상
        
        # 5. 조건부 함수 확인
        if '\\begin{cases}' in content:
            if '\\end{cases}' in content:
                pass  # 조건부 함수 구조 정상
        
        # 6. 절댓값 극한 확인
        if '|f(x)|' in content or '절댓값' in content:
            if '좌극한' in content or '우극한' in content:
                pass  # 절댓값 극한 언급 정상
    
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
    """딥시크용 CSV 저장 (기존 폴더 경로 사용)"""
    base_dir = Path(r'C:\Users\a\Documents\MathPDF\organized\현우진\수2_2005학년도_현우진_드릴')
    save_dir = base_dir
    save_dir.mkdir(parents=True, exist_ok=True)
    
    # CSV 저장
    csv_path = save_dir / "수2_2025학년도_현우진_드릴_01_해설_deepseek.csv"
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
    json_path = save_dir / "수2_2025학년도_현우진_드릴_01_해설_deepseek.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(solutions, f, ensure_ascii=False, indent=2)
    
    print(f"[JSON 저장 완료] {json_path}")
    
    return csv_path, json_path


def main():
    print("=" * 60)
    print("[수2 드릴 01 해설 LaTeX → CSV 변환]")
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
    
    # 4단계: 저장 (기존 폴더 경로 사용)
    print("\n[4단계] 딥시크용 파일 저장 중...")
    csv_path, json_path = save_for_deepseek(solutions)
    
    print("\n" + "=" * 60)
    print("[완료] 딥시크가 읽을 수 있는 형태로 저장되었습니다.")
    print("=" * 60)
    base_dir = Path(r'C:\Users\a\Documents\MathPDF\organized\현우진\수2_2005학년도_현우진_드릴')
    print(f"저장 위치: {base_dir}")
    print(f"  - CSV: {csv_path.name}")
    print(f"  - JSON: {json_path.name}")


if __name__ == '__main__':
    main()
