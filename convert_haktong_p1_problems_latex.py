# convert_haktong_p1_problems_latex.py
# 확통 드릴 P1 문제 LaTeX를 딥시크용 CSV로 변환

import re
import sys
import os
from pathlib import Path
from latex_utils import (
    extract_body, extract_options_generic, clean_latex_text
)
from convert_template import review_problems, save_for_deepseek

# Windows 콘솔 인코딩 설정
if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')

# Mathpix에서 온 LaTeX 내용
latex_content = """% This LaTeX document needs to be compiled with XeLaTeX.
\\documentclass[10pt]{article}
\\usepackage[utf8]{inputenc}
\\usepackage{amsmath}
\\usepackage{amsfonts}
\\usepackage{amssymb}
\\usepackage[version=4]{mhchem}
\\usepackage{stmaryrd}
\\usepackage{graphicx}
\\usepackage[export]{adjustbox}
\\graphicspath{ {./images/} }
\\usepackage[fallback]{xeCJK}
\\usepackage{polyglossia}
\\usepackage{fontspec}
\\IfFontExistsTF{Noto Serif CJK KR}
{\\setCJKmainfont{Noto Serif CJK KR}}
{\\IfFontExistsTF{Apple SD Gothic Neo}
  {\\setCJKmainfont{Apple SD Gothic Neo}}
  {\\IfFontExistsTF{UnDotum}
    {\\setCJKmainfont{UnDotum}}
    {\\setCJKmainfont{Malgun Gothic}}
}}

\\setmainlanguage{english}
\\IfFontExistsTF{CMU Serif}
{\\setmainfont{CMU Serif}}
{\\IfFontExistsTF{DejaVu Sans}
  {\\setmainfont{DejaVu Sans}}
  {\\setmainfont{Georgia}}
}

\\begin{document}
\\section*{Chapter 1}
\\section*{경우의 수}
\\section*{(11)}
4 개의 숫자 $1,2,2,4$ 와 3 개의 문자 $a, a, b$ 가 있다. 이 7 개를 모두 일렬로 나열할 때, 첫 번째 수와 두 번째 수의 곱이 세 번째 수와 네 번째 수의 곱보다 작은 경우의 수는? [3점]\\\\
(1) 364\\\\
(2) 392\\\\
(3) 420\\\\
(4) 448\\\\
(5) 476\\\\
\\includegraphics[max width=\\textwidth, center]{ef391959-c5fd-4280-9e49-09fcf23a4e27-2_248_246_555_174}

7 개의 문자 $a, a, b, b, c, c, c$ 를 모두 일렬로 나열할 때, 다음 조건을 만족시키는 경우의 수는? [3점]\\\\
(가) 양 끝의 문자는 서로 다르다.\\\\
(나) $a$ 끼리는 서로 이웃하지 않는다.\\\\
(1) 114\\\\
(2) 116\\\\
(3) 118\\\\
(4) 120\\\\
(5) 122

\\section*{Chapter 1}
경우의 수

\\section*{03}
숫자 $1,1,2,2,3,3$ 이 하나씩 적혀 있는 6 장의 카드가 있다. 이 6 장의 카드 중 3 장을 택해 일렬로 나열 하여 만든 세 자리의 자연수를 $N_{1}$, 남은 3 장을 일렬로 나열하여 만든 세 자리의 자연수를 $N_{2}$ 라 할 때, $N_{1}-N_{2} \\geq 100$ 인 경우의 수를 구하시오. [4점]\\\\
\\includegraphics[max width=\\textwidth, center]{ef391959-c5fd-4280-9e49-09fcf23a4e27-4_252_248_538_174}

숫자 $1,2,3,4$ 중에서 중복을 허락하여 6 개를 택해 그림과 같은 6 개의 빈칸에 1 개씩 적을 때, 다음 조건을 만족시키는 경우의 수를 구하시오. [4점]\\\\
\\includegraphics[max width=\\textwidth, center]{ef391959-c5fd-4280-9e49-09fcf23a4e27-4_106_92_891_1000}\\\\
\\includegraphics[max width=\\textwidth, center]{ef391959-c5fd-4280-9e49-09fcf23a4e27-4_119_89_891_1108}\\\\
\\includegraphics[max width=\\textwidth, center]{ef391959-c5fd-4280-9e49-09fcf23a4e27-4_121_91_891_1216}\\\\
\\includegraphics[max width=\\textwidth, center]{ef391959-c5fd-4280-9e49-09fcf23a4e27-4_120_85_1028_1002}\\\\
\\includegraphics[max width=\\textwidth, center]{ef391959-c5fd-4280-9e49-09fcf23a4e27-4_120_87_1028_1108}\\\\
\\includegraphics[max width=\\textwidth, center]{ef391959-c5fd-4280-9e49-09fcf23a4e27-4_124_94_1026_1213}\\\\
(가) 2 가 적힌 칸의 개수와 4 가 적힌 칸의 개수는 각각 2 이하이다.\\\\
(나) 짝수가 적힌 모든 칸의 개수는 짝수이다.\\\\
(다) 상하로 이웃한 두 칸에 적힌 두 수의 곱은 모두 짝수이고, 좌우로 이웃한 두 칸에 적힌 두 수의 곱도 모두 짝수이다.

\\section*{Chapter 1 \\\\
 경우의 수}
\\section*{(15)}
숫자 $1,1,1,2,2,2,3,3,3,3$ 이 하나씩 적혀 있는 10 장의 카드가 있다. 이 10 장의 카드를 그림과 같은 10 개의 자리에 각각 한 장씩 다음 조건을 만족시키도록 놓는 경우의 수를 구하시오.\\\\[0pt]
(단, 같은 숫자가 적혀 있는 카드끼리는 서로 구별하지 않는다.) [4점]\\\\
\\includegraphics[max width=\\textwidth, center]{ef391959-c5fd-4280-9e49-09fcf23a4e27-5_300_483_951_906}\\\\
(가) 각 행에 적어도 1 장의 2 가 적혀 있는 카드를 놓는다.\\\\
(나) 각행에 적어도 1 장의 3 이 적혀 있는 카드를 놓는다.\\\\
(다) 각 열의 1 행에 놓인 카드에 적혀 있는 수는 2 행에 놓인 카드에 적혀 있는 수보다 크지 않다.

\\section*{Chapter 1 경우의 수}
\\begin{center}
\\includegraphics[max width=\\textwidth]{ef391959-c5fd-4280-9e49-09fcf23a4e27-6_239_244_551_189}
\\end{center}

남학생 4 명과 여학생 2 명이 있다. 이 6 명의 학생이 일정한 간격을 두고 원 모양의 탁자에 둘러앉을 때, 남학생 중 2 명만 서로 맞은편에 앉는 경우의 수는? (단, 회전하여 일치하는 것은 같은 것으로 본다.) [3점]\\\\
(1) 90\\\\
(2) 96\\\\
(3) 102\\\\
(4) 108\\\\
(5) 114\\\\
\\includegraphics[max width=\\textwidth, center]{ef391959-c5fd-4280-9e49-09fcf23a4e27-6_425_378_994_972}

그림과 같이 한 정삼각형을 서로 합동인 9 개의 정삼각형으로 나누었다. 이 9 개의 정삼각형 중 3 개의 정삼각형에 빨간색, 파란색, 노란색을 모두 사용하여 칠하려고 한다. 한 정삼각형에 한 가지 색만을 칠할 때, 다음 조건을 만족시키는 경우의 수를 구하시오. (단, 회전하여 일치하는 것은 같은 것으로 본다.) [4점]\\\\
\\includegraphics[max width=\\textwidth, center]{ef391959-c5fd-4280-9e49-09fcf23a4e27-7_326_371_955_968}\\\\
(가) 빨간색을 칠한 정삼각형과 파란색을 칠한 정삼각형은 변을 공유한다.\\\\
(나) 빨간색을 칠한 정삼각형과 노란색을 칠한 정삼각형은 변을 공유하지 않는다.


\\end{document}"""


def extract_problems_from_latex(latex_content, debug=False):
    """LaTeX에서 문제 추출"""
    problems = []
    
    # 본문 추출
    body = extract_body(latex_content)
    
    # 사전 컴파일된 정규식
    point_pattern = re.compile(r'\[3점\]|\[4점\]|［3점］|［4점］')
    options_pattern = re.compile(r'\([1-5]\)|（[1-5]）|①|②|③|④|⑤')
    
    # 점수 마커 찾기
    markers = []
    for match in point_pattern.finditer(body):
        point = 3 if '[3점]' in match.group() or '［3점］' in match.group() else 4
        markers.append((match.start(), point))
    
    if debug:
        print(f"[디버깅] 점수 마커 발견: {len(markers)}개")
    
    # 섹션 헤더 위치 찾기
    section_pattern = re.compile(r'\\section\*?\{[^}]*\}')
    sections = []
    for match in section_pattern.finditer(body):
        sections.append(match.start())
    
    # 문제 시작 패턴 (우선순위 순서)
    problem_start_patterns = [
        r'[0-9]+ 개의 숫자',
        r'[0-9]+ 개의 문자',
        r'숫자 \$[0-9, ]+\$',
        r'[0-9]+ 장의 카드',
        r'남학생',
        r'여학생',
        r'그림과 같이',
        r'한 정삼각형',
        r'경우의 수',
    ]
    
    # 각 점수 마커 주변에서 문제 추출
    for i, (pos, point) in enumerate(markers, 1):
        # 문제 시작: 이전 마커 이후 또는 문서 시작
        if i > 1:
            prev_pos = markers[i-2][0]
            # 이전 마커의 끝 찾기
            prev_marker_end = prev_pos
            prev_match = point_pattern.search(body[prev_pos:prev_pos+50])
            if prev_match:
                prev_marker_end = prev_pos + prev_match.end()
            
            # 이전 문제의 선택지 끝 찾기
            search_start = max(0, prev_marker_end - 50)
            search_end = min(len(body), prev_marker_end + 600)
            search_area = body[search_start:search_end]
            
            # 이전 문제의 마지막 선택지 패턴 찾기
            last_option_match = None
            for opt_num in range(5, 0, -1):
                pattern = rf'（{opt_num}）|\({opt_num}\)'
                match = re.search(pattern, search_area)
                if match:
                    # 선택지 텍스트 끝 찾기
                    option_text_end = search_start + match.end()
                    # 다음 섹션이나 줄바꿈까지
                    after_option = body[option_text_end:min(len(body), option_text_end + 300)]
                    section_pos = after_option.find('\\section')
                    if section_pos != -1:
                        last_option_match = option_text_end + section_pos
                    else:
                        # 줄바꿈 2개 이상이면 선택지 끝으로 간주
                        double_newline = after_option.find('\n\n')
                        if double_newline != -1:
                            last_option_match = option_text_end + double_newline
                        else:
                            # 선택지 다음 100자 이후
                            last_option_match = option_text_end + 100
                    break
            
            if last_option_match:
                problem_start = last_option_match + 10
            else:
                problem_start = prev_marker_end + 50
        else:
            problem_start = 0
        
        # 현재 마커 이전의 마지막 섹션 찾기
        for sec_pos in reversed(sections):
            if sec_pos < pos:
                # 섹션 헤더 끝 찾기
                section_end = body.find('}', sec_pos)
                if section_end != -1:
                    # 섹션 이후에 문제 시작 패턴 찾기
                    after_section = body[section_end+1:pos]
                    for pattern in problem_start_patterns:
                        match = re.search(pattern, after_section)
                        if match:
                            found_start = section_end + 1 + match.start()
                            if found_start > problem_start:
                                problem_start = found_start
                            break
                break
        
        # 문제 시작 패턴으로 정확한 시작점 찾기 (섹션 이후)
        # 이전 마커 이후부터 현재 마커까지의 범위에서 문제 시작 찾기
        if i > 1:
            prev_pos = markers[i-2][0]
            search_start = max(0, prev_pos + 100)
        else:
            search_start = 0
        
        search_area_text = body[search_start:pos]
        # 가장 가까운 문제 시작 패턴 찾기 (우선순위 순서대로)
        best_match = None
        best_pos = problem_start
        for pattern in problem_start_patterns:
            matches = list(re.finditer(pattern, search_area_text))
            if matches:
                # 마지막 매치를 사용 (가장 가까운 것)
                match = matches[-1]
                match_pos = search_start + match.start()
                # 문제 시작점이 현재 마커보다 앞에 있어야 함
                if match_pos < pos and match_pos >= search_start:
                    if best_pos < search_start or match_pos > best_pos:
                        best_match = match
                        best_pos = match_pos
                        # 우선순위가 높은 패턴을 찾았으면 중단
                        break
        
        if best_match and best_pos < pos:
            problem_start = best_pos
        
        # 문제 끝: 다음 마커 이전 또는 문서 끝
        if i < len(markers):
            next_pos = markers[i][0]
            # "고른 것은"이 있으면 보기 문제일 가능성이 높으므로 범위 확장
            check_text = body[max(0, pos-200):pos+200]
            if '고른 것은' in check_text or '〈보기〉' in check_text:
                problem_end = next_pos + 300  # 보기 문제는 범위 확장
            else:
                # 다음 마커 이전까지, 단 선택지가 있으면 다음 마커까지 포함
                problem_end = next_pos - 30  # 범위를 좁혀서 다음 문제와 겹치지 않도록
                # 선택지가 있는 경우 다음 마커까지 포함
                if options_pattern.search(body[pos:next_pos]):
                    problem_end = next_pos - 20
                # 다음 섹션이 있으면 그 전까지 (단, 선택지가 있으면 섹션 전까지)
                next_section = body.find('\\section', pos)
                if next_section != -1 and next_section < next_pos:
                    # 선택지가 없으면 섹션 전까지
                    if not options_pattern.search(body[pos:next_pos]):
                        problem_end = min(problem_end, next_section)
        else:
            problem_end = len(body)
        
        problem_text_raw = body[problem_start:problem_end].strip()
        
        # 점수 마커를 기준으로 문제와 선택지 분리
        point_match_in_text = point_pattern.search(problem_text_raw)
        if not point_match_in_text:
            continue
        
        question_part = problem_text_raw[:point_match_in_text.start()].strip()
        options_part = problem_text_raw[point_match_in_text.start():].strip()
        
        # 문제 시작 부분이 잘린 경우 복구 시도
        if (question_part.startswith('}+') or question_part.startswith('}$') or 
            question_part.startswith('ction*') or question_part.startswith('f(x)$') or
            question_part.startswith(')=x') or len(question_part) < 30):
            # 이전 텍스트에서 문제 시작 찾기
            search_back = body[max(0, problem_start - 500):problem_start]
            for pattern in problem_start_patterns:
                match = re.search(pattern, search_back)
                if match:
                    # 찾은 부분부터 현재까지
                    full_question_part = search_back[match.start():] + question_part
                    question_part = full_question_part
                    break
        
        # 텍스트 정리
        question = clean_latex_text(question_part)
        
        # 섹션 헤더 제거 (문제 본문에 포함되지 않도록)
        question = re.sub(r'\\section\*?\{[^}]*\}', '', question)
        question = re.sub(r'Chapter 1[^가-힣]*경우의 수', '', question)
        question = re.sub(r'^경우의 수\s+', '', question)  # 시작 부분의 "경우의 수" 제거
        question = question.strip()
        
        # 주제 판단
        topic = "경우의 수"  # 기본값
        
        # 선택지 추출
        options = []
        has_options = bool(options_pattern.search(options_part))
        
        # 보기 문제 확인 ("고른 것은?"이 있으면 객관식)
        is_boogi_problem = '〈보기〉' in options_part or '보기' in question or '고른 것은' in question
        
        # 주관식 문제 확인
        # "구하시오"가 있고 선택지 패턴이 없으면 주관식
        # 단, "고른 것은?"이 있으면 객관식
        if '고른 것은' in question or is_boogi_problem:
            # 보기 문제는 무조건 객관식
            has_options = True
        elif '구하시오' in question:
            # options_part에서 선택지 패턴이 실제로 있는지 확인
            actual_options = options_pattern.findall(options_part)
            if len(actual_options) == 0:
                has_options = False
            else:
                # 선택지가 제대로 추출되는지 확인
                has_options = True
        elif not has_options:
            # 선택지 패턴이 없으면 주관식
            has_options = False
        elif has_options:
            # '〈보기〉'가 포함된 문제 처리
            if is_boogi_problem or '\\section\\*\\{〈보기〉' in options_part:
                # 보기 내용 추출 (섹션 헤더 포함)
                boogi_patterns = [
                    r'\\section\*\{〈보기〉\}(.*?)(?=（[1-5]）|$|\\section)',
                    r'〈보기〉(.*?)(?=（[1-5]）|$|\\section)',
                ]
                boogi_content = ""
                for pattern in boogi_patterns:
                    boogi_match = re.search(pattern, options_part, re.DOTALL)
                    if boogi_match:
                        boogi_content = clean_latex_text(boogi_match.group(1))
                        question += f" 〈보기〉 {boogi_content}"
                        break
                
                # 선택지 (1)~(5) 추출 (전각 괄호 우선)
                search_text = options_part
                if i < len(markers):
                    next_pos = markers[i][0]
                    search_text = body[problem_start:min(next_pos, problem_end + 500)]
                
                found_options = {}
                for opt_num in range(1, 6):
                    # 전각 괄호: （1）~（5）
                    pattern1 = rf'（{opt_num}）\s*([^（]+?)(?=（[1-5]）|$|\\section|\\end)'
                    # 반각 괄호: (1)~(5)
                    pattern2 = rf'\({opt_num}\)\s*([^(]+?)(?=\([1-5]\)|$|\\section|\\end)'
                    
                    # search_text 전체에서 검색
                    match1 = re.search(pattern1, search_text, re.DOTALL)
                    match2 = re.search(pattern2, search_text, re.DOTALL)
                    match = match1 or match2
                    
                    if match:
                        option_text = clean_latex_text(match.group(1))
                        # 보기 내용이 선택지에 포함되지 않도록 확인
                        # 선택지가 ㄱ,ㄴ,ㄷ 조합이어야 함
                        if ('ㄱ' in option_text or 'ㄴ' in option_text or 'ㄷ' in option_text or 
                            'ᄀ' in option_text or 'ᄂ' in option_text or 'ᄃ' in option_text):
                            found_options[opt_num] = option_text
                
                # 순서대로 정렬
                for opt_num in sorted(found_options.keys()):
                    options.append(f"{['①', '②', '③', '④', '⑤'][opt_num-1]} {found_options[opt_num]}")
            else:
                # 일반 객관식 문제
                # options_part에서 선택지 추출 시 다음 마커까지 포함
                if i < len(markers):
                    next_pos = markers[i][0]
                    extended_options_text = body[pos:min(next_pos, pos + 1000)]
                else:
                    extended_options_text = options_part
                
                options = extract_options_generic(extended_options_text, num_options=5)
                
                # 선택지가 제대로 추출되지 않았고 "구하시오"가 있으면 주관식으로 변경
                if len(options) == 0 and '구하시오' in question:
                    has_options = False
        
        # 문제 추가
        if len(question) > 30:  # 최소 길이 필터링
            problem_entry = {
                "index": f"{i:02d}",
                "page": (i // 2) + 1,
                "topic": topic,
                "question": question,
                "point": point,
                "answer_type": "multiple_choice" if has_options and len(options) > 0 else "short_answer"
            }
            if has_options and len(options) > 0:
                problem_entry["options"] = options
            problems.append(problem_entry)
    
    return problems


def main():
    print("=" * 60)
    print("[확통 드릴 P1 문제 LaTeX → CSV 변환]")
    print("=" * 60)
    
    # 1단계: LaTeX 읽기
    print(f"\n[1단계] LaTeX 내용 읽기 완료 ({len(latex_content)}자)")
    
    # 2단계: 문제 추출
    print("\n[2단계] 문제 추출 중...")
    problems = extract_problems_from_latex(latex_content, debug=True)
    print(f"[완료] {len(problems)}개 문제 추출됨")
    
    # 3단계: 검토 (수학적 논리 포함)
    print("\n[3단계] 문제 검토 중...")
    is_valid = review_problems(problems)
    
    # 4단계: 저장
    print("\n[4단계] 딥시크용 파일 저장 중...")
    base_dir = Path(r'C:\Users\a\Documents\MathPDF\organized\현우진\확통_2005학년도_현우진_드릴')
    base_filename = "확통_2024학년도_현우진_드릴_P1_문제"
    csv_path, json_path = save_for_deepseek(problems, base_dir, base_filename)
    
    print("\n" + "=" * 60)
    print("[완료] 딥시크가 읽을 수 있는 형태로 저장되었습니다.")
    print("=" * 60)
    print(f"저장 위치: {base_dir}")
    print(f"  - CSV: {csv_path.name}")
    print(f"  - JSON: {json_path.name}")


if __name__ == '__main__':
    main()
