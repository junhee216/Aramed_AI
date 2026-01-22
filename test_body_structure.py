# test_body_structure.py
# body 구조 확인

import re

# LaTeX 내용 읽기
with open('convert_su1_p2_problems_latex.py', 'r', encoding='utf-8') as f:
    content = f.read()

# latex_content 추출
match = re.search(r'latex_content = """(.*?)"""', content, re.DOTALL)
if match:
    latex_content = match.group(1)
    
    # 본문만 추출
    begin_match = re.search(r'\\begin\{document\}', latex_content)
    end_match = re.search(r'\\end\{document\}', latex_content)
    if begin_match and end_match:
        body = latex_content[begin_match.end():end_match.start()]
        
        print("=" * 80)
        print("body 처음 500자:")
        print("=" * 80)
        print(repr(body[:500]))
        print("\n" + "=" * 80)
        print("문제 1번 패턴 테스트:")
        print("=" * 80)
        
        # 패턴 테스트
        patterns = [
            (r'(\$a>1\$ 인 상수.*?\[4점\])(.*?)(?=\\\\section)', "기본 패턴 ($)"),
            (r'(\\\$a>1\\\$ 인 상수.*?\[4점\])(.*?)(?=\\\\section)', "이스케이프 패턴 (\\$)"),
        ]
        
        for pattern, desc in patterns:
            print(f"\n{desc}:")
            match2 = re.search(pattern, body, re.DOTALL)
            if match2:
                print(f"  [성공] 매칭 성공!")
                print(f"  문제 텍스트 길이: {len(match2.group(1))}")
                print(f"  선택지 텍스트 길이: {len(match2.group(2)) if match2.lastindex >= 2 else 0}")
                if match2.lastindex >= 2:
                    options_text = match2.group(2)
                    print(f"  선택지 텍스트:\n{repr(options_text[:300])}")
            else:
                print(f"  [실패] 매칭 실패")
