# test_p1_options_final.py
# 문제 1번 선택지 최종 테스트

import re

# 실제 body 텍스트
options_text = '\\\\\\\\\n(1) \\$\\\\frac{15}{16}\\$\\\\\\\\\n(2) 1\\\\\\\\\n(3) \\$\\\\frac{17}{16}\\$\\\\\\\\\n(4) \\$\\\\frac{9}{8}\\$\\\\\\\\\n(5) \\$\\\\frac{19}{16}\\$\n\n'

print("=" * 80)
print("문제 1번 선택지 최종 테스트")
print("=" * 80)
print(f"선택지 텍스트:\n{repr(options_text)}")
print("\n" + "=" * 80)

options = []
for i in range(1, 6):
    print(f"\n선택지 {i}:")
    # 실제 body 텍스트: (1) \\$\\\\frac{15}{16}\\$ 또는 (2) 1\\\\
    patterns = [
        rf'\({i}\)\s*\\\$\\\\frac{{([0-9]+)}}\{{([0-9]+)}}\\\$',  # (1) $\frac{15}{16}$
        rf'\({i}\)\s*([0-9]+)(?=\\\\\\\\)',                        # (2) 1\\\\
    ]
    match = None
    for j, pattern in enumerate(patterns):
        match = re.search(pattern, options_text)
        if match:
            print(f"  패턴 {j+1} 성공: {match.groups()}")
            print(f"  전체 매칭: {repr(match.group(0))}")
            break
    if match:
        option_num = ["①", "②", "③", "④", "⑤"][i-1]
        if len(match.groups()) == 2 and match.group(1).isdigit() and match.group(2).isdigit():
            opt_text = f"\\frac{{{match.group(1)}}}{{{match.group(2)}}}"
            options.append(f"{option_num} ${opt_text}$")
            print(f"  최종 선택지: {options[-1]}")
        else:
            options.append(f"{option_num} {match.group(1)}")
            print(f"  최종 선택지: {options[-1]}")
    else:
        print(f"  모든 패턴 실패")

print("\n" + "=" * 80)
print(f"총 선택지 수: {len(options)}")
print(f"선택지 목록: {options}")
