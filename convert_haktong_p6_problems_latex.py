# convert_haktong_p6_problems_latex.py
# 확통_2024학년도_현우진_드릴_P6_문제 LaTeX 변환

import json
import re
import sys
from pathlib import Path

# Windows 콘솔 인코딩 설정
if sys.platform == 'win32':
    import os
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')

from latex_utils import extract_body, clean_latex_text, extract_options_generic
from convert_template import review_problems, save_for_deepseek

# LaTeX 내용 (파일에서 읽기)
latex_file = Path(__file__).parent / 'haktong_p6_problems_latex.txt'
if latex_file.exists():
    with open(latex_file, 'r', encoding='utf-8') as f:
        latex_content = f.read()
else:
    # 직접 입력
    latex_content = r"""% This LaTeX document needs to be compiled with XeLaTeX.
\documentclass[10pt]{article}
\usepackage[utf8]{inputenc}
\usepackage{amsmath}
\usepackage{amsfonts}
\usepackage{amssymb}
\usepackage[version=4]{mhchem}
\usepackage{stmaryrd}
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
\section*{Chapter 3}
통계

이산확률변수 $X$ 가 가지는 값이 1 부터 4 까지의 자연수이고, 확률변수 $X$ 는 다음 조건을 만족시킨다.\\
(가) $\mathrm{P}(X=1)=\frac{1}{2}$\\
(나) $\mathrm{P}(X>n+1)=\{\mathrm{P}(X>n)\}^{2}(n=1,2)$\\
$\mathrm{E}(X)$ 의 값은? [4점]\\
(1) $\frac{13}{8}$\\
(2) $\frac{27}{16}$\\
(3) $\frac{7}{4}$\\
(4) $\frac{29}{16}$\\
(5) $\frac{15}{8}$

\section*{Chapter 3 \\
 통계}
(13)

이산확률변수 $X$ 의 확률질량함수가

$$
\mathrm{P}\left(X=a_{i}\right)=p_{i}(i=1,2,3)
$$

이고, $a_{i}$ 가 다음 조건을 만족시킨다.\\
(가) $a_{1}+p_{1}=\frac{5}{4}$\\
(나) 세 수 $a_{1}, a_{2}, a_{3}$ 은 이 순서대로 공차가 2 인 등차수열을 이룬다.\\
$\mathrm{E}(X)=a_{2}$ 이고 $\mathrm{V}(X)=2$ 일 때, $\mathrm{E}\left(X^{2}\right)$ 의 값은? [4점]\\
(1) 8\\
(2) 9\\
(3) 10\\
(4) 11\\
(5) 12

\section*{Chapter 3 \\
 통계}
10 개의 서로 다른 양수 $a_{1}, a_{2}, \cdots, a_{10}$ 에 대하여 이차방정식

$$
x^{2}-x-a_{k}=0(k=1,2, \cdots, 10)
$$

의 두 실근을 $x_{2 k-1}, x_{2 k}$ 라 하자. 이산확률변수 $X$ 가 갖는 값이 $x_{1}, x_{2}, x_{3}, x_{4}, \cdots, x_{20}$ 이고, 20 이하의 임의의 두 자연수 $m, n$ 에 대하여 $\mathrm{P}\left(X=x_{m}\right)=\mathrm{P}\left(X=x_{n}\right)$ 이다. $\sum_{k=1}^{10} a_{k}=10$ 일 때, $\mathrm{V}(X)$ 의 값은? [4점]\\
(1) $\frac{3}{4}$\\
(2) $\frac{7}{8}$\\
(3) 1\\
(4) $\frac{9}{8}$\\
(5) $\frac{5}{4}$

\section*{Chapter 3 \\
 통계}
\section*{(15)}
숫자 $1,1,1,1,2$ 가 하나씩 적혀 있는 5 개의 공이 들어 있는 주머니가 있다. 이 주머니에서 임의로 3 개의 공을 동시에 꺼내어 공에 적혀 있는 세 수를 확인한 후, 3 개의 공을 다시 주머니에 넣는 시행을 한다. 이 시행을 25 번 반복하여 확인한 75 개의 수의 합을 확률변수 $X$ 라 하자. $\mathrm{E}\left(X^{2}\right)$ 의 값은? [4점]\\
(1) 8094\\
(2) 8097\\
(3) 8100\\
(4) 8103\\
(5) 8106

\section*{Chapter 3 \\
 통계}
\section*{06}
50 개의 공과 비어 있는 주머니가 있다. 한 개의 주사위를 사용하여 다음 규칙에 따라 공을 주머니에 넣는 시행을 한다.\\
(가) 첫 번째 시행에서 주사위를 한 번 던져서 나온 눈의 수가 6 이면 공 1 개를 주머니에 넣고, 6 이 아니면 공 2 개를 주머니에 넣는다.\\
(나) $n(n \geq 2)$ 번째 시행에서 주사위를 한 번 던져서 나온 눈의 수가 6 이면 공 1 개를 주머니에 넣고, 6 이 아니면 첫 번째 시행에서 주머니에 넣은 공의 개수와 같은 개수의 공을 주머니에 넣는다.

25 번째 시행 후 주머니에 들어 있는 공의 개수를 확률변수 $X$ 라 할 때, $\mathrm{E}(2 X)$ 의 값을 구하시오. [4점]

\section*{Chapter 3 \\
 통계}
$a>\frac{5}{3}$ 인 실수 $a$ 에 대하여 연속확률변수 $X$ 가 갖는 값의 범위는 $0 \leq X \leq a$ 이고, 연속확률변수 $Y$ 가 갖는 값의 범위는 $0 \leq Y \leq 1$ 이다. 상수 $k$ 와 일차함수 $h(x)$ 에 대하여 확률변수 $X$ 의 확률밀도함수 $f(x)$ 는

$$
f(x)= \begin{cases}k x & \left(0 \leq x<\frac{2}{3}\right) \\ h(x) & \left(\frac{2}{3} \leq x \leq \frac{4}{3}\right) \\ k(x-a)+1 & \left(\frac{4}{3}<x \leq a\right)\end{cases}
$$

이고, 확률변수 $Y$ 의 확률밀도함수 $g(x)$ 는 $f(x)$ 의 역함수이다. 함수 $f(x)$ 가 닫힌구간 $[0, a]$ 에서 연속 이고, $\mathrm{P}\left(f\left(\frac{1}{3}\right) \leq Y \leq f\left(\frac{5}{3}\right)\right)=\frac{7}{9}$ 일 때, $f\left(\frac{5 k}{a}\right)=\frac{q}{p}$ 이다. $p+q$ 의 값을 구하시오.\\
(단, $p$ 와 $q$ 는 서로소인 자연수이다.) [4점]

\section*{Chapter 3 \\
 통계}
확률변수 $X$ 는 정규분포 $\mathrm{N}\left(10,2^{2}\right)$ 을 따르고, $m>10$ 인 상수 $m$ 에 대하여 확률변수 $Y$ 는 정규분포 $\mathrm{N}\left(m, 2^{2}\right)$ 을 따른다.\\
실수 $k$ 에 대하여 함수 $f(k)$ 를

$$
f(k)=\mathrm{P}(X \leq k)+\mathrm{P}(Y \geq k)
$$

라 하자. 함수 $f(k)$ 의 최댓값이 1.6826 일 때, $\mathrm{P}(13 \leq Y \leq 16)$ 의 값을 오른쪽 표준정규분포표를 이용하여 구한 것은? [4점]

\begin{center}
\begin{tabular}{c|c}
\hline
$z$ & $\mathrm{P}(0 \leq Z \leq z)$ \\
\hline
0.5 & 0.1915 \\
\hline
1.0 & 0.3413 \\
\hline
1.5 & 0.4332 \\
\hline
2.0 & 0.4772 \\
\hline
\end{tabular}
\end{center}

(1) 0.2857\\
(2) 0.4332\\
(3) 0.5328\\
(4) 0.6247\\
(5) 0.7745

\section*{Chapter 3}
\section*{통계}
정규분포를 따르고 표준편차가 2 인 두 확률변수 $X, Y$ 에 대하여 실수 전체의 집합에서 연속인 함수\\
$f(x)$ 가

$$
f(x)= \begin{cases}\mathrm{P}(X \leq x) & (x<1) \\ \mathrm{P}(Y \geq x+2) & (x \geq 1)\end{cases}
$$

이다. $f(4)+\mathrm{P}(Y \geq 2)=1$ 일 때, $f(-2)$ 의 값을 오른쪽 표준정규분포표를 이용하여 구한 것은? [4점]

\begin{center}
\begin{tabular}{c|c}
\hline
$z$ & $\mathrm{P}(0 \leq Z \leq z)$ \\
\hline
0.5 & 0.1915 \\
\hline
1.0 & 0.3413 \\
\hline
1.5 & 0.4332 \\
\hline
2.0 & 0.4772 \\
\hline
\end{tabular}
\end{center}

(1) 0.0228\\
(2) 0.0668\\
(3) 0.1587\\
(4) 0.2857\\
(5) 0.3085


\end{document}"""

def extract_problems_from_latex(latex_content):
    """LaTeX에서 문제 추출"""
    body = extract_body(latex_content)
    problems = []
    
    # 섹션 헤더 찾기
    section_pattern = r'\\section\*?\{([^}]+)\}'
    sections = list(re.finditer(section_pattern, body))
    
    # 점수 마커 찾기 ([4점])
    point_pattern = r'\[4점\]'
    point_markers = list(re.finditer(point_pattern, body))
    
    print(f"📊 발견된 섹션: {len(sections)}개")
    print(f"📊 발견된 점수 마커: {len(point_markers)}개")
    
    # 문제 시작 패턴 (통계 관련)
    problem_start_patterns = [
        r'이산확률변수',
        r'연속확률변수',
        r'확률변수',
        r'숫자.*?공',
        r'개의 공',
        r'주머니',
        r'공과',
        r'정규분포',
    ]
    
    # 문제 번호 추출 (섹션과 점수 마커의 위치 관계로 매칭)
    problem_number_map = {}
    
    # 섹션별 문제 번호 추출
    section_numbers = []
    for section in sections:
        section_pos = section.start()
        section_text = section.group(1).strip()
        problem_num = None
        
        # 숫자만 있는 경우 (예: "06")
        if re.match(r'^\d+$', section_text):
            problem_num = int(section_text)
        # 괄호 안 숫자 (예: "(13)", "(15)")
        elif re.match(r'^\(\d+\)$', section_text):
            problem_num = int(re.search(r'\d+', section_text).group())
        
        if problem_num:
            section_numbers.append((section_pos, problem_num))
    
    # 각 점수 마커에 대해 가장 가까운 섹션 번호 매핑
    # 섹션은 한 번만 사용되도록 함
    used_sections = set()
    
    for i, marker in enumerate(point_markers):
        marker_pos = marker.start()
        closest_section = None
        
        for section_pos, problem_num in section_numbers:
            if section_pos < marker_pos and (section_pos, problem_num) not in used_sections:
                # 다음 섹션 찾기
                next_section_pos = None
                for next_pos, _ in section_numbers:
                    if next_pos > section_pos:
                        if next_section_pos is None or next_pos < next_section_pos:
                            next_section_pos = next_pos
                
                # 다음 섹션이 없거나 마커 이후에 있으면 이 섹션 사용
                if next_section_pos is None or next_section_pos > marker_pos:
                    if closest_section is None or section_pos > closest_section[0]:
                        closest_section = (section_pos, problem_num)
        
        if closest_section:
            problem_number_map[i] = closest_section[1]
            used_sections.add(closest_section)
    
    # 섹션이 없는 문제들에 번호 할당
    # P6 문제 순서: 1(섹션없음), 13, 2(섹션없음), 15, 6, 7(섹션없음), 8(섹션없음), 9(섹션없음)
    used_numbers = set(problem_number_map.values())
    section_less_indices = [i for i in range(len(point_markers)) if i not in problem_number_map]
    
    # 섹션이 없는 문제들의 예상 번호 (순서대로)
    expected_numbers = [1, 2, 7, 8, 9]  # 섹션 없는 문제들의 번호
    for idx, problem_idx in enumerate(section_less_indices):
        if idx < len(expected_numbers):
            problem_number_map[problem_idx] = expected_numbers[idx]
        else:
            # 예상 번호가 부족하면 사용되지 않은 번호 중 최소값 사용
            candidate = 1
            while candidate in used_numbers or candidate in problem_number_map.values():
                candidate += 1
            problem_number_map[problem_idx] = candidate
    
    print(f"📊 문제 번호 매핑: {problem_number_map}")
    
    # 각 점수 마커를 기준으로 문제 추출
    seen_questions = set()
    
    for i, marker in enumerate(point_markers):
        marker_pos = marker.start()
        point = 4
        
        # 이전 마커 위치
        prev_marker_pos = point_markers[i-1].end() if i > 0 else 0
        
        # 다음 마커 위치
        next_marker_pos = point_markers[i+1].start() if i < len(point_markers) - 1 else len(body)
        
        # 문제 본문 추출 (더 넓은 범위)
        search_start = max(prev_marker_pos, marker_pos - 4000)
        question_text = body[search_start:marker_pos]
        
        # 마커 이후 텍스트
        after_marker = body[marker_pos:next_marker_pos]
        
        # 섹션 헤더 찾기 (문제 시작점으로 사용)
        section_before_marker = None
        for section in sections:
            if section.start() < marker_pos and section.start() >= search_start:
                if section_before_marker is None or section.start() > section_before_marker.start():
                    section_before_marker = section
        
        # 섹션이 있으면 섹션 이후부터, 없으면 문제 시작 패턴으로 찾기
        if section_before_marker:
            section_end = section_before_marker.end()
            question_text = body[section_end:marker_pos]
        else:
            # 문제 시작 패턴으로 실제 시작점 찾기
            for pattern in problem_start_patterns:
                match = re.search(pattern, question_text)
                if match:
                    question_text = question_text[match.start():]
                    break
        
        # 이미지 및 표 제거
        question_text = re.sub(r'\\includegraphics.*?\{[^}]+\}', '', question_text)
        question_text = re.sub(r'\\begin\{center\}.*?\\end\{center\}', '', question_text, flags=re.DOTALL)
        question_text = re.sub(r'\\begin\{tabular\}.*?\\end\{tabular\}', '', question_text, flags=re.DOTALL)
        
        # LaTeX 명령어 정리
        question_text = clean_latex_text(question_text)
        
        # 빈 문제 제거
        if not question_text.strip() or len(question_text.strip()) < 10:
            continue
        
        # 중복 제거
        question_key = question_text[:100].strip()
        if question_key in seen_questions:
            continue
        seen_questions.add(question_key)
        
        # 선택지 추출
        options = []
        answer_type = 'short_answer'
        
        search_end = next_marker_pos
        for section in sections:
            if section.start() > marker_pos:
                search_end = min(search_end, section.start())
                break
        
        # "구하시오" 확인
        has_구하시오 = '구하시오' in question_text or '구하시오' in body[marker_pos:min(marker_pos + 300, search_end)]
        
        if not has_구하시오:
            options_search_text = body[marker_pos:min(marker_pos + 800, search_end)]
            options_pattern = r'\(1\)|（1）'
            has_options_pattern = re.search(options_pattern, options_search_text)
            
            if has_options_pattern:
                options = extract_options_generic(options_search_text)
                if len(options) < 5:
                    # 수동 추출
                    for opt_num in range(1, 6):
                        pattern = rf'\({opt_num}\)\s*([^\(]+?)(?=\([1-5]\)|\\section|$)'
                        match = re.search(pattern, options_search_text, re.DOTALL)
                        if match:
                            opt_text = match.group(1).strip()
                            opt_text = re.sub(r'\\\\', '', opt_text)
                            opt_text = clean_latex_text(opt_text)
                            if opt_text:
                                opt_num_symbol = ["①", "②", "③", "④", "⑤"][opt_num-1]
                                options.append(f"{opt_num_symbol} {opt_text}")
                
                if len(options) >= 5:
                    answer_type = 'multiple_choice'
                elif len(options) > 0:
                    answer_type = 'multiple_choice'
        
        # 문제 번호 결정
        if i in problem_number_map:
            problem_num = problem_number_map[i]
        else:
            # 매핑이 없으면 순서대로
            problem_num = i + 1
        
        # 주제 감지
        topic = '통계'
        
        problem = {
            'index': f"{problem_num:02d}",
            'page': 1,
            'topic': topic,
            'question': question_text.strip(),
            'point': point,
            'answer_type': answer_type,
            'options': options
        }
        
        problems.append(problem)
        print(f"✅ 문제 {problem['index']} 추출 완료 ({answer_type}, {len(options)}개 선택지)")
    
    return problems

def main():
    print("=" * 80)
    print("확통_2024학년도_현우진_드릴_P6_문제 변환")
    print("=" * 80)
    
    # 문제 추출
    problems = extract_problems_from_latex(latex_content)
    
    print(f"\n📊 총 {len(problems)}개 문제 추출 완료\n")
    
    # 검토
    is_valid = review_problems(problems)
    
    # 저장
    base_dir = Path(r'C:\Users\a\Documents\MathPDF\organized\현우진\확통_2005학년도_현우진_드릴')
    base_filename = '확통_2024학년도_현우진_드릴_P6_문제'
    
    if is_valid or len(problems) > 0:
        save_for_deepseek(problems, base_dir, base_filename)
        print(f"\n✅ 저장 완료: {base_dir}")
    else:
        print("\n❌ 검토 실패")

if __name__ == '__main__':
    main()
