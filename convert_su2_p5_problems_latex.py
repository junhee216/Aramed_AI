# convert_su2_p5_problems_latex.py
# 수2 드릴 P5 문제 LaTeX를 딥시크용 CSV로 변환

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
\\IfFontExistsTF{Noto Serif CJK TC}
{\\setCJKfallbackfamilyfont{\\CJKrmdefault}{Noto Serif CJK TC}}
{\\IfFontExistsTF{STSong}
  {\\setCJKfallbackfamilyfont{\\CJKrmdefault}{STSong}}
  {\\IfFontExistsTF{Droid Sans Fallback}
    {\\setCJKfallbackfamilyfont{\\CJKrmdefault}{Droid Sans Fallback}}
    {\\setCJKfallbackfamilyfont{\\CJKrmdefault}{SimSun}}
}}

\\setmainlanguage{english}
\\IfFontExistsTF{CMU Serif}
{\\setmainfont{CMU Serif}}
{\\IfFontExistsTF{DejaVu Sans}
  {\\setmainfont{DejaVu Sans}}
  {\\setmainfont{Georgia}}
}

\\begin{document}
\\section*{Chapter 3}
\\section*{적분}
다항함수 $f(x)$ 가 모든 실수 $x$ 에 대하여

$$
f(x)+\\int_{0}^{1} x^{4} f(t) d t=x^{2}+\\int_{-1}^{1} f(t) d t
$$

를 만족시킬 때, $f(2)$ 의 값은? [4점]\\\\
(1) $\\frac{55}{6}$\\\\
(2) $\\frac{19}{2}$\\\\
(3) $\\frac{59}{6}$\\\\
(4) $\\frac{61}{6}$\\\\
(5) $\\frac{21}{2}$

\\section*{Chapter 3}
적분

함수 $f(x)=3 x^{2}+a x+1$ 이 모든 실수 $x$ 에 대하여

$$
f(x) \\geq f\\left(\\int_{0}^{1} f(t) d t\\right)
$$

를 만족시킬 때, $f(a)$ 의 값을 구하시오. (단, $a$ 는 상수이다.) [4점]

\\section*{Chapter 3 \\\\
 적분}
최고차항의 계수가 1 인 삼차함수 $f(x)$ 가 다음 조건을 만족시킨다.\\\\
(가) $\\int_{0}^{1} f^{\\prime}(x) d x=\\int_{1}^{2} f^{\\prime}(x) d x=f(1)$\\\\
(나) $\\int_{1}^{2}\\left|f^{\\prime}(x)\\right| d x=f(1)+f(2)$\\\\
$f(4)$ 의 값을 구하시오. [4점]

\\section*{Chapter 3 \\\\
 적분}
최고차항의 계수가 양수인 이차함수 $f(x)$ 에 대하여

$$
\\int_{0}^{k} f(x) d x=\\int_{k}^{k+1} f(k) f(x) d x
$$

를 만족시키는 모든 실수 $k$ 의 집합을 $A$ 라 하자．\\\\
$0 \\in A$ 일 때，〈보기〉에서 옳은 것만을 있는 대로 고른 것은？［4점］\\\\
〈보기〉\\\\
ㄱ．방정식 $f(x)=0$ 의 실근이 구간 $[0,1)$ 에 적어도 하나 존재한다．\\\\
ㄴ． $1 \\in A$ 이고 방정식 $f(x)=0$ 의 음의 실근이 존재하면 $f(1)<1$ 이다．\\\\
ᄃ．$\\{-1,1\\} \\subset A$ 이면 $f(-5)=\\frac{13}{5}$ 이다．\\\\
（1）ᄀ\\\\
（2）ᄀ，ᄂ\\\\
（3）ㄱ，ㄷ\\\\
（4）ᄂ，ᄃ\\\\
（5）ᄀ，ᄂ，ᄃ

\\section*{Chapter 3}
\\section*{적분}
다항함수 $f(x)$ 가 모든 실수 $x$ 에 대하여

$$
f(x)+a x+b=\\int_{0}^{x}\\left\\{f(t)-t^{3}\\right\\} d t
$$

를 만족시킨다. $f(1)=12$ 일 때, $f(b-a)$ 의 값은? (단, $a, b$ 는 상수이다.) [4점]\\\\
(1) 22\\\\
(2) 26\\\\
(3) 30\\\\
(4) 34\\\\
(5) 38

\\section*{Chapter 3 \\\\
 적분}
$f(1)>0$ 인 다항함수 $f(x)$ 가 상수 $a(a>0)$ 와 모든 실수 $x$ 에 대하여

$$
a \\int_{0}^{x} f(t) d t=f(1) x^{4}-2 f(-1) x^{2}
$$

을 만족시킨다. 곡선 $y=f(x)$ 와 $x$ 축 및 두 직선 $x=1, x=2$ 로 둘러싸인 부분의 넓이가 42 일 때, $f(a-6)$ 의 값을 구하시오. [4점]

\\section*{Chapter 3 \\\\
 적분}
삼차함수 $f(x)$ 는 $f(0)>0$ 을 만족시킨다．함수 $g(x)$ 를

$$
g(x)=\\left|\\int_{0}^{x} f(t) d t\\right|
$$

라 하자．함수 $y=g(x)$ 의 그래프는 그림과 같고，함수 $g(x)$ 는 $x=2$ 에서 극댓값，$x=3$ 에서 극솟값을 갖는다．\\\\
\\includegraphics[max width=\\textwidth, center]{d152a808-44a9-4ba7-8954-2547bc6d6879-07_381_502_1017_909}

〈보기〉에서 옳은 것만을 있는 대로 고른 것은？［4점］

\\section*{〈보기〉}
ㄱ．방정식 $f(x)=0$ 의 서로 다른 실근의 개수는 2 이다．\\\\
ㄴ．$f^{\\prime}(-2)>0$\\\\
ㄷ．함수 $y=f(x)$ 는 열린구간 $(2,3)$ 에서 극솟값을 갖는다．\\\\
（1）ᄂ\\\\
（2）ᄃ\\\\
（3）ᄀ，ᄂ\\\\
（4）ㄴ，ㄷ\\\\
（5）ᄀ，ᄂ，ᄃ

\\section*{Chapter 3}
적분

이차함수 $f(x)$ 가 다음 조건을 만족시킨다.\\\\
(가) 모든 실수 $x$ 에 대하여 $(x-1) \\int_{1}^{x} f(t) d t \\geq 0$ 이다.\\\\
(나) 모든 실수 $x$ 에 대하여 $f(x) \\geq 3 x-12$ 이다.\\\\
$\\int_{1}^{4} f(x) d x=0$ 일 때, $f(6)$ 의 값을 구하시오. [4점]

\\section*{Chapter 3 \\\\
 적분}
상수 $a$ 에 대하여 함수 $f(x)=x^{3}-(a+4) x^{2}+4 a x$ 와 실수 전체의 집합에서 미분가능한 함수 $g(x)$ 가 모든 실수 $x$ 에 대하여

$$
|g(x)|=\\int_{a}^{x} f(t) d t
$$

를 만족시킨다. 함수 $g(x)$ 가 오직 하나의 극값 $k(k>0)$ 를 갖고, $g^{\\prime}(3)>0$ 일 때, $a+k$ 의 값은? [4점]\\\\
(1) 60\\\\
(2) 63\\\\
(3) 66\\\\
(4) 69\\\\
(5) 72

\\section*{Chapter 3 \\\\
 적분}
최고차항의 계수가 양수이고 $f(0)<0$ 인 이차함수 $f(x)$ 에 대하여 부등식

$$
\\int_{0}^{x} f(t) d t \\times\\left\\{\\int_{1}^{x} f(t) d t+x-1\\right\\} \\leq 0
$$

의 해가 $-1 \\leq x \\leq 3$ 일 때, $\\int_{0}^{5} f(x) d x$ 의 값을 구하시오. [4점]

\\section*{Chapter 3}
\\section*{적분}
최고차항의 계수가 1 인 두 이차함수 $f(x), g(x)$ 에 대하여 실수 전체의 집합에서 정의된 함수

$$
h(x)=\\int_{k}^{x}\\{f(x)-f(t)\\} g(t) d t
$$

가 있다. 함수 $h(x)$ 가 극값을 갖지 않도록 하는 실수 $k$ 의 값은 $a, a+3$ 뿐이고

$$
g(a)=0, \\quad \\lim _{x \\rightarrow 0} \\frac{f(x)+g(x)}{x}=4 a
$$

일 때, $f(5) \\times g(5)$ 의 값을 구하시오. (단, $a$ 는 상수이다.) [4점]

\\section*{Chapter 3}
\\section*{적분}
최고차항의 계수가 양수인 삼차함수 $f(x)$ 가 역함수 $g(x)$ 를 갖는다. 함수

$$
h(x)=\\int_{0}^{x}\\{f(t)-g(t)\\} d t
$$

가

$$
\\lim _{x \\rightarrow 0} \\frac{h(x)}{x}=\\lim _{x \\rightarrow 2} \\frac{h(x)}{x-2}=0
$$

을 만족시킬 때, $f(3)$ 의 최댓값을 구하시오. [4점]


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
    
    # 문제 시작 패턴
    problem_start_patterns = [
        r'다항함수 \$f\(x\)',
        r'함수 \$f\(x\)',
        r'삼차함수 \$f\(x\)',
        r'이차함수 \$f\(x\)',
        r'최고차항의 계수가',
        r'상수 \$a',
        r'최고차항의 계수가 양수',
        r'최고차항의 계수가 1',
    ]
    
    # 각 점수 마커 주변에서 문제 추출
    for i, (pos, point) in enumerate(markers, 1):
        # 문제 시작: 이전 마커 이후 또는 문서 시작
        if i > 1:
            prev_pos = markers[i-2][0]
            # 이전 마커의 끝 찾기
            prev_marker_end = prev_pos
            prev_match = point_pattern.search(body[prev_pos:prev_pos+100])
            if prev_match:
                prev_marker_end = prev_pos + prev_match.end()
            # 이전 문제의 선택지 끝 찾기
            search_start = max(0, prev_marker_end - 300)
            search_end = prev_marker_end + 200
            search_area = body[search_start:search_end]
            
            # 이전 문제의 마지막 선택지 패턴 찾기
            last_option_match = None
            for opt_num in range(5, 0, -1):
                pattern = rf'（{opt_num}）|\({opt_num}\)'
                match = re.search(pattern, search_area)
                if match:
                    last_option_match = search_start + match.end()
                    break
            
            if last_option_match:
                problem_start = last_option_match + 50
            else:
                problem_start = prev_marker_end + 50
        else:
            problem_start = 0
        
        # 현재 마커 이전의 마지막 섹션 찾기
        for sec_pos in reversed(sections):
            if sec_pos < pos and sec_pos >= problem_start - 200:
                # 섹션 헤더 끝 찾기
                section_end = body.find('}', sec_pos)
                if section_end != -1:
                    # 섹션 이후에 문제 시작 패턴 찾기
                    after_section = body[section_end+1:pos]
                    for pattern in problem_start_patterns:
                        match = re.search(pattern, after_section)
                        if match:
                            problem_start = section_end + 1 + match.start()
                            break
                    if problem_start < section_end + 1:
                        problem_start = section_end + 1
                break
        
        # 문제 시작 패턴으로 정확한 시작점 찾기
        search_area_start = max(0, problem_start - 300)
        search_area_text = body[search_area_start:pos]
        for pattern in problem_start_patterns:
            match = re.search(pattern, search_area_text)
            if match:
                problem_start = search_area_start + match.start()
                break
        
        # 문제 끝: 다음 마커 이전 또는 문서 끝
        # 보기 문제의 경우 선택지가 다음 섹션에 있을 수 있으므로 범위 확장
        if i < len(markers):
            next_pos = markers[i][0]
            # "고른 것은"이 있으면 보기 문제일 가능성이 높으므로 범위 확장
            if '고른 것은' in body[max(0, pos-200):pos+200]:
                problem_end = next_pos + 200  # 보기 문제는 범위 확장
            else:
                problem_end = next_pos - 50
        else:
            problem_end = len(body)
        
        problem_text_raw = body[problem_start:problem_end].strip()
        
        # 점수 마커를 기준으로 문제와 선택지 분리
        point_match_in_text = point_pattern.search(problem_text_raw)
        if not point_match_in_text:
            continue
        
        question_part = problem_text_raw[:point_match_in_text.start()].strip()
        options_part = problem_text_raw[point_match_in_text.start():].strip()
        
        # 텍스트 정리
        question = clean_latex_text(question_part)
        
        # 섹션 헤더 제거 (문제 본문에 포함되지 않도록)
        question = re.sub(r'\\section\*?\{[^}]*\}', '', question)
        question = re.sub(r'Chapter 3[^가-힣]*적분', '', question)
        question = re.sub(r'^적분\s+', '', question)  # 시작 부분의 "적분" 제거
        question = question.strip()
        
        # 문제 시작 부분이 잘린 경우 복구 시도
        if (question.startswith('}+') or question.startswith('}$') or 
            question.startswith('ction*') or question.startswith('f(x)$') or
            question.startswith(')=x') or len(question) < 50):
            # 이전 텍스트에서 문제 시작 찾기
            search_back = body[max(0, problem_start - 400):problem_start]
            for pattern in problem_start_patterns:
                match = re.search(pattern, search_back)
                if match:
                    # 찾은 부분부터 현재까지
                    full_question = search_back[match.start():] + question_part
                    question = clean_latex_text(full_question)
                    question = re.sub(r'\\section\*?\{[^}]*\}', '', question)
                    question = re.sub(r'Chapter 3[^가-힣]*적분', '', question)
                    question = re.sub(r'^적분\s+', '', question)
                    question = question.strip()
                    break
        
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
                options = extract_options_generic(options_part, num_options=5)
                
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
    print("[수2 드릴 P5 문제 LaTeX → CSV 변환]")
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
    base_filename = "수2_2025학년도_현우진_드릴_P5_문제"
    csv_path, json_path = save_for_deepseek(problems, base_dir, base_filename)
    
    print("\n" + "=" * 60)
    print("[완료] 딥시크가 읽을 수 있는 형태로 저장되었습니다.")
    print("=" * 60)
    print(f"저장 위치: {base_dir}")
    print(f"  - CSV: {csv_path.name}")
    print(f"  - JSON: {json_path.name}")


if __name__ == '__main__':
    main()
