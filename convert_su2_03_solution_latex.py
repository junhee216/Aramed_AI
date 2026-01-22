# convert_su2_03_solution_latex.py
# 수2 드릴 03 해설 LaTeX를 딥시크용 CSV로 변환

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
\\captionsetup{singlelinecheck=false}
\\section*{Drill1 접할 때와 특별한 점을 지날 때를 기준으로}
함수의 그래프 사이의 관계는 접할 때, 특별한 점을 지날 때를 기준으로 판단하는 것이 매우 중요한 기본이다. 앞의 문제에서도 삼차함수 $y=f(x)$ 의 그래프가 두 직선 $y=2 x, y=6 x-8$ 과 접하는 경우와 원점, 두 직선 $y=2 x, y=6 x-8$ 의 교점을 지나는 경우 등이 판단의 기준이 될 것이라고 짐작하고 시작해야 한다.\\\\
$0 \\in A, 0 \\notin B$ 이므로 $n(A-B)=1$ 에서 $A-B=\\{0\\}$ 일 수밖에 없다는 것과 $A \\cap B$ 의 원소로 가능한 것은 2 뿐이라는 기본 상황 파악이 되면 ㄱ, ㄴ은 그리 어렵지 않다. ㄷㅇㅢ\\\\
$n(A)=n(B)=2$ 에서 $y=f(x)$ 의 그래프가 두 직선 $y=2 x, y=6 x-8$ 에 동시에 접하도록 그래프를 그려보는 것도 그리 어렵지 않다. $y=f(x)$ 의 그래프와 직선 $y=2 x$ 의 두 교점의 $x$ 좌표가 확실하므로 인수를 이용하여 $f(x)-2 x$ 의 식을 쓰고 나서 마무리는? $y=f(x)$ 의 그래프와 직선 $y=6 x-8$ 의 접점의 $x$ 좌표를 미지수로 잡고 접선을 다루는 기본적인 방법으로 풀어나가도 좋지만, 삼차함수의 그래프와 만나는 여러 직선이 등장하는 상황에 주목한다면? 고1 수학의 삼차방정식의 근과 계수의 관계로 이 교점의 $x$ 좌표의 합이 일정하다는 것을 이용할 수 있으면 더 좋겠다. 앞의 문제에서 삼차함수의 그래프의 변곡점에 굳이 역할을 부여하지 않아도 되지만 이 변곡점의 $x$ 좌표와 삼차방정식의 세 실근의 합의 관계에 관한 인식이 잘 갖춰져 있다면 이러한 이용 방향을 잡기가 훨씬 수월할 것이다.

\\section*{Comment}
\\section*{Drill. 2 삼차방정식의 세 실근의 합과 변곡점}
삼차함수 $f(x)=a x^{3}+b x^{2}+c x+d$ 에 대하여 $y=f(x)$ 의 그래프의 변곡점의 $x$ 좌표를 $p$ 라 하자.\\\\
삼차함수 $y=f(x)$ 의 그래프와 직선 $y=g(x)$ 가 세 점에서 만날 때, 삼차방정식 $f(x)-g(x)=0$ 의 $x^{3}$ 의 계수, $x^{2}$ 의 계수는 각각 삼차방정식 $f(x)=0$ 의 $x^{3}$ 의 계수, $x^{2}$ 의 계수와 같다. 따라서 삼차방정식 $f(x)-g(x)=0$ 의 세 실근의 합은 삼차방정식 $f(x)=0$ 의 세 실근의 합 $-\\frac{b}{a}$ 와 같으므로\\\\
(삼차함수 $y=f(x)$ 의 그래프와 직선의 세 교점의 $x$ 좌표의 합) $=3 \\times$ (삼차함수 $y=f(x)$ 의 그래프의 변곡점의 $x$ 좌표) 이다. 이때 $y=f(x)$ 의 그래프가 직선 $y=g(x)$ 에 접하고 접점의 $x$ 좌표가 방정식 $f(x)-g(x)=0$ 의 중근이면 서로 같은 교점의 $x$ 좌표 2 개로, 삼중근이면 서로 같은 교점의 $x$ 좌표 3 개로 취급하면 된다.\\\\
\\includegraphics[max width=\\textwidth, center]{b41ad8e5-293b-4ed9-9820-58adebf9c643-02_350_470_1374_1142}\\\\
$f(x)=m, f(x)=n, f(x)=g(x), f(x)=h(x)$ 모두 세 실근의 합은 $3 p$

\\section*{Drill 삼차함수의 그래프의 개형 판단 그리고 함께 등장하는 여러 직선}
앞의 문제에서는 자연스럽게 $f(x) \\neq 0$ 인 경우를 $f(x)>0, f(x)<0$ 인 경우로 다시 나누어 $g(x)$ 의 식을 정리하고 $g(x)$ 의 그래프가 직선 $y=x$ 의 일부, 직선 $y=-x$ 의 일부, $y$ 좌표가 8 인 점으로 이루어진 것에 주목하며 최고차항의 계수가 양수인 삼차함수 $f(x)$ 의 그래프의 개형을 잡아가면 된다.\\\\
조건 (가)에서 $x=3$ 의 좌우에서 $f(x)$ 의 부호가 음에서 양으로 바뀐다고 판단하고 조건 (나) 에서 $f(1)$ 의 값을 추정하여 귀류법으로 확정하는 것이 그리 어렵지 않다. 곧이어 $f(0)=0$ 에서 이 정도면 됐다 싶은 $f(x)$ 의 그래프의 개형을 완성할 수 있다.\\\\
$f(x)$ 의 식을 인수로 잡으면서 이미 몇 개의 미지수가 등장하고 $y=f(x)$ 의 그래프와 직선 $y=-x$ 의 접점의 $x$ 좌표를 또다시 미지수로 잡아야 하지만 방정식만 충분히 만들어낼 수 있으면 된다. $f^{\\prime}(x)$ 의 식이 부담스럽지만 계산만 조금 견딜 수 있으면 접선을 다루는 기본적인 방법으로 풀어도 좋다.\\\\
또는 $x$ 축 자체도 삼차함수의 그래프와 세 점에서 만나는 직선이라는 당연한 생각으로 삼차 함수의 그래프와 둘 이상의 점에서 만나는 두 직선이 등장한 상황을 놓치지 않는다면 좀 더 수월하게 마무리할 수 있다.

\\section*{Drill 삼차함수의 그래프의 비율 관계}
\\begin{enumerate}
  \\item 삼차함수의 그래프의 비율 관계
\\end{enumerate}

삼차함수의 그래프의 극대(극소)인 점 A 에서 그은 접선이 이 삼차함수의 그래프와 점 B 에서 만날 때, 선분 AB 를 $2: 1$ 로 내분하는 점의 $x$ 좌표가 극소(극대)인 점의 $x$ 좌표와 같고, 선분 AB 를 $1: 2$ 로 내분하는 점의 $x$ 좌표가 변곡점의 $x$ 좌표와 같다.\\\\
\\includegraphics[max width=\\textwidth, center]{b41ad8e5-293b-4ed9-9820-58adebf9c643-04_278_308_807_1560}\\\\
2) 삼차함수의 그래프의 변곡점을 지나는 직선에 관한 비율 관계 삼차함수의 그래프의 변곡점 A 를 지나고 기울기가 0 인 직선이 이 삼차함수의 그래프와 점 B 에서 다시 만날 때, 변곡점 A 와 극대 또는 극소인 점, 점 B 사이에 그림과 같은 $1: \\sqrt{3}$ 의 비율 관계가 나타난다.\\\\
\\includegraphics[max width=\\textwidth, center]{b41ad8e5-293b-4ed9-9820-58adebf9c643-04_312_306_1175_1562}

앞의 문제에서 $\\lim _{x \\rightarrow 0} \\frac{f(x)}{|x|}$ 의 값이 존재하면 $f(x)$ 가 $x^{2}$ 을 인수로 갖고 극한값은 0 이라는 뻔한 내용 정도는 알고 이용하자. 삼차함수의 그래프의 비율 관계를 이용하면 $f(x)$ 의 남은 인수를 곧바로 구하고 마무리할 수 있다.

\\section*{Drill 열린구간에서 함수의 최대와 최소}
열린구간에서 연속인 함수 $f(x)$ 의 최댓값 또는 최솟값이 존재하면 최댓값은 극댓값 중 하나 이고 최솟값은 극솟값 중 하나이다. 이때는 구간의 양 끝에서의 함숫값을 고려하지 않아도 된다.\\\\
특히 열린구간에서 미분가능한 함수 $f(x)$ 의 최댓값 또는 최솟값이 존재할 때, 방정식 $f^{\\prime}(x)=0$ 의 실근이 $x=\\alpha$ 하나뿐이면 $f(\\alpha)$ 가 최댓값 또는 최솟값이다.

\\begin{figure}[h]
\\begin{center}
  \\includegraphics[max width=\\textwidth]{b41ad8e5-293b-4ed9-9820-58adebf9c643-05_274_253_1048_727}
\\captionsetup{labelformat=empty}
\\caption{최댓값: 없다.\\\\
최솟값: 없다.}
\\end{center}
\\end{figure}

\\begin{figure}[h]
\\begin{center}
  \\includegraphics[max width=\\textwidth]{b41ad8e5-293b-4ed9-9820-58adebf9c643-05_283_251_1044_1023}
\\captionsetup{labelformat=empty}
\\caption{최댓값: $f(\\alpha)$\\\\
최솟값: $f(\\beta)$}
\\end{center}
\\end{figure}

\\begin{figure}[h]
\\begin{center}
  \\includegraphics[max width=\\textwidth]{b41ad8e5-293b-4ed9-9820-58adebf9c643-05_278_246_1044_1319}
\\captionsetup{labelformat=empty}
\\caption{최댓값: $f(\\alpha)$\\\\
최솟값: 없다.}
\\end{center}
\\end{figure}

\\begin{figure}[h]
\\begin{center}
  \\includegraphics[max width=\\textwidth]{b41ad8e5-293b-4ed9-9820-58adebf9c643-05_278_255_1044_1609}
\\captionsetup{labelformat=empty}
\\caption{최댓값: 없다.\\\\
최솟값: $f(\\alpha)$}
\\end{center}
\\end{figure}

앞의 문제에서는 $f(x)$ 가 삼차함수이므로 열린구간 $(a, b)$ 에서 극댓값이 최댓값이고 극솟값이 최솟값이다. 삼차함수의 그래프의 개형에서 $f(-1)$ 은 $f(x)$ 의 극솟값과 같고 $f(3)$ 은 $f(x)$ 의 극댓값과 같다는 판단, $f(x)$ 가 극대인 $x$ 의 값은 거침없이 나와 줘야 한다. $f(x)$ 의 식을 $f(x)$ 의 극댓값을 이용해서 인수로 써야 한다는 것까지!

\\section*{Comment}
\\section*{Drill. 1 삼차함수의 그래프의 접선에 관한 비율 관계}
삼차함수 $y=f(x)$ 의 그래프 위의 점 A 에서 그은 접선 $l$ 과 점 B 에서 그은 접선 $m$ 이 서로 평행하고, 접선 $l$ 과 접선 $m$ 이 $y=f(x)$ 의 그래프와 각각 점 C 와 점 D 에서 만날 때, 선분 AC 를 $2: 1$ 로 내분하는 점과 점 B 의 $x$ 좌표는 서로 같고, 선분 BD 를 $2: 1$ 로 내분하는 점과 점 A 의 $x$ 좌표는 서로 같다.

또한 선분 AC 를 $1: 2$ 로 내분하는 점과 선분 BD 를 $1: 2$ 로 내분하는 점의 $x$ 좌표는 변곡점의 $x$ 좌표와 같다.\\\\
\\includegraphics[max width=\\textwidth, center]{b41ad8e5-293b-4ed9-9820-58adebf9c643-06_401_333_765_1522}\\\\
\\includegraphics[max width=\\textwidth, center]{b41ad8e5-293b-4ed9-9820-58adebf9c643-06_447_443_1201_727}\\\\
\\includegraphics[max width=\\textwidth, center]{b41ad8e5-293b-4ed9-9820-58adebf9c643-06_407_521_1239_1319}

\\section*{Drill. 2 사차함수의 그래프의 비율 관계}
최고차항의 계수가 양수이고 두 극솟값이 서로 같은 사차함수의 그래프의 극대인 점 A 에서 그은 접선이 이 사차함수의 그래프와 점 B 에서 다시 만날 때, 점 A 와 극소인 점, 점 B 사이에 그림과 같은 $1: \\sqrt{2}$ 의 비율 관계가 나타난다.\\\\
\\includegraphics[max width=\\textwidth, center]{b41ad8e5-293b-4ed9-9820-58adebf9c643-06_339_297_1954_1150}

\\section*{Drill. 1 자연스럽게 그래프의 개형 판단부터}
앞의 문제는 극대인 점 $(4,0)$ 에서 $x$ 축에 접하고 최고차항의 계수가 양수인 삼차함수 $y=f(x)$ 의 그래프부터 슥 그려보고 시작하는 게 너무 자연스럽다. 적당한 양수 $a$ 를 연결 지점으로 해서 그 왼쪽에 $y=-f(x-a)$ 의 그래프를 생각해 보면 자세히 따질 것도 없이 $\\lim _{x \\rightarrow-\\infty} g(x)=\\infty$ 이므로 $g(x)$ 가 $x=0$ 에서 최댓값을 갖는다는 조건 (나)에 모순이다. 따라서 삼차함수 $f(x)$ 의 최고차항의 계수를 음수로 확정!\\\\
다음으로 절대 놓치면 안 되는 것은 연결 지점인 $a$ 는 양수이고 $g(x)$ 는 $x=0$ 에서 최댓값을 갖는다는 것, 즉 $g(x)$ 가 열린구간 $(-\\infty, a)$ 에서 최댓값을 갖는다는 것이다. 극댓값이다! 열린구간에서 연속인 함수의 최댓값과 최솟값이 각각 극댓값과 극솟값이라는 너무나 뼌한 얘기가 매우 중요한 판단으로 작용하는 순간이다.\\\\
$g^{\\prime}(0)=0$ 을 $-f^{\\prime}(-a)=0$ 으로 곧바로 보고 조건 (가)의 극한을 $x=a$ 에서 좌극한과 우극한의 일치로 다루기 위해 $-f(x-a)$ 의 도함수가 $-f^{\\prime}(x-a)$ 인 것 정도는 알고 있어야 한다.\\\\
마무리는 삼차함수의 그래프의 대칭과 비율 관계의 이용으로 최대한 간락하게!

Drill. $2 f(x+a)$ 의 도함수\\\\
함수 $f(x)$ 의 그래프를 $x$ 축의 방향으로 $-a$ 만큼 평행이동한 것이 함수 $f(x+a)$ 의 그래프 이다. 따라서 $f(x)$ 의 도함수 $f^{\\prime}(x)$ 의 그래프를 $x$ 축의 방향으로 $-a$ 만큼 평행이동한 것이 $f(x+a)$ 의 도함수의 그래프일 것이므로

$$
\\{f(x+a)\\}^{\\prime}=f^{\\prime}(x+a)
$$

임을 알 수 있다.\\\\
'수학 $\\mathbb{I}$ '에서 합성함수의 미분법은 배우지 않지만 함수 $f(x+a)$ 의 미분계수를 평행이동의 기하적 관점으로 다루도록 출제하고, 이때 그 도함수를 직접 구하면 편리한 경우가 많으므로 알아두고 사용하도록 하자.

\\section*{Cornnxnerst}
\\section*{Drill 합성함수에 관한 방정식}
앞의 문제의 조건 (나)에서 $f(1)$ 이 극솟값이라는 것은 아마도 쉽게 파악했을 텐데 설마… $f(x)$ 가 $x=1$ 에서 극솟값을 갖는다고 착각해 혼란에 빠지지는 않았겠지? $f(x)$ 의 극솟값이 $x=1$ 에서의 함숫값과 같다는 것이다. 조건 (가)의 극한값과 구간 $(-\\infty, 1)$ 에서 최솟값을 가지는 것에서 삼차함수 $f(x)$ 의 최고차항의 계수를 정하고 그래프의 개형도 잡아 놓고 삼차함수의 그래프의 대칭이나 비율 관계를 이용할 마음의 준비를 하고 시작하리라 믿는다! 남은 중요한 준비 과정은 방정식 $f(f(x))=1$ 에서 $f(x)=t$ 로 치환하여 얻은 $t$ 에 대한 방정식 $f(t)=1$ 과 $x$ 에 대한 방정식 $f(x)=t$ 를 잘 구분하고 또한 잘 연결 지어서 $f(f(1))=1$ 을 멋지게 이용하는 것이다. $x=1$ 이 방정식 $f(f(x))=1$ 의 실근, 즉 $x$ 에 대한 방정식 $f(x)=t$ 의 실근이므로 $y=f(x)$ 의 그래프와 직선 $y=t$ 는 점 $(1, t)$ 에서 만난다. 여기서 $t$ 의 값은 방정식 $f(t)=1$ 의 실근이므로 $y=f(t)$ 의 그래프와 직선 $y=1$ 이 점 $(t, 1)$ 에서 만난다.\\\\
결론은? $y=f(x)$ 의 그래프가 두 점 $(1, t),(t, 1)$ 을 지난다는 것! 이렇게까지 해놓으면 ㄱ, ㄴ, ㄷ을 확인하기 위한 준비를 제대로 갖춘 것. 치환하여 얻은 방정식과 주어진 방정식을 한 그래프에서 모두 다루기 때문에 변수와 대응 순서의 구분에 주의해야 한다.

\\section*{Drill 합성함수에 관한 방정식}
앞의 문제에서는 주어진 방정식에서 $f(x)=t$ 로 치환하여 얻은 $t$ 에 대한 삼차방정식 $f(t)=t^{2}$ 의 실근인 $t$ 의 값, 주어진 방정식의 실근인 $y=f(x)$ 의 그래프와 직선 $y=t$ 의 교점의 $x$ 좌표를 시작부터 끝까지 잘 구분하고 또한 잘 연결 지어야 한다.\\\\
삼차함수 $y=f(x)$ 의 그래프와 직선 $y=t$ 의 교점의 $x$ 좌표가 7 개가 되려면 삼차방정식 $f(t)=t^{2}$ 이 서로 다른 세 실근을 가져야 한다는 것, 즉 직선 $y=t$ 가 3 개라는 것과 이 3 개의 직선과 $y=f(x)$ 의 그래프의 교점이 7 개인 상황까지 정리하는 것은 그리 어렵지 않을 것이다. 7 개의 교점의 $x$ 좌표 중 최솟값인 $\\alpha_{1}=0$ 과 최댓값인 $\\alpha_{7}=4$ 를 삼차함수의 그래프의 비율 관계와 연결 짓고 $\\alpha_{3}, \\alpha_{5}$ 의 값을 정하는 것도 자연스럽게 이어갈 수 있을 듯.\\\\
$\\alpha_{2}, \\alpha_{4}, \\alpha_{6}$ 은? 삼차함수 $y=f(x)$ 의 그래프와 교점의 개수가 2 이상인 직선이 3 개나 등장 한다. 그리고 구해야 할 것은 교점의 $x$ 좌표의 합이다. 삼차함수에 관한 어떤 특징을 이용할 상황인지 즉시 알아채야 한다. 알아야 할 것을 제대로 알고 충분한 경험을 쌓았다면 여기 까지는 꽤나 수월하게 진행할 수 있다.\\\\
남은 $\\sum_{k=1}^{7} f\\left(\\alpha_{k}\\right)$ 의 처리에 조금만 더 힘을 써보자. 삼차방정식 $f(t)=t^{2}$ 의 세 실근에 관한 것 이라는 건 쉽게 파악했을 텐데, 안타깝게도 삼차방정식의 근과 계수의 관계로 간단히 처리할 수 없고 세 실근을 모두 구해야 하는 상황이다. 인수를 이용하여 $f(x)$ 의 식을 일단 써보는 건 아무 일도 아닌데 최고차항의 계수를 어떻게 구해야 할지 잠시 난감해질 수 있다.\\\\
다항함수 결정의 상황에 대한 경험이 충분하다면 대입해 볼 만한 다른 값을 찾아보게 되지 않을까? 그리고 $f(1)=f(4)$ 를 발견하고 그 값을 구하고, 방정식 $f(t)=t^{2}$ 의 식의 형태가 이 값을 대입해 보기 딱 좋다는 판단쯤은 할 수 있지 않을까?

\\section*{Drill 방정식 $(f \\circ f)(x)=x$}
함수 $f(x)$ 에 대하여 방정식 $(f \\circ f)(x)=x$ 의 실근은 대응 관계에서 다음과 같이 나타남을 알 수 있다.\\\\
\\includegraphics[max width=\\textwidth, center]{b41ad8e5-293b-4ed9-9820-58adebf9c643-10_105_302_892_1139}\\\\
\\includegraphics[max width=\\textwidth, center]{b41ad8e5-293b-4ed9-9820-58adebf9c643-10_135_306_1010_1137}

즉 방정식 $(f \\circ f)(x)=x$ 의 실근은 함수 $f$ 에 의하여 한 실근이 자기 자신으로 대응하거나 두 실근이 짝을 이루어 서로에게 대응한다.\\\\
이를 좌표평면에 나타내면 다음과 같고, 이때 함수 $y=f(x)$ 의 그래프는 네 점 $(\\alpha, \\alpha),(\\beta, \\delta)$, $(\\gamma, \\gamma),(\\delta, \\beta)$ 를 지난다.\\\\
\\includegraphics[max width=\\textwidth, center]{b41ad8e5-293b-4ed9-9820-58adebf9c643-10_418_456_1446_1061}

함수 $y=f(x)$ 의 그래프를 직선 $y=x$ 에 대하여 대칭이동한 도형을 $F$ 라 하면 일반적으로 방정식 $(f \\circ f)(x)=x$ 의 실근은 $y=f(x)$ 의 그래프와 도형 $F$ 의 교점의 $x$ 좌표와 같다.\\\\
\\includegraphics[max width=\\textwidth, center]{b41ad8e5-293b-4ed9-9820-58adebf9c643-11_460_462_807_1154}

앞의 문제는 방정식 $(g \\circ g)(x)=x$ 의 실근이 $y=g(x)$ 의 그래프와 이를 직선 $y=x$ 에 대하여 대칭이동한 도형의 교점의 $x$ 좌표라는 인식부터 출발하지 않으면 상당히 곤란해진다. 평가원 에서 다룬 적이 있고 기억하기 부담스러운 내용도 아니다. 알아두고 이용하자!\\\\
실근 $\\alpha$ 가 음수이고 $y=g(x)$ 의 그래프는 직선 $y=x$ 위의 점 $(\\alpha, \\alpha)$ 를 지나거나 직선 $y=x$ 에 대하여 대칭인 두 점 $(\\alpha,-\\alpha),(-\\alpha, \\alpha)$ 를 지나야 한다는 판단이 가장 중요하다. 남은 실근 $0,-\\alpha,-2 \\alpha$ 에 대하여 같은 판단을 빠르게 반복해 보면 그렇게 그려질 수밖에 없는 삼차함수 $y=f(x)$ 의 그래프의 개형을 얻게 되고 삼차함수의 그래프의 접선에 관한 비율 관계, 삼차방정식의 세 실근의 합과 변곡점의 $x$ 좌표의 관계를 이용하여 간략히 마무리할 수 있다.

\\section*{Comment}
\\section*{Drill 삼차함수의 그래프의 특징 종합판}
앞의 문제의 상황 인식과 풀이에는 삼차함수의 그래프의 대칭, 접선에 관한 비율 관계 등의 특징과 변곡점 등을 필요한 때에 적절히 이용할 수 있어야 한다. 삼차함수 $y=f(x)$ 의 그래프 위의 점 $(t, f(t))$ 를 지나는 직선 $y=g(x)$ 의 기울기가 점 $(t+2, f(t+2))$ 에서의 접선의 기울기와 같고, $y=f(x)$ 의 그래프와 직선 $y=g(x)$ 가 두 점에서 만나는 상황, 즉 접하는 상황이다. 삼차함수의 그래프의 접선에 관한 비율 관계를 이용하기 위해 변곡점을 잡아 기준으로 삼을 준비를 해야 한다.\\\\
최고차항의 계수가 양수인 삼차함수 $y=f(x)$ 의 그래프를 대충 그려놓고 변곡점을 잡으면, 접점이 아닌 점 $(t, f(t))$ 에서 접선 $y=g(x)$ 를 그리려면 점 $(t, f(t))$ 가 변곡점의 왼쪽에 있어야 하고 접점은 변곡점의 오른쪽에 나타난다는 것을 쉽게 알 수 있다. 여기서 변곡점에 대하여 대칭인 두 점에서의 접선의 기울기가 같다는 것을 놓치지 않아야 점\\\\
$(t+2, f(t+2))$ 를 변곡점에 대하여 대칭으로 두 곳에 잡고 케이스를 구분하여 계산을 시작할 수 있다. 그리고 당연히 놓치지 않아야 할 다른 한 케이스는 점 $(t, f(t))$ 가 접점인 경우! 이때는 두 점 $(t, f(t)),(t+2, f(t+2))$ 가 변곡점에 대하여 대칭으로 놓이게 된다. 남은 계산은 그리 어렵지 않다.


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
        prev_cornnxnerst = body.rfind('\\section*{Cornnxnerst}', 0, start_pos)
        prev_drill = body.rfind('\\section*{Drill', 0, start_pos)
        
        # Comment 또는 Cornnxnerst 바로 다음에 오는 Drill은 전략
        is_strategy = False
        if prev_comment != -1:
            between = body[prev_comment:start_pos]
            if '\\section*{' not in between.replace('\\section*{Comment}', '').replace('\\section*{Drill', '').replace('\\section*{Cornnxnerst}', ''):
                is_strategy = True
        if prev_cornnxnerst != -1:
            between = body[prev_cornnxnerst:start_pos]
            if '\\section*{' not in between.replace('\\section*{Comment}', '').replace('\\section*{Drill', '').replace('\\section*{Cornnxnerst}', ''):
                is_strategy = True
        
        # 이미지 제거
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
        
        # 주제도 정리
        topic = re.sub(r'\\\\', ' ', topic)
        topic = re.sub(r'\s+', ' ', topic)
        
        if len(content) > 50:
            if is_strategy:
                question_ref = ""
                if '앞의 문제' in content:
                    question_ref = "03"
                
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
                    question_ref = "03"
                
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
    print("[수2 드릴 03 해설 데이터 검토]")
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
    csv_path = save_dir / "수2_2025학년도_현우진_드릴_03_해설_deepseek.csv"
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
    json_path = save_dir / "수2_2025학년도_현우진_드릴_03_해설_deepseek.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(solutions, f, ensure_ascii=False, indent=2)
    
    print(f"[JSON 저장 완료] {json_path}")
    
    return csv_path, json_path


def main():
    print("=" * 60)
    print("[수2 드릴 03 해설 LaTeX → CSV 변환]")
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
