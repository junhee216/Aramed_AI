# fix_p5_options.py
# 문제 02, 06, 07번 선택지 수정

import csv
import json
import re
from pathlib import Path

csv_path = Path(r'C:\Users\a\Documents\MathPDF\organized\미적분\미적분_2025학년도_현우진_드릴_05_문제_deepseek.csv')
json_path = Path(r'C:\Users\a\Documents\MathPDF\organized\미적분\미적분_2025학년도_현우진_드릴_05_문제_deepseek.json')
latex_file = Path(r'C:\Users\a\Documents\MathPDF\organized\미적분\8be6025d-df00-424f-a26c-1b69144de03c\8be6025d-df00-424f-a26c-1b69144de03c.tex')

# LaTeX 파일 읽기
with open(latex_file, 'r', encoding='utf-8') as f:
    latex_content = f.read()

# 문제 02번 선택지 추출
p2_match = re.search(r'삼차함수.*?\[4점\](.*?)(?:\\section|열린구간)', latex_content, re.DOTALL)
if p2_match:
    options_text = p2_match.group(1)
    p2_options = []
    for i in range(1, 6):
        pattern = rf'\({i}\)\s*(\d+)'
        match = re.search(pattern, options_text)
        if match:
            option_num = ["①", "②", "③", "④", "⑤"][i-1]
            p2_options.append(f"{option_num} {match.group(1)}")
    print(f"[문제 02] 선택지: {p2_options}")

# 문제 06번 선택지 추출
p6_match = re.search(r'모든 항의 계수가.*?\[4점\](.*?)(?:두 상수|\\end)', latex_content, re.DOTALL)
if p6_match:
    options_text = p6_match.group(1)
    p6_options = []
    for i in range(1, 6):
        pattern = rf'\({i}\)\s*(\d+)'
        match = re.search(pattern, options_text)
        if match:
            option_num = ["①", "②", "③", "④", "⑤"][i-1]
            p6_options.append(f"{option_num} {match.group(1)}")
    print(f"[문제 06] 선택지: {p6_options}")

# 문제 07번 선택지 추출
p7_match = re.search(r'두 상수.*?\[4점\](.*?)(?:\\end|$)', latex_content, re.DOTALL)
if p7_match:
    options_text = p7_match.group(1)
    p7_options = []
    for i in range(1, 6):
        pattern = rf'\({i}\)\s*\$([^\$]+)\$'
        match = re.search(pattern, options_text)
        if match:
            option_num = ["①", "②", "③", "④", "⑤"][i-1]
            p7_options.append(f"{option_num} ${match.group(1)}$")
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
