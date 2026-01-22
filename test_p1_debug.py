# test_p1_debug.py
# 문제 1번 디버깅

import re

# 실제 body 텍스트
body = """\$a>1\$ 인 상수 \$a\$ 에 대하여 곡선 \$y=a^{x}\$ 과 직선 \$y=2 x\$ 가 두 점 \$\\mathrm{A}, \\mathrm{B}\$ 에서 만나고, 곡선 \$y=a^{2 x}\$ 과 직선 \$y=4 x\$ 가 두 점 \$\\mathrm{C}, \\mathrm{D}\$ 에서 만난다. 직선 AD 의 기울기가 -4 일 때, 점 A 의 \$x\$ 좌표는?\\\\
(단, 원점 O 에 대하여 \$\\overline{\\mathrm{OA}}<\\overline{\\mathrm{OB}}, \\overline{\\mathrm{OC}}<\\overline{\\mathrm{OD}}\$ 이다. ) [4점]\\\\
(1) \$\\frac{15}{16}\$\\\\
(2) 1\\\\
(3) \$\\frac{17}{16}\$\\\\
(4) \$\\frac{9}{8}\$\\\\
(5) \$\\frac{19}{16}\$

\\section*{Chapter 1 \\\\
 지수함수와 로그함수}"""

print("=" * 80)
print("문제 1번 디버깅")
print("=" * 80)

# 패턴 테스트
patterns = [
    (r'(\\\$a>1\\\$ 인 상수.*?\[4점\])(.*?)(?=\\\\section)', "기본 패턴"),
    (r'(\\\$a>1\\\$ 인 상수.*?\[4점\])(.*?)(?=\\\\section\*\{Chapter)', "Chapter 패턴"),
    (r'(\\\$a>1\\\$ 인 상수.*?\[4점\])(.*?)(?=\\\\section\*\{Chapter 1)', "Chapter 1 패턴"),
]

for pattern, desc in patterns:
    print(f"\n{desc}: {pattern}")
    match = re.search(pattern, body, re.DOTALL)
    if match:
        print(f"  [성공] 매칭 성공!")
        print(f"  문제 텍스트 길이: {len(match.group(1))}")
        print(f"  선택지 텍스트 길이: {len(match.group(2)) if match.lastindex >= 2 else 0}")
        if match.lastindex >= 2:
            options_text = match.group(2)
            print(f"  선택지 텍스트:\n{repr(options_text[:300])}")
            
            # 선택지 추출 테스트
            options = []
            for j in range(1, 6):
                patterns2 = [
                    rf'\({j}\)\s*\\\$\\frac{{([0-9]+)}}\{{([0-9]+)}}\\\$',
                    rf'\({j}\)\s*([0-9]+)(?=\\\\)',
                ]
                for pattern2 in patterns2:
                    match2 = re.search(pattern2, options_text)
                    if match2:
                        print(f"    선택지 {j}: {match2.groups()}")
                        options.append(f"선택지 {j}")
                        break
            print(f"  추출된 선택지 수: {len(options)}")
        break
    else:
        print(f"  [실패] 매칭 실패")

# 직접 찾기
print("\n" + "=" * 80)
print("직접 찾기")
print("=" * 80)
pos = body.find('\\section')
if pos != -1:
    print(f"\\section 위치: {pos}")
    print(f"앞부분 (마지막 200자):\n{repr(body[max(0, pos-200):pos])}")
