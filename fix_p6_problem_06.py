# fix_p6_problem_06.py
# 문제 06번 선택지 추가

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

# 문제 06번 선택지 추출
p6_match = re.search(r'미분가능한 함수 \$f\(x\)\$ 에 대하여 함수 \$g\(x\)\$ 가.*?\[4점\](.*?)(?:실수|\\section)', body, re.DOTALL)
if p6_match:
    options_text = p6_match.group(1) if p6_match.lastindex >= 1 else ""
    p6_options = []
    for i in range(1, 6):
        # 수식 선택지: (1) $-\frac{e}{2} k$
        pattern_formula = rf'\({i}\)\s*\$([^\$]+)\$'
        match_formula = re.search(pattern_formula, options_text)
        if match_formula:
            option_num = ["①", "②", "③", "④", "⑤"][i-1]
            p6_options.append(f"{option_num} ${match_formula.group(1)}$")
    print(f"[문제 06] 선택지: {p6_options}")

# 문제 07번 선택지 정리 (\\\\ 제거)
p7_options = ['① -1', '② $-\frac{1}{2}$', '③ $\frac{1}{2}$', '④ 1', '⑤ 2']

# CSV 읽기 및 수정
problems = []
with open(csv_path, 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        idx = row['index']
        if idx == '06' and p6_options:
            row['options'] = ', '.join(p6_options)
            row['answer_type'] = 'multiple_choice'
        elif idx == '07':
            row['options'] = ', '.join(p7_options)
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
    if idx == '06' and p6_options:
        problem['options'] = p6_options
        problem['answer_type'] = 'multiple_choice'
    elif idx == '07':
        problem['options'] = p7_options
        problem['answer_type'] = 'multiple_choice'

with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"[JSON 수정 완료] {json_path}")
