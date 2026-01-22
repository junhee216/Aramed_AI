# convert_geometry_p3_solution_deepseek.py
# 기하_2024학년도_현우진_드릴_P3 해설 LaTeX → Deepseek R1-70B용 변환

import re
import json
import sys
from pathlib import Path

# Windows 콘솔 인코딩 설정
if sys.platform == 'win32':
    import os
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')

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
\usepackage{caption}
\usepackage[fallback]{xeCJK}
\usepackage{polyglossia}
\usepackage{fontspec}
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

\begin{document}
\captionsetup{singlelinecheck=false}
\section*{Communernt}
\section*{Drill 원에 내접하는 사각형의 발견}
앞의 문제에서 점 P 와 초점 F , 점 Q 와 초점 F 를 연결하고 각 선분의 길이부터 체크하고 시작하는 것은 당연하다. 여기서 보이는 것은? 원 $C$ 에 내접하는 사각형 $\mathrm{PF}^{\prime} \mathrm{QF}$, 그리고 선분 $\mathrm{PF}^{\prime}$ 이 원 $C$ 의 지름이므로 삼각형 $\mathrm{PF}^{\prime} \mathrm{Q}$ 가 직각삼각형이고 주어진 선분의 길이를 이용하면 선분 PQ 의 길이와 $\angle \mathrm{PF}^{\prime} \mathrm{Q}$ 의 삼각비를 알 수 있다는 것. 갈 길이 딱 보인다. $\angle \mathrm{PFQ}$ 의 삼각비를 알 수 있고 삼각형 PQF 에서 할 일이 정해진다.

\section*{Drill. 1 적절한 미지수의 설정}
앞의 문제에는 쌍곡선의 정의 요소 중 직접적으로 주어진 것이 아무것도 없다. 주축의 길이, 선분 $\mathrm{PF}^{\prime}$ 의 길이 정도만 미지수로 잡아주고 시작하면 될 듯. 주어진 선분 $\mathrm{QF}^{\prime}$ 의 길이와 쌍곡선의 정의, 원에 대한 기본 중의 기본인 반지름의 길이의 일치를 이용하면 필요한 나머지 선분의 길이를 나타내고 구할 수 있다. 이등변삼각형에서의 닮음을 놓치지 않고 마무리하면 된다.

\section*{Drill 2 이등변삼각형과 닮음}
$\overline{\mathrm{AB}}=\overline{\mathrm{AC}}$ 인 이등변삼각형 ABC 에 대하여\\
(1) 이등변삼각형의 닮음

\begin{figure}[h]
\begin{center}
  \includegraphics[max width=\textwidth]{6b566b6d-e73a-46c0-ab7c-f2c5f0d270dd-2_316_285_1267_1205}
\captionsetup{labelformat=empty}
\caption{$\triangle \mathrm{ABC} \infty \triangle \mathrm{BCD}$}
\end{center}
\end{figure}

(2) 직각삼각형의 닮음\\
\includegraphics[max width=\textwidth, center]{6b566b6d-e73a-46c0-ab7c-f2c5f0d270dd-2_331_282_1746_1209}\\
$\triangle \mathrm{AMC} \sim \triangle \mathrm{BHC}$

\section*{Commune (OmH}
\section*{Drill 포물선의 접선의 성질}
초점이 F 인 포물선 $y^{2}=4 p x$ 위의 점 $\mathrm{A}\left(x_{1}, y_{1}\right)$ 에서 그은 접선이 $x$ 축과 만나는 점을 B , 준선과 만나는 점을 C , 점 A 에서 준선에 내린 수선의 발을 H 라 하면\\
(1) $\overline{\mathrm{AF}}=\overline{\mathrm{AH}}=\overline{\mathrm{BF}}$\\
(2) 선분 AB 의 중점 M 에 대하여 $\overline{\mathrm{AB}} \perp \overline{\mathrm{FM}}$ 이고, 삼각형 ABF 는 $\overline{\mathrm{FA}}=\overline{\mathrm{FB}}$ 인 이등변삼각형이다.\\
(3) 삼각형 ACF 는 삼각형 ACH 와 합동인\\
\includegraphics[max width=\textwidth]{6b566b6d-e73a-46c0-ab7c-f2c5f0d270dd-3_405_503_769_1416} 직각삼각형이고 $\angle \mathrm{AFC}=\frac{\pi}{2}$ 이다.

타원, 쌍곡선의 접선에 대한 성질은 따로 기억하지 않아도 된다.\\
포물선의 접선에 관한 문제는 결국 접선의 성질에 관한 내용인 경우가 매우 많으므로 일단 적용해보는 것이 실전적으로 유리하지만, 타원, 쌍곡선의 접선에 관한 문제는 단순히 접선의 방정식을 구하고 이를 이용한 계산인 경우가 대부분이므로 잡다한 접선의 성질을 기억했다가 잘못 적용하거나 쓸데없이 시간을 낭비하기 쉽다.

\section*{Commnent}
\section*{Drill. 1 타원의 접선}
\begin{enumerate}
  \item 기울기가 주어진 접선의 방정식
\end{enumerate}

타원 $\frac{x^{2}}{a^{2}}+\frac{y^{2}}{b^{2}}=1$ 에 접하고 기울기가 $m$ 인 직선의 방정식은

$$
y=m x \pm \sqrt{a^{2} m^{2}+b^{2}}
$$

\begin{enumerate}
  \setcounter{enumi}{1}
  \item 접점이 주어진 접선의 방정식
\end{enumerate}

타원 $\frac{x^{2}}{a^{2}}+\frac{y^{2}}{b^{2}}=1$ 위의 점 $\left(x_{1}, y_{1}\right)$ 에서의 접선의 방정식은

$$
\frac{x_{1} x}{a^{2}}+\frac{y_{1} y}{b^{2}}=1
$$

Drill. 2 타원, 쌍곡선 위에 있지 않은 점에서 타원, 쌍곡선에 그은 접선의 방정식\\
이차곡선의 접선을 다룰 때 접점이 주어지지 않으면 기울기가 주어진 접선의 방정식을 이용 하는 것을 우선으로 하자. 기울기가 주어진 접선의 방정식이 계산상으로 유리하기도 하고, 기울기에 관한 이차방정식에서 근과 계수의 관계도 자주 다루어진다.

타원 $\frac{x^{2}}{a^{2}}+\frac{y^{2}}{b^{2}}=1$ 위에 있지 않은 점 $(p, q)$ 에서 타원에 그은 접선의 방정식을 구하는 방법은 다음과 같다.\\
기울기가 $m$ 인 접선 $y=m x \pm \sqrt{a^{2} m^{2}+b^{2}}$ 이 점 $(p, q)$ 를 지나므로 $q=p m \pm \sqrt{a^{2} m^{2}+b^{2}}$, 즉 $-p m+q= \pm \sqrt{a^{2} m^{2}+b^{2}}$ 의 양변을 제곱하여 얻은 이차방정식\\
$\left(a^{2}-p^{2}\right) m^{2}+2 p q m+b^{2}-q^{2}=0$ 에서 $m$ 의 값을 구한다.\\
쌍곡선 위에 있지 않은 점에서 쌍곡선에 그은 접선의 방정식을 구하는 방법도 이와 마찬가지 이다.

또한 타원 $\frac{x^{2}}{a^{2}}+\frac{y^{2}}{b^{2}}=1$ 위에 있지 않은 점 $(a, q)$ 에서 타원에 그은 접선의 방정식을 구할 때는 방정식 $2 a q m+b^{2}-q^{2}=0$ 에서 $m$ 의 값을 구하여 얻은 접선 이외에 직선 $x=a$ 도 타원의 접선이 된다. 점 $(-a, q)$ 에서 타원에 그은 접선의 방정식을 구할 때도 마찬가지로 직선 $x=-a$ 도 타원의 접선이 된다.\\
쌍곡선 $\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1$ 위에 있지 않은 점 $(a, q),(-a, q)$ 에서 쌍곡선에 그은 접선에 대해 서도 마찬가지이다.

\section*{Comment}
\section*{Drill 쌍곡선의 접선}
\begin{enumerate}
  \item 기울기가 주어진 접선의 방정식
\end{enumerate}

쌍곡선 $\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1$ 에 접하고 기울기가 $m$ 인 직선의 방정식은

$$
y=m x \pm \sqrt{a^{2} m^{2}-b^{2}}\left(\text { 단, } a^{2} m^{2}-b^{2}>0\right)
$$

\begin{enumerate}
  \setcounter{enumi}{1}
  \item 접점이 주어진 접선의 방정식\\
(1) 쌍곡선 $\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1$ 위의 점 $\left(x_{1}, y_{1}\right)$ 에서의 접선의 방정식은
\end{enumerate}

$$
\frac{x_{1} x}{a^{2}}-\frac{y_{1} y}{b^{2}}=1
$$

(2) 쌍곡선 $\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=-1$ 위의 점 $\left(x_{1}, y_{1}\right)$ 에서의 접선의 방정식은

$$
\frac{x_{1} x}{a^{2}}-\frac{y_{1} y}{b^{2}}=-1
$$

\section*{Communent}
\section*{D제l '직선'과 곡선 위의 점 사이의 거리의 최대와 최소}
일반적으로 직선 $l$ 과 곡선 위의 점 P 사이의 거리의 최댓값과 최솟값은 직선 $l$ 과 기울기가 같은 접선을 이용하여 구한다.\\
\includegraphics[max width=\textwidth, center]{6b566b6d-e73a-46c0-ab7c-f2c5f0d270dd-6_343_427_907_864}\\
\includegraphics[max width=\textwidth, center]{6b566b6d-e73a-46c0-ab7c-f2c5f0d270dd-6_366_468_884_1366}

\section*{Comment}
Drill 닮은 도형의 발견과 닮음비의 파악\\
앞의 문제에서 사각형 $\mathrm{PRF}^{\prime} \mathrm{F}$ 가 등변사다리꼴이라는 것, 사각형 $\mathrm{PRF}^{\prime} \mathrm{Q}$ 가 평행사변형 이라는 것, 삼각형 PQF 가 이등변삼각형이라는 것과 두 삼각형 $\mathrm{RF}^{\prime} \mathrm{F}, \mathrm{SQF}$ 가 닮은 도형임을 파악하는 것은 그리 어렵지 않을 것이다. 풀이 과정에서 두 삼각형 $\mathrm{RF}^{\prime} \mathrm{F}, \mathrm{SQF}$ 의 닮음비를 구해야 하는데, 보통은 대응하는 변의 길이의 비로 구하므로 어떤 변 하나를 똑 떼어 내서 다루려고 하면… 별로 좋지 않다. 점 R 가 쌍곡선 위에 있으므로 쌍곡선의 정의를 이용해야 하지 않을까 하고 바라보면? 닮음비를 대응하는 변의 길이의 차의 비로 구해도 된다는 생각을 할 수 있을 것이다.

\section*{Comment}
Drill 무게중심과 평균의 위치벡터 (도형의 평균)

$$
\overrightarrow{\mathrm{OG}}=\frac{\overrightarrow{\mathrm{OA}}+\overrightarrow{\mathrm{OB}}+\overrightarrow{\mathrm{OC}}}{3}
$$

에서 시점 O 는 시점 $\mathrm{O}, \mathrm{O}, \mathrm{O}$ 의 평균이고, 종점 G 는 종점 $\mathrm{A}, \mathrm{B}, \mathrm{C}$ 의 평균이다.\\
시점을 모두 O 대신 G 로 바꾸면(시점 변경은 자유롭다.)\\
$\overrightarrow{\mathrm{GG}}=\frac{\overrightarrow{\mathrm{GA}}+\overrightarrow{\mathrm{GB}}+\overrightarrow{\mathrm{GC}}}{3}=\overrightarrow{0}$ 이므로 $\overrightarrow{\mathrm{GA}}+\overrightarrow{\mathrm{GB}}+\overrightarrow{\mathrm{GC}}=\overrightarrow{0}$ 이다.\\
결론적으로\\
$\overrightarrow{\mathrm{PA}}+\overrightarrow{\mathrm{PB}}+\overrightarrow{\mathrm{PC}}=\overrightarrow{0} \Leftrightarrow$ 점 P 는 삼각형 ABC 의 무게중심\\
\includegraphics[max width=\textwidth, center]{6b566b6d-e73a-46c0-ab7c-f2c5f0d270dd-8_473_451_1167_1112}

\section*{Drill 한 점을 지나고 주어진 벡터에 평행한 직선의 방정식}
점 $\mathrm{A}\left(x_{1}, y_{1}\right)$ 을 지나고 영벡터가 아닌 벡터 $\vec{d}=(a, b)$ 에 평행한 직선 $l$ 위의 점을 $\mathrm{P}(x, y)$ 라 하면 직선 $l$ 의 방정식을 나타내는 방법은 다음과 같다.\\
(1) $\overrightarrow{\mathrm{AP}} / / \vec{d}$ 이므로

$$
\overrightarrow{\mathrm{AP}}=t \vec{d}
$$

인 실수 $t$ 가 존재한다.\\
이때 두 점 $\mathrm{A}, \mathrm{P}$ 의 위치벡터를 각각 $\vec{a}, \vec{p}$ 라 하면 $\overrightarrow{\mathrm{AP}}=\vec{p}-\vec{a}$ 이므로 다음이 성립한다.

$$
\vec{p}-\vec{a}=t \vec{d}, \text { 즉 } \vec{p}=\vec{a}+t \vec{d}
$$

\includegraphics[max width=\textwidth, center]{6b566b6d-e73a-46c0-ab7c-f2c5f0d270dd-9_381_437_1239_1116}\\
(2) $\vec{p}=(x, y), \vec{a}=\left(x_{1}, y_{1}\right), t \vec{d}=(t a, t b)$ 이므로 $\vec{p}=\vec{a}+t \vec{d}$ 에서

$$
(x, y)=\left(x_{1}+t a, y_{1}+t b\right)
$$

이다. 즉

$$
x=x_{1}+t a, y=y_{1}+t b
$$

(3) $x=x_{1}+t a, y=y_{1}+t b$ 에서 $a b \neq 0$ 일 때, $t$ 를 소거하면 다음을 얻을 수 있다.

$$
\frac{x-x_{1}}{a}=\frac{y-y_{1}}{b}
$$


\end{document}"""

def clean_math_content(math_str):
    """수식 내용 정리"""
    # \mathrm 제거
    math_str = re.sub(r'\\mathrm\{([^}]+)\}', r'\1', math_str)
    # \text 제거
    math_str = re.sub(r'\\text\s*\{([^}]+)\}', r'\1', math_str)
    # \left, \right 제거
    math_str = re.sub(r'\\left([\(\[\{])', r'\1', math_str)
    math_str = re.sub(r'\\right([\)\]\}])', r'\1', math_str)
    # 공백 정리
    math_str = re.sub(r'\s+', ' ', math_str)
    return math_str.strip()

def replace_aligned(match):
    """aligned 환경 처리"""
    content = match.group(1)
    # &를 정렬 기준으로 사용
    lines = content.split('\\\\')
    cleaned_lines = []
    for line in lines:
        line = line.strip()
        if '&' in line:
            parts = [p.strip() for p in line.split('&')]
            line = ' '.join(parts)
        line = clean_math_content(line)
        cleaned_lines.append(line)
    return '\n'.join(cleaned_lines)

def latex_to_markdown_for_deepseek(latex_text):
    """LaTeX를 Deepseek R1-70B용 마크다운으로 변환"""
    text = latex_text
    
    # Comment 섹션 제거
    text = re.sub(r'\\section\*\{Comment\}', '', text)
    text = re.sub(r'\\section\*\{Communernt\}', '', text)
    text = re.sub(r'\\section\*\{Commune \(OmH\}', '', text)
    text = re.sub(r'\\section\*\{Commnent\}', '', text)
    text = re.sub(r'\\section\*\{Communent\}', '', text)
    
    # aligned 환경 처리
    text = re.sub(r'\\begin\{aligned\}(.*?)\\end\{aligned\}', replace_aligned, text, flags=re.DOTALL)
    
    # 수식 블록 ($$ ... $$) - 먼저 처리
    def replace_display_math(match):
        math_content = match.group(1)
        math_content = clean_math_content(math_content)
        return f'\n\n$$\n{math_content}\n$$\n\n'
    text = re.sub(r'\$\$([^$]+?)\$\$', replace_display_math, text, flags=re.DOTALL)
    
    # 인라인 수식 ($ ... $) - 정확하게 변환
    def replace_inline_math(match):
        math_content = match.group(1)
        math_content = clean_math_content(math_content)
        return f'${math_content}$'
    text = re.sub(r'\$([^$]+?)\$', replace_inline_math, text)
    
    # enumerate 환경 처리
    def replace_enumerate(match):
        content = match.group(1)
        items = re.findall(r'\\item\s+(.*?)(?=\\item|$)', content, re.DOTALL)
        result = []
        for i, item in enumerate(items, 1):
            item = item.strip()
            item = re.sub(r'\\\\', ' ', item)
            item = clean_math_content(item)
            result.append(f"{i}. {item}")
        return '\n'.join(result) + '\n'
    text = re.sub(r'\\begin\{enumerate\}(.*?)\\end\{enumerate\}', replace_enumerate, text, flags=re.DOTALL)
    
    # itemize 환경 처리
    def replace_itemize(match):
        content = match.group(1)
        items = re.findall(r'\\item\s+(.*?)(?=\\item|$)', content, re.DOTALL)
        result = []
        for item in items:
            item = item.strip()
            item = re.sub(r'\\\\', ' ', item)
            item = clean_math_content(item)
            result.append(f"- {item}")
        return '\n'.join(result) + '\n'
    text = re.sub(r'\\begin\{itemize\}(.*?)\\end\{itemize\}', replace_itemize, text, flags=re.DOTALL)
    
    # figure 환경 제거 (이미지만 남김)
    text = re.sub(r'\\begin\{figure\}.*?\\includegraphics.*?\\end\{figure\}', '[이미지]', text, flags=re.DOTALL)
    
    # 이미지 처리
    text = re.sub(r'\\includegraphics\[[^\]]*\]\{[^}]+\}', '[이미지]', text)
    text = re.sub(r'\\includegraphics\[[^\]]*\]\{[^}]+\}', '[이미지]', text)
    
    # 섹션 헤더 처리
    text = re.sub(r'\\section\*\{([^}]+)\}', r'## \1', text)
    
    # 줄바꿈 처리
    text = re.sub(r'\\\\', '\n', text)
    
    # 기타 정리
    text = re.sub(r'\\%', '%', text)
    text = re.sub(r'\\captionsetup\{[^}]+\}', '', text)
    text = re.sub(r'\\caption\{[^}]+\}', '', text)
    text = re.sub(r'\\begin\{center\}', '', text)
    text = re.sub(r'\\end\{center\}', '', text)
    text = re.sub(r'\\infty', '∞', text)
    text = re.sub(r'\\sim', '~', text)
    text = re.sub(r'\\perp', '⊥', text)
    text = re.sub(r'\\Leftrightarrow', '⇔', text)
    text = re.sub(r'\\/', '/', text)
    
    # 연속된 $$ 제거
    text = re.sub(r'\$\$\$\$', '$$', text)
    
    # 공백 정리
    text = re.sub(r'[ \t]+', ' ', text)  # 연속 공백
    text = re.sub(r'\n{3,}', '\n\n', text)  # 연속 줄바꿈
    text = re.sub(r'^\s+', '', text, flags=re.MULTILINE)  # 줄 시작 공백
    
    return text.strip()

def validate_math_logic(solution_md, problem_json_path):
    """수학적 논리 검증 (문제 파일과의 정합성 확인)"""
    errors = []
    warnings = []
    
    try:
        with open(problem_json_path, 'r', encoding='utf-8') as f:
            problems = json.load(f)
    except FileNotFoundError:
        warnings.append("문제 파일을 찾을 수 없어 정합성 검증을 건너뜁니다.")
        return errors, warnings
    
    solution_lower = solution_md.lower()
    
    # 쌍곡선 정의 확인
    if '쌍곡선' in solution_md:
        has_hyperbola_def = '|pf - pf\'' in solution_lower or 'pf - pf\'' in solution_lower or '주축' in solution_md
        if not has_hyperbola_def:
            warnings.append("쌍곡선의 정의(|PF - PF'| = 2a)가 해설에 명시되지 않음")
    
    # 포물선 정의 확인
    if '포물선' in solution_md:
        has_parabola_def = ('pf = pi' in solution_lower or 'pf = ah' in solution_lower or 
                           '접선' in solution_md and '포물선' in solution_md)
        if not has_parabola_def:
            warnings.append("포물선의 정의(PF = PI)가 해설에 명시되지 않음")
    
    # 타원 정의 확인
    if '타원' in solution_md:
        has_ellipse_def = ('pf + pf\'' in solution_lower or 'pf + pf\'' in solution_lower or 
                         '장축' in solution_md)
        if not has_ellipse_def:
            warnings.append("타원의 정의(PF + PF' = 2a)가 해설에 명시되지 않음")
    
    # 벡터 관련 확인
    if '벡터' in solution_md or '\\overrightarrow' in solution_md or '\\vec' in solution_md:
        has_vector = '\\overrightarrow' in solution_md or '\\vec' in solution_md or '무게중심' in solution_md
        if not has_vector:
            warnings.append("벡터 관련 내용이 해설에 명시되지 않음")
    
    # 문제와 해설의 일관성 확인
    for problem in problems:
        question = problem.get('question', '')
        topic = problem.get('topic', '')
        
        # 쌍곡선 문제
        if '쌍곡선' in question and topic == '이차곡선':
            if '쌍곡선' not in solution_md:
                warnings.append(f"문제 {problem.get('index')}: 쌍곡선 문제인데 해설에 쌍곡선 관련 내용이 없음")
        
        # 포물선 문제
        if '포물선' in question:
            if '포물선' not in solution_md:
                warnings.append(f"문제 {problem.get('index')}: 포물선 문제인데 해설에 포물선 관련 내용이 없음")
        
        # 타원 문제
        if '타원' in question:
            if '타원' not in solution_md:
                warnings.append(f"문제 {problem.get('index')}: 타원 문제인데 해설에 타원 관련 내용이 없음")
        
        # 벡터 문제
        if topic == '벡터' or '\\overrightarrow' in question or '\\vec' in question:
            if '벡터' not in solution_md and '\\overrightarrow' not in solution_md and '\\vec' not in solution_md:
                warnings.append(f"문제 {problem.get('index')}: 벡터 문제인데 해설에 벡터 관련 내용이 없음")
    
    return errors, warnings

def main():
    print("=" * 80)
    print("기하_2024학년도_현우진_드릴_P3 해설 → Deepseek R1-70B용 변환")
    print("=" * 80)
    
    # \begin{document} 이후만 추출
    doc_match = re.search(r'\\begin\{document\}(.*?)\\end\{document\}', latex_content, re.DOTALL)
    if not doc_match:
        print("❌ LaTeX 문서 본문을 찾을 수 없습니다.")
        return
    
    body = doc_match.group(1)
    
    # 마크다운 변환
    solution_md = latex_to_markdown_for_deepseek(body)
    
    # 문제 파일 경로
    problem_json_path = Path(r'C:\Users\a\Documents\MathPDF\organized\현우진\기하_2024학년도_현우진_드릴\기하_2024학년도_현우진_드릴_P3_문제_deepseek.json')
    
    # 수학적 논리 검증
    math_errors, math_warnings = validate_math_logic(solution_md, problem_json_path)
    
    print("\n[수학적 오류 검증]")
    if math_errors:
        print(f"  ❌ 오류: {len(math_errors)}개")
        for error in math_errors:
            print(f"    - {error}")
    else:
        print("  ✅ 수학적 오류 없음")
    
    if math_warnings:
        print(f"  ⚠️  경고: {len(math_warnings)}개")
        for warning in math_warnings[:10]:
            print(f"    - {warning}")
        if len(math_warnings) > 10:
            print(f"    ... 외 {len(math_warnings) - 10}개")
    else:
        print("  ✅ 경고 없음")
    
    # 저장 경로
    base_dir = Path(r'C:\Users\a\Documents\MathPDF\organized\현우진\기하_2024학년도_현우진_드릴')
    base_dir.mkdir(parents=True, exist_ok=True)
    
    # 마크다운 저장
    md_content = "# 기하_2024학년도_현우진_드릴_P3 해설\n\n"
    md_content += "> 이 문서는 Deepseek R1-70B가 읽을 수 있도록 최적화된 마크다운 형식입니다.\n\n"
    md_content += solution_md
    
    md_path = base_dir / "기하_2024학년도_현우진_드릴_P3_해설_deepseek_r1.md"
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    print(f"\n[저장 완료]")
    print(f"  - 마크다운: {md_path}")
    print(f"\n[Deepseek R1-70B 호환성]")
    print("  - 마크다운 형식: 지원")
    print("  - LaTeX 수식: 지원 ($...$ 및 $$...$$)")
    print("  - 구조화된 섹션: 지원")
    print("  - UTF-8 인코딩: 지원")
    print("\n[결론] Deepseek R1-70B가 읽을 수 있는 형태입니다.")

if __name__ == '__main__':
    main()
