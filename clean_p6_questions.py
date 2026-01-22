# clean_p6_questions.py
# P6 문제 질문 텍스트 정리

import json
import csv
from pathlib import Path

json_path = Path(r'C:\Users\a\Documents\MathPDF\organized\현우진\확통_2005학년도_현우진_드릴\확통_2024학년도_현우진_드릴_P6_문제_deepseek.json')

with open(json_path, 'r', encoding='utf-8') as f:
    problems = json.load(f)

# 질문 텍스트 정리
for problem in problems:
    question = problem['question']
    
    # "통계"로 시작하는 경우 제거
    if question.startswith('통계 '):
        question = question[3:]
    
    # "(13)"으로 시작하는 경우 제거
    if question.startswith('(13) '):
        question = question[5:]
    
    problem['question'] = question

# 저장
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(problems, f, ensure_ascii=False, indent=2)

# CSV도 업데이트
csv_path = json_path.with_suffix('.csv')
with open(csv_path, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=problems[0].keys())
    writer.writeheader()
    writer.writerows(problems)

print("질문 텍스트 정리 완료")
