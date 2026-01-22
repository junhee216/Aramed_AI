# test_p1_options_detailed.py
# 문제 1번 선택지 추출 상세 테스트

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

# 문제 1번 선택지 추출
p1_match = re.search(r'(\\\$a>1\\\$ 인 상수.*?\[4점\])(.*?)(?=\\\\section)', body, re.DOTALL)
if p1_match:
    options_text = p1_match.group(2) if p1_match.lastindex >= 2 else ""
    print("=" * 80)
    print("문제 1번 선택지 텍스트 (원본):")
    print(repr(options_text))
    print("\n" + "=" * 80)
    print("선택지 추출 테스트:")
    
    for i in range(1, 6):
        print(f"\n선택지 {i}:")
        # 실제 텍스트 구조에 맞는 패턴들
        patterns = [
            (rf'\({i}\)\s*\\\$\\frac{{([0-9]+)}}\{{([0-9]+)}}\\\$', "분수 패턴"),
            (rf'\({i}\)\s*\\\$([^\\\$]+)\\\$', "일반 패턴"),
            (rf'\({i}\)\s*([0-9]+)(?=\\\\)', "숫자 패턴"),
        ]
        
        for pattern, desc in patterns:
            match = re.search(pattern, options_text)
            if match:
                print(f"  {desc} 성공: {match.groups()}")
                print(f"  전체 매칭: {match.group(0)}")
                break
        else:
            print(f"  모든 패턴 실패")
            # 직접 찾기
            pos = options_text.find(f'({i})')
            if pos != -1:
                print(f"  위치: {pos}")
                print(f"  주변 100자: {repr(options_text[pos:pos+100])}")
