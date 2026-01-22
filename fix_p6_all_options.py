# fix_p6_all_options.py
# 모든 문제의 선택지 정확히 추출 및 수정

import re
import csv
import json
from pathlib import Path

csv_path = Path(r'C:\Users\a\Documents\MathPDF\organized\미적분\미적분_2025학년도_현우진_드릴_06_문제_deepseek.csv')
json_path = Path(r'C:\Users\a\Documents\MathPDF\organized\미적분\미적분_2025학년도_현우진_드릴_06_문제_deepseek.json')
latex_file = Path(r'C:\Users\a\Documents\MathPDF\organized\미적분\7a29de0b-de28-4298-9ab8-1c373ea3bd1e\7a29de0b-de28-4298-9ab8-1c373ea3bd1e.tex')

# LaTeX 파일 읽기
with open(latex_file, 'r', encoding='utf-8') as f:
    latex_content = f.read()

# 본문만 추출
begin_match = re.search(r'\\begin\{document\}', latex_content)
end_match = re.search(r'\\end\{document\}', latex_content)
if begin_match and end_match:
    body = latex_content[begin_match.end():end_match.start()]
else:
    body = latex_content

# 문제별 선택지 추출 함수
def extract_options_for_problem(problem_num, body):
    """특정 문제의 선택지 추출"""
    options = []
    
    patterns = {
        1: r'실수 전체의 집합에서 미분가능한 함수 \$f\(x\)\$.*?\[3점\](.*?)(?:\\section|\$f\(1\))',
        2: r'\$f\(1\)=f\(3\)=0\$.*?\[4점\](.*?)(?:\\section|양의)',
        3: r'양의 실수 전체의 집합에서 미분가능한 함수.*?\[4점\](.*?)(?:\\section|실수)',
        4: r'실수 전체의 집합에서 연속인 두 함수.*?\[4점\](.*?)(?:\\section|실수)',
        5: r'실수 전체의 집합에서 연속인 함수 \$f\(x\)\$.*?\[4점\](.*?)(?:\\section|미분가능)',
        6: r'미분가능한 함수 \$f\(x\)\$.*?\[4점\](.*?)(?:실수|\\section)',
        7: r'실수 전체의 집합에서 미분가능하고 도함수가 연속인 함수.*?\[4점\](.*?)(?:\\section|함수)',
        8: r'함수 \$f\(x\)\$ 는 실수 전체의 집합에서 연속인 도함수.*?\[4점\](.*?)(?:\\section|첫째항)',
        9: r'첫째항이 4 인 등비수열.*?\[4점\](.*?)(?:\\end|$)',
    }
    
    pattern = patterns.get(problem_num)
    if pattern:
        match = re.search(pattern, body, re.DOTALL)
        if match:
            options_text = match.group(1) if match.lastindex >= 1 else ""
            for i in range(1, 6):
                # 수식 선택지: (1) $\frac{1}{\pi}$
                pattern_formula = rf'\({i}\)\s*\$([^\$]+)\$'
                match_formula = re.search(pattern_formula, options_text)
                if match_formula:
                    option_num = ["①", "②", "③", "④", "⑤"][i-1]
                    options.append(f"{option_num} ${match_formula.group(1)}$")
                else:
                    # 숫자 선택지: (1) -1
                    pattern_num = rf'\({i}\)\s*([^\n\(]+)'
                    match_num = re.search(pattern_num, options_text)
                    if match_num:
                        option_num = ["①", "②", "③", "④", "⑤"][i-1]
                        opt_text = match_num.group(1).strip()
                        # $ 기호가 없으면 추가
                        if '$' not in opt_text and ('\\frac' in opt_text or 'e' in opt_text or 'ln' in opt_text or '-' in opt_text):
                            opt_text = f"${opt_text}$"
                        options.append(f"{option_num} {opt_text}")
    
    return options if options else None

# 각 문제의 선택지 추출
all_options = {}
for i in range(1, 10):
    opts = extract_options_for_problem(i, body)
    if opts:
        all_options[str(i).zfill(2)] = opts
        print(f"[문제 {i:02d}] 선택지: {opts}")

# CSV 읽기 및 수정
problems = []
with open(csv_path, 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        idx = row['index']
        if idx in all_options:
            row['options'] = ', '.join(all_options[idx])
            row['answer_type'] = 'multiple_choice'
        problems.append(row)

# CSV 다시 저장
with open(csv_path, 'w', encoding='utf-8-sig', newline='') as f:
    if problems:
        fieldnames = list(problems[0].keys())
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(problems)

print(f"\n[CSV 수정 완료] {csv_path}")

# JSON도 수정
with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

for problem in data['문제데이터']:
    idx = problem.get('index')
    if idx in all_options:
        problem['options'] = all_options[idx]
        problem['answer_type'] = 'multiple_choice'

with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"[JSON 수정 완료] {json_path}")
