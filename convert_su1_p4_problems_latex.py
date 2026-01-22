# convert_su1_p4_problems_latex.py
# 수1 드릴 P4 문제 LaTeX를 딥시크용 CSV로 변환
# 개선: latex_utils와 convert_template 활용으로 더 빠르고 안정적인 처리

import re
import csv
import sys
import os
from pathlib import Path
from datetime import datetime
import json
from latex_utils import (
    extract_body, extract_options_generic, clean_latex_text,
    diagnose_latex_structure
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
$n \\geq 2$ 인 자연수 $n$ 에 대하여 열린구간 $\\left(0, \\frac{\\pi}{2}\\right)$ 에서 $x$ 에 대한 방정식

$$
\\tan x+\\tan n x=0
$$

의 실근의 개수를 $f(n)$ ，모든 실근의 합을 $g(n)$ 이라 하자．〈보기〉에서 옳은 것만을 있는 대로 고른 것은？\\\\
［4점］\\\\
〈보기〉\\\\
ㄱ．모든 자연수 $p$ 에 대하여 $\\tan x+\\tan (p \\pi-x)=0$ 이다．\\\\
ㄴ．모든 자연수 $q$ 에 대하여 $f(2 q)+f(2 q+1)=2 q$ 이다．\\\\
ㄷ．$\\sum_{k=1}^{15} g(2 k+1)=30 \\pi$\\\\
（1）ᄀ\\\\
（2）ㄱ，ㄴ\\\\
（3）ㄱ，ㄷ\\\\
（4）ᄂ，ᄃ\\\\
（5）ᄀ，ᄂ，ᄃ

\\section*{Chapter 2 \\\\
 삼각함수}
$\\overline{\\mathrm{AB}}=6, \\overline{\\mathrm{AC}}=5$ 인 삼각형 ABC 에 대하여

$$
\\sin A=2 \\sqrt{2} \\cos (B+C)
$$

일 때, 삼각형 ABC 에 내접하는 원의 넓이는 $k \\pi$ 이다. 자연수 $k$ 의 값을 구하시오. [4점]

그림과 같이 반지름의 길이가 1 이고 중심각의 크기가 $\\frac{\\pi}{2}$ 인 부채꼴 OAB 가 있다.\\\\
호 AB 위의 점 P 에 대하여

$$
\\sin (\\angle \\mathrm{PAB})=3 \\sqrt{2} \\sin (\\angle \\mathrm{PBA})
$$

일 때, 삼각형 APB 의 넓이는? [4점]\\\\
\\includegraphics[max width=\\textwidth, center]{83279859-6848-49c9-a8bd-606f19038d81-03_397_424_987_974}\\\\
(1) $\\frac{2}{25}$\\\\
(2) $\\frac{1}{10}$\\\\
(3) $\\frac{3}{25}$\\\\
(4) $\\frac{7}{50}$\\\\
(5) $\\frac{4}{25}$

\\section*{Chapter 2 삼각함수}
서로 다른 두 점 $\\mathrm{A}, \\mathrm{B}$ 에서 만나는 두 원 $C_{1}, C_{2}$ 의 반지름의 길이가 각각 $\\frac{2 \\sqrt{3}}{3}, \\sqrt{3}$ 이다. 원 $C_{2}$ 의 내부에 있고 원 $C_{1}$ 위에 있는 점 C 에 대하여 직선 AC 가 원 $C_{2}$ 와 만나는 점 중 A 가 아닌 점을 D 라 하자.\\\\
$\\overline{\\mathrm{BC}}=2, \\angle \\mathrm{CAB}=\\angle \\mathrm{CBD}$ 일 때, 삼각형 ABD 의 넓이는 $\\frac{q}{p} \\sqrt{3}$ 이다. $p+q$ 의 값을 구하시오.\\\\
(단, $p$ 와 $q$ 는 서로소인 자연수이다.) [4점]\\\\
\\includegraphics[max width=\\textwidth, center]{83279859-6848-49c9-a8bd-606f19038d81-04_466_599_1032_886}

그림과 같이 한 원 위에 있는 네 점 $\\mathrm{A}, \\mathrm{B}, \\mathrm{C}, \\mathrm{D}$ 에 대하여 $\\overline{\\mathrm{AD}}=6, \\overline{\\mathrm{BD}}=5, \\overline{\\mathrm{CD}}=4$ 이다. 삼각형 ADB 의 넓이가 삼각형 BDC 의 넓이의 3 배일 때, $\\overline{\\mathrm{AB}}+\\overline{\\mathrm{BC}}$ 의 값은? [4점]\\\\
\\includegraphics[max width=\\textwidth, center]{83279859-6848-49c9-a8bd-606f19038d81-05_447_445_831_968}\\\\
(1) $\\frac{9 \\sqrt{7}}{7}$\\\\
(2) $\\frac{10 \\sqrt{7}}{7}$\\\\
(3) $\\frac{11 \\sqrt{7}}{7}$\\\\
(4) $\\frac{12 \\sqrt{7}}{7}$\\\\
(5) $\\frac{13 \\sqrt{7}}{7}$

그림과 같이 $\\angle \\mathrm{CAB}>\\frac{\\pi}{2}$ 인 삼각형 ABC 의 변 BC 와 정사각형 ABDE 의 변 AE 가 E 가 아닌 점 F 에서 만난다. 세 삼각형 $\\mathrm{ABF}, \\mathrm{BDF}, \\mathrm{CFE}$ 의 외접원의 넓이를 각각 $S_{1}, S_{2}, S_{3}$ 이라 하자.

$$
S_{1}: S_{2}: S_{3}=16: 17: 1, \\quad \\overline{\\mathrm{CF}}=2
$$

일 때, 선분 AC 의 길이는 $l$ 이다. $l^{2}$ 의 값을 구하시오. [4점]\\\\
\\includegraphics[max width=\\textwidth, center]{83279859-6848-49c9-a8bd-606f19038d81-06_502_540_998_909}

그림과 같이 $\\angle \\mathrm{BAC}<\\frac{\\pi}{2}$ 인 삼각형 ABC 에서 선분 AB 의 중점을 D 라 하고, 선분 AD 를 지름으로 하는 원이 선분 AC 와 만나는 점 중 A 가 아닌 점을 E 라 하자.

$$
\\overline{\\mathrm{AB}}=\\overline{\\mathrm{CE}}, \\quad \\overline{\\mathrm{BC}}^{2}=8 \\overline{\\mathrm{DE}}^{2}
$$

이고, 삼각형 ABC 의 외접원의 넓이가 $18 \\pi$ 일 때, 선분 AC 의 길이는 $\\frac{q}{p}$ 이다. $p+q$ 의 값을 구하시오.\\\\
(단, $p$ 와 $q$ 는 서로소인 자연수이다.) [4점]\\\\
\\includegraphics[max width=\\textwidth, center]{83279859-6848-49c9-a8bd-606f19038d81-07_418_436_1082_960}

그림과 같이 선분 AB 를 지름으로 하는 반원의 호 AB 위의 세 점 $\\mathrm{P}, \\mathrm{Q}, \\mathrm{R}$ 이

$$
\\overline{\\mathrm{PQ}}=\\overline{\\mathrm{QR}}=\\sqrt{6}, \\quad \\overline{\\mathrm{PR}}=2 \\sqrt{5}
$$

를 만족시킨다. 삼각형 PAQ 의 넓이가 $\\frac{\\sqrt{5}}{2}$ 일 때, $\\overline{\\mathrm{BQ}}^{2}-\\overline{\\mathrm{AP}}^{2}$ 의 값을 구하시오. (단, $\\overline{\\mathrm{AP}}<\\overline{\\mathrm{AQ}}$ ) [4점]\\\\
\\includegraphics[max width=\\textwidth, center]{83279859-6848-49c9-a8bd-606f19038d81-08_359_669_938_850}\\\\
$\\angle \\mathrm{ABC}>\\frac{\\pi}{2}, \\overline{\\mathrm{AB}}=2, \\overline{\\mathrm{BC}}=3$ 인 삼각형 ABC 에 대하여 선분 BC 를 $1: 2$ 로 내분하는 점을 D , 삼각형 ABD 의 외접원 $C$ 가 선분 AC 와 만나는 점 중 A 가 아닌 점을 E 라 하자. $\\overline{\\mathrm{DE}}=1$ 일 때, 원 $C$ 의 넓이는 $k \\pi$ 이다. 유리수 $k$ 에 대하여 $30 k$ 의 값을 구하시오. [4점]\\\\
\\includegraphics[max width=\\textwidth, center]{83279859-6848-49c9-a8bd-606f19038d81-09_428_633_922_869}\\\\
$\\overline{\\mathrm{AB}}=6$ 인 예각삼각형 ABC 가 있다. 선분 BC 를 $3: 2$ 로 내분하는 점을 D 라 하고, 선분 BD 를 지름으로 하는 원 $C_{1}$ 이 선분 AB 와 만나는 점 중 B 가 아닌 점을 E , 선분 CD 를 지름으로 하는 원 $C_{2}$ 가 선분 AC 와 만나는 점 중 C 가 아닌 점을 F 라 하자.

$$
\\overline{\\mathrm{DE}}=\\overline{\\mathrm{DF}}, \\quad \\cos (\\angle \\mathrm{EDF})=-\\frac{9}{16}
$$

일 때, 두 원 $C_{1}, C_{2}$ 의 넓이의 합은 $\\frac{q}{p} \\pi$ 이다. $p+q$ 의 값을 구하시오.\\\\
(단, $p$ 와 $q$ 는 서로소인 자연수이다. ) [4점]\\\\
\\includegraphics[max width=\\textwidth, center]{83279859-6848-49c9-a8bd-606f19038d81-10_424_659_1163_858}

삼각형 ABC 에서 $\\angle \\mathrm{BAC}$ 를 이등분하는 직선이 선분 BC 와 만나는 점을 D 라 하고, 삼각형 ABD 의 외접원이 선분 AC 와 만나는 점 중 A 가 아닌 점을 E , 점 D 에서 선분 AC 에 내린 수선의 발을 H 라 하자.\\\\
$\\overline{\\mathrm{BD}}: \\overline{\\mathrm{DC}}=1: 2, \\overline{\\mathrm{AB}}: \\overline{\\mathrm{EC}}=4: 5, \\overline{\\mathrm{EH}}=\\frac{1}{2}$\\\\
일 때, $\\overline{\\mathrm{BE}}^{2}$ 의 값은? (단, $\\angle \\mathrm{ABC}<\\frac{\\pi}{2}$ ) [4점]\\\\
(1) $\\frac{33}{2}$\\\\
(2) 17\\\\
(3) $\\frac{35}{2}$\\\\
(4) 18\\\\
(5) $\\frac{37}{2}$\\\\
\\includegraphics[max width=\\textwidth, center]{83279859-6848-49c9-a8bd-606f19038d81-11_386_716_1167_832}


\\end{document}"""

def extract_problems_from_latex(latex_content):
    """LaTeX에서 문제 추출"""
    problems = []
    
    # 본문만 추출
    begin_match = re.search(r'\\begin\{document\}', latex_content)
    end_match = re.search(r'\\end\{document\}', latex_content)
    if begin_match and end_match:
        body = latex_content[begin_match.end():end_match.start()]
    else:
        body = latex_content
    
    # 점수 마커로 문제 구분
    point_markers = list(re.finditer(r'\[4점\]|［4점］', body))
    print(f"[디버깅] [4점] 마커 발견: {len(point_markers)}개")
    
    # 각 점수 마커 주변에서 문제 추출
    for i, marker in enumerate(point_markers, 1):
        start_pos = max(0, marker.start() - 1000)  # 앞으로 1000자
        end_pos = min(len(body), marker.end() + 500)  # 뒤로 500자
        
        # 문제 시작 찾기
        problem_start = start_pos
        for j in range(marker.start(), max(0, marker.start() - 1000), -1):
            if j > 0:
                # 이전 문제의 끝이나 섹션 시작 찾기
                if body[j-1] == '\n' and (
                    body[j:j+10].startswith('$') or 
                    body[j:j+20].find('그림') != -1 or
                    body[j:j+30].find('서로') != -1 or
                    body[j:j+30].find('삼각형') != -1 or
                    body[j:j+30].find('선분') != -1
                ):
                    problem_start = j
                    break
                # 이전 문제의 [4점] 찾기
                if j > 50:
                    prev_marker = body.rfind('[4점]', max(0, j-500), j)
                    if prev_marker == -1:
                        prev_marker = body.rfind('［4점］', max(0, j-500), j)
                    if prev_marker != -1:
                        problem_start = prev_marker + 100
                        break
        
        # 문제 끝 찾기
        problem_end = marker.end() + 300
        next_section = body.find('\\section', marker.end())
        if next_section != -1:
            problem_end = min(problem_end, next_section)
        next_problem = body.find('[4점]', marker.end() + 50)
        if next_problem == -1:
            next_problem = body.find('［4점］', marker.end() + 50)
        if next_problem != -1:
            problem_end = min(problem_end, next_problem - 50)
        
        problem_text = body[problem_start:problem_end]
        
        # 선택지 확인 (보기 문제 포함)
        has_options = bool(re.search(r'\([1-5]\)|①|②|③|④|⑤|ㄱ|ㄴ|ㄷ|（[1-5]）', problem_text))
        
        # 문제 본문 추출
        question_end = problem_text.find('[4점]')
        if question_end == -1:
            question_end = problem_text.find('［4점］')
        if question_end != -1:
            question = problem_text[:question_end].strip()
            options_text = problem_text[question_end:] if has_options else ""
        else:
            question = problem_text.strip()
            options_text = ""
        
        # 문제 3번은 객관식이므로 선택지가 있어야 함 - 강제 설정
        if i == 3 and ('삼각형 APB' in question or '부채꼴' in question):
            has_options = True
            if not options_text or len(options_text) < 50:
                # options_text 재확인
                problem_03_full = body[max(0, marker.start()-800):marker.end()+500]
                question_end_03 = problem_03_full.find('[4점]')
                if question_end_03 != -1:
                    options_text = problem_03_full[question_end_03:]
        
        # 텍스트 정리 (latex_utils 활용)
        question = clean_latex_text(question)
        
        # 문제 시작 부분이 너무 짧으면 확장
        if len(question) < 50:
            extended_start = max(0, problem_start - 300)
            extended_text = body[extended_start:problem_end]
            question_end_ext = extended_text.find('[4점]')
            if question_end_ext == -1:
                question_end_ext = extended_text.find('［4점］')
            if question_end_ext != -1:
                question = clean_latex_text(extended_text[:question_end_ext])
                options_text = extended_text[question_end_ext:] if has_options else ""
        
        if len(question) < 30:
            continue
        
        # 선택지 추출
        options = []
        if has_options and options_text:
            # 보기 문제 (ㄱ, ㄴ, ㄷ)
            if 'ㄱ' in options_text or 'ㄴ' in options_text or 'ㄷ' in options_text:
                # 보기 내용 추출
                boogi_match = re.search(r'〈보기〉(.*?)(?=（[1-5]）|$)', options_text, re.DOTALL)
                if boogi_match:
                    boogi_content = boogi_match.group(1).strip()
                    boogi_content = re.sub(r'\\\\', ' ', boogi_content)
                    boogi_content = re.sub(r'\s+', ' ', boogi_content)
                    options.append(f"〈보기〉 {boogi_content}")
                
                # 선택지 추출
                for opt_num in range(1, 6):
                    pattern = rf'（{opt_num}）\s*([^（]+?)(?=（[1-5]）|$)'
                    match = re.search(pattern, options_text)
                    if match:
                        option_num = ["①", "②", "③", "④", "⑤"][opt_num-1]
                        opt_text = match.group(1).strip()
                        opt_text = re.sub(r'\\\\', ' ', opt_text)
                        opt_text = re.sub(r'\s+', ' ', opt_text)
                        options.append(f"{option_num} {opt_text}")
            else:
                # 일반 객관식 문제
                # body에서는 백슬래시가 그대로 있으므로 \\$ 형태
                for opt_num in range(1, 6):
                    patterns = [
                        rf'\({opt_num}\)\s*\\\$\\frac{{([0-9]+)}}\{{([0-9]+)}}\\\$',
                        rf'\({opt_num}\)\s*\\\$([0-9]+) \\sqrt{{([0-9]+)}}\\\$',
                        rf'\({opt_num}\)\s*\\\$\\frac{{([0-9]+) \\sqrt{{([0-9]+)}}}}\{{([0-9]+)}}\\\$',
                        rf'\({opt_num}\)\s*\\\$([0-9]+)\\\$',
                        rf'\({opt_num}\)\s*([0-9]+)(?=\\\\\\\\)',
                        rf'\({opt_num}\)\s*([0-9]+)(?=\\\\|\s|$)',
                    ]
                    match = None
                    for pattern in patterns:
                        match = re.search(pattern, options_text)
                        if match:
                            break
                    
                    if match:
                        option_num = ["①", "②", "③", "④", "⑤"][opt_num-1]
                        if len(match.groups()) == 2 and match.group(1).isdigit() and match.group(2).isdigit():
                            opt_text = f"\\frac{{{match.group(1)}}}{{{match.group(2)}}}"
                            options.append(f"{option_num} ${opt_text}$")
                        elif len(match.groups()) == 1 and match.group(1).isdigit():
                            if 'sqrt' in pattern:
                                opt_text = f"\\sqrt{{{match.group(1)}}}"
                                options.append(f"{option_num} ${opt_text}$")
                            else:
                                options.append(f"{option_num} {match.group(1)}")
                        elif len(match.groups()) == 2:
                            opt_text = f"{match.group(1)} \\sqrt{{{match.group(2)}}}"
                            options.append(f"{option_num} ${opt_text}$")
                        elif len(match.groups()) == 3:
                            opt_text = f"\\frac{{{match.group(1)} \\sqrt{{{match.group(2)}}}}}{{{match.group(3)}}}"
                            options.append(f"{option_num} ${opt_text}$")
        
        # 문제 3번은 객관식인데 선택지가 누락될 수 있음 - 특별 처리
        if i == 3 and len(options) < 5:
            # 문제 3번 재추출 시도
            problem_03_text = body[max(0, marker.start()-800):marker.end()+500]
            if '삼각형 APB' in problem_03_text or '부채꼴' in problem_03_text:
                # 선택지 재추출 - body에서는 $ 형태 (백슬래시 없음)
                options_03 = []
                for opt_num in range(1, 6):
                    # body에서는 $ 형태 (백슬래시 없음)
                    # LaTeX: (1) $\frac{2}{25}$\\
                    # 실제 body에서는 $ 형태로 나타남
                    patterns = [
                        rf'\({opt_num}\)\s*\$\$?frac{{([0-9]+)}}\{{([0-9]+)}}\$',  # $ 형태
                        rf'\({opt_num}\)\s*\$\$?frac{{([0-9]+)}}\{{([0-9]+)}}\\\$',  # $ 형태 + \\$
                        rf'\({opt_num}\)\s*\$\$?frac{{([0-9]+)}}\{{([0-9]+)}}\\\\',  # $ 형태 + \\\\ (줄바꿈)
                        rf'\({opt_num}\)\s*\\\$\\frac{{([0-9]+)}}\{{([0-9]+)}}\\\$',  # \\$ 형태
                    ]
                    match = None
                    for pattern in patterns:
                        match = re.search(pattern, problem_03_text)
                        if match:
                            break
                    if not match:
                        # 더 간단한 패턴 시도: (1) $...$ 형태
                        simple_pattern = rf'\({opt_num}\)\s*\$([^$]+)\$'
                        match = re.search(simple_pattern, problem_03_text)
                    if match:
                        option_num = ["①", "②", "③", "④", "⑤"][opt_num-1]
                        if len(match.groups()) == 2 and match.group(1).isdigit() and match.group(2).isdigit():
                            opt_text = f"\\frac{{{match.group(1)}}}{{{match.group(2)}}}"
                            options_03.append(f"{option_num} ${opt_text}$")
                        elif len(match.groups()) == 1:
                            # 간단한 패턴으로 매칭된 경우
                            opt_content = match.group(1).strip()
                            if 'frac' in opt_content:
                                # frac 추출
                                frac_match = re.search(r'frac\{([0-9]+)\}\{([0-9]+)\}', opt_content)
                                if frac_match:
                                    opt_text = f"\\frac{{{frac_match.group(1)}}}{{{frac_match.group(2)}}}"
                                    options_03.append(f"{option_num} ${opt_text}$")
                            else:
                                options_03.append(f"{option_num} ${opt_content}$")
                        else:
                            opt_text = f"\\frac{{{match.group(1)}}}{{{match.group(2)}}}"
                            options_03.append(f"{option_num} ${opt_text}$")
                if len(options_03) == 5:
                    options = options_03
                    has_options = True
                    print(f"[디버깅] 문제 3번 선택지 재추출 성공: {len(options)}개")
                elif len(options_03) > 0:
                    # 일부만 추출된 경우도 사용
                    options = options_03
                    has_options = True
                    print(f"[디버깅] 문제 3번 선택지 부분 추출: {len(options)}개")
                else:
                    # 디버깅: 문제 3번 텍스트 일부 출력
                    print(f"[디버깅] 문제 3번 선택지 추출 실패, 텍스트 일부: {problem_03_text[-400:]}")
        
        # 문제 추가
        # 보기 문제는 선택지가 6개 이상일 수 있음 (보기 내용 포함)
        # 일반 객관식은 5개 선택지
        if len(options) >= 5:
            # 보기 문제인지 확인
            is_boogi = any('보기' in opt or 'ㄱ' in opt or 'ㄴ' in opt or 'ㄷ' in opt for opt in options)
            if is_boogi or len(options) >= 6:
                # 보기 문제는 선택지 수가 6개 이상일 수 있음
                problems.append({
                    "index": f"{i:02d}",
                    "page": (i // 2) + 1,
                    "topic": "삼각함수",
                    "question": question,
                    "point": 4,
                    "answer_type": "multiple_choice",
                    "options": options
                })
            elif len(options) == 5:
                # 일반 객관식
                problems.append({
                    "index": f"{i:02d}",
                    "page": (i // 2) + 1,
                    "topic": "삼각함수",
                    "question": question,
                    "point": 4,
                    "answer_type": "multiple_choice",
                    "options": options
                })
        elif len(question) > 50:
            problems.append({
                "index": f"{i:02d}",
                "page": (i // 2) + 1,
                "topic": "삼각함수",
                "question": question,
                "point": 4,
                "answer_type": "short_answer"
            })
    
    return problems

def review_problems_legacy(problems):
    """문제 데이터 검토"""
    print("=" * 60)
    print("[수1 드릴 P4 문제 데이터 검토]")
    print("=" * 60)
    
    issues = []
    
    for prob in problems:
        idx = prob.get("index", "?")
        print(f"\n[문제 {idx}]")
        
        question = prob.get("question", "")
        # $$ 블록은 짝수 개의 $로 계산해야 함
        dollar_count = question.count('$')
        # $$ 블록 제거 후 계산
        question_no_dblock = re.sub(r'\$\$', '', question)
        dollar_count_single = question_no_dblock.count('$')
        
        if dollar_count_single % 2 != 0:
            issues.append(f"문제 {idx}: LaTeX 수식 괄호 불일치")
            print("[LaTeX] 오류: 수식 괄호 불일치")
        else:
            print("[LaTeX] 정상")
        
        print(f"[내용 길이] {len(question)}자")
        
        answer_type = prob.get("answer_type", "")
        print(f"[유형] {answer_type}")
        
        if answer_type == "multiple_choice":
            options = prob.get("options", [])
            print(f"[선택지 수] {len(options)}개")
            if len(options) >= 5:
                print("[선택지] 정상")
            else:
                issues.append(f"문제 {idx}: 선택지 수 오류 ({len(options)}개)")
                print(f"[선택지] 오류: {len(options)}개 (5개 이상이어야 함)")
    
    print("\n" + "=" * 60)
    print("[검토 결과]")
    print("=" * 60)
    print(f"[총 문제수] {len(problems)}개")
    
    mc_count = sum(1 for p in problems if p.get("answer_type") == "multiple_choice")
    sa_count = sum(1 for p in problems if p.get("answer_type") == "short_answer")
    print(f"[객관식] {mc_count}개")
    print(f"[주관식] {sa_count}개")
    
    if issues:
        print("\n[오류]")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("\n[오류] 없음")
    
    return len(issues) == 0

def save_for_deepseek_legacy(problems):
    """딥시크용 CSV 저장 (레거시 버전)"""
    base_dir = Path(r'C:\Users\a\Documents\MathPDF\organized\현우진\수1_2025학년도_현우진_드릴')
    base_filename = "수1_2025학년도_현우진_드릴_P4_문제"
    return save_for_deepseek(problems, base_dir, base_filename)

def main():
    print("=" * 60)
    print("[수1 드릴 P4 문제 LaTeX → CSV 변환]")
    print("=" * 60)
    
    # 1단계: LaTeX 읽기
    print(f"\n[1단계] LaTeX 내용 읽기 완료 ({len(latex_content)}자)")
    
    # 2단계: 문제 추출
    print("\n[2단계] 문제 추출 중...")
    problems = extract_problems_from_latex(latex_content)
    print(f"[완료] {len(problems)}개 문제 추출됨")
    
    # 3단계: 검토 (convert_template 활용)
    print("\n[3단계] 문제 검토 중...")
    is_valid = review_problems(problems)
    
    # 4단계: 저장 (convert_template 활용)
    print("\n[4단계] 딥시크용 파일 저장 중...")
    base_dir = Path(r'C:\Users\a\Documents\MathPDF\organized\현우진\수1_2025학년도_현우진_드릴')
    base_filename = "수1_2025학년도_현우진_드릴_P4_문제"
    csv_path, json_path = save_for_deepseek(problems, base_dir, base_filename)
    
    print("\n" + "=" * 60)
    print("[완료] 딥시크가 읽을 수 있는 형태로 저장되었습니다.")
    print("=" * 60)
    base_dir = Path(r'C:\Users\a\Documents\MathPDF\organized\현우진\수1_2025학년도_현우진_드릴')
    print(f"저장 위치: {base_dir}")
    print(f"  - CSV: {csv_path.name}")
    print(f"  - JSON: {json_path.name}")

if __name__ == '__main__':
    main()
