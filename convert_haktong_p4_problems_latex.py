# convert_haktong_p4_problems_latex.py
# 확통_2024학년도_현우진_드릴_P4_문제 LaTeX 변환

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
\usepackage{fvextra, csquotes}
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
\section*{03}
검은 공 3 개, 흰 공 2 개가 들어 있는 주머니가 있다. 이 주머니와 한 개의 주사위를 사용하여 다음 시행을 한다.

주사위를 한 번 던져 나온 눈의 수를 $k$ 라 할 때,\\
$k$ 가 홀수이면 주머니에서 임의로 2 개의 공을 동시에 꺼내고,\\
$k$ 가 짝수이면 주머니에서 임의로 $\frac{k}{2}$ 개의 공을 동시에 꺼낸다.

이 시행을 한 번 하여 주머니에서 꺼낸 공 중 적어도 하나가 흰 공일 확률은? [3점]\\
(1) $\frac{37}{60}$\\
(2) $\frac{13}{20}$\\
(3) $\frac{41}{60}$\\
(4) $\frac{43}{60}$\\
(5) $\frac{3}{4}$\\
\includegraphics[max width=\textwidth, center]{130484c4-d424-4c79-b60d-37ec25d7d5b3-01_190_184_1517_839}\\
\includegraphics[max width=\textwidth, center]{130484c4-d424-4c79-b60d-37ec25d7d5b3-01_339_345_1407_1106}

\section*{(6)}
집합 $X=\{1,2,3,4\}$ 에 대하여 $X$ 에서 $X$ 로의 모든 함수 $f$ 중에서 임의로 하나를 선택할 때, 이 함수가 다음 조건을 만족시킬 확률은 $\frac{q}{p}$ 이다. $p+q$ 의 값을 구하시오. (단, $p$ 와 $q$ 는 서로소인 자연수이다.) [4점]

\begin{displayquote}
(가) 함수 $f$ 의 치역과 합성함수 $f \circ f$ 의 치역은 서로 같다.\\
(나) $f(n) \leq f(4)(n=1,2,3)$
\end{displayquote}

\section*{Chapter 2}
\section*{확률}
\section*{05}
한 개의 주사위를 두 번 던져서 나오는 눈의 수를 차례로 $a, b$ 라 하자. 2 이상의 자연수 $m$ 에 대하여 $a$ 가 $m$ 이하의 짝수인 사건을 $A, a+b \leq 4$ 인 사건을 $B$ 라 할 때, 두 사건 $A, B$ 가 서로 독립이 되도록 하는 모든 $m$ 의 값의 합을 구하시오. [4점]

\section*{Chapter 2}
확률

\section*{06}
수직선의 원점에 점 P 가 있다. 한 개의 동전을 사용하여 다음 시행을 한다.

\section*{동전을 한 번 던져}
앞면이 나오면 점 P 를 양의 방향으로 1 만큼,\\
뒷면이 나오면 점 P 를 음의 방향으로 2 만큼\\
이동시킨다.

위의 시행을 5 번 반복할 때, $n(1 \leq n \leq 5)$ 번째 시행 후 점 P 가 이동된 점을 $\mathrm{P}_{n}$ 이라 하자.\\
$\overline{\mathrm{OP}_{1}}=\overline{\mathrm{OP}_{5}}$ 일 확률은? (단, O 는 원점이다.) [4점]\\
(1) $\frac{7}{32}$\\
(2) $\frac{1}{4}$\\
(3) $\frac{9}{32}$\\
(4) $\frac{5}{16}$\\
(5) $\frac{11}{32}$

\section*{Chapter 2 \\
 확률}
좌표평면 위의 점 $\mathrm{A}(-4,0)$ 에 점 P 가 있다. 한 개의 주사위를 사용하여 다음 시행을 한다.

주사위를 한 번 던져 나온 눈의 수가\\
6 의 약수이면 점 P 를 좌표평면에서 원점을 중심으로 시계 방향으로 $30^{\circ}$ 만큼 회전시키고,\\
6 의 약수가 아니면 점 P 를 좌표평면에서 원점을 중심으로 시계 반대 방향으로 $60^{\circ}$ 만큼 회전시킨다.

위의 시행을 5 번 반복하여 점 P 가 옮겨진 점을 Q 라 하자. 점 $\mathrm{B}(2,0)$ 에 대하여 삼각형 AQB 의 넓이가\\
$6 \sqrt{3}$ 일 확률은 $\frac{q}{p}$ 이다. $p+q$ 의 값을 구하시오. (단, $p$ 와 $q$ 는 서로소인 자연수이다.) [4점]

어느 학급의 학생 25 명이 각각 진로활동 프로그램 $\mathrm{A}, \mathrm{B}, \mathrm{C}$ 중 서로 다른 2 개를 선택하도록 한 결과 프로그램 A 를 선택한 학생은 17 명, 프로그램 B 를 선택한 학생은 14 명이었다. 이 학급의 학생 25 명 중에서 임의로 선택한 한 명이 프로그램 C 를 선택한 학생일 때, 이 학생이 프로그램 A 도 선택했을 확률은 $\frac{q}{p}$ 이다. $p+q$ 의 값을 구하시오. (단, $p$ 와 $q$ 는 서로소인 자연수이다.) [4점]

\section*{09}
그림과 같이 검은색 카드 1 장, 흰색 카드 9 장이 일렬로 나열되어 있다.\\
\includegraphics[max width=\textwidth, center]{130484c4-d424-4c79-b60d-37ec25d7d5b3-07_113_800_832_757}

다음 규칙에 따라 카드를 교체하는 시행을 한다.

흰색 카드 중에서 임의로 3 장을 선택하여 파란색 카드로 교체하고, 파란색 카드 중에서 임의로 1 장을 선택하여 검은색 카드로 교체한다.

이 시행을 한 번 하여 검은색 카드끼리 서로 이웃하지 않을 때, 2 장의 파란색 카드 사이에 적어도 1 장의 검은색 카드가 있을 확률은 ${ }_{p}^{q}$ 이다. $p+q$ 의 값을 구하시오. (단, $p$ 외 $q$ 는 서로소인 자연수이다.) [4점]

\section*{(10)}
좌표평면에 점 $\mathrm{P}_{0}(0,0)$ 이 있다.\\
한 개의 주사위를 사용하여 다음 규칙에 따라 점 $\mathrm{P}_{n}\left(x_{n}, y_{n}\right)$ ( $n$ 은 자연수)을 정한다.

\begin{itemize}
  \item 주사위를 한 번 던져 나온 눈의 수가 3 의 배수이면 점 $\mathrm{P}_{n-1}$ 을 $x$ 축의 양의 방향으로 1 만큼, $y$ 축의 양의 방향으로 1 만큼 이동시킨 점이 $\mathrm{P}_{n}$ 이다.
  \item 주사위를 한 번 던져 나온 눈의 수가 3 의 배수가 아닐 때, $x_{n-1}<y_{n-1}$ 이면 점 $\mathrm{P}_{n-1}$ 을 $x$ 축의 양의 방향으로 1 만큼, $x_{n-1} \geq y_{n-1}$ 이면 점 $\mathrm{P}_{n-1}$ 을 $y$ 축의 양의 방향으로 2 만큼 이동시킨 점이 $\mathrm{P}_{n}$ 이다.
\end{itemize}

위의 시행을 5 번 반복한 후 점 $\mathrm{P}_{5}$ 가 직선 $y=x$ 위에 있을 때, 네 점 $\mathrm{P}_{1}, \mathrm{P}_{2}, \mathrm{P}_{3}, \mathrm{P}_{4}$ 중 적어도 한 점이 직선 $y=x$ 위에 있을 확률은 $\frac{q}{p}$ 이다. $p+q$ 의 값을 구하시오. (단, $p$ 와 $q$ 는 서로소인 자연수이다.) [4점]

집합 $X=\{1,2,3,4\}$ 에 대하여 함수 $f: X \rightarrow X$ 가 다음 조건을 만족시킨다.\\
(가) $f(1)+f(2)+f(3)$ 은 3 의 배수이다.\\
(나) 함수 $f$ 의 역함수는 존재하지 않는다.

모든 함수 $f$ 중에서 임의로 하나를 선택할 때, 이 함수가

$$
f(1) \leq f(2) \leq f(3) \leq f(4)
$$

를 만족시킬 확률은 $\frac{q}{p}$ 이다. $p+q$ 의 값을 구하시오. (단, $p$ 와 $q$ 는 서로소인 자연수이다.) [4점]

\section*{Chapter 2 \\
 확률}
\section*{(12)}
그림과 같이 8 개의 자리에 놓인 8 장의 흰색 카드가 있다.\\
\includegraphics[max width=\textwidth, center]{130484c4-d424-4c79-b60d-37ec25d7d5b3-10_212_795_828_751}

빨간색, 파란색, 검은색을 사용하여 8 개의 자리의 각 카드에 색칠하는 모든 경우 중에서 임의로 선택한 한 경우가 다음 조건을 만족시킬 때, 빨간색을 칠한 카드의 개수가 파란색을 칠한 카드의 개수보다 클 확률은 $\frac{q}{p}$ 이다. $p+q$ 의 값을 구하시오. (단, 각 카드에는 한 가지 색만 칠하고, $p$ 와 $q$ 는 서로소인 자연수이다.)\\
(가) $1 \leq n \leq 4$ 인 자연수 $n$ 에 대하여 $n$ 번째 자리에 놓인 카드에 칠한 색깔과 $9-n$ 번째 자리에 놓인 카드에 칠한 색깔은 서로 다르다.\\
(나) 검은색을 칠한 카드의 개수는 3 이상이다.


\end{document}"""

def extract_problems_from_latex(latex_content):
    """LaTeX에서 문제 추출"""
    body = extract_body(latex_content)
    problems = []
    
    # 섹션 헤더 찾기
    section_pattern = r'\\section\*\{([^}]+)\}'
    sections = list(re.finditer(section_pattern, body))
    
    # 점수 마커 찾기 ([3점] 또는 [4점])
    point_pattern = r'\[([34])점\]'
    point_markers = list(re.finditer(point_pattern, body))
    
    print(f"📊 발견된 섹션: {len(sections)}개")
    print(f"📊 발견된 점수 마커: {len(point_markers)}개")
    
    # 문제 시작 패턴
    problem_start_patterns = [
        r'검은 공',
        r'집합\s+\$X=',
        r'한 개의 주사위',
        r'수직선의 원점',
        r'좌표평면 위의 점',
        r'어느 학급',
        r'그림과 같이',
        r'좌표평면에 점',
    ]
    
    # 문제 번호 추출 (섹션과 점수 마커의 위치 관계로 매칭)
    problem_number_map = {}  # 마커 인덱스 -> 문제 번호
    
    # 섹션별 문제 번호 추출 (문제 번호를 가진 섹션만)
    section_numbers = []
    for section in sections:
        section_pos = section.start()
        section_text = section.group(1).strip()
        problem_num = None
        
        # 숫자만 있는 경우 (예: "03", "05", "06", "09")
        if re.match(r'^\d+$', section_text):
            problem_num = int(section_text)
        # 괄호 안 숫자 (예: "(6)", "(10)", "(12)")
        elif re.match(r'^\(\d+\)$', section_text):
            problem_num = int(re.search(r'\d+', section_text).group())
        
        if problem_num:
            section_numbers.append((section_pos, problem_num))
    
    # 각 점수 마커에 대해 가장 가까운 섹션 번호 매핑
    # 단, 섹션이 마커 이전에 있어야 하고, 다음 섹션이 마커 이후에 있어야 함
    for i, marker in enumerate(point_markers):
        marker_pos = marker.start()
        # 이 마커 이전에 있는 가장 가까운 섹션 찾기
        closest_section = None
        for section_pos, problem_num in section_numbers:
            if section_pos < marker_pos:
                # 다음 섹션이 마커 이후에 있는지 확인
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
        
        # 문제 텍스트 범위
        problem_start = max(prev_marker_pos, marker_pos - 2000)
        problem_end = next_marker_pos
        
        problem_text = body[problem_start:problem_end]
        
        # 문제 시작 패턴 찾기
        actual_start = problem_start
        for pattern in problem_start_patterns:
            match = re.search(pattern, problem_text)
            if match:
                actual_start = problem_start + match.start()
                break
        
        # 문제 본문 추출 (더 넓은 범위)
        search_start = max(prev_marker_pos, marker_pos - 3000)
        question_text = body[search_start:marker_pos]
        
        # 마커 이후 텍스트 (선택지 포함 가능)
        after_marker = body[marker_pos:problem_end]
        
        # 문제 시작 패턴으로 실제 시작점 찾기
        for pattern in problem_start_patterns:
            match = re.search(pattern, question_text)
            if match:
                question_text = question_text[match.start():]
                break
        
        # 이미지 제거
        question_text = re.sub(r'\\includegraphics.*?\{[^}]+\}', '', question_text)
        question_text = re.sub(r'\\begin\{center\}.*?\\end\{center\}', '', question_text, flags=re.DOTALL)
        
        # displayquote는 내용 보존
        displayquote_match = re.search(r'\\begin\{displayquote\}(.*?)\\end\{displayquote\}', question_text, re.DOTALL)
        if displayquote_match:
            quote_content = displayquote_match.group(1)
            question_text = question_text.replace(displayquote_match.group(0), quote_content)
        
        # itemize는 내용 보존
        itemize_match = re.search(r'\\begin\{itemize\}(.*?)\\end\{itemize\}', question_text, re.DOTALL)
        if itemize_match:
            itemize_content = itemize_match.group(1)
            # \item 제거하고 내용만 유지
            itemize_content = re.sub(r'\\item\s*', '', itemize_content)
            question_text = question_text.replace(itemize_match.group(0), itemize_content)
        
        # LaTeX 명령어 정리
        question_text = clean_latex_text(question_text)
        
        # 빈 문제 제거
        if not question_text.strip() or len(question_text.strip()) < 10:
            continue
        
        # 중복 제거 (첫 100자 비교)
        question_key = question_text[:100].strip()
        if question_key in seen_questions:
            continue
        seen_questions.add(question_key)
        
        # 선택지 추출 (마커 이후 제한된 범위에서만)
        options = []
        answer_type = 'short_answer'
        
        # 객관식 패턴 확인 (제한된 범위)
        # 다음 마커나 섹션이 나오기 전까지만 검색
        search_end = next_marker_pos
        # 다음 섹션이 있으면 그것도 고려
        for section in sections:
            if section.start() > marker_pos:
                search_end = min(search_end, section.start())
                break
        
        # "구하시오" 확인 (먼저 확인하여 주관식이면 선택지 추출 생략)
        has_구하시오 = '구하시오' in question_text or '구하시오' in body[marker_pos:min(marker_pos + 300, search_end)]
        
        # 선택지 검색 범위를 더 제한 (600자 이내, "구하시오"가 없을 때만)
        if not has_구하시오:
            options_search_text = body[marker_pos:min(marker_pos + 600, search_end)]
        else:
            options_search_text = ""
        
        # 선택지 패턴 확인 (반드시 (1)부터 시작, "구하시오"가 없을 때만)
        options_pattern = r'\(1\)|（1）'
        has_options_pattern = False
        if options_search_text and not has_구하시오:
            has_options_pattern = re.search(options_pattern, options_search_text)
        
        if has_options_pattern and not has_구하시오:
            # extract_options_generic 사용
            options = extract_options_generic(options_search_text)
            
            # 선택지가 5개 미만이면 수동으로 추출 시도
            if len(options) < 5:
                # (1)부터 (5)까지 직접 추출
                for opt_num in range(1, 6):
                    pattern = rf'\({opt_num}\)\s*([^\(]+?)(?=\([1-5]\)|\\section|$)'
                    match = re.search(pattern, options_search_text, re.DOTALL)
                    if match:
                        opt_text = match.group(1).strip()
                        # \\ 제거
                        opt_text = re.sub(r'\\\\', '', opt_text)
                        opt_text = clean_latex_text(opt_text)
                        if opt_text and opt_text not in options:
                            options.append(opt_text)
            
            # 선택지가 5개 이상이면 객관식
            if len(options) >= 5:
                answer_type = 'multiple_choice'
            elif len(options) > 0:
                # 선택지가 있으면 객관식으로 처리
                answer_type = 'multiple_choice'
        
        # "?" 확인 (객관식 질문 - "?"가 있고 선택지가 있으면 객관식, "구하시오"가 없을 때만)
        if '?' in question_text and question_text.strip().endswith('?') and not has_구하시오:
            if has_options_pattern:
                if len(options) < 5:
                    # 다시 추출 시도
                    options = extract_options_generic(options_search_text)
                if len(options) >= 5:
                    answer_type = 'multiple_choice'
        
        # 주제 감지
        topic = '확률'
        if '경우의 수' in body[max(0, actual_start-500):actual_start+500]:
            topic = '경우의 수'
        
        # 문제 번호 결정
        # 섹션 매핑이 있으면 사용
        if i in problem_number_map:
            problem_num = problem_number_map[i]
        else:
            # 섹션이 없는 문제는 순서대로 번호 매기기
            # 이미 매핑된 문제 번호들을 확인하여 다음 번호 결정
            used_numbers = set(problem_number_map.values())
            # 문제 순서: 03, (6), 05, 06, 07, 08, 09, (10), 11, (12)
            # 섹션이 없는 문제는 07, 08, 11
            # 이전 문제들의 번호를 확인하여 다음 번호 결정
            prev_numbers = [problem_number_map.get(j) for j in range(i) if j in problem_number_map]
            if prev_numbers:
                max_prev = max(prev_numbers)
                # 다음 번호 후보: 07, 08, 11
                candidates = [7, 8, 11]
                problem_num = None
                for cand in candidates:
                    if cand > max_prev and cand not in used_numbers:
                        problem_num = cand
                        break
                if problem_num is None:
                    # 후보가 없으면 순서대로
                    problem_num = max_prev + 1
            else:
                problem_num = 7  # 첫 번째 섹션 없는 문제는 07
        
        problem = {
            'index': f"{problem_num:02d}",
            'page': (i // 2) + 1,
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
    print("확통_2024학년도_현우진_드릴_P4_문제 변환")
    print("=" * 80)
    
    # 문제 추출
    problems = extract_problems_from_latex(latex_content)
    
    print(f"\n📊 총 {len(problems)}개 문제 추출 완료\n")
    
    # 검토
    is_valid = review_problems(problems)
    
    # 저장
    base_dir = Path(r'C:\Users\a\Documents\MathPDF\organized\현우진\확통_2005학년도_현우진_드릴')
    base_filename = '확통_2024학년도_현우진_드릴_P4_문제'
    
    if is_valid or len(problems) > 0:
        save_for_deepseek(problems, base_dir, base_filename)
        print(f"\n✅ 저장 완료: {base_dir}")
    else:
        print("\n❌ 검토 실패")

if __name__ == '__main__':
    main()
