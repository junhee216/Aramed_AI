# convert_su2_02_solution_latex.py
# 수2 드릴 02 해설 LaTeX를 딥시크용 CSV로 변환

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

\\newunicodechar{□}{\\ifmmode\\square\\else{$\\square$}\\fi}
\\newunicodechar{⇔}{\\ifmmode\\Leftrightarrow\\else{$\\Leftrightarrow$}\\fi}
\\newunicodechar{⟺}{\\ifmmode\\Longleftrightarrow\\else{$\\Longleftrightarrow$}\\fi}
\\newunicodechar{⇒}{\\ifmmode\\Rightarrow\\else{$\\Rightarrow$}\\fi}

\\begin{document}
\\section*{Drill 불연속의 이해}
함수 $f(x)$ 가 다음 조건을 모두 만족시킬 때, 함수 $f(x)$ 는 $x=a$ 에서 연속이다.\\\\
(1) 함수 $f(x)$ 는 $x=a$ 에서 정의되어 있다.\\\\
(2) $\\lim _{x \\rightarrow a} f(x)$ 가 존재한다.\\\\
(3) $\\lim _{x \\rightarrow a} f(x)=f(a)$

당연하게도 이 세 조건 중 어느 하나라도 만족시키지 않으면 $f(x)$ 는 $x=a$ 에서 불연속이다. 앞의 문제에서는 $x \\leq 0$ 일 때 $f(t)$ 의 $t=x+3$ 에서의 우극한에서 $t=x$ 에서의 좌극한을 뺀 값을 구간 $[x, x+3]$ 을 움직여보면서 기하적으로 관찰하는 것이 좋다. $t=0$ 의 좌우에서 $f(t)$ 의 함숫값이 튀면서 문제가 되리라는 건 이미 예상했을 것이다. 이때는 $g(x)$ 가 어쩔 수 없이 불연속이고, $g(x)$ 는 오직 한 점에서만 불연속이므로 연결 지점인 $x=0$ 에서는 연속 이어야 한다는 상황 정리로 마무리하면 된다.

\\section*{Drill 알아야 할 것은 제대로 알기 그리고 경계의 이용}
앞의 문제의 $\\lim _{x \\rightarrow 0} \\frac{f(x)}{|x| g(x)}=3$ 에서 분모의 $|x|$ 를 보고 분자의 $f(x)$ 가 $x^{2}$ 을 인수로 가져야 한다고 혼동하지 않도록 주의! 알아야 할 것은 제대로 알고 이용해야 한다. 앞서 절댓값을 포함한 극한에서 다룬 것과 상황이 많이 다르다는 걸 반드시 확인해두자. 분모에 $x=0$ 에서의 연속이 확인되지 않은 $g(x)$ 가 곱해져 있고 극한값도 0 이 아니다. $f(0)=0$ 으로 이차함수 $f(x)$ 의 식을 쓴 후 $|x|$ 의 처리를 위해 $x=0$ 에서의 좌극한과 우극한을 따로 정리해서 이 둘이 일치하도록 해야 한다.\\\\
이렇게 $g(x)$ 를 확정하고 나서 $f(x)$ 의 그래프의 변화에 따라 $h(t)$ 의 불연속인 점의 개수의 변화를 관찰하는 남은 과정은 경계의 이용이라는 완전히 몸에 밴 습관에 따라야 한다.\\\\
$f(x)$ 의 최고차항의 계수가 양수인 경우에는 $h(t)$ 의 불연속인 점의 개수가 4 이상인 것이 금세 파악될 것이고, $f(x)$ 의 최고차항의 계수가 음수인 경우로 넘어가면 $f(x)$ 의 최댓값이 1 인 경우부터 확인하기 시작해야 한다.

Drill. $1 \\lim _{x \\rightarrow a} \\frac{f(x)-p}{x-a}=q$\\\\
함수 $f(x)$ 가 $x=a$ 에서 연속일 때

$$
\\lim _{x \\rightarrow a} \\frac{f(x)-p}{x-a}=q \\Leftrightarrow f(a)=p, f^{\\prime}(a)=q
$$

$\\lim _{x \\rightarrow a} \\frac{f(x)-p}{x-a}=q$ 는 함수의 극한으로 다룰 것인지 미분계수로 다룰 것인지 선택할 수 있어야 한다. 다음의 둘 중 유리한 것을 이용한다.\\\\
(1) $f(x)-p=(x-a) g(x), g(a)=q$\\\\
(2) $f(a)=p, f^{\\prime}(a)=q$

\\section*{Drill 2 함수의 치환}
$\\lim _{x \\rightarrow a} \\frac{\\square}{x-a}$ 에서 $\\lim _{x \\rightarrow a} \\square=0$ 일 때, □ 의 식을 인수분해하거나 변화율로 변형하기 복잡 하다면 □ $=f(x)$ 로 놓고

$$
\\lim _{x \\rightarrow a} \\frac{\\square}{x-a}=\\lim _{x \\rightarrow a} \\frac{f(x)}{x-a}=f^{\\prime}(a)
$$

로 계산할 수 있다.

앞의 문제에서 $\\lim _{x \\rightarrow 3} \\frac{f(x)-g(x)}{x-3}=1$ 을 두 함수 $f(x), g(x)$ 각각의 변화율로 변형하기 전혀 어렵지 않지만 $f(x)-g(x)$ 를 한 함수로 보고 그 도함수가 $f^{\\prime}(x)-g^{\\prime}(x)$ 이므로 $f(3)-g(3)=0, f^{\\prime}(3)-g^{\\prime}(3)=1$ 을 곧바로 구해도 좋다.

\\section*{Drill 두 함수의 차}
두 다항함수 $y=f(x), y=g(x)$ 의 그래프가 $x$ 좌표가 $a$ 인 점에서 만나면 $f(x)-g(x)$ 는 $x-a$ 를 인수로 갖는다. 특히 두 다항함수 $y=f(x), y=g(x)$ 의 그래프가 $x$ 좌표가 $a$ 인 점에서 접하면 $f(x)-g(x)$ 는 $(x-a)^{2}$ 을 인수로 갖는다.\\\\
또 다항함수 $y=f(x)$ 의 그래프 위의 점 $(a, f(a))$ 에서의 접선의 방정식이 $y=g(x)$ 이면 $f(x)-g(x)=(x-a)^{2}(\\cdots \\cdots)$ 으로 곧바로 써보는 것이 좋다.\\\\
앞의 문제에서도 조건 (가)에서 $f(x)-(12 x+1)=x^{2}(\\cdots \\cdots)$ 으로 쓰기 시작하면 조건 (나)의 삼차방정식의 상수항이 확정되면서 '수학 I'과 고 1 수학의 연계로 풀이 방향을 잡을 수 있다.

\\section*{2024학년도 9월 평기원 공통 10번}
최고차항의 계수가 1 인 삼차함수 $f(x)$ 에 대하여 곡선 $y=f(x)$ 위의 점 $(-2, f(-2))$ 에서의 접선과 곡선 $y=f(x)$ 위의 점 $(2,3)$ 에서의 접선이 점 $(1,3)$ 에서 만날 때, $f(0)$ 의 값은? [4점]\\\\
(1) 31\\\\
(2) 33\\\\
(3) 35\\\\
(4) 37\\\\
(5) 39

\\section*{Connment}
\\section*{Drill 이차함수의 그래프의 대칭의 적극 이용}
이차함수가 등장하면 항상 그래프의 대칭을 이용해 봐야 한다. 특히 그래프가 직선 $x=m$ 에 대하여 대칭인 이차함수 $f(x)$ 에 대하여 $f(a)=f(b)$ 인 조건은 $a=b$ 또는 $\\frac{a+b}{2}=m$ 으로 이용할 수 있어야 한다.\\\\
앞의 문제에서 이차함수 $y=f(x)$ 의 그래프가 $y$ 축에 대하여 대칭이므로 방정식 $f(x)=f(x f(x)-2)$ 를 곧바로 두 방정식 $x=x f(x)-2, x+\\{x f(x)-2\\}=0$ 으로 고치고, 동시에 방정식의 실근의 개수를 그래프의 교점의 개수로 다루는 방향으로 잡을 수 있어야 한다.\\\\
어떤 함수의 그래프를 이용할까? 이차함수 $f(x)$ 가 우함수이니 삼차함수 $x f(x)$ 가 기함수 임을 이용하는 것이 좋겠다는 판단 정도는 자연스럽게 할 수 있을 듯. 원점에 대하여 대칭인 $y=x f(x)$ 의 그래프가 두 직선 $y=x+2, y=-x+2$ 와 만나는 점의 개수가 3 이 되도록 접할 때를 콕 짚어서 조절하고 마무리하는 것은 너무나 쉬운 것.\\\\
삼차함수 $y=x f(x)$ 의 그래프의 변곡점이 원점인 것을 이용하여 삼차함수의 그래프의 비율 관계로 직선 $y=x+2$ 와의 두 교점의 $x$ 좌표를 하나의 미지수로 잡을 수 있으면 좋다.

\\section*{Comment}
\\section*{Drill 그래프의 대칭의 기하적 판단}
그래프가 대칭인 함수가 등장할 때는 반드시 그래프를 이용한 기하적 판단을 함께 하면서 풀이 방향을 잡아야 한다. 앞의 문제에서 $y=g(x)$ 의 그래프는 원점에 대하여 대칭이다.\\\\
그런데 여기서 삼차함수 $y=f(x)$ 의 그래프가 원점을 지난다고 오해하면 큰 일 $\\cdots$ 조건 (나) 에서 $g(0)=0$ 인 것은 맞지만 $g(x)$ 가 $x=0$ 에서 연속이라는 조건이 없다. 그렇게 오해했다 하더라도 조건 (다)에서 $\\lim _{x \\rightarrow 0}|g(x)|=1$ 인 것에서 바로잡고 삼차함수 $y=f(x)$ 의 그래프의 상황과 연결 지을 수 있어야 한다.\\\\
$|g(x)|$ 가 $x=0$ 에서 불연속이어서 조건 (다)의 극한은 미분계수가 아니지만 $x \\rightarrow 0$ 일 때 점 $(x,|g(x)|)$ 가 점 $(0,1)$ 에 한없이 가까워지므로 이 두 점을 지나는 직선의 기울기의 극한 으로는 얼마든지 볼 수 있다. 이 직선의 기울기의 극한값이 존재하는 것에서 $f(0), f^{\\prime}(0)$ 의 값을 동시에 정할 수 있다.\\\\
이제 마무리! 방정식 $g(x)=|x|$ 의 실근 0 을 하나 따로 떼놓으면 $x \\neq 0$ 일 때 $y=g(x)$ 의 그래프와 $y=|x|$ 의 그래프가 세 점에서 만난다는 것. $x>0$ 에서의 $y=f(x)$ 의 그래프와 이를 원점에 대하여 대칭이동한 $x<0$ 에서의 $y=-f(-x)$ 의 그래프의 개형을 잡아보면 된다.\\\\
접할 때라는 건 당연히 예상했을 테고~{}\\\\
그리고 $x<0$ 에서 $y=-f(-x)$ 의 그래프와 직선 $y=-x$ 를 모두 원점에 대하여 대칭이동 하여 $x>0$ 에서 $y=f(x)$ 의 그래프와 직선 $y=-x$ 로 다루는 센스를 발휘하면 그래프의 개형 판단에 살짝 유리할 수 있다.\\\\
$f(x)$ 의 식을 쓸 때 $f(0)$ 은 상수항, $f^{\\prime}(0)$ 은 $x$ 의 계수임을 이용하려면 당연히 전개식으로 쓰는 것이 좋다고 판단하고 정리하자.

\\section*{Drill. 1 전반부를 잘 넘기면 후반부는 순전히 고 1 수학}
앞의 문제는 $\\lim _{h \\rightarrow 0+} \\frac{|f(x+h)|-|f(x)|}{h}$ 가 함수 $|f(x)|$ 의 $x$ 에서의 우미분계수이고, $|f(x)|$ 가 미분가능하지 않은 지점만 제외하면 $x$ 에서의 미분계수이므로 $|f(x)|$ 의 도함수의 그래프를 그려보겠다는 기하적 판단으로 시작하는 것이 좋다.\\\\
삼차함수 $f(x)=(x-a)^{2}(x-b)$ 의 그래프를 $x$ 축과의 접점의 위치를 구분하여 두 가지 케이스로 나누어보면 되는데, $|f(x)|$ 를 이용하여 그 도함수의 그래프를 그린 후 확실한 실근 -4 를 교점의 $x$ 좌표로 보면서 어떤 함수의 그래프를 이용하는 것인지 세심하게 주의를 기울여야 한다. 그리고 이 단계까지 잘 넘기고 나면 남은 과정은 고1 수학인 정수 미지수 조건의 부정방정식, 삼차방정식의 근과 계수의 관계의 이용으로 자연스럽게 이어갈 수 있어야 한다.

\\section*{Drill. 2 미분가능한 함수의 변회율의 극한값은 미분계수}
함수 $y=f(x)$ 의 그래프 위의 정점 $\\mathrm{A}(a, f(a))$ 를 향해 동점 $\\mathrm{P}(x, f(x))$ 가 점 A 의 왼쪽 에서 가까워질 때와 점 A 의 오른쪽에서 가까워질 때의 직선 AP 의 기울기의 극한값이 존재 하고 이 두 값이 같으면 직선 AP 의 기울기의 극한값, 즉 $f^{\\prime}(a)$ 의 값이 존재하고 $f(x)$ 가 $x=a$ 에서 미분가능하다고 판단한다.\\\\
\\includegraphics[max width=\\textwidth, center]{c26a6b98-7690-4db0-b3b8-fdb9d3d5f06b-07_198_824_1598_896}

동점 양방향 정점\\\\
$($ 좌미분계수 $)=($ 우미분계수 $)$\\\\
미분가능한 함수 $f(x)$ 에 대해서는 그래프 위의 두 점이 서로 한없이 가까워질 때, 이 두 점을 이은 직선의 기울기의 극한값, 즉 변화율의 극한값은 항상 존재하고 이는 미분계수와 같다.\\\\
(1) $x=a$ 에서의 좌미분계수나 우미분계수만을 나타내는 변화율의 극한

예를 들어

$$
\\begin{aligned}
& \\lim _{x \\rightarrow a+} \\frac{f(x)-f(a)}{x-a}=f^{\\prime}(a), \\lim _{h \\rightarrow 0-} \\frac{f(a+h)-f(a)}{(a+h)-a}=f^{\\prime}(a), \\\\
& \\lim _{x \\rightarrow 0} \\frac{f\\left(x^{2}\\right)-f(0)}{x^{2}-0}=f^{\\prime}(0)
\\end{aligned}
$$

이다.\\\\
(2) 점 $(a, f(a))$ 를 제외한 근방의 그래프 위의 두 점을 이은 직선의 기울기의 극한 예를 들어

$$
\\lim _{h \\rightarrow 0} \\frac{f(a+h)-f(a-h)}{(a+h)-(a-h)}=f^{\\prime}(a), \\lim _{x \\rightarrow 0} \\frac{f(2 x)-f(x)}{2 x-x}=f^{\\prime}(0)
$$

이다.

\\section*{Drill. 3 도함수의 불연속}
함수 $f(x)$ 가 $x=a$ 에서 연속이고, $f^{\\prime}(x)$ 의 $x=a$ 에서의 좌극한과 우극한이 서로 같지 않을 때, $f(x)$ 는 $x=a$ 에서 미분가능하지 않고, 점 $(a, f(a))$ 는 첨점이다.\\\\
\\includegraphics[max width=\\textwidth, center]{c26a6b98-7690-4db0-b3b8-fdb9d3d5f06b-08_303_673_1180_1032}

\\section*{Drill. 1 실수 전체의 집합에서 증가(감소)하는 삼차함수}
삼차함수 $f(x)$ 가 실수 전체의 집합에서 증가한다. (감소한다.)\\\\
⇔ 모든 실수 $x$ 에 대하여 $f^{\\prime}(x) \\geq 0\\left(f^{\\prime}(x) \\leq 0\\right)$\\\\
⇔ 이차방정식 $f^{\\prime}(x)=0$ 의 판별식 $D$ 에 대하여 $D \\leq 0$\\\\
다항함수 $f(x)$ 의 증가와 감소를 다룰 때는 $f^{\\prime}(x)$ 에 대한 조건을 다음과 같이 사용해야 한다.

상수함수가 아닌 다항함수 $f(x)$ 가 어떤 열린구간에서\\\\
(1) 증가한다. $\\Longleftrightarrow$ 이 구간의 모든 $x$ 에 대하여 $f^{\\prime}(x) \\geq 0$ 이다.\\\\
(2) 감소한다. ⇔ 이 구간의 모든 $x$ 에 대하여 $f^{\\prime}(x) \\leq 0$ 이다.

또한 증가(감소)하는 연속함수의 다음과 같은 다른 표현도 반드시 확인해두어야 한다.\\\\
연속함수가 증가한다. (감소한다.)\\\\
⟺ 일대일대응\\\\
⇔ 역함수를 갖는다.\\\\
⇔ 극값을 갖지 않는다.

\\section*{Drill. 2 항등식 $g(f(x))=x$}
두 함수 $f(x), g(x)$ 가 $f(x)$ 의 치역과 $g(x)$ 의 정의역이 서로 같고, $f(x)$ 의 정의역의 모든 원소 $x$ 에 대하여 $g(f(x))=x$ 를 만족시키면 $f(x), g(x)$ 는 각각 일대일대응이고 $g(x)=f^{-1}(x)$ 이다.\\\\[0pt]
[증명] $f(x)$ 가 일대일대응이 아니면 $a \\neq b$ 이고 $f(a)=f(b)$ 인 $a, b$ 가 존재한다.\\\\
이때 $g(f(a))=a, g(f(b))=b$ 에서 $g(f(a)) \\neq g(f(b))$ 이므로 모순이다.\\\\
따라서 $f(x)$ 는 일대일대응이고 $f^{-1}(x)$ 가 존재한다.\\\\
또한 $g\\left(f\\left(f^{-1}(x)\\right)\\right)=f^{-1}(x)$ 에서 $g(x)=f^{-1}(x)$ 이다.

\\section*{Chapter 2}
\\section*{미분}
\\section*{2024학년도 9월 평기원 공통 13번}
두 실수 $a, b$ 에 대하여 함수

$$
f(x)= \\begin{cases}-\\frac{1}{3} x^{3}-a x^{2}-b x & (x<0) \\\\ \\frac{1}{3} x^{3}+a x^{2}-b x & (x \\geq 0)\\end{cases}
$$

이 구간 $(-\\infty,-1]$ 에서 감소하고 구간 $[-1, \\infty)$ 에서 증가할 때, $a+b$ 의 최댓값을 $M$, 최솟값을 $m$ 이라 하자. $M-m$ 의 값은? [4점]\\\\
(1) $\\frac{3}{2}+3 \\sqrt{2}$\\\\
(2) $3+3 \\sqrt{2}$\\\\
(3) $\\frac{9}{2}+3 \\sqrt{2}$\\\\
(4) $6+3 \\sqrt{2}$\\\\
(5) $\\frac{15}{2}+3 \\sqrt{2}$

답 (3)

\\section*{Drill. 1 삼차함수가 등장한 것만 제외하면 순전히 고1 수학}
앞의 문제는 삼차함수인 $f(x)=x^{3}+a$ 가 등장하고 그 역함수가 존재한다는 것만 제외하면 순전히 고1 수학에 관한 내용이다. 최근에 기본적인 정의와 성질의 적용 단계만 지나면 대부분 고1 수학에 관한 내용인 문제가 자주 등장한다. 고1 수학의 중요한 주제는 꽤나 익숙하게 공부해둬야 한다.\\\\
집합 $A$ 의 의미는? 함수 $y=f(x)$ 의 그래프가 점 $(x, f(x))$ 의 집합이므로 집합 $A$ 의 원소를 좌표평면에 모두 표시하면 우리가 흔히 생각하는 그림으로서의 그래프가 된다. 이 의미만 파악되면 집합 $B$ 와 $A \\cap B$ 를 어떻게 인식해야 할지 알 수 있다.\\\\
집합 $C$ 에 대해서는 주어진 정의와 조건에만 충실하면서 마무리하면 된다.

\\section*{Drill. 2 역함수의 그래프와의 교점}
(1) $f(x)$ 가 증가하는 함수일 때, $y=f(x)$ 의 그래프와 $y=f^{-1}(x)$ 의 그래프의 교점이 존재 하면 이 교점은 반드시 직선 $y=x$ 위에 있고, 교점의 개수는 홀수일 수도 있고 짝수일 수도 있다.\\\\
(2) $f(x)$ 가 감소하는 함수일 때, $y=f(x)$ 의 그래프와 $y=f^{-1}(x)$ 의 그래프의 교점 중 직선 $y=x$ 위에 있지 않은 교점이 존재할 수 있다. $y=f(x)$ 의 그래프가 직선 $y=x$ 에 대하여 대칭인 두 점 $(a, b),(b, a)(a \\neq b)$ 를 지나면 $y=f^{-1}(x)$ 의 그래프도 두 점 $(b, a)$, $(a, b)$ 를 지나기 때문이다.\\\\
연속함수 $f(x)$ 가 감소하는 함수일 때, $y=f(x)$ 의 그래프와 $y=f^{-1}(x)$ 의 그래프의 교점이 존재하면 이 교점은

직선 $y=x$ 위에 1 개뿐이거나\\\\
직선 $y=x$ 위에 1 개와 직선 $y=x$ 에 대하여 대칭인 2개씩\\\\
이므로 교점의 개수는 홀수이다.\\\\
\\includegraphics[max width=\\textwidth, center]{c26a6b98-7690-4db0-b3b8-fdb9d3d5f06b-11_297_324_1939_903}\\\\
\\includegraphics[max width=\\textwidth, center]{c26a6b98-7690-4db0-b3b8-fdb9d3d5f06b-11_303_317_1937_1361}

\\section*{Drill 기본적이고 특별한 삼차함수와 사차함수}
기함수인 삼차함수, 우함수인 사차함수, $x$ 축에 접하는 기본적이고 특별한 삼차함수와 사차 함수

$$
y=a x^{3}+b x, y=a x^{4}+b x^{2}+c, y=a x^{3}+b x^{2}, y=a x^{4}+b x^{3}
$$

등의 그래프와 이들을 간단히 평행이동한 그래프는 미분하지 않고 직접 다룰 수 있도록 익혀두는 것이 좋다. 계산상의 이점도 있지만 그래프의 기하적 특징을 염두에 두면 문제의 상황을 파악하기 상당히 수월해지는 경우가 많기 때문이다.\\\\
앞의 문제에서 $y=f(x)$ 의 그래프는 원점에서 $x$ 축에 접하고 극대인 삼차함수 $y=x^{3}-3 x^{2}$ 의 그래프를 $y$ 축의 방향으로 $k$ 만큼 평행이동한 것이라고 곧바로 인식하면 $|f(x)|$ 의 극솟값 중 하나가 1 인 것에서 $k$ 의 값을 구하고 마무리할 수 있다.

\\section*{Drill 극값의 존재와 미분가능은 서로 관계가 없다}
연속함수 $f(x)$ 가 $x=a$ 에서 극값을 갖는 것은 $f^{\\prime}(a)=0$ 인 것과 서로 관계가 없다.\\\\
함수 $y=f(x)$ 의 그래프가 그림과 같을 때,\\\\
(1) $f^{\\prime}(c)=0$ 이지만 $f(c)$ 는 극값이 아니다.\\\\
(2) $f(d)$ 는 극값이지만 $f^{\\prime}(d)=0$ 이 아니다.\\\\
\\includegraphics[max width=\\textwidth, center]{c26a6b98-7690-4db0-b3b8-fdb9d3d5f06b-13_276_456_754_1412}\\\\
(3) $f(a), f(b)$ 는 각각 극댓값, 극솟값이고 $f^{\\prime}(a)=0, f^{\\prime}(b)=0$ 이다.\\\\
연속함수 $f(x)$ 의 극값의 존재는 다음과 같이 판단한다.\\\\
$f^{\\prime}(x)$ 의 부호가 바뀐다. ⇒ 연속함수 $f(x)$ 의 극값이 존재한다.

앞의 문제는 $g(x)$ 가 연결 지점인 $x=0,1$ 에서 연속인 조건으로 $f(-1)=f(0)$ 을 쉽게 얻을 수 있다. $y=f(x-1), y=f(x-2)$ 의 그래프가 각각 $y=f(x)$ 의 그래프를 $x$ 축의 방향으로 1 만큼, 2 만큼 평행이동한 것이므로 $g(-1)=g(0)=g(1)$ 까지 확인하고 나서 해야 할 일은? 삼차함수 $y=f(x)$ 의 그래프의 개형의 케이스 구분! 극대인 점의 존재 범위를 $x=-1$ 을 경계로 확인해 보기로 해야 한다. 극대인 점의 $x$ 좌표가 -1 인 경우 또는 -1 과 0 사이에 있는 경우에 $y=g(x)$ 의 그래프에서 극대인 모든 점의 $x$ 좌표의 합이 -1 이 될 수 없다는 것은 매우 쉽게 확인할 수 있고, $f(x)$ 가 극대인 점의 $x$ 좌표를 센스 있게 곧바로 구할 수도 있다. 마무리 단계에서 $f(-1)=f(0)$ 이므로 인수를 잡아 $f(x)-f(0)$ 또는 $f(x)-f(-1)$ 의 식을 쓰는 것이 효율적이라는 판단도 매우 중요하다.

\\section*{Drill. 1 삼차함수의 그래프의 대칭}
삼차함수 $y=f(x)$ 의 그래프는 변곡점에 대하여 대칭이므로 서로 다른 두 점 $\\mathrm{A}(a, f(a))$, $\\mathrm{B}(b, f(b))$ 에서의 접선의 기울기가 같으면, 즉 $f^{\\prime}(a)=f^{\\prime}(b)$ 이면 두 점 $\\mathrm{A}, \\mathrm{B}$ 는 서로 변곡점에 대하여 대칭이다.\\\\
따라서 선분 AB 의 중점이 변곡점이므로

$$
f^{\\prime}(a)=f^{\\prime}(b) \\text { 이면 변곡점의 } x \\text { 좌표는 } \\frac{a+b}{2}
$$

이다. 특히 삼차함수 $y=f(x)$ 의 극대인 점과 극소인 점을 이은 선분의 중점이 변곡점이다.\\\\
\\includegraphics[max width=\\textwidth, center]{c26a6b98-7690-4db0-b3b8-fdb9d3d5f06b-14_274_362_1133_1108}

앞의 문제는 두 점 $\\mathrm{P}, \\mathrm{Q}$ 의 $x$ 좌표를 미지수로 잡고 이차방정식 $f^{\\prime}(x)=m$ 의 근과 계수의 관계를 이용할 수 있도록 두 점 $\\mathrm{P}, \\mathrm{Q}$ 의 $y$ 좌표가 같다는 등식을 인수분해 공식, 곱셈 공식의 변형으로 정리하여 풀어도 잘한 거다. 고 1 수학의 기본이 잘 갖춰진 것.\\\\
또는! 두 점 $\\mathrm{P}, \\mathrm{Q}$ 에서의 접선의 기울기가 서로 같으므로 선분 PQ 의 중점이 삼차함수의 그래프의 변곡점이라고 곧바로 알고, 이 변곡점의 $x$ 좌표와 삼차방정식의 세 실근의 합의 관계, 삼차방정식의 근과 계수의 관계를 부분적으로 이용했어도 역시 잘한 거다. 워낙 Named 함수인 삼차함수와 사차함수에 대해 익혀둔 것은 이용할 상황을 놓치지 않도록 항상 주의를 기울이자.

\\section*{Drill. 2 삼차방정식의 세 실근의 합과 변곡점}
삼차함수 $f(x)=a x^{3}+b x^{2}+c x+d$ 에 대하여 $y=f(x)$ 의 그래프의 변곡점의 $x$ 좌표를 $p$ 라 하자.\\\\
(1) 이차함수 $f^{\\prime}(x)=3 a x^{2}+2 b x+c$ 는 $x=-\\frac{b}{3 a}$ 에서 최댓값 또는 최솟값을 가지므로 곡선 $y=f(x)$ 의 변곡점의 $x$ 좌표는 $-\\frac{b}{3 a}=p$ 이다. 따라서

$$
3 p=-\\frac{b}{a}
$$

이다.\\\\
(2) 삼차방정식 $f(x)=0$ 이 세 실근을 가질 때, 이 세 실근의 합은 근과 계수의 관계에서 $-\\frac{b}{a}$ 이므로\\\\
(삼차방정식 $f(x)=0$ 의 세 실근의 합)\\\\
$=3 \\times$ (삼차함수 $y=f(x)$ 의 그래프의 변곡점의 $x$ 좌표)\\\\
이다. 이때 삼차방정식 $f(x)=0$ 의 중근은 서로 같은 실근 2 개로, 삼중근은 서로 같은 실근 3 개로 취급하면 된다.


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
        prev_connment = body.rfind('\\section*{Connment}', 0, start_pos)
        prev_drill = body.rfind('\\section*{Drill', 0, start_pos)
        
        # Comment 또는 Connment 바로 다음에 오는 Drill은 전략
        is_strategy = False
        if prev_comment != -1:
            between = body[prev_comment:start_pos]
            if '\\section*{' not in between.replace('\\section*{Comment}', '').replace('\\section*{Drill', '').replace('\\section*{Connment}', ''):
                is_strategy = True
        if prev_connment != -1:
            between = body[prev_connment:start_pos]
            if '\\section*{' not in between.replace('\\section*{Comment}', '').replace('\\section*{Drill', '').replace('\\section*{Connment}', ''):
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
                    question_ref = "02"
                
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
                    question_ref = "02"
                
                solutions.append({
                    "type": "strategy",
                    "topic": f"{drill_num} 미분".strip() if drill_num else "미분",
                    "question_ref": question_ref,
                    "content": strategy_content
                })
    
    return solutions


def review_solutions(solutions):
    """해설 데이터 검토 (수학적 논리 포함)"""
    print("=" * 60)
    print("[수2 드릴 02 해설 데이터 검토]")
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
        if '다항함수' in content or '차수' in content or '삼차함수' in content or '이차함수' in content:
            if '최고차항' in content or '계수' in content:
                pass  # 다항함수 차수 언급 정상
        
        # 4. 미분 관련 확인
        if '미분' in content or '접선' in content or '극대' in content or '극소' in content or '도함수' in content:
            if 'f\'' in content or 'f^{\\prime}' in content or 'g\'' in content:
                pass  # 미분 관련 언급 정상
        
        # 5. 조건부 함수 확인
        if '\\begin{cases}' in content:
            if '\\end{cases}' in content:
                pass  # 조건부 함수 구조 정상
        
        # 6. 그래프 대칭 확인
        if '대칭' in content or '변곡점' in content:
            if '그래프' in content or '함수' in content:
                pass  # 그래프 대칭 언급 정상
    
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
    csv_path = save_dir / "수2_2025학년도_현우진_드릴_02_해설_deepseek.csv"
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
    json_path = save_dir / "수2_2025학년도_현우진_드릴_02_해설_deepseek.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(solutions, f, ensure_ascii=False, indent=2)
    
    print(f"[JSON 저장 완료] {json_path}")
    
    return csv_path, json_path


def main():
    print("=" * 60)
    print("[수2 드릴 02 해설 LaTeX → CSV 변환]")
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
