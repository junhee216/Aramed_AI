# convert_haktong_p7_solution_deepseek.py
# 확통_2024학년도_현우진_드릴_P7_해설 LaTeX → 딥시크용 마크다운 변환

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
\usepackage{fvextra, csquotes}
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

\newunicodechar{⋯}{\ifmmode\cdots\else{$\cdots$}\fi}
\newunicodechar{⇒}{\ifmmode\Rightarrow\else{$\Rightarrow$}\fi}

\begin{document}
\section*{Comment}
\section*{Drill 표준편차가 같은 두 정규분포}
두 정규분포의 표준편차가 서로 다를 때 확률밀도함수의 최댓값의 대소 이외에 그래프 사이의 일반적인 기하적 관점은 없다보니, 두 정규분포의 확률밀도함수의 그래프 사이의 기하적 관점을 필요로 한다면 표준편차가 같은 경우가 대부분이다.\\
앞의 문제에서도 표준편차가 같은 두 정규분포가 등장하므로 확률밀도함수의 그래프의 합동, 대칭을 바탕으로 한 기하적 관점을 이용할 준비를 해야 한다.

\section*{Drill 확률밀도함수의 그래프의 합동과 대칭}
앞의 문제에서 방정식 $|f(x)-g(x)|=f(x)+g(x)-2 g(6)$ 의 실근을 함수 $y=\frac{f(x)+g(x)-|f(x)-g(x)|}{2}$ 의 그래프와 직선 $y=g(6)$ 의 교점의 $x$ 좌표로 다루겠다는 생각은 보자마자 할 수 있을 듯. 함수 $y=\frac{f(x)+g(x)-|f(x)-g(x)|}{2}$ 의 식을 정리하고 나면 두 정규분포 각각의 평균 $m_{1}, m_{2}$ 의 대소에 따라 케이스를 구분하고 확률밀도함수의 그래프의 합동과 대칭을 감안하여 적절한 상황을 확정하면 된다.

\section*{Drill 표준편차가 같은 두 정규분포의 확률밀도함수의 그래프의 교점의 개수}
앞의 문제에서 $h(t)$ 는 합동인 두 확률밀도함수 $y=f(x), y=g(x)$ 의 그래프와 직선 $y=t$ 의 서로 다른 교점의 개수이다. 평균 $m_{1}, m_{2}$ 가 서로 다르다는 것은 슥 확인해보면 되고, $h(t)$ 의 값은 $0,2,3,4$ 로 딱 정해진다. $h(f(2))<h(f(4))<h(g(4))$ 에서 $h(f(2)), h(f(4))$, $h(g(4))$ 의 값은 뚝딱 확정. $h(t)$ 의 값이 2,3 인 것이 특수한 경우이므로 이를 이용하여 두 확률밀도함수의 그래프의 기하적 관계를 정리하면 된다. 표준편차가 같은 두 정규분포의 평균이 서로 다를 때, 확률밀도함수의 그래프는 오직 한 점에서 만난다는 것에도 은근히 주의할 필요가 있다.

\section*{Drill 실전적인 태도}
앞의 문제는 충분한 근거로 논리적으로 풀어나가려 하면 만만치 않지만 실전에서는 그러지 말아야⋯ 적당한 선에서 기하적 상황을 짐작해보고 이 짐작에 따라 별다른 모순 없이 순조 롭게 결론에 다다르면 이 결론이 모든 조건을 만족시키는지 확인하는 정도로 마무리하는 것이 좋다.\\
$k$ 가 $2 p$ 이하의 자연수일 때 $f(k)$ 의 서로 다른 값의 개수가 $k$ 가 $p$ 이하의 자연수일 때 $f(k)$ 의 서로 다른 값의 개수보다 1 만큼 큰 $p$ 를 작은 수부터 크기순으로 나열한 것이 $\alpha, \beta$, $\gamma$ 라는 것. 정규분포의 확률밀도함수 $y=f(x)$ 의 그래프가 직선 $x=m$ 에 대하여 대칭이고 이 그래프의 $x>0$ 인 부분만 취급한다. 정수 $m$ 의 값을 0 근처에서 조금만 조절해보면 $m$ 의 기본적인 값의 범위는 어렵지 않게 정할 수 있고, 동시에 $\alpha=1$ 인 것도 알 수 있다.\\
$\beta+\gamma=17$ 이 되도록 $\beta, \gamma$ 의 값을 마저 정하면 되는데, 순서쌍 $(\beta, \gamma)$ 를 모두 나열해본다고 해도 기껏해야 7 개뿐이다. 순서쌍 $(\beta, \gamma)$ 가 $(2,15)$ 인 경우부터 $m$ 의 값을 조절해보면 $\beta, \gamma$ 의 차가 너무 크면 안 되겠다는 느낌이 팍 온다. 그렇다먼 쪽 넘어가서 순서쌍 $(\beta, \gamma)$ 가 $(8,9)$ 인 경우부터 $m$ 의 값을 조절해보는 것이 어떨까?

\section*{Drill 표본평균 $\bar{X}$ 의 평균, 분산, 표준편차}
모평균이 $m$ 이고 모표준편차가 $\sigma$ 인 모집단에서 크기가 $n$ 인 표본을 임의추출할 때, 표본평균 $\bar{X}$ 에 대하여

$$
\mathrm{E}(\bar{X})=m, \quad \mathrm{~V}(\bar{X})=\frac{\sigma^{2}}{n}, \quad \sigma(\bar{X})=\frac{\sigma}{\sqrt{n}}
$$

표본평균 $\bar{X}$ 의 분산 $\mathrm{V}(\bar{X})$ 의 값을 구하는 방법은 다음과 같이 나누어볼 수 있다.\\
(1) $\mathrm{V}(\bar{X})=\frac{\mathrm{V}(X)}{n}$\\
(2) $\mathrm{V}(\bar{X})=\mathrm{E}\left(\bar{X}^{2}\right)-\{\mathrm{E}(\bar{X})\}^{2}$

\section*{Comment}
\section*{Drill. 1 임의추출과 복원추출, 비복원추출}
모집단에서 표본을 추출할 때, 한 개의 자료를 추출한 후 되돌려 놓고 다시 추출하는 것을 복원추출이라고 하는데 이러한 복원추출은 임의추출이다. 한편, 한 개의 자료를 추출한 후 되돌려 놓지 않고 다시 추출하는 것을 비복원추출이라고 하는데 모집단의 크기가 충분히 크거나 표본의 크기가 충분히 큰 경우에는 비복원추출도 임의추출로 보고 복원추출과 구분 하지 않는다. 특별한 언급이 없으면 임의추출은 복원추출로 생각한다.

\begin{displayquote}
크기가 작은 모집단에서 크기가 작은 표본의 임의추출\\
⇒ 복원추출(중복순열)\\
정규분포를 따르는(크기가 충분히 큰) 모집단에서 임의추출\\
⇒ 복원추출, 비복원추출을 구분하지 않는다.\\
크기가 충분히 큰 표본의 임의추출\\
⇒ 복원추출, 비복원추출을 구분하지 않는다.
\end{displayquote}

앞의 문제는 '표본', '추출' 등의 용어는 사용하지 않았지만 자료를 추출한 후 되돌려 놓고 다시 추출하는 복원추출의 상황이고 표본평균의 기호 $\bar{X}$ 가 등장하기도 하므로 친숙한 $\bar{X}$ 에 관한 확률로 다루면 된다.\\[0pt]
[예] 1 부터 3 까지의 자연수가 하나씩 적혀 있는 3 장의 카드를 모집단으로 했을 때, 임의추출한 크기가 2 인 모든 표본을 순서쌍으로 나타내면 다음과 같다.\\
$(1,1),(1,2),(1,3)$,\\
$(2,1),(2,2),(2,3)$,\\
$(3,1),(3,2),(3,3)$\\
크기가 작은 모집단에서 크기가 작은 표본을 임의추출한 것이고 특별한 언급이 없으므로 복원추출로 생각해야 한다. 따라서 중복순열의 관점에서 $(1,2)$ 와 $(2,1),(2,3)$ 과 $(3,2)$ 등은 서로 다른 표본이고, 표본을 임의추출하는 경우의 수는 $3 \times 3=9$ 이다.

Drill. $2 \bar{X}=a$ 일 확률\\
$\mathrm{P}(\bar{X}=a)$ 의 값은 $\bar{X}$ 의 값이 $a$ 가 되는 모든 경우에 대하여 확률의 곱셈정리와 덧셈정리를 이용하여 계산한다. 예를 들어 모집단의 확률변수 $X$ 의 값이 $1,3,5$ 이고, 크기가 2 인 표본을 복원추출할 때

$$
\mathrm{P}(\bar{X}=3)=\mathrm{P}(X=1) \mathrm{P}(X=5)+\mathrm{P}(X=3) \mathrm{P}(X=3)+\mathrm{P}(X=5) \mathrm{P}(X=1)
$$

\section*{Drill. 1 표본평균 $\bar{X}$ 의 분포}
모평균이 $m$ 이고 모표준편차가 $\sigma$ 인 모집단에서 크기가 $n$ 인 표본을 임의추출할 때, 표본평균 $\bar{X}$ 에 대하여 모집단의 분포가 정규분포이면 $\bar{X}$ 는 $n$ 의 크기에 관계없이 정규분포 $\mathrm{N}\left(m, \frac{\sigma^{2}}{n}\right)$ 을 따른다.

모집단의 분포가 정규분포가 아닐 때에도 $n$ 이 충분히 크면 $\bar{X}$ 의 분포는 근사적으로 정규분포 $\mathrm{N}\left(m, \frac{\sigma^{2}}{n}\right)$ 을 따른다.

\section*{Drill. $2 \bar{X}$ 의 범위에 관한 확률}
$\bar{X}$ 의 범위에 관한 확률은 정규분포 $\mathrm{N}\left(m, \frac{\sigma^{2}}{n}\right)$ 을 따르므로

$$
Z=\frac{\bar{X}-m}{\frac{\sigma}{\sqrt{n}}}
$$

으로 표준화하고 표준정규분포표를 이용하여 계산한다.

\section*{Drill 모평균의 추정}
정규분포 $\mathrm{N}\left(m, \sigma^{2}\right)$ 을 따르는 모집단에서 크기가 $n$ 인 표본을 임의추출하여 구한 표본평균이 $\bar{X}$ 이면 모평균 $m$ 에 대한 신뢰구간은

신뢰도 $95 \%$ 일 때 $\left[\bar{X}-1.96 \frac{\sigma}{\sqrt{n}}, \bar{X}+1.96 \frac{\sigma}{\sqrt{n}}\right]$\\
신뢰도 $99 \%$ 일 때 $\left[\bar{X}-2.58 \frac{\sigma}{\sqrt{n}}, \bar{X}+2.58 \frac{\sigma}{\sqrt{n}}\right]$

\begin{center}
\begin{tabular}{c|c}
\hline
$z$ & $\mathrm{P}(0 \leq Z \leq z)$ \\
\hline
1.96 & 0.475 \\
\hline
2.58 & 0.495 \\
\hline
\end{tabular}
\end{center}

[참고] 그림의 (1)과 같이 $m-1.96 \times \frac{\sigma}{\sqrt{n}} \leq \bar{X} \leq m+1.96 \times \frac{\sigma}{\sqrt{n}}$ 이면 구간 $\left[\bar{X}-1.96 \times \frac{\sigma}{\sqrt{n}}, \bar{X}+1.96 \times \frac{\sigma}{\sqrt{n}}\right]$ 에 모평균이 포함되고, 그림의 (2)와 같이 $\bar{X}<m-1.96 \times \frac{\sigma}{\sqrt{n}}$ 또는 $\bar{X}>m+1.96 \times \frac{\sigma}{\sqrt{n}}$ 이면 구간 $\left[\bar{X}-1.96 \times \frac{\sigma}{\sqrt{n}}, \bar{X}+1.96 \times \frac{\sigma}{\sqrt{n}}\right]$ 에 모평균이 포함되지 않는다. 따라서 구간 $\left[\bar{X}-1.96 \times \frac{\sigma}{\sqrt{n}}, \bar{X}+1.96 \times \frac{\sigma}{\sqrt{n}}\right]$ 에 모평균이 포함된다고 추정할 때 $\mathrm{P}\left(m-1.96 \times \frac{\sigma}{\sqrt{n}} \leq \bar{X} \leq m+1.96 \times \frac{\sigma}{\sqrt{n}}\right)=\mathrm{P}(-1.96 \leq Z \leq 1.96)=0.95$ 이므로 이 추정이 맞을 확률은 $95 \%$ 이다.\\
\includegraphics[max width=\textwidth, center]{1ac38584-f903-4169-b897-fea39e9691b4-8_357_804_1764_931}

\section*{Drill. 1 신뢰상수}
신뢰도 $95 \%$ 의 신뢰구간에서 1.96 은 표준정규분포표에서 확률 $0.95 \times \frac{1}{2}=0.475$ 에 대응하는 $z$ 의 값이고, 신뢰도 $99 \%$ 의 신뢰구간에서 2.58 은 표준정규분포표에서 확률

\begin{center}
\begin{tabular}{c|c}
\hline
$z$ & $\mathrm{P}(0 \leq Z \leq z)$ \\
\hline
1.96 & 0.475 \\
\hline
2.58 & 0.495 \\
\hline
\end{tabular}
\end{center}

$0.99 \times \frac{1}{2}=0.495$ 에 대응하는 $z$ 의 값이다.

이러한 $z$ 의 값을 신뢰상수라고도 부르는데 신뢰도 $\alpha \%$ 일 때 신뢰상수 $k$ 는 표준정규분포표에서

확률 $\frac{\alpha}{100} \times \frac{1}{2}=\frac{\alpha}{200}$ 에 대응하는 $z$ 의 값

\begin{center}
\begin{tabular}{c|c}
\hline
$z$ & $\mathrm{P}(0 \leq Z \leq z)$ \\
\hline
$k$ & $\frac{\alpha}{200}$ \\
\hline
\end{tabular}
\end{center}

이다.

\section*{Drill. 2 신뢰구간과 표본평균}
모평균의 추정에 관한 문제에서 신뢰구간이 주어질 때는 표본평균이 주어진 것으로 이용할 수 있어야 한다.

모평균 $m$ 에 대한 신뢰구간이 $a \leq m \leq b$ 이면 표본평균 $\bar{X}=\frac{a+b}{2}$


\end{document}"""

def latex_to_markdown(latex_text):
    """LaTeX를 마크다운으로 변환 (더 정확한 변환)"""
    text = latex_text
    
    # 문서 구조 제거 (더 정확하게)
    text = re.sub(r'\\begin\{document\}.*?', '', text, flags=re.DOTALL)
    text = re.sub(r'\\end\{document\}.*?', '', text, flags=re.DOTALL)
    
    # 섹션 헤더 변환
    def replace_section(match):
        title = match.group(1)
        return f'\n## {title}\n'
    text = re.sub(r'\\section\*\{([^}]+)\}', replace_section, text)
    
    # 수식 블록 ($$ ... $$)
    def replace_display_math(match):
        math_content = match.group(1)
        # 내부 명령어 정리
        math_content = re.sub(r'\\mathrm\{([^}]+)\}', r'\1', math_content)
        math_content = re.sub(r'\\left\(', '(', math_content)
        math_content = re.sub(r'\\right\)', ')', math_content)
        math_content = re.sub(r'\\left\[', '[', math_content)
        math_content = re.sub(r'\\right\]', ']', math_content)
        return f'\n```math\n{math_content}\n```\n'
    text = re.sub(r'\$\$([^$]+)\$\$', replace_display_math, text)
    
    # 인라인 수식 ($ ... $) - 더 신중하게
    def replace_inline_math(match):
        math_content = match.group(1)
        # 기본 수학 명령어 변환
        math_content = re.sub(r'\\mathrm\{([^}]+)\}', r'\1', math_content)
        math_content = re.sub(r'\\bar\{([^}]+)\}', r'\\bar{\\1}', math_content)
        return f'${math_content}$'
    text = re.sub(r'\$([^$]+)\$', replace_inline_math, text)
    
    # 수학 명령어 (인라인 수식 외부에서도)
    text = re.sub(r'\\mathrm\{([^}]+)\}', r'\1', text)
    text = re.sub(r'\\text\{([^}]+)\}', r'\1', text)
    text = re.sub(r'\\bar\{([^}]+)\}', r'$\\bar{\\1}$', text)
    text = re.sub(r'\\frac\{([^}]+)\}\{([^}]+)\}', r'$\\frac{\\1}{\\2}$', text)
    text = re.sub(r'\\sqrt\{([^}]+)\}', r'$\\sqrt{\\1}$', text)
    text = re.sub(r'\\sigma\b', r'$\\sigma$', text)
    text = re.sub(r'\\alpha\b', r'$\\alpha$', text)
    text = re.sub(r'\\beta\b', r'$\\beta$', text)
    text = re.sub(r'\\gamma\b', r'$\\gamma$', text)
    text = re.sub(r'\\leq\b', r'$\\leq$', text)
    text = re.sub(r'\\geq\b', r'$\\geq$', text)
    text = re.sub(r'\\times\b', r'$\\times$', text)
    text = re.sub(r'\\cdots\b', r'$\\cdots$', text)
    text = re.sub(r'\\Rightarrow\b', r'$\\Rightarrow$', text)
    
    # 괄호 명령어
    text = re.sub(r'\\left\(', '(', text)
    text = re.sub(r'\\right\)', ')', text)
    text = re.sub(r'\\left\[', '[', text)
    text = re.sub(r'\\right\]', ']', text)
    text = re.sub(r'\\left\{', '{', text)
    text = re.sub(r'\\right\}', '}', text)
    
    # 줄바꿈
    text = re.sub(r'\\\\', '\n', text)
    text = re.sub(r'\\\[0pt\]', '\n', text)
    
    # 인용문
    def replace_quote(match):
        content = match.group(1)
        lines = content.split('\n')
        quoted = '\n'.join(f'> {line}' if line.strip() else '' for line in lines)
        return f'\n{quoted}\n'
    text = re.sub(r'\\begin\{displayquote\}(.*?)\\end\{displayquote\}', replace_quote, text, flags=re.DOTALL)
    
    # 표 변환
    def replace_table(match):
        table_content = match.group(1)
        lines = table_content.split('\n')
        result = []
        for line in lines:
            if '\\hline' in line:
                result.append('| --- | --- |')
            elif '&' in line:
                cells = [cell.strip() for cell in line.split('&')]
                result.append('| ' + ' | '.join(cells) + ' |')
        return '\n' + '\n'.join(result) + '\n'
    text = re.sub(r'\\begin\{center\}.*?\\begin\{tabular\}\{([^}]+)\}(.*?)\\end\{tabular\}.*?\\end\{center\}', replace_table, text, flags=re.DOTALL)
    
    # 이미지
    text = re.sub(r'\\includegraphics\[[^\]]*\]\{([^}]+)\}', r'![이미지](\\1)', text)
    
    # 기타 정리
    text = re.sub(r'\\%', '%', text)
    text = re.sub(r'\{([^}]+)\}', r'\1', text)  # 남은 단순 중괄호 제거
    text = re.sub(r'\s+', ' ', text)  # 연속 공백
    text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)  # 연속 줄바꿈
    
    return text.strip()

def extract_solutions(latex_content):
    """해설 섹션 추출"""
    solutions = []
    
    # \begin{document} 이후만 추출
    doc_match = re.search(r'\\begin\{document\}(.*?)\\end\{document\}', latex_content, re.DOTALL)
    if not doc_match:
        return solutions
    
    body = doc_match.group(1)
    
    # 섹션별로 분리
    pattern = r'\\section\*\{([^}]+)\}(.*?)(?=\\section\*\{|$)'
    matches = re.finditer(pattern, body, re.DOTALL)
    
    for match in matches:
        title = match.group(1).strip()
        content = match.group(2).strip()
        
        if content:
            solutions.append({
                'title': title,
                'content': content
            })
    
    return solutions

def main():
    print("=" * 80)
    print("확통_2024학년도_현우진_드릴_P7_해설 변환")
    print("=" * 80)
    
    # 해설 추출
    solutions = extract_solutions(latex_content)
    
    # 마크다운 변환
    markdown_solutions = []
    for sol in solutions:
        markdown_content = latex_to_markdown(sol['content'])
        markdown_solutions.append({
            'title': sol['title'],
            'content': markdown_content
        })
    
    # 전체 마크다운 생성
    full_markdown = "# 확통_2024학년도_현우진_드릴_P7_해설\n\n"
    for sol in markdown_solutions:
        full_markdown += f"## {sol['title']}\n\n{sol['content']}\n\n"
    
    # 저장 경로
    base_dir = Path(r'C:\Users\a\Documents\MathPDF\organized\현우진\확통_2024학년도_현우진_드릴')
    base_dir.mkdir(parents=True, exist_ok=True)
    
    # 마크다운 저장
    md_path = base_dir / "확통_2024학년도_현우진_드릴_P7_해설_deepseek.md"
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(full_markdown)
    
    # JSON 저장
    json_path = base_dir / "확통_2024학년도_현우진_드릴_P7_해설_deepseek.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(markdown_solutions, f, ensure_ascii=False, indent=2)
    
    print(f"\n[저장 완료]")
    print(f"  - 마크다운: {md_path}")
    print(f"  - JSON: {json_path}")
    print(f"\n총 {len(markdown_solutions)}개 섹션 변환 완료")

if __name__ == '__main__':
    main()
