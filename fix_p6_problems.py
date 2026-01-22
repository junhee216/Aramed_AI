# fix_p6_problems.py
# 문제 05번과 09번 수정

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

# 문제 05번 추출
p5_match = re.search(r'실수 전체의 집합에서 연속인 함수 \$f\(x\)\$.*?\[4점\](.*?)(?:실수|미분가능)', body, re.DOTALL)
if p5_match:
    p5_question = p5_match.group(0).split('[4점]')[0].strip() + " [4점]"
    p5_question = re.sub(r'\\section\*\{[^}]*\}', '', p5_question)
    p5_question = re.sub(r'\\\\', ' ', p5_question)
    p5_question = re.sub(r'\s+', ' ', p5_question)
    
    p5_options_text = p5_match.group(1) if p5_match.lastindex >= 1 else ""
    p5_options = []
    for i in range(1, 6):
        pattern = rf'\({i}\)\s*\$([^\$]+)\$'
        match = re.search(pattern, p5_options_text)
        if match:
            option_num = ["①", "②", "③", "④", "⑤"][i-1]
            p5_options.append(f"{option_num} ${match.group(1)}$")
    print(f"[문제 05] 선택지: {p5_options}")

# 문제 09번 선택지 추출
p9_match = re.search(r'첫째항이 4 인 등비수열.*?\[4점\](.*?)(?:\\end|$)', body, re.DOTALL)
if p9_match:
    p9_options_text = p9_match.group(1) if p9_match.lastindex >= 1 else ""
    p9_options = []
    for i in range(1, 6):
        pattern = rf'\({i}\)\s*\$([^\$]+)\$'
        match = re.search(pattern, p9_options_text)
        if match:
            option_num = ["①", "②", "③", "④", "⑤"][i-1]
            p9_options.append(f"{option_num} ${match.group(1)}$")
    print(f"[문제 09] 선택지: {p9_options}")

# CSV 읽기 및 수정
problems = []
with open(csv_path, 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        idx = row['index']
        if idx == '05' and p5_question and p5_options:
            row['question'] = p5_question
            row['options'] = ', '.join(p5_options)
            row['answer_type'] = 'multiple_choice'
        elif idx == '09' and p9_options:
            row['options'] = ', '.join(p9_options)
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
    if idx == '05' and p5_question and p5_options:
        problem['question'] = p5_question
        problem['options'] = p5_options
        problem['answer_type'] = 'multiple_choice'
    elif idx == '09' and p9_options:
        problem['options'] = p9_options
        problem['answer_type'] = 'multiple_choice'

with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"[JSON 수정 완료] {json_path}")
