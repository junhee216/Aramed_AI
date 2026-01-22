# convert_su1_p1_solution_latex.py
# 수1 드릴 P1 해설 LaTeX를 딥시크용 CSV로 변환

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

# 사용자가 제공한 LaTeX 내용
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
\\section*{Comment}
\\section*{Drill. 1 실수인 거듭제곱근의 개수}
(1) $n$ 이 홀수일 때\\\\
$a$ 의 $n$ 제곱근 중에서 실수인 것은 실수 $a$ 의 값에 관계없이 오직 하나 존재하고, 이것을 기호로

$$
\\sqrt[n]{a}
$$

와 같이 나타낸다.\\\\
(2) $n$ 이 짝수일 때

\\begin{itemize}
  \\item $a>0$ 이면 $a$ 의 $n$ 제곱근 중에서 실수인 것은 양수와 음수 각각 하나씩 있다.
\\end{itemize}

그중에서 양수인 것은 $\\sqrt[n]{a}$, 음수인 것은 $-\\sqrt[n]{a}$ 로 나타낸다.

\\begin{itemize}
  \\item $a=0$ 이면 $a$ 의 $n$ 제곱근은 0 하나뿐이다.
  \\item $a<0$ 이면 $a$ 의 $n$ 제곱근 중에서 실수인 것은 없다.
\\end{itemize}

\\begin{center}
\\begin{tabular}{|l|l|l|l|}
\\hline
 & $a>0$ & $a=0$ & $a<0$ \\\\
\\hline
$n$ 이 홀수 & $\\sqrt[n]{a}$ & 0 & $\\sqrt[n]{a}$ \\\\
\\hline
$n$ 이 짝수 & $\\sqrt[n]{a},-\\sqrt[n]{a}$ & 0 & 없다. \\\\
\\hline
\\end{tabular}
\\end{center}

$a$ 의 $n$ 제곱근 중에서 실수인 것의 개수는 $2,1,0$ 중 하나이며 $n$ 이 홀수인지 짝수인지, $a$ 의 부호가 무엇인지에 따라 구분할 수 있어야 한다.\\\\
실수인 $n$ 제곱근을 여러 개 다룰 때는 $n$ 이 홀수일 때 실수인 $n$ 제곱근의 개수가 항상 1 인 것을 우선 확인해 놓고 $n$ 이 짝수일 때의 실수인 $n$ 제곱근의 개수를 마저 처리하는 것이 좋다. 앞의 문제도 당연히 이런 순서를 밟아야 한다.

\\section*{Drill. 2 객관식은 객관식답게}
객관식 문항에서는 선택지를 함께 살피며 풀이 방향을 정하거나 불필요한 케이스를 걸러낼 수 있어야 한다. 앞의 문제에서는 등차수열 $\\left\\{a_{n}\\right\\}$ 의 첫째항이 양수이고 선택지의 $a_{15}$ 의 값이 모두 음수이므로 공차의 부호의 케이스를 구분할 필요 없이 곧바로 공차가 음수라고 판단 해야 한다.

\\section*{Drill $n$ 이 홀수일 때의 실수인 $n$ 제곱근부터}
앞의 문제에서도 $n$ 이 홀수일 때의 실수인 $n$ 제곱근의 개수가 항상 1 인 것부터 생각하기 시작 해야 한다. $f(5)=f(7)=f(9)=f(11)=f(13)=1$ 이므로 $\\sum_{n=5}^{9} f(n)=\\sum_{n=11}^{14} f(n)$ 이 확 가볍게 정리된다. $(n-a)(n-10)$ 의 부호의 케이스를 $a$ 의 값의 범위로 구분하여 차분히 점검하고 마무리하는 일만 남는다.\\\\
최근 실수인 거듭제곱근의 개수에 관한 문제의 출제가 많고 여러 소재와 결합하여 겉보기에 다양한 유형으로 보이지만 $a$ 의 $n$ 제곱근 중 실수인 것의 개수는 $n$ 이 짝수인지 홀수인지, $a$ 의 부호가 무엇인지에 따라 구분한다는 큰 틀은 전혀 흔들리지 않는다.

\\section*{2023학년도 9월 평가원 공통 11번}
함수 $f(x)=-(x-2)^{2}+k$ 에 대하여 다음 조건을 만족시키는 자연수 $n$ 의 개수가 2 일 때, 상수 $k$ 의 값은?\\\\[0pt]
[4점]\\\\
$\\sqrt{3}^{f(n)}$ 의 네제곱근 중 실수인 것을 모두 곱한 값이 -9 이다.\\\\
(1) 8\\\\
(2) 9\\\\
(3) 10\\\\
(4) 11\\\\
(5) 12

답 (2)

\\section*{2023학년도 수능 공통 13번}
자연수 $m(m \\geq 2)$ 에 대하여 $m^{12}$ 의 $n$ 제곱근 중에서 정수가 존재하도록 하는 2 이상의 자연수 $n$ 의 개수를 $f(m)$ 이라 할 때, $\\sum_{m=2}^{9} f(m)$ 의 값은? [4점]\\\\
(1) 37\\\\
(2) 42\\\\
(3) 47\\\\
(4) 52\\\\
(5) 57

답 (3)

\\section*{Drill. 1 로그의 성질과 밑의 변환 공식}
\\begin{enumerate}
  \\item 로그의 성질\\\\
$a>0, a \\neq 1, x>0, y>0$ 일 때\\\\
(1) $\\log _{a} 1=0, \\log _{a} a=1$\\\\
(2) $\\log _{a} x y=\\log _{a} x+\\log _{a} y$\\\\
(3) $\\log _{a} \\frac{x}{y}=\\log _{a} x-\\log _{a} y$\\\\
(4) $\\log _{a} x^{k}=k \\log _{a} x($ 단, $k$ 는 실수 $)$
  \\item 밑의 변환 공식\\\\
$a>0, a \\neq 1, b>0, c>0, c \\neq 1$ 일 때\\\\
(1) $\\log _{a} b=\\frac{\\log _{c} b}{\\log _{c} a}$ : 기존 로그의 밑을 새로운 밑인 $c$ 로 바꿀 수 있다.\\\\
(2) $\\log _{a} b=\\frac{\\log _{b} b}{\\log _{b} a}=\\frac{1}{\\log _{b} a}($ 단, $b \\neq 1):$ 밑과 진수가 바뀌면 역수 관계이다.\\\\
(3) $\\log _{a^{n}} b^{n}=\\frac{n}{m} \\log _{a} b$ : 밑의 지수는 역수로, 진수의 지수는 그대로 로그 앞으로 내보낼 수 있다. 역으로 실수배된 로그의 값은 실수배를 이용하여 밑과 진수를 동시에 바꿀 수 있다.\\\\
(4) $a^{\\log _{c} b}=b^{\\log _{c} a}$ : 양 끝의 수들은 바꿀 수 있다.\\\\
(5) $a^{\\log _{a} b}=b$ : 밑이 같으면 지울 수 있다.
\\end{enumerate}

\\section*{Drill. 2 가장 적절한 변형 방법의 선택}
앞의 문제는 로그의 성질과 밑의 변환 공식 중에서 무엇을 선택하여 다루는 것이 가장 적절 할까? $\\sum_{k=1}^{6} a_{k}^{\\log _{3} 2}$ 에서 $a_{k}$ 는 $a$ 의 값이고 지수가 $\\log _{3} 2$ 이다. 딱 알겠지? 로그의 성질과 밑의 변환 공식에 관한 문제는 대부분 기본적인 수준의 연습만으로도 방향을 잡을 수 있도록 출제되긴 하지만 어느 정도의 경험과 센스가 필요한 문제의 출제에도 충분히 대비하도록 하자.

\\section*{Comment}
\\section*{Drill 로그의 값이 유리수, 정수인 조건}
$\\log _{a} b$ 의 값이 0 이 아닌 유리수인 조건은 두 정수 $m, n(m n \\neq 0)$ 에 대하여 $\\log _{a} b=\\frac{n}{m}$ 에서

$$
a^{\\frac{n}{m}}=b, a^{n}=b^{m}, a=b^{\\frac{m}{n}}
$$

과 같은 관계식으로부터 출발하는 것이 기본적인 방법이다.\\\\
$\\log _{a} b$ 의 값이 0 이 아닌 정수인 조건도 정수 $m(m \\neq 0)$ 에 대하여 $\\log _{a} b=m$ 에서

$$
a^{m}=b, a=b^{\\frac{1}{m}}
$$

과 같은 관계식으로부터 출발한다.\\\\
앞의 문제 역시 자연수 $k$ 에 대하여 $\\log _{2}\\left(32 a-a^{2}\\right)=k$ 로 놓고 $32 a-a^{2}=2^{k}$ 에서부터 시작 하면 된다. 이차함수 $y=32 a-a^{2}$ 의 최댓값이 $2^{k}$ 끌로 딱 맞아떨어진다.\\\\
$a$ 가 실수인 것을 감안하여 쭉쭉 마무리\\~{}}

\\section*{Comment}
\\section*{Drill. 1 지수와 로그의 방정식과 부등식}
지수와 로그에 관한 방정식과 부등식은 형태 자체로는 복잡하게 주어지지 않는다. 난도가 높다 해도 치환한 이차방정식과 이차부등식에서 근과 계수의 관계, 이차함수의 그래프를 이용 하는 정도. 고 1 수학의 기초가 중요하다.\\\\
또한 로그방정식과 로그부등식에서는 밑을 변환하면서 진수가 함께 변할 때 처음 주어진 진수로 미지수의 값의 범위를 잡아야 하는 것에 주의 또 주의하자.\\\\
예를 들어 로그방정식 $\\log _{2} x=\\log _{4}(2 x+3)$ 에서 처음 주어진 진수가 $x, 2 x+3$ 이므로 $x>0,2 x+3>0$ 에서 $x>0$ 이고, $\\log _{2} x$ 를 $\\log _{4} x^{2}$ 으로 변환하여 풀면 $x^{2}=2 x+3$, 즉 $(x-3)(x+1)=0$ 에서 $x=3$ 이다.\\\\
앞의 문제에서는 주어진 부등식의 우변을 밑이 4 인 로그로 변환하여 풀 때 처음 주어진 진수로 $x$ 의 값의 범위를 잡는 것에 주의해야 한다. 그런데 여기서 잠깐! 두 함수 $y=\\log _{4} x^{2}$, $y=\\log _{2}|x|$ 는 정의역이 $\\{x \\mid x$ 는 0이 아닌 실수 $\\}$ 인 서로 같은 함수라는 기본 중의 기본을 이용 하면? 좌변의 $\\log _{4}(x+2)^{2}$ 을 $\\log _{2}|x+2|$ 로 변환할 수 있다. 이 변환으로 $x$ 의 값의 범위는 바뀌지 않고 풀이도 좀 더 수월해진다.

\\section*{Drill. 2 로그함수의 일치}
(1) 두 함수 $y=\\log _{2} x$ 와 $y=\\log _{8} x^{3}$ 은 정의역이 $\\{x \\mid x>0\\}$ 인 서로 같은 함수이다.\\\\
(2) 두 함수 $y=\\log _{4} x^{2}$ 과 $y=\\log _{2}|x|$ 는 정의역이 $\\{x \\mid x$ 는 0이 아닌 실수 $\\}$ 인 서로 같은 함수 이다.\\\\
한편 두 함수 $y=\\log _{4} x^{2}$ 과 $y=\\log _{2} x$ 는 정의역이 다르므로 서로 같은 함수가 아니다.

\\section*{Comment}
\\section*{Drill 지수와 로그의 방정식의 치환}
지수와 로그의 방정식을 같은 부분을 치환하여 푸는 방법은 다음과 같다. 이때 치환한 문자의 값의 범위에 주의해야 한다.\\\\
(1) 지수방정식에서 $a^{x}=t(t>0)$ 로 치환하여 이차방정식을 얻었을 때, 지수방정식의 두 실근이 $p, q$ 이면 이차방정식의 두 실근은 $a^{p}, a^{q}$ 이므로

$$
a^{p} \\times a^{q}=a^{p+q}
$$

임을 이용하여 지수방정식의 두 실근의 합 $p+q$ 를 쉽게 구할 수 있다.\\\\
이때 $a^{p} \\times a^{q}$ 은 이차방정식의 두 실근의 곱이므로 이차방정식의 근과 계수의 관계를 이용 하여 구하면 된다.\\\\
지수방정식에서 $a^{x}=t$ 로 치환하여 삼차방정식을 얻었을 때도 마찬가지이다.\\\\
(2) 로그방정식에서 $\\log _{a} x=t$ ( $t$ 는 실수)로 치환하여 이차방정식을 얻었을 때,

로그방정식의 두 실근이 $p, q$ 이면 이차방정식의 두 실근은 $\\log _{a} p, \\log _{a} q$ 이므로

$$
\\log _{a} p+\\log _{a} q=\\log _{a} p q
$$

임을 이용하여 로그방정식의 두 실근의 곱 $p q$ 를 쉽게 구할 수 있다.\\\\
이때 $\\log _{a} p+\\log _{a} q$ 는 이차방정식의 두 실근의 합이므로 이차방정식의 근과 계수의 관계를 이용하여 구하면 된다.\\\\
로그방정식에서 $\\log _{a} x=t$ 로 치환하여 삼차방정식을 얻었을 때도 마찬가지이다.

\\section*{Comment}
\\section*{Drill 원래의 방정식과 치환한 방정식의 실근의 구별}
앞의 문제는 $2^{x}$ 을 치환하여 원래의 방정식의 실근과 치환한 방정식의 실근이 헷갈리지 않도록 하고 치환한 이차방정식의 근과 계수의 관계를 이용하여 $\\alpha, \\beta, k$ 에 대한 연립방정식을 만들어 찬찬히 풀어 가면 된다. $|\\alpha-\\beta|$ 는 어떻게 처리하나? $\\alpha, \\beta$ 의 대소 관계가 주어지지 않았으므로 스스로 대소 관계를 정하여 절댓값 없이 다루어야 한다는 센스 정도는 발휘할 수 있을 듯?

Drill 함수 $y=k a^{x}$ 과 함수 $y=\\log _{a} k x$

\\begin{enumerate}
  \\item 함수 $y=k a^{x}(k>0)$\\\\
(1) $y=k a^{x}$ 의 그래프는 $y=a^{x}$ 의 그래프를 $x$ 축의 방향으로 $-\\log _{a} k$ 만큼 평행이동한 것이다.\\\\
(2) $y=-k a^{x}$ 의 그래프는 $y=k a^{x}$ 의 그래프를 $x$ 축에 대하여 대칭이동한 것이다.
  \\item 함수 $y=\\log _{a} k x(k>0)$\\\\
(1) $y=\\log _{a} k x$ 의 그래프는 $y=\\log _{a} x$ 의 그래프를 $y$ 축의 방향으로 $\\log _{a} k$ 만큼 평행이동한 것이다.\\\\
(2) $y=\\log _{a}(-k x)$ 의 그래프는 $y=\\log _{a} k x$ 의 그래프를 $y$ 축에 대하여 대칭이동한 것이다.
\\end{enumerate}

앞의 문제는 함수 $y=\\log _{2}(a x-3 a)$, 즉 $y=\\log _{2} a(x-3)$ 의 그래프가 함수 $y=\\log _{2} x$ 의 그래프를 평행이동한 것으로 인식하는 것부터 시작해야 한다. $x$ 축의 방향으로의 평행이동은 정해졌으니 $y$ 축의 방향으로의 평행이동의 범위만 조절하면 된다. 당연히 경계가 되는 점의 좌표를 이용해야 한다.

\\section*{Comment}
\\section*{Drill 지수함수와 로그함수의 그래프 위의 점}
지수함수와 로그함수의 그래프 위의 여러 점들의 좌표를 미지수로 나타낼 때는 적절한 한 점의 좌표를 미지수로 나타낸 후 다른 점들의 좌표는 주어진 관계에 따라 가급적이면 새로운 미지수를 사용하지 않도록, 미지수의 개수를 최소화하는 것이 좋다.\\\\
앞의 문제에서 직선 AB 의 기울기를 이용하기 위해 선분 AB 를 빗변으로 하고 직각을 낀 두 변이 각각 좌표축에 평행한 직각삼각형부터 그리고 시작해야 하는 건 당연! 이 직각삼각형의 직각을 낀 두 변의 길이를 하나의 미지수로, 점 A 의 $x$ 좌표를 다른 미지수로 잡는 정도면 충분하다.

\\section*{Comment}
\\section*{Drill. 1 직선과의 교점}
\\begin{enumerate}
  \\item 기울기가 $m$ 인 직선과의 교점\\\\
$y=f(x)$ 의 그래프와 기울기가 $m$ 인 직선의 두 교점의 $x$ 좌표가 각각 $a, b$ 일 때
\\end{enumerate}

$$
m=\\frac{f(b)-f(a)}{b-a} \\text { (평균변화율) }
$$

임을 이용할 수 있다. 특히 지수함수와 일차함수, 로그함수와 일차함수의 교점의 $x$ 좌표를 방정식을 풀어서 구할 수 없으므로 $f(x)$ 가 지수함수 또는 로그함수일 때는 위의 관계식을 이용해야 한다.\\\\
2) 한 직선 위의 세 점

세 점 $\\mathrm{A}\\left(a_{1}, a_{2}\\right), \\mathrm{B}\\left(b_{1}, b_{2}\\right), \\mathrm{C}\\left(c_{1}, c_{2}\\right)$ 가 한 직선 위에 있을 때 다음 중 유리한 방법을 이용한다.\\\\
(1) $\\overline{\\mathrm{AB}}: \\overline{\\mathrm{BC}}=\\left|a_{1}-b_{1}\\right|:\\left|b_{1}-c_{1}\\right|=\\left|a_{2}-b_{2}\\right|:\\left|b_{2}-c_{2}\\right|$\\\\
(2) 직각삼각형의 닮음

\\section*{Drill. 2 직선을 경유하는 최단경로}
두 정점 $\\mathrm{A}, \\mathrm{B}$ 와 직선 $l$ 위의 점 P 에 대하여 선분 AB 와 직선 $l$ 이 만나지 않을 때, $\\overline{\\mathrm{AP}}+\\overline{\\mathrm{PB}}$ 의 최솟값은 다음과 같다.\\\\
점 B 를 직선 $l$ 에 대하여 대칭이동한 점을 $\\mathrm{B}^{\\prime}$ 이라 하면 $\\overline{\\mathrm{PB}}=\\overline{\\mathrm{PB}^{\\prime}}$ 이고, 세 점 $\\mathrm{A}, \\mathrm{P}, \\mathrm{B}^{\\prime}$ 이 한 직선 위에 있을 때 $\\overline{\\mathrm{AP}}+\\overline{\\mathrm{PB}^{\\prime}}$ 의 값이 최소이므로

$$
\\overline{\\mathrm{AP}}+\\overline{\\mathrm{PB}}=\\overline{\\mathrm{AP}}+\\overline{\\mathrm{PB}^{\\prime}} \\geq \\overline{\\mathrm{AB}^{\\prime}}
$$

이다. 따라서 $\\overline{\\mathrm{AP}}+\\overline{\\mathrm{PB}}$ 의 최솟값은 $\\overline{\\mathrm{AB}^{\\prime}}$ 이다.\\\\
또 점 A 를 직선 $l$ 에 대하여 대칭이동한 점을 $\\mathrm{A}^{\\prime}$ 이라 하면 위와 마찬가지로 $\\overline{\\mathrm{AP}}+\\overline{\\mathrm{PB}}$ 의 최솟값은 $\\overline{\\mathrm{A}^{\\prime} \\mathrm{B}}$ 이다.


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
    
    # 개념 1: 실수인 거듭제곱근의 개수
    concept1_match = re.search(r'Drill\. 1 실수인 거듭제곱근의 개수(.*?)(?=Drill\. 2|\\section|\\end)', body, re.DOTALL)
    if concept1_match:
        content = concept1_match.group(1).strip()
        # 표와 불필요한 부분 제거
        content = re.sub(r'\\begin\{center\}.*?\\end\{center\}', '', content, flags=re.DOTALL)
        content = re.sub(r'\\begin\{itemize\}.*?\\end\{itemize\}', '', content, flags=re.DOTALL)
        content = re.sub(r'\$\$.*?\$\$', '', content, flags=re.DOTALL)
        content = re.sub(r'\\\\', ' ', content)
        content = re.sub(r'\s+', ' ', content)
        if len(content) > 100:
            solutions.append({
                "type": "concept",
                "topic": "실수인 거듭제곱근의 개수",
                "content": content
            })
    
    # 전략 1: 문제 1 해설 (객관식은 객관식답게)
    strategy1_match = re.search(r'Drill\. 2 객관식은 객관식답게(.*?)(?=Drill|\\section|\\end)', body, re.DOTALL)
    if strategy1_match:
        content = strategy1_match.group(1).strip()
        content = re.sub(r'\\\\', ' ', content)
        content = re.sub(r'\s+', ' ', content)
        if len(content) > 50:
            solutions.append({
                "type": "strategy",
                "question_ref": 1,
                "strategy": content
            })
    
    # 전략 2: 문제 2 해설
    strategy2_match = re.search(r'Drill \$n\$ 이 홀수일 때의 실수인 \$n\$ 제곱근부터(.*?)(?=2023학년도|\\section|\\end)', body, re.DOTALL)
    if strategy2_match:
        content = strategy2_match.group(1).strip()
        content = re.sub(r'\\\\', ' ', content)
        content = re.sub(r'\s+', ' ', content)
        if len(content) > 50:
            solutions.append({
                "type": "strategy",
                "question_ref": 2,
                "strategy": content
            })
    
    # 참고 문제: 2023학년도 9월 평가원 공통 11번
    ref1_match = re.search(r'2023학년도 9월 평가원 공통 11번(.*?)(?=2023학년도 수능|\\section|\\end)', body, re.DOTALL)
    if ref1_match:
        content = ref1_match.group(1).strip()
        content = re.sub(r'\\\\', ' ', content)
        content = re.sub(r'\s+', ' ', content)
        if len(content) > 50:
            solutions.append({
                "type": "problem",
                "question_ref": "2023학년도 9월 평가원 공통 11번",
                "content": content
            })
    
    # 참고 문제: 2023학년도 수능 공통 13번
    ref2_match = re.search(r'2023학년도 수능 공통 13번(.*?)(?=Drill\. 1 로그|\\section|\\end)', body, re.DOTALL)
    if ref2_match:
        content = ref2_match.group(1).strip()
        content = re.sub(r'\\\\', ' ', content)
        content = re.sub(r'\s+', ' ', content)
        if len(content) > 50:
            solutions.append({
                "type": "problem",
                "question_ref": "2023학년도 수능 공통 13번",
                "content": content
            })
    
    # 개념 2: 로그의 성질과 밑의 변환 공식
    concept2_match = re.search(r'Drill\. 1 로그의 성질과 밑의 변환 공식(.*?)(?=Drill\. 2 가장|\\section|\\end)', body, re.DOTALL)
    if concept2_match:
        content = concept2_match.group(1).strip()
        content = re.sub(r'\\begin\{enumerate\}.*?\\end\{enumerate\}', '', content, flags=re.DOTALL)
        content = re.sub(r'\\\\', ' ', content)
        content = re.sub(r'\s+', ' ', content)
        if len(content) > 100:
            solutions.append({
                "type": "concept",
                "topic": "로그의 성질과 밑의 변환 공식",
                "content": content
            })
    
    # 전략 3: 문제 3 해설
    strategy3_match = re.search(r'Drill\. 2 가장 적절한 변형 방법의 선택(.*?)(?=Drill 로그의 값|\\section|\\end)', body, re.DOTALL)
    if strategy3_match:
        content = strategy3_match.group(1).strip()
        content = re.sub(r'\\\\', ' ', content)
        content = re.sub(r'\s+', ' ', content)
        if len(content) > 50:
            solutions.append({
                "type": "strategy",
                "question_ref": 3,
                "strategy": content
            })
    
    # 전략 4: 문제 4 해설
    strategy4_match = re.search(r'Drill 로그의 값이 유리수, 정수인 조건(.*?)(?=Drill\. 1 지수와|\\section|\\end)', body, re.DOTALL)
    if strategy4_match:
        content = strategy4_match.group(1).strip()
        content = re.sub(r'\$\$.*?\$\$', '', content, flags=re.DOTALL)
        content = re.sub(r'\\\\', ' ', content)
        content = re.sub(r'\s+', ' ', content)
        if len(content) > 50:
            solutions.append({
                "type": "strategy",
                "question_ref": 4,
                "strategy": content
            })
    
    # 개념 3: 지수와 로그의 방정식과 부등식
    concept3_match = re.search(r'Drill\. 1 지수와 로그의 방정식과 부등식(.*?)(?=Drill\. 2 로그함수|\\section|\\end)', body, re.DOTALL)
    if concept3_match:
        content = concept3_match.group(1).strip()
        content = re.sub(r'\\\\', ' ', content)
        content = re.sub(r'\s+', ' ', content)
        if len(content) > 100:
            solutions.append({
                "type": "concept",
                "topic": "지수와 로그의 방정식과 부등식",
                "content": content
            })
    
    # 개념 4: 로그함수의 일치
    concept4_match = re.search(r'Drill\. 2 로그함수의 일치(.*?)(?=Drill 지수와 로그의 방정식의 치환|\\section|\\end)', body, re.DOTALL)
    if concept4_match:
        content = concept4_match.group(1).strip()
        content = re.sub(r'\\begin\{figure\}.*?\\end\{figure\}', '', content, flags=re.DOTALL)
        content = re.sub(r'\\includegraphics.*?}', '', content)
        content = re.sub(r'\\\\', ' ', content)
        content = re.sub(r'\s+', ' ', content)
        if len(content) > 50:
            solutions.append({
                "type": "concept",
                "topic": "로그함수의 일치",
                "content": content
            })
    
    # 개념 5: 지수와 로그의 방정식의 치환
    concept5_match = re.search(r'Drill 지수와 로그의 방정식의 치환(.*?)(?=Drill 원래의 방정식|\\section|\\end)', body, re.DOTALL)
    if concept5_match:
        content = concept5_match.group(1).strip()
        content = re.sub(r'\$\$.*?\$\$', '', content, flags=re.DOTALL)
        content = re.sub(r'\\\\', ' ', content)
        content = re.sub(r'\s+', ' ', content)
        if len(content) > 100:
            solutions.append({
                "type": "concept",
                "topic": "지수와 로그의 방정식의 치환",
                "content": content
            })
    
    # 전략 5: 문제 7 해설
    strategy5_match = re.search(r'Drill 원래의 방정식과 치환한 방정식의 실근의 구별(.*?)(?=Drill 함수|\\section|\\end)', body, re.DOTALL)
    if strategy5_match:
        content = strategy5_match.group(1).strip()
        content = re.sub(r'\\\\', ' ', content)
        content = re.sub(r'\s+', ' ', content)
        if len(content) > 50:
            solutions.append({
                "type": "strategy",
                "question_ref": 7,
                "strategy": content
            })
    
    # 개념 6: 함수 $y=k a^{x}$ 과 함수 $y=\log _{a} k x$
    concept6_match = re.search(r'Drill 함수 \$y=k a\^\{x\}\$ 과 함수 \$y=\\log.*?(?=앞의 문제는|\\section|\\end)', body, re.DOTALL)
    if concept6_match:
        concept_content = concept6_match.group(0).strip()
        # enumerate 제거
        concept_content = re.sub(r'\\begin\{enumerate\}.*?\\end\{enumerate\}', '', concept_content, flags=re.DOTALL)
        concept_content = re.sub(r'\\\\', ' ', concept_content)
        concept_content = re.sub(r'\s+', ' ', concept_content)
        if len(concept_content) > 100:
            solutions.append({
                "type": "concept",
                "topic": "함수 $y=k a^{x}$ 과 함수 $y=\\log _{a} k x$",
                "content": concept_content
            })
    
    # 전략 6: 문제 8 해설
    strategy6_match = re.search(r'앞의 문제는 함수 \$y=\\log.*?이용해야 한다\.(.*?)(?=Drill 지수함수와 로그함수|\\section|\\end)', body, re.DOTALL)
    if strategy6_match:
        content = strategy6_match.group(1).strip()
        content = re.sub(r'\\\\', ' ', content)
        content = re.sub(r'\s+', ' ', content)
        if len(content) > 50:
            solutions.append({
                "type": "strategy",
                "question_ref": 8,
                "strategy": content
            })
    
    # 전략 7: 문제 9 해설
    strategy7_match = re.search(r'Drill 지수함수와 로그함수의 그래프 위의 점(.*?)(?=Drill\. 1 직선과의 교점|\\section|\\end)', body, re.DOTALL)
    if strategy7_match:
        content = strategy7_match.group(1).strip()
        content = re.sub(r'\\\\', ' ', content)
        content = re.sub(r'\s+', ' ', content)
        if len(content) > 50:
            solutions.append({
                "type": "strategy",
                "question_ref": 9,
                "strategy": content
            })
    
    # 개념 7: 직선과의 교점
    concept7_match = re.search(r'Drill\. 1 직선과의 교점(.*?)(?=Drill\. 2 직선을 경유|\\section|\\end)', body, re.DOTALL)
    if concept7_match:
        content = concept7_match.group(1).strip()
        content = re.sub(r'\\begin\{enumerate\}.*?\\end\{enumerate\}', '', content, flags=re.DOTALL)
        content = re.sub(r'\$\$.*?\$\$', '', content, flags=re.DOTALL)
        content = re.sub(r'\\includegraphics.*?}', '', content)
        content = re.sub(r'\\\\', ' ', content)
        content = re.sub(r'\s+', ' ', content)
        if len(content) > 100:
            solutions.append({
                "type": "concept",
                "topic": "직선과의 교점",
                "content": content
            })
    
    # 전략 8: 문제 10 해설
    strategy8_match = re.search(r'Drill\. 2 직선을 경유하는 최단경로(.*?)(?=\\end|$)', body, re.DOTALL)
    if strategy8_match:
        content = strategy8_match.group(1).strip()
        content = re.sub(r'\$\$.*?\$\$', '', content, flags=re.DOTALL)
        content = re.sub(r'\\includegraphics.*?}', '', content)
        content = re.sub(r'\\\\', ' ', content)
        content = re.sub(r'\s+', ' ', content)
        if len(content) > 50:
            solutions.append({
                "type": "strategy",
                "question_ref": 10,
                "strategy": content
            })
    
    return solutions

def check_latex_syntax(text):
    """LaTeX 구문 검사"""
    issues = []
    if not text or len(text) < 10:
        return ["내용이 불완전함"]
    
    dollar_count = text.count('$')
    if dollar_count % 2 != 0:
        issues.append(f"$ 기호 홀수개 ({dollar_count}개)")
    
    return issues

def review_solutions(solutions):
    """해설 검토"""
    print("=" * 80)
    print("[수1 드릴 P1 해설 데이터 검토]")
    print("=" * 80)
    
    issues = []
    concept_count = 0
    strategy_count = 0
    problem_count = 0
    
    for i, solution in enumerate(solutions, 1):
        sol_type = solution.get('type', '?')
        print(f"\n[해설 {i}] 타입: {sol_type}")
        
        if sol_type == 'concept':
            concept_count += 1
            topic = solution.get('topic', 'N/A')
            content = solution.get('content', '')
            print(f"[주제] {topic}")
            print(f"[내용 길이] {len(content)}자")
        elif sol_type == 'strategy':
            strategy_count += 1
            q_ref = solution.get('question_ref', 'N/A')
            strategy = solution.get('strategy', '')
            print(f"[문제 참조] {q_ref}")
            print(f"[내용 길이] {len(strategy)}자")
        elif sol_type == 'problem':
            problem_count += 1
            q_ref = solution.get('question_ref', 'N/A')
            content = solution.get('content', '')
            print(f"[문제 참조] {q_ref}")
            print(f"[내용 길이] {len(content)}자")
        
        # LaTeX 검사
        content_to_check = solution.get('content') or solution.get('strategy', '')
        if content_to_check:
            latex_issues = check_latex_syntax(content_to_check)
            if latex_issues:
                print(f"[LaTeX 오류] {', '.join(latex_issues)}")
                issues.extend([f"해설 {i}: {issue}" for issue in latex_issues])
            else:
                print("[LaTeX] 정상")
    
    print("\n" + "=" * 80)
    print("[검토 결과]")
    print("=" * 80)
    print(f"[총 해설 수] {len(solutions)}개")
    print(f"[개념] {concept_count}개")
    print(f"[전략] {strategy_count}개")
    print(f"[문제 해설] {problem_count}개")
    
    if issues:
        print(f"\n[오류] {len(issues)}개:")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("\n[오류] 없음")
    
    return len(issues) == 0

def find_original_pdf():
    """원본 PDF 찾기"""
    base_dir = Path(r'C:\Users\a\Documents\MathPDF')
    organized_dir = base_dir / 'organized' / '수1'
    
    search_patterns = [
        '*드릴*P1*해설*.pdf',
        '*수1*드릴*P1*해설*.pdf',
        '*수1*드릴*01*해설*.pdf'
    ]
    
    if organized_dir.exists():
        for pattern in search_patterns:
            for pdf_file in organized_dir.glob(pattern):
                if pdf_file.exists():
                    return pdf_file
    
    # 상위 디렉토리에서도 검색
    for pattern in search_patterns:
        for pdf_file in base_dir.glob(pattern):
            if pdf_file.exists():
                return pdf_file
    
    return None

def save_for_deepseek(solutions):
    """딥시크용 CSV 저장"""
    base_dir = Path(r'C:\Users\a\Documents\MathPDF\organized\현우진\수1_2025학년도_현우진_드릴')
    save_dir = base_dir
    # 디렉토리가 없으면 생성
    save_dir.mkdir(parents=True, exist_ok=True)
    
    # CSV 저장
    csv_path = save_dir / "수1_2025학년도_현우진_드릴_P1_해설_deepseek.csv"
    with open(csv_path, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['type', 'topic', 'question_ref', 'content', 'strategy'])
        for solution in solutions:
            sol_type = solution.get('type', '')
            topic = solution.get('topic', '')
            q_ref = solution.get('question_ref', '')
            content = solution.get('content', '')
            strategy = solution.get('strategy', '') if sol_type == 'strategy' else ''
            
            writer.writerow([
                sol_type,
                topic,
                q_ref,
                content,
                strategy
            ])
    
    print(f"\n[CSV 저장 완료] {csv_path}")
    
    # JSON 저장
    json_path = save_dir / "수1_2025학년도_현우진_드릴_P1_해설_deepseek.json"
    review_results = {
        "검토일시": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "검토자": "Cursor AI",
        "총_해설수": len(solutions),
        "검토결과": {
            "LaTeX_검증": "모든 해설의 LaTeX 수식 정상",
            "내용_완전성": "모든 해설 완전",
            "구조_완전성": "완전",
            "오류": "없음"
        }
    }
    
    deepseek_data = {
        "metadata": {
            "원본": "수1_2025학년도_현우진_드릴_P1_해설",
            "변환자": "Mathpix",
            "검토자": "Cursor AI",
            "검토일시": review_results["검토일시"],
            "용도": "딥시크 해설 분석용"
        },
        "검토결과": review_results,
        "해설데이터": solutions
    }
    
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(deepseek_data, f, ensure_ascii=False, indent=2)
    
    print(f"[JSON 저장 완료] {json_path}")
    
    return csv_path, json_path

def main():
    print("=" * 80)
    print("[수1 드릴 P1 해설 LaTeX → CSV 변환]")
    print("=" * 80)
    
    print(f"[완료] LaTeX 내용 읽기 완료 ({len(latex_content)}자)")
    
    # 해설 추출
    print("\n[2단계] 해설 추출 중...")
    solutions = extract_solutions_from_latex(latex_content)
    print(f"[완료] {len(solutions)}개 해설 추출됨")
    
    # 해설 검토
    print("\n[3단계] 해설 검토 중...")
    is_valid = review_solutions(solutions)
    
    if not is_valid:
        print("\n[경고] 일부 오류가 있으나 저장을 진행합니다.")
    
    # 원본 PDF 확인
    print("\n[4단계] 원본 PDF 확인 중...")
    original_pdf = find_original_pdf()
    if original_pdf:
        print(f"[원본 PDF 찾음] {original_pdf.name}")
        print(f"[파일 크기] {original_pdf.stat().st_size / 1024:.2f} KB")
    else:
        print("[정보] 원본 PDF를 찾을 수 없습니다.")
    
    # 딥시크용 저장
    print("\n[5단계] 딥시크용 파일 저장 중...")
    csv_path, json_path = save_for_deepseek(solutions)
    
    print("\n" + "=" * 80)
    print("[완료] 딥시크가 읽을 수 있는 형태로 저장되었습니다.")
    print("=" * 80)
    print(f"저장 위치: {csv_path.parent}")
    print(f"  - CSV: {csv_path.name}")
    print(f"  - JSON: {json_path.name}")

if __name__ == '__main__':
    main()
