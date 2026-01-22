# convert_haktong_p6_solution_latex.py
# 확통_2024학년도_현우진_드릴_P6_해설 LaTeX 변환

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

# LaTeX 파일 읽기
latex_file = Path(__file__).parent / 'haktong_p6_solution_latex.txt'
if latex_file.exists():
    with open(latex_file, 'r', encoding='utf-8') as f:
        latex_content = f.read()
else:
    # 직접 입력 (사용자가 제공한 내용)
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
\usepackage{bbold}
\usepackage{caption}
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
\IfFontExistsTF{Noto Serif CJK TC}
{\setCJKfallbackfamilyfont{\CJKrmdefault}{Noto Serif CJK TC}}
{\IfFontExistsTF{STSong}
  {\setCJKfallbackfamilyfont{\CJKrmdefault}{STSong}}
  {\IfFontExistsTF{Droid Sans Fallback}
    {\setCJKfallbackfamilyfont{\CJKrmdefault}{Droid Sans Fallback}}
    {\setCJKfallbackfamilyfont{\CJKrmdefault}{SimSun}}
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
\captionsetup{singlelinecheck=false}
\section*{Drill 확률질량함수}
\begin{enumerate}
  \item 확률질량함수
\end{enumerate}

확률변수 $X$ 가 가지는 값이 유한개이거나 자연수와 같이 셀 수 있을 때, 그 확률변수 $X$ 를 이산확률변수라고 한다.\\
또, 이산확률변수 $X$ 가 어떤 값 $x$ 를 가질 확률을 기호

$$
\mathrm{P}(X=x)
$$

로 나타낼 때, $X$ 가 가지는 값 $x_{i}(i=1,2,3, \cdots, n)$ 와 $X$ 가 $x_{i}$ 를 가질 확률 $p_{i}$ 의 대응 관계

$$
\mathrm{P}\left(X=x_{i}\right)=p_{i}(i=1,2,3, \cdots, n)
$$

를 이산확률변수 $X$ 의 확률분포라고 한다.\\
이 대응 관계를 나타내는 함수를 확률질량함수라고 한다.

2 ) 확률질량함수의 성질\\
(1) $0 \leq p_{i} \leq 1(i=1,2,3, \cdots, n)$\\
(2) $\sum_{i=1}^{n} p_{i}=1$\\
(3) $\mathrm{P}\left(x_{i} \leq X \leq x_{j}\right)=\sum_{k=i}^{j} p_{k}(i, j=1,2,3, \cdots, n, i \leq j)$

\section*{Drill 확률변수의 합의 대칭과 확률의 대칭}
이산확률변수 $X$ 의 확률분포가 $\mathrm{P}\left(X=x_{i}\right)=p_{i}(i=1,2,3, \cdots, n)$ 일 때 $x_{1}+x_{n}=x_{2}+x_{n-1}=x_{3}+x_{n-2}=\cdots$ 이고 $p_{1}=p_{n}, p_{2}=p_{n-1}, p_{3}=p_{n-2}, \cdots$ 이면 $\mathrm{E}(X)=\frac{x_{1}+x_{n}}{2}$\\[0pt]
[증명] $n=2 k$ ( $k$ 는 자연수)일 때

$$
\begin{aligned}
& x_{1}+x_{n}=x_{2}+x_{n-1}=\cdots=x_{k}+x_{k+1} \text { 이고, } p_{1}=p_{n}, p_{2}=p_{n-1}, \cdots, p_{k}=p_{k+1} \text { 에서 } \\
& \begin{aligned}
&\left(p_{1}+p_{2}+\cdots+p_{k}\right)+\left(p_{k+1}+\cdots+p_{n-1}+p_{n}\right)=1, \text { 즉 } p_{1}+p_{2}+\cdots+p_{k}=\frac{1}{2} \text { 이므로 } \\
& \mathrm{E}(X)=\left(x_{1} p_{1}+x_{n} p_{n}\right)+\left(x_{2} p_{2}+x_{n-1} p_{n-1}\right)+\cdots+\left(x_{k} p_{k}+x_{k+1} p_{k+1}\right) \\
&=\left(x_{1}+x_{n}\right) p_{1}+\left(x_{1}+x_{n}\right) p_{2}+\cdots+\left(x_{1}+x_{n}\right) p_{k} \\
&=\left(x_{1}+x_{n}\right)\left(p_{1}+p_{2}+\cdots+p_{k}\right) \\
&=\frac{x_{1}+x_{n}}{2}
\end{aligned} \\
& \begin{aligned}
& n=2 k+1 \text { 일 때 } \\
& x_{1}+x_{n}=x_{2}+x_{n-1}=\cdots=x_{k}+x_{k+2}=2 x_{k+1} \text { 이고, } p_{1}=p_{n}, p_{2}=p_{n-1}, \cdots, \\
& p_{k}=p_{k+2} \text { 에서 }\left(p_{1}-p_{2}+\cdots+p_{k}\right)+p_{k+1}+\left(p_{k+2}+\cdots+p_{n-1}+p_{n}\right)=1, \text { 즉 } \\
& 2\left(p_{1}+p_{2}+\cdots+p_{k}\right)=1-p_{k+1} \text { 이므로 } \\
& \mathrm{E}(X)=\left(x_{1} p_{1}+x_{n} p_{n}\right)+\left(x_{2} p_{2}+x_{n-1} p_{n-1}\right)+\cdots+\left(x_{k} p_{k}+x_{k+2} p_{k+2}\right)+x_{k+1} p_{k+1} \\
&=2 x_{k+1} p_{1}+2 x_{k+1} p_{2}+\cdots+2 x_{k+1} p_{k}+x_{k+1} p_{k+1} \\
&=x_{k+1}\left(1-p_{k+1}\right)+x_{k+1} p_{k+1}=x_{k+1} \\
&=\frac{x_{1}+x_{n}}{2}
\end{aligned}
\end{aligned}
$$

\section*{Drill 분산의 계산 방법의 선택}
분산을 ' $(\text { 편차 })^{2}$ 의 평균'으로 구할 것인지 '(제곱의 평균) - (평균의 제곱)'으로 구할 것인지 상황에 따라 적절히 선택할 수 있도록 하자. '(제곱의 평균)-(평균의 제곱)'으로 다루는 것이 유리한 경우가 많고 앞의 문제도 마찬가지이지만 ' (편차) ${ }^{2}$ 의 평균'으로 다루는 것이 유리한 경우도 있으므로 잊지 않도록 하자. 이는 분산의 정의이기도 하다.

\section*{Drill. 1 이항분포의 평균, 분산, 표준편차}
확률변수 $X$ 가 이항분포 $\mathrm{B}(n, p)$ 를 따를 때 (단, $q=1-p$ )

$$
\begin{aligned}
& \mathrm{E}(X)=n p=\sum_{x=0}^{n} x_{n} \mathrm{C}_{x} p^{x} q^{n-x} \\
& \begin{aligned}
\mathrm{V}(X)=n p q & =\sum_{x=0}^{n}(x-n p)_{n}^{2} \mathrm{C}_{x} p^{x} q^{n-x} \\
& =\sum_{x=0}^{n} x_{n}^{2} \mathrm{C}_{x} p^{x} q^{n-x}-(n p)^{2}
\end{aligned} \\
& \begin{aligned}
\sigma(X) & =\sqrt{n p q}
\end{aligned}
\end{aligned}
$$

Drill. 2 이항분포의 상황 파악\\
이항분포에 관한 문제는 시행 횟수와 주목하는 사건의 발생 확률만 파악하면 그만이다. 결국 이항분포임을 알아채는 것이 관건이므로 이항분포에 관한 다음 특징을 잘 기억하도록 하자.\\
(1) 독립시행에 관한 확률분포이다. ⇒ 어떤 동일한 시행이 독립적으로 $n$ 번 반복되는 상황 이라면 이항분포인지 체크해볼 필요가 있다.\\
(2) 독립시행에서 주목하는 사건의 발생 횟수가 확률변수이다.

\section*{Drill 이항분포와 확률변수의 변환}
이항분포의 상황에서 출발하여 이항분포의 확률변수 $X$ 가 아닌 다른 확률변수 $Y$ 에 대해 다루는 경우가 많다. 이때는 두 확률변수 사이에 $Y=a X+b$ 꼴의 관계식을 구한 후, 손쉽게 구할 수 있는 $X$ 의 평균, 분산, 표준편차를 이용하여 $Y$ 의 평균, 분산, 표준편차를 다루게 된다는 흐름을 알아두자.\\
앞의 문제에서는 첫 번째 시행에서 주머니에 공을 넣는 개수에 따라 케이스를 구분해야 한다. 첫 번째 시행에서 주머니에 공을 1 개 넣는다면 두 번째 시행부터는 주머니에 공을 1 개씩만 넣게 된다. 첫 번째 시행에서 주머니에 공을 2 개 넣는다면 두 번째 시행부터는 주머니에 공을 넣는 개수가 두 가지로 나누어진다. 주머니에 공을 1 개 넣는 것과 2 개 넣는 것 중 어느 사건에 주목해야 확률변수 $X$ 의 값의 변화를 나타낼 수 있는지부터 정해야 한다.

\section*{Drill. 1 확률밀도함수}
일반적으로 $\alpha \leq X \leq \beta$ 에서 모든 실숫값을 가지는 연속확률변수 $X$ 에 대하여 다음 확률밀도 함수의 성질을 만족시키는 함수 $f$ 가 존재하며, 이러한 함수 $f$ 를 연속확률변수 $X$ 의 확률밀도 함수라 한다.\\
또한 $X$ 는 확률밀도함수가 $f$ 인 확률분포를 따른다고 한다.\\
(1) $f(x) \geq 0$\\
(2) 함수 $y=f(x)$ 의 그래프와 $x$ 축 및 두 직선 $x=\alpha, x=\beta$ 로 둘러싸인 부분의 넓이는 1 이다.\\
(3) 확률 $\mathrm{P}(a \leq X \leq b)$ 는 함수 $y=f(x)$ 의 그래프와 $x$ 축 및 두 직선 $x=a, x=b$ 로 둘러싸인 부분의 넓이와 같다. (단, $\alpha \leq a \leq b \leq \beta$ )\\
\includegraphics[max width=\textwidth, center]{80267479-dc9f-4c5e-8e7b-d229535fc6e5-6_339_380_1231_1157}

확률밀도함수의 성질의 (1), (2)는 $f$ 가 확률밀도함수이기 위한 필요충분조건이다.

확률질량함수 $\mathrm{P}(X=x)$ 의 $x$ 에서의 함숫값은 확률을 나타내지만, 확률밀도함수 $f(x)$ 의 $x$ 에서의 함숫값은 확률을 나타내지 않는다는데 주의하자.

\section*{Drill. 2 확률밀도함수의 정적분}
연속확률변수 $X$ 의 확률밀도함수가 $f(x)$ 일 때

$$
\mathrm{P}(X=c)=0(c \text { 는 상수 })
$$

이므로

$$
\mathrm{P}(a<X<b)=\mathrm{P}(a \leq X<b)=\mathrm{P}(a<X \leq b)=\mathrm{P}(a \leq X \leq b)=\int_{a}^{b} f(x) d x
$$

이고, 연속확률변수에서 확률은 확률밀도함수의 정적분으로 다룰 수 있다는 것에 주목할 필요가 있다.\\
주로 넓이에 관한 기하적 관점과 정적분의 성질을 이용하게 된다.\\
다음은 교육부 고시 제 2015-74호의 '수학과 교육과정'에서 이에 대해 언급한 내용이다.\\
(나) 교수 •학습 방법 및 유의 사항

\begin{itemize}
  \item 〈수학 $\mathbb{I}$ 〉를 이수한 학생들에게는 연속확률변수와 관련된 내용을 적분을 이용하여 설명할 수 있다.
\end{itemize}

\section*{Comment}
\section*{Drill. 1 표준정규분포표의 이용}
정규분포 $\mathrm{N}\left(m, \sigma^{2}\right)$ 의 확률 $\mathrm{P}\left(x_{1} \leq X \leq x_{2}\right)$ 는\\
표준정규분포 $\mathrm{N}\left(0,1^{2}\right)$ 의 확률 $\mathrm{P}\left(\frac{x_{1}-m}{\sigma} \leq Z \leq \frac{x_{2}-m}{\sigma}\right)$ 과 같고,\\
표준정규분포표를 이용하여 그 값을 구할 수 있다.\\
\includegraphics[max width=\textwidth, center]{80267479-dc9f-4c5e-8e7b-d229535fc6e5-8_201_505_1007_903}\\
\includegraphics[max width=\textwidth, center]{80267479-dc9f-4c5e-8e7b-d229535fc6e5-8_220_369_1007_1394}

확률변수 $X$ 가 정규분포 $\mathrm{N}\left(m, \sigma^{2}\right)$ 을 따를 때,\\
확률 $\mathrm{P}(m \leq X \leq m+k \sigma), \mathrm{P}(m-k \sigma \leq X \leq m)(k>0)$ 의 값은 표준정규분포표에서 $z=k$ 일 때의 값과 같다.\\
확률변수 $Z$ 가 표준정규분포 $\mathrm{N}\left(0,1^{2}\right)$ 을 따를 때,\\
확률 $\mathrm{P}(0 \leq Z \leq k), \mathrm{P}(-k \leq Z \leq 0)(k>0)$ 의 값은 표준정규분포표에서 $z=k$ 일 때의 값과 같다.

\section*{Drill. 2 정규분포에서 확률의 최댓값}
정규분포 $\mathrm{N}\left(m, \sigma^{2}\right)$ 을 따르는 확률변수가 $X$ 일 때, $b-a$ 의 값이 일정하면 $\mathrm{P}(a \leq X \leq b)$ 의 값은 $\frac{a+b}{2}=m$ 일 때 최대이다.

\begin{figure}[h]
\begin{center}
  \includegraphics[max width=\textwidth]{80267479-dc9f-4c5e-8e7b-d229535fc6e5-8_182_344_1831_929}
\captionsetup{labelformat=empty}
\caption{(단, $b-a$ 일정)}
\end{center}
\end{figure}

구간이 평균에 가까워질수록 확률이 커진다.

\begin{figure}[h]
\begin{center}
  \includegraphics[max width=\textwidth]{80267479-dc9f-4c5e-8e7b-d229535fc6e5-8_188_446_1829_1287}
\captionsetup{labelformat=empty}
\caption{$m=\frac{a+b}{2}$ 일 때, 최대}
\end{center}
\end{figure}

\section*{Comment}
Drill 정규분포에서 확률밀도함수의 그래프의 높이의 대소와 합동\\
(1) 정규분포에서 확률밀도함수의 그래프의 높이의 대소

정규분포에서 확률밀도함수의 그래프와 $x$ 축 사이의 넓이는 1 로 일정하므로 그 높이는 평균 으로부터 넓게 퍼지면(표준편차가 커지면) 작아지고 평균에 모이면(표준편차가 작아 지면) 커지게 된다.

\begin{figure}[h]
\begin{center}
  \includegraphics[max width=\textwidth]{80267479-dc9f-4c5e-8e7b-d229535fc6e5-9_250_362_1033_934}
\captionsetup{labelformat=empty}
\caption{[표준편차가 커질 때]}
\end{center}
\end{figure}

\begin{figure}[h]
\begin{center}
  \includegraphics[max width=\textwidth]{80267479-dc9f-4c5e-8e7b-d229535fc6e5-9_248_365_1033_1351}
\captionsetup{labelformat=empty}
\caption{[표준편차가 작아질 때]}
\end{center}
\end{figure}

(2) 정규분포에서 확률밀도함수의 그래프의 합동

표준편차가 같고 평균이 각각 $m_{1}, m_{2}$ 인 두 정규분포의 확률밀도함수의 그래프는 $m_{1}$, $m_{2}$ 의 값에 관계없이 서로 합동이고, $m_{1} \neq m_{2}$ 일 때 교점의 $x$ 좌표는 $\frac{m_{1}+m_{2}}{2}$ 이다.\\
\includegraphics[max width=\textwidth, center]{80267479-dc9f-4c5e-8e7b-d229535fc6e5-9_275_554_1635_1050}


\end{document}"""

def extract_solutions_from_latex(latex_content):
    """LaTeX에서 해설 추출"""
    body = extract_body(latex_content)
    solutions = []
    
    # 섹션 헤더 찾기
    section_pattern = r'\\section\*\{([^}]+)\}'
    sections = list(re.finditer(section_pattern, body))
    
    print(f"📊 발견된 섹션: {len(sections)}개")
    
    # Comment 섹션 찾기
    comment_sections = []
    for section in sections:
        section_text = section.group(1).strip()
        if 'Comment' in section_text:
            comment_sections.append(section.start())
    
    print(f"📊 발견된 Comment 섹션: {len(comment_sections)}개")
    
    # Drill 섹션 추출
    seen_titles = set()
    is_strategy_mode = False  # Comment 이후의 Drill은 strategy
    
    for i, section in enumerate(sections):
        section_text = section.group(1).strip()
        
        # Comment 섹션 확인
        if 'Comment' in section_text:
            is_strategy_mode = True
            # Comment 다음에 바로 나오는 Drill 텍스트 처리
            comment_end = section.end()
            if i < len(sections) - 1:
                next_section_start = sections[i+1].start()
            else:
                next_section_start = len(body)
            
            # Comment 섹션 다음의 텍스트를 해설로 추출
            content = body[comment_end:next_section_start]
            
            # "Drill"로 시작하는 텍스트 찾기
            drill_match = re.search(r'Drill\s+([^\n\\]+)', content)
            if drill_match:
                title = drill_match.group(1).strip()
                content_start = drill_match.end()
                content_text = content[content_start:].strip()
                
                # 이미지 제거
                content_text = re.sub(r'\\includegraphics.*?\{[^}]+\}', '', content_text)
                content_text = re.sub(r'\\begin\{figure\}.*?\\end\{figure\}', '', content_text, flags=re.DOTALL)
                content_text = clean_latex_text(content_text)
                
                if content_text and len(content_text) > 10:
                    solution = {
                        'index': f"{len(solutions)+1:02d}",
                        'title': title,
                        'type': 'strategy',
                        'content': content_text
                    }
                    solutions.append(solution)
                    print(f"✅ 해설 {solution['index']} 추출 완료 (strategy): {title}")
            continue
        
        # Drill 섹션만 처리
        if not section_text.startswith('Drill'):
            continue
        
        # 섹션 제목 추출
        title = section_text.replace('Drill', '').strip()
        # "Drill. 1", "Drill. 2" 같은 번호 제거
        title = re.sub(r'^\.\s*\d+\s*', '', title).strip()
        # "Drill. 1" 패턴 처리
        title = re.sub(r'^\.\s*\d+\s+', '', title).strip()
        
        # 중복 제거 (제목 기반)
        title_key = title[:50]  # 첫 50자로 비교
        if title_key in seen_titles:
            continue
        seen_titles.add(title_key)
        
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
        
        # figure 환경 제거
        content = re.sub(r'\\begin\{figure\}.*?\\end\{figure\}', '', content, flags=re.DOTALL)
        
        # enumerate 환경 제거 (내용은 보존)
        enumerate_match = re.search(r'\\begin\{enumerate\}(.*?)\\end\{enumerate\}', content, re.DOTALL)
        if enumerate_match:
            enumerate_content = enumerate_match.group(1)
            enumerate_content = re.sub(r'\\item\s*', '', enumerate_content)
            content = content.replace(enumerate_match.group(0), enumerate_content)
        
        # itemize 환경 제거 (내용은 보존)
        itemize_match = re.search(r'\\begin\{itemize\}(.*?)\\end\{itemize\}', content, re.DOTALL)
        if itemize_match:
            itemize_content = itemize_match.group(1)
            itemize_content = re.sub(r'\\item\s*', '', itemize_content)
            content = content.replace(itemize_match.group(0), itemize_content)
        
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
        
        # 수학적 논리 검사 (통계 관련)
        if '이항분포' in content:
            if 'B(n' not in content and '독립시행' not in content:
                warnings.append(f"해설 {solution['index']}: 이항분포에서 독립시행 명시 없음")
        
        if '확률밀도함수' in content:
            if '정적분' not in content and '넓이' not in content:
                warnings.append(f"해설 {solution['index']}: 확률밀도함수에서 정적분/넓이 명시 없음")
        
        if '정규분포' in content:
            if 'N(' not in content and '표준정규분포' not in content:
                warnings.append(f"해설 {solution['index']}: 정규분포에서 표준정규분포 언급 없음")
        
        if '분산' in content:
            if 'E(X)' not in content and 'V(X)' not in content:
                warnings.append(f"해설 {solution['index']}: 분산에서 기댓값 언급 없음")
        
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
    print("확통_2024학년도_현우진_드릴_P6_해설 변환")
    print("=" * 80)
    
    # 해설 추출
    solutions = extract_solutions_from_latex(latex_content)
    
    print(f"\n📊 총 {len(solutions)}개 해설 추출 완료\n")
    
    # 검토
    is_valid = review_solutions(solutions)
    
    # 문제 파일과 비교
    base_dir = Path(r'C:\Users\a\Documents\MathPDF\organized\현우진\확통_2005학년도_현우진_드릴')
    problems_path = base_dir / '확통_2024학년도_현우진_드릴_P6_문제_deepseek.json'
    compare_with_problems(solutions, problems_path)
    
    # 저장
    base_filename = '확통_2024학년도_현우진_드릴_P6_해설'
    
    if is_valid or len(solutions) > 0:
        save_for_deepseek(solutions, base_dir, base_filename)
        print(f"\n✅ 저장 완료: {base_dir}")
    else:
        print("\n❌ 검토 실패")

if __name__ == '__main__':
    main()
