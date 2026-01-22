# convert_su2_p7_problems_latex.py
# 수2 드릴 P7 문제 LaTeX를 딥시크용 CSV로 변환

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
최고차항의 계수가 양수인 삼차함수 $f(x)$ 와 실수 $t$ 에 대하여 함수 $g(t)$ 를

$$
g(t)=\\int_{-1}^{5}|f(x)-t| d x
$$

라 하자. 함수 $g(t)$ 가 다음 조건을 만족시킨다.\\\\
(가) 모든 실수 $t$ 에 대하여 $g(2-t)=g(2+t)$ 이다.\\\\
(나) $g(f(1))=g(f(4)) \\neq g(f(5))$\\\\
$g(f(5))=216$ 일 때, $f(6)$ 의 값을 구하시오. [4점]

\\section*{Chapter 3}
\\section*{적분}
$f(0)=0$ 이고 최고차항의 계수가 1 인 삼차함수 $f(x)$ 에 대하여 실수 전체의 집합에서 정의된 함수 $g(x)$ 가

$$
g(x)=\\int_{2-x}^{2+x} f(t) d t
$$

이다. 두 함수 $f(x), g(x)$ 가 다음 조건을 만족시킨다.\\\\
(가) 모든 실수 $x$ 에 대하여

$$
g(x+1)-g(x)=2 f(2)>0
$$

이다.\\\\
(나) 방정식 $f(x)=g(x)$ 의 서로 다른 실근의 개수는 2 이다.\\\\
$f(3)$ 의 값을 구하시오. [4점]

\\section*{Chapter 3}
\\section*{적분}
$f(-2)=0$ 인 이차함수 $f(x)$ 와 정의역이 실수 전체의 집합이고 치역이 $\\{0, a\\}(a>0)$ 인 함수 $g(x)$ 가 다음 조건을 만족시킨다.\\\\
(가) 함수 $f(x) g(x)$ 는 실수 전체의 집합에서 연속이다.\\\\
(나) 모든 실수 $x$ 에 대하여

$$
\\int_{-3}^{g(x)} f(t) d t=1, \\quad \\int_{-3}^{g(x)}|f(t) g(t)| d t=a
$$

이다.\\\\
$\\{f(4)\\}^{2}$ 의 값을 구하시오. [4점]

\\section*{Chapter 3}
\\section*{적분}
시각 $t=0$ 일 때 원점을 출발하여 수직선 위를 움직이는 점 P 가 있다. 점 P 의 시각 $t(t \\geq 0)$ 에서의 속도\\\\
$v(t)$ 가 상수 $a, b$ 에 대하여

$$
v(t)=a t^{2}+b t(a<0, b>0)
$$

이다. 시각 $t=k$ 에서 점 P 의 위치가 4 인 양수 $k$ 의 값이 2 뿐일 때, $a+b$ 의 값은? [4점]\\\\
(1) 3\\\\
(2) 4\\\\
(3) 5\\\\
(4) 6\\\\
(5) 7

\\section*{Chapter 3 \\\\
 적분}
수직선 위를 움직이는 두 점 $\\mathrm{P}, \\mathrm{Q}$ 의 시각 $t(t \\geq 0)$ 에서의 속도가 각각

$$
v_{1}(t)=3 t^{2}-12 t+9, \\quad v_{2}(t)=a
$$

이다. 두 점 $\\mathrm{P}, \\mathrm{Q}$ 는 출발한 후 시각 $t=2$ 와 시각 $t=4$ 에서 만난다. 시각 $t=a$ 에서 $t=a+3$ 까지 점 P 가 움직인 거리는? (단, $a$ 는 양수이다.) [4점]\\\\
(1) $\\frac{13}{2}$\\\\
(2) 7\\\\
(3) $\\frac{15}{2}$\\\\
(4) 8\\\\
(5) $\\frac{17}{2}$

\\section*{Chapter 3 \\\\
 적분}
수직선 위를 움직이는 두 점 $\\mathrm{P}, \\mathrm{Q}$ 에 대하여 점 P 의 시각 $t(t \\geq 0)$ 에서의 위치 $x(t)$ 가

$$
x(t)=t^{3}+a t^{2}+b t(a, b \\text { 는 상수 })
$$

이고, 점 Q 는 시각 $t=0$ 에서 점 A 를 출발하여 일정한 속도 -8 로 움직인다. 두 점 $\\mathrm{P}, \\mathrm{Q}$ 가 다음 조건을 만족시킬 때, 점 A 의 좌표를 구하시오. [4점]\\\\
(가) 점 P 는 시각 $t=3$ 과 시각 $t=k(k>3)$ 에서 운동 방향을 바꾼다.\\\\
(나) 시각 $t=3$ 과 시각 $t=k$ 에서 각각 두 점 $\\mathrm{P}, \\mathrm{Q}$ 의 위치는 같다.


\\end{document}"""


def extract_problems_from_latex(latex_content, debug=False):
    """LaTeX에서 문제 추출 (최적화 버전)"""
    problems = []
    
    # 본문 추출
    body = extract_body(latex_content)
    
    # 사전 컴파일된 정규식
    point_pattern = re.compile(r'\[4점\]|\[3점\]|［4점］|［3점］')
    options_pattern = re.compile(r'\([1-5]\)|（[1-5]）|①|②|③|④|⑤')
    
    # 점수 마커 찾기
    markers = []
    for match in point_pattern.finditer(body):
        point = 4 if '[4점]' in match.group() or '［4점］' in match.group() else 3
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
        r'최고차항의 계수가 양수인 삼차함수',
        r'\$f\(0\)=0\$ 이고 최고차항의 계수가 1 인 삼차함수',
        r'\$f\(-2\)=0\$ 인 이차함수',
        r'시각 \$t=0\$ 일 때 원점을 출발하여',
        r'수직선 위를 움직이는 두 점',
        r'다항함수 \$f\(x\)',
        r'함수 \$f\(x\)',
        r'삼차함수 \$f\(x\)',
        r'이차함수 \$f\(x\)',
        r'최고차항의 계수가',
        r'상수 \$a',
        r'최고차항의 계수가 1',
        r'최고차항의 계수가 음수',
        r'두 양수',
        r'실수 전체의 집합',
        r'\$0<a<1\$',
        r'\$f\(0\)=0\$',
        r'\$f\(-2\)=0\$',
        r'시각',
        r'수직선',
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
        search_area_start = max(0, problem_start - 600)
        search_area_text = body[search_area_start:pos]
        # 가장 가까운 문제 시작 패턴 찾기 (우선순위 순서대로)
        best_match = None
        best_pos = problem_start
        for pattern in problem_start_patterns:
            matches = list(re.finditer(pattern, search_area_text))
            if matches:
                # 마지막 매치를 사용 (가장 가까운 것)
                match = matches[-1]
                match_pos = search_area_start + match.start()
                # 문제 시작점이 현재 마커보다 앞에 있어야 함
                if match_pos < pos and match_pos >= problem_start - 600:
                    if best_pos == problem_start or match_pos > best_pos:
                        best_match = match
                        best_pos = match_pos
                        # 우선순위가 높은 패턴을 찾았으면 중단
                        break
        
        if best_match and best_pos < pos:
            problem_start = best_pos
        
        # 문제 끝: 다음 마커 이전 또는 문서 끝
        # 보기 문제의 경우 선택지가 다음 섹션에 있을 수 있으므로 범위 확장
        if i < len(markers):
            next_pos = markers[i][0]
            # "고른 것은"이 있으면 보기 문제일 가능성이 높으므로 범위 확장
            check_text = body[max(0, pos-200):pos+200]
            if '고른 것은' in check_text or '〈보기〉' in check_text:
                problem_end = next_pos + 300  # 보기 문제는 범위 확장
            else:
                # 다음 마커 이전까지, 단 선택지가 있으면 다음 마커까지 포함
                problem_end = next_pos - 50
                # 선택지가 있는 경우 다음 마커까지 포함
                if options_pattern.search(body[pos:next_pos]):
                    problem_end = next_pos
                # 다음 섹션이 있으면 그 전까지
                next_section = body.find('\\section', pos)
                if next_section != -1 and next_section < next_pos:
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
        question = re.sub(r'Chapter 3[^가-힣]*적분', '', question)
        question = re.sub(r'^적분\s+', '', question)  # 시작 부분의 "적분" 제거
        question = question.strip()
        
        # 주제 판단
        topic = "적분"  # 기본값
        
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
                # 전체 options_part와 다음 섹션까지 검색
                # 다음 문제 시작 전까지 검색 범위 확장
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
        
        # 문제 추가 (중복 제거)
        if len(question) > 30:  # 최소 길이 필터링
            # 중복 문제 확인 (동일한 질문이 이미 있는지)
            is_duplicate = False
            for existing_problem in problems:
                # 질문의 처음 100자 비교
                existing_q_start = existing_problem.get('question', '')[:100]
                current_q_start = question[:100]
                if existing_q_start == current_q_start and len(existing_q_start) > 50:
                    is_duplicate = True
                    break
            
            if not is_duplicate:
                problem_entry = {
                    "index": f"{len(problems)+1:02d}",
                    "page": (len(problems) // 2) + 1,
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
    print("[수2 드릴 P7 문제 LaTeX → CSV 변환]")
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
    base_dir = Path(r'C:\Users\a\Documents\MathPDF\organized\현우진\수2_2005학년도_현우진_드릴')
    base_filename = "수2_2025학년도_현우진_드릴_P7_문제"
    csv_path, json_path = save_for_deepseek(problems, base_dir, base_filename)
    
    print("\n" + "=" * 60)
    print("[완료] 딥시크가 읽을 수 있는 형태로 저장되었습니다.")
    print("=" * 60)
    print(f"저장 위치: {base_dir}")
    print(f"  - CSV: {csv_path.name}")
    print(f"  - JSON: {json_path.name}")


if __name__ == '__main__':
    main()
