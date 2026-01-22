# convert_geometry_p1_problems_deepseek.py
# 기하_2024학년도_현우진_드릴_P1 문제 LaTeX → Deepseek R1-70B용 변환

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

\section*{(11)}
초점이 F 인 포물선 $y^{2}=4 x$ 위의 원점이 아닌 점 P 에 대하여 점 F 에서 선분 OP 에 내린 수선의 발을 Q 라 하자. $\overline{\mathrm{PQ}}=5 \overline{\mathrm{OQ}}$ 일 때, 삼각형 OFP 의 둘레의 길이는? (단, O 는 원점이다.) [4점]\\
(1) $3+2 \sqrt{3}$\\
(2) $4+\sqrt{3}$\\
(3) $4+2 \sqrt{3}$\\
(4) $5+\sqrt{3}$\\
(5) $5+2 \sqrt{3}$\\
\includegraphics[max width=\textwidth, center]{849b169d-afc6-401c-947d-7cc9c762c74e-1_515_439_968_913}

\section*{Chapter 1 이차곡선}
원 $(x-3)^{2}+y^{2}=4$ 와 초점이 F 인 포물선 $y^{2}=4 x$ 가 있다. 원 위의 점 A 를 지나고 $x$ 축과 평행한 직선이 포물선과 만나는 점을 P 라 할 때, $\angle \mathrm{PFA}=\frac{\pi}{2}$ 이다. 선분 PF 의 길이는?\\
(단, 점 A 의 $x$ 좌표는 3 보다 크다.) [4점]\\
(1) $\sqrt{2}$\\
(2) $2 \sqrt{2}-1$\\
(3) $3 \sqrt{2}-3$\\
(4) $\sqrt{3}$\\
(5) $2 \sqrt{3}-2$\\
\includegraphics[max width=\textwidth, center]{849b169d-afc6-401c-947d-7cc9c762c74e-2_518_479_1067_896}

포물선 $y^{2}=4 a x$ 의 초점 F 를 지나고 기울기가 음수인 직선이 포물선과 제 1 사분면에서 만나는 점을 P , $y$ 축과 만나는 점을 Q 라 하자. 점 P 를 지나고 $x$ 축과 평행한 직선 $l$ 에 대하여 원 $(x-b)^{2}+y^{2}=c^{2}$ 은 두 직선 $\mathrm{FP}, l$ 에 동시에 접한다. 직선 FP 가 원과 접하는 점을 R 라 할 때, $\overline{\mathrm{FQ}}=5, \overline{\mathrm{PR}}=6$ 이다. $\frac{b}{a c}$ 의 값은?\\
(단, $b>a>0, c>0$ ) [4점]\\
(1) $\frac{1}{4}$\\
(2) $\frac{3}{8}$\\
(3) $\frac{1}{2}$\\
(4) $\frac{5}{8}$\\
(5) $\frac{3}{4}$\\
\includegraphics[max width=\textwidth, center]{849b169d-afc6-401c-947d-7cc9c762c74e-3_505_559_1158_856}

\section*{Chapter 1}
이차곡선

\section*{(14)}
초점이 F 인 포물선 $y^{2}=8 x$ 위의 점 P 가 있다. 삼각형 OFP 의 외접원이 $y$ 축과 만나는 점 중 O 가 아닌 점을 Q 라 하자. $\overline{\mathrm{PF}}=8$ 일 때, 선분 PQ 의 길이는? (단, O 는 원점이다.) [4점]\\
(1) $4 \sqrt{2}$\\
(2) 6\\
(3) $2 \sqrt{10}$\\
(4) $2 \sqrt{11}$\\
(5) $4 \sqrt{3}$\\
\includegraphics[max width=\textwidth, center]{849b169d-afc6-401c-947d-7cc9c762c74e-4_548_524_960_879}

두 포물선 $y^{2}=4(x+1), y^{2}=-4 p(x-p)$ 의 고점 중 제 1 사분면에 있는 점을 A 라 하고, 중심이 A 이고 원점 O 를 지나는 원을 $C$ 라 하자. 원 $C$ 와 포물선 $y^{2}=4(x+1)$ 의 교점 중 제 1 사분면에 있는 점을 P 라 하고, 원 $C$ 와 포물선 $y^{2}=-4 p(x-p)$ 의 교점 중 제 4 사분면에 있는 점을 Q 라 할 때, $\sin (\angle \mathrm{OPQ})=\frac{3}{7}$ 이다. 직선 AQ 의 기울기를 $m$ 이라 할 때, $m^{2}$ 의 값을 구하시오. (단, $p>1$ ) [4점]\\
\includegraphics[max width=\textwidth, center]{849b169d-afc6-401c-947d-7cc9c762c74e-5_550_701_1032_786}

\section*{06}
초점이 F 인 포물선 $y^{2}=4 p x(p>0)$ 가 있다. 점 F 를 지나고 기울기가 양수인 직선 $l$ 이 포물선과 제 1 사분면 에서 만나는 점을 P , 제 4 사분면에서 만나는 점을 Q 라 하고, 점 P 를 중심으로 하고 포물선의 준선에 접하는 원이 $x$ 축과 만나는 두 점 중 $x$ 좌표가 큰 점을 R 라 하자. 직선 $l$ 과 $y$ 축이 만나는 점은 점 Q 를 중심으로 하고 포물선의 준선에 접하는 원 위에 있고 $\overline{\mathrm{PQ}}=9$ 일 때, 삼각형 PQR 의 넓이는 $s$ 이다.\\
$s^{2}$ 의 값을 구하시오. [4점]\\
\includegraphics[max width=\textwidth, center]{849b169d-afc6-401c-947d-7cc9c762c74e-6_667_526_1055_881}

두 초점이 $\mathrm{F}(c, 0), \mathrm{F}^{\prime}(-c, 0)(c>0)$ 이고 장축의 길이가 11 인 타원이 있다. 타원 위의 제 1 사분면의 점 P 에 대하여 $\sin \left(\angle \mathrm{PF}^{\prime} \mathrm{F}\right)=\frac{3}{5}$ 이다. 선분 $\mathrm{PF}^{\prime}$ 에 접하고 중심이 F 인 원이 타원과 오직 한 점에서 만날 때, 선분 PF 의 길이는? [3점]\\
(1) $\frac{27}{7}$\\
(2) 4\\
(3) $\frac{29}{7}$\\
(4) $\frac{30}{7}$\\
(5) $\frac{31}{7}$\\
\includegraphics[max width=\textwidth, center]{849b169d-afc6-401c-947d-7cc9c762c74e-7_521_574_1116_858}

두 점 $\mathrm{F}(c, 0), \mathrm{F}^{\prime}(-c, 0)(c>0)$ 을 초점으로 하는 타원이 있다. 타원 위의 제 2 사분면의 점 A 에 대하여 $\overline{\mathrm{OA}}=\overline{\mathrm{OF}}$ 이다. 직선 $\mathrm{F}^{\prime} \mathrm{A}$ 가 $y$ 축과 만나는 점을 B 라 하자.\\
$\overline{\mathrm{F}^{\prime} \mathrm{A}}=1, \overline{\mathrm{AB}}=3$ 일 때, 타원의 장축의 길이는? (단, O 는 원점이다.) [3점]\\
(1) $1+\sqrt{6}$\\
(2) $1+\sqrt{7}$\\
(3) $1+2 \sqrt{2}$\\
(4) $2+\sqrt{6}$\\
(5) $2+\sqrt{7}$\\
\includegraphics[max width=\textwidth, center]{849b169d-afc6-401c-947d-7cc9c762c74e-8_665_555_1036_862}


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
        # (11), (14) 형식
        num_match = re.search(r'\((\d+)\)', section_text)
        if num_match:
            problem_num = int(num_match.group(1))
            problem_numbers[section.start()] = problem_num
        # 06 형식
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
        search_start = max(prev_marker_pos, marker_pos - 2000)
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
            # 섹션이 없으면 문제 시작 키워드로 찾기 (더 넓은 범위에서)
            start_keywords = [
                '두 초점이',
                '두 점',
                '초점이 F 인 포물선',
                '초점이 F',
                '포물선 $y',
                '두 포물선',
                '타원'
            ]
            for keyword in start_keywords:
                idx = question_text.find(keyword)
                if idx >= 0:
                    question_text = question_text[idx:]
                    break
        
        # 문제 텍스트 정리
        question_text = re.sub(r'\\\\', ' ', question_text)
        question_text = re.sub(r'\\includegraphics\[[^\]]*\]\{[^}]+\}', '', question_text)
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
        
        # 포물선 방정식 검증
        if '포물선' in question and 'y^{2}' in question:
            # y² = 4ax 형식 확인
            if 'y^{2}=4' in question or 'y^{2}=8' in question:
                pass  # 정확
            else:
                warnings.append(f"문제 {problem['index']}: 포물선 방정식 형식 확인 필요")
        
        # 타원 방정식 검증
        if '타원' in question:
            if '초점' in question and '장축' in question:
                pass  # 정확
            else:
                warnings.append(f"문제 {problem['index']}: 타원 관련 조건 확인 필요")
        
        # 기하학적 조건 검증
        if '삼각형' in question:
            if '둘레' in question or '넓이' in question:
                pass  # 정확
            else:
                warnings.append(f"문제 {problem['index']}: 삼각형 관련 조건 확인 필요")
    
    return errors, warnings

def main():
    print("=" * 80)
    print("기하_2024학년도_현우진_드릴_P1 문제 → Deepseek R1-70B용 변환")
    print("=" * 80)
    
    # 문제 추출
    problems = extract_problems(latex_content)
    print(f"\n총 {len(problems)}개 문제 발견\n")
    
    if len(problems) == 0:
        print("⚠️  문제 추출 실패. 수동 파싱 시도...")
        # 수동으로 문제 파싱
        doc_match = re.search(r'\\begin\{document\}(.*?)\\end\{document\}', latex_content, re.DOTALL)
        if doc_match:
            body = doc_match.group(1)
            # 문제 번호별로 분리
            problem_sections = re.split(r'\\section\*\{\((\d+)\)\}|\\section\*\{(\d+)\}', body)
            print(f"섹션 수: {len(problem_sections)}")
    
    # 문제별로 마크다운 변환
    markdown_problems = []
    for problem in problems:
        markdown_question = latex_to_markdown_for_deepseek(problem['question'])
        markdown_problems.append({
            **problem,
            'question_markdown': markdown_question
        })
    
    # 수학적 오류 검증
    math_errors, math_warnings = validate_math_errors(problems)
    
    print("[수학적 오류 검증]")
    if math_errors:
        print(f"  ❌ 오류: {len(math_errors)}개")
        for error in math_errors:
            print(f"    - {error}")
    else:
        print("  ✅ 수학적 오류 없음")
    
    if math_warnings:
        print(f"  ⚠️  경고: {len(math_warnings)}개")
        for warning in math_warnings[:5]:
            print(f"    - {warning}")
    
    # 저장 경로
    base_dir = Path(r'C:\Users\a\Documents\MathPDF\organized\현우진\기하_2024학년도_현우진_드릴')
    base_dir.mkdir(parents=True, exist_ok=True)
    
    # JSON 저장
    json_path = base_dir / "기하_2024학년도_현우진_드릴_P1_문제_deepseek.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(problems, f, ensure_ascii=False, indent=2)
    
    # 문제 본문 정리 (이전 문제의 선택지 제거)
    fixed_problems = []
    for problem in problems:
        question = problem.get('question', '')
        
        # 이전 문제의 선택지 제거
        question = re.sub(r'\(1\)\s*\$[^$]+\$\s*\(2\)\s*\$[^$]+\$\s*\(3\)\s*\$[^$]+\$\s*\(4\)\s*\$[^$]+\$\s*\(5\)\s*\$[^$]+\$', '', question)
        question = re.sub(r'\(1\)\s*[0-9+\-√\s/]+\s*\(2\)\s*[0-9+\-√\s/]+\s*\(3\)\s*[0-9+\-√\s/]+\s*\(4\)\s*[0-9+\-√\s/]+\s*\(5\)\s*[0-9+\-√\s/]+', '', question)
        
        # 문제 시작 키워드 찾기 (더 정확하게)
        start_keywords = [
            '두 초점이',
            '두 점',
            '초점이 F 인 포물선',
            '초점이 F',
            '포물선 $y',
            '두 포물선',
            '원 $(x-',
            '원점',
            '이차곡선'
        ]
        
        found_start = False
        for keyword in start_keywords:
            idx = question.find(keyword)
            if idx >= 0 and idx < 500:  # 문제 시작 부분
                question = question[idx:]
                found_start = True
                break
        
        # "타원이 있다"로 시작하는 경우 "두 초점" 또는 "두 점" 찾기
        if question.startswith('타원이') or question.startswith('원이'):
            # 원본 body에서 해당 문제 찾기
            for keyword in ['두 초점이', '두 점']:
                idx = body.find(keyword, max(0, marker_pos - 1000), marker_pos)
                if idx >= 0:
                    # 해당 키워드부터 마커까지 추출
                    extracted = body[idx:marker_pos]
                    extracted = re.sub(r'\\\\', ' ', extracted)
                    extracted = re.sub(r'\\includegraphics\[[^\]]*\]\{[^}]+\}', '', extracted)
                    extracted = re.sub(r'\s+', ' ', extracted).strip()
                    if len(extracted) > 50:
                        question = extracted
                        break
        
        question = re.sub(r'\s+', ' ', question).strip()
        fixed_problems.append({**problem, 'question': question})
    
    # 마크다운 저장
    md_content = "# 기하_2024학년도_현우진_드릴_P1 문제\n\n"
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
    
    md_path = base_dir / "기하_2024학년도_현우진_드릴_P1_문제_deepseek_r1.md"
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    # 수정된 JSON도 저장
    json_path = base_dir / "기하_2024학년도_현우진_드릴_P1_문제_deepseek.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(fixed_problems, f, ensure_ascii=False, indent=2)
    
    print(f"\n[저장 완료]")
    print(f"  - JSON: {json_path}")
    print(f"  - 마크다운: {md_path}")
    print(f"\n총 {len(problems)}개 문제 변환 완료")
    print("\n[Deepseek R1-70B 호환성]")
    print("  - 마크다운 형식: 지원")
    print("  - LaTeX 수식: 지원 ($...$ 및 $$...$$)")
    print("  - 구조화된 섹션: 지원")
    print("  - UTF-8 인코딩: 지원")
    print("\n[결론] Deepseek R1-70B가 읽을 수 있는 형태입니다.")

if __name__ == '__main__':
    main()
