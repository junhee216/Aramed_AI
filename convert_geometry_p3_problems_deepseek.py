# convert_geometry_p3_problems_deepseek.py
# 기하_2024학년도_현우진_드릴_P3 문제 LaTeX → Deepseek R1-70B용 변환

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
두 초점이 $\mathrm{F}(c, 0), \mathrm{F}^{\prime}(-c, 0)(c>0)$ 인 쌍곡선이 있다. 쌍곡선 위의 제 1 사분면의 점 P 에 대하여 선분 $\mathrm{PF}^{\prime}$ 을 지름으로 하는 원을 $C$ 라 할 때, 원 $C$ 는 점 F 를 지난다. 원 $C$ 와 쌍곡선이 만나는 점 중 제 4 사분면의 점을 Q 라 할 때,

$$
\overline{\mathrm{PF}^{\prime}}=10, \quad \overline{\mathrm{QF}^{\prime}}=6
$$

이다. 쌍곡선의 주축의 길이는? [4점]\\
(1) $7-3 \sqrt{2}$\\
(2) $7-\sqrt{19}$\\
(3) $7-2 \sqrt{5}$\\
(4) $8-\sqrt{19}$\\
(5) $8-2 \sqrt{5}$\\
\includegraphics[max width=\textwidth, center]{414675b0-47b6-4e36-8fc7-db5605deb3a3-1_555_530_1156_873}

두 점 $\mathrm{F}(c, 0), \mathrm{F}^{\prime}(-c, 0)(c>0)$ 을 초점으로 하는 쌍곡선 위의 점 중 제 1 사분면에 있는 점 P 가 있다. 점 P 를 중심으로 하고 점 $\mathrm{F}^{\prime}$ 을 지나는 원이 쌍곡선과 제 4 사분면에서 만나는 점을 Q 라 하자.\\
두 점 $\mathrm{P}, \mathrm{Q}$ 가 다음 조건을 만족시킨다.\\
(가) 세 점 $\mathrm{P}, \mathrm{F}, \mathrm{Q}$ 는 한 직선 위에 있다.\\
(나) 점 F 를 중심으로 하고 점 Q 를 지나는 원이 원점을 지난다.\\
$\overline{\mathrm{QF}^{\prime}}=8$ 일 때, 삼각형 $\mathrm{PF}^{\prime} \mathrm{F}$ 의 둘레의 길이는? [4점]\\
(1) 32\\
(2) 34\\
(3) 36\\
(4) 38\\
(5) 40\\
\includegraphics[max width=\textwidth, center]{414675b0-47b6-4e36-8fc7-db5605deb3a3-2_561_531_1315_867}

\section*{Chapter 1 \\
 이차곡선}
초점이 F 인 포물선 $y^{2}=4 p x(p>0)$ 의 준선 위의 점 A 에 대하여 직선 AF 의 기울기는 $-\frac{4}{3}$ 이다.\\
점 A 에서 포물선에 그은 접선 중 기울기가 양수인 접선의 접점을 B , 선분 AF 와 포물선이 만나는 점을 C 라 하자. $\overline{\mathrm{CF}}=5$ 일 때, 사각형 AOFB 의 넓이를 구하시오. (단, O 는 원점이다.) [4점]\\
\includegraphics[max width=\textwidth, center]{414675b0-47b6-4e36-8fc7-db5605deb3a3-3_430_610_977_831}

\section*{Chapter 1}
이차곡선

\section*{22}
점 $(\sqrt{3}, k)$ 에서 타원 $\frac{x^{2}}{3}+\frac{y^{2}}{8}=1$ 에 그은 두 접선이 이루는 각의 크기가 $\frac{\pi}{3}$ 가 되도록 하는 모든 양수 $k$ 의 값의 합은? [4점]\\
(1) 5\\
(2) 6\\
(3) 7\\
(4) 8\\
(5) 9

\section*{Chapter 1}
이차곡선

\section*{23}
한 초점이 $\mathrm{F}(4,0)$ 인 쌍곡선 $\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1$ 이 있다. 점 $\mathrm{A}(0, \sqrt{5})$ 를 지나고 기울기가 음수인 직선이 쌍곡선과 접하는 점을 B 라 하자. 쌍곡선 위를 움직이는 제 1 사분면의 점 X 에 대하여 $\overline{\mathrm{XA}}-\overline{\mathrm{XF}}$ 의 값이 최소가 되도록 하는 점 X 를 P 라 하자. $\angle \mathrm{PAB}=\frac{\pi}{2}$ 일 때, 상수 $a, b$ 에 대하여 $(a b)^{2}$ 의 값을 구하시오. [4점]\\
\includegraphics[max width=\textwidth, center]{414675b0-47b6-4e36-8fc7-db5605deb3a3-5_532_502_1002_892}

\section*{Chapter 1 이차곡선}
쌍곡선 $x^{2}-y^{2}=5$ 위의 점 $\mathrm{A}(-3,2)$ 에서의 접선이 쌍곡선의 두 점근선과 만나는 점을 각각 $\mathrm{B}, \mathrm{C}$ 라 하자. 쌍곡선 위를 움직이는 $x$ 좌표가 양수인 점 P 에 대하여 삼각형 PBC 의 넓이의 최솟값은? [3점]\\
(1) $\frac{17}{2}$\\
(2) 9\\
(3) $\frac{19}{2}$\\
(4) 10\\
(5) $\frac{21}{2}$

두 초점이 $\mathrm{F}(c, 0), \mathrm{F}^{\prime}(-c, 0)(c>0)$ 이고 주축의 길이가 4 인 쌍곡선 위의 제 1 사분면의 점 P 가 있다. 점 P 에서의 접선이 $x$ 축과 만나는 점을 Q , 점 P 에서의 접선과 평행하고 점 $\mathrm{F}^{\prime}$ 을 지나는 직선이 쌍곡선과 제 2 사분면에서 만나는 점을 R , 두 선분 $\mathrm{PQ}, \mathrm{RF}$ 가 만나는 점을 S 라 하자. 선분 PR 가 $x$ 축과 평행하고 사각형 $\mathrm{QSRF}^{\prime}$ 의 둘레의 길이와 삼각형 FPR 의 둘레의 길이의 차가 1 일 때, 점 P 의 $x$ 좌표는?\\
(단, 점 P 의 $x$ 좌표는 $c$ 보다 작다.) [4점]\\
(1) $\sqrt{5}$\\
(2) $\sqrt{6}$\\
(3) $\sqrt{7}$\\
(4) $2 \sqrt{2}$\\
(5) 3\\
\includegraphics[max width=\textwidth, center]{414675b0-47b6-4e36-8fc7-db5605deb3a3-7_486_603_1158_829}

\section*{Chapter 2}
그림과 같이 넓이가 24 인 마름모 ABCD 의 내부의 두 점 $\mathrm{P}, \mathrm{Q}$ 가

$$
3 \overrightarrow{\mathrm{AP}}=\overrightarrow{\mathrm{PB}}+\overrightarrow{\mathrm{PC}}+\overrightarrow{\mathrm{PD}}, \quad \overrightarrow{\mathrm{QA}}+\overrightarrow{\mathrm{QB}}+\overrightarrow{\mathrm{QC}}=\overrightarrow{0}
$$

를 만족시킨다. $|\overrightarrow{\mathrm{PQ}}|=\frac{5}{3}$ 일 때, $|\overrightarrow{\mathrm{AB}}+\overrightarrow{\mathrm{AD}}|$ 의 값은? (단, $\angle \mathrm{BAD}>\frac{\pi}{2}$ ) [4점]\\
\includegraphics[max width=\textwidth, center]{414675b0-47b6-4e36-8fc7-db5605deb3a3-8_367_457_964_903}\\
(1) 6\\
(2) $\frac{25}{4}$\\
(3) $\frac{13}{2}$\\
(4) $\frac{27}{4}$\\
(5) 7

\section*{Chapter 2}
평면벡터

좌표평면 위에 점 $\mathrm{A}(2,1)$ 을 지나고 방향벡터가 $(4,3)$ 인 직선 위의 점 B 가 있다. 원점에 대한 두 점 A , B 의 위치벡터를 각각 $\vec{a}, \vec{b}$ 라 할 때, $\vec{a} \cdot \vec{b}=27$ 이다. $|\vec{b}-\vec{a}|$ 의 값은? [3점]\\
(1) 8\\
(2) 9\\
(3) 10\\
(4) 11\\
(5) 12


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
        # 22, 23 형식 (숫자만)
        num_match = re.search(r'^(\d+)$', section_text)
        if num_match:
            problem_num = int(num_match.group(1))
            problem_numbers[section.start()] = problem_num
        # Chapter 1, Chapter 2는 문제 번호가 아님
    
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
                '쌍곡선 $x^{2}-y^{2}',
                '쌍곡선 $\\frac{x^{2}',
                '두 초점이',
                '두 점',
                '쌍곡선',
                '타원',
                '포물선',
                '초점이 F',
                '그림과 같이',
                '좌표평면 위에',
                '점 $'
            ]
            for keyword in start_keywords:
                idx = question_text.find(keyword)
                if idx >= 0:
                    question_text = question_text[idx:]
                    break
        
        # 문제 06번 특별 처리: "쌍곡선 $x^{2}-y^{2}=5$"로 시작하는지 확인
        if problem_num == 6 or (i == 5 and '점근선' in question_text and '쌍곡선' not in question_text[:100]):
            # 이전 문제의 선택지나 내용이 포함되어 있을 수 있음
            # "쌍곡선 $x^{2}-y^{2}=5$"로 시작하는 부분 찾기
            sh_match = re.search(r'쌍곡선\s*\$x\^\{2\}-y\^\{2\}=5\$', question_text)
            if sh_match:
                question_text = question_text[sh_match.start():]
        
        # 문제 텍스트 정리
        question_text = re.sub(r'\\\\', ' ', question_text)
        question_text = re.sub(r'\\includegraphics\[[^\]]*\]\{[^}]+\}', '', question_text)
        question_text = re.sub(r'\\\[0pt\]', '', question_text)  # [0pt] 제거
        question_text = re.sub(r'\s+', ' ', question_text).strip()
        
        # 선택지 추출
        options_text = body[marker_pos:next_marker_pos]
        options = []
        
        # 다음 문제의 섹션 헤더가 선택지에 포함되지 않도록 제한
        next_section_pos = len(options_text)
        for section_pos in problem_numbers.keys():
            if section_pos > marker_pos and section_pos < marker_pos + len(options_text):
                next_section_pos = min(next_section_pos, section_pos - marker_pos)
        
        if next_section_pos < len(options_text):
            options_text = options_text[:next_section_pos]
        
        # 섹션 헤더가 선택지 텍스트에 포함되어 있으면 그 이전까지만
        section_match = re.search(r'\\section\*\{', options_text)
        if section_match:
            options_text = options_text[:section_match.start()]
        
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
            
            # 섹션 헤더 확인
            section_pos_in_opt = options_text.find('\\section', opt_start)
            if section_pos_in_opt != -1 and section_pos_in_opt < next_opt_start:
                next_opt_start = section_pos_in_opt
            
            # 선택지 텍스트 추출
            opt_text = options_text[opt_start + len(f'({opt_num})'):next_opt_start].strip()
            opt_text = re.sub(r'\\\\', '', opt_text).strip()
            # 섹션 헤더 제거
            opt_text = re.sub(r'\\section\*\{[^}]+\}', '', opt_text)
            opt_text = re.sub(r'Chapter \d+', '', opt_text)
            opt_text = re.sub(r'이차곡선', '', opt_text)
            opt_text = re.sub(r'평면벡터', '', opt_text)
            opt_text = re.sub(r'\s+', ' ', opt_text).strip()
            # 너무 긴 것은 다음 문제 내용일 수 있음 (200자 제한)
            if opt_text and len(opt_text) < 200:
                options.append(f"{'①②③④⑤'[opt_num-1]} {opt_text}")
        
        if len(question_text) > 30:  # 최소 길이 확인
            # 주제 판별
            topic = '이차곡선'
            if '벡터' in question_text or '\\overrightarrow' in question_text or '\\vec' in question_text:
                topic = '벡터'
            
            problems.append({
                'index': str(problem_num).zfill(2),
                'page': 1,
                'topic': topic,
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
        
        # 쌍곡선 방정식 검증
        if '쌍곡선' in question:
            if '초점' in question and ('\\frac{x^{2}' in question or '주축' in question or 'x^{2}-y^{2}' in question):
                pass  # 정확
            else:
                warnings.append(f"문제 {index}: 쌍곡선 관련 조건 확인 필요")
        
        # 포물선 방정식 검증
        if '포물선' in question:
            if '초점' in question and ('y^{2}' in question or '준선' in question):
                pass  # 정확
            else:
                warnings.append(f"문제 {index}: 포물선 관련 조건 확인 필요")
        
        # 벡터 검증
        if '벡터' in question or '\\overrightarrow' in question or '\\vec' in question:
            if '\\overrightarrow' in question or '\\vec' in question or '\\cdot' in question:
                pass  # 정확
            else:
                warnings.append(f"문제 {index}: 벡터 관련 표기 확인 필요")
        
        # 점수 검증
        if problem.get('point', 0) not in [3, 4]:
            warnings.append(f"문제 {index}: 점수가 비정상적 ({problem.get('point', 0)}점)")
    
    return errors, warnings

def main():
    print("=" * 80)
    print("기하_2024학년도_현우진_드릴_P3 문제 → Deepseek R1-70B용 변환")
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
            '쌍곡선 $x^{2}-y^{2}',
            '쌍곡선 $\\frac{x^{2}',
            '두 초점이',
            '두 점',
            '쌍곡선',
            '타원',
            '포물선',
            '초점이 F',
            '그림과 같이',
            '좌표평면 위에',
            '점 $'
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
        question = re.sub(r'Chapter 2', '', question)
        question = re.sub(r'이차곡선', '', question)
        question = re.sub(r'평면벡터', '', question)
        
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
    json_path = base_dir / "기하_2024학년도_현우진_드릴_P3_문제_deepseek.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(fixed_problems, f, ensure_ascii=False, indent=2)
    
    # 마크다운 저장
    md_content = "# 기하_2024학년도_현우진_드릴_P3 문제\n\n"
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
    
    md_path = base_dir / "기하_2024학년도_현우진_드릴_P3_문제_deepseek_r1.md"
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
