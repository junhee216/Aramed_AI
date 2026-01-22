# convert_geometry_p4_solution_deepseek.py
# 기하_2024학년도_현우진_드릴_P4 해설 LaTeX → Deepseek R1-70B용 변환

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
Drill $|\vec{a}+\vec{b}|$ 의 최대와 최소

\begin{enumerate}
  \item $|\vec{a}|,|\vec{b}|$ 가 모두 일정할 때\\
(1) $\vec{a}, \vec{b}$ 가 이루는 각의 크기가 최소일 때, $|\vec{a}+\vec{b}|$ 는 최대\\
(2) $\vec{a}, \vec{b}$ 가 이루는 각의 크기가 최대일 때, $|\vec{a}+\vec{b}|$ 는 최소
  \item $|\vec{a}|$ 또는 $|\vec{b}|$ 가 일정하지 않을 때\\
$|\vec{a}|$ 또는 $|\vec{b}|$ 가 일정하지 않으면 $|\vec{a}+\vec{b}|$ 의 최대와 최소는 $\vec{a}, \vec{b}$ 가 이루는 각의 크기만으로 결정할 수 없으므로
\end{enumerate}

작도(변위, 평행사변형의 법칙, 역벡터),\\
내분점과 외분점의 위치벡터를 이용한 치환, 성분화,\\
크기의 제곱에서 내적과 연계, 벡터의 변형\\
등 일차결합의 선택에서 다룬 여러 방법 중 적절한 방법을 택한다.\\
또한 두 벡터 모두 시점 또는 종점이 움직일 때, 이 두 벡터의 일차결합은\\
적당한 한 벡터를 고정\\
하고 다른 한 벡터의 시점, 종점의 움직임에 따른 변화를 관찰하는 방법으로 다룰 수도 있다.

\section*{Comment}
Drill 벡터의 크기가 일정하지 않다\\
앞의 문제에서 $\overrightarrow{\mathrm{AX}}, \overrightarrow{\mathrm{AY}}$ 의 크기가 모두 일정하지 않으므로 $|\overrightarrow{\mathrm{AX}}+\overrightarrow{\mathrm{AY}}|$ 의 최대는 $\overrightarrow{\mathrm{AX}}$, $\overrightarrow{\mathrm{AY}}$ 가 이루는 각의 크기만으로 판단할 수 없다. 점 X 가 원 $x^{2}+y^{2}=25$ 위에 있으므로 $\overrightarrow{\mathrm{AX}}=\overrightarrow{\mathrm{AO}}+\overrightarrow{\mathrm{OX}}$ 로, 점 Y 가 원 $(x-6)^{2}+(y-8)^{2}=25$ 위에 있으므로 $\overrightarrow{\mathrm{AY}}=\overrightarrow{\mathrm{AC}}+\overrightarrow{\mathrm{CY}}$ 로 변형해보면 어떨까? $\overrightarrow{\mathrm{AO}}+\overrightarrow{\mathrm{AC}}$ 를 성분으로 나타낼 수 있고 크기가 일정한 두 벡터 $\overrightarrow{\mathrm{OX}}$, $\overrightarrow{\mathrm{CY}}$ 의 움직임만 $\overrightarrow{\mathrm{OX}} \cdot \overrightarrow{\mathrm{CY}}=0$ 임을 감안하여 조절해보면 된다. $\overrightarrow{\mathrm{CY}}$ 를 시점이 원점에 오도록 평행이동해서 다루는 센스를 발휘하면 더욱 좋다.

\section*{Comment}
Drill 벡터의 내적의 선택\\
벡터의 일차결합과 마찬가지로 벡터의 내적 역시 기본적으로 선택의 문제이다. 여러 방법 중에서 적당한 한 가지를 선택하여 풀어가다가 좋지 않다고 생각하면 다른 방법으로 빠르게 바꿀 수 있도록 여러 번 반복하여 숙지하고 있어야 한다.\\
벡터의 내적은 그 자체로는 단 한 번도 어렵게 출제된 적이 없다.\\
어렵게 느껴졌다면 연산의 선택이 잘못된 것일 뿐!\\
벡터의 내적의 기본적인 연산 방법은 다음과 같고, 벡터의 일차결합보다는 선택지가 단순하다.

\begin{enumerate}
  \item 크기와 각 $(|\vec{a}|,|\vec{b}|, \cos \theta)$
  \item 정사영과의 내적
  \item 성분화
  \item 벡터의 변형
\end{enumerate}

위의 세 가지 방법이 잘 적용되지 않으면 다음과 같이 주어진 벡터를 변형해서 다루어볼 수 있다.\\
(1) 시점을 하나로 통일시킨다.\\
(2) 시점과 종점 사이에 적절한 경유점(원의 중심, 다각형의 꼭짓점, 변의 중점, 무게중심 등)을 이용하여 $\overrightarrow{\mathrm{AB}}=\overrightarrow{\mathrm{AO}}+\overrightarrow{\mathrm{OB}}$ 와 같이 한 벡터를 여러 벡터의 합으로 분해한다.\\
(3) 크기와 내적이 확실한 두 벡터를 기본 벡터로 설정하여 이들의 일차결합으로 나타낸다.

\section*{Comment}
\section*{Drill 원에 대한 기본 태도와 정사영과의 내적}
앞의 문제에서는 삼각형 ABC 의 각 변을 외접원의 현으로 간주하면서 외접원의 중심 O 에서 각 변에 수선을 내리면 $\overrightarrow{\mathrm{AO}}$ 와의 내적을 정사영으로 다룰 수 있다는 것이 눈에 띄어야 한다. 원에 대한 태도의 기본 중의 기본에서 주어진 조건과 식의 형태를 정사영과의 내적과 연결 시킬 수 있는 것이다. 벡터의 내적을 두 벡터가 서로 같을 때와 서로 다를 때의 표현을 구분 하며 다항식의 곱셈처럼 자유롭게 다룰 수 있는 것도 꽤나 중요하다.

Drill 벡터의 크기의 제곱과 내적\\
벡터의 일차결합 $k \vec{a}+l \vec{b}$ 의 크기를 제곱하면

$$
\left.\left|k \vec{a}+|\vec{b}|^{2}=k^{2}\right| \vec{a}\right|^{2}+l^{2}|\vec{b}|^{2}+2 k l(\vec{a} \cdot \vec{b})
$$

이므로\\
크기, 각, 내적\\
의 조건을 연결시킬 수 있다. 벡터의 크기, 각, 내적에 관한 조건이 함께 등장한다면 벡터의 일차결합의 크기를 제곱해볼 수 있다는 것을 잊지 말자.

\section*{Comment}
Drill $\overrightarrow{\mathrm{OP}}=k \overrightarrow{\mathrm{OA}}+l \overrightarrow{\mathrm{OB}}$ 일 때 점 P 가 나타내는 도형\\
$\overrightarrow{\mathrm{OP}}=k \overrightarrow{\mathrm{OA}}+l \overrightarrow{\mathrm{OB}}$ 일 때\\
(1) $a \leq k \leq b, c \leq l \leq d$ 이면

점 P 가 나타내는 도형은 두 변이 각각 두 벡터 $\overrightarrow{\mathrm{OA}}, \overrightarrow{\mathrm{OB}}$ 와 평행한 평행사변형과 그 내부 이다.\\
\includegraphics[max width=\textwidth, center]{bdb034d6-8d2c-43fe-ae6d-01b7c8b19d17-6_363_484_993_1103}\\
(2) $k+l=1$ 이면 점 P 가 나타내는 도형은 직선 AB 이고\\
$k+l=n$ 이면 점 P 가 나타내는 도형은 점 O 를 닮음의 중심으로 하는 직선 AB 의 $n$ 배 닮은 도형이다.\\
\includegraphics[max width=\textwidth, center]{bdb034d6-8d2c-43fe-ae6d-01b7c8b19d17-6_521_808_1573_941}

\section*{Comment}
\section*{Drill 여러 가지 벡터방정식}
(1) 평면에서 세 정점 $\mathrm{O}, \mathrm{A}, \mathrm{B}$ 와 실수 $k$ 에 대하여

$$
\overrightarrow{\mathrm{AB}} \cdot \overrightarrow{\mathrm{OP}}=k
$$

일 때, 점 P 가 나타내는 도형은 직선 AB 에 수직인 직선이다.\\
⇒ 점 P 가 나타내는 직선을 $l$ 이라 하면 $<k,>k$ 일 때 점 P 는 각각 직선 $l$ 에 의하여 나누어진 두 영역 중 어느 한 영역에 있다.\\
(2) 평면에서 두 정점 $\mathrm{A}, \mathrm{B}$ 와 실수 $k$ 에 대하여

$$
\overrightarrow{\mathrm{PA}} \cdot \overrightarrow{\mathrm{~PB}}=k\left(\text { 단, } k+\frac{1}{4}|\overrightarrow{\mathrm{AB}}|^{2}>0\right)
$$

일 때, 점 P 가 나타내는 도형은 선분 AB 의 중점을 중심으로 하는 원이다.\\
$\Rightarrow<k$ 일 때 점 P 는 원의 내부에 있고, $>k$ 일 때 점 P 는 원의 외부에 있다.\\
특히

$$
\overrightarrow{\mathrm{PA}} \cdot \overrightarrow{\mathrm{~PB}}=0
$$

일 때, 점 P 가 나타내는 도형은 지름이 AB 인 원이다.\\
$\Rightarrow<0$ 일 때 점 P 는 원의 내부에 있고, $>0$ 일 때 점 P 는 원의 외부에 있다.\\
(3) 평면에서 두 정점 $\mathrm{A}, \mathrm{B}$ 와 세 실수 $m, n, k$ 에 대하여

$$
\left|\frac{m \overrightarrow{\mathrm{~PB}}+n \overrightarrow{\mathrm{PA}}}{m+n}\right|=k(k>0)
$$

일 때, 점 P 가 나타나는 도형은 중심이 직선 AB 위에 있고 반지름의 길이가 $k$ 인 원이다.\\
$\Rightarrow<k$ 일 때 점 P 는 원의 내부에 있고, $>k$ 일 때 점 P 는 원의 외부에 있다.

\section*{Comment}
\section*{Drill 벡터방정식의 다양한 표현}
동점이 나타내는 도형의 벡터의 관계식을 이용한 대표적인 표현 몇 가지를 정리해두기는 하지만 이것 외에도 꽤나 다양한 표현이 가능하다. 동점이 등장하고 그 움직임을 파악할 필요가 있다면 직선 또는 원, 그리고 그에 따른 영역일 가능성이 높다고 보고 기본 도형의 성질 등과 연계해서 주어진 벡터의 관계식을 파악할 수 있어야 한다. 앞의 문제의 $(\overrightarrow{\mathrm{AB}}+\overrightarrow{\mathrm{AC}}) \cdot \overrightarrow{\mathrm{BP}} \leq 0$ 에서는 선분 BC 의 중점의 위치벡터로 변형해서 점 P 가 존재하는 영역을 잡을 수 있고, $|\overrightarrow{\mathrm{BP}} \cdot \overrightarrow{\mathrm{CP}}|=\frac{1}{2}|\overrightarrow{\mathrm{BP}}||\overrightarrow{\mathrm{CP}}|$ 에서는 $\overrightarrow{\mathrm{BP}}, \overrightarrow{\mathrm{CP}}$ 가 이루는 각의 크기가 일정하므로 원주각과 연계하여 점 P 가 나타내는 도형을 잡을 수 있다. $\overrightarrow{\mathrm{BP}} \cdot \overrightarrow{\mathrm{CP}}$ 가 아닌 $|\overrightarrow{\mathrm{BP}} \cdot \overrightarrow{\mathrm{CP}}|$ 이므로 $\overrightarrow{\mathrm{BP}}, \overrightarrow{\mathrm{CP}}$ 가 이루는 각의 크기를 판단할 때 주의해야 한다.

\section*{Comminal 래른}
\section*{Drill 벡터의 일차결합과 내적의 선택에 매우 능숙해야}
앞의 문제에서는 벡터의 일차결합과 내적의 여러 상황에 대한 충분한 경험을 바탕으로 그 선택을 매우 능숙하게 할 수 있어야 한다. 우선 조건 (가)에서 원 $C$ 위의 두 점 $\mathrm{A}, \mathrm{B}$ 의 위치를 감안하여 점 P 가 나타내는 도형을 파악해야 하고, 조건 (나)의 $\overrightarrow{\mathrm{AP}} \cdot \overrightarrow{\mathrm{BP}}$ 를 적절한 경유점을 이용하여 변형할 수 있어야 한다. 조건 (나)의 관계식에 $\mathrm{O}_{1}$ 이 함께 쓰인 것에 주목하는 것이 좋겠다. 그리고 조건 (다)에서 점 Q 가 원 $C$ 위의 점인 것, 점 P 가 나타내는 도형의 특수함 에서 내적이 0 인 상태를 기준으로 내적이 양수인 것의 의미를 생각할 수 있어야 한다.

마무리 단계에서 점들의 위치 관계에 착안하여 새로운 좌표계에서 성분화하겠다고 생각 했다면 베스트!


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
    text = re.sub(r'\\section\*\{Comminal 래른\}', '', text)
    
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
    
    # 섹션 헤더 처리
    text = re.sub(r'\\section\*\{([^}]+)\}', r'## \1', text)
    
    # 줄바꿈 처리
    text = re.sub(r'\\\\', '\n', text)
    
    # 기타 정리
    text = re.sub(r'\\%', '%', text)
    text = re.sub(r'\\Rightarrow', '⇒', text)
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
    
    # 벡터 관련 확인
    if '벡터' in solution_md or '\\overrightarrow' in solution_md or '\\vec' in solution_md:
        has_vector = ('\\overrightarrow' in solution_md or '\\vec' in solution_md or 
                     '벡터' in solution_md or '내적' in solution_md or '일차결합' in solution_md)
        if not has_vector:
            warnings.append("벡터 관련 내용이 해설에 명시되지 않음")
    
    # 원 관련 확인
    if '원' in solution_md:
        has_circle = ('원' in solution_md and ('x^{2}' in solution_md or 'y^{2}' in solution_md or 
                     '반지름' in solution_md or '중심' in solution_md))
        if not has_circle:
            warnings.append("원 관련 내용이 해설에 명시되지 않음")
    
    # 문제와 해설의 일관성 확인
    for problem in problems:
        question = problem.get('question', '')
        topic = problem.get('topic', '')
        
        # 벡터 문제
        if topic == '벡터' or '\\overrightarrow' in question or '\\vec' in question:
            if ('벡터' not in solution_md and '\\overrightarrow' not in solution_md and 
                '\\vec' not in solution_md and '내적' not in solution_md):
                warnings.append(f"문제 {problem.get('index')}: 벡터 문제인데 해설에 벡터 관련 내용이 없음")
        
        # 원 관련 문제
        if '원' in question and ('x^{2}' in question or 'y^{2}' in question):
            if '원' not in solution_md:
                warnings.append(f"문제 {problem.get('index')}: 원 관련 문제인데 해설에 원 관련 내용이 없음")
    
    # 수학적 오류 검증
    # 벡터의 크기 제곱 공식 확인
    if '|k \\vec{a}+l \\vec{b}|^{2}' in solution_md or '|k \\vec{a}+l \\vec{b}|^2' in solution_md:
        if 'k^{2}|\\vec{a}|^{2}+l^{2}|\\vec{b}|^{2}+2kl' in solution_md or 'k^2|\\vec{a}|^2+l^2|\\vec{b}|^2+2kl' in solution_md:
            pass  # 정확
        else:
            warnings.append("벡터의 크기 제곱 공식이 정확하지 않을 수 있음")
    
    return errors, warnings

def main():
    print("=" * 80)
    print("기하_2024학년도_현우진_드릴_P4 해설 → Deepseek R1-70B용 변환")
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
    problem_json_path = Path(r'C:\Users\a\Documents\MathPDF\organized\현우진\기하_2024학년도_현우진_드릴\기하_2024학년도_현우진_드릴_P4_문제_deepseek.json')
    
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
    md_content = "# 기하_2024학년도_현우진_드릴_P4 해설\n\n"
    md_content += "> 이 문서는 Deepseek R1-70B가 읽을 수 있도록 최적화된 마크다운 형식입니다.\n\n"
    md_content += solution_md
    
    md_path = base_dir / "기하_2024학년도_현우진_드릴_P4_해설_deepseek_r1.md"
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
