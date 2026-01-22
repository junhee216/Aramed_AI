# test_p1_direct.py
# 문제 1번 선택지 직접 테스트

import re

# 실제 LaTeX 텍스트 (line 59-65)
options_text = """(1) \$\\frac{15}{16}\$\\\\
(2) 1\\\\
(3) \$\\frac{17}{16}\$\\\\
(4) \$\\frac{9}{8}\$\\\\
(5) \$\\frac{19}{16}\$
"""

print("선택지 텍스트:")
print(repr(options_text))
print("\n" + "=" * 80)

# 패턴 테스트
for i in range(1, 6):
    print(f"\n선택지 {i}:")
    # 실제 텍스트: (1) \$\\frac{15}{16}\$
    # body에서는 \$ 형태이므로 패턴 수정
    patterns = [
        rf'\({i}\)\s*\\\$\\frac{{([0-9]+)}}\{{([0-9]+)}}\\\$',  # (1) $\frac{15}{16}$
        rf'\({i}\)\s*([0-9]+)(?=\\\\)',                          # (2) 1\\
    ]
    for j, pattern in enumerate(patterns):
        match = re.search(pattern, options_text)
        if match:
            print(f"  패턴 {j+1} 성공: {match.groups()}")
            print(f"  전체 매칭: {match.group(0)}")
            break
    else:
        print(f"  모든 패턴 실패")
        # 직접 찾기
        pos = options_text.find(f'({i})')
        if pos != -1:
            print(f"  위치: {pos}")
            print(f"  주변 텍스트: {repr(options_text[pos:pos+50])}")
