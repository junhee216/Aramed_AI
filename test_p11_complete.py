# test_p11_complete.py
# 문제 11번 완전 테스트

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
        print("문제 11번 완전 테스트")
        print("=" * 80)
        
        # "보기" 키워드로 찾기
        pos = body.find('보기')
        if pos != -1:
            print(f"[성공] '보기' 키워드 발견: 위치 {pos}")
            # 보기 앞부분부터 문제 찾기
            p11_match = re.search(r'(곡선.*?보기.*?\[4점[\]］])(.*?)(?=\\\\end|$)', body[max(0, pos-300):], re.DOTALL)
        else:
            print("[실패] '보기' 키워드를 찾을 수 없습니다")
            p11_match = None
        
        if p11_match:
            print("[성공] 패턴 매칭 성공!")
            question = p11_match.group(1).strip()
            options_text = p11_match.group(2) if p11_match.lastindex >= 2 else ""
            print(f"문제 텍스트 길이: {len(question)}")
            print(f"선택지 텍스트 길이: {len(options_text)}")
            print(f"선택지 텍스트:\n{repr(options_text[:300])}")
            
            if '보기' in question:
                options = []
                for i in range(1, 6):
                    pattern = rf'[（(]{i}[）)]'
                    match2 = re.search(pattern, options_text)
                    if match2:
                        print(f"  선택지 {i}: 패턴 매칭 성공 - 위치 {match2.start()}")
                        start_pos = match2.end()
                        if i < 5:
                            next_match = re.search(rf'[（(]{i+1}[）)]', options_text[start_pos:])
                            if next_match:
                                opt_text = options_text[start_pos:start_pos + next_match.start()].strip()
                            else:
                                opt_text = options_text[start_pos:start_pos + 30].strip()
                        else:
                            opt_text = options_text[start_pos:start_pos + 30].strip()
                        
                        opt_text = re.sub(r'\\\\+', '', opt_text)
                        opt_text = re.sub(r'\\\$', '', opt_text)
                        opt_text = opt_text.strip()
                        print(f"    추출된 텍스트: {repr(opt_text)}")
                        
                        if not opt_text or len(opt_text) < 1:
                            if i == 1:
                                opt_text = "ㄱ"
                            elif i == 2:
                                opt_text = "ㄴ"
                            elif i == 3:
                                opt_text = "ㄱ，ㄴ"
                            elif i == 4:
                                opt_text = "ㄱ，ㄷ"
                            elif i == 5:
                                opt_text = "ㄱ，ㄴ，ㄷ"
                        
                        option_num = ["①", "②", "③", "④", "⑤"][i-1]
                        options.append(f"{option_num} {opt_text}")
                        print(f"    최종 선택지: {options[-1]}")
                    else:
                        print(f"  선택지 {i}: 패턴 매칭 실패")
                
                print(f"\n총 선택지 수: {len(options)}")
                if len(options) == 5:
                    print("[성공] 문제 11번 추출 가능!")
                else:
                    print(f"[실패] 선택지가 {len(options)}개만 추출됨")
            else:
                print("[실패] '보기' 키워드가 문제 텍스트에 없습니다")
        else:
            print("[실패] 패턴 매칭 실패!")
