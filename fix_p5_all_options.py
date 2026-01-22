# fix_p5_all_options.py
# 모든 문제의 선택지 정확히 추출 및 수정

import re
import csv
import json
from pathlib import Path

csv_path = Path(r'C:\Users\a\Documents\MathPDF\organized\미적분\미적분_2025학년도_현우진_드릴_05_문제_deepseek.csv')
json_path = Path(r'C:\Users\a\Documents\MathPDF\organized\미적분\미적분_2025학년도_현우진_드릴_05_문제_deepseek.json')
latex_file = Path(r'C:\Users\a\Documents\MathPDF\organized\미적분\8be6025d-df00-424f-a26c-1b69144de03c\8be6025d-df00-424f-a26c-1b69144de03c.tex')

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

# 문제별 선택지 추출
def extract_options_for_problem(problem_num, body):
    """특정 문제의 선택지 추출"""
    options = []
    
    if problem_num == 2:
        # 문제 2: (1) 5, (2) 6, ...
        pattern = r'삼차함수.*?\[4점\](.*?)(?:\\section|열린구간)'
        match = re.search(pattern, body, re.DOTALL)
        if match:
            options_text = match.group(1)
            for i in range(1, 6):
                pattern_num = rf'\({i}\)\s*(\d+)'
                match_num = re.search(pattern_num, options_text)
                if match_num:
                    option_num = ["①", "②", "③", "④", "⑤"][i-1]
                    options.append(f"{option_num} {match_num.group(1)}")
    
    elif problem_num == 6:
        # 문제 6: (1) 21, (2) 26, ...
        pattern = r'모든 항의 계수가.*?\[4점\](.*?)(?:두 상수|\\end)'
        match = re.search(pattern, body, re.DOTALL)
        if match:
            options_text = match.group(1)
            for i in range(1, 6):
                pattern_num = rf'\({i}\)\s*(\d+)'
                match_num = re.search(pattern_num, options_text)
                if match_num:
                    option_num = ["①", "②", "③", "④", "⑤"][i-1]
                    options.append(f"{option_num} {match_num.group(1)}")
    
    elif problem_num == 7:
        # 문제 7: (1) $20 e^{5}$, (2) $22 e^{5}$, ...
        pattern = r'두 상수.*?\[4점\](.*?)(?:\\end|$)'
        match = re.search(pattern, body, re.DOTALL)
        if match:
            options_text = match.group(1)
            for i in range(1, 6):
                pattern_formula = rf'\({i}\)\s*\$([^\$]+)\$'
                match_formula = re.search(pattern_formula, options_text)
                if match_formula:
                    option_num = ["①", "②", "③", "④", "⑤"][i-1]
                    options.append(f"{option_num} ${match_formula.group(1)}$")
    
    return options if options else None

# 각 문제의 선택지 추출
p2_options = extract_options_for_problem(2, body)
p6_options = extract_options_for_problem(6, body)
p7_options = extract_options_for_problem(7, body)

print(f"[문제 02] 선택지: {p2_options}")
print(f"[문제 06] 선택지: {p6_options}")
print(f"[문제 07] 선택지: {p7_options}")

# CSV 읽기 및 수정
problems = []
with open(csv_path, 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        idx = row['index']
        if idx == '02' and p2_options:
            row['options'] = ', '.join(p2_options)
            row['answer_type'] = 'multiple_choice'
        elif idx == '06' and p6_options:
            row['options'] = ', '.join(p6_options)
            row['answer_type'] = 'multiple_choice'
        elif idx == '07' and p7_options:
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
    if idx == '02' and p2_options:
        problem['options'] = p2_options
        problem['answer_type'] = 'multiple_choice'
    elif idx == '06' and p6_options:
        problem['options'] = p6_options
        problem['answer_type'] = 'multiple_choice'
    elif idx == '07' and p7_options:
        problem['options'] = p7_options
        problem['answer_type'] = 'multiple_choice'

with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"[JSON 수정 완료] {json_path}")
