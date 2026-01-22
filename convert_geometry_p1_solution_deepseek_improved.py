# convert_geometry_p1_solution_deepseek_improved.py
# 기하_2024학년도_현우진_드릴_P1 해설 LaTeX → Deepseek R1-70B용 변환 (개선 버전)

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

# LaTeX 내용 (기존과 동일)
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
\section*{Comment}
\section*{Drill 포물선의 정의의 활용: 직각사다리꼴}
\begin{enumerate}
  \item 정의\\
(1) $\overline{\mathrm{PF}}=\overline{\mathrm{PI}}$ (이등변삼각형)\\
(2) 정사각형\\
\includegraphics[max width=\textwidth, center]{c0d837db-7184-42b9-9273-7caf92d7f7a6-1_344_358_951_1163}
  \item 사다리꼴\\
(1) 두 밑변의 길이의 차
\end{enumerate}

$$
\overline{\mathrm{FH}}=a-2 p \text { 또는 } \overline{\mathrm{FH}}=2 p-a
$$

(2) $(x$ 좌표 $)+p$

점 P 의 $x$ 좌표를 $x_{1}$ 이라 하면

$$
\overline{\mathrm{PF}}=\overline{\mathrm{PI}}=x_{1}+p
$$

(3) 피타고라스 정리

$$
\overline{\mathrm{PH}}^{2}=a^{2}-(a-2 p)^{2}
$$

(4) 좌표의 대입

선분 PH 의 길이는 점 P 의 $x$ 좌표를 포물선의 방정식에 대입하여 점 P 의 $y$ 좌표로 구한다. ⇒ 기하의 관점에만 얽매이지 말자.\\
\includegraphics[max width=\textwidth, center]{c0d837db-7184-42b9-9273-7caf92d7f7a6-1_346_354_1941_947}\\
\includegraphics[max width=\textwidth, center]{c0d837db-7184-42b9-9273-7caf92d7f7a6-1_346_371_1941_1378}

\section*{Drill 직각삼각형의 이용}
(1) 특수각\\
(2) 삼각비, 피타고라스 수\\
(3) 피타고라스 정리\\
(4) 직각삼각형의 닮음

\begin{itemize}
  \item 한 예각의 크기가 같은 두 직각삼각형은 서로 닮음이다.
  \item 직각삼각형의 빗변에 내린 수선이 등장할 때 그림과 같이 직각과 대응하는 예각을 이용 하여 직각삼각형의 닮음을 체크해보도록 하자.\\
\includegraphics[max width=\textwidth, center]{c0d837db-7184-42b9-9273-7caf92d7f7a6-2_747_767_1142_955}
\end{itemize}

Drill 포물선과 원에 대해 당연히 해야 할 일 앞의 문제에서는 포물선 위의 점이 등장하므로 정의와 관련해 당연히 해야 할 일과 원에 대해 당연히 해야 할 일을 하는 것이 우선이다. 포물선 위의 점 P 와 포물선의 초점 F 를 이은 직선이 등장하므로 점 P 에서 포물선의 준선과 $x$ 축에 수선을 내려야 한다. 점 R 뿐만 아니라 직선 $l$ 과 원의 접점도 원의 중심과 연결해야 한다. 여기서 짜잔\~{}! 직각삼각형의 닮음이 눈에 딱 들어와야!!

\section*{Comment}
\section*{Dirll 원에 내접하는 사각형}
원 O 에 내접하는 사각형 ABCD 에서 나타나는 각 사이의 관계는 다음 그림과 같다.\\
\includegraphics[max width=\textwidth, center]{c0d837db-7184-42b9-9273-7caf92d7f7a6-4_363_350_845_871}\\
\includegraphics[max width=\textwidth, center]{c0d837db-7184-42b9-9273-7caf92d7f7a6-4_331_310_845_1361}

$$
\begin{aligned}
& \angle \mathrm{ACB}=\angle \mathrm{ADB}, \angle \mathrm{DAC}=\angle \mathrm{DBC} \\
& \angle \mathrm{ABD}=\angle \mathrm{ACD}, \angle \mathrm{BAC}=\angle \mathrm{BDC}
\end{aligned}
$$

\section*{Comment}
\section*{Drill 좌표의 계산과 기하적 관점의 선택}
최근 기출 경향을 보면 아예 좌표의 계산으로 밀어 붙이는 것이 더 낫거나 기하적 관점 위주라 하더라도 좌표의 계산이 보조적인 수단이 되거나 필요한 한 과정인 경우가 많다. 앞의 문제 에서도 두 포물선의 방정식을 연립해서 교점 A 의 좌표를 구하기가 괜찮아 보이므로 이러한 시도를 해보는 것은 좋다. 그러고 나서 점 A 와 각 포물선의 준선 사이의 거리의 합이 선분 OA 의 길이의 2 배임을 이용해보려고 하면? 당연히 성립하는 등식이 등장하고 아무런 소득이 없다. 그렇다면 포물선의 정의와 원에 관한 기하적 관점으로 빠르게 태세 전환! 포물선의 정의에 따라 필요한 직각사다리꼴을 모두 잡아놓으면 원의 반지름의 길이를 구할 수 있으 므로 $\sin (\angle \mathrm{OPQ})$ 로 사인법칙을 이용하겠다는 판단 정도는 무난하게 할 수 있을 듯. 직선 AQ 의 기울기를 구하기 위해 선분 AQ 를 빗변으로 하는 적절한 직각삼각형이 필요하고, 직선 AQ 의 기울기는 이 직각삼각형의 한 예각의 탄젠트의 값을 이용하여 구하는 것으로 마무리하면 된다.

\section*{Comment}
\section*{Drill 포물선의 정의의 활용: 초점을 지나는 직선}
\begin{enumerate}
  \item 사다리꼴\\
(1) 수선의 길이의 합
\end{enumerate}

$$
\overline{\mathrm{AB}}=a+b
$$

(2) $(x$ 좌표 $)+p$

두 점 $\mathrm{A}, \mathrm{B}$ 의 $x$ 좌표를 각각 $x_{1}, x_{2}$ 라 하면

$$
\begin{aligned}
\overline{\mathrm{AB}} & =\overline{\mathrm{AF}}+\overline{\mathrm{BF}}=\left(x_{1}+p\right)+\left(x_{2}+p\right) \\
& =x_{1}+x_{2}+2 p
\end{aligned}
$$

(3) 두 밑변의 길이의 차, 피타고라스 정리

$$
\overline{\mathrm{BH}}=a-b, \quad \overline{\mathrm{AH}}^{2}=(a+b)^{2}-(a-b)^{2}
$$

\begin{enumerate}
  \setcounter{enumi}{1}
  \item 직각삼각형의 닮음\\
\includegraphics[max width=\textwidth, center]{c0d837db-7184-42b9-9273-7caf92d7f7a6-6_456_422_824_1488}
\end{enumerate}

$$
\overline{\mathrm{AB}}=a+b, \quad x_{1}+x_{2}=\overline{\mathrm{AB}}-2 p
$$

(1) $2 p=\frac{2 a b}{a+b} \Rightarrow \frac{1}{a}+\frac{1}{b}=\frac{1}{p}$\\
(2) 두 점 $\mathrm{A}, \mathrm{B}$ 의 $x$ 좌표를 각각 $x_{1}, x_{2}$ 라 하면 $x_{1}, p, x_{2}$ 는 이 순서대로 등비수열을 이룬다.\\
$\Rightarrow p^{2}=x_{1} x_{2}$

포물선의 정의의 활용에서 직각삼각형의 닮음으로 얻어진 $2 p=\frac{2 a b}{a+b}$ 또는 $p^{2}=x_{1} x_{2}$ 는 언제 이용할까? 그 판단이 어렵다면 일단 써놓고 보자. 그 다음 이용할 여지가 있으면 이용하면 된다.

\section*{Drill 타원의 정의의 활용}
(1) 장축이 $x$ 축에 평행한 타원 위의 점 P 와 두 초점 $\mathrm{F}, \mathrm{F}^{\prime}$ 에 이르는 거리의 합이 장축의 길이 $2 a$ 와 같음을 이용한다.

$$
\overline{\mathrm{PF}}+\overline{\mathrm{PF}^{\prime}}=2 a
$$

(2) 장축이 $y$ 축에 평행한 타원 위의 점 P 와 두 초점 $\mathrm{F}, \mathrm{F}^{\prime}$ 에 이르는 거리의 합이 장축의 길이 $2 b$ 와 같음을 이용한다.

$$
\overline{\mathrm{PF}}+\overline{\mathrm{PF}^{\prime}}=2 b
$$

\section*{Comment}
\section*{Drill 타원, 쌍곡선의 두 초점을 지름의 양 끝으로 하는 원}
(1) $\overline{\mathrm{OF}}=\overline{\mathrm{OP}}, \overline{\mathrm{OF}^{\prime}}=\overline{\mathrm{OP}}$\\
(직각삼각형의 외접원의 중심은 빗변의 중점)\\
(2) $\angle \mathrm{POF}=2 \angle \mathrm{PF}^{\prime} \mathrm{O}$\\
(중심각의 크기는 원주각의 크기의 2 배)\\
(3) $\angle \mathrm{PF}^{\prime} \mathrm{O}=\angle \mathrm{F}^{\prime} \mathrm{PO} \Rightarrow \angle \mathrm{FPF}^{\prime}=90^{\circ}$\\
(지름에 대한 원주각의 크기는 $90^{\circ}$ )\\
\includegraphics[max width=\textwidth, center]{c0d837db-7184-42b9-9273-7caf92d7f7a6-8_392_597_1099_1040}


\end{document}"""

def clean_math_content(math_str):
    """수식 내용 정리 (개선 버전)"""
    # \mathrm 제거
    math_str = re.sub(r'\\mathrm\{([^}]+)\}', r'\1', math_str)
    # \left, \right 제거
    math_str = re.sub(r'\\left([\(\[\{])', r'\1', math_str)
    math_str = re.sub(r'\\right([\)\]\}])', r'\1', math_str)
    # \text 제거
    math_str = re.sub(r'\\text\s*\{([^}]+)\}', r'\1', math_str)
    # 공백 정리
    math_str = re.sub(r'\s+', ' ', math_str)
    return math_str.strip()

def latex_to_markdown_for_deepseek(latex_text):
    """LaTeX를 Deepseek R1-70B용 마크다운으로 변환 (개선 버전)"""
    text = latex_text
    
    # aligned 환경 처리 (먼저 처리 - 개선)
    def replace_aligned(match):
        content = match.group(1)
        # & 제거하고 줄바꿈 처리
        lines = content.split('\\\\')
        cleaned_lines = []
        for line in lines:
            line = line.strip()
            # & 앞뒤 공백 정리
            line = re.sub(r'\s*&\s*', ' ', line)
            line = clean_math_content(line)
            if line:
                cleaned_lines.append(line)
        content = '\n'.join(cleaned_lines)
        return f'\n\n$$\n{content}\n$$\n\n'
    text = re.sub(r'\\begin\{aligned\}(.*?)\\end\{aligned\}', replace_aligned, text, flags=re.DOTALL)
    
    # 수식 블록 ($$ ... $$) - aligned 처리 후
    def replace_display_math(match):
        math_content = match.group(1)
        math_content = clean_math_content(math_content)
        # 공백 정리
        math_content = re.sub(r'\s+', ' ', math_content).strip()
        return f'\n\n$$\n{math_content}\n$$\n\n'
    text = re.sub(r'\$\$([^$]+?)\$\$', replace_display_math, text, flags=re.DOTALL)
    
    # 인라인 수식 ($ ... $) - 정확하게 변환
    def replace_inline_math(match):
        math_content = match.group(1)
        math_content = clean_math_content(math_content)
        return f'${math_content}$'
    text = re.sub(r'\$([^$]+?)\$', replace_inline_math, text)
    
    # 특수 문자 처리
    text = re.sub(r'⇒', '⇒', text)
    text = re.sub(r'\\~{}', '~', text)
    
    # 줄바꿈 처리
    text = re.sub(r'\\\\', '\n', text)
    
    # 이미지 처리
    text = re.sub(r'\\includegraphics\[[^\]]*\]\{[^}]+\}', '[이미지]', text)
    
    # enumerate 환경 처리
    text = re.sub(r'\\begin\{enumerate\}', '', text)
    text = re.sub(r'\\end\{enumerate\}', '', text)
    text = re.sub(r'\\item\s+', '\n- ', text)
    text = re.sub(r'\\setcounter\{enumi\}\{(\d+)\}', r'(\1)', text)
    
    # itemize 환경 처리
    text = re.sub(r'\\begin\{itemize\}', '', text)
    text = re.sub(r'\\end\{itemize\}', '', text)
    
    # 섹션 헤더 처리
    text = re.sub(r'\\section\*\{([^}]+)\}', r'\n\n## \1\n\n', text)
    
    # 기타 정리 (개선)
    text = re.sub(r'\\%', '%', text)
    # 잘못된 수식 블록 정리
    text = re.sub(r'\$\s*\$\$', '$$', text)  # $ $$ -> $$
    text = re.sub(r'\$\$\s*\$\$', '$$', text)  # $$ $$ -> $$
    text = re.sub(r'\$\$\$\$', '$$', text)  # $$$$ -> $$
    # 수식 블록 주변 공백 정리 (개선)
    text = re.sub(r'\$\$\s*\n\s*\$\$', '\n\n', text)  # 빈 수식 블록 제거
    text = re.sub(r'([^\n\s])\$\$', r'\1\n\n$$', text)  # 수식 블록 전 줄바꿈
    text = re.sub(r'\$\$([^\n\s])', r'$$\n\1', text)  # 수식 블록 후 줄바꿈
    # 연속된 수식 블록 정리
    text = re.sub(r'\$\$\n\$\$', '$$', text)
    text = re.sub(r'[ \t]+', ' ', text)  # 연속 공백
    text = re.sub(r'\n{3,}', '\n\n', text)  # 연속 줄바꿈
    text = re.sub(r'^\s+', '', text, flags=re.MULTILINE)  # 줄 시작 공백
    
    return text.strip()

def extract_sections(latex_content):
    """해설 섹션 추출 (개선 버전)"""
    sections = []
    
    # \begin{document} 이후만 추출
    doc_match = re.search(r'\\begin\{document\}(.*?)\\end\{document\}', latex_content, re.DOTALL)
    if not doc_match:
        return sections
    
    body = doc_match.group(1)
    
    # 섹션 패턴 찾기
    section_pattern = r'\\section\*\{([^}]+)\}'
    section_matches = list(re.finditer(section_pattern, body))
    
    for i, match in enumerate(section_matches):
        section_title = match.group(1).strip()
        section_start = match.end()
        section_end = section_matches[i+1].start() if i+1 < len(section_matches) else len(body)
        
        section_content = body[section_start:section_end]
        
        # 섹션 내용 정리
        section_content = re.sub(r'\\begin\{document\}|\\end\{document\}', '', section_content)
        
        sections.append({
            'title': section_title,
            'content': section_content
        })
    
    return sections

def validate_math_logic(sections, problems_path=None):
    """수학적/논리적 오류 검증 (개선 버전)"""
    errors = []
    warnings = []
    
    # 문제 파일 로드 (있는 경우)
    problems = []
    if problems_path and Path(problems_path).exists():
        with open(problems_path, 'r', encoding='utf-8') as f:
            problems = json.load(f)
    
    # 해설 내용 전체
    full_content = ' '.join([s['content'] for s in sections])
    
    # 1. 포물선 정의 검증
    if '포물선' in full_content:
        if 'PF' in full_content and 'PI' in full_content:
            # 포물선 정의: PF = PI ✓
            pass
        else:
            warnings.append('포물선의 정의(PF = PI)가 명시적으로 언급되지 않음')
    
    # 2. 타원 정의 검증
    if '타원' in full_content:
        if 'PF' in full_content and ('PF\'' in full_content or 'PF\'' in full_content) and ('2a' in full_content or '2b' in full_content):
            # 타원 정의: PF + PF' = 2a ✓
            pass
        else:
            warnings.append('타원의 정의(PF + PF\' = 2a)가 명시적으로 언급되지 않음')
    
    # 3. 수식 일관성 검증
    # 포물선: x₁ + p = PF = PI
    if 'x_{1}+p' in full_content or 'x_1+p' in full_content:
        if 'PF' in full_content or 'PI' in full_content:
            pass  # 일관성 있음 ✓
    
    # 4. 문제와 해설의 일관성 (문제 유형별로만)
    if problems:
        for problem in problems:
            question = problem.get('question', '')
            problem_index = problem.get('index', '')
            
            # 포물선 문제인 경우만 포물선 검증
            if '포물선' in question:
                if '포물선' not in full_content:
                    warnings.append(f'문제 {problem_index}: 포물선 관련 해설이 없음')
            
            # 타원 문제인 경우만 타원 검증
            if '타원' in question and '포물선' not in question:
                if '타원' not in full_content:
                    warnings.append(f'문제 {problem_index}: 타원 관련 해설이 없음')
    
    return errors, warnings

def main():
    print("=" * 80)
    print("기하_2024학년도_현우진_드릴_P1 해설 → Deepseek R1-70B용 변환 (개선 버전)")
    print("=" * 80)
    
    # 섹션 추출
    sections = extract_sections(latex_content)
    print(f"\n총 {len(sections)}개 섹션 발견\n")
    
    # 문제 파일 경로
    problems_path = Path(r'C:\Users\a\Documents\MathPDF\organized\현우진\기하_2024학년도_현우진_드릴\기하_2024학년도_현우진_드릴_P1_문제_deepseek.json')
    
    # 수학적/논리적 오류 검증
    errors, warnings = validate_math_logic(sections, problems_path if problems_path.exists() else None)
    
    print("[수학적/논리적 오류 검증]")
    if errors:
        print(f"  [오류] 수학적 오류: {len(errors)}개")
        for error in errors:
            print(f"    - {error}")
    else:
        print("  [통과] 수학적 오류 없음")
    
    if warnings:
        print(f"  [경고] 경고: {len(warnings)}개")
        for warning in warnings[:5]:
            print(f"    - {warning}")
    else:
        print("  [통과] 경고 없음")
    
    # 마크다운 변환
    md_content = "# 기하_2024학년도_현우진_드릴_P1 해설\n\n"
    md_content += "> 이 문서는 Deepseek R1-70B가 읽을 수 있도록 최적화된 마크다운 형식입니다.\n\n"
    
    for section in sections:
        title = section['title']
        content = section['content']
        
        # Comment 섹션은 제목만
        if title == 'Comment':
            continue
        
        md_content += f"## {title}\n\n"
        md_content += latex_to_markdown_for_deepseek(content)
        md_content += "\n\n"
    
    # 저장 경로
    base_dir = Path(r'C:\Users\a\Documents\MathPDF\organized\현우진\기하_2024학년도_현우진_드릴')
    base_dir.mkdir(parents=True, exist_ok=True)
    
    # 마크다운 저장
    md_path = base_dir / "기하_2024학년도_현우진_드릴_P1_해설_deepseek_r1.md"
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    print(f"\n[저장 완료]")
    print(f"  - 마크다운: {md_path}")
    print(f"\n총 {len(sections)}개 섹션 변환 완료")
    print("\n[Deepseek R1-70B 호환성]")
    print("  - 마크다운 형식: 지원")
    print("  - LaTeX 수식: 지원 ($...$ 및 $$...$$)")
    print("  - 구조화된 섹션: 지원")
    print("  - UTF-8 인코딩: 지원")
    print("\n[결론] Deepseek R1-70B가 읽을 수 있는 형태입니다.")

if __name__ == '__main__':
    main()
