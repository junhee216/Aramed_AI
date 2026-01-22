# test_p1_complete.py
# 문제 1번 완전 테스트

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
        print("문제 1번 완전 테스트")
        print("=" * 80)
        
        # 패턴 테스트
        p1_match = re.search(r'(\\\$a>1\\\$ 인 상수.*?\[4점\])(.*?)(?=\\\\section)', body, re.DOTALL)
        
        if p1_match:
            print("[성공] 패턴 매칭 성공!")
            question = p1_match.group(1).strip()
            options_text = p1_match.group(2) if p1_match.lastindex >= 2 else ""
            print(f"문제 텍스트 길이: {len(question)}")
            print(f"선택지 텍스트 길이: {len(options_text)}")
            
            options = []
            for i in range(1, 6):
                patterns = [
                    rf'\({i}\)\s*\\\$\\\\frac{{([0-9]+)}}\{{([0-9]+)}}\\\$',
                    rf'\({i}\)\s*([0-9]+)(?=\\\\\\\\)',
                ]
                match2 = None
                for pattern in patterns:
                    match2 = re.search(pattern, options_text)
                    if match2:
                        break
                
                if match2:
                    option_num = ["①", "②", "③", "④", "⑤"][i-1]
                    if len(match2.groups()) == 2 and match2.group(1).isdigit() and match2.group(2).isdigit():
                        opt_text = f"\\frac{{{match2.group(1)}}}{{{match2.group(2)}}}"
                        options.append(f"{option_num} ${opt_text}$")
                    else:
                        options.append(f"{option_num} {match2.group(1)}")
                    print(f"  선택지 {i}: {options[-1]}")
                else:
                    print(f"  선택지 {i}: 추출 실패")
            
            print(f"\n총 선택지 수: {len(options)}")
            if len(options) == 5:
                print("[성공] 문제 1번 추출 가능!")
            else:
                print(f"[실패] 선택지가 {len(options)}개만 추출됨")
        else:
            print("[실패] 패턴 매칭 실패!")
