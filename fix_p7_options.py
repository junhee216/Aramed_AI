# fix_p7_options.py
# 문제 03, 05, 06번 선택지 추가

import re
import csv
import json
from pathlib import Path

csv_path = Path(r'C:\Users\a\Documents\MathPDF\organized\미적분\미적분_2025학년도_현우진_드릴_07_문제_deepseek.csv')
json_path = Path(r'C:\Users\a\Documents\MathPDF\organized\미적분\미적분_2025학년도_현우진_드릴_07_문제_deepseek.json')
latex_file = Path(r'C:\Users\a\Documents\MathPDF\organized\미적분\미적분_2025학년도_현우진_드릴_07_문제_변환집\366f2979-0c56-4add-ab0b-6b6f1b1e9f93.tex')

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

# 문제 03번 선택지 추출
p3_match = re.search(r'일 때, \$f\(k\)\$ 의 값은\?.*?\[4점\](.*?)(?:\\section|최고차항)', body, re.DOTALL)
if p3_match:
    options_text = p3_match.group(1) if p3_match.lastindex >= 1 else ""
    p3_options = []
    for i in range(1, 6):
        pattern = rf'\({i}\)\s*(\d+)'
        match = re.search(pattern, options_text)
        if match:
            option_num = ["①", "②", "③", "④", "⑤"][i-1]
            p3_options.append(f"{option_num} {match.group(1)}")
    print(f"[문제 03] 선택지: {p3_options}")

# 문제 05번 선택지 추출
p5_match = re.search(r'선분.*?\[4점\](.*?)(?:\(1\)|\\includegraphics|\\section)', body, re.DOTALL)
if p5_match:
    options_text = p5_match.group(1) if p5_match.lastindex >= 1 else ""
    p5_options = []
    for i in range(1, 6):
        pattern = rf'\({i}\)\s*\$([^\$]+)\$'
        match = re.search(pattern, options_text)
        if match:
            option_num = ["①", "②", "③", "④", "⑤"][i-1]
            p5_options.append(f"{option_num} ${match.group(1)}$")
    print(f"[문제 05] 선택지: {p5_options}")

# 문제 06번 선택지 추출
p6_match = re.search(r'라 할 때,.*?\[3점\](.*?)(?:\(1\)|\\end)', body, re.DOTALL)
if p6_match:
    options_text = p6_match.group(1) if p6_match.lastindex >= 1 else ""
    p6_options = []
    for i in range(1, 6):
        pattern = rf'\({i}\)\s*\$([^\$]+)\$'
        match = re.search(pattern, options_text)
        if match:
            option_num = ["①", "②", "③", "④", "⑤"][i-1]
            p6_options.append(f"{option_num} ${match.group(1)}$")
    print(f"[문제 06] 선택지: {p6_options}")

# CSV 읽기 및 수정
problems = []
with open(csv_path, 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        idx = row['index']
        if idx == '03' and p3_options:
            row['options'] = ', '.join(p3_options)
            row['answer_type'] = 'multiple_choice'
        elif idx == '05' and p5_options:
            row['options'] = ', '.join(p5_options)
            row['answer_type'] = 'multiple_choice'
        elif idx == '06' and p6_options:
            row['options'] = ', '.join(p6_options)
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
    if idx == '03' and p3_options:
        problem['options'] = p3_options
        problem['answer_type'] = 'multiple_choice'
    elif idx == '05' and p5_options:
        problem['options'] = p5_options
        problem['answer_type'] = 'multiple_choice'
    elif idx == '06' and p6_options:
        problem['options'] = p6_options
        problem['answer_type'] = 'multiple_choice'

with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"[JSON 수정 완료] {json_path}")
