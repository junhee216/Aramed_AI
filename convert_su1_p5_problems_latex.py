# convert_su1_p5_problems_latex.py
# 수1 드릴 P5 문제 LaTeX를 딥시크용 CSV로 변환

import re
import sys
import os
from pathlib import Path
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
길이가 3 인 선분 $\\mathrm{O}_{1} \\mathrm{O}_{2}$ 에 대하여 점 $\\mathrm{O}_{1}$ 을 중심으로 하고 반지름의 길이가 2 인 원 $C_{1}$ 과 점 $\\mathrm{O}_{2}$ 를 중심으로 하고 반지름의 길이가 4 인 원 $C_{2}$ 가 있다．두 원 $C_{1}, C_{2}$ 가 만나는 두 점 중 한 점을 A ，선분 $\\mathrm{O}_{1} \\mathrm{O}_{2}$ 가 원 $C_{1}$ 과 만나는 점을 B ，직선 AB 가 원 $C_{2}$ 와 만나는 점 중 A 가 아닌 점을 C 라 하자．〈보기〉에서 옳은 것만을 있는 대로 고른 것은？［4점］

〈보기〉\\\\
ᄀ． $\\cos \\left(\\angle \\mathrm{AO}_{1} \\mathrm{~B}\\right)=-\\frac{1}{4}$\\\\
ㄴ．$\\overline{\\mathrm{BC}}=\\frac{3 \\sqrt{10}}{2}$\\\\
ㄷ．삼각형 $\\mathrm{O}_{1} \\mathrm{CB}$ 의 외접원의 넓이는 $28 \\pi$ 이다．\\\\
（1）ᄀ\\\\
（2）ᄀ，ᄂ\\\\
（3）ᄀ，ᄃ\\\\
（4）ᄂ，ᄃ\\\\
（5）ᄀ，ᄂ，ᄃ\\\\
\\includegraphics[max width=\\textwidth, center]{8d030df5-32f5-436f-8d16-2c468ea8508a-01_445_449_1446_966}

반지름의 길이가 3 인 원 $C_{1}$ 에 반지름의 길이가 $r(r<3)$ 인 원 $C_{2}$ 가 점 T 에서 내접한다. 점 T 에서 원 $C_{1}$ 에 접하는 직선 위의 점 중 T 가 아닌 점 P 를 지나고 원 $C_{2}$ 에 접하는 직선이 원 $C_{2}$ 와 접하는 점을 Q , 원 $C_{1}$ 과 만나는 두 점을 각각 $\\mathrm{R}, \\mathrm{S}$ 라 하자. $\\angle \\mathrm{TPQ}=\\theta_{1}, \\angle \\mathrm{TSQ}=\\theta_{2}$ 일 때,

$$
\\frac{\\sin \\theta_{1}}{\\sin \\theta_{2}}=\\frac{3 \\sqrt{5}}{5}, \\quad \\cos \\left(\\theta_{1}+\\theta_{2}\\right)=\\frac{\\sqrt{5}}{5}
$$

이다. $r=\\frac{q}{p}$ 일 때, $p+q$ 의 값을 구하시오. (단, $\\overline{\\mathrm{PR}}<\\overline{\\mathrm{PS}}$ 이고, $p$ 와 $q$ 는 서로소인 자연수이다.) [4점]\\\\
\\includegraphics[max width=\\textwidth, center]{8d030df5-32f5-436f-8d16-2c468ea8508a-02_511_644_1082_856}

한 원 위에 있는 네 점 $\\mathrm{A}, \\mathrm{B}, \\mathrm{C}, \\mathrm{D}$ 가 다음 조건을 만족시킨다.\\\\
(가) $\\overline{\\mathrm{AB}} \\times \\overline{\\mathrm{AD}}=\\overline{\\mathrm{CB}} \\times \\overline{\\mathrm{CD}}=\\frac{9}{2}, \\overline{\\mathrm{BD}}=\\frac{\\sqrt{65}}{2}$\\\\
(나) 사각형 ABCD 의 둘레의 길이는 10 이다.

사각형 ABCD 의 넓이를 $s$ 라 할 때, $s^{2}$ 의 값을 구하시오. (단, 두 선분 $\\mathrm{AC}, \\mathrm{BD}$ 는 한 점에서 만난다.)\\[0pt]
[4점]\\\\
$\\overline{\\mathrm{AB}}=3, \\overline{\\mathrm{BC}}=4, \\overline{\\mathrm{CA}}=\\sqrt{13}$ 인 삼각형 ABC 가 있다．삼각형 ABC 의 내부의 점 P 에 대하여 삼각형 PAB 의 외접원의 반지름의 길이가 $\\sqrt{3}$ ，삼각형 PBC 의 외접원의 반지름의 길이가 $\\frac{4 \\sqrt{3}}{3}$ 일 때，〈보기〉에서 옳은 것만을 있는 대로 고른 것은？［4점］

〈보기〉\\\\
ㄱ．$\\angle \\mathrm{ABC}=\\frac{\\pi}{3}$\\\\
ᄂ． $\\sin (\\angle \\mathrm{PAB}): \\sin (\\angle \\mathrm{PCB})=4: 3$\\\\
ㄷ．$\\overline{\\mathrm{PA}} \\times \\overline{\\mathrm{PC}}=\\frac{144}{37}$\\\\
（1）ᄀ\\\\
（2）ᄀ，ᄂ\\\\
（3）ᄀ，ᄃ\\\\
（4）ᄂ，ᄃ\\\\
（5）ᄀ，ᄂ，ᄃ\\\\
\\includegraphics[max width=\\textwidth, center]{8d030df5-32f5-436f-8d16-2c468ea8508a-04_581_517_1412_926}

그림과 같이 한 변의 길이가 2 인 마름모 ABCD 가 있다．선분 CD 를 지름으로 하는 원 $C$ 에 대하여 원 $C$ 와 선분 BC 가 만나는 점 중 C 가 아닌 점을 E ，점 A 에서 원 C 에 그은 한 접선의 접점을 F 라 하자． $\\angle \\mathrm{FEC}=\\alpha, \\angle \\mathrm{FAD}=\\beta$ 라 할 때，$\\frac{\\sin \\alpha}{\\sin \\beta}=2 \\sqrt{5}$ 이다．〈보기〉에서 옳은 것만을 있는 대로 고른 것은？\\\\
（단，$\\angle \\mathrm{BCD}<\\frac{\\pi}{2}$ 이고，점 F 는 점 E 를 포함하지 않는 호 CD 위에 있다．）［4점］\\\\
\\includegraphics[max width=\\textwidth, center]{8d030df5-32f5-436f-8d16-2c468ea8508a-05_377_646_1036_867}

〈보기〉\\\\
ᄀ．$\\overline{\\mathrm{DF}}=2 \\cos \\alpha$\\\\
ㄴ． $\\sin \\beta=\\frac{1}{10}$\\\\
ㄷ．삼각형 ADF 의 외접원의 중심을 O 라 하면 삼각형 CFO 의 넓이는 $\\frac{2}{5}$ 이다．\\\\
（1）ᄀ\\\\
（2）ᄀ，ᄂ\\\\
（3）ᄀ，ᄃ\\\\
（4）ᄂ，ᄃ\\\\
（5）ᄀ，ᄂ，ᄃ

\\section*{Chapter 3}
수열

첫째항이 -6 이고 공차가 $\\frac{4}{3}$ 인 등차수열 $\\left\\{a_{n}\\right\\}$ 에 대하여 부등식

$$
\\left(a_{m}\\right)^{2}-\\left|a_{m}\\right|-2 \\leq 0
$$

을 만족시키는 모든 자연수 $m$ 의 값의 합을 구하시오. [4점]

\\section*{Chapter 3}
수열

첫째항과 공차가 같은 등차수열 $\\left\\{a_{n}\\right\\}$ 과 수열 $\\left\\{b_{n}\\right\\}$ 이 모든 자연수 $n$ 에 대하여

$$
a_{n+1}=(-1)^{n} b_{n}-2 a_{n}
$$

을 만족시킨다. $\\sum_{k=1}^{30} b_{k}=90$ 일 때, $\\sum_{k=1}^{15} b_{k}$ 의 값은? [4점]\\\\
(1) -80\\\\
(2) -50\\\\
(3) -20\\\\
(4) 10\\\\
(5) 40

\\section*{Chapter 3}
수열

공차가 3 이고 모든 항이 자연수인 등차수열 $\\left\\{a_{n}\\right\\}$ 에 대하여

$$
\\left|\\sum_{n=1}^{m}(-1)^{n+1} a_{n}\\right|=126
$$

을 만족시키는 모든 자연수 $m$ 의 값의 합이 157 일 때, $\\sum_{n=1}^{10} a_{n}$ 의 값을 구하시오. [4점]

\\section*{Chapter 3 \\\\
 수열}
모든 항이 양수인 등차수열 $\\left\\{a_{n}\\right\\}$ 에 대하여 수열 $\\left\\{b_{n}\\right\\}$ 이

$$
b_{n}= \\begin{cases}a_{n} & (n \\leq 10) \\\\ a_{n-10} & (n>10)\\end{cases}
$$

이다.

$$
\\sum_{n=1}^{9} \\log _{2} \\frac{b_{n+1}}{b_{n}}=2, \\quad \\sum_{n=1}^{5} b_{4 n}=80
$$

일 때, $\\sum_{n=1}^{10} a_{n}$ 의 값을 구하시오. [4점]

\\section*{Chapter 3}
수열

공차가 정수인 두 등차수열 $\\left\\{a_{n}\\right\\},\\left\\{b_{n}\\right\\}$ 이 다음 조건을 만족시킨다.\\\\
(가) $a_{1}=b_{1}+5$\\\\
(나) $\\left|a_{3}\\right|=b_{3}$\\\\
$\\sum_{n=1}^{7}\\left(a_{n}+b_{n}\\right)=7$ 일 때, $a_{6}+b_{10}$ 의 최솟값을 구하시오. [4점]

\\section*{Chapter 3}
수열

공차가 -3 이고 모든 항이 정수인 등차수열 $\\left\\{a_{n}\\right\\}$ 의 첫째항부터 제 $n$ 항까지의 합을 $S_{n}$ 이라 하자.

$$
S_{m}>S_{m+1}
$$

을 만족시키는 자연수 $m$ 의 최솟값이 4 일 때, 모든 $a_{1}$ 의 값의 합을 구하시오. [4점]


\\end{document}"""


def extract_problems_from_latex(latex_content, debug=False):
    """LaTeX에서 문제 추출"""
    problems = []
    
    # 본문 추출
    body = extract_body(latex_content)
    
    if debug:
        print("[LaTeX 구조 진단]")
        diagnose_latex_structure(body, max_chars=300)
    
    # 점수 마커로 문제 구분
    point_markers = list(re.finditer(r'\[4점\]|［4점］', body))
    print(f"[디버깅] [4점] 마커 발견: {len(point_markers)}개")
    
    # 각 점수 마커 주변에서 문제 추출
    for i, marker in enumerate(point_markers, 1):
        start_pos = max(0, marker.start() - 1500)
        end_pos = min(len(body), marker.end() + 800)
        
        # 문제 시작 찾기
        problem_start = start_pos
        for j in range(marker.start(), max(0, marker.start() - 1500), -1):
            if j > 0:
                # 이전 문제의 끝 또는 섹션 시작 찾기
                if j > 100:
                    prev_marker = body.rfind('[4점]', max(0, j-800), j)
                    if prev_marker == -1:
                        prev_marker = body.rfind('［4점］', max(0, j-800), j)
                    if prev_marker != -1:
                        problem_start = prev_marker + 200
                        break
                # 섹션 시작 찾기
                if body[j:j+10].find('\\section') != -1:
                    problem_start = j
                    break
        
        # 문제 끝 찾기
        problem_end = marker.end() + 500
        next_section = body.find('\\section', marker.end())
        if next_section != -1:
            problem_end = min(problem_end, next_section)
        next_problem = body.find('[4점]', marker.end() + 50)
        if next_problem == -1:
            next_problem = body.find('［4점］', marker.end() + 50)
        if next_problem != -1:
            problem_end = min(problem_end, next_problem - 50)
        
        problem_text = body[problem_start:problem_end]
        
        # 선택지 확인
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
        
        # 텍스트 정리
        question = clean_latex_text(question)
        
        # 문제 시작 부분이 너무 짧으면 확장
        if len(question) < 50:
            extended_start = max(0, problem_start - 500)
            extended_text = body[extended_start:problem_end]
            question_end_ext = extended_text.find('[4점]')
            if question_end_ext == -1:
                question_end_ext = extended_text.find('［4점］')
            if question_end_ext != -1:
                question = clean_latex_text(extended_text[:question_end_ext])
                options_text = extended_text[question_end_ext:] if has_options else ""
        
        if len(question) < 30:
            continue
        
        # 주제 판단 (수열 또는 기하)
        topic = "수열" if "수열" in question or "등차수열" in question or "Chapter 3" in body[max(0, problem_start-200):problem_start] else "기하"
        
        # 선택지 추출
        options = []
        if has_options and options_text:
            # 보기 문제 (ㄱ, ㄴ, ㄷ)
            if 'ㄱ' in options_text or 'ㄴ' in options_text or 'ㄷ' in options_text:
                # 보기 내용은 문제 본문에 포함되므로 선택지에서 제외
                # 선택지만 추출 (1) ~ (5)
                for opt_num in range(1, 6):
                    pattern = rf'（{opt_num}）\s*([^（]+?)(?=（[1-5]）|$|\\section|\\end|\\includegraphics)'
                    match = re.search(pattern, options_text)
                    if match:
                        option_num = ["①", "②", "③", "④", "⑤"][opt_num-1]
                        opt_text = clean_latex_text(match.group(1))
                        # 보기 내용이 선택지에 포함되지 않도록 확인
                        if '〈보기〉' not in opt_text and 'ㄱ' not in opt_text and 'ㄴ' not in opt_text and 'ㄷ' not in opt_text:
                            options.append(f"{option_num} {opt_text}")
            else:
                # 일반 객관식 문제
                options = extract_options_generic(options_text, num_options=5)
        
        # 문제 추가
        if len(options) >= 5:
            problems.append({
                "index": f"{i:02d}",
                "page": (i // 2) + 1,
                "topic": topic,
                "question": question,
                "point": 4,
                "answer_type": "multiple_choice",
                "options": options
            })
        elif len(question) > 50:
            problems.append({
                "index": f"{i:02d}",
                "page": (i // 2) + 1,
                "topic": topic,
                "question": question,
                "point": 4,
                "answer_type": "short_answer"
            })
    
    return problems


def main():
    """메인 실행 함수"""
    print("=" * 60)
    print("[수1 드릴 P5 문제 LaTeX → CSV 변환]")
    print("=" * 60)
    
    # 1단계: LaTeX 읽기
    print(f"\n[1단계] LaTeX 내용 읽기 완료 ({len(latex_content)}자)")
    
    # 2단계: 문제 추출
    print("\n[2단계] 문제 추출 중...")
    problems = extract_problems_from_latex(latex_content, debug=False)
    print(f"[완료] {len(problems)}개 문제 추출됨")
    
    # 3단계: 검토
    print("\n[3단계] 문제 검토 중...")
    is_valid = review_problems(problems)
    
    # 4단계: 저장
    print("\n[4단계] 딥시크용 파일 저장 중...")
    base_dir = Path(r'C:\Users\a\Documents\MathPDF\organized\현우진\수1_2025학년도_현우진_드릴')
    base_filename = "수1_2025학년도_현우진_드릴_P5_문제"
    csv_path, json_path = save_for_deepseek(problems, base_dir, base_filename)
    
    print("\n" + "=" * 60)
    print("[완료] 딥시크가 읽을 수 있는 형태로 저장되었습니다.")
    print("=" * 60)
    print(f"저장 위치: {base_dir}")
    print(f"  - CSV: {csv_path.name}")
    print(f"  - JSON: {json_path.name}")


if __name__ == '__main__':
    main()
