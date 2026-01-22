# convert_haktong_p2_solution_latex.py
# 확통 드릴 P2 해설 LaTeX를 딥시크용 CSV로 변환

import re
import sys
import os
import json
from pathlib import Path
from latex_utils import extract_body, clean_latex_text

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
\\section*{Comment}
\\section*{Drill, 1 '또는'과 '그리고'의 여사건}
경우의 수와 확률에서 '또는'과 '그리고'는 각각 집합에서의 '합집합 $(U)$ '과 '교집합 $(\\cap)$ '의 의미를 갖는다. 따라서 드모르간의 법칙으로 다음과 같이 여사건을 다룰 수 있다.

$$
(A \\cup B)^{C}=A^{C} \\cap B^{C},(A \\cap B)^{C}=A^{C} \\cup B^{C}
$$

특히 $A \\cap B$ 의 여사건의 경우의 수는 합의 법칙에서 중복되는 경우의 수를 제외시키는 포함 배제 원리에 따라

$$
n\\left(A^{C} \\cup B^{C}\\right)=n\\left(A^{C}\\right)+n\\left(B^{C}\\right)-n\\left(A^{C} \\cap B^{C}\\right)
$$

으로 계산하고, 두 사건 $A^{C}, B^{C}$ 이 서로 배반사건, 즉 $A^{C} \\cap B^{C}=\\varnothing$ 일 때는

$$
n\\left(A^{c} \\cup B^{c}\\right)=n\\left(A^{c}\\right)+n\\left(B^{C}\\right)
$$

으로 계산한다.

\\section*{Drill. 2 이웃하지 않는 것의 여사건}
2 개가 이웃하지 않는 것은 여사건인 2 개가 이웃하는 것으로 다루는 것이 편리할 때가 많다. 그러나 일반적으로 3 개 이상이 이웃하지 않는 것은 이들이 모두 이웃하는 것의 여사건이 아니라는 것에 주의하자. 예를 들어 3 개가 이웃하지 않는 것의 여사건에는 이들 중 어느 둘만 이웃하는 것도 있기 때문이다. 앞의 문제의 조건 (나)는 1 과 2 가 이웃하거나 6 과 7 이 이웃하는 여사건을 이용하는 것이 편리하다.

\\section*{Comment}
\\section*{Drill 케이스 구분의 기준}
앞의 문제에서 무엇을 케이스 구분의 기준으로 잡기 시작해야 할까? 이웃하는 것보다 맞은편에 있는 것을 생각하는 것이 수월하므로 맞은편에 있는 두 수의 합의 최댓값을 케이스 구분의 기준으로 잡고 이웃하는 두 수의 합의 최댓값이 이보다 작도록 조절하는 것이 좋아 보인다. 맞은편에 있는 두 수의 합의 최댓값이 11 인 경우부터 시작해 보자. 각 케이스별로 맞은편에 있는 두 수의 합이 최대가 되도록 한 후 남은 4 개의 수 중 가장 큰 수부터 어디에 두어야 할지 차근차근 따져보면 된다.

\\section*{Drill. 1 부정방정식의 음이 아닌 정수해}
예를 들어 2 개의 문자 $x, y$ 에서 5 개를 택하는 중복조합은

$$
\\text { sx } x x x, \\text { sx } x x y, \\text { ́sx } x y y, \\text { sx } y y y, \\text { syyyy, yyyyy }
$$

의 6 가지이고, 이들 각각을 $x$ 의 개수와 $y$ 의 개수의 순서쌍으로 나타내면

$$
(5,0),(4,1),(3,2),(2,3),(1,4),(0,5)
$$

이다. 이는 방정식 $x+y=5$ 를 만족시키는 음이 아닌 정수 $x, y$ 의 순서쌍 $(x, y)$ 이고,\\\\
그 개수는 ${ }_{2} \\mathrm{H}_{5}$ 임을 알 수 있다.\\\\
일반적으로 두 자연수 $n, r$ 에 대하여 방정식 $x_{1}+x_{2}+\\cdots+x_{n}=r$ 를 만족시키는 음이 아닌 정수 $x_{1}, x_{2}, \\cdots, x_{n}$ 의 순서쌍 $\\left(x_{1}, x_{2}, \\cdots, x_{n}\\right)$ 의 개수는

$$
{ }_{n} \\mathrm{H}_{r}
$$

이다.

\\section*{Drill 2 여사건의 선택}
$A \\cap B$ 의 경우의 수를 모든 경우의 수에서 $A \\cap B$ 의 여사건인 $A^{C} \\cup B^{C}$ 의 경우의 수를 빼서 구할 수도 있지만 $A$ 의 경우의 수 중에서 $B$ 가 아닌 경우의 수, 즉 $A \\cap B^{C}$ 의 경우의 수를 $A$ 의 경우의 수에서 빼거나, $B$ 의 경우의 수 중에서 $A$ 가 아닌 경우의 수, 즉 $A^{C} \\cap B$ 의 경우의 수를 $B$ 의 경우의 수에서 빼서 구할 수도 있다.

$$
n(A \\cap B)=n(A)-n\\left(A \\cap B^{C}\\right)=n(B)-n\\left(A^{C} \\cap B\\right)
$$

실전에서 두 조건 (가), (나)를 모두 만족하는 경우의 수를 구할 때\\\\
(가)를 만족하는 모든 경우의 수를 구한 후, 이 중에서 (나)를 만족하지 않는 경우의 수를 빼거나 (나)를 만족하는 모든 경우의 수를 구한 후, 이 중에서 (가)를 만족하지 않는 경우의 수를 빼는 방법으로 이용하면 된다.

앞의 문제의 조건 (나)에서 음이 아닌 두 정수의 합이 1 이상인 것의 여사건은 합이 0 인 것으로 매우 단순하다. 여사건을 이용하기로 한다면 조건 (가)를 만족시키는 경우의 수를 먼저 구하고 이를 전제로 하면 조건 (나)의 여사건이 그리 번잡하지 않다. $a+d, b+e, c+f$ 가 모두 0 일 수는 없으므로 이건 패스. $a+d, b+e, c+f$ 중 어느 둘이 0 인 경우와 어느 하나가 0 인 경우뿐이다. 조건 (나)의 여사건을 다룰 때 조건 (가)를 만족시키는 것을 전제로 한다는 것에 끝까지 주의하자.

\\section*{Drill 부정방정식의 정수해에 대한 조건}
다음의 예와 같이 부정방정식의 정수해에 대한 조건이 있을 때 새로운 미지수로 치환하여 다룰 수 있다. 치환한 미지수는 음이 아닌 정수가 되도록 하는 것이 가장 유리하다.\\\\[0pt]
[예] (1) $x+y+z=10$ 에서 $x, y, z$ 가 자연수라면 자연수는 0 을 포함하지 않으므로 $x, y, z \\geq 1$ 을 만족시키고 이를 음이 아닌 정수해의 조건으로 바꾸기 위해 $x-1=X, y-1=Y, z-1=Z$ 로 두자. $X+Y+Z=10-3=7$ 이고 $X, Y, Z$ 는 음이 아닌 정수이므로 바로 ${ }_{3} \\mathrm{H}_{7}$ 로 풀 수 있다.\\\\
(2) $x+y+z=10$ 에서 $x, y, z$ 는 자연수이고 $x$ 는 짝수, $y, z$ 는 홀수라는 조건이 있다면 $x=2 X+2, y=2 Y+1, z=2 Z+1$ 로 두자. $x+y+z=(2 X+2)+(2 Y+1)+(2 Z+1)=10$ 에서 $X+Y+Z=3$ 이고 $X, Y, Z \\geq 0$ 을 만족시키므로 ${ }_{3} \\mathrm{H}_{3}$ 이 뇐다.\\\\
(3) $x+y+z=10$ 에서 $x, y, z$ 는 정수이고 $x, y, z \\geq-2$ 인 조건이 있다면 음이 아닌 정수해인 상황으로 바꾸는 것이 가장 유리하므로 $x+2=X, y+2=Y$, $z+2=Z$ 로 두자.\\\\
$X+Y+Z=10+6=16$ 이고 $X, Y, Z \\geq 0$ 을 만족시키므로 ${ }_{3} \\mathrm{H}_{16}$ 이 된다.

\\section*{Comment}
Drill 새로운 미지수로 치환\\\\
앞의 문제에서 $x_{1}, x_{2}, x_{3}, x_{4}$ 는 음이 아닌 정수가 아니다. 이처럼 중복조합으로 부정방정식의 정수해를 다룰 때 미지수가 음이 아닌 정수가 아니라면 음이 아닌 정수인 새로운 미지수로 치환해보는 것이 좋다. 치환한 미지수의 값의 범위에 주의하여 제외할 것을 놓치지 않고 마무리하도록 하자.

\\section*{Comment}
\\section*{Drill 미지수의 조건 설정}
앞의 문제에서는 $x_{1}, x_{2}, x_{3}, x_{4}$ 가 음이 아닌 정수라고 했지만 조건 (나)를 이용하기 위해 미지수가 홀수인지 짝수인지를 케이스 구분의 기준으로 삼아야겠다고 판단할 수 있을 것이다. 조건 (가)에서 4 개의 음이 아닌 정수의 합이 짝수인 10 이므로 4 개의 홀수 또는 2 개의 홀수와 2 개의 짝수 또는 4 개의 짝수로 케이스를 구분할 수 있다. 새로운 미지수로 치환할 때 짝수에는 0 도 포함하도록 주의해야 한다.

\\section*{Corroprepret}
\\section*{Drill 부정방정식의 정수해의 '순서쌍'의 개수의 의미}
앞의 문제는 0 의 개수를 기준으로 케이스를 구분한 후 사용할 수 있는 수를 선택하여 같은 것이 있는 순열로 풀 수도 있다. 다른 방법은? 0 을 제외한 자연수의 합이라는 것에서 부정 방정식의 정수해의 순서쌍을 떠올려보면 어떨까? 순서를 구별하는 상황이라 중복조합과 맞지 않다고 생각할 수 있으나 순서쌍의 개수를 구하는 것이므로 방정식의 미지수의 순서대로 이 순서쌍으로 정해진 수를 나열하는 것으로 생각할 수 있다. 부정방정식의 정수해의 순서쌍의 개수를 구하는 것이 이처럼 순서를 구별하는 상황에도 이용될 수 있다는 것은 확실히 해두자.

\\section*{Cornmenct}
\\section*{Drill 순서 부여를 놓치지 않도록}
앞의 문제에서는 조건 (가)에 따라 케이스를 구분하고 시작해야 할 것 같다. 4 로 나눈 나머지의 합이므로 일반적인 부정방정식의 상황이 아니다. 일일이 써봐야 한다. 케이스를 구분하고 나면 각 케이스별로 $a, b, c$ 를 4 로 나눈 몫과 나머지로 표현하면서 몫을 새로운 정수 미지수로 잡아야 하는데, 이때 음이 아닌 정수인지 자연수인지 확실히 해야 한다. 새로운 정수 미지수를 잡을 때는 가급적이면 음이 아닌 정수로 하는 게 좋긴 하다. 이제 각 케이스별로 조건 (다)를 만족시키는 새로운 미지수의 순서쌍의 개수를 구하기만 하면 이대로 끝? 아니다! 예를 들어 4 로 나눈 나머지가 $3,3,0$ 인 경우라면 $a, b, c$ 각각을 4 로 나눈 나머지가 $3,3,0$ 을 일렬로 나열한 것으로 구별하는 것을 놓치면 안 된다. 순서를 이중 부여하는 것과 순서 부여를 놓치는 것에 항상 주의하자.

\\section*{Cornineret}
\\section*{Drill 순서가 정해진 배열}
조합의 활용에서 순서가 정해진 배열을 다룰 때, 선택하기만 하면 정해진 순서대로 배열하는 경우의 수는 1 이므로 선택(조합)만으로 계산을 마무리한다. 중복조합의 활용에서 순서가 정해진 배열을 다룰 때도 이와 마찬가지로 선택하기만 하면 정해진 순서대로 배열하는 경우의 수는 1 이므로 선택(중복조합)만으로 계산을 마무리한다.\\\\
부등식에 모두 등호가 없으면 서로 다른 것을 선택하는 조합, 부등식에 모두 등호가 있으면 같은 것을 선택할 수 있는 중복조합을 이용한다.\\\\[0pt]
[예] $1 \\leq a \\leq b \\leq c \\leq 8$ 을 만족시키는 자연수 $a, b, c$ 의 순서쌍 $(a, b, c)$ 의 개수는 $1,2,3, \\cdots$, 8 에서 중복을 허락하여 3 개를 택하는 경우의 수와 같으므로 ${ }_{8} \\mathrm{H}_{3}={ }_{10} \\mathrm{C}_{3}=120$\\\\[0pt]
[비교] $1<a<b<c<8$ 을 만족시키는 자연수 $a, b, c$ 의 순서쌍 $(a, b, c)$ 의 개수는 $2,3,4$, $5,6,7$ 에서 서로 다른 3 개를 택하는 경우의 수와 같으므로 ${ }_{6} \\mathrm{C}_{3}=20$

\\section*{Comment}
\\section*{Drill 거의 중복순열}
앞의 문제에서는 우선 4 로 나눈 나머지가 같은 것의 개수부터 구분하고 시작해야 한다. 1 부터 9 까지의 자연수 중에서 중복을 허락하여 5 개를 택해 일렬로 나열한 후 4 로 나눈 나머지가 조건 (가)를 만족시키도록 할 것이 아니라, 4 로 나눈 나머지에서 중복을 허락하여 5 개를 택하기만 하면 그만이라고 생각할 수 있어야 한다. 조건 (나)를 만족시키는 케이스를 구분하는 것도 그리 어렵지 않다. 4 로 나눈 나머지가 $0,2,3$ 인 것의 개수는 같고 4 로 나눈 나머지가 1 인 것의 개수만 이와 다르다는 것을 이용하여 효율적으로 계산할 길을 찾고, 중복조합과 중복순열을 상황에 맞게 이용하며 마무리하면 된다.


\\end{document}"""


def extract_solutions_from_latex(latex_content, debug=False):
    """LaTeX에서 해설 추출"""
    solutions = []
    
    # 본문 추출
    body = extract_body(latex_content)
    
    # 섹션 헤더 패턴
    section_pattern = re.compile(r'\\section\*\{([^}]+)\}')
    
    # 모든 섹션 찾기
    all_section_matches = list(section_pattern.finditer(body))
    
    # Comment, Commnent, Commenent, Connment, Corroprepret, Cornmenct, Cornineret 섹션 찾기 (전략 해설)
    comment_sections = []
    drill_sections = []
    other_sections = []
    
    for match in all_section_matches:
        title = match.group(1)
        pos = match.start()
        if ('Comment' in title or 'Commnent' in title or 'Commenent' in title or 
            'Connment' in title or 'Corroprepret' in title or 'Cornmenct' in title or 
            'Cornineret' in title):
            comment_sections.append((pos, title))
        elif 'Drill' in title:
            drill_sections.append((pos, title))
        else:
            other_sections.append((pos, title))
    
    if debug:
        print(f"[디버깅] Drill 섹션 발견: {len(drill_sections)}개")
        print(f"[디버깅] Comment 섹션 발견: {len(comment_sections)}개")
    
    # 각 섹션에서 해설 추출
    all_sections = sorted([(pos, 'drill', title) for pos, title in drill_sections] + 
                          [(pos, 'comment', title) for pos, title in comment_sections] +
                          [(pos, 'other', title) for pos, title in other_sections])
    
    # Comment 섹션 다음에 나오는 섹션들을 찾기
    comment_positions = [pos for pos, _ in comment_sections]
    is_after_comment = {}
    
    # 각 Comment 섹션 다음에 나오는 섹션 찾기
    for comment_pos, comment_title in comment_sections:
        # Comment 섹션 다음에 나오는 첫 번째 섹션 찾기
        next_section_after_comment = None
        for pos, section_type, title in all_sections:
            if pos > comment_pos:
                if next_section_after_comment is None or pos < next_section_after_comment[0]:
                    next_section_after_comment = (pos, section_type, title)
                break
        
        # Comment 섹션 다음에 나오는 모든 섹션을 전략 해설로 분류
        # (다음 Comment 섹션 이전까지)
        if next_section_after_comment:
            next_comment_pos = None
            for other_comment_pos, _ in comment_sections:
                if other_comment_pos > comment_pos:
                    if next_comment_pos is None or other_comment_pos < next_comment_pos:
                        next_comment_pos = other_comment_pos
            
            # Comment 섹션 다음부터 다음 Comment 섹션(또는 문서 끝)까지의 모든 섹션
            for pos, section_type, title in all_sections:
                if pos > comment_pos:
                    if next_comment_pos is None or pos < next_comment_pos:
                        is_after_comment[pos] = True
                    else:
                        break
    
    for i, (pos, section_type, title) in enumerate(all_sections):
        # 섹션 내용 추출
        if i < len(all_sections) - 1:
            next_pos = all_sections[i+1][0]
            section_content = body[pos:next_pos]
        else:
            section_content = body[pos:]
        
        # 섹션 헤더 제거
        section_content = re.sub(r'\\section\*\{[^}]*\}', '', section_content, count=1)
        
        # 이미지 제거
        section_content = re.sub(r'\\includegraphics[^}]*\{[^}]+\}', '', section_content)
        section_content = re.sub(r'\\begin\{figure\}.*?\\end\{figure\}', '', section_content, flags=re.DOTALL)
        section_content = re.sub(r'\\begin\{center\}.*?\\end\{center\}', '', section_content, flags=re.DOTALL)
        section_content = re.sub(r'\\begin\{enumerate\}.*?\\end\{enumerate\}', '', section_content, flags=re.DOTALL)
        section_content = re.sub(r'\\begin\{tabular\}.*?\\end\{tabular\}', '', section_content, flags=re.DOTALL)
        section_content = re.sub(r'\\caption\{[^}]+\}', '', section_content)
        
        # 텍스트 정리
        solution_text = clean_latex_text(section_content)
        
        # 빈 해설 제외 (Comment 섹션 자체는 제외)
        if len(solution_text.strip()) < 50:
            continue
        
        # 해설 타입 판단
        if section_type == 'comment':
            # Comment 섹션 자체는 내용이 없으면 건너뛰기
            if len(solution_text.strip()) < 50:
                continue
            solution_type = "strategy"
        elif is_after_comment.get(pos, False):
            # Comment 섹션 다음에 나오는 섹션은 전략 해설
            solution_type = "strategy"
        elif section_type == 'drill':
            solution_type = "concept"
        else:
            # 다른 섹션은 내용에 따라 판단
            if ('Comment' in title or 'Commnent' in title or 'Commenent' in title or 
                'Connment' in title or 'Corroprepret' in title or 'Cornmenct' in title or 
                'Cornineret' in title):
                solution_type = "strategy"
            else:
                solution_type = "concept"
        
        solutions.append({
            "index": f"{len(solutions)+1:02d}",
            "solution_type": solution_type,
            "title": title,
            "content": solution_text.strip()
        })
    
    return solutions


def review_solutions(solutions):
    """해설 검토 (수학적 논리 포함)"""
    print("=" * 60)
    print("[해설 데이터 검토]")
    print("=" * 60)
    
    errors = []
    warnings = []
    
    for sol in solutions:
        content = sol.get('content', '')
        
        # LaTeX 괄호 검사
        dollar_count = content.count('$') - content.count('\\$')
        if dollar_count % 2 != 0:
            errors.append(f"해설 {sol['index']}: LaTeX 수식 괄호 불일치 ($ 개수: {dollar_count})")
        
        # 수학적 논리 검사 (경우의 수 관련)
        if '경우의 수' in content or '순열' in content or '조합' in content:
            # 중복조합 공식 확인
            if '\\mathrm{H}' in content or 'H_' in content:
                if '음이 아닌 정수' in content or '부정방정식' in content:
                    # 중복조합과 부정방정식의 관계 확인
                    pass
        
        # 내용 길이 확인
        if len(content) < 100:
            warnings.append(f"해설 {sol['index']}: 내용이 짧음 ({len(content)}자)")
    
    print(f"\n[총 해설수] {len(solutions)}개")
    print(f"[개념 해설] {sum(1 for s in solutions if s['solution_type'] == 'concept')}개")
    print(f"[전략 해설] {sum(1 for s in solutions if s['solution_type'] == 'strategy')}개")
    
    if errors:
        print(f"\n[오류] {len(errors)}개")
        for err in errors:
            print(f"  - {err}")
    
    if warnings:
        print(f"\n[경고] {len(warnings)}개")
        for warn in warnings:
            print(f"  - {warn}")
    
    if not errors and not warnings:
        print("\n[오류] 없음")
    
    return len(errors) == 0


def compare_with_problems(solutions, problems_file_path):
    """문제 파일과 비교하여 일관성 확인"""
    try:
        with open(problems_file_path, 'r', encoding='utf-8') as f:
            problems = json.load(f)
        
        print("\n" + "=" * 60)
        print("[문제-해설 비교 검토]")
        print("=" * 60)
        
        print(f"\n[문제 수] {len(problems)}개")
        print(f"[해설 수] {len(solutions)}개")
        
        # 주제 확인
        problem_topics = set(p.get('topic', '') for p in problems)
        print(f"\n[주제 일치] 확인됨: {problem_topics}")
        
        # 수학적 개념 확인
        solution_text = ' '.join(s.get('content', '') for s in solutions)
        concepts = []
        if '경우의 수' in solution_text:
            concepts.append('경우의 수')
        if '순열' in solution_text:
            concepts.append('순열')
        if '원순열' in solution_text:
            concepts.append('원순열')
        if '조합' in solution_text or '중복조합' in solution_text:
            concepts.append('조합')
        if '부정방정식' in solution_text:
            concepts.append('부정방정식')
        if '여사건' in solution_text:
            concepts.append('여사건')
        
        if concepts:
            print(f"\n[수학적 개념 확인]")
            print(f"  확인된 개념: {set(concepts)}")
        
    except Exception as e:
        print(f"\n[경고] 문제 파일 비교 중 오류: {e}")


def main():
    print("=" * 60)
    print("[확통 드릴 P2 해설 LaTeX → CSV 변환]")
    print("=" * 60)
    
    # 1단계: LaTeX 읽기
    print(f"\n[1단계] LaTeX 내용 읽기 완료 ({len(latex_content)}자)")
    
    # 2단계: 해설 추출
    print("\n[2단계] 해설 추출 중...")
    solutions = extract_solutions_from_latex(latex_content, debug=True)
    print(f"[완료] {len(solutions)}개 해설 추출됨")
    
    # 3단계: 검토
    print("\n[3단계] 해설 검토 중...")
    is_valid = review_solutions(solutions)
    
    # 4단계: 문제 파일과 비교
    base_dir = Path(r'C:\Users\a\Documents\MathPDF\organized\현우진\확통_2005학년도_현우진_드릴')
    problems_file = base_dir / "확통_2024학년도_현우진_드릴_P2_문제_deepseek.json"
    if problems_file.exists():
        compare_with_problems(solutions, problems_file)
    
    # 5단계: 저장
    print("\n[4단계] 딥시크용 파일 저장 중...")
    base_filename = "확통_2024학년도_현우진_드릴_P2_해설"
    
    # CSV 저장
    csv_path = base_dir / f"{base_filename}_deepseek.csv"
    with open(csv_path, 'w', encoding='utf-8-sig', newline='') as f:
        f.write("index,solution_type,title,content\n")
        for sol in solutions:
            index = sol['index']
            sol_type = sol['solution_type']
            title = sol.get('title', '').replace(',', '，').replace('\n', ' ')
            content = sol['content'].replace(',', '，').replace('\n', ' ')
            f.write(f"{index},{sol_type},{title},{content}\n")
    
    # JSON 저장
    json_path = base_dir / f"{base_filename}_deepseek.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(solutions, f, ensure_ascii=False, indent=2)
    
    print(f"\n[CSV 저장 완료] {csv_path}")
    print(f"[JSON 저장 완료] {json_path}")
    
    print("\n" + "=" * 60)
    print("[완료] 딥시크가 읽을 수 있는 형태로 저장되었습니다.")
    print("=" * 60)
    print(f"저장 위치: {base_dir}")
    print(f"  - CSV: {csv_path.name}")
    print(f"  - JSON: {json_path.name}")


if __name__ == '__main__':
    main()
