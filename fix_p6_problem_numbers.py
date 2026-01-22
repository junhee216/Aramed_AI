# fix_p6_problem_numbers.py
# P6 문제 번호 수정

import json
from pathlib import Path

json_path = Path(r'C:\Users\a\Documents\MathPDF\organized\현우진\확통_2005학년도_현우진_드릴\확통_2024학년도_현우진_드릴_P6_문제_deepseek.json')

with open(json_path, 'r', encoding='utf-8') as f:
    problems = json.load(f)

# 문제 번호 수정
# 순서: 1, 13, 2, 15, 6, 7, 8, 9
correct_numbers = [1, 13, 2, 15, 6, 7, 8, 9]

for i, problem in enumerate(problems):
    if i < len(correct_numbers):
        problem['index'] = f"{correct_numbers[i]:02d}"
        print(f"문제 {i+1}: {problem['index']}로 수정")

# 저장
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(problems, f, ensure_ascii=False, indent=2)

print(f"\n수정 완료: {json_path}")

# CSV도 업데이트
import csv
csv_path = json_path.with_suffix('.csv')
with open(csv_path, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=problems[0].keys())
    writer.writeheader()
    writer.writerows(problems)
print(f"CSV 업데이트 완료: {csv_path}")
