# convert_haktong_p4_solution_latex.py
# 확통_2024학년도_현우진_드릴_P4_해설 LaTeX 변환

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
\section*{Cornerre Orret}
Drill 경우의 수에 의한 확률의 계산\\
기본적으로 확률의 계산은 '경우의 수'와 '확률의 덧셈정리와 곱셈정리' 중 유리한 것의 선택 에서 출발한다. 경우의 수로 확률을 계산할 때의 기본 태도는 다음과 같다.\\
(1) 모든 대상은 같은 확률을 가지는 서로 다른 것으로 본다.\\
(2) 순서는 분모와 분자에 모두 고려하거나 모두 고려하지 않는다.\\
(3) 주어진 조건 이외의 경우의 수는 분모와 분자에서 모두 계산하거나 모두 계산하지 않는다.

\section*{Drill 함수의 대응 관계의 파악}
함수를 파악할 때 정의역의 원소와 공역의 원소 사이의 대응 관계를 그려보는 것이 도움이 될 때가 많다. 앞의 문제에서도 함수 $f$ 의 치역과 합성함수 $f \circ f$ 의 치역이 같다는 것의 의미를 대응 관계를 예를 들어 몇 개쯤 그려보고 파악하는 것이 좋다. 결론은 $f$ 의 치역과 $f \circ f$ 의 치역 사이가 일대일대응이어야 한다는 것! 그리고 조건 (나)를 만족시키려면 치역의 원소의 개수에 따라 케이스를 구분하고 각 케이스별로 $f(4)$ 의 값에 따라 다시 케이스를 구분해야 겠다는 판단은 자연스럽게 할 수 있을 듯.

\section*{Drill. 1 사건의 독립과 종속}
두 사건 $A, B$ 에 대하여 한 사건이 일어나는 것이 다른 사건이 일어날 확률에 아무런 영향을 주지 않을 때, 즉

$$
\mathrm{P}(B \mid A)=\mathrm{P}(B) \text { 또는 } \mathrm{P}(A \mid B)=\mathrm{P}(A)
$$

일 때, 두 사건 $A, B$ 는 서로 독립이라고 한다.\\
또, 두 사건이 서로 독립이 아닐 때, 두 사건은 서로 종속이라고 한다.

\section*{Drill. 2 사건의 독립의 확인 방법}
두 사건 $A, B$ 의 독립은\\
(1) 이중분할표에서 비의 일치\\
(2) $\mathrm{P}(A \cap B)=\mathrm{P}(A) \mathrm{P}(B)$

로 확인하는 것이 보통이지만 다음의 방법으로 확인할 수도 있다.\\
(3) $\mathrm{P}(A \mid B)=\mathrm{P}(A), \mathrm{P}(B \mid A)=\mathrm{P}(B)$

이들 중 어느 한 방법이 일반적으로 유리하다고 할 수 없으므로 상황에 따라 적절한 방법을 적용해보면 된다.

\section*{Comment}
\section*{Drill 독립시행}
동전 또는 주사위를 여러 번 던지는 경우와 같이 동일한 조건에서 어떤 시행을 되풀이할 때, 각 시행의 결과가 다른 시행의 결과에 영향을 주지 않는 경우, 즉 각 시행에서 일어나는 사건이 서로 독립이면 이런 시행을 독립시행이라고 한다.

매회의 시행에서 사건 $A$ 가 일어날 확률이 $p$ 로 일정할 때, $n$ 회의 독립시행에서 사건 $A$ 가 $r$ 회 일어날 확률은

$$
{ }_{n} \mathrm{C}_{r} p^{r}(1-p)^{n-r}(r=0,1,2, \cdots, n)
$$

이다. 여기서 ${ }_{n} \mathrm{C}_{r}$ 는 생각의 순서가 바뀌는 경우의 수이고 상황에 따라 ${ }_{n} \mathrm{C}_{r}$ 가 아닌 다른 경우의 수가 될 수도 있다. 이때는 확률의 곱셈정리에서의 생각의 순서가 바뀌는 경우의 수로 계산 하면 된다.

\section*{Comment}
\section*{Drill 독립시행의 상황 인지}
독립시행의 상황임을 인지하는 것이 매우 중요하다.\\
(1) 같은 시행의 $n$ 회 반복, $n$ 명에 대한 조사, $n$ 개에 대한 조사 등에서\\
(2) 주목하는 한 사건의 확률 $p$ (고정)

가 드러난다면 확실히 독립시행이다.\\
독립시행은 이항분포의 기초인데, 실전에서 독립시행과 이항분포임을 인지하지 못해 풀이의 방향을 잡지 못하는 일이 자주 벌어진다.

\section*{Comment}
\section*{Drill 조건부확률}
표본공간 $S$ 의 두 사건 $A, B$ 에 대하여 사건 $A$ 가 일어났을 때, 사건 $B$ 가 일어날 확률을 사건 $A$ 가 일어났을 때의 사건 $B$ 의 조건부확률이라고 하며, 이것을 기호로

$$
\mathrm{P}(B \mid A)
$$

와 같이 나타낸다.\\
\includegraphics[max width=\textwidth, center]{55e2a05b-ace4-49a4-9910-3243891bd87a-06_240_308_804_1597}\\
(1) $\mathrm{P}(B \mid A)=\frac{\mathrm{P}(A \cap B)}{\mathrm{P}(A)}=\frac{\frac{n(A \cap B)}{n(S)}}{\frac{n(A)}{n(S)}}=\frac{n(A \cap B)}{n(A)}($ 단, $\mathrm{P}(A)>0)$\\
(2) $\mathrm{P}\left(B^{C} \mid A\right)=1-\mathrm{P}(B \mid A)$

\section*{Comment}
Drill 조건부확률의 체크리스트\\
조건부확률을 다룰 때 다음 사항을 전반적으로 점검하도록 하자.\\
(1) 조건부확률의 상황임을 파악 (전사건이 주어지고 그 일부에 대해 다루면 표본공간을 축소)\\
(2) 경우의 수를 이용하여 계산할 것인지 확률을 이용하여 계산할 것인지 판단\\
(3) 분모의 케이스를 구분할 것인지 한 번에 다룰 것인지 또는 여사건을 이용할 것인지 판단\\
(4) 조건이 되는 사건의 발생 순서 구분 (조건이 되는 사건이 먼저 발생한다면 이 사건의 발생을 전제로 구하고자 하는 확률을 직접 계산)\\
(5) 경우의 수나 확률이 주어질 때 이중분할표 적극 활용 (수치화, 정량화의 수단)

\section*{Drill 조건부확률에서 여사건}
$\mathrm{P}(B \mid A)$ 는 여사건의 확률을 이용하여 $1-\mathrm{P}\left(B^{C} \mid A\right)$ 로 구할 수도 있다.\\
이때 $\mathrm{P}\left(B^{C} \mid A\right)=\frac{\mathrm{P}\left(A \cap B^{C}\right)}{\mathrm{P}(A)}$ 이므로 $\mathrm{P}\left(B^{C}\right)$ 이 아닌 $\mathrm{P}\left(A \cap B^{C}\right)$ 을 구해야 한다는 것,\\
즉 축소된 표본공간을 벗어나지 말아야 한다는 것에 주의하자.\\
앞의 문제는 여사건을 이용하는 것이 유리한 상황임을 금세 알 수 있을 것이다. 주어진 규칙에 따른 시행을 5 번 반복한 후 점 $\mathrm{P}_{5}$ 가 직선 $y=x$ 위에 있는 것으로 축소된 표본공간을 감안 하고, 네 점 $\mathrm{P}_{1}, \mathrm{P}_{2}, \mathrm{P}_{3}, \mathrm{P}_{4}$ 가 모두 직선 $y=x$ 위에 있지 않을 확률로 여사건의 확률을 구해야 한다.

\section*{Corrunnerat}
\section*{Drill 축소된 표본공간의 구성과 케이스 구분}
앞의 문제에서 함수 $f$ 의 역함수가 존재하지 않는다는 것의 의미는? 치역의 원소의 개수가 3 이하라는 것이다. 이와 함께 $f(1)+f(2)+f(3)$ 의 값이 3 의 배수가 되도록 하는 것이 축소된 표본공간을 구성하는 것이다. $f(1)+f(2)+f(3)$ 의 값이 $3,6,9,12$ 일 때로 케이스를 구분하고 각 케이스별로 $f(1) \leq f(2) \leq f(3) \leq f(4)$ 를 만족시키는 경우를 따져봐야 한다. 축소된 표본공간의 케이스를 구분하여 구성할 때는 보통 이 케이스들 중에서 조건부확률을 구하고자 하는 사건에 해당하는 경우의 수나 확률을 골라서 쓸 수 있게 된다.

\section*{Comment}
\section*{Drill. 1 축소된 표본공간의 케이스가 나누어질 때의 주의점}
조건부확률에서 축소된 표본공간의 케이스가 나누어질 때 이를 확률의 덧셈정리로 잘못 다루지 않도록 주의해야 한다. $\mathrm{P}(B \mid A)$ 에서 서로 배반인 두 사건 $A_{1}, A_{2}$ 에 대하여 $A=A_{1} \cup A_{2}$ 이고, 사건 $A_{1}$ 의 근원사건 중 사건 $B$ 에 해당하는 것으로 이루어진 사건을 $B_{1}$, 사건 $A_{2}$ 의 근원사건 중 사건 $B$ 에 해당하는 것으로 이루어진 사건을 $B_{2}$ 라 하면 $\mathrm{P}(B \mid A)=\frac{n\left(B_{1}\right)+n\left(B_{2}\right)}{n\left(A_{1}\right)+n\left(A_{2}\right)}$ 로 계산해야 한다.\\
$\mathrm{P}(B \mid A) \neq \frac{n\left(B_{1}\right)}{n\left(A_{1}\right)}+\frac{n\left(B_{2}\right)}{n\left(A_{2}\right)}$ 인 것에 주의하자.\\
앞의 문제에서 검은색을 칠한 카드의 개수는 3,4 로 나누어지는데, 각각의 경우의 수를 $a, b$ 라 하고, 각각 남은 조건을 만족시키는 경우의 수를 $c, d$ 라 하면 $\frac{c+d}{a+b}$ 로 계산해야 맞다. $\frac{c}{a}+\frac{d}{b}$ 로 계산하면 안 된다.

\section*{Drill. 2 상황의 대칭성의 인식}
앞의 문제에서 빨간색과 파란색을 각각 몇 개의 카드에 칠해야 하는지에 대한 조건은 딱히 없다. 두 조건 (가), (나)를 만족시키기만 하면 된다. 여기서 드는 생각! 빨간색을 칠한 카드의 개수와 파란색을 칠한 카드의 개수가 각각 $a, b$ 인 것과 각각 $b, a$ 인 것은 색깔만 서로 맞바꾸면 되는 같은 상황 아닐까? 이렇게 생각할 수 있다면 빨간색을 칠한 카드의 개수가 파란색을 칠한 카드의 개수보다 큰 것은 빨간색을 칠한 카드의 개수와 파란색을 칠한 카드의 개수가 다르다는 것에서 출발해서 단순하게 처리할 수 있다.


\end{document}"""

def extract_solutions_from_latex(latex_content):
    """LaTeX에서 해설 추출"""
    body = extract_body(latex_content)
    solutions = []
    
    # 섹션 헤더 찾기
    section_pattern = r'\\section\*\{([^}]+)\}'
    sections = list(re.finditer(section_pattern, body))
    
    print(f"📊 발견된 섹션: {len(sections)}개")
    
    # Comment/Corrunnerat/Cornerre Orret 섹션 찾기 (오타 포함)
    comment_sections = []
    for section in sections:
        section_text = section.group(1).strip()
        if 'Comment' in section_text or 'Corrunnerat' in section_text or 'Cornerre Orret' in section_text:
            comment_sections.append(section.start())
    
    print(f"📊 발견된 Comment 섹션: {len(comment_sections)}개")
    
    # Drill 섹션 추출
    seen_titles = set()
    is_strategy_mode = False  # Comment 이후의 Drill은 strategy
    
    for i, section in enumerate(sections):
        section_text = section.group(1).strip()
        
        # Comment/Corrunnerat/Cornerre Orret 섹션 확인
        if 'Comment' in section_text or 'Corrunnerat' in section_text or 'Cornerre Orret' in section_text:
            is_strategy_mode = True
            continue
        
        # Drill 섹션만 처리
        if not section_text.startswith('Drill'):
            continue
        
        # 섹션 제목 추출
        title = section_text.replace('Drill', '').strip()
        # "Drill. 1", "Drill. 2" 같은 번호 제거
        title = re.sub(r'^\.\s*\d+\s*', '', title).strip()
        
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
        if '독립시행' in content:
            if '이항분포' not in content and 'C_' not in content:
                warnings.append(f"해설 {solution['index']}: 독립시행에서 이항분포/조합 명시 없음")
        
        if '조건부확률' in content:
            if '표본공간' not in content and '근원사건' not in content:
                warnings.append(f"해설 {solution['index']}: 조건부확률에서 표본공간/근원사건 명시 없음")
        
        if '사건의 독립' in content or '독립' in content:
            if 'P(A ∩ B)' not in content and 'P(A)P(B)' not in content:
                warnings.append(f"해설 {solution['index']}: 사건의 독립에서 확률 곱셈정리 명시 없음")
        
        if '여사건' in content:
            if '축소된 표본공간' not in content and '표본공간' not in content:
                warnings.append(f"해설 {solution['index']}: 여사건에서 표본공간 명시 없음")
        
        if '함수' in content and '대응' in content:
            if '치역' not in content and '공역' not in content:
                warnings.append(f"해설 {solution['index']}: 함수의 대응 관계에서 치역/공역 명시 없음")
        
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
    print("확통_2024학년도_현우진_드릴_P4_해설 변환")
    print("=" * 80)
    
    # 해설 추출
    solutions = extract_solutions_from_latex(latex_content)
    
    print(f"\n📊 총 {len(solutions)}개 해설 추출 완료\n")
    
    # 검토
    is_valid = review_solutions(solutions)
    
    # 문제 파일과 비교
    base_dir = Path(r'C:\Users\a\Documents\MathPDF\organized\현우진\확통_2005학년도_현우진_드릴')
    problems_path = base_dir / '확통_2024학년도_현우진_드릴_P4_문제_deepseek.json'
    compare_with_problems(solutions, problems_path)
    
    # 저장
    base_filename = '확통_2024학년도_현우진_드릴_P4_해설'
    
    if is_valid or len(solutions) > 0:
        save_for_deepseek(solutions, base_dir, base_filename)
        print(f"\n✅ 저장 완료: {base_dir}")
    else:
        print("\n❌ 검토 실패")

if __name__ == '__main__':
    main()
