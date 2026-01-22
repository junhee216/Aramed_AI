# fix_p7_options_v2.py
# 문제 05, 06번 선택지 추가 (개선 버전)

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

# 문제 05번 선택지 추출 (더 넓은 범위)
p5_match = re.search(r'선분.*?\[4점\](.*?)(?:\\includegraphics|\\section|닫힌구간)', body, re.DOTALL)
if p5_match:
    options_text = p5_match.group(1) if p5_match.lastindex >= 1 else ""
    # 전체 본문에서 문제 05번 부분 찾기
    p5_full_match = re.search(r'구간.*?\[4점\](.*?)(?:\\section|닫힌구간)', body, re.DOTALL)
    if p5_full_match:
        options_text = p5_full_match.group(1) if p5_full_match.lastindex >= 1 else ""
    
    p5_options = []
    for i in range(1, 6):
        pattern = rf'\({i}\)\s*\$([^\$]+)\$'
        match = re.search(pattern, options_text)
        if match:
            option_num = ["①", "②", "③", "④", "⑤"][i-1]
            p5_options.append(f"{option_num} ${match.group(1)}$")
    print(f"[문제 05] 선택지: {p5_options}")

# 문제 06번 선택지 추출
p6_match = re.search(r'닫힌구간.*?\[3점\](.*?)(?:\(1\)|\\end)', body, re.DOTALL)
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

# 직접 LaTeX에서 찾기
if not p5_options:
    # 문제 05번 선택지 직접 추출
    p5_direct = re.search(r'\(1\)\s*\$\\frac\{e\^\{2\}\}-3\}\{2\}\$.*?\(5\)\s*\$\\frac\{e\^\{2\}\}\+3\}\{2\}\$', body, re.DOTALL)
    if p5_direct:
        p5_options = [
            "① $\\frac{e^{2}-3}{2}$",
            "② $\\frac{e^{2}-1}{2}$",
            "③ $\\frac{e^{2}}{2}$",
            "④ $\\frac{e^{2}+1}{2}$",
            "⑤ $\\frac{e^{2}+3}{2}$"
        ]
        print(f"[문제 05] 선택지 (직접 추출): {p5_options}")

if not p6_options:
    # 문제 06번 선택지 직접 추출
    p6_direct = re.search(r'\(1\)\s*\$2\+\\frac\{\\sqrt\{3\}\}\{3\} \\pi\$', body)
    if p6_direct:
        p6_options = [
            "① $2+\\frac{\\sqrt{3}}{3} \\pi$",
            "② $2+\\frac{2 \\sqrt{3}}{3} \\pi$",
            "③ $3+\\frac{\\sqrt{3}}{3} \\pi$",
            "④ $3+\\frac{2 \\sqrt{3}}{3} \\pi$",
            "⑤ $4+\\frac{\\sqrt{3}}{3} \\pi$"
        ]
        print(f"[문제 06] 선택지 (직접 추출): {p6_options}")

# CSV 읽기 및 수정
problems = []
with open(csv_path, 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        idx = row['index']
        if idx == '05' and p5_options:
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
    if idx == '05' and p5_options:
        problem['options'] = p5_options
        problem['answer_type'] = 'multiple_choice'
    elif idx == '06' and p6_options:
        problem['options'] = p6_options
        problem['answer_type'] = 'multiple_choice'

with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"[JSON 수정 완료] {json_path}")
