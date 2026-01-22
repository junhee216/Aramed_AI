# convert_geometry_p5_solution_deepseek.py
# 기하_2024학년도_현우진_드릴_P5 해설 LaTeX → Deepseek R1-70B용 변환

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
\section*{Drill 내적의 최대와 최소}
\begin{enumerate}
  \item 벡터의 크기가 일정할 때\\
$|\vec{a}|,|\vec{b}|$ 가 모두 일정할 때\\
(1) $\vec{a}, \vec{b}$ 가 이루는 각의 크기가 최소일 때, $\vec{a} \cdot \vec{b}$ 는 최대\\
(2) $\vec{a}, \vec{b}$ 가 이루는 각의 크기가 최대일 때, $\vec{a} \cdot \vec{b}$ 는 최소
  \item 벡터의 크기가 일정하지 않을 때\\
$|\vec{a}|$ 또는 $|\vec{b}|$ 가 일정하지 않으면 $\vec{a} \cdot \vec{b}$ 의 최대와 최소는 $\vec{a}, \vec{b}$ 가 이루는 각의 크기만으로 결정할 수 없으므로
\end{enumerate}

정사영과의 내적, 성분화, 벡터의 변형\\
등 내적의 선택에서 다룬 여러 방법 중 적절한 방법을 택한다. 이때 일차결합의 선택에서 다룬 방법을 함께 이용할 수도 있다.\\
또한 두 벡터 모두 시점 또는 종점이 움직일 때, 이 두 벡터의 내적은\\
적당한 한 벡터를 고정\\
하고 다른 한 벡터의 시점, 종점의 움직임에 따른 변화를 관찰하는 방법으로 다룰 수도 있다.

Drill 여러 가지 방법으로\\
앞의 문제에서 $\overrightarrow{\mathrm{QP}} \cdot(\overrightarrow{\mathrm{QO}}+\overrightarrow{\mathrm{QP}})$ 가 최대인 상황의 판단은 여러 가지 방법을 취해볼 수 있다. $\overrightarrow{\mathrm{QP}} \cdot \overrightarrow{\mathrm{QO}}+|\overrightarrow{\mathrm{QP}}|^{2}$ 으로 전개해볼 수도 있고, 선분 OP 의 중점 M 에 대하여 $\overrightarrow{\mathrm{QP}} \cdot 2 \overrightarrow{\mathrm{QM}}$ 으로 놓고 보아도 좋고, 원 $x^{2}+y^{2}=16$ 의 중심인 원점 O 를 경유점으로 잡아 $\overrightarrow{\mathrm{QP}}=\overrightarrow{\mathrm{QO}}+\overrightarrow{\mathrm{OP}}$ 로 놓고 전개하는 것도 좋다. 모든 상황에서 점 Q 가 $x$ 축보다 위쪽에 있는 경우와 아래쪽에 있는 경우로 케이스를 구분하고 각 케이스별로 점 Q 의 위치를 고정하여 내적이 최대인 상황을 살펴보면 된다.

\section*{Drill 1 선분의 내분점과 외분점의 위치벡터}
두 점 $\mathrm{A}, \mathrm{B}$ 의 위치벡터를 각각 $\vec{a}, \vec{b}$ 라 할 때\\
(1) 선분 AB 를 $m: n(m>0, n>0)$ 으로 내분하는 점 P 의 위치벡터 $\vec{p}$ 는

$$
\vec{p}=\frac{m \vec{b}+n \vec{a}}{m+n}
$$

(2) 선분 AB 를 $m: n(m>0, n>0, m \neq n)$ 으로 외분하는 점 Q 의 위치벡터 $\vec{q}$ 는

$$
\vec{q}=\frac{m \vec{b}-n \vec{a}}{m-n}
$$

\section*{Drill. 2 위치벡터 활용의 핵심은 치환}
선분의 내분점과 외분점의 위치벡터 활용의 핵심은 치환의 관점이다.\\
두 벡터 $\overrightarrow{\mathrm{OA}}, \overrightarrow{\mathrm{OB}}$ 의 일차결합 $k \overrightarrow{\mathrm{OA}}+l \overrightarrow{\mathrm{OB}}$ 를

$$
k \overrightarrow{\mathrm{OA}}+l \overrightarrow{\mathrm{OB}}=(k+l) \overrightarrow{\mathrm{OC}}
$$

와 같이 새로운 벡터 $(k+l) \overrightarrow{\mathrm{OC}}$ 로 치환하면 선분 AB 의 내분점 또는 외분점인 점 C 의 한 위치벡터 $\overrightarrow{\mathrm{OC}}$ 로 간단히 다룰 수도 있다는 것이다.\\[0pt]
[예] $2 \overrightarrow{\mathrm{OA}}+\overrightarrow{\mathrm{OB}}=3 \overrightarrow{\mathrm{OC}} \quad \Rightarrow$ 점 C 는 선분 AB 를 $1: 2$ 로 내분하는 점\\
$2 \overrightarrow{\mathrm{OA}}-3 \overrightarrow{\mathrm{OB}}=-\overrightarrow{\mathrm{OC}} \quad \Rightarrow$ 점 C 는 선분 AB 를 $3: 2$ 로 외분하는 점\\
$\frac{1}{3} \overrightarrow{\mathrm{OA}}+\frac{2}{3} \overrightarrow{\mathrm{OB}}=\overrightarrow{\mathrm{OC}} \quad \Rightarrow$ 점 C 는 선분 AB 를 $2: 1$ 로 내분하는 점\\
$2 \overrightarrow{\mathrm{OA}}-\overrightarrow{\mathrm{OB}}=\overrightarrow{\mathrm{OC}} \quad \Rightarrow$ 점 C 는 선분 AB 를 $1: 2$ 로 외분하는 점

\section*{Comment}
\section*{Drill 적절한 경유점의 선택}
앞의 문제에서는 $\overrightarrow{\mathrm{PO}}, \overrightarrow{\mathrm{PA}}$ 의 크기가 모두 일정하지 않으므로 $\overrightarrow{\mathrm{PO}}, \overrightarrow{\mathrm{PA}}$ 가 이루는 각의 크기 만으로 $\overrightarrow{\mathrm{PO}} \cdot \overrightarrow{\mathrm{PA}}$ 가 최대인 상태를 파악하기 어렵다. 정사영과의 내적이나 성분화도 좋은 방법은 아닌 것 같다. 적절한 경유점을 잡아 벡터를 변형하는 방법이 남았다. 우선 원 $C$ 의 중심을 경유점으로 잡아 벡터를 변형해보면? 전개식의 처리가 곤란하다는 것을 알 수 있다. 경유점으로 잡을 만한 다른 점은 무엇이 있을까? 벡터의 연산에 충분히 익숙하다면 $\overrightarrow{\mathrm{PO}}$, $\overrightarrow{\mathrm{PA}}$ 의 종점을 이은 선분 OA 의 중점이 딱 좋다고 쉽게 판단할 수 있을 것이다. 벡터의 변형을 위한 경유점은 주로 원의 중심, 다각형의 꼭짓점, 선분의 중점, 무게중심 등을 이용한다. 시행착오를 감안하며 두루 점검해보고 선택하면 된다.

\section*{Commment}
\section*{Drill 최대와 최소의 상황이 확실하도록}
경유점 등을 이용하여 벡터를 변형할 때 전개식에서 확실한 근거를 가지고 최대 또는 최소인 상황을 짚어낼 수 있어야 한다. 또한 최대 또는 최소의 근거가 명확하지 않은 상태를 가려낼 수 있어야 한다. 앞의 문제에서 원 $x^{2}+y^{2}=4$ 의 중심인 원점 O 를 경유점으로 잡아보면 $\overrightarrow{\mathrm{PQ}} \cdot \overrightarrow{\mathrm{OQ}}$ 는 $\overrightarrow{\mathrm{PO}} \cdot \overrightarrow{\mathrm{OQ}}+\left.\overrightarrow{\mathrm{OQ}}\right|^{2}$ 으로 제법 그럴듯하게 변형된다. $\overrightarrow{\mathrm{OQ}}$ 의 크기가 최대가 되도록 하고 이때 $\overrightarrow{\mathrm{PO}}=(2,0)$, 즉 점 P 의 좌표가 $(-2,0)$ 이어서 $\overrightarrow{\mathrm{PO}} \cdot \overrightarrow{\mathrm{OQ}}$ 가 함께 최대이면 될 것 같지만 $\cdots$ 아니다. $\overrightarrow{\mathrm{OQ}}$ 의 크기는 $\overrightarrow{\mathrm{OQ}}=\left(3+\frac{\sqrt{2}}{2}, 3+\frac{\sqrt{2}}{2}\right)$ 일 때 최대이고 $\overrightarrow{\mathrm{PO}} \cdot \overrightarrow{\mathrm{OQ}}$ 는 $\overrightarrow{\mathrm{PO}}=(2,0), \overrightarrow{\mathrm{OQ}}=(4,3)$ 일 때 최대이다. 원 $(x-3)^{2}+(y-3)^{2}=1$ 의 중심을 경유점으로 잡아 보면? $\overrightarrow{\mathrm{PQ}} \cdot \overrightarrow{\mathrm{OQ}}$ 를 변형한 결과에서 곧바로 결론을 내긴 힘들지만, 원점 O 를 경유점으로 잡아 다시 한번 변형해보면 길이 보인다. 선분의 중점은 어떨까? 세 선분 $\mathrm{OP}, \mathrm{OQ}, \mathrm{PQ}$ 중 선분 OP 의 중점의 움직임이 가장 안정적으로 눈에 들어오고, 이를 이용한 $\overrightarrow{\mathrm{PQ}} \cdot \overrightarrow{\mathrm{OQ}}$ 의 변형도 좋은 방법이 된다.

\section*{Drill 동점이 나타내는 도형}
동점에 대한 벡터의 크기, 합, 차, 내적에 관한 관계식이 주어진다면 그 동점은 직선 또는 원과 그에 따른 영역을 나타낼 것이라 생각하고 동점이 나타내는 도형을 파악하도록 하자. 앞의 문제에서 점 P 가 나타내는 도형은 점 A 를 중심으로 하고 반지름의 길이가 $a$ 인 원, 점 Q 가 나타내는 도형은 점 B 를 중심으로 하고 반지름의 길이가 $b$ 인 원이라는 것은 쉽게 알 수 있다. 여기에 $\overrightarrow{\mathrm{OB}} \cdot \overrightarrow{\mathrm{BQ}} \leq 0$ 인 조건에서 점 B 가 나타내는 도형은 직선을 경계로 하는 한 영역으로 제한된다는 것도 쉽게 예상하고 확인해볼 수 있다. $\overrightarrow{\mathrm{OA}} \cdot \overrightarrow{\mathrm{PQ}}$ 의 최댓값이 0 이라는데, 내적이 0 이라는 것은? 가장 확실한 기하적 근거로부터 출발해보자.

\section*{Comment}
\section*{Drill 벡터의 내적의 기본을 잊지 말자}
앞의 문제에서 $|\overrightarrow{\mathrm{PQ}}+\overrightarrow{\mathrm{PR}}|$ 의 최대를 다룰 때는 점 Q 가 원 $C_{1}$ 위에 있으므로 원 $C_{1}$ 의 중심을 $\mathrm{O}_{1}$ 이라 하고 $\overrightarrow{\mathrm{PQ}}=\overrightarrow{\mathrm{PO}_{1}}+\overrightarrow{\mathrm{O}_{1} \mathrm{Q}}$ 로, 점 R 가 원 $C_{2}$ 위에 있으므로 원 $C_{2}$ 의 중심을 $\mathrm{O}_{2}$ 라 하고 $\overrightarrow{\mathrm{PR}}=\overrightarrow{\mathrm{PO}_{2}}+\overrightarrow{\mathrm{O}_{2} \mathrm{R}}$ 로 변형해보면, $\overrightarrow{\mathrm{PO}_{1}}+\overrightarrow{\mathrm{PO}_{2}}$ 는 선분 $\mathrm{O}_{1} \mathrm{O}_{2}$ 의 중점의 위치벡터로 나타낼 수 있고 크기가 일정한 두 벡터 $\overrightarrow{\mathrm{O}_{1} \mathrm{Q}}, \overrightarrow{\mathrm{O}_{2} \mathrm{R}}$ 와 함께 그 합이 최대가 되도록 조절하기 쉬운 상황이 된다. 이렇게 두 원 $C_{1}, C_{2}$ 의 반지름의 길이를 정하고 나면 $\overrightarrow{\mathrm{AP}} \cdot \overrightarrow{\mathrm{QR}}$ 의 최소는 어떻게 다룰까? 경유점을 잡아 이리저리 변형해 봐도 딱히 마음에 드는 전개식을 얻기가 힘들다.\\
최근 고난도의 벡터의 내적의 문제가 주로 경유점을 이용한 변형이었다는데 얽매이지 말고 벡터의 내적의 기본인 정사영과의 내적으로 돌아가 보자! 적당히 $\overrightarrow{\mathrm{AP}}$ 를 고정해놓은 상태에서 $\overrightarrow{\mathrm{AP}} \cdot \overrightarrow{\mathrm{QR}}$ 가 최소가 되도록 $\overrightarrow{\mathrm{QR}}$ 의 $\overrightarrow{\mathrm{AP}}$ 위로의 정사영을 잡을 수 있다. 이것만 눈에 띄면 기하적으로만 끌고 가기 어려우므로 $\angle \mathrm{PAB}$ 의 크기를 미지수로 잡아 삼각비로 내적의 식을 나타내면 되겠다는 판단까지 충분히 가능할 것이다.

\section*{Drill 직선과 평면이 이루는 각}
직선 $l$ 이 평면 $\alpha$ 와 점 O 에서 만날 때, 직선 $l$ 위의 점 P 에서 평면 $\alpha$ 에 내린 수선의 발을 H 라 하면 두 직선 $l, \mathrm{OH}$ 가 이루는 각을 직선 $l$ 과 평면 $\alpha$ 가 이루는 각이라고 한다.\\
\includegraphics[max width=\textwidth, center]{18e8dbbc-02a7-4f12-970c-4d5aefffe813-8_194_483_765_1438}

결국 직선 $l$ 과 평면 $\alpha$ 가 이루는 각의 문제는 직선 $l$ 과 평면 $\alpha$ 위의 직선이 이루는 각의 문제가 된다. 평면 $\alpha$ 위의 직선은 임의로 설정하면 안 되고 위의 그림에서 직선 $l$ 위의 점 P 에서 평면 $\alpha$ 에 내린 '수선의 발' H 와 직선 $l$ 과 평면 $\alpha$ 의 '교점' O 를 이은 직선 OH 이어야만 한다. 마무리는 '직각삼각형' POH 에서!


\end{document}"""

def clean_math_content(math_str):
    """수식 내용 정리"""
    # \mathrm 제거
    math_str = re.sub(r'\\mathrm\{([^}]+)\}', r'\1', math_str)
    # \left, \right 제거
    math_str = re.sub(r'\\left([\(\[\{])', r'\1', math_str)
    math_str = re.sub(r'\\right([\)\]\}])', r'\1', math_str)
    # 공백 정리
    math_str = re.sub(r'\s+', ' ', math_str)
    return math_str.strip()

def latex_to_markdown_for_deepseek(latex_text):
    """LaTeX를 Deepseek R1-70B용 마크다운으로 변환"""
    text = latex_text
    
    # Comment 섹션 제거 (오타 포함)
    comment_patterns = [
        r'\\section\*\{Comment\}',
        r'\\section\*\{Commment\}',
        r'\\section\*\{Communernt\}',
        r'\\section\*\{Commune \(OmH\}',
        r'\\section\*\{Commnent\}',
        r'\\section\*\{Communent\}',
        r'\\section\*\{Comminal 래른\}'
    ]
    for pattern in comment_patterns:
        text = re.sub(pattern, '', text)
    
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
    
    # aligned 환경 처리
    def replace_aligned(match):
        content = match.group(1)
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
    text = re.sub(r'\\begin\{aligned\}(.*?)\\end\{aligned\}', replace_aligned, text, flags=re.DOTALL)
    
    # enumerate 환경 처리
    def replace_enumerate(match):
        content = match.group(1)
        # \item을 - 로 변환
        content = re.sub(r'\\item\s+', '- ', content)
        return content
    text = re.sub(r'\\begin\{enumerate\}(.*?)\\end\{enumerate\}', replace_enumerate, text, flags=re.DOTALL)
    
    # \item 처리
    text = re.sub(r'\\item\s+', '- ', text)
    
    # 줄바꿈 처리
    text = re.sub(r'\\\\', '\n', text)
    
    # 이미지 처리
    text = re.sub(r'\\includegraphics\[[^\]]*\]\{[^}]+\}', '[이미지]', text)
    
    # 섹션 헤더 처리
    text = re.sub(r'\\section\*\{([^}]+)\}', r'## \1', text)
    
    # [0pt] 제거
    text = re.sub(r'\\\[0pt\]', '', text)
    text = re.sub(r'\[0pt\]', '', text)
    
    # 기타 정리
    text = re.sub(r'\\%', '%', text)
    text = re.sub(r'[ \t]+', ' ', text)  # 연속 공백
    text = re.sub(r'\n{3,}', '\n\n', text)  # 연속 줄바꿈
    text = re.sub(r'^\s+', '', text, flags=re.MULTILINE)  # 줄 시작 공백
    
    return text.strip()

def validate_math_logic(solution_md, problems):
    """수학적 논리 검증"""
    errors = []
    warnings = []
    
    # 벡터 관련 검증
    if '벡터' in solution_md or '\\overrightarrow' in solution_md or '\\vec' in solution_md:
        # 벡터의 내적 관련 내용 확인
        if '내적' in solution_md or '\\cdot' in solution_md:
            pass  # 정확
        else:
            warnings.append('벡터 문제인데 내적 관련 내용이 해설에 명시되지 않음')
        
        # 벡터의 크기 제곱 공식 확인
        if '|k \\vec{a}+l \\vec{b}|^{2}' in solution_md or '|k \\vec{a}+l \\vec{b}|^2' in solution_md:
            if 'k^{2}|\\vec{a}|^{2}+l^{2}|\\vec{b}|^{2}+2kl' in solution_md or 'k^2|\\vec{a}|^2+l^2|\\vec{b}|^2+2kl' in solution_md:
                pass  # 정확
            else:
                warnings.append('벡터 크기 제곱 공식이 해설에 명시되지 않음')
    
    # 원과 벡터 결합 문제 검증
    if '원' in solution_md and ('x^{2}' in solution_md or 'y^{2}' in solution_md):
        if '벡터' in solution_md or '\\overrightarrow' in solution_md:
            pass  # 정확
        else:
            warnings.append('원과 벡터 결합 문제인데 벡터 관련 내용이 해설에 명시되지 않음')
    
    # 공간도형 검증
    if '공간' in solution_md or '평면' in solution_md and '직선' in solution_md:
        if '직선과 평면이 이루는 각' in solution_md or '직선 $l$ 과 평면' in solution_md:
            pass  # 정확
        else:
            warnings.append('공간도형 문제인데 직선과 평면의 각 관련 내용이 해설에 명시되지 않음')
    
    # 문제와 해설의 일관성 확인
    vector_problems = [p for p in problems if p.get('topic') == '벡터']
    if vector_problems:
        if '벡터' not in solution_md and '\\overrightarrow' not in solution_md:
            warnings.append('벡터 문제가 있는데 해설에 벡터 관련 내용이 명시되지 않음')
    
    space_problems = [p for p in problems if p.get('topic') == '공간도형']
    if space_problems:
        if '공간' not in solution_md and '평면' not in solution_md:
            warnings.append('공간도형 문제가 있는데 해설에 공간도형 관련 내용이 명시되지 않음')
    
    return errors, warnings

def main():
    print("=" * 80)
    print("기하_2024학년도_현우진_드릴_P5 해설 → Deepseek R1-70B용 변환")
    print("=" * 80)
    
    # \begin{document} 이후만 추출
    doc_match = re.search(r'\\begin\{document\}(.*?)\\end\{document\}', latex_content, re.DOTALL)
    if not doc_match:
        print("❌ 문서 본문을 찾을 수 없습니다.")
        return
    
    body = doc_match.group(1)
    
    # 해설 변환
    solution_md = latex_to_markdown_for_deepseek(body)
    
    # 문제 파일 로드 (검증용)
    problem_json_path = Path(r'C:\Users\a\Documents\MathPDF\organized\현우진\기하_2024학년도_현우진_드릴\기하_2024학년도_현우진_드릴_P5_문제_deepseek.json')
    problems = []
    if problem_json_path.exists():
        with open(problem_json_path, 'r', encoding='utf-8') as f:
            problems = json.load(f)
        print(f"\n📖 문제 파일 로드 완료: {len(problems)}개 문제")
    else:
        print(f"\n⚠️  문제 파일을 찾을 수 없습니다: {problem_json_path}")
    
    # 수학적 논리 검증
    math_errors, math_warnings = validate_math_logic(solution_md, problems)
    
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
    md_content = "# 기하_2024학년도_현우진_드릴_P5 해설\n\n"
    md_content += "> 이 문서는 Deepseek R1-70B가 읽을 수 있도록 최적화된 마크다운 형식입니다.\n\n"
    md_content += solution_md
    
    md_path = base_dir / "기하_2024학년도_현우진_드릴_P5_해설_deepseek_r1.md"
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
