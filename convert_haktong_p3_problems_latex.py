# convert_haktong_p3_problems_latex.py
# 확통_2024학년도_현우진_드릴_P3_문제 LaTeX 변환

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
\section*{18}
20 이하의 자연수 중에서 서로 다른 4 개의 수를 선택하여 작은 수부터 크기순으로 나열한 것을 $a, b, c, d$ 라 하자. 다음 조건을 만족시키는 모든 순서쌍 $(a, b, c, d)$ 의 개수를 구하시오. [4점]\\
$a, b, c, d$ 중에서 선택한 서로 다른 2 개의 수의 차의 최댓값은 15 이고 최솟값은 2 이다.

\section*{Chapter 1 \\
 경우의 수}
1 부터 11 까지의 자연수 중에서 4 개의 자연수 $a_{1}, a_{2}, a_{3}, a_{4}$ 를 다음 조건을 만족시키도록 선택하는 경우의 수를 구하시오. [4점]\\
(가) $a_{1}<a_{2}<a_{3}<a_{4}$\\
(나) $a_{n+1}-a_{n} \geq 2$ 를 만족시키는 3 이하의 자연수 $n$ 의 개수는 2 이다.\\
(다) $a_{1}+a_{4}$ 는 짝수이다.

\section*{Chapter 1 \\
 경우의 수}
집합 $X=\{1,2,3,4\}$ 에서 집합 $Y=\{3,4,5\}$ 로의 함수 $f$ 중에서

$$
\sum_{k=1}^{4} f(k) \geq 15
$$

를 만족시키는 함수 $f$ 의 개수를 구하시오. [4점]

\section*{Chapter 1 경우의 수}
\begin{center}
\includegraphics[max width=\textwidth]{2a0a8861-8d0c-4060-889a-05d4fcb7d009-4_248_265_551_157}
\end{center}

집합 $X=\{1,2,3,4,5,6\}$ 에 대하여 다음 조건을 만족시키는 함수 $f: X \rightarrow X$ 의 개수를 구하시오.\\[0pt]
[4점]\\
(가) $f(3)=5$\\
(나) 집합 $X$ 의 원소 $x$ 에 대하여\\
$x$ 가 홀수이면 $f(x) \leq f(x+1)$ 이고,\\
$x$ 가 짝수이면 $f(x) \geq f\left(\frac{x}{2}\right)$ 이다.\\
\includegraphics[max width=\textwidth, center]{2a0a8861-8d0c-4060-889a-05d4fcb7d009-5_246_257_551_176}

집합 $X=\{1,2,3,4,5\}$ 에 대하여 다음 조건을 만족시키는 $X$ 에서 $X$ 로의 함수 $f$ 의 개수를 구하시오.\\[0pt]
[4점]

\begin{displayquote}
(가) 함수 $f$ 의 치역의 원소의 개수는 3 이상이다.\\
(나) 함수 $f$ 의 치역의 모든 원소의 합은 4 의 배수이다.
\end{displayquote}

\section*{Chapter 1 \\
 경우의 수}
\section*{23}
다항식 $\left(2 x^{2}-\sqrt[3]{2} x\right)^{6}$ 의 전개식에서 계수가 유리수인 모든 항의 계수의 합은? [3점]\\
(1) -252\\
(2) -246\\
(3) -240\\
(4) -234\\
(5) -228

\section*{(20)}
0 부터 9 까지의 정수 중에서 중복을 허락하여 3 개를 택해 일렬로 나열하여 세 자리의 자연수를 만들 때, 각 자리의 수의 합이 $n$ 인 세 자리의 자연수의 개수를 $f(n)$ 이라 하자.\\
예를 들어 각 자리의 수의 합이 3 인 세 자리의 자연수는 $300,210,201,120,102,111$ 이므로 $f(3)=6$ 이다.\\
$\sum_{n=1}^{11} f(n)$ 의 값을 구하시오. [4점]

\section*{Chapter 2}
\section*{확률}
\section*{(11)}
1 부터 6 까지의 자연수가 하나씩 적혀 있는 6 장의 카드가 있다. 이 6 장의 카드를 모두 한 번씩 사용하여 일렬로 임의로 나열할 때, 양 끝의 카드에 적힌 두 수의 곱이 6 의 배수가 아닐 확률은? [3점]\\
(1) $\frac{4}{15}$\\
(2) $\frac{1}{3}$\\
(3) $\frac{2}{5}$\\
(4) $\frac{7}{15}$\\
(5) $\frac{8}{15}$

\section*{Chapter 2 \\
 확률}
\section*{(12)}
숫자 $1,1,1,2,3,4$ 가 하나씩 적혀 있는 6 개의 공이 들어 있는 주머니가 있다. 학생 A가 먼저 이 주머니에 들어 있는 6 개의 공 중에서 임의로 3 개의 공을 동시에 꺼내고, 학생 B 가 이 주머니에 남아 있는 3 개의 공 중에서 임의로 1 개의 공을 꺼낼 때, 학생 A 가 꺼낸 공에 적혀 있는 수의 합 $a$ 와 학생 B 가 꺼낸 공에 적혀 있는 수 $b$ 에 대하여 $a \times b$ 가 짝수일 확률은? [3점]\\
(1) $\frac{3}{5}$\\
(2) $\frac{2}{3}$\\
(3) $\frac{11}{15}$\\
(4) $\frac{4}{5}$\\
(5) $\frac{13}{15}$


\end{document}"""

def extract_problems_from_latex(latex_content):
    """LaTeX에서 문제 추출"""
    body = extract_body(latex_content)
    problems = []
    
    # 섹션 헤더 찾기
    section_pattern = r'\\section\*\{([^}]+)\}'
    sections = list(re.finditer(section_pattern, body))
    
    # 점수 마커 찾기
    point_pattern = r'\[([34])점\]'
    point_markers = list(re.finditer(point_pattern, body))
    
    print(f"📊 발견된 섹션: {len(sections)}개")
    print(f"📊 발견된 점수 마커: {len(point_markers)}개")
    
    # 문제 시작 패턴
    problem_start_patterns = [
        r'\d+\s+이하의 자연수',
        r'\d+\s+부터\s+\d+\s+까지',
        r'집합\s+\$X=',
        r'다항식\s+\$',
        r'\d+\s+부터\s+\d+\s+까지의 정수',
        r'\d+\s+부터\s+\d+\s+까지의 자연수',
        r'숫자\s+\$',
    ]
    
    # 문제 번호 추출 (섹션과 점수 마커의 위치 관계로 매칭)
    problem_number_map = {}  # 마커 인덱스 -> 문제 번호
    
    for section in sections:
        section_pos = section.start()
        section_text = section.group(1).strip()
        problem_num = None
        
        # 숫자만 있는 경우 (예: "18", "23")
        if re.match(r'^\d+$', section_text):
            problem_num = int(section_text)
        # 괄호 안 숫자 (예: "(20)", "(11)", "(12)")
        elif re.match(r'^\(\d+\)$', section_text):
            problem_num = int(re.search(r'\d+', section_text).group())
        
        if problem_num:
            # 이 섹션 다음에 오는 첫 번째 점수 마커 찾기
            for i, marker in enumerate(point_markers):
                if marker.start() > section_pos:
                    if i not in problem_number_map:
                        problem_number_map[i] = problem_num
                    break
    
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
        
        # 선택지 추출 (마커 이후 전체 범위에서)
        options = []
        answer_type = 'short_answer'
        
        # 객관식 패턴 확인 (더 넓은 범위)
        if i < len(point_markers) - 1:
            # 다음 마커까지 확장
            next_marker_start = point_markers[i+1].start()
            options_search_text = body[marker_pos:min(marker_pos + 2000, next_marker_start)]
        else:
            # 마지막 문제인 경우 더 넓게 검색
            options_search_text = body[marker_pos:min(marker_pos + 2000, len(body))]
        
        # 선택지 패턴 확인 (반드시 (1)부터 시작)
        # \\로 구분된 선택지도 처리
        options_pattern = r'\(1\)|（1）'
        if re.search(options_pattern, options_search_text):
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
            
            if len(options) >= 5:
                answer_type = 'multiple_choice'
            elif len(options) > 0:
                # 선택지가 있으면 객관식으로 처리
                answer_type = 'multiple_choice'
        
        # "?" 확인 (객관식 질문 - "?"가 있고 선택지가 있으면 객관식)
        if '?' in question_text:
            if re.search(options_pattern, options_search_text):
                if len(options) < 5:
                    # 다시 추출 시도
                    options = extract_options_generic(options_search_text)
                if len(options) >= 5:
                    answer_type = 'multiple_choice'
        
        # "구하시오" 확인 (주관식)
        if '구하시오' in question_text or '구하시오' in after_marker:
            if len(options) < 5:
                answer_type = 'short_answer'
        
        # 주제 감지
        topic = '경우의 수'
        if '확률' in body[max(0, actual_start-500):actual_start+500]:
            topic = '확률'
        elif '다항식' in question_text or '전개식' in question_text:
            topic = '경우의 수'  # 이항정리 관련
        
        # 문제 번호 결정
        problem_num = i + 1
        if i in problem_number_map:
            problem_num = problem_number_map[i]
        
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
    print("확통_2024학년도_현우진_드릴_P3_문제 변환")
    print("=" * 80)
    
    # 문제 추출
    problems = extract_problems_from_latex(latex_content)
    
    print(f"\n📊 총 {len(problems)}개 문제 추출 완료\n")
    
    # 검토
    is_valid = review_problems(problems)
    
    # 저장
    base_dir = Path(r'C:\Users\a\Documents\MathPDF\organized\현우진\확통_2005학년도_현우진_드릴')
    base_filename = '확통_2024학년도_현우진_드릴_P3_문제'
    
    if is_valid or len(problems) > 0:
        save_for_deepseek(problems, base_dir, base_filename)
        print(f"\n✅ 저장 완료: {base_dir}")
    else:
        print("\n❌ 검토 실패")

if __name__ == '__main__':
    main()
