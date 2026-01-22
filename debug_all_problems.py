# debug_all_problems.py
# 모든 문제 패턴 매칭 확인

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

print("=" * 80)
print("모든 문제 패턴 매칭 확인")
print("=" * 80)

# 문제 1번
print("\n[문제 1번]")
p1_match = re.search(r'(\\\$a>1\\\$ 인 상수.*?\[4점\])(.*?)(?=\\\\section)', body, re.DOTALL)
print(f"패턴 매칭: {p1_match is not None}")
if p1_match:
    question = p1_match.group(1).strip()
    options_text = p1_match.group(2) if p1_match.lastindex >= 2 else ""
    print(f"문제 길이: {len(question)}자")
    print(f"선택지 텍스트 길이: {len(options_text)}자")
    
    # 선택지 추출 테스트
    options = []
    for i in range(1, 6):
        pattern = rf'\({i}\)\s*\\\$?([^\\\$\(]+)\\?\$?'
        match = re.search(pattern, options_text)
        if match:
            options.append(match.group(1).strip())
    print(f"추출된 선택지 수: {len(options)}개")
    if len(options) < 5:
        print(f"선택지 텍스트 (처음 300자): {options_text[:300]}")

# 문제 7번
print("\n[문제 7번]")
p7_match = re.search(r'(그림과 같이 곡선.*?구하시오\. \[4점\])(.*?)(?=\\\\$a>1\\\$ 인 실수.*?두 곡선|\\\\section|\\end)', body, re.DOTALL)
print(f"패턴 매칭: {p7_match is not None}")
if p7_match:
    question = p7_match.group(1).strip()
    print(f"문제 길이: {len(question)}자")
    print(f"'b^{3}' 포함: {'b^{3}' in question or 'b^3' in question}")
    print(f"문제 내용 (처음 200자): {question[:200]}")

# 문제 8번
print("\n[문제 8번]")
p8_match = re.search(r'(\\\$a>1\\\$ 인 실수 \\\$a\\\$ 에 대하여 두 곡선.*?구하시오\. \[4점\])', body, re.DOTALL)
print(f"패턴 매칭: {p8_match is not None}")
if p8_match:
    question = p8_match.group(1).strip()
    print(f"문제 길이: {len(question)}자")
    print(f"'p+q' 포함: {'p+q' in question or 'p\\+q' in question}")
    print(f"문제 내용 (처음 200자): {question[:200]}")

# 문제 9번
print("\n[문제 9번]")
p9_match = re.search(r'(\\\$a>1\\\$ 인 실수.*?곡선.*?\\\$y=\\\\left\(\\frac\{1\}\{a\}\\right\)\^\{x\}.*?\[4점\])', body, re.DOTALL)
print(f"패턴 매칭: {p9_match is not None}")
if p9_match:
    question = p9_match.group(1).strip()
    print(f"문제 길이: {len(question)}자")
    print(f"문제 내용 (처음 200자): {question[:200]}")

# 문제 11번
print("\n[문제 11번]")
p11_match = re.search(r'(곡선 \\\$y=\\\\log.*?\[4점[\]］])', body, re.DOTALL)
print(f"패턴 매칭: {p11_match is not None}")
if p11_match:
    question = p11_match.group(1).strip()
    print(f"문제 길이: {len(question)}자")
    print(f"문제 내용 (처음 200자): {question[:200]}")
