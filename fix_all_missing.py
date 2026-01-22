# fix_all_missing.py
# 누락된 문제 수정 스크립트

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
print("문제 1번 선택지 추출 테스트")
print("=" * 80)

# 문제 1번 선택지 추출
p1_match = re.search(r'(\\\$a>1\\\$ 인 상수.*?\[4점\])(.*?)(?=\\\\section)', body, re.DOTALL)
if p1_match:
    options_text = p1_match.group(2) if p1_match.lastindex >= 2 else ""
    print(f"선택지 텍스트 길이: {len(options_text)}")
    print(f"선택지 텍스트 (처음 200자):\n{options_text[:200]}\n")
    
    # 각 선택지 추출 시도
    for i in range(1, 6):
        print(f"\n선택지 {i} 추출 시도:")
        patterns = [
            rf'\({i}\)\s*\\\$([^\\\$]+)\\\$',      # (1) \$\frac{15}{16}\$
            rf'\({i}\)\s*\\\$([^\\\$]+)\$',         # (1) \$\frac{15}{16}$
            rf'\({i}\)\s*([0-9]+)(?=\\\\)',        # (2) 1\\
            rf'\({i}\)\s*([0-9]+)',                # (2) 1
        ]
        for j, pattern in enumerate(patterns):
            match = re.search(pattern, options_text)
            if match:
                print(f"  패턴 {j+1} 성공: {match.group(1)}")
                break
        else:
            print(f"  모든 패턴 실패")
            # 직접 찾기
            pos = options_text.find(f'({i})')
            if pos != -1:
                print(f"  위치: {pos}")
                print(f"  주변 텍스트: {options_text[pos:pos+50]}")
