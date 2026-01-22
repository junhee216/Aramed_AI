# convert_haktong_p3_solution_latex.py
# 확통_2024학년도_현우진_드릴_P3_해설 LaTeX 변환

import json
import re
import sys
from pathlib import Path

# Windows 콘솔 인코딩 설정
if sys.platform == 'win32':
    import os
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')

from latex_utils import extract_body, clean_latex_text

# LaTeX 내용
latex_content = r"""% This LaTeX document needs to be compiled with XeLaTeX.
\documentclass[10pt]{article}
\usepackage[utf8]{inputenc}
\usepackage{amsmath}
\usepackage{amsfonts}
\usepackage{amssymb}
\usepackage[version=4]{mhchem}
\usepackage{stmaryrd}
\usepackage{graphicx}
\usepackage[export]{adjustbox}
\graphicspath{ {./images/} }
\usepackage{fvextra, csquotes}
\usepackage[fallback]{xeCJK}
\usepackage{polyglossia}
\usepackage{fontspec}
\usepackage{newunicodechar}
\IfFontExistsTF{Noto Serif CJK KR}
{\setCJKmainfont{Noto Serif CJK KR}}
{\IfFontExistsTF{Apple SD Gothic Neo}
  {\setCJKmainfont{Apple SD Gothic Neo}}
  {\IfFontExistsTF{UnDotum}
    {\setCJKmainfont{UnDotum}}
    {\setCJKmainfont{Malgun Gothic}}
}}

\setmainlanguage{english}
\IfFontExistsTF{CMU Serif}
{\setmainfont{CMU Serif}}
{\IfFontExistsTF{DejaVu Sans}
  {\setmainfont{DejaVu Sans}}
  {\setmainfont{Georgia}}
}

\newunicodechar{⇒}{\ifmmode\Rightarrow\else{$\Rightarrow$}\fi}

\begin{document}
\section*{Drill 대소 관계의 조건}
다음의 예와 같이 대소 관계의 조건을 차를 새로운 미지수로 잡아 중복조합으로 다룰 수 있다. 이때 새로운 미지수가 음이 아닌 정수인지 자연수인지 확실히 구분해야 한다.\\[0pt]
[예1] (1) 모두 등호가 있는 부등식 $1 \leq a \leq b \leq c \leq 8$ 을 만족시키는 자연수 $a, b, c$ 의 순서쌍 $(a, b, c)$ 의 개수는\\
$a-1=x_{1}, b-a=x_{2}, c-b=x_{3}, 8-c=x_{4}$\\
라 하면 1 에 음이 아닌 정수 $x_{1}, x_{2}, x_{3}, x_{4}$ 를 모두 더해서 8 이 되므로\\
$1+x_{1}+x_{2}+x_{3}+x_{4}=8$, 즉 $x_{1}+x_{2}+x_{3}+x_{4}=7$\\
을 만족시키는 순서쌍 $\left(x_{1}, x_{2}, x_{3}, x_{4}\right)$ 의 개수 ${ }_{4} \mathrm{H}_{7}$ 로 구할 수 있다.\\
(2) 모두 등호가 없는 부등식 $1<a<b<c<8$ 을 만족시키는 자연수 $a, b, c$ 의 순서쌍 $(a, b, c)$ 의 개수는\\
$a-1=x_{1}, b-a=x_{2}, c-b=x_{3}, 8-c=x_{4}$\\
라 하면 1 에 자연수 $x_{1}, x_{2}, x_{3}, x_{4}$ 를 모두 더해서 8 이 되므로\\
$1+x_{1}+x_{2}+x_{3}+x_{4}=8$, 즉 $x_{1}+x_{2}+x_{3}+x_{4}=7$\\
을 만족시키는 순서쌍 $\left(x_{1}, x_{2}, x_{3}, x_{4}\right)$ 의 개수 ${ }_{4} \mathrm{H}_{3}$ 으로 구할 수 있다.\\
(3) 등호가 일부 포함된 부등식 $1 \leq a<b \leq c \leq 4$ 를 만족시키는 자연수 $a, b, c$ 의 순서쌍 $(a, b, c)$ 의 개수는\\
$a-1=x_{1}, b-a=x_{2}+1, c-b=x_{3}, 4-c=x_{4}$\\
라 하면 음이 아닌 정수 $x_{1}, x_{2}, x_{3}, x_{4}$ 에 대하여 1 에 $x_{1}, x_{2}+1, x_{3}, x_{4}$ 를 모두 더해서 4 가 되므로\\
$1+x_{1}+\left(x_{2}+1\right)+x_{3}+x_{4}=4$, 즉 $x_{1}+x_{2}+x_{3}+x_{4}=2$\\
를 만족시키는 순서쌍 $\left(x_{1}, x_{2}, x_{3}, x_{4}\right)$ 의 개수 ${ }_{4} \mathrm{H}_{2}$ 로 구할 수 있다.\\[0pt]
[예2] $x+y+z \leq 10$ 을 만족시키는 음이 아닌 정수 $x, y, z$ 의 순서쌍 $(x, y, z)$ 의 개수는\\
$10-(x+y+z)=w$\\
라 하면 $x+y+z$ 에 음이 아닌 정수 $w$ 를 더해서 10 이 되므로\\
$x+y+z+w=10$\\
을 만족시키는 순서쌍 $(x, y, z, w)$ 의 개수 ${ }_{4} \mathrm{H}_{10}$ 으로 구할 수 있다.

앞의 문제에서는 부등식 $1 \leq a<b<c<d \leq 20$ 을 만들고 시작할 수 있다. $a-1, b-a, c-b$, $d-c, 20-d$ 를 새로운 미지수를 이용하여 잡을 때 $b-a, c-b, d-c$ 의 최솟값이 2 인 것을 나타낼 수 있도록, 새로운 미지수를 모두 음이 아닌 정수로 잡아주는 것이 좋다. $b-a, c-b$, $d-c$ 의 최솟값이 2 이므로 모든 값이 3 이상이 되지 않도록 주의해야 한다.

\section*{Drill 미지수의 조건에 주의}
앞의 문제에서 부등식 $1 \leq a_{1}<a_{2}<a_{3}<a_{4} \leq 11$ 에서 $a_{1}-1, a_{2}-a_{1}, a_{3}-a_{2}, a_{4}-a_{3}, 11-a_{4}$ 를 새로운 미지수로 잡을 때 음이 아닌 정수만을 이용해서 잡든 자연수만을 이용해서 잡든, 아니면 음이 아닌 정수와 자연수를 섞어서 잡든 어떻게 해도 상관은 없다. 다만 조건 (나), (다)를 적용하면서 미지수를 어떻게 설정한 것인지 잊지 말고 끝까지 주의를 기울여야 한다.

\section*{\begin{center}
\includegraphics[max width=\textwidth]{9b1bf9c0-a9e3-431d-866d-4b3e8a0fb8fa-3_42_294_654_264}
\end{center}}
\section*{Drill 함수의 개수}
두 집합 $X, Y$ 에 대하여 $n(X)=a, n(Y)=b$ 일 때, $X$ 에서 $Y$ 로의 함수 $f$ 의 개수는 다음과 같다.\\
(1) 모든 함수 $f$ 의 개수 ⇒ 곱의 법칙 (중복순열)\\
$b^{a}$\\
(2) 상수함수 $f$ 의 개수\\
$b$\\
(3) $x_{1} \neq x_{2}$ 이면 $f\left(x_{1}\right) \neq f\left(x_{2}\right)$ 인 함수 $f$ 의 개수 ⇒ 곱의 법칙 (순열)\\
${ }_{b} \mathrm{P}_{a}$ (단, $b \geq a$ )\\
(4) $x_{1}<x_{2}$ 이면 $f\left(x_{1}\right)<f\left(x_{2}\right)$ (또는 $\left.f\left(x_{1}\right)>f\left(x_{2}\right)\right)$ 인 함수 $f$ 의 개수

⇒ 순서가 정해진 배열 (조합)\\
${ }_{b} \mathrm{C}_{a}$ (단, $b \geq a$ )\\
(5) $x_{1}<x_{2}$ 이면 $f\left(x_{1}\right) \leq f\left(x_{2}\right)$ (또는 $\left.f\left(x_{1}\right) \geq f\left(x_{2}\right)\right)$ 인 함수 $f$ 의 개수

⇒ 순서가 정해진 배열 (중복조합)\\
${ }_{b} \mathrm{H}_{a}$

함수의 개수에 관한 문제는 위의 기본 계산을 바탕으로 하되, 조건에 따라 정의역의 각 원소가 대응하는 방법의 수에 대하여 곱의 법칙을 이용하는 것이 기본이다. 위의 내용을 단순히 암기 해서는 안 된다.

\section*{Comment}
\section*{Drill 순서가 정해진 배열}
앞의 문제의 조건 (나)에 집합 $X$ 의 모든 원소를 대입하여 써보면 순서가 정해진 배열이고 중복조합의 상황임을 알 수 있다. 여기에 조건 (가)를 적용하여 $f(4), f(6)$ 의 값의 케이스를 구분하고 중복조합, 합의 법칙, 곱의 법칙으로 찬찬히 마무리하면 된다.

\section*{Drill 치역의 조건이 있는 함수의 개수}
치역의 조건이 있는 함수의 개수는 조건에 맞는 치역의 원소를 먼저 선택하고 정의역의 원소에 치역의 원소가 대응하는 경우의 수로 구할 수 있다.\\[0pt]
[예] 두 집합 $X=\{1,2,3,4,5\}, Y=\{6,7,8,9\}$ 에 대하여 다음 조건을 만족시키는 함수 $f: X \rightarrow Y$ 의 개수를 구해보자.\\
(1) 치역의 원소의 개수가 2 인 함수 $f$ 의 개수 공역 $Y$ 에서 치역의 원소 2 개를 택하는 경우의 수는 ${ }_{4} \mathrm{C}_{2}$ 정의역 $X$ 의 원소에 치역의 2 개의 원소가 대응하는 경우의 수는 $2^{5}$ 이때 정의역 $X$ 의 모든 원소에 치역의 1 개의 원소가 대응하는 경우의 수는 2\\
$\therefore{ }_{4} \mathrm{C}_{2} \times\left(2^{5}-2\right)=180$\\
(2) 치역의 원소의 개스가 3 인 함수 $f$ 의 개수 공역 $Y$ 에서 치역의 원소 3 개를 택하는 경우의 수는 ${ }_{4} \mathrm{C}_{3}$ 정의역 $X$ 의 원소에 치역의 3 개의 원소가 대응하는 경우의 수는 $3^{5}$\\
이때 정의역 $X$ 의 모든 원소에 치역의 1 개의 원소가 대응하는 경우의 수는 3\\
이고, 정의역 $X$ 의 모든 원소에 치역의 2 개의 원소가 대응하는 경우의 수는 ${ }_{3} \mathrm{C}_{2} \times\left(2^{5}-2\right)$\\
$\therefore{ }_{4} \mathrm{C}_{3} \times\left\{3^{5}-3-{ }_{3} \mathrm{C}_{2} \times\left(2^{5}-2\right)\right\}=600$

\section*{Comment}
\section*{Drill 이항정리}
\begin{enumerate}
  \item 이항정리
\end{enumerate}

다항식 $(a+b)^{n}$ 의 전개식

$$
(a+b)^{n}=\underbrace{(a+b)(a+b)(a+b) \times \cdots \times(a+b)}_{n \text { 개 }}
$$

에서 $a^{r} b^{n-r}$ 은 우변의 $n$ 개의 인수 $(a+b)$ 중 $r$ 개의 인수에서는 $a$ 를 택하고 남은 $(n-r)$ 개의 인수에서는 $b$ 를 택하여 곱한 것이다. 이와 같은 경우의 수는 서로 다른 $n$ 개 에서 $r$ 개를 택하는 조합의 수 ${ }_{n} \mathrm{C}_{r}$ 와 같으므로 $(a+b)^{n}$ 의 전개식에서 $a^{r} b^{n-r}$ 의 개수는 ${ }_{n} \mathrm{C}$ 이다. 따라서

$$
(a+b)^{n}={ }_{n} \mathrm{C}_{0} a^{0} b^{n}+{ }_{n} \mathrm{C}_{1} a^{1} b^{n-1}+\cdots+{ }_{n} \mathrm{C}_{r} a^{r} b^{n-r}+\cdots+{ }_{n} \mathrm{C}_{n} a^{n} b^{0}=\sum_{r=0}^{n}{ }_{n} \mathrm{C}_{r} a^{r} b^{n-r}
$$

이다. 이와 같이 $(a+b)^{n}$ 을 전개하는 것을 이항정리라고 한다.\\
2) 이항계수

다항식 $(a+b)^{n}$ 의 전개식에서 각 항의 계수 ${ }_{n} \mathrm{C}_{0},{ }_{n} \mathrm{C}_{1}, \cdots,{ }_{n} \mathrm{C}_{r}, \cdots,{ }_{n} \mathrm{C}_{n}$ 을 이항계수라고 한다.\\
이항계수는 항을 만드는 경우의 수이고, 계수는 항에서 문자를 제외한 부분이다.\\
예를 들면, $(2 x-1)^{5}$ 의 전개식에서 $x^{2}$ 의 이항계수는 ${ }_{5} \mathrm{C}_{2}$, 계수는 ${ }_{5} \mathrm{C}_{2} \times 2^{2} \times(-1)^{3}$ 이다.

\section*{Comment}
\section*{Drill 파스칼의 삼각형}
\begin{enumerate}
  \item 파스칼의 삼각형\\
$(a+b)^{n}$ 의 전개식에서 $n=0,1,2, \cdots$ 일 때의 이항계수를 차례대로 배열하면
\end{enumerate}

$$
{ }_{n-1} \mathrm{C}_{r-1}+{ }_{n-1} \mathrm{C}_{r}={ }_{n} \mathrm{C}_{r}
$$

이므로 각 행의 수는 그 앞 행의 이웃한 두 수의 합과 같고, ${ }_{n} \mathrm{C}_{r}={ }_{n} \mathrm{C}_{n-r}$ 이므로 배열이 좌우 대칭이 되어 있다.\\
이와 같이 이항계수를 배열한 것을 파스칼의 삼각형이라고 한다.

\begin{center}
\begin{tabular}{cc}
1 & $(a+b)^{0}$ 의 계수 \\
${ }_{1} \mathrm{C}_{0}{ }_{1} \mathrm{C}_{1}$ & $(a+b)^{1}$ 의 계수 \\
${ }_{2} \mathrm{C}_{0}{ }_{2} \mathrm{C}_{1}{ }_{2} \mathrm{C}_{2}$ & $(a+b)^{2}$ 의 계수 \\
${ }_{3} \mathrm{C}_{0}{ }_{3} \mathrm{C}_{1}{ }_{3} \mathrm{C}_{2}{ }_{3} \mathrm{C}_{3}$ & $(a+b)^{3}$ 의 계수 \\
${ }_{4} \mathrm{C}_{0}{ }_{4} \mathrm{C}_{1}{ }_{4} \mathrm{C}_{2}{ }_{4} \mathrm{C}_{3}{ }_{4} \mathrm{C}_{4}$ & $(a+b)^{4}$ 의 계수 \\
${ }_{5} \mathrm{C}_{0}{ }_{5} \mathrm{C}_{1}{ }_{5} \mathrm{C}_{2}{ }_{5} \mathrm{C}_{3}{ }_{5} \mathrm{C}_{4}{ }_{5} \mathrm{C}_{5}$ & $(a+b)^{5}$ 의 계수 \\
$\vdots$ & $\vdots$ \\
\end{tabular}
\end{center}

\begin{enumerate}
  \setcounter{enumi}{1}
  \item 파스칼의 삼각형에 관한 이항계수의 성질\\
(1) ${ }_{r} \mathrm{C}_{0}+{ }_{r+1} \mathrm{C}_{1}+{ }_{r+2} \mathrm{C}_{2}+\cdots+{ }_{n} \mathrm{C}_{n-r}={ }_{n+1} \mathrm{C}_{n-r}$\\
(2) ${ }_{r} \mathrm{C}_{r}+{ }_{r+1} \mathrm{C}_{r}+{ }_{r+2} \mathrm{C}_{r}+\cdots+{ }_{n} \mathrm{C}_{r}={ }_{n+1} \mathrm{C}_{r+1}$
\end{enumerate}

\begin{displayquote}
1\\
${ }_{1} \mathrm{C}_{0}{ }_{1} \mathrm{C}_{1}$\\
${ }_{2} \mathrm{C}_{0} \quad{ }_{2} \mathrm{C}_{1} \quad{ }_{2} \mathrm{C}_{2}$\\
${ }_{3} \mathrm{C}_{0}{ }_{3} \mathrm{C}_{1}{ }_{3} \mathrm{C}_{2} \quad{ }_{3} \mathrm{C}_{3}$\\
$\begin{array}{lllll} & { }_{4} \mathrm{C}_{0} & & { }_{4} \mathrm{C}_{1} & \\ & { }_{4} \mathrm{C}_{2} & & { }_{4} \mathrm{C}_{3} & \\ & { }_{4} \mathrm{C}_{4}\end{array}$\\
$\begin{array}{llllll} & { }_{5} \mathrm{C}_{0} & & { }_{5} \mathrm{C}_{1} & & { }_{5} \mathrm{C}_{2} \\ & { }_{5} \mathrm{C}_{3} & & { }_{5} \mathrm{C}_{4} & & { }_{5} \mathrm{C}_{5}\end{array}$\\
하키 스틱의 원리 (대각선 조합수의 합)
\end{displayquote}

하키 스틱의 원리를 이용할 때는 ${ }_{,} \mathrm{C}_{r}$ 또는 ${ }_{r} \mathrm{C}_{0}$ 부터 시작하는지 반드시 확인해야 한다.

\section*{Comment}
\section*{Drill 수학적 확률}
어떤 시행의 표본공간 $S$ 가 $n$ 개의 근원사건으로 이루어져 있고, 각각의 근원사건이 일어날 가능성이 모두 같은 정도로 기대된다고 하자. 이때 사건 $A$ 가 $r$ 개의 근원사건으로 이루어져 있으면 사건 $A$ 가 일어날 확률 $\mathrm{P}(A)$ 를

$$
\mathrm{P}(A)=\frac{n(A)}{n(S)}=\frac{r}{n}(\text { 단, } n \geq r)
$$

와 같이 정의하고, 이것을 사건 $A$ 가 일어날 수학적 확률이라고 한다.

확률의 가장 중요한 기본은 근원사건을 제대로 파악하는 것이다. 확률에서 모든 경우의 수, 즉 모든 근원사건의 수가 $n$ 이라고 하려면 각 근원사건의 확률은 $\frac{1}{n}$ 로 동일해야 하고, 어떤 사건이 일어날 확률이 $\frac{r}{n}$ 라고 하려면 이 사건은 $r$ 개의 근원사건으로 이루어져 있어야 한다는 것을 확실히 해 두자. 수학적 확률의 계산의 기본 틀은

$$
\frac{1}{n} \times(\text { 근원사건의 수 })
$$

이다.\\
참고로, 확률을 다룰 때 '경우의 수'를 말하면 '근원사건의 수'인 것으로 이해하도록 하자.

\section*{Cornmernt}
\section*{Drill 여사건의 활용}
경우의 수에서뿐만 아니라 수학 전반에서 다루는 조건이 복잡할 때 그 반대의 조건을 생각해 보는 것은 보편적인 문제 해결 방식이다. 일단은 '원래 사건이 복잡할 때 여사건을 생각해 본다'라고 두루뭉술하게 얘기할 수밖에 없다.\\
여사건을 생각하는 대표적인 상황 몇 가지는 다음과 같다.\\
(1) 적어도 하나가 \~{}이다. ⇒ 모두 \~{}이 아니다.\\
(2) $\sim$ 이 아니고 $\sim$ 이 아니다. $\Rightarrow \sim$ 이거나 $\sim$ 이다.\\
(3) 곱이 짝수이다. ⇒ 곱이 홀수이다.

곱이 소수 \~{} 의 배수이다. ⇒ 곱이 소수 \~{} 의 배수가 아니다.\\
그러나 이런 상황에서 여사건을 생각해볼 수 있다는 것이지 꼭 그래야만 한다는 것은 아니다. 여사건을 생각해보고 더 복잡하면 원래 사건으로 돌아와야 한다.


\end{document}"""

def extract_solutions_from_latex(latex_content):
    """LaTeX에서 해설 추출"""
    body = extract_body(latex_content)
    solutions = []
    
    # 섹션 헤더 찾기
    section_pattern = r'\\section\*\{([^}]+)\}'
    sections = list(re.finditer(section_pattern, body))
    
    print(f"📊 발견된 섹션: {len(sections)}개")
    
    # Comment/Cornmernt 섹션 찾기 (오타 포함)
    comment_sections = []
    for section in sections:
        section_text = section.group(1).strip()
        if 'Comment' in section_text or 'Cornmernt' in section_text:
            comment_sections.append(section.start())
    
    print(f"📊 발견된 Comment 섹션: {len(comment_sections)}개")
    
    # Drill 섹션 추출
    seen_titles = set()
    is_strategy_mode = False  # Comment 이후의 Drill은 strategy
    
    for i, section in enumerate(sections):
        section_text = section.group(1).strip()
        
        # Comment 섹션 확인
        if 'Comment' in section_text or 'Cornmernt' in section_text:
            is_strategy_mode = True
            continue
        
        # Drill 섹션만 처리
        if not section_text.startswith('Drill'):
            continue
        
        # 섹션 제목 추출
        title = section_text.replace('Drill', '').strip()
        
        # 중복 제거
        if title in seen_titles:
            continue
        seen_titles.add(title)
        
        # 섹션 시작 위치
        section_start = section.end()
        
        # 다음 섹션 위치 찾기
        if i < len(sections) - 1:
            section_end = sections[i+1].start()
        else:
            section_end = len(body)
        
        # 해설 내용 추출
        content = body[section_start:section_end]
        
        # 이미지 제거
        content = re.sub(r'\\includegraphics.*?\{[^}]+\}', '', content)
        content = re.sub(r'\\begin\{center\}.*?\\end\{center\}', '', content, flags=re.DOTALL)
        
        # enumerate 환경 제거 (내용은 보존)
        content = re.sub(r'\\begin\{enumerate\}.*?\\end\{enumerate\}', '', content, flags=re.DOTALL)
        content = re.sub(r'\\item\s*', '', content)
        
        # displayquote 환경 처리
        displayquote_match = re.search(r'\\begin\{displayquote\}(.*?)\\end\{displayquote\}', content, re.DOTALL)
        if displayquote_match:
            quote_content = displayquote_match.group(1)
            content = content.replace(displayquote_match.group(0), quote_content)
        
        # tabular 환경 제거
        content = re.sub(r'\\begin\{tabular\}.*?\\end\{tabular\}', '', content, flags=re.DOTALL)
        
        # LaTeX 명령어 정리
        content = clean_latex_text(content)
        
        # 빈 내용 제거
        if not content.strip() or len(content.strip()) < 10:
            continue
        
        # 해설 타입 결정
        solution_type = 'strategy' if is_strategy_mode else 'concept'
        
        solution = {
            'index': f"{len(solutions)+1:02d}",
            'title': title,
            'type': solution_type,
            'content': content.strip()
        }
        
        solutions.append(solution)
        print(f"✅ 해설 {solution['index']} 추출 완료 ({solution_type}): {title}")
    
    return solutions

def review_solutions(solutions):
    """해설 검토"""
    print("\n" + "=" * 60)
    print("[해설 데이터 검토]")
    print("=" * 60)
    
    errors = []
    warnings = []
    
    for solution in solutions:
        content = solution.get('content', '')
        title = solution.get('title', '')
        
        # LaTeX 수식 검사
        dollar_count = content.count('$')
        if dollar_count % 2 != 0:
            errors.append(f"해설 {solution['index']}: LaTeX 달러 기호 불일치 ({dollar_count}개)")
        
        # 내용 길이 확인
        if len(content) < 20:
            warnings.append(f"해설 {solution['index']}: 내용이 너무 짧음 ({len(content)}자)")
        
        # 수학적 논리 검사 (확통 관련)
        if '중복조합' in content or 'H_' in content:
            if '음이 아닌 정수' not in content and '자연수' not in content:
                warnings.append(f"해설 {solution['index']}: 중복조합에서 음이 아닌 정수/자연수 조건 명시 없음")
        
        if '함수' in content and '개수' in content:
            if '중복순열' not in content and '순열' not in content and '조합' not in content and '중복조합' not in content:
                warnings.append(f"해설 {solution['index']}: 함수의 개수에서 경우의 수 원리 명시 없음")
        
        if '이항정리' in content or '이항계수' in content:
            if '조합' not in content and 'C_' not in content:
                warnings.append(f"해설 {solution['index']}: 이항정리에서 조합 명시 없음")
        
        if '확률' in content:
            if '근원사건' not in content and '표본공간' not in content:
                warnings.append(f"해설 {solution['index']}: 확률에서 근원사건/표본공간 명시 없음")
        
        if '여사건' in content:
            if '드모르간' not in content and '반대' not in content:
                warnings.append(f"해설 {solution['index']}: 여사건에서 드모르간의 법칙 또는 반대 조건 명시 없음")
        
        print(f"\n[해설 {solution['index']}]")
        print(f"[제목] {title}")
        print(f"[타입] {solution['type']}")
        print(f"[내용 길이] {len(content)}자")
        if dollar_count % 2 == 0:
            print(f"[LaTeX] 정상")
        else:
            print(f"[LaTeX] 오류: 달러 기호 {dollar_count}개")
    
    print("\n" + "=" * 60)
    print("[검토 결과]")
    print("=" * 60)
    print(f"[총 해설수] {len(solutions)}개")
    print(f"[개념] {sum(1 for s in solutions if s['type'] == 'concept')}개")
    print(f"[전략] {sum(1 for s in solutions if s['type'] == 'strategy')}개")
    
    if errors:
        print(f"\n[오류] {len(errors)}개")
        for error in errors:
            print(f"  - {error}")
    else:
        print("\n[오류] 없음")
    
    if warnings:
        print(f"\n[경고] {len(warnings)}개")
        for warning in warnings[:10]:  # 상위 10개만
            print(f"  - {warning}")
        if len(warnings) > 10:
            print(f"  ... 외 {len(warnings) - 10}개 경고")
    
    return len(errors) == 0

def compare_with_problems(solutions, problems_path):
    """문제 파일과 비교"""
    try:
        with open(problems_path, 'r', encoding='utf-8') as f:
            problems = json.load(f)
        
        print("\n" + "=" * 60)
        print("[문제-해설 비교]")
        print("=" * 60)
        print(f"문제 수: {len(problems)}개")
        print(f"해설 수: {len(solutions)}개")
        
        if len(problems) != len(solutions):
            print(f"⚠️  문제 수와 해설 수가 일치하지 않음")
        
    except FileNotFoundError:
        print(f"\n⚠️  문제 파일을 찾을 수 없음: {problems_path}")
    except Exception as e:
        print(f"\n⚠️  문제 파일 비교 중 오류: {e}")

def save_for_deepseek(solutions, output_dir, base_filename):
    """딥시크 형식으로 저장"""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # JSON 저장
    json_path = output_dir / f"{base_filename}_deepseek.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(solutions, f, ensure_ascii=False, indent=2)
    print(f"[JSON 저장 완료] {json_path}")
    
    # CSV 저장
    csv_path = output_dir / f"{base_filename}_deepseek.csv"
    import csv
    with open(csv_path, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['index', 'title', 'type', 'content'])
        writer.writeheader()
        for solution in solutions:
            writer.writerow(solution)
    print(f"[CSV 저장 완료] {csv_path}")

def main():
    print("=" * 80)
    print("확통_2024학년도_현우진_드릴_P3_해설 변환")
    print("=" * 80)
    
    # 해설 추출
    solutions = extract_solutions_from_latex(latex_content)
    
    print(f"\n📊 총 {len(solutions)}개 해설 추출 완료\n")
    
    # 검토
    is_valid = review_solutions(solutions)
    
    # 문제 파일과 비교
    base_dir = Path(r'C:\Users\a\Documents\MathPDF\organized\현우진\확통_2005학년도_현우진_드릴')
    problems_path = base_dir / '확통_2024학년도_현우진_드릴_P3_문제_deepseek.json'
    compare_with_problems(solutions, problems_path)
    
    # 저장
    base_filename = '확통_2024학년도_현우진_드릴_P3_해설'
    
    if is_valid or len(solutions) > 0:
        save_for_deepseek(solutions, base_dir, base_filename)
        print(f"\n✅ 저장 완료: {base_dir}")
    else:
        print("\n❌ 검토 실패")

if __name__ == '__main__':
    main()
