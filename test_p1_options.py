# test_p1_options.py
# 문제 1번 선택지 추출 테스트

import re

# 실제 선택지 텍스트
options_text = """\\\\
(1) \$\\frac{15}{16}\$\\\\
(2) 1\\\\
(3) \$\\frac{17}{16}\$\\\\
(4) \$\\frac{9}{8}\$\\\\
(5) \$\\frac{19}{16}\$
"""

print("선택지 텍스트:")
print(repr(options_text))
print("\n" + "=" * 80)

# 여러 패턴 테스트
patterns = [
    (r'\(1\)\s*\\\$([^\\\$]+)\\\$', "패턴 1: (1) \\$...\\$"),
    (r'\(1\)\s*\\\$([^\\\$]+)\$', "패턴 2: (1) \\$...$"),
    (r'\(1\)\s*\$([^\$]+)\$', "패턴 3: (1) $...$"),
    (r'\(1\)\s*\\\$\\frac\{15\}\{16\}\\\$', "패턴 4: 정확한 매칭"),
    (r'\(1\)\s*\\\$\\frac\{([0-9]+)\}\{([0-9]+)\}\\\$', "패턴 5: 분수 추출"),
    (r'\(1\)\s*\\?\$?([^\\\$\(]+)\\?\$?', "패턴 6: 일반"),
]

for pattern, desc in patterns:
    match = re.search(pattern, options_text)
    print(f"\n{desc}")
    print(f"패턴: {pattern}")
    print(f"매칭: {match is not None}")
    if match:
        print(f"그룹: {match.groups()}")
        print(f"매칭된 텍스트: {match.group(0)}")

# 올바른 패턴 찾기
print("\n" + "=" * 80)
print("올바른 추출:")
for i in range(1, 6):
    # 실제로 작동하는 패턴
    pattern = rf'\({i}\)\s*\\?\$?([^\\\$\(]+)\\?\$?'
    match = re.search(pattern, options_text)
    if match:
        opt_text = match.group(1).strip()
        opt_text = re.sub(r'\\\\', '', opt_text)
        print(f"선택지 {i}: {opt_text}")
