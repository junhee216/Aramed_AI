# debug_p2_extraction.py
# P2 문제 추출 디버깅

import re
import sys
import os

if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')

# LaTeX 내용 읽기
with open('convert_su1_p2_problems_latex.py', 'r', encoding='utf-8') as f:
    content = f.read()

# latex_content 추출
match = re.search(r'latex_content = """(.*?)"""', content, re.DOTALL)
if match:
    latex_content = match.group(1)
else:
    print("latex_content를 찾을 수 없습니다.")
    sys.exit(1)

# 본문만 추출
begin_match = re.search(r'\\begin\{document\}', latex_content)
end_match = re.search(r'\\end\{document\}', latex_content)
if begin_match and end_match:
    body = latex_content[begin_match.end():end_match.start()]
else:
    body = latex_content

print(f"Body 길이: {len(body)}자")
print(f"Body 시작 200자:\n{body[:200]}\n")
print("=" * 80)

# 문제 1번 패턴 테스트
print("\n[문제 1번 패턴 테스트]")
p1_pattern = r'(\\\$a>1\\\$ 인 상수.*?\[4점\])'
p1_match = re.search(p1_pattern, body, re.DOTALL)
print(f"패턴: {p1_pattern}")
print(f"매칭 결과: {p1_match is not None}")
if p1_match:
    print(f"매칭된 내용 (처음 100자): {p1_match.group(1)[:100]}")
else:
    # 대체 패턴 테스트
    print("\n대체 패턴 테스트:")
    alt_patterns = [
        r'(\$a>1\$ 인 상수.*?\[4점\])',
        r'(a>1 인 상수.*?\[4점\])',
        r'(\$a>1.*?\[4점\])',
    ]
    for i, pattern in enumerate(alt_patterns):
        match = re.search(pattern, body, re.DOTALL)
        print(f"  패턴 {i+1}: {pattern[:50]}... -> {match is not None}")

# 문제 2번 패턴 테스트
print("\n[문제 2번 패턴 테스트]")
p2_pattern = r'(함수 \$f\(x\)=\\log.*?구하시오\. \[4점\])'
p2_match = re.search(p2_pattern, body, re.DOTALL)
print(f"패턴: {p2_pattern}")
print(f"매칭 결과: {p2_match is not None}")
if p2_match:
    print(f"매칭된 내용 (처음 100자): {p2_match.group(1)[:100]}")
else:
    # 대체 패턴 테스트
    print("\n대체 패턴 테스트:")
    alt_patterns = [
        r'(함수.*?구하시오\. \[4점\])',
        r'(함수.*?log.*?구하시오)',
    ]
    for i, pattern in enumerate(alt_patterns):
        match = re.search(pattern, body, re.DOTALL)
        print(f"  패턴 {i+1}: {pattern[:50]}... -> {match is not None}")

# 문제 6번 패턴 테스트
print("\n[문제 6번 패턴 테스트]")
p6_pattern = r'10\\\\\s*(\\\$a>1\\\$ 인 실수.*?\[4점\])'
p6_match = re.search(p6_pattern, body, re.DOTALL)
print(f"패턴: {p6_pattern}")
print(f"매칭 결과: {p6_match is not None}")
if p6_match:
    print(f"매칭된 내용 (처음 100자): {p6_match.group(1)[:100]}")
else:
    # "10" 검색
    ten_pos = body.find('10\\\\')
    if ten_pos != -1:
        print(f"'10\\\\' 위치: {ten_pos}")
        print(f"'10\\\\' 주변 200자:\n{body[ten_pos:ten_pos+200]}\n")
    else:
        print("'10\\\\'를 찾을 수 없습니다.")

# 문제 8번 패턴 테스트
print("\n[문제 8번 패턴 테스트]")
p8_pattern = r'(\\\$a>1\\\$ 인 실수 \\\$a\\\$ 에 대하여 두 곡선.*?구하시오\. \[4점\])'
p8_match = re.search(p8_pattern, body, re.DOTALL)
print(f"패턴: {p8_pattern[:80]}...")
print(f"매칭 결과: {p8_match is not None}")
if p8_match:
    print(f"매칭된 내용 (처음 100자): {p8_match.group(1)[:100]}")
else:
    # "두 곡선" 검색
    pos = body.find('두 곡선')
    if pos != -1:
        print(f"'두 곡선' 위치: {pos}")
        print(f"'두 곡선' 주변 200자:\n{body[pos-50:pos+150]}\n")

# 문제 9번 패턴 테스트
print("\n[문제 9번 패턴 테스트]")
p9_pattern = r'(\\\$a>1\\\$ 인 실수.*?곡선.*?\[4점\])'
p9_match = re.search(p9_pattern, body, re.DOTALL)
print(f"패턴: {p9_pattern[:80]}...")
print(f"매칭 결과: {p9_match is not None}")

# 문제 11번 패턴 테스트
print("\n[문제 11번 패턴 테스트]")
p11_pattern = r'(곡선 \$y=\\log.*?\[4점］)'
p11_match = re.search(p11_pattern, body, re.DOTALL)
print(f"패턴: {p11_pattern}")
print(f"매칭 결과: {p11_match is not None}")
if not p11_match:
    # "곡선" 검색
    pos = body.find('곡선 $y=\\log')
    if pos != -1:
        print(f"'곡선 $y=\\log' 위치: {pos}")
        print(f"주변 200자:\n{body[pos:pos+200]}\n")

print("\n" + "=" * 80)
print("[섹션 구분자 확인]")
sections = re.findall(r'\\section\*\{[^}]*\}', body)
print(f"섹션 개수: {len(sections)}")
for i, section in enumerate(sections[:10]):
    print(f"  {i+1}. {section}")
