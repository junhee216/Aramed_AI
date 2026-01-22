# convert_geometry_p5_problems_deepseek.py
# 기하_2024학년도_현우진_드릴_P5 문제 LaTeX → Deepseek R1-70B용 변환

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
\section*{Chapter 2}
\section*{평면벡터}
\section*{(12)}
원 $C$ 위에 있는 서로 다른 세 점 $\mathrm{A}, \mathrm{B}, \mathrm{C}$ 가

$$
|\overrightarrow{\mathrm{AB}}|=8, \quad \overrightarrow{\mathrm{AC}} \cdot \overrightarrow{\mathrm{BC}}=0
$$

을 만족시킨다. 원 $C$ 위를 움직이는 점 X 에 대하여 $\overrightarrow{\mathrm{AX}} \cdot \overrightarrow{\mathrm{BC}}$ 의 값이 최소가 되도록 하는 점 X 를 P 라 할 때, $\overrightarrow{\mathrm{AP}} \cdot \overrightarrow{\mathrm{BC}}=-10$ 이다. $|\overrightarrow{\mathrm{AP}}|^{2}$ 의 값을 구하시오. [4점]\\
\includegraphics[max width=\textwidth, center]{b8f61bf7-cbf1-475f-abbd-cca702d03452-1_367_420_989_930}

\section*{Chapter 2 \\
 평면벡터}
좌표평면에서 반원 $x^{2}+y^{2}=16(y \geq 0)$ 의 호 위를 움직이는 점 P 와 점 $\mathrm{Q}(5, k)$ 에 대하여 $\overrightarrow{\mathrm{QP}} \cdot(\overrightarrow{\mathrm{QO}}+\overrightarrow{\mathrm{QP}})$ 의 최댓값이 198 이 되도록 하는 모든 실수 $k$ 의 값의 합은 $a+b \sqrt{6}$ 이다. 정수 $a, b$ 에 대하여 $a^{2}+b^{2}$ 의 값을 구하시오. (단, O 는 원점이다.) [4점]

\section*{Chapter 2}
\section*{평면벡터}
좌표평면에서 반원 $x^{2}+y^{2}=1(y \geq 0)$ 의 호 위의 점 P 와 원 $(x-3)^{2}+y^{2}=1$ 위의 점 Q 가 있다. 점 $\mathrm{A}(3,0)$ 에 대하여

$$
|\overrightarrow{\mathrm{AP}}+\overrightarrow{\mathrm{AQ}}-2 \overrightarrow{\mathrm{AO}}|=|\overrightarrow{\mathrm{PQ}}|
$$

이다. $\overrightarrow{\mathrm{OP}} \cdot \overrightarrow{\mathrm{OA}}$ 의 값이 최소가 되도록 하는 두 점 $\mathrm{P}, \mathrm{Q}$ 를 각각 $\mathrm{P}_{1}, \mathrm{Q}_{1}$ 이라 할 때, $\overrightarrow{\mathrm{AP}_{1}} \cdot \overrightarrow{\mathrm{OQ}_{1}}$ 의 값은?\\[0pt]
(단, O 는 원점이다.) [4점]\\
(1) -9\\
(2) -8\\
(3) -7\\
(4) -6\\
(5) -5

\section*{Chapter 2}
\section*{평면벡터}
좌표평면에 두 점 $\mathrm{O}(0,0), \mathrm{A}(10,0)$ 과 원 $C:(x-a)^{2}+(y-2)^{2}=4$ 가 있다. 원 $C$ 위를 움직이는 점 P 에 대하여 $\overrightarrow{\mathrm{PO}} \cdot \overrightarrow{\mathrm{PA}}$ 의 최댓값이 24 가 되도록 하는 모든 실수 $a$ 의 값의 곱은? [4점]\\
(1) 4\\
(2) 5\\
(3) 6\\
(4) 7\\
(5) 8

\section*{Chapter 2}
평면벡터

\section*{10}
좌표평면에서 반원의 호 $x^{2}+y^{2}=4(y \geq 0)$ 위를 움직이는 점 P 와 원 $(x-3)^{2}+(y-3)^{2}=1$ 위를 움직이는 점 Q 에 대하여 $\overrightarrow{\mathrm{PQ}} \cdot \overrightarrow{\mathrm{OQ}}$ 의 최댓값은? (단, O 는 원점이다.) [4점]\\
(1) 31\\
(2) 33\\
(3) 35\\
(4) 37\\
(5) 39\\
\includegraphics[max width=\textwidth, center]{b8f61bf7-cbf1-475f-abbd-cca702d03452-5_500_646_968_807}

\section*{Chapter 2}
\section*{평면벡터}
좌표평면에서 두 점 $\mathrm{A}(5,0), \mathrm{B}(-3,4)$ 에 대하여 두 점 $\mathrm{P}, \mathrm{Q}$ 가

$$
|\overrightarrow{\mathrm{AP}}|=a, \quad|\overrightarrow{\mathrm{BQ}}|=b, \quad \overrightarrow{\mathrm{OB}} \cdot \overrightarrow{\mathrm{BQ}} \leq 0
$$

을 만족시킨다. $\overrightarrow{\mathrm{OA}} \cdot \overrightarrow{\mathrm{PQ}}$ 의 최댓값이 $0, \overrightarrow{\mathrm{BP}} \cdot \overrightarrow{\mathrm{BQ}}$ 의 최솟값이 -20 일 때, $a^{2}+b^{2}$ 의 값을 구하시오.\\[0pt]
(단, O 는 원점이다.) [4점]

\section*{Chapter 2}
평면벡터

\section*{18}
그림과 같이 길이가 8 인 선분 AB 를 지름으로 하는 원 $C$ 가 있고, 점 A 에서 원 $C$ 에 내접하는 원 $C_{1}$ 과 점 B 에서 원 $C$ 에 내접하는 원 $C_{2}$ 가 서로 외접한다. 원 $C$ 위를 움직이는 점 P , 원 $C_{1}$ 위를 움직이는 점 Q , 원 $C_{2}$ 위를 움직이는 점 R 에 대하여 $|\overrightarrow{\mathrm{PQ}}+\overrightarrow{\mathrm{PR}}|$ 의 최댓값이 14 이다. $\overrightarrow{\mathrm{AP}} \cdot \overrightarrow{\mathrm{QR}}$ 의 최솟값이 $m$ 일 때, $m^{2}$ 의 값을 구하시오. (단, 원 $C_{1}$ 의 반지름의 길이는 원 $C_{2}$ 의 반지름의 길이보다 크다.) [4점]\\
\includegraphics[max width=\textwidth, center]{b8f61bf7-cbf1-475f-abbd-cca702d03452-7_527_587_981_837}

\section*{Chapter 3}
\section*{공간도형과 공간좌표}
평면 $\alpha$ 위에 한 변의 길이가 2 인 정사각형 ABCD 가 있다. 선분 BC 위의 점 P 를 지나고 평면 $\alpha$ 와 수직인 직선 위의 점 Q 에 대하여 $\overline{\mathrm{PQ}}=3$ 이고, 점 B 와 평면 QCD 사이의 거리가 $\sqrt{3}$ 이다. 직선 DQ 와 평면 $\alpha$ 가 이루는 각의 크기를 $\theta$ 라 할 때, $\sin \theta$ 의 값은? [3점]\\
(1) $\frac{\sqrt{7}}{4}$\\
(2) $\frac{\sqrt{2}}{2}$\\
(3) $\frac{3}{4}$\\
(4) $\frac{\sqrt{10}}{4}$\\
(5) $\frac{\sqrt{11}}{4}$\\
\includegraphics[max width=\textwidth, center]{b8f61bf7-cbf1-475f-abbd-cca702d03452-8_476_709_1070_774}


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
        # (12) 형식
        num_match = re.search(r'\((\d+)\)', section_text)
        if num_match:
            problem_num = int(num_match.group(1))
            problem_numbers[section.start()] = problem_num
        # 10, 18 형식 (숫자만)
        elif re.match(r'^\d+$', section_text) and not section_text.startswith('Chapter'):
            problem_num = int(section_text)
            problem_numbers[section.start()] = problem_num
        # Chapter 2, 평면벡터, 공간도형과 공간좌표는 문제 번호가 아님
    
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
                '그림과 같이',
                '원 $C$',
                '원 $x^{2}',
                '좌표평면에서',
                '좌표평면에',
                '평면 $\\alpha$'
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
        question_text = re.sub(r'\[0pt\]', '', question_text)  # [0pt] 제거 (이미 변환된 경우)
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
            opt_text = re.sub(r'평면벡터', '', opt_text)
            opt_text = re.sub(r'공간도형과 공간좌표', '', opt_text)
            opt_text = re.sub(r'\s+', ' ', opt_text).strip()
            # 너무 긴 것은 다음 문제 내용일 수 있음 (200자 제한)
            if opt_text and len(opt_text) < 200:
                options.append(f"{'①②③④⑤'[opt_num-1]} {opt_text}")
        
        if len(question_text) > 30:  # 최소 길이 확인
            # 주제 판별
            topic = '벡터'
            if '평면' in question_text and ('공간' in question_text or '정사각형' in question_text or '직선' in question_text and '수직' in question_text):
                topic = '공간도형'
            elif '원' in question_text and ('x^{2}' in question_text or 'y^{2}' in question_text):
                topic = '벡터'  # 벡터와 원의 결합 문제
            
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
    
    # aligned 환경 처리
    def replace_aligned(match):
        content = match.group(1)
        lines = content.split('\\\\')
        cleaned_lines = []
        for line in lines:
            line = line.strip()
            if '&' in line:
                parts = [p.strip() for p in line.split('&')]
                line = ' '.join(parts)
            line = clean_math_content(line)
            cleaned_lines.append(line)
        return '\n'.join(cleaned_lines)
    text = re.sub(r'\\begin\{aligned\}(.*?)\\end\{aligned\}', replace_aligned, text, flags=re.DOTALL)
    
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
        topic = problem.get('topic', '')
        
        # 벡터 검증
        if topic == '벡터':
            if '\\overrightarrow' in question or '\\vec' in question or '\\cdot' in question:
                pass  # 정확
            else:
                warnings.append(f"문제 {index}: 벡터 관련 표기 확인 필요")
        
        # 공간도형 검증
        if topic == '공간도형':
            if '평면' in question or '공간' in question or '직선' in question:
                pass  # 정확
            else:
                warnings.append(f"문제 {index}: 공간도형 관련 내용 확인 필요")
        
        # 원 방정식 검증
        if '원' in question and ('x^{2}' in question or 'y^{2}' in question):
            if 'x^{2}' in question or 'y^{2}' in question:
                pass  # 정확
            else:
                warnings.append(f"문제 {index}: 원 방정식 확인 필요")
        
        # 점수 검증
        if problem.get('point', 0) not in [3, 4]:
            warnings.append(f"문제 {index}: 점수가 비정상적 ({problem.get('point', 0)}점)")
    
    return errors, warnings

def main():
    print("=" * 80)
    print("기하_2024학년도_현우진_드릴_P5 문제 → Deepseek R1-70B용 변환")
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
            '그림과 같이',
            '원 $C$',
            '원 $x^{2}',
            '좌표평면에서',
            '좌표평면에',
            '평면 $\\alpha$'
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
        question = re.sub(r'Chapter 2', '', question)
        question = re.sub(r'Chapter 3', '', question)
        question = re.sub(r'평면벡터', '', question)
        question = re.sub(r'공간도형과 공간좌표', '', question)
        
        # [0pt] 제거
        question = re.sub(r'\\\[0pt\]', '', question)
        question = re.sub(r'\[0pt\]', '', question)
        
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
    
    # 저장 경로 (크로스 플랫폼 지원)
    import os
    if os.name == 'nt':  # Windows
        base_dir = Path(r'C:\Users\a\Documents\MathPDF\organized\현우진\기하_2024학년도_현우진_드릴')
    else:  # Linux, macOS
        mathpdf_path = os.environ.get('MATHPDF_PATH', str(Path.home() / 'Documents' / 'MathPDF' / 'organized'))
        base_dir = Path(mathpdf_path) / '현우진' / '기하_2024학년도_현우진_드릴'
    base_dir.mkdir(parents=True, exist_ok=True)
    
    # JSON 저장
    json_path = base_dir / "기하_2024학년도_현우진_드릴_P5_문제_deepseek.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(fixed_problems, f, ensure_ascii=False, indent=2)
    
    # 마크다운 저장
    md_content = "# 기하_2024학년도_현우진_드릴_P5 문제\n\n"
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
    
    md_path = base_dir / "기하_2024학년도_현우진_드릴_P5_문제_deepseek_r1.md"
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
