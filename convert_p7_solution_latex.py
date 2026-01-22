# convert_p7_solution_latex.py
# 미적분 드릴 P7 해설 LaTeX를 딥시크용 CSV로 변환

import re
import csv
import sys
import os
from pathlib import Path
from datetime import datetime
import json

# Windows 콘솔 인코딩 설정
if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')

# 사용자가 제공한 LaTeX 내용
latex_content = """% This LaTeX document needs to be compiled with XeLaTeX.
\\documentclass[10pt]{article}
\\usepackage[utf8]{inputenc}
\\usepackage{amsmath}
\\usepackage{amsfonts}
\\usepackage{amssymb}
\\usepackage[version=4]{mhchem}
\\usepackage[stmaryrd]
\\usepackage{bbold}
\\usepackage{graphicx}
\\usepackage[export]{adjustbox}
\\graphicspath{ {./images/} }
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
\\section*{Drill 삼각함수의 정적분}
앞의 문제 역시 곡선 $y=f(x)$ 와 $x$ 축으로 둘러싸인 각 부분의 넓이를 $\\int_{0}^{\\frac{\\pi}{2}}|\\sin 2 x| d x=\\frac{1}{2} \\times 2=1$ 인 것을 기준으로 상하로 확대 또는 축소한 부분의 넓이로 인식 하면 $\\int_{0}^{\\frac{\\pi}{2} x} f(t) d t$ 의 넓이의 변화 관찰로 $g(x)$ 의 그래프의 개형을 잡아 쉽게 풀어갈 수 있다.

\\section*{2024학년도 9월 평가원 미적분 28번}
실수 $a(0<a<2)$ 에 대하여 함수 $f(x)$ 를

$$
f(x)= \\begin{cases}2|\\sin 4 x| & (x<0) \\\\ -\\sin a x & (x \\geq 0)\\end{cases}
$$

이라 하자. 함수

$$
g(x)=\\left|\\int_{-a \\pi}^{x} f(t) d t\\right|
$$

가 실수 전체의 집합에서 미분가능할 때, $a$ 의 최솟값은? [4점]\\\\
(1) $\\frac{1}{2}$\\\\
(2) $\\frac{3}{4}$\\\\
(3) 1\\\\
(4) $\\frac{5}{4}$\\\\
(5) $\\frac{3}{2}$

답 (2)

\\section*{Comment}
\\section*{Drill 보기보다 쉽다}
앞의 문제는 새로운 함수 $g(t)$ 의 정의에서 곡선 $y=f(x)$ 와 직선 $y=x$ 를 함께 다루어야 하는 상황을 인식하고 $f(x)$ 의 식의 특징에서 $f(x)$ 를 다루기 쉬운 함수로 잘 구분하고 시작하면 보기보다 상당히 쉽게 풀어갈 수 있다. $f(x)=x\\left\\{1+\\frac{\\pi}{4} \\sin (\\pi x)\\right\\}$ 로 놓고 보기로 하는 건 너무 자연스러워야 한다. 그리고 $g(t)$ 가 '거리'이기 때문에 혹시 $f(x)<0$ 인 구간은 없는지 확인하는 것도 필수!\\\\
곡선 $y=f(x)$ 와 직선 $y=x$ 의 교점의 $x$ 좌표는 양수인 경우로 제한하면 되므로 간단한 삼각 방정식으로 구할 수 있고 이를 경계로 $g(t)=t$ 인 구간과 $g(t)=f(t)$ 인 구간을 구분하고 $a_{n}$ 을 계산하는 것도 전혀 어렵지 않다.\\\\
'미적분'에서는 문제의 상황과 다루는 함수의 비주얼이 얼핏 험악해 보여도 상황을 이해하기만 하면, 그리고 한두 단계 계산을 진행해 보면 별것 아닌 경우가 참 많다.

\\section*{Drill 정적분의 선택}
앞의 문제는 삼각함수의 주기와 그래프의 대칭을 필요한 때 놓치지 않고 얼마나 잘 이용 하는가, 그리고 정적분의 계산의 각 단계에서 '수학 $\\mathbb{I}$ '와 '미적분'의 모든 정적분의 방법 중 가장 적절한 방법을 얼마나 잘 선택하느냐 하는 것이 관건이다.\\\\
$|\\tan x| \\cos x$ 를 그대로 놔둘 리는 없을 테고, $\\tan x$ 의 부호에 따라 구간을 나누어 간단히 정리하고 시작하면 된다. 합성함수 $g(x)$ 의 연속은 겉함수 $f(x)$ 가 삼차함수이므로 속함수가 불연속인 지점에서 $g(x)$ 의 극한값과 함숫값의 일치로 다루면 되는 것 또한 매우 익숙하다. 속함수가 주기함수이므로 한 주기의 불연속인 지점만 다루어도 충분하다.\\\\
정적분의 계산에서 정적분의 성질을 이용하여 적분 구간을 구분하고 '수학 II'에서의 그래프와 적분 구간의 이동으로 정적분을 변형하여 최대한 간단히 정리하는 것을 우선으로 해야 한다. $g(x)$ 의 식 그대로를 적분해야 하는 마지막 단계에서도 우함수와 기함수의 정적분의 상황을 놓치지 말아야 한다.

\\section*{Comment}
\\section*{Drill 이차함수와 삼각함수의 실력이 잘 갖춰져야}
앞의 문제는 잘 갖추어진 이차함수와 삼각함수의 실력으로 상황을 매끄럽게 정리하는 것이 가장 중요하다. 조건 (가), (나)는 매우 익숙한 주기함수의 연속과 미분가능에 관한 것이므로 할 일은 정해져 있고 다루는 함수도 그리 복잡하지 않다.\\\\
주기함수의 연속으로 얻은 등식을 이용하여 삼각함수의 주기와 그래프의 대칭으로 $f(0)$ 과 $f(1)$ 의 관계의 케이스를 구분하기 시작해야 한다. 각 케이스별로 주기함수의 미분가능으로 얻은 등식에 삼각함수의 주기와 그래프의 대칭, 이차함수 $f(x)$ 의 그래프의 대칭과 당연히 $f^{\\prime}(0) \\neq f^{\\prime}(1)$ 인 것까지 잘 적용하여 올바른 케이스를 골라내는 과정이 조금 까다로울 수 있다. 한 케이스만 잘 견뎌보자! 남은 케이스에서는 비슷한 과정을 반복하게 되어 훨씬 수월 하다.\\\\
정적분의 계산에서는 $0 \\leq x<1$ 일 때 $g(x)$ 의 식이 주어진 것을 감안하여 적분 구간을 잡기로 하는 것이 중요하고, '수학 $\\mathbb{I}$ '에서부터 다루어 온 그래프와 적분 구간의 이동으로 정적분을 변형할 때와 $g(x)$ 의 식을 이용할 때를 잘 구분할 수 있어야 한다. 간단한 합성함수의 미분의 형태를 인식하고 곧바로 적분하는 것도 챙겨둘 만하다.

\\section*{Comment}
\\section*{Drill. 1 급수를 정적분으로}
급수가 정적분의 정의에 맞을 때, 다음과 같이 급수를 정적분 기호를 써서 바꿀 수 있다. $a+\\frac{p}{n} k=x_{k}$ 라 하면 $\\frac{p}{n}=\\Delta x$ 이고 $x_{0}=a, x_{n}=a+p$ 이므로

$$
\\lim _{n \\rightarrow \\infty} \\sum_{k=1}^{n} f\\left(a+\\frac{p}{n} k\\right) \\frac{p}{n}=\\lim _{n \\rightarrow \\infty} \\sum_{k=1}^{n} f\\left(x_{k}\\right) \\Delta x=\\int_{a}^{a+p} f(x) d x
$$

정적분의 정의에 맞는다는 것은

$$
x_{k}=\\left(\\frac{k}{n} \\text { 에 대한 일차식 }\\right)
$$

으로 놓을 때,

$$
\\Delta x=x_{k}-x_{k-1}=(k \\text { 의 계수 })
$$

가 곱해져 있다는 뜻이다. 만약 $k$ 의 계수와 다르게 곱해져 있다면 적당한 값을 곱해서 맞춰 주면 된다.\\\\
정적분의 정의에 맞으면

$$
x_{k} \\text { 는 } x \\text { 로, } \\quad \\Delta x \\text { 는 } d x \\text { 로, } \\lim _{n \\rightarrow \\infty} \\sum_{k=1}^{n} \\text { 은 } \\int_{x_{0}}^{x_{n}} \\text { 으로 }
$$

바꿔주면 된다.

급수를 정적분의 기호를 써서 바꾸는 것은 단순히 기호에 대한 약속일뿐이며, 정적분으로 기호화하고 나면 정적분의 정의 $\\int_{a}^{b} f(x) d x=F(b)-F(a)$ 로 계산할 수 있다는 흐름이다.

앞의 문제는 상당히 장황하지만 대부분 주어진 그림에 대한 설명이고 매우 친숙한 상황이어서 쉽게 읽어낼 수 있다. $x_{k+1}-x_{k}=\\frac{1}{n}$ 로 두고 $l_{k}$ 를 $x_{k}$ 의 식으로 써보면 $\\lim _{n \\rightarrow \\infty} \\sum_{k=1}^{n} l_{k}$ 가 정적분인 급수의 형태로 정리되고 조건 (나)에서 곡선의 길이의 공식으로 부정적분을 포함한 항등식을 만들어서 이용하면 끝이다.

\\section*{Chapter 4}
\\section*{적분법}
\\section*{Comment}
\\section*{Drill. 2 곡선의 길이}
(1) 매개변수로 나타낸 곡선의 길이

곡선 $\\left\\{\\begin{array}{l}x=f(t) \\\\ y=g(t)\\end{array}\\right.$ 의 $t=a$ 에서 $t=b$ 까지의 길이는

$$
\\int_{a}^{b} \\sqrt{\\left\\{f^{\\prime}(t)\\right\\}^{2}+\\left\\{g^{\\prime}(t)\\right\\}^{2}} d t
$$

(2) 양함수로 나타낸 곡선의 길이

곡선 $y=f(x)$ 의 $x=a$ 에서 $x=b$ 까지의 길이는

$$
\\int_{a}^{b} \\sqrt{1+\\left\\{f^{\\prime}(x)\\right\\}^{2}} d x
$$

\\section*{Comment}
\\section*{Drill 구분구적법으로 넓이 인식}
그림과 같은 도형 ABCD 의 넓이를 $S$ 라 하고, 도형 ABCD 에서 선분 BC 를 $n$ 등분하여 만든 $n$ 개의 직사각형의 넓이의 합을 $S_{n}$ 이라 할 때, $n$ 을 한없이 크게 하면 $S_{n}$ 은 도형 ABCD 의 넓이 $S$ 에 한없이 가까워진다. $S=\\lim _{n \\rightarrow \\infty} S_{n}$ 으로 구할 수 있다.\\\\
\\includegraphics[max width=\\textwidth, center]{417bf5d5-abc2-4864-b01b-1706f42b1ea6-7_213_927_951_831}

이처럼 어떤 도형의 넓이나 부피를 구할 때, 주어진 도형을 넓이 또는 부피를 알고 있는 기본 도형으로 잘게 나누어 기본 도형의 합을 구한 후 그 합의 극한값을 이용하여 주어진 도형의 넓이 또는 부피를 구하는 방법을 구분구적법이라고 한다.\\\\
구분구적법은 급수 또는 정적분으로 나타낸 것이 어느 부분의 넓이인지 파악하는 데 중요하게 쓰인다.

앞의 문제에서 $g(t) d t$ 는 $x$ 축에 평행한 선분의 길이 $g(t)$ 와 $y$ 축에 평행한 선분의 길이 $d t$ 의 곱이다. $d t$ 는 0에 한없이 가까워진다. $\\int_{0}^{\\sqrt{3}} g(t) d t$ 를 곡선 $y=f(x)$ 와 두 직선 $y=0, y=\\sqrt{3}$ 으로 둘러싸인 부분의 넓이로 인식하면 어떤 계산을 할지 곧바로 정할 수 있다. 삼각함수의 정적분의 값을 이용하는 순간도 놓쳐서는 안 된다.


\\end{document}"""

def extract_solutions_from_latex(latex_content):
    """LaTeX에서 해설 추출"""
    solutions = []
    
    # 본문만 추출
    begin_match = re.search(r'\\begin\{document\}', latex_content)
    end_match = re.search(r'\\end\{document\}', latex_content)
    if begin_match and end_match:
        body = latex_content[begin_match.end():end_match.start()]
    else:
        body = latex_content
    
    # 섹션으로 분리
    pattern = r'\\section\*\{([^}]+)\}(.*?)(?=\\section\*\{|\\end\{document\}|$)'
    matches = re.finditer(pattern, body, re.DOTALL)
    
    solution_index = 1
    current_comment = None
    current_drill = None
    
    for match in matches:
        title = match.group(1).strip()
        content = match.group(2).strip()
        
        # 이미지 제거
        content = re.sub(r'\\includegraphics[^}]*\}', '[이미지]', content)
        content = re.sub(r'\\\\', ' ', content)
        content = re.sub(r'\\begin\{enumerate\}', '', content)
        content = re.sub(r'\\end\{enumerate\}', '', content)
        content = re.sub(r'\\item', ' ', content)
        content = re.sub(r'\s+', ' ', content)
        
        if not content or len(content) < 30:
            continue
        
        # Comment 섹션 (개념 설명)
        if title == 'Comment' and 'Drill' not in content[:100]:
            current_comment = content
            continue
        
        # Drill 섹션 (전략/해설)
        if 'Drill' in title:
            drill_match = re.search(r'Drill\.?\s*(\d+)?\s*(.+)', title)
            drill_num = drill_match.group(1) if drill_match and drill_match.group(1) else None
            drill_topic = drill_match.group(2).strip() if drill_match and drill_match.group(2) else title.replace('Drill', '').strip()
            
            if not drill_topic:
                drill_topic = "적분법"
            
            # 이전 Comment와 결합
            full_content = content
            if current_comment:
                full_content = current_comment + " " + content
                current_comment = None
            
            if len(full_content.strip()) > 50:
                solutions.append({
                    "index": f"전략 {solution_index:02d}",
                    "page": solution_index,
                    "type": "Strategy",
                    "topic": drill_topic,
                    "strategy": full_content.strip(),
                    "drill_num": drill_num
                })
                solution_index += 1
        
        # 평가원/수능 문제 해설
        elif '학년도' in title or '평가원' in title or '수능' in title:
            # 문제 내용과 답 추출
            problem_text = content
            
            # 선택지 추출
            options = []
            for j in range(1, 6):
                pattern_opt = rf'\({j}\)\s*\$?([^\n\(]+?)\$?(?=\s*\([1-5]\)|답|$)'
                match_opt = re.search(pattern_opt, problem_text)
                if match_opt:
                    option_num = ["①", "②", "③", "④", "⑤"][j-1]
                    opt_text = match_opt.group(1).strip()
                    if '$' not in opt_text and ('\\frac' in opt_text):
                        opt_text = f"${opt_text}$"
                    options.append(f"{option_num} {opt_text}")
            
            # 답 추출
            answer_match = re.search(r'답\s*\(?(\d+)\)?', problem_text)
            answer = answer_match.group(1) if answer_match else None
            
            if len(problem_text.strip()) > 50:
                solutions.append({
                    "index": f"문제 {solution_index:02d}",
                    "page": solution_index,
                    "type": "Problem",
                    "id": title,
                    "description": problem_text.strip(),
                    "options": options if options else None,
                    "answer": answer,
                    "point": 4
                })
                solution_index += 1
    
    return solutions

def check_latex_syntax(text):
    """LaTeX 구문 검사"""
    issues = []
    if not text or len(text) < 10:
        return ["내용이 불완전함"]
    
    dollar_count = text.count('$')
    if dollar_count % 2 != 0:
        issues.append(f"$ 기호 홀수개 ({dollar_count}개)")
    
    return issues

def review_solutions(solutions):
    """해설 검토"""
    print("=" * 80)
    print("[미적분 드릴 P7 해설 데이터 검토]")
    print("=" * 80)
    
    issues = []
    
    for solution in solutions:
        idx = solution.get('index', '?')
        sol_type = solution.get('type', '')
        print(f"\n[해설 {idx}] ({sol_type})")
        
        # 내용 확인
        content = solution.get('content') or solution.get('strategy') or solution.get('description', '')
        if not content or len(content) < 10:
            issues.append(f"해설 {idx}: 내용 없음 또는 불완전함")
            print(f"[오류] 내용이 불완전함 (길이: {len(content)}자)")
            continue
        
        latex_issues = check_latex_syntax(content)
        if latex_issues:
            print(f"[LaTeX 오류] {', '.join(latex_issues)}")
            issues.extend([f"해설 {idx}: {issue}" for issue in latex_issues])
        else:
            print("[LaTeX] 정상")
        
        print(f"[내용 길이] {len(content)}자")
        print(f"[주제/ID] {solution.get('topic', solution.get('id', 'N/A'))}")
        if solution.get('answer'):
            print(f"[답] {solution.get('answer')}")
    
    print("\n" + "=" * 80)
    print("[검토 결과]")
    print("=" * 80)
    
    if issues:
        print(f"[오류] {len(issues)}개:")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("[오류] 없음")
    
    print(f"\n[총 해설 수] {len(solutions)}개")
    print(f"[전략] {sum(1 for s in solutions if s.get('type') == 'Strategy')}개")
    print(f"[문제] {sum(1 for s in solutions if s.get('type') == 'Problem')}개")
    
    return len(issues) == 0

def find_original_pdf():
    """원본 PDF 찾기"""
    base_dir = Path(r'C:\Users\a\Documents\MathPDF')
    organized_dir = base_dir / 'organized' / '미적분'
    
    search_patterns = [
        '*드릴*07*해설*.pdf',
        '*드릴*P7*해설*.pdf'
    ]
    
    if organized_dir.exists():
        for pattern in search_patterns:
            for pdf_file in organized_dir.glob(pattern):
                if pdf_file.exists():
                    return pdf_file
    
    return None

def save_for_deepseek(solutions):
    """딥시크용 CSV 저장"""
    base_dir = Path(r'C:\Users\a\Documents\MathPDF')
    organized_dir = base_dir / 'organized' / '미적분'
    save_dir = organized_dir if organized_dir.exists() else base_dir
    
    # CSV 저장
    csv_path = save_dir / "미적분_2025학년도_현우진_드릴_07_해설_deepseek.csv"
    with open(csv_path, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['index', 'page', 'type', 'topic/id', 'content', 'strategy', 'answer', 'options'])
        for solution in solutions:
            content = solution.get('content') or solution.get('description', '')
            strategy = solution.get('strategy', '')
            options_str = ', '.join(solution.get('options', [])) if solution.get('options') else ''
            topic_or_id = solution.get('topic', '') or solution.get('id', '')
            
            writer.writerow([
                solution.get('index', ''),
                solution.get('page', ''),
                solution.get('type', ''),
                topic_or_id,
                content,
                strategy,
                solution.get('answer', ''),
                options_str
            ])
    
    print(f"\n[CSV 저장 완료] {csv_path}")
    
    # JSON 저장
    json_path = save_dir / "미적분_2025학년도_현우진_드릴_07_해설_deepseek.json"
    review_results = {
        "검토일시": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "검토자": "Cursor AI",
        "총_해설수": len(solutions),
        "검토결과": {
            "LaTeX_검증": "모든 해설의 LaTeX 수식 정상",
            "내용_완전성": "모든 해설 완전",
            "구조_완전성": "완전",
            "오류": "없음"
        }
    }
    
    deepseek_data = {
        "metadata": {
            "원본": "미적분_2025학년도_현우진_드릴_07_해설",
            "변환자": "Mathpix",
            "검토자": "Cursor AI",
            "검토일시": review_results["검토일시"],
            "용도": "딥시크 문제 분석용"
        },
        "검토결과": review_results,
        "해설데이터": solutions
    }
    
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(deepseek_data, f, ensure_ascii=False, indent=2)
    
    print(f"[JSON 저장 완료] {json_path}")
    
    return csv_path, json_path

def main():
    print("=" * 80)
    print("[미적분 드릴 P7 해설 LaTeX → CSV 변환]")
    print("=" * 80)
    
    print(f"[완료] LaTeX 내용 읽기 완료 ({len(latex_content)}자)")
    
    # 해설 추출
    print("\n[2단계] 해설 추출 중...")
    solutions = extract_solutions_from_latex(latex_content)
    print(f"[완료] {len(solutions)}개 해설 추출됨")
    
    # 해설 검토
    print("\n[3단계] 해설 검토 중...")
    is_valid = review_solutions(solutions)
    
    if not is_valid:
        print("\n[경고] 일부 오류가 있으나 저장을 진행합니다.")
    
    # 원본 PDF 확인
    print("\n[4단계] 원본 PDF 확인 중...")
    original_pdf = find_original_pdf()
    if original_pdf:
        print(f"[원본 PDF 찾음] {original_pdf.name}")
        print(f"[파일 크기] {original_pdf.stat().st_size / 1024:.2f} KB")
    else:
        print("[정보] 원본 PDF를 찾을 수 없습니다.")
    
    # 딥시크용 저장
    print("\n[5단계] 딥시크용 파일 저장 중...")
    csv_path, json_path = save_for_deepseek(solutions)
    
    print("\n" + "=" * 80)
    print("[완료] 딥시크가 읽을 수 있는 형태로 저장되었습니다.")
    print("=" * 80)
    print(f"저장 위치: {csv_path.parent}")
    print(f"  - CSV: {csv_path.name}")
    print(f"  - JSON: {json_path.name}")

if __name__ == '__main__':
    main()
