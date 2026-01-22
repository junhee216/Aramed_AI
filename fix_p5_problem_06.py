# fix_p5_problem_06.py
# 문제 06번 LaTeX 오류 수정

import csv
import json
import re
from pathlib import Path

csv_path = Path(r'C:\Users\a\Documents\MathPDF\organized\미적분\미적분_2025학년도_현우진_드릴_05_문제_deepseek.csv')
json_path = Path(r'C:\Users\a\Documents\MathPDF\organized\미적분\미적분_2025학년도_현우진_드릴_05_문제_deepseek.json')

# 원본 LaTeX에서 문제 06번 정확히 추출
problem_06_text = """두 상수 $a, b(a>0)$ 에 대하여 함수 $f(x)$ 가

$$
f(x)=\left(a x^{2}+b x\right) e^{x}
$$

이다. 구간 $[t, \infty)$ 의 임의의 두 실수 $x_{1}, x_{2}\left(x_{1} \neq x_{2}\right)$ 에 대하여

$$
\frac{f\left(x_{2}\right)-f\left(x_{1}\right)}{x_{2}-x_{1}}>c
$$

를 만족시키는 실수 $c$ 의 최댓값을 $g(t)$ 라 하자.\\
실수 전체의 집합에서 미분가능한 함수 $g(t)$ 가 다음 조건을 만족시킨다.\\
(가) $g(2)=-5 e^{2}$\\
(나) 방정식 $g^{\prime}(t)=0$ 의 해는 $t \leq 2$ 이다.\\
$g(5)$ 의 값은? [4점]\\
(1) $20 e^{5}$\\
(2) $22 e^{5}$\\
(3) $24 e^{5}$\\
(4) $26 e^{5}$\\
(5) $28 e^{5}$"""

# 문제 06번 정리
question_06 = problem_06_text.replace('\\\\', ' ').replace('\\', '').strip()
options_06 = [
    "① $20 e^{5}$",
    "② $22 e^{5}$",
    "③ $24 e^{5}$",
    "④ $26 e^{5}$",
    "⑤ $28 e^{5}$"
]

# CSV 읽기 및 수정
problems = []
with open(csv_path, 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row['index'] == '06':
            # 문제 06번 수정
            row['question'] = question_06
            row['options'] = ', '.join(options_06)
        problems.append(row)

# CSV 다시 저장
with open(csv_path, 'w', encoding='utf-8-sig', newline='') as f:
    if problems:
        fieldnames = list(problems[0].keys())
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(problems)

print(f"[수정 완료] {csv_path}")

# JSON도 수정
with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

for problem in data['문제데이터']:
    if problem.get('index') == '06':
        problem['question'] = question_06
        problem['options'] = options_06

with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"[수정 완료] {json_path}")

# LaTeX 검사
dollar_count = question_06.count('$')
print(f"\n[문제 06번 LaTeX 검사]")
print(f"$ 기호 개수: {dollar_count}개 ({'정상' if dollar_count % 2 == 0 else '오류'})")
print(f"선택지 개수: {len(options_06)}개")
