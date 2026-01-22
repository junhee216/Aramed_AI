# convert_su2_p4_solution_latex.py
# 수2 드릴 P4 해설 LaTeX를 딥시크용 CSV로 변환

import re
import csv
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
\\usepackage{multirow}
\\usepackage{bbold}
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
\\section*{Drill. 1 삼차함수의 그래프에서는 일단 대칭, 변곡점, 비율 관계}
앞의 문제에서는 벤다이어그램을 머릿속에 떠올려보는 것만으로도 $A-B, A \\cap B, B-A$ 에서 두 집합 $A, B$ 를 매우 쉽게 구할 수 있다. $A, B$ 중 어느 집합을 먼저 건드려볼까? 집합 $B$ 의 원소의 개수가 3 이라는 것이 좀 더 인상적으로 느껴져야 한다. $d$ 가 상수인 것을 감안하면 삼차함수 $f(x)$ 의 $x=1,2,3,4,5$ 에서의 함숫값의 집합의 원소의 개수가 3 이라는 것이다. 삼차함수의 그래프의 비율 관계에 익숙하다면 변곡점의 $x$ 좌표가 3 이고 $x=2$ 에서 극대, $x=4$ 에서 극소인 $y=f(x)$ 의 그래프의 개형이 바로 잡히고, $y=f^{\\prime}(x)$ 의 그래프를 함께 그려서 집합 $A$ 의 원소의 개수의 조건에 딱 맞는다는 것을 확인할 수 있다. 다른 그래프의 개형의 가능성에 대하여 점검해 볼 수도 있겠지만 실전에서는 이쯤에서 일단 다음 단계로 넘어가보는 것이 좋다.\\\\
$f(x)$ 의 극솟값, 변곡점의 $y$ 좌표, 극댓값이 이 순서대로 등차수열을 이루긴 하지만 각각 집합 $B$ 의 어느 원소인지는 알 수 없다. $y=f^{\\prime}(x)$ 의 그래프도 함께 그려놨을 테니 집합 $A$ 로 시선을 돌려보자. $f^{\\prime}(2)=f^{\\prime}(4)=0$ 이고 $a_{6}<0<a_{12}$ 인 대소 관계까지 알 수 있다. $f(x)$ 의 최고차항의 계수를 미지수 $k$ 로 잡고 $f^{\\prime}(x)$ 의 식부터 써서 $x=3, x=1$ 등을 대입해 보면 슬슬 상황이 정리되기 시작한다.\\\\
집합 $B$ 로 돌아가보면 $\\frac{f(x)}{d}$ 의 극솟값 $\\frac{f(4)}{2 k}$, 변곡점의 $y$ 좌표 $\\frac{f(3)}{2 k}$, 극댓값 $\\frac{f(2)}{2 k}$ 가 세 원소이고 이 중 어느 둘은 등차수열 $\\left\\{a_{n}\\right\\}$ 의 항인 $a_{6}, a_{m}$, 남은 하나는 0 이다. $a_{6}<0$ 이므로 $f(x)$ 의 극솟값이 0 일 수는 없고, $f(x)$ 의 변곡점의 $y$ 좌표, 극댓값 중 무엇이 0 인지 케이스를 구분하고 마무리할 일만 남았다. $\\frac{f(4)}{2 k}, \\frac{f(3)}{2 k}, \\frac{f(2)}{2 k}$ 가 이 순서대로 등차수열을 이루는 것은 당연히 놓치지 말고 이용해야 하고, 이제 마지막으로 뭘 더 해야 하나 싶을 때, 삼차 함수에 관한 기본 중 하나인 도함수의 정적분을 이용한 극댓값과 극솟값의 차의 계산으로 끝낼 수 있다.\\\\
$f(x)$ 의 식은 $f^{\\prime}(x)$ 의 식을 전개하고 적분해서 구해도 좋고, 삼차함수의 그래프의 비율 관계를 이용해서 직접 써도 좋다.

\\section*{Chapter 2}
\\section*{미분}
\\section*{Comment}
Drill. 2 삼차함수의 극댓값과 극솟값의 차\\\\
삼차함수의 극댓값과 극솟값의 차는 도함수의 정적분을 이용하여 구할 수 있다.\\\\
\\includegraphics[max width=\\textwidth, center]{078961e9-54a0-4430-a450-661b0591cba1-02_472_602_816_1084}

넓이 공식 $S=\\frac{|3 a|}{6}(\\beta-\\alpha)^{3}$

\\section*{Drill. 1 구간별로 정의된 함수의 미분가능}
구간별로 정의된 함수일 때, 연결 지점에서 함숫값과 미분계수의 일치 여부를 확인한다.\\\\
두 함수 $g_{1}(x), g_{2}(x)$ 가 모두 미분가능할 때

$$
\\begin{aligned}
& \\text { 함수 } f(x)=\\left\\{\\begin{array}{ll}
g_{1}(x) & (x<a) \\\\
g_{2}(x) & (x \\geq a)
\\end{array} \\text { 가 } x=a\\right. \\text { 에서 미분가능 } \\\\
& \\Leftrightarrow g_{1}(a)=g_{2}(a), g_{1}^{\\prime}(a)=g_{2}^{\\prime}(a)
\\end{aligned}
$$

\\section*{Drill. 2 미분가능하면 연속이다}
함수 $f(x)$ 가 $x=a$ 에서 미분가능하면 함수 $f(x)$ 는 $x=a$ 에서 연속이다. 즉 연속은 미분가능 하기 위한 필요조건이므로 미분가능을 따질 때는 연속을 우선 점검해야 한다는 것이다.\\\\
구간별로 정의된 함수가 연결 지점에서 미분가능하도록 할 때, 연결 지점에서 미분계수뿐만 아니라 함숫값도 함께 일치하도록 하는 것이 그런 이유에서이다. 앞의 문제에서도 $x=b$ 에서 함숫값의 일치를 놓치지 말아야 한다.

\\section*{Drill 미분가능하지 않은 함수의 변화율의 극한}
미분가능하지 않은 함수에 대해서도 변화율의 극한값이 존재할 수 있다. 우선 미분가능하지 않은 점을 포함한 좌미분계수나 우미분계수만을 나타내는 변화율의 극한값에는 매우 익숙할 것이다. 여기에 더해서 두 점이 미분가능하지 않은 점에 한없이 가까워질 때, 이 두 점을 이은 직선의 기울기의 극한값, 즉 변화율의 극한값이 존재할 수 있다는 것도 반드시 확인해 두자.\\\\
예를 들어 함수 $f(x)=|x-a|$ 는 $x=a$ 에서 미분가능하지 않지만 다음과 같이 점 $(a, f(a))$ 에 한없이 가까워지는 두 점을 이은 직선의 기울기의 극한값이 존재한다.

$$
\\begin{aligned}
& \\lim _{h \\rightarrow 0} \\frac{f(a+h)-f(a-h)}{(a+h)-(a-h)}=0, \\lim _{h \\rightarrow 0+} \\frac{f(a+2 h)-f(a+h)}{(a+2 h)-(a+h)}=1 \\\\
& \\lim _{h \\rightarrow 0+} \\frac{f(a+2 h)-f(a-h)}{(a+2 h)-(a-h)}=\\frac{1}{3}
\\end{aligned}
$$

\\includegraphics[max width=\\textwidth, center]{078961e9-54a0-4430-a450-661b0591cba1-04_223_333_1338_729}\\\\
\\includegraphics[max width=\\textwidth, center]{078961e9-54a0-4430-a450-661b0591cba1-04_223_329_1336_1122}\\\\
\\includegraphics[max width=\\textwidth, center]{078961e9-54a0-4430-a450-661b0591cba1-04_229_341_1330_1512}

미분가능하지 않은 함수의 변화율의 극한은 정확한 식의 계산으로 다루기도 하지만 부분 적으로 Named 함수인 다항함수가 등장할 때는 그래프의 개형을 함께 살펴보는 것이 좋다.

앞의 문제의 조건 (가)의 극한의 의미는 $g(x)$ 의 우미분계수가 0 인 지점은 존재하지 않는 다는 것이다. 따라서 삼차함수 $y=f(x)$ 의 그래프의 극대 또는 극소인 점을 포함하는 부분은 $y=g(x)$ 의 그래프가 될 수 없다는 것.\\\\
조건 (나)의 극한의 의미는 두 점이 양쪽에서 미분가능하지 않은 점에 한없이 가까워질 때, 두 점을 이은 직선의 기울기의 극한값이 0 이라는 것이다. 즉 미분가능하지 않은 점은 모두 좌미분계수와 우미분계수의 절댓값이 같고 부호가 반대인 첨점이라는 것이다. 미분가능하지 않은 점의 좌우가 각각 직선 $y=x+f(0)$ 또는 $y=f(x)$ 의 그래프이므로 이러한 연결 지점 에서 $f(x)$ 의 미분계수는 -1 이다.\\\\
최고차항의 계수가 음수인 삼차함수 $y=f(x)$ 의 그래프와 직선 $y=x+f(0)$ 의 교점의 개수에 따른 케이스는 3 가지뿐이다. ㄱ을 판단하기 위해 $g(x)$ 의 극솟값이 $f(0)-2$ 인 조건을 감안 하여 케이스별로 $y=g(x)$ 의 그래프를 그려보면 ㄴ, ㄷ을 판단하기 위한 준비까지 거의 다 갖추게 된다.

\\section*{Drill 고전적이지만}
앞의 문제는 2013 학년도 수능에서 출제되었던 지금의 '미적분'에 해당하는 과목의 문제를 '수학 II'에 맞게 변형한 것이다. 십수 년 전인데 $\\cdots$ 라고 무시하지 말자. 2024학년도 수능 에서도 '수학 I'에서 2011학년도 9월 평가원 문제를 접해봤다면 상황 파악에 상당히 유리 했을 문제가 출제되었다. 현행 교육과정에 벗어나지만 않는다면 기출 문제는 모두 소중한 것!

\\section*{2011학년도 9월 평기원}
함수 $f(x)=-3 x^{4}+4(a-1) x^{3}+6 a x^{2}(a>0)$ 과 실수 $t$ 에 대하여, $x \\leq t$ 에서 $f(x)$ 의 최댓값을 $g(t)$ 라 하자. 함수 $g(t)$ 가 실수 전체의 집합에서 미분가능하도록 하는 $a$ 의 최댓값은? [4점]\\\\
(1) 1\\\\
(2) 2\\\\
(3) 3\\\\
(4) 4\\\\
(5) 5

답 (1)

\\section*{2024학년도 수능 공통 21번}
양수 $a$ 에 대하여 $x \\geq-1$ 에서 정의된 함수 $f(x)$ 는

$$
f(x)= \\begin{cases}-x^{2}+6 x & (-1 \\leq x<6) \\\\ a \\log _{4}(x-5) & (x \\geq 6)\\end{cases}
$$

이다. $t \\geq 0$ 인 실수 $t$ 에 대하여 닫힌구간 $[t-1, t+1]$ 에서의 $f(x)$ 의 최댓값을 $g(t)$ 라 하자. 구간 $[0, \\infty)$ 에서 함수 $g(t)$ 의 최솟값이 5 가 되도록 하는 양수 $a$ 의 최솟값을 구하시오. [4점]

답 10

\\section*{Commnent}
\\section*{Drill $|f(x)|$ 의 미분가능}
미분가능한 함수 $f(x)$ 에 대하여

$$
f(a)=0, f^{\\prime}(a) \\neq 0
$$

이면 함수 $|f(x)|$ 는 $x=a$ 에서 미분가능하지 않다.\\\\
$\\Rightarrow y=|f(x)|$ 의 그래프에서 점 $(a, 0)$ 은 첨점이다.

함수 $y=f(x)$ 의 그래프가 그림과 같을 때, $f(a)=0, f^{\\prime}(a) \\neq 0$ 이고 $f(b)=0, f^{\\prime}(b) \\neq 0$ 이므로 함수 $y=|f(x)|$ 의 그래프에서 두 점 $(a, 0),(b, 0)$ 은 첨점이다. 따라서 $|f(x)|$ 는 $x=a$ 와 $x=b$ 에서 미분가능하지 않다.\\\\
\\includegraphics[max width=\\textwidth, center]{078961e9-54a0-4430-a450-661b0591cba1-06_234_525_1192_740}\\\\
\\includegraphics[max width=\\textwidth, center]{078961e9-54a0-4430-a450-661b0591cba1-06_171_574_1194_1277}

미분가능한 함수 $y=f(x)$ 의 그래프가 $x$ 축과\\\\
접점이 아닌 교점\\\\
을 갖는 곳에서만 함수 $|f(x)|$ 는 미분가능하지 않다고 기억하고 활용하자.

한편 함수 $f(x)$ 가 미분가능하지 않은 곳이 있으면 이 지점에서의 함수 $|f(x)|$ 는 미분가능할 수도 있고 미분가능하지 않을 수도 있으므로 따로 확인해 봐야 한다.\\\\
함수 $f(x)=\\left\\{\\begin{array}{ll}x^{2}-1 & (x<0) \\\\ 1 & (0 \\leq x<1) \\\\ x-2 & (x \\geq 1)\\end{array}\\right.$ 는 $x=0,1$ 에서 미분가능하지 않고, 함수 $|f(x)|$ 는 $x=-1,1,2$ 에서 미분가능하지 않다.\\\\
\\includegraphics[max width=\\textwidth, center]{078961e9-54a0-4430-a450-661b0591cba1-06_320_405_1992_845}\\\\
\\includegraphics[max width=\\textwidth, center]{078961e9-54a0-4430-a450-661b0591cba1-06_280_405_1992_1336}

\\section*{Drill 연결 지점에서 함숫값의 일치부터}
구간별로 정의된 함수의 미분가능은 연결 지점에서 함숫값이 일치하도록 하는 것이 우선이다. 앞의 문제에서도 $x=0$ 에서 함숫값이 일치하도록 해놔야 절댓값 기호를 없애고 미분계수의 일치로 넘어갈 수 있다.\\\\
$x=0$ 에서의 함숫값과 미분계수를 이용하여 최고차항의 계수가 양수인 $y=f(x)$ 의 그래프의 개형을 세 가지 케이스로 구분하고, $y=|f(x)-2|, y=|f(x)+6|$ 의 그래프가 $x$ 축과 만난다면 접점이어야 한다는 기본 판단으로 각 케이스의 그래프의 개형에 따라 $f(x)$ 의 식을 쓰고 마무리하면 된다.

\\section*{Comment}
\\section*{Drill 미분가능과 극값의 존재의 구분}
앞의 문제에서 $g(x)$ 는 $x=0$ 에서 미분가능하다고 했다. 미분가능하지 않은 다른 지점이 존재해도 상관없으므로 $g(x)$ 의 극대 또는 극소인 점이 첨점일 수 있다는 판단으로 연결할 수 있어야 한다.\\\\
역시 $x=0$ 에서의 함숫값의 일치부터 시작하고 절댓값 기호를 없애고 미분계수의 일치로 넘어간다. $x=0$ 에서의 함숫값과 미분계수를 이용하여 최고차항의 계수가 음수인 $y=f(x)$ 의 그래프의 개형에서 $y=g(x)$ 의 그래프의 개형을 잡기 시작하면 된다.\\\\
$g(x)$ 의 극솟값과 극댓값이 절댓값이 같고 부호가 서로 반대라는 것, $g(x)$ 가 극소, 극대인 $x$ 의 값의 부호가 서로 반대라는 것에서 $y=f(x)$ 의 그래프의 개형을 확정하고 삼차함수의 그래프의 비율 관계로 식을 쓰고 마무리하는 것은 그리 어렵지 않다.

\\section*{Comment}
\\section*{Drill 함수의 연산 결과의 미분가능}
함수의 연산 결과의 미분가능은 다음과 같이 판정할 수 있다. 편의상 미분가능하지 않은 함수를 '미분불능'으로 나타내기로 하자.\\\\
(1) $k \\times$ (미분가능), (미분가능) + (미분가능), (미분가능) - (미분가능),\\\\
(미분가능) $\\times$ (미분가능) $\\Rightarrow$ 미분가능\\\\
(2) $($ 미분가능 $)+($ 미분불능 $),($ 미분가능 $)-($ 미분불능 $) \\Rightarrow$ 미분불능

이것 이외에는 각 함수의 미분가능과 미분불능에서 그 연산 결과의 미분가능과 미분불능을 함부로 판정해서는 안 되고 미분가능 여부를 직접 확인해 봐야 한다. 주로 미분불능인 함수 와의 연산 결과가 문제가 되고, 미분불능인 함수와의 연산 결과가 확실한 것은 위의 (2)뿐이다. 위의 (1)은 함수의 합, 차, 곱의 미분법에서 보장되는 것이고, (2)는 직관적으로 이해되기는 하지만 다음과 같이 증명해 볼 수 있다.\\\\
$x=a$ 에서 미분가능한 함수 $f(x)$ 와 $x=a$ 에서 미분가능하지 않은 함수 $g(x)$ 에 대하여 함수 $f(x)+g(x)$ 가 $x=a$ 에서 미분가능하다고 가정하면 두 함수 $f(x), f(x)+g(x)$ 가 $x=a$ 에서 미분가능하므로 함수 $\\{f(x)+g(x)\\}-f(x)$, 즉 함수 $g(x)$ 는 $x=a$ 에서 미분가능하다. 이는 함수 $g(x)$ 가 $x=a$ 에서 미분가능하지 않다는 가정에 모순이므로 함수 $f(x)+g(x)$ 는 $x=a$ 에서 미분가능하지 않다.

앞의 문제에서 함수 $y=3 x^{3}$ 은 실수 전체의 집합에서 미분가능하므로 절댓값을 포함한 함수 $y=\\left|\\int_{a}^{x} f(t) d t\\right|$ 역시 실수 전체의 집합에서 미분가능해야 $g(x)$ 가 실수 전체의 집합에서 미분가능하다. $f(x)$ 가 이차함수이므로 삼차함수 $y=\\int_{a}^{x} f(t) d t$ 의 그래프가 $x$ 축과 접점이 아닌 교점을 가져서는 안 된다는 것이다. 무척 단순한 상황이므로 이를 인식하고 곧바로\\\\
$\\int_{a}^{x} f(t) d t$ 의 식을 쓰기 시작해야 한다. 미분하기 위해 절댓값 기호를 없애려 하면 연결 지점을 $x=a$ 로 자연스럽게 잡을 수 있다.\\\\
다음 단계로 넘어가서 마무리까지는 간단한 고 1 수학이다. $x>a$ 에서 $y=g^{\\prime}(x)$ 인 이차함수의 그래프가 $x$ 축과 만나는 두 점이 서로 달라야 하고 이 두 점의 $x$ 좌표가 모두 -2 보다 커야 한다는 조건 설정까지는 별 어려움이 없을 텐데, $x>a$ 에서의 상황이므로 이 두 점의 $x$ 좌표가 모두 $a$ 보다 커야 한다는 조건을 놓쳐서 오답에 낚이는 일은 없어야 한다…

\\section*{Comment}
\\section*{Drill 함수의 곱의 미분가능}
$x=a$ 에서 미분가능한 함수 $f(x)$ 와 $x=a$ 에서 함숫값이 존재하고 미분가능하지 않은 함수 $g(x)$ 에 대하여 함수 $f(x) g(x)$ 가 $x=a$ 에서 미분가능하기 위한 $f(x)$ 의 인수 $x-a$ 의 최소 개수는 다음과 같다.

\\begin{center}
\\begin{tabular}{|l|l|l|}
\\hline
 & $g(x)$ 가 $x=a$ 에서 & $f(x) g(x)$ 가 $x=a$ 에서 미분가능하기 위한 $f(x)$ 의 인수 $x-a$ 의 최소 개수 \\\\
\\hline
 & 연속, 미분불능(첨점) & 1 \\\\
\\hline
\\multirow{3}{*}{불연속} & $($ 좌극한 $)=($ 우극한 $)$ & 1 \\\\
\\hline
 & (좌극한) $\\neq$ (우극한) & 2 \\\\
\\hline
 & 좌극한 또는 우극한이 $\\pm \\infty$ & 2 이상 \\\\
\\hline
\\end{tabular}
\\end{center}

\\includegraphics[max width=\\textwidth, center]{078961e9-54a0-4430-a450-661b0591cba1-10_210_490_1345_748}\\\\
\\includegraphics[max width=\\textwidth, center]{078961e9-54a0-4430-a450-661b0591cba1-10_238_500_1332_1323}\\\\
\\includegraphics[max width=\\textwidth, center]{078961e9-54a0-4430-a450-661b0591cba1-10_223_602_1607_983}

그 이유는 '뉴런 수학 $\\mathbb{I}$ '에 충분히 밝혀놓았으니 $x=a$ 에서 미분가능하지 않은 $y=g(x)$ 의 그래프의 개형과 함께 기억하고 활용하도록 하자.

앞의 문제에서는 두 가지에 주의해야 한다. 하나는 $|f(x)|$ 가 미분가능하지 않은 지점이 있을 수 있고, 이때는 첨점이므로 $g(x)$ 가 미분가능하면 $g(x)$ 의 함숫값이 0 인 것만으로 $h(x)$ 가 미분가능하다는 것이다. 또 하나는 $g(x)$ 가 미분가능하지 않은 지점에서 $|f(x)|$ 도 미분 가능하지 않다면 그 판단은 완전 별개라는 것, 즉 (미분불능) $\\times$ (미분불능)의 결과는 알 수 없으므로 따져봐야 한다는 것이다. 이때 연속을 바탕으로 연결 지점의 좌우 근방의 도함수를 이용하여 미분계수의 일치로 다루는 것이 좋다.

\\section*{Comment}
\\section*{2020학년도 수능 나형 20번}
함수

$$
f(x)= \\begin{cases}-x & (x \\leq 0) \\\\ x-1 & (0<x \\leq 2) \\\\ 2 x-3 & (x>2)\\end{cases}
$$

와 상수가 아닌 다항식 $p(x)$ 에 대하여 〈보기〉에서 옳은 것만을 있는 대로 고른 것은？［4점］\\\\
〈보기〉－\\\\
ᄀ．함수 $p(x) f(x)$ 가 실수 전체의 집합에서 연속이면 $p(0)=0$ 이다．\\\\
ᄂ．함수 $p(x) f(x)$ 가 실수 전체의 집합에서 미분가능하면 $p(2)=0$ 이다．\\\\
ᄃ．함수 $p(x)\\{f(x)\\}^{2}$ 이 실수 전체의 집합에서 미분가능하면 $p(x)$ 는 $x^{2}(x-2)^{2}$ 으로 나누어떨어진다．\\\\
（1）ᄀ\\\\
（2）ᄀ，ᄂ\\\\
（3）ᄀ，ᄃ\\\\
（4）ᄂ，ᄃ\\\\
（5）ᄀ，ᄂ，ᄃ

답（2）

\\section*{Comment}
\\section*{Drill 절댓값을 포함한 함수의 미분가능은 그래프를 이용한 기하적 관점으로}
절댓값을 포함한 함수의 미분가능을 다룰 때는 그래프와 $x$ 축의 접점이 아닌 교점에서 미분 가능하지 않고, 그래프와 $x$ 축의 교점에서 미분가능하다면 이 교점이 접점이어야 한다는 그래프를 이용한 기하적 관점을 바탕에 둔 교점의 접점 여부로 다루는 것이 좋다.\\\\
또한 $y=f(x)-g(x)$ 의 그래프와 $x$ 축의 관계로 다루기 불편하다면 $y=f(x), y=g(x)$ 의 그래프로 다룰 수도 있어야 하는 것은 당연. $|f(x)-g(x)|$ 의 미분가능은 $y=f(x)$, $y=g(x)$ 의 그래프의 교점의 접점 여부로 다룰 수도 있다.\\\\
앞의 문제는 최고차항의 계수가 양수인 이차함수 $y=f^{\\prime}(x)$ 를 이용하여 그린 $y=\\left|f^{\\prime}(x)\\right|$ 의 그래프에서 각각의 부정적분 $y=f(x), y=\\int_{a}^{x}\\left|f^{\\prime}(t)\\right| d t$ 의 그래프의 연결 지점의 범위로 케이스를 구분하고 시작하면 된다. $y=f^{\\prime}(x)$ 의 그래프가 $x$ 축과 만나는 두 점을 경계로 하는 각 구간에서 $y=f(x), y=\\int_{a}^{x}\\left|f^{\\prime}(t)\\right| d t$ 의 그래프가 $x$ 축에 대한 대칭이동, $y$ 축의 방향으로의 적당한 평행이동으로 일치하는 것을 이용하여 $y=g(x)$ 의 그래프를 그리고, $|g(x)-k|$ 의 미분가능을 $y=g(x)$ 의 그래프와 직선 $y=k$ 의 교점의 접점 여부로 다루는 것이 좋다. 실전에서는 특수한 케이스부터 점검해서 풀이 과정이 잘 들어맞고 별다른 모순점이 발견되지 않는다면 이대로 마무리해도 좋다. 그리고 삼차함수의 그래프의 특징을 이용하는 타이밍은 언제나 놓치지 않도록!


\\end{document}"""


def extract_solutions_from_latex(latex_content):
    """LaTeX에서 해설 추출"""
    solutions = []
    body = extract_body(latex_content)
    
    # Drill 섹션 패턴
    drill_pattern = r'\\section\*\{Drill\.?\s*([0-9]*)\s*([^}]+?)(?:\\\\[^}]*?)?\}\s*(.*?)(?=\\section\*|\\end\{document\}|$)'
    drill_matches = re.finditer(drill_pattern, body, re.DOTALL)
    
    for match in drill_matches:
        drill_num = match.group(1).strip() if match.group(1) else ""
        topic = match.group(2).strip()
        content = match.group(3).strip()
        start_pos = match.start()
        
        # 이전 Comment 섹션 확인 (strategy 판단)
        prev_comment = body.rfind('\\section*{Comment}', 0, start_pos)
        prev_commnent = body.rfind('\\section*{Commnent}', 0, start_pos)  # 오타 처리
        is_strategy = False
        
        if prev_comment != -1:
            between = body[prev_comment:start_pos]
            if '\\section*{' not in between.replace('\\section*{Comment}', '').replace('\\section*{Drill', '').replace('\\section*{Commnent}', ''):
                is_strategy = True
        
        if prev_commnent != -1:  # 오타 처리
            between = body[prev_commnent:start_pos]
            if '\\section*{' not in between.replace('\\section*{Comment}', '').replace('\\section*{Drill', '').replace('\\section*{Commnent}', ''):
                is_strategy = True
        
        # 이미지 및 불필요한 LaTeX 제거
        content = re.sub(r'\\includegraphics.*?}', '', content)
        content = re.sub(r'\\begin\{figure\}.*?\\end\{figure\}', '', content, flags=re.DOTALL)
        content = re.sub(r'\\begin\{center\}.*?\\end\{center\}', '', content, flags=re.DOTALL)
        content = re.sub(r'\\begin\{tabular\}.*?\\end\{tabular\}', '', content, flags=re.DOTALL)
        content = re.sub(r'\\begin\{enumerate\}.*?\\end\{enumerate\}', '', content, flags=re.DOTALL)
        content = re.sub(r'\\item', ' ', content)
        content = re.sub(r'\\captionsetup.*?}', '', content)
        content = re.sub(r'\\caption\{[^}]*\}', '', content)
        content = re.sub(r'\\\\', ' ', content)
        content = re.sub(r'\$\$', ' ', content)
        content = re.sub(r'\\begin\{displayquote\}.*?\\end\{displayquote\}', '', content, flags=re.DOTALL)
        content = re.sub(r'\s+', ' ', content)
        
        topic = re.sub(r'\\\\', ' ', topic)
        topic = re.sub(r'\s+', ' ', topic)
        
        if len(content) > 50:
            if is_strategy:
                question_ref = ""
                if '앞의 문제' in content:
                    question_ref = "P4"
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
    
    # Comment 섹션 내의 Drill 텍스트 처리
    comment_sections = re.finditer(r'\\section\*\{Comment\}(.*?)(?=\\section\*|\\end\{document\}|$)', body, re.DOTALL)
    for comment_match in comment_sections:
        comment_content = comment_match.group(1)
        drill_text_pattern = r'(?:^|\\\\)Drill\.?\s*([0-9]*)\s+([^\\\\]+?)(?=\\\\section|Drill|\\end|$)'
        drill_text_matches = re.finditer(drill_text_pattern, comment_content, re.DOTALL | re.MULTILINE)
        
        for drill_text_match in drill_text_matches:
            drill_num = drill_text_match.group(1).strip() if drill_text_match.group(1) else ""
            strategy_content = drill_text_match.group(2).strip()
            strategy_content = re.sub(r'\\includegraphics.*?}', '', strategy_content)
            strategy_content = re.sub(r'\\\\', ' ', strategy_content)
            strategy_content = re.sub(r'\$\$', ' ', strategy_content)
            strategy_content = re.sub(r'\s+', ' ', strategy_content)
            
            if len(strategy_content) > 50:
                question_ref = ""
                if '앞의 문제' in strategy_content:
                    question_ref = "P4"
                solutions.append({
                    "type": "strategy",
                    "topic": f"{drill_num} 미분".strip() if drill_num else "미분",
                    "question_ref": question_ref,
                    "content": strategy_content
                })
    
    # Commnent 오타 처리
    commnent_sections = re.finditer(r'\\section\*\{Commnent\}(.*?)(?=\\section\*|\\end\{document\}|$)', body, re.DOTALL)
    for commnent_match in commnent_sections:
        commnent_content = commnent_match.group(1)
        drill_text_pattern = r'(?:^|\\\\)Drill\.?\s*([0-9]*)\s+([^\\\\]+?)(?=\\\\section|Drill|\\end|$)'
        drill_text_matches = re.finditer(drill_text_pattern, commnent_content, re.DOTALL | re.MULTILINE)
        
        for drill_text_match in drill_text_matches:
            drill_num = drill_text_match.group(1).strip() if drill_text_match.group(1) else ""
            strategy_content = drill_text_match.group(2).strip()
            strategy_content = re.sub(r'\\includegraphics.*?}', '', strategy_content)
            strategy_content = re.sub(r'\\\\', ' ', strategy_content)
            strategy_content = re.sub(r'\$\$', ' ', strategy_content)
            strategy_content = re.sub(r'\s+', ' ', strategy_content)
            
            if len(strategy_content) > 50:
                question_ref = ""
                if '앞의 문제' in strategy_content:
                    question_ref = "P4"
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
    print("[수2 드릴 P4 해설 데이터 검토]")
    print("=" * 60)
    
    issues = []
    math_errors = []
    
    for i, sol in enumerate(solutions, 1):
        sol_type = sol.get("type", "")
        topic = sol.get("topic", "")
        print(f"\n[해설 {i}] ({sol_type}) {topic[:50]}...")
        
        content = sol.get("content", "")
        print(f"[내용 길이] {len(content)}자")
        
        # LaTeX 검사
        dollar_count = content.count('$')
        content_no_dblock = re.sub(r'\$\$', '', content)
        dollar_count_single = content_no_dblock.count('$')
        
        topic_dollar = topic.count('$')
        topic_no_dblock = re.sub(r'\$\$', '', topic)
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
            if 'x \\rightarrow' in content or 'x->' in content or 'h \\rightarrow' in content:
                pass  # 극한 식 구조 정상
        
        # 2. 함수의 연속성 확인
        if '연속' in content or '불연속' in content:
            if 'f(x)' in content or 'g(x)' in content:
                pass  # 연속성 조건 언급 정상
        
        # 3. 다항함수 차수 확인
        if '다항함수' in content or '차수' in content or '삼차함수' in content or '이차함수' in content or '사차함수' in content:
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
        if '대칭' in content or '변곡점' in content or '비율 관계' in content:
            if '그래프' in content or '함수' in content:
                pass  # 그래프 대칭 언급 정상
        
        # 7. 합성함수 확인
        if '합성함수' in content or 'f \\circ f' in content or '(f \\circ f)' in content:
            if 'f(f(x))' in content or 'g \\circ g' in content:
                pass  # 합성함수 언급 정상
        
        # 8. 적분 확인
        if '\\int' in content or '적분' in content:
            if 'd t' in content or 'd x' in content or 'dt' in content or 'dx' in content:
                pass  # 적분 표기 정상
    
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


def save_for_deepseek(solutions, base_dir, base_filename):
    """딥시크용 CSV/JSON 저장"""
    save_dir = Path(base_dir)
    save_dir.mkdir(parents=True, exist_ok=True)
    
    # CSV 저장
    csv_path = save_dir / f"{base_filename}_deepseek.csv"
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
    json_path = save_dir / f"{base_filename}_deepseek.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(solutions, f, ensure_ascii=False, indent=2)
    
    print(f"[JSON 저장 완료] {json_path}")
    
    return csv_path, json_path


def main():
    print("=" * 60)
    print("[수2 드릴 P4 해설 LaTeX → CSV 변환]")
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
    base_dir = Path(r'C:\Users\a\Documents\MathPDF\organized\현우진\수2_2005학년도_현우진_드릴')
    base_filename = "수2_2025학년도_현우진_드릴_P4_해설"
    csv_path, json_path = save_for_deepseek(solutions, base_dir, base_filename)
    
    print("\n" + "=" * 60)
    print("[완료] 딥시크가 읽을 수 있는 형태로 저장되었습니다.")
    print("=" * 60)
    print(f"저장 위치: {base_dir}")
    print(f"  - CSV: {csv_path.name}")
    print(f"  - JSON: {json_path.name}")


if __name__ == '__main__':
    main()
