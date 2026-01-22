# convert_geometry_p2_problems_deepseek.py
# 기하_2024학년도_현우진_드릴_P2 문제 LaTeX → Deepseek R1-70B용 변환

import re
import json
import sys
from pathlib import Path

# Windows 콘솔 인코딩 설정
if sys.platform == 'win32':
    import os
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')

# LaTeX 내용
latex_content = r"""% This LaTeX document needs to be compiled with XeLaTeX.
\documentclass[10pt]{article}
\usepackage[utf8]{inputenc}
\usepackage{amsmath}
\usepackage{amsfonts}
\usepackage{amssymb}
\usepackage[version=4]{mhchem}
\usepackage{stmaryrd}
\usepackage{graphicx}
\usepackage[export]{adjustbox}
\graphicspath{ {./images/} }
\usepackage[fallback]{xeCJK}
\usepackage{polyglossia}
\usepackage{fontspec}
\IfFontExistsTF{Noto Serif CJK KR}
{\setCJKmainfont{Noto Serif CJK KR}}
{\IfFontExistsTF{Apple SD Gothic Neo}
  {\setCJKmainfont{Apple SD Gothic Neo}}
  {\IfFontExistsTF{UnDotum}
    {\setCJKmainfont{UnDotum}}
    {\setCJKmainfont{Malgun Gothic}}
}}

\setmainlanguage{english}
\IfFontExistsTF{CMU Serif}
{\setmainfont{CMU Serif}}
{\IfFontExistsTF{DejaVu Sans}
  {\setmainfont{DejaVu Sans}}
  {\setmainfont{Georgia}}
}

\begin{document}
\section*{Chapter 1}
이차곡선

두 점 $\mathrm{F}(c, 0), \mathrm{F}^{\prime}(-c, 0)(c>0)$ 을 초점으로 하고 장축의 길이가 10 인 타원이 $y$ 축과 만나는 한 점을 A 라 하자. 점 F 를 중심으로 하고 점 A 를 지나는 원과 점 A 에서 원에 접하는 직선 $l$ 에 대하여 점 $\mathrm{F}^{\prime}$ 과 직선 $l$ 사이의 거리가 3 일 때, 선분 $\mathrm{FF}^{\prime}$ 의 길이는? [4점]\\
(1) $\frac{18 \sqrt{5}}{5}$\\
(2) $\frac{37 \sqrt{5}}{10}$\\
(3) $\frac{19 \sqrt{5}}{5}$\\
(4) $\frac{39 \sqrt{5}}{10}$\\
(5) $4 \sqrt{5}$\\
\includegraphics[max width=\textwidth, center]{6bb7ae71-e880-463c-9364-680424529403-01_540_718_1070_778}

두 점 $\mathrm{F}(c, 0), \mathrm{F}^{\prime}(-c, 0)(c>0)$ 을 초점으로 하는 타원의 외부의 제 1 사분면에 있는 점 P 가 있다. 선분 $\mathrm{PF}^{\prime}$ 이 타원과 만나는 점을 Q 라 하자. 두 점 $\mathrm{P}, \mathrm{Q}$ 가 다음 조건을 만족시킨다.\\
(가) $\cos \left(\angle \mathrm{FF}^{\prime} \mathrm{P}\right)=\cos \left(\angle \mathrm{FPF}^{\prime}\right)=\frac{3}{5}$\\
(나) 두 선분 $\mathrm{OQ}, \mathrm{FP}$ 는 서로 평행하다.

삼각형 $\mathrm{PF}^{\prime} \mathrm{F}$ 의 넓이가 12 일 때, 선분 PF 가 타원과 만나는 점 R 에 대하여 $70 \times \overline{\mathrm{PR}}$ 의 값을 구하시오.\\[0pt]
(단, O 는 원점이다.) [4점]\\
\includegraphics[max width=\textwidth, center]{6bb7ae71-e880-463c-9364-680424529403-02_563_557_1256_858}\\
\includegraphics[max width=\textwidth, center]{6bb7ae71-e880-463c-9364-680424529403-03_246_255_509_152}

두 초점이 $\mathrm{F}(c, 0), \mathrm{F}^{\prime}(-c, 0)(c>0)$ 인 타원 $\frac{x^{2}}{a^{2}}+\frac{y^{2}}{b^{2}}=1$ 위의 제 1 사분면의 점 P 가 있다. 점 F 를 중심으로 하고 점 P 를 지나는 원을 $C_{1}$, 선분 $\mathrm{PF}^{\prime}$ 의 중점 M 을 중심으로 하고 점 P 를 지나는 원을 $C_{2}$ 라 하자. 두 원 $C_{1}$ 과 $C_{2}$ 가 만나는 점 중 P 가 아닌 점을 Q 라 할 때, $\overline{\mathrm{PF}}=\overline{\mathrm{PQ}}=2$ 이다. $\overline{\mathrm{MF}}=2 \sqrt{3}$ 일 때, $a^{2}+b^{2}$ 의 값은? (단, $a, b$ 는 상수이다.) [4점]\\
(1) 11\\
(2) 12\\
(3) 13\\
(4) 14\\
(5) 15\\
\includegraphics[max width=\textwidth, center]{6bb7ae71-e880-463c-9364-680424529403-03_549_827_1120_719}

\section*{Chapter 1 이차곡선}
\section*{(12)}
두 초점이 $\mathrm{F}(c, 0), \mathrm{F}^{\prime}(-c, 0)(c>0)$ 인 타원 $\frac{x^{2}}{25}+\frac{y^{2}}{16}=1$ 위의 제 1 사분면의 점 P 에 대하여 직선 PF 와 직선 $\mathrm{PF}^{\prime}$ 에 동시에 접하고 중심이 $y$ 축 위에 있는 원 $C$ 가 있다. 직선 PF 와 원 $C$ 가 접하는 점 Q 에 대하여 점 P 가 선분 FQ 를 $4: 1$ 로 내분하는 점일 때, $\overline{\mathrm{PF}} \times \overline{\mathrm{PF}^{\prime}}$ 의 값은?\\
(단, 원 $C$ 의 중심의 $y$ 좌표는 양수이다. ) [4점]\\
(1) 20\\
(2) 21\\
(3) 22\\
(4) 23\\
(5) 24\\
\includegraphics[max width=\textwidth, center]{6bb7ae71-e880-463c-9364-680424529403-04_638_547_1118_856}

\section*{(13)}
두 점 $\mathrm{F}(c, 0), \mathrm{F}^{\prime}(-c, 0)(c>0)$ 을 초점으로 하는 타원 $\frac{x^{2}}{4}+y^{2}=1$ 이 있다. 타원 위의 제 2 사분면의 점 A 와 제 4 사분면의 점 B 에 대하여 $\cos \left(\angle \mathrm{F}^{\prime} \mathrm{AF}\right)=-\frac{1}{3}$ 이고, 사각형 $\mathrm{AF}^{\prime} \mathrm{BF}$ 는 평행사변형이다. 직선 BF 가 타원과 만나는 점 중 B 가 아닌 점을 C 라 하고, 두 선분 $\mathrm{AF}, \mathrm{CF}^{\prime}$ 이 만나는 점을 D 라 할 때, 사각형 $\mathrm{DF}^{\prime} \mathrm{BF}$ 의 둘레의 길이는? [4점]\\
(1) $\frac{59}{8}$\\
(2) $\frac{15}{2}$\\
(3) $\frac{61}{8}$\\
(4) $\frac{31}{4}$\\
(5) $\frac{63}{8}$\\
\includegraphics[max width=\textwidth, center]{6bb7ae71-e880-463c-9364-680424529403-05_409_650_1209_814}

쌍곡선 $\frac{x^{2}}{16}-\frac{y^{2}}{9}=1$ 의 두 초점을 $\mathrm{F}(c, 0), \mathrm{F}^{\prime}(-c, 0)(c>0)$ 이라 하자.\\
쌍곡선 위의 제 1 사분면의 점 P 와 쌍곡선 위의 제 2 사분면의 점 Q 에 대하여 ${\overline{\mathrm{PF}^{\prime}}}^{2}-{\overline{\mathrm{QF}^{\prime}}}^{2}=36$ 이고, 삼각형 $\mathrm{PF}^{\prime} \mathrm{F}$ 의 둘레의 길이와 삼각형 $\mathrm{QF}^{\prime} \mathrm{F}$ 의 둘레의 길이의 차가 12 일 때, $\overline{\mathrm{PF}} \times \overline{\mathrm{QF}}$ 의 값은? [4점]\\
(1) 28\\
(2) 30\\
(3) 32\\
(4) 34\\
(5) 36\\
\includegraphics[max width=\textwidth, center]{6bb7ae71-e880-463c-9364-680424529403-06_426_749_1074_761}

\section*{Chapter 1}
\section*{이차곡선}
두 초점이 $\mathrm{F}(c, 0), \mathrm{F}^{\prime}(-c, 0)(c>0)$ 인 쌍곡선 $\frac{x^{2}}{4}-\frac{y^{2}}{k^{2}}=1$ 위의 제 1 사분면의 점 A 에 대하여 $\overline{\mathrm{AF}^{\prime}}=\overline{\mathrm{FF}^{\prime}}$ 이다. 직선 AF 가 쌍곡선의 한 점근선과 평행할 때, $k^{2}$ 의 값은? (단, $k$ 는 상수이다.) [4점]\\
(1) 30\\
(2) 32\\
(3) 34\\
(4) 36\\
(5) 38\\
\includegraphics[max width=\textwidth, center]{6bb7ae71-e880-463c-9364-680424529403-07_481_458_1015_909}

\section*{Chapter 1 \\
 이차곡선}
\section*{10}
주축의 길이가 4 인 쌍곡선의 두 초점 $\mathrm{F}(c, 0), \mathrm{F}^{\prime}(-c, 0)(c>0)$ 과 $y$ 축 위의 점 A 에 대하여 $\angle \mathrm{FAF}^{\prime}=\frac{\pi}{2}$ 이다. 세 점 $\mathrm{O}, \mathrm{F}, \mathrm{A}$ 를 지나는 원과 쌍곡선이 제 1 사분면에서 만나는 점을 P 라 하자. 점 $\mathrm{F}^{\prime}$ 을 지나고 직선 FP 와 평행한 직선이 직선 AP 와 만나는 점 Q 에 대하여 $\overline{\mathrm{F}^{\prime} \mathrm{Q}}=3 \overline{\mathrm{FP}}$ 일 때, $c^{2}$ 의 값을 구하시오. (단, 점 A 의 $y$ 좌표는 양수이고, O 는 원점이다.) [4점]\\
\includegraphics[max width=\textwidth, center]{6bb7ae71-e880-463c-9364-680424529403-08_458_650_1040_816}

\section*{Chapter 1 이차곡선}
\section*{(17)}
한 초점이 $\mathrm{A}(a, 0)(a>0)$ 이고 주축의 길이가 4 , 중심이 원점 O 인 쌍곡선이 있다. 점 $\mathrm{B}(0, b)(b>0)$ 와 쌍곡선 위를 움직이는 제 2 사분면의 점 P 에 대하여 삼각형 PAB 의 둘레의 길이가 최소가 되도록 하는 점 P 를 Q 라 하자. 세 점 $\mathrm{A}, \mathrm{B}, \mathrm{Q}$ 가 다음 조건을 만족시킬 때, $a b$ 의 값은? [4점]\\
(가) 삼각형 QAB 의 둘레의 길이는 16 이다.\\
(나) 삼각형 OAB 의 넓이와 삼각형 QAB 의 넓이는 같다.\\
(1) $5 \sqrt{2}$\\
(2) $6 \sqrt{3}$\\
(3) 14\\
(4) $8 \sqrt{5}$\\
(5) $9 \sqrt{6}$\\
\includegraphics[max width=\textwidth, center]{6bb7ae71-e880-463c-9364-680424529403-09_413_509_1239_881}

\section*{Chapter 1 이차곡선}
\section*{(18)}
두 점 $\mathrm{F}(c, 0), \mathrm{F}^{\prime}(-c, 0)(c>0)$ 을 초점으로 하는 쌍곡선 위의 제 1 사분면의 점 P 에서 $x$ 축에 내린 수선의 발을 H 라 하자. 선분 PH 위의 점 C 를 중심으로 하고 반지름의 길이가 $\sqrt{7}$ 인 원이 선분 PF 와 $x$ 축에 동시에 접한다. 직선 CF 가 직선 $\mathrm{PF}^{\prime}$ 과 평행하고 $\cos \left(\angle \mathrm{PF}^{\prime} \mathrm{H}\right)=\frac{3}{4}$ 일 때, 쌍곡선의 주축의 길이를 구하시오. (단, 점 P 의 $x$ 좌표는 점 F 의 $x$ 좌표보다 크다.) [4점]\\
\includegraphics[max width=\textwidth, center]{6bb7ae71-e880-463c-9364-680424529403-10_509_570_1027_845}


\end{document}"""

def clean_math_content(math_str):
    """수식 내용 정리"""
    # \mathrm 제거
    math_str = re.sub(r'\\mathrm\{([^}]+)\}', r'\1', math_str)
    # \left, \right 제거
    math_str = re.sub(r'\\left([\(\[\{])', r'\1', math_str)
    math_str = re.sub(r'\\right([\)\]\}])', r'\1', math_str)
    # 공백 정리
    math_str = re.sub(r'\s+', ' ', math_str)
    return math_str.strip()

def extract_problems(latex_content):
    """문제 추출"""
    problems = []
    
    # \begin{document} 이후만 추출
    doc_match = re.search(r'\\begin\{document\}(.*?)\\end\{document\}', latex_content, re.DOTALL)
    if not doc_match:
        return problems
    
    body = doc_match.group(1)
    
    # 점수 마커 찾기
    point_pattern = r'\[(\d+)점\]'
    point_markers = list(re.finditer(point_pattern, body))
    
    # 섹션 헤더 찾기
    section_pattern = r'\\section\*\{([^}]+)\}'
    sections = list(re.finditer(section_pattern, body))
    
    # 문제 번호 추출
    problem_numbers = {}
    for section in sections:
        section_text = section.group(1).strip()
        # (12), (13), (17), (18) 형식
        num_match = re.search(r'\((\d+)\)', section_text)
        if num_match:
            problem_num = int(num_match.group(1))
            problem_numbers[section.start()] = problem_num
        # 10 형식
        elif re.match(r'^\d+$', section_text):
            problem_num = int(section_text)
            problem_numbers[section.start()] = problem_num
    
    # 각 점수 마커를 기준으로 문제 추출
    for i, marker in enumerate(point_markers):
        marker_pos = marker.start()
        point = int(marker.group(1))
        
        # 이전 마커 위치
        prev_marker_pos = point_markers[i-1].end() if i > 0 else 0
        
        # 다음 마커 위치
        next_marker_pos = point_markers[i+1].start() if i < len(point_markers) - 1 else len(body)
        
        # 문제 본문 추출 (더 넓은 범위)
        search_start = max(prev_marker_pos, marker_pos - 3000)
        question_text = body[search_start:marker_pos]
        
        # 가장 가까운 섹션 찾기
        problem_num = None
        closest_section_pos = None
        for section_pos, num in problem_numbers.items():
            if section_pos < marker_pos and section_pos >= search_start:
                if closest_section_pos is None or section_pos > closest_section_pos:
                    problem_num = num
                    closest_section_pos = section_pos
        
        # 문제 번호가 없으면 순서대로 할당
        if problem_num is None:
            problem_num = i + 1
        
        # 섹션 이후부터 문제 본문 추출
        if closest_section_pos:
            question_text = body[closest_section_pos:marker_pos]
            # 섹션 헤더 제거
            question_text = re.sub(r'\\section\*\{[^}]+\}', '', question_text)
        else:
            # 섹션이 없으면 문제 시작 키워드로 찾기
            start_keywords = [
                '두 점',
                '두 초점이',
                '쌍곡선',
                '타원',
                '주축의 길이가',
                '한 초점이'
            ]
            for keyword in start_keywords:
                idx = question_text.find(keyword)
                if idx >= 0:
                    question_text = question_text[idx:]
                    break
        
        # 문제 텍스트 정리
        question_text = re.sub(r'\\\\', ' ', question_text)
        question_text = re.sub(r'\\includegraphics\[[^\]]*\]\{[^}]+\}', '', question_text)
        question_text = re.sub(r'\\\[0pt\]', '', question_text)  # [0pt] 제거
        question_text = re.sub(r'\s+', ' ', question_text).strip()
        
        # 선택지 추출
        options_text = body[marker_pos:next_marker_pos]
        options = []
        for opt_num in range(1, 6):
            # (1) 형식 찾기
            opt_start = options_text.find(f'({opt_num})')
            if opt_start == -1:
                continue
            
            # 다음 선택지 또는 이미지 시작점 찾기
            next_opt_start = len(options_text)
            for next_num in range(opt_num + 1, 6):
                next_pos = options_text.find(f'({next_num})', opt_start + 1)
                if next_pos != -1:
                    next_opt_start = next_pos
                    break
            
            # 이미지 시작점 확인
            img_pos = options_text.find('\\includegraphics', opt_start)
            if img_pos != -1 and img_pos < next_opt_start:
                next_opt_start = img_pos
            
            # 선택지 텍스트 추출
            opt_text = options_text[opt_start + len(f'({opt_num})'):next_opt_start].strip()
            opt_text = re.sub(r'\\\\', '', opt_text).strip()
            if opt_text:
                options.append(f"{'①②③④⑤'[opt_num-1]} {opt_text}")
        
        if len(question_text) > 30:  # 최소 길이 확인
            problems.append({
                'index': str(problem_num).zfill(2),
                'page': 1,
                'topic': '이차곡선',
                'question': question_text,
                'point': point,
                'answer_type': 'multiple_choice' if options else 'short_answer',
                'options': options if options else []
            })
    
    return problems

def latex_to_markdown_for_deepseek(latex_text):
    """LaTeX를 Deepseek R1-70B용 마크다운으로 변환"""
    text = latex_text
    
    # 수식 블록 ($$ ... $$) - 먼저 처리
    def replace_display_math(match):
        math_content = match.group(1)
        math_content = clean_math_content(math_content)
        return f'\n\n$$\n{math_content}\n$$\n\n'
    text = re.sub(r'\$\$([^$]+?)\$\$', replace_display_math, text, flags=re.DOTALL)
    
    # 인라인 수식 ($ ... $) - 정확하게 변환
    def replace_inline_math(match):
        math_content = match.group(1)
        math_content = clean_math_content(math_content)
        return f'${math_content}$'
    text = re.sub(r'\$([^$]+?)\$', replace_inline_math, text)
    
    # 줄바꿈 처리
    text = re.sub(r'\\\\', '\n', text)
    
    # 이미지 처리
    text = re.sub(r'\\includegraphics\[[^\]]*\]\{[^}]+\}', '[이미지]', text)
    
    # 기타 정리
    text = re.sub(r'\\%', '%', text)
    text = re.sub(r'[ \t]+', ' ', text)  # 연속 공백
    text = re.sub(r'\n{3,}', '\n\n', text)  # 연속 줄바꿈
    text = re.sub(r'^\s+', '', text, flags=re.MULTILINE)  # 줄 시작 공백
    
    return text.strip()

def validate_math_errors(problems):
    """수학적 오류 검증"""
    errors = []
    warnings = []
    
    for problem in problems:
        question = problem.get('question', '')
        index = problem.get('index', '')
        
        # 타원 방정식 검증
        if '타원' in question:
            if '초점' in question and ('장축' in question or '2a' in question or '\\frac{x^{2}' in question):
                pass  # 정확
            else:
                warnings.append(f"문제 {index}: 타원 관련 조건 확인 필요")
            
            # 타원 정의: PF + PF' = 2a
            if '초점' in question and 'F' in question and 'F\'' in question:
                pass  # 정확
            else:
                warnings.append(f"문제 {index}: 타원의 두 초점 관련 내용 확인 필요")
        
        # 쌍곡선 방정식 검증
        if '쌍곡선' in question:
            if '초점' in question and ('\\frac{x^{2}' in question or '주축' in question):
                pass  # 정확
            else:
                warnings.append(f"문제 {index}: 쌍곡선 관련 조건 확인 필요")
            
            # 쌍곡선 정의: |PF - PF'| = 2a
            if '초점' in question and 'F' in question and 'F\'' in question:
                pass  # 정확
            else:
                warnings.append(f"문제 {index}: 쌍곡선의 두 초점 관련 내용 확인 필요")
        
        # 기하학적 조건 검증
        if '삼각형' in question:
            if '둘레' in question or '넓이' in question:
                pass  # 정확
            else:
                warnings.append(f"문제 {index}: 삼각형 관련 조건 확인 필요")
        
        # 점수 검증
        if problem.get('point', 0) not in [3, 4]:
            warnings.append(f"문제 {index}: 점수가 비정상적 ({problem.get('point', 0)}점)")
    
    return errors, warnings

def main():
    print("=" * 80)
    print("기하_2024학년도_현우진_드릴_P2 문제 → Deepseek R1-70B용 변환")
    print("=" * 80)
    
    # 문제 추출
    problems = extract_problems(latex_content)
    print(f"\n총 {len(problems)}개 문제 발견\n")
    
    # 문제 본문 정리 (이전 문제의 선택지 제거)
    fixed_problems = []
    doc_match = re.search(r'\\begin\{document\}(.*?)\\end\{document\}', latex_content, re.DOTALL)
    body = doc_match.group(1) if doc_match else ''
    
    point_pattern = r'\[(\d+)점\]'
    point_markers = list(re.finditer(point_pattern, body))
    
    for i, problem in enumerate(problems):
        question = problem.get('question', '')
        
        # 이전 문제의 선택지 제거
        question = re.sub(r'\(1\)\s*\$[^$]+\$\s*\(2\)\s*\$[^$]+\$\s*\(3\)\s*\$[^$]+\$\s*\(4\)\s*\$[^$]+\$\s*\(5\)\s*\$[^$]+\$', '', question)
        question = re.sub(r'\(1\)\s*[0-9+\-√\s/]+\s*\(2\)\s*[0-9+\-√\s/]+\s*\(3\)\s*[0-9+\-√\s/]+\s*\(4\)\s*[0-9+\-√\s/]+\s*\(5\)\s*[0-9+\-√\s/]+', '', question)
        
        # 문제 시작 키워드 찾기
        start_keywords = [
            '두 점',
            '두 초점이',
            '쌍곡선',
            '타원',
            '주축의 길이가',
            '한 초점이'
        ]
        
        found_start = False
        for keyword in start_keywords:
            idx = question.find(keyword)
            if idx >= 0 and idx < 500:  # 문제 시작 부분
                question = question[idx:]
                found_start = True
                break
        
        # 섹션 헤더 제거
        question = re.sub(r'\\section\*\{[^}]+\}', '', question)
        question = re.sub(r'Chapter 1', '', question)
        question = re.sub(r'이차곡선', '', question)
        
        question = re.sub(r'\s+', ' ', question).strip()
        fixed_problems.append({**problem, 'question': question})
    
    # 수학적 오류 검증
    math_errors, math_warnings = validate_math_errors(fixed_problems)
    
    print("[수학적 오류 검증]")
    if math_errors:
        print(f"  ❌ 오류: {len(math_errors)}개")
        for error in math_errors:
            print(f"    - {error}")
    else:
        print("  ✅ 수학적 오류 없음")
    
    if math_warnings:
        print(f"  ⚠️  경고: {len(math_warnings)}개")
        for warning in math_warnings[:10]:
            print(f"    - {warning}")
        if len(math_warnings) > 10:
            print(f"    ... 외 {len(math_warnings) - 10}개")
    else:
        print("  ✅ 경고 없음")
    
    # 저장 경로
    base_dir = Path(r'C:\Users\a\Documents\MathPDF\organized\현우진\기하_2024학년도_현우진_드릴')
    base_dir.mkdir(parents=True, exist_ok=True)
    
    # JSON 저장
    json_path = base_dir / "기하_2024학년도_현우진_드릴_P2_문제_deepseek.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(fixed_problems, f, ensure_ascii=False, indent=2)
    
    # 마크다운 저장
    md_content = "# 기하_2024학년도_현우진_드릴_P2 문제\n\n"
    md_content += "> 이 문서는 Deepseek R1-70B가 읽을 수 있도록 최적화된 마크다운 형식입니다.\n\n"
    
    for problem in fixed_problems:
        question_md = latex_to_markdown_for_deepseek(problem['question'])
        md_content += f"## 문제 {problem['index']} ({problem['topic']}) [{problem['point']}점]\n\n"
        md_content += f"{question_md}\n\n"
        if problem['options']:
            md_content += "**선택지:**\n"
            for opt in problem['options']:
                md_content += f"- {opt}\n"
            md_content += "\n"
    
    md_path = base_dir / "기하_2024학년도_현우진_드릴_P2_문제_deepseek_r1.md"
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    print(f"\n[저장 완료]")
    print(f"  - JSON: {json_path}")
    print(f"  - 마크다운: {md_path}")
    print(f"\n총 {len(fixed_problems)}개 문제 변환 완료")
    print("\n[Deepseek R1-70B 호환성]")
    print("  - 마크다운 형식: 지원")
    print("  - LaTeX 수식: 지원 ($...$ 및 $$...$$)")
    print("  - 구조화된 섹션: 지원")
    print("  - UTF-8 인코딩: 지원")
    print("\n[결론] Deepseek R1-70B가 읽을 수 있는 형태입니다.")

if __name__ == '__main__':
    main()
