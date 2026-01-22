# convert_haktong_p7_problems_latex.py
# 확통_2024학년도_현우진_드릴_P7_문제 LaTeX 변환

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
정규분포 $\mathrm{N}\left(-m, \sigma^{2}\right)$ 을 따르는 확률변수 $X$ 와 정규분포 $\mathrm{N}\left(m^{2}, \sigma^{2}\right)$ 을 따르는 확률변수 $Y$ 가 다음 조건을 만족시킨다.\\
(가) $\mathrm{P}(X \leq m)=0.9772$\\
(나) $\mathrm{P}(Y \leq m)=0.1587$

확률변수 $X$ 의 확률밀도함수 $f(x)$ 와 확률변수 $Y$ 의 확률밀도함수 $g(x)$ 에 대하여 $f(a)=g(a)$ 일 때, $\mathrm{P}(X \geq a)$ 의 값을 오른쪽 표준정규분포표를 이용하여 구한 것은? [4점]\\
(1) 0.0228\\
(2) 0.0668\\
(3) 0.1587\\
(4) 0.2417\\
(5) 0.3085

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

\section*{Chapter 3}
\section*{통계}
\section*{(1)}
확률변수 $X$ 는 정규분포 $\mathrm{N}\left(m_{1}, 2^{2}\right)$, 확률변수 $Y$ 는 정규분포 $\mathrm{N}\left(m_{2}, 2^{2}\right)$ 을 따르고, 확률변수 $X$ 와 $Y$ 의 확률밀도함수는 각각 $f(x)$ 와 $g(x)$ 이다. 방정식

$$
|f(x)-g(x)|=f(x)+g(x)-2 g(6)
$$

의 실근이 2,3 일 때, $\mathrm{P}(X \leq 3)+\mathrm{P}(Y \leq 1)$ 의 값을 오른쪽 표준정규분포표를 이용하여 구한 것은? [4점]

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

(1) 0.8502\\
(2) 0.8641\\
(3) 0.9081\\
(4) 0.9560\\
(5) 0.9834

\section*{(12)}
두 확률변수 $X$ 와 $Y$ 는 각각 정규분포 $\mathrm{N}\left(m_{1}, 2^{2}\right)$ 과 $\mathrm{N}\left(m_{2}, 2^{2}\right)$ 을 따르고, $X$ 와 $Y$ 의 확률밀도함수는 각각 $f(x)$ 와 $g(x)$ 이다. 양의 실수 $t$ 에 대하여 $x$ 에 대한 방정식

$$
\{f(x)-t\}\{g(x)-t\}=0
$$

의 서로 다른 실근의 개수를 $h(t)$ 라 하자.

$$
h(f(2))<h(f(4))<h(g(4))
$$

일 때, $\mathrm{P}\left(m_{2} \leq X \leq m_{2}+3\right)=p$ 이다.\\
$1000 \times p$ 의 값을 오른쪽 표준정규분포표를 이용하여 구하시오. [4점]

\begin{center}
\begin{tabular}{c|c}
\hline
$z$ & $\mathrm{P}(0 \leq Z \leq z)$ \\
\hline
0.5 & 0.192 \\
\hline
1.0 & 0.341 \\
\hline
1.5 & 0.433 \\
\hline
2.0 & 0.477 \\
\hline
\end{tabular}
\end{center}

\section*{Chapter 3}
\section*{통계}
\section*{13}
정수 $m$ 에 대하여 정규분포 $\mathrm{N}\left(m, 2^{2}\right)$ 을 따르는 확률변수 $X$ 의 확률밀도함수는 $f(x)$ 이다. 자연수 $n$ 에 대하여 집합

$$
A_{n}=\{f(k) \mid k \text { 는 } n \text { 이하의 자연수 }\}
$$

의 원소의 개수를 $a_{n}$ 이라 하자.

$$
a_{2 p}=a_{p}+1
$$

을 만족시키는 모든 자연수 $p$ 를 작은 수부터 크기순으로 나열하면 $\alpha, \beta$, $\gamma$ 이고 $\alpha+\beta+\gamma=18$ 이다. $1000 \times \mathrm{P}(\beta-\alpha \leq X \leq \gamma+\alpha)$ 의 값을 오른쪽 표준정규분포표를 이용하여 구하시오. [4점]

\begin{center}
\begin{tabular}{c|c}
\hline
$z$ & $\mathrm{P}(0 \leq Z \leq z)$ \\
\hline
0.5 & 0.192 \\
\hline
1.0 & 0.341 \\
\hline
1.5 & 0.433 \\
\hline
2.0 & 0.477 \\
\hline
2.5 & 0.494 \\
\hline
\end{tabular}
\end{center}

\section*{Chapter 3}
\section*{통계}
\begin{center}
\includegraphics[max width=\textwidth]{a2c107d8-7a1e-4e4e-bef8-80a7f38924a8-5_238_242_546_178}
\end{center}

어느 모집단의 확률변수 $X$ 의 확률분포가 다음 표와 같다.

\begin{center}
\begin{tabular}{|c|c|c|c|c|c|}
\hline
$X$ & -2 & -1 & 0 & $a$ & 합계 \\
\hline
$\mathrm{P}(X=x)$ & $\frac{1}{5}$ & $\frac{1}{5}$ & $\frac{1}{5}$ & $\frac{2}{5}$ & 1 \\
\hline
\end{tabular}
\end{center}

이 모집단에서 임의추출한 크기가 16 인 표본의 표본평균 $\bar{X}$ 에 대하여 $\mathrm{V}(\bar{X})=\frac{2}{5}$ 일 때, 양수 $a$ 의 값은?\\
(1) 2\\
(2) 3\\
(3) 4\\
(4) 5\\
(5) 6

\section*{Chapter 3 \\
 통계}
\begin{center}
\includegraphics[max width=\textwidth]{a2c107d8-7a1e-4e4e-bef8-80a7f38924a8-6_251_259_535_174}
\end{center}

숫자 $2,4, a$ 가 하나씩 적혀 있는 공이 각각 1 개 이상씩 들어 있는 주머니가 있다.\\
이 주머니에서 임의로 1 개의 공을 꺼내어 적혀 있는 수를 확인한 후 다시 넣는 시행을 한다. 이 시행을 1 번 하여 확인한 수를 확률변수 $X$ 라 하고, 이 시행을 2 번 반복하여 확인한 2 개의 수의 평균을 확률변수 $\bar{X}$ 라 하자.

$$
\mathrm{P}(\bar{X}=2)=\frac{4}{81}, \quad \mathrm{P}(\bar{X}=3)=\frac{40}{81}
$$

일 때, $\frac{\mathrm{P}(\bar{X}<3)}{\mathrm{P}(X=a)}$ 의 값은? (단, $a$ 는 2,4 가 아닌 자연수이다.) [4점]\\
(1) $\frac{14}{27}$\\
(2) $\frac{5}{9}$\\
(3) $\frac{16}{27}$\\
(4) $\frac{17}{27}$\\
(5) $\frac{2}{3}$

\section*{Chapter 3}
\section*{통계}
정규분포 $\mathrm{N}\left(0,2^{2}\right)$ 을 따르는 모집단에서 크기가 4 인 표본을 임의추출하여 구한 표본평균을 $\bar{X}$, 정규분포 $\mathrm{N}\left(4,5^{2}\right)$ 을 따르는 모집단에서 크기가 $n$ 인 표본을 임의추출하여 구한 표본평균을 $\bar{Y}$ 라 하자.\\
$\mathrm{P}(\bar{X} \leq 1) \geq \mathrm{P}(\bar{Y} \geq 3)$ 을 만족시키는 자연수 $n$ 의 최댓값을 구하시오. [4점]

어느 공장에서 생산하는 과자 한 봉지의 무게는 평균이 $m$ 이고 표준편차가 $\sigma$ 인 정규분포를 따른다고 한다. 이 공장에서 생산한 과자 25 봉지를 임의추출하여 구한 과자 한 봉지의 무게의 표본평균이 $\overline{x_{1}}$ 일 때, 모평균 $m$ 에 대한 신뢰도 $95 \%$ 의 신뢰구간이 $a \leq m \leq b$ 이다. 이 공장에서 생산한 과자 100 봉지를 임의추출하여 구한 과자 한 봉지의 무게의 표본평균이 $\overline{x_{2}}$ 일 때, 모평균 $m$ 에 대한 신뢰도 $95 \%$ 의 신뢰구간이 $c \leq m \leq d$ 이다. $50 \overline{x_{1}}=49 \overline{x_{2}}$ 이고 $c-a=1.4, d=50.4$ 일 때, $b$ 의 값은? (단, 무게의 단위는 g 이고, $Z$ 가 표준정규분포를 따르는 확률변수일 때, $\mathrm{P}(|Z| \leq 1.96)=0.95$ 로 계산한다.) [3점]\\
(1) 49.8\\
(2) 49.9\\
(3) 50.0\\
(4) 50.1\\
(5) 50.2

\section*{Chapter 3 \\
 통계}
\section*{(18)}
어느 제과점에서 만드는 케이크 1 개의 무게는 평균이 $m$ 이고 표준편차가 $\sigma$ 인 정규분포를 따른다고 한다. 이 제과점에서 만든 케이크 16 개를 임의추출하여 얻은 케이크 1 개의 무게의 표본평균이 $\overline{x_{1}}$ 일 때, 모평균 $m$ 에 대한 신뢰도 $95 \%$ 의 신뢰구간이

$$
a \leq m \leq a+9.8
$$

이다. 이 제과점에서 만든 케이크 36 개를 임의추출하여 얻은 케이크 1 개의 무게의 표본평균이 $\overline{x_{2}}$ 일 때, 모평균 $m$ 에 대한 신뢰도 $99 \%$ 의 신뢰구간이

$$
\frac{100}{103} \overline{x_{1}}-\frac{a}{30} \leq m \leq \frac{100}{103} \overline{x_{1}}+\frac{a}{30}
$$

이다. $\overline{x_{2}}$ 의 값은? (단, 무게의 단위는 g 이고, $Z$ 가 표준정규분포를 따르는 확률변수일 때, $\mathrm{P}(|Z| \leq 1.96)=0.95, \mathrm{P}(|Z| \leq 2.58)=0.99$ 로 계산한다. $)$ [4점]\\
(1) 125.1\\
(2) 130.0\\
(3) 134.9\\
(4) 139.8\\
(5) 144.7


\end{document}"""

def extract_problems_from_latex(latex_content):
    """LaTeX에서 문제 추출"""
    body = extract_body(latex_content)
    problems = []
    
    # 섹션 헤더 찾기
    section_pattern = r'\\section\*?\{([^}]+)\}'
    sections = list(re.finditer(section_pattern, body))
    
    # 점수 마커 찾기 ([4점], [3점])
    point_pattern = r'\[([34])점\]'
    point_markers = list(re.finditer(point_pattern, body))
    
    print(f"📊 발견된 섹션: {len(sections)}개")
    print(f"📊 발견된 점수 마커: {len(point_markers)}개")
    
    # 문제 시작 패턴 (통계 관련)
    problem_start_patterns = [
        r'정규분포',
        r'확률변수',
        r'어느 모집단',
        r'숫자.*?공',
        r'주머니',
        r'어느 공장',
        r'어느 제과점',
    ]
    
    # 문제 번호 추출 (섹션과 점수 마커의 위치 관계로 매칭)
    problem_number_map = {}
    
    # 섹션별 문제 번호 추출
    section_numbers = []
    for section in sections:
        section_pos = section.start()
        section_text = section.group(1).strip()
        problem_num = None
        
        # 숫자만 있는 경우 (예: "13")
        if re.match(r'^\d+$', section_text):
            problem_num = int(section_text)
        # 괄호 안 숫자 (예: "(1)", "(12)", "(18)")
        elif re.match(r'^\(\d+\)$', section_text):
            problem_num = int(re.search(r'\d+', section_text).group())
        
        if problem_num:
            section_numbers.append((section_pos, problem_num))
    
    # 각 점수 마커에 대해 가장 가까운 섹션 번호 매핑
    used_sections = set()
    
    for i, marker in enumerate(point_markers):
        marker_pos = marker.start()
        point = int(marker.group(1))
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
    # P7 문제 순서: 첫 번째(섹션없음, 번호 없음), 1, 12, 13, 4(섹션없음), 5(섹션없음), 6(섹션없음), 7(섹션없음), 18
    used_numbers = set(problem_number_map.values())
    section_less_indices = [i for i in range(len(point_markers)) if i not in problem_number_map]
    
    # 섹션이 없는 문제들의 예상 번호 (순서대로)
    # 첫 번째 문제는 번호 없음(특별 처리), 나머지는 4, 5, 6, 7
    expected_numbers = [4, 5, 6, 7]  # 섹션 없는 문제들의 번호
    for idx, problem_idx in enumerate(section_less_indices):
        if idx == 0:
            # 첫 번째 문제는 번호 없음으로 처리 (나중에 1번으로 할당)
            continue
        elif idx - 1 < len(expected_numbers):
            if expected_numbers[idx - 1] not in used_numbers:
                problem_number_map[problem_idx] = expected_numbers[idx - 1]
                used_numbers.add(expected_numbers[idx - 1])
        else:
            # 예상 번호가 부족하면 사용되지 않은 번호 중 최소값 사용
            candidate = 1
            while candidate in used_numbers or candidate in problem_number_map.values():
                candidate += 1
            problem_number_map[problem_idx] = candidate
    
    # 첫 번째 문제에 번호 할당 (1번이 이미 사용되었는지 확인)
    if section_less_indices and 0 in section_less_indices:
        if 1 not in used_numbers:
            problem_number_map[0] = 1
        else:
            # 1번이 이미 사용되었으면 사용되지 않은 최소 번호 사용
            candidate = 1
            while candidate in used_numbers or candidate in problem_number_map.values():
                candidate += 1
            problem_number_map[0] = candidate
    
    print(f"📊 문제 번호 매핑: {problem_number_map}")
    
    # 각 점수 마커를 기준으로 문제 추출
    seen_questions = set()
    
    for i, marker in enumerate(point_markers):
        marker_pos = marker.start()
        point = int(marker.group(1))
        
        # 이전 마커 위치
        prev_marker_pos = point_markers[i-1].end() if i > 0 else 0
        
        # 다음 마커 위치
        next_marker_pos = point_markers[i+1].start() if i < len(point_markers) - 1 else len(body)
        
        # 문제 본문 추출 (더 넓은 범위)
        search_start = max(prev_marker_pos, marker_pos - 4000)
        question_text = body[search_start:marker_pos]
        
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
            
            # 문제 06번 특수 처리: "어느 공장"으로 시작하는 부분 찾기
            if '정규분포를 따른다고 한다' in question_text and '어느 공장' not in question_text:
                # 이전 부분에서 "어느 공장" 찾기
                extended_search = body[max(0, search_start - 200):marker_pos]
                factory_match = re.search(r'어느 공장.*?정규분포를 따른다고 한다', extended_search, re.DOTALL)
                if factory_match:
                    factory_start = max(0, search_start - 200) + factory_match.start()
                    question_text = body[factory_start:marker_pos]
        
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
            options_search_text = body[marker_pos:min(marker_pos + 1000, search_end)]
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
        print(f"✅ 문제 {problem['index']} 추출 완료 ({answer_type}, {len(options)}개 선택지, {point}점)")
    
    return problems

def main():
    print("=" * 80)
    print("확통_2024학년도_현우진_드릴_P7_문제 변환")
    print("=" * 80)
    
    # 문제 추출
    problems = extract_problems_from_latex(latex_content)
    
    print(f"\n📊 총 {len(problems)}개 문제 추출 완료\n")
    
    # 검토
    is_valid = review_problems(problems)
    
    # 저장
    base_dir = Path(r'C:\Users\a\Documents\MathPDF\organized\현우진\확통_2005학년도_현우진_드릴')
    base_filename = '확통_2024학년도_현우진_드릴_P7_문제'
    
    if is_valid or len(problems) > 0:
        save_for_deepseek(problems, base_dir, base_filename)
        print(f"\n✅ 저장 완료: {base_dir}")
    else:
        print("\n❌ 검토 실패")

if __name__ == '__main__':
    main()
