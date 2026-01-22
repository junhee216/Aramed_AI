# convert_su2_p7_solution_latex.py
# 수2 드릴 P7 해설 LaTeX를 딥시크용 CSV로 변환

import re
import sys
import os
from pathlib import Path
from latex_utils import extract_body, clean_latex_text
import json

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
\\usepackage{newunicodechar}
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

\\newunicodechar{□}{\\ifmmode\\square\\else{$\\square$}\\fi}

\\begin{document}
\\section*{Drill 정적분으로 정의된 함수 그리고 넓이의 관점}
정적분 $\\int_{a}^{b} \\square d x$ 에서 □ 의 식에 $x$ 가 아닌 변수가 포함되어 있고, $x$ 와 이 변수 사이의 관계식이 따로 주어지지 않으면 $\\int_{a}^{b} \\square d x$ 는 이 변수에 대한 함수가 된다.

앞의 문제에서는 정적분으로 정의된 함수 $g(t)=\\int_{-1}^{5}|f(x)-t| d x$ 를 구간 $[-1,5]$ 에서 곡선 $y=f(x)$ 와 직선 $y=t$ 로 둘러싸인 부분의 넓이인 $t$ 에 대한 함수로 인식하고 직선 $y=t$ 의 위치의 변화에 따른 넓이의 변화 관찰로 방향을 잡기 시작해야 한다.\\\\
조건 (가)의 항등식을 정적분의 넓이의 관점에서 살펴보면 삼차함수 $y=f(x)$ 의 그래프의 변곡점 $(2,2)$ 를 직감할 수 있다. 아니라면 어떤 일이 벌어지는지 그래프로 간단히 확인해 보고 확정하면 된다.\\\\
$g(f(k))$ 는 별거 아니다. 구간 $[-1,5]$ 에서 곡선 $y=f(x)$ 와 직선 $y=f(k)$ 로 둘러싸인 부분의 넓이이다. 삼차함수 $f(x)$ 가 극값을 갖지 않으면 조건 (나)에 모순인 것과 함께 삼차 함수의 그래프의 비율 관계, 대칭 등의 특징을 이용할 타이밍을 놓치지 않도록 주의하면서 마무리 단계로 접어들면 된다.\\\\
모든 과정이 시행착오를 감안한 그래프의 기하적 상황의 추정과 확인으로 실전적으로 이루어 져야 한다.

\\section*{Drill 넓이의 관점과 표현}
앞의 문제에서는 $g(x)=\\int_{2-x}^{2+x} f(t) d t$ 의 적분 구간에서 삼차함수 $f(x)$ 의 그래프의 대칭과 변곡점의 이용을 직감하고 시작해야 한다.\\\\
조건 (가)의 항등식을 무겁게 바라보지만 않는다면 $g(x)$ 의 그래프가 기울기가 $2 f(2)$ 인 직선을 나타낸다는 것을 쉽게 알 수 있고, $g(x)=\\int_{2-x}^{2+x} f(t) d t$ 에 우선 대입해 볼 만한 값으로 $x=0$ 을 떠올릴 수 있다. $g(0)=0$ 이다.\\\\
$\\int_{2-x}^{2+x} f(t) d t=2 f(2) x$ 는 그래프의 특수한 상태에 대한 추정과 확인의 방법으로 이용해야 한다. 정중앙에 2 가 있는 구간에서의 정적분이다. $y=f(x)$ 의 그래프의 변곡점에 대해 진작 관심을 두고 있었고 점 $(2, f(2))$ 가 매우 의심스럽다. $2 f(2) x$ 를 그래프가 점 $(2, f(2))$ 에 대하여 대칭인 함수의 정적분인지 확인해 보겠다고 방향만 제대로 잡는다면 식의 변형은 그리 어렵지 않다.\\\\
여기까지 성공하면 남은 과정은 삼차함수의 그래프의 접선에 관한 비율 관계 등을 이용하여 식을 쓰고 계산하는 것. 이미 미분에서 충분히 친숙해졌을 과정이다.

\\section*{Drill 당연히 해야 할 일들의 연결}
앞의 문제의 조건 (나)의 정적분에 당황하면 안 된다. $g(x)$ 의 치역이 $\\{0, a\\}$ 이다. 모든 실수 $x$ 에 대한 것이므로 $\\int_{-3}^{g(x)}$ 는 $\\int_{-3}^{0}, \\int_{-3}^{a}$ 로 고치면 그만이다. 한 함수에 대한 여러 정적분이 등장할 때 정적분의 성질을 이용해 보는 것은 당연하고, 정적분의 값이 0 이라는 것의 의미도 매우 친숙한 것이다. 보통은 그 구간에 함숫값이 양수인 부분과 음수인 부분이 모두 존재하는 것으로 그래프의 개형을 잡아서 이용한다. 그런데 함수의 절댓값의 정적분이 0 이라는 것의 의미는? 이 또한 당연히 그 구간에서 함숫값이 모두 0 , 즉 그 구간에서의 그래프가 $x$ 축 위에 놓인 선분이라는 것이다.\\\\
$y=g(x)$ 의 그래프가 직선 $y=0$ 의 일부와 직선 $y=a$ 의 일부의 조합으로 이루어졌으므로 불연속인 점이 존재한다. $f(x) g(x)$ 가 실수 전체의 집합에서 연속이라는 것은 전형적인 $($ 연속 $) \\times($ 불연속 $)=($ 연속 $)$ 의 상황이고, $g(x)$ 가 불연속인 점의 후보는 $y=f(x)$ 의 그래프와 $x$ 축의 두 교점뿐이다. 여기까지의 판단을 종합하면 $g(x)$ 의 함숫값이 0 인 구간을 구하고 곧이어 $g(x)$ 의 함숫값이 $a$ 인 구간도 마저 구하게 된다.\\\\
남은 중요한 판단은 적절히 구간을 나누어 $g(x)$ 를 0 또는 $a$ 인 상수로 고치는 것! 주어진 정적분의 값을 이용하여 $f(x)$ 의 최고차항의 계수의 부호를 정하고 마무리해 갈 수 있다.

\\section*{Commnent}
\\section*{Drill. 1 속도와 거리}
점 P 가 수직선 위를 시각 $t=a$ 에서 $t=b$ 까지 움직일 때, 시각 $t$ 에서의 속도를 $v(t)$, 시각 $t=a$ 일 때의 위치를 $x_{0}$ 이라 하면\\\\
(1) 시각 $t=b$ 일 때의 점 P 의 위치는

$$
x=x_{0}+\\int_{a}^{b} v(t) d t
$$

(2) 시각 $t=a$ 에서 $t=b$ 까지 점 P 의 위치의 변화량은

$$
\\int_{a}^{b} v(t) d t
$$

(3) 시각 $t=a$ 에서 $t=b$ 까지 점 P 가 움직인 거리는

$$
\\int_{a}^{b}|v(t)| d t
$$

\\section*{Drill. 2 속도의 그래프의 이용}
속도가 주어질 때는 속도의 그래프를 그리고 시작하는 것이 좋다. 속도의 부호와 넓이로 위치, 위치의 변화량, 움직인 거리 등을 다룰 수 있고 속도의 부정적분인 위치의 그래프를 파악할 수도 있다.\\\\
앞의 문제는 속도의 그래프를 이용하여 얻은 위치의 그래프에서 삼차함수의 그래프의 비율 관계를 적용해도 좋고, 위치의 두 극값의 차가 속도의 그래프와 $t$ 축으로 둘러싸인 부분의 넓이인 것에서 이차함수에 관한 넓이의 공식을 이용해도 좋다.

\\section*{Drill 속도의 그래프의 이용}
앞의 문제 역시 속도 $v_{1}(t)$ 의 그래프를 그리는 것부터 시작해야 한다. 두 속도 $v_{1}(t), v_{2}(t)$ 의 부정적분인 위치를 각각 $x_{1}(t), x_{2}(t)$ 라 하면 $x_{1}(t)$ 는 $t=1$ 에서 극대, $t=3$ 에서 극소인 삼차함수이고 $x_{2}(t)$ 의 그래프는 기울기가 $a$ 인 직선이다. $x_{1}(t), x_{2}(t)$ 의 그래프가 $t=2,4$ 에서 만난단다. 삼차함수의 그래프의 대칭과 비율 관계에서 삼차방정식 $x_{1}(t)-x_{2}(t)=0$ 의 세 실근이 $0,2,4$ 인 것을 곧바로 알아내면 거의 다 된 거다. 삼차방정식 $x_{1}(t)-x_{2}(t)=0$ 의 근과 계수의 관계의 이용도 괜찮은 방법이다.

\\section*{2024학년도 수능 공통 10번}
시각 $t=0$ 일 때 동시에 원점을 출발하여 수직선 위를 움직이는 두 점 $\\mathrm{P}, \\mathrm{Q}$ 의 시각 $t(t \\geq 0)$ 에서의 속도가 각각

$$
v_{1}(t)=t^{2}-6 t+5, \\quad v_{2}(t)=2 t-7
$$

이다. 시각 $t$ 에서의 두 점 $\\mathrm{P}, \\mathrm{Q}$ 사이의 거리를 $f(t)$ 라 할 때, 함수 $f(t)$ 는 구간 $[0, a]$ 에서 증가하고, 구간 $[a, b]$ 에서 감소하고, 구간 $[b, \\infty)$ 에서 증가한다. 시각 $t=a$ 에서 $t=b$ 까지 점 Q 가 움직인 거리는?\\\\
(단, $0<a<b$ ) [4점]\\\\
(1) $\\frac{15}{2}$\\\\
(2) $\\frac{17}{2}$\\\\
(3) $\\frac{19}{2}$\\\\
(4) $\\frac{21}{2}$\\\\
(5) $\\frac{23}{2}$

답 (2)

\\section*{Drill 속도의 부호와 넓이}
수직선 위를 움직이는 점의 운동 방향이 바뀐다는 것은 속도의 부호가 바뀐다는 것이다. 앞의 문제에서는 점 P 의 위치의 식이 주어졌지만 조건 (가)에서 점 P 의 속도의 식부터 잡고 시작하자고 판단하는 게 맞다.\\\\
조건 (나)의 이용 방법은? $3 \\leq t \\leq k$ 에서 두 점 $\\mathrm{P}, \\mathrm{Q}$ 모두 운동 방향이 바뀌지 않으므로 이 구간에서 속도의 그래프와 $t$ 축으로 둘러싸인 부분의 넓이가 서로 같다는 것으로 이용하거나 두 점 $\\mathrm{P}, \\mathrm{Q}$ 의 위치의 그래프의 교점의 좌표를 이용해도 좋다.


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
    
    # Comment, Commnent 섹션 찾기 (전략 해설)
    comment_sections = []
    drill_sections = []
    other_sections = []
    
    for match in all_section_matches:
        title = match.group(1)
        pos = match.start()
        if 'Comment' in title or 'Commnent' in title:
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
    
    # 각 Comment 섹션 다음에 나오는 모든 섹션 찾기
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
            if 'Comment' in title or 'Commnent' in title:
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
        
        # 수학적 논리 검사 (적분 관련)
        if '적분' in content:
            # 정적분 정의 확인
            if '\\int_{a}^{b}' in content and 'f(b)-f(a)' not in content and 'f(a)-f(b)' not in content:
                if '도함수' in content or 'f\'' in content:
                    warnings.append(f"해설 {sol['index']}: 정적분과 도함수 관계 언급 가능")
        
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
        import json
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
        if '적분' in solution_text:
            concepts.append('적분')
        if '넓이' in solution_text:
            concepts.append('넓이')
        if '함수' in solution_text:
            concepts.append('함수 관계')
        if '정적분' in solution_text:
            concepts.append('정적분')
        if '속도' in solution_text:
            concepts.append('속도')
        if '거리' in solution_text:
            concepts.append('거리')
        
        if concepts:
            print(f"\n[수학적 개념 확인]")
            print(f"  확인된 개념: {set(concepts)}")
        
    except Exception as e:
        print(f"\n[경고] 문제 파일 비교 중 오류: {e}")


def main():
    print("=" * 60)
    print("[수2 드릴 P7 해설 LaTeX → CSV 변환]")
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
    base_dir = Path(r'C:\Users\a\Documents\MathPDF\organized\현우진\수2_2005학년도_현우진_드릴')
    problems_file = base_dir / "수2_2025학년도_현우진_드릴_P7_문제_deepseek.json"
    if problems_file.exists():
        compare_with_problems(solutions, problems_file)
    
    # 5단계: 저장
    print("\n[4단계] 딥시크용 파일 저장 중...")
    base_filename = "수2_2025학년도_현우진_드릴_P7_해설"
    
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
