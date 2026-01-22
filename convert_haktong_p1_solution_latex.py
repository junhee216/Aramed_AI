# convert_haktong_p1_solution_latex.py
# 확통 드릴 P1 해설 LaTeX를 딥시크용 CSV로 변환

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
\\section*{Drill. 1 같은 것이 있는 순열}
$n$ 개 중에 서로 같은 것이 각각 $p$ 개, $q$ 개, $\\cdots, r$ 개 있을 때, $n$ 개를 모두 일렬로 배열하는 순열의 수는

$$
\\frac{n!}{p!q!\\cdots r!}(\\text { 단, } p+q+\\cdots+r=n)
$$

\\section*{Drill 2 순서가 정해진 배열}
전체 중 $r$ 개의 순서가 정해진 배열의 경우의 수

$$
\\text { (전체의 배열) } \\times \\frac{1}{r!}
$$

$\\Rightarrow r$ 개의 순서를 무시하고 정해진 순서 1 가지로 취급한다. 즉 $r$ 개를 같은 것으로 본다.

앞의 문제에서는 7 개의 자리 중 숫자를 놓을 4 개의 자리를 먼저 선택한 후 수의 곱의 대소에 관한 조건을 만족하도록 수의 배치를 끝내고, 남은 3 개의 문자를 같은 것이 있는 순열로 마저 배치하면 된다. 그런데 4개의 수의 순서가 정해져 있으므로 처음부터 4개의 수를 같은 것으로 보고 다루어도 좋다.

\\section*{Comment}
\\section*{Drill 이웃하는 것, 이웃하지 않는 것이 있는 배열}
\\begin{enumerate}
  \\item 서로 다른 $r$ 개\\\\
(1) 서로 다른 $r$ 개가 이웃하는 배열 $r$ 개를 1 개로 보고 배열의 수를 계산한 후, $r!$ 을 곱한다.\\\\
(2) 서로 다른 $r$ 개가 이웃하지 않는 배열 $r$ 개를 제외한 배열의 수를 계산한 후, 각각의 사이사이와 양 끝의 빈자리에 $r$ 개를 배열하는 경우의 수를 곱한다.
  \\item 서로 같은 $r$ 개\\\\
(1) 서로 같은 $r$ 개가 이웃하는 배열 $r$ 개를 1 개로 보고 배열의 수를 계산한다.\\\\
(2) 서로 같은 $r$ 개가 이웃하지 않는 배열 $r$ 개를 제외한 배열의 수를 계산한 후, 각각의 사이사이와 양 끝의 빈자리 중 $r$ 개의 자리를 선택한다.
\\end{enumerate}

이웃하는 것, 이웃하지 않는 것에 대한 위의 계산 원칙은 다른 조건 없이 모두 일렬로 나열할 때만 적용된다. 다른 조건이 있거나 모두 일렬로 나열하는 것이 아닐 때는 다른 조건과 자리 배치에 따라 케이스를 구분하여 따져봐야 하고 계산의 방향도 달라질 수 있다. 앞의 문제 에서도 조건 (가)가 없다면 $b, b, c, c, c$ 를 우선 나열한 후 각각의 사이사이와 양 끝의 빈자리 중 $a, a$ 의 자리 2 개를 선택하면 그만이지만 조건 (가) 때문에 양 끝의 문자에 대한 케이스를 구분해야 하고 이후 계산의 방향도 달라진다.

\\section*{Drill 자연수의 십진법 전개식}
예를 들어 자연수 12345 의 $1 \\times 10^{4}+2 \\times 10^{3}+3 \\times 10^{2}+4 \\times 10+5$ 와 같은 십진법 전개식은 문제에 주어지기도 하지만 필요에 따라 스스로 만들어 쓸 수도 있어야 한다. 앞의 문제에서는 $N_{1}=a_{1} \\times 10^{2}+b_{1} \\times 10+c_{1}, N_{2}=a_{2} \\times 10^{2}+b_{2} \\times 10+c_{2}$ 와 같이 나타낸 후 $a_{1}, a_{2}$ 의 값을 정하는 것으로 케이스를 구분하고 각 케이스별로 $b_{1} \\times 10+c_{1}$ 과 $b_{2} \\times 10+c_{2}$ 의 대소 관계에 따라 $b_{1}, b_{2}, c_{1}, c_{2}$ 의 값을 정해주면 된다.

\\section*{Commenent}
\\section*{Drill 조건의 이용 순서 조정}
주어진 조건을 반드시 (가), (나), (다)의 순서대로 이용하라는 법은 없다. 상황에 따라 이용 순서를 조정할 수 있어야 한다. 앞의 문제에서는 조건 (다)를 우선 고려하여 상하 또는 좌우로 홀수가 이웃하면 안 된다는 것에서 남은 조건 (가), (나)에 의해 2,4 의 개수를 정할 수 있다. 그리고 주어진 대로 가는 것이 나을지 여사건을 이용하는 것이 나을지 비교해보는 것은 '확률과 통계' 전반에서 기본적인 태도이다. 여사건인 홀수 2 개가 이웃하는 경우를 따로 따져 보는 것이 낫겠다는 느낌이 확 오지 않나?

\\section*{Comment}
\\section*{Drill 케이스 구분의 기준}
앞의 문제에서는 조건 (다)에 초점을 맞추어 1 행의 3 의 개수 또는 2 행의 3 의 개수에 따라 케이스를 구분하고 시작하는 것이 좋아 보인다. 1 행의 3 의 개수보다 2 행의 3 의 개수가 크거나 같아야 한다. 1 행의 3 의 개수가 1 또는 2 이므로 이에 따라 2 의 개수를 조절하거나 2 행의 3 의 개수가 2 또는 3 이므로 이에 따라 2 의 개수를 조절해보면 된다.

\\section*{Connment}
\\section*{Drill 원순열}
서로 다른 것을 원형으로 배열하는 순열을 원순열이라고 한다. 서로 다른 $n$ 개를 원형으로 배열하는 원순열의 수는

$$
\\frac{n!}{n}=(n-1)!
$$

원순열은 순열의 확장판이라고 생각하면 된다. 순열을 기본으로 하고 원순열에서 경우를 구별하는 기준을 고려하여 경우의 수를 계산한다. 원순열에서 경우를 구별하는 기준은 자리의 '위치'가 아니라 '관계'이다.\\\\
자리가 달라지더라도 서로 간의 배치 관계가 같으면 같은 경우로 본다는 것이다. 이를 '회전하여 일치하는 것은 같은 것으로 본다.'\\\\
라고 표현한다.

\\section*{Comment}
\\section*{Drill 원순열은 무엇 하나라도 배치하고 나면 순열}
원순열에서 가장 중요한 것은 무엇 하나라도 배치하고 나면 곧바로 순열의 상황으로 바뀐다는 것이다. 이때 최초의 배치는 원순열의 관점으로, 즉 회전하여 일치하면 같은 것으로 본다는 관점으로 처리한다. 앞의 문제에서 원순열의 관점으로 빨간색을 칠하는 정삼각형의 자리의 케이스를 구분하고 각 케이스별로 빨간색을 칠하는 경우의 수를 1 로 잡으면 이후는 순열의 상황이 된다.


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
    
    # Comment, Commnent, Commenent, Connment 섹션 찾기 (전략 해설)
    comment_sections = []
    drill_sections = []
    other_sections = []
    
    for match in all_section_matches:
        title = match.group(1)
        pos = match.start()
        if 'Comment' in title or 'Commnent' in title or 'Commenent' in title or 'Connment' in title:
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
            if 'Comment' in title or 'Commnent' in title or 'Commenent' in title or 'Connment' in title:
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
        if '경우의 수' in content or '순열' in content:
            # 순열 공식 확인
            if '\\frac{n!}' in content and 'p!q!' not in content and 'r!' not in content:
                if '같은 것이 있는' in content:
                    warnings.append(f"해설 {sol['index']}: 같은 것이 있는 순열 공식 확인 가능")
        
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
        if '조합' in solution_text:
            concepts.append('조합')
        
        if concepts:
            print(f"\n[수학적 개념 확인]")
            print(f"  확인된 개념: {set(concepts)}")
        
    except Exception as e:
        print(f"\n[경고] 문제 파일 비교 중 오류: {e}")


def main():
    print("=" * 60)
    print("[확통 드릴 P1 해설 LaTeX → CSV 변환]")
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
    problems_file = base_dir / "확통_2024학년도_현우진_드릴_P1_문제_deepseek.json"
    if problems_file.exists():
        compare_with_problems(solutions, problems_file)
    
    # 5단계: 저장
    print("\n[4단계] 딥시크용 파일 저장 중...")
    base_filename = "확통_2024학년도_현우진_드릴_P1_해설"
    
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
