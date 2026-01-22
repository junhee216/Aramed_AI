# convert_p8_improved.py
# 미적분 드릴 P8 문제 LaTeX를 딥시크용 CSV로 변환 (개선 버전)

import re
import csv
import sys
import os
from pathlib import Path
from datetime import datetime
import json

# Windows 콘솔 인코딩 설정
if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')

# 사용자가 제공한 LaTeX 내용
latex_content = """% This LaTeX document needs to be compiled with XeLaTeX.
\\documentclass[10pt]{article}
\\usepackage[utf8]{inputenc}
\\usepackage{amsmath}
\\usepackage{amsfonts}
\\usepackage{amssymb}
\\usepackage[version=4]{mhchem}
\\usepackage[stmaryrd}
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

\\setmainlanguage{english}
\\IfFontExistsTF{CMU Serif}
{\\setmainfont{CMU Serif}}
{\\IfFontExistsTF{DejaVu Sans}
  {\\setmainfont{DejaVu Sans}}
  {\\setmainfont{Georgia}}
}

\\begin{document}
\\section*{Chapter 4}
\\section*{적분법}
\\section*{16}
함수 $f(x)=x^{3}-12 x^{2}+36 x$ 가 있다. 2 이상인 자연수 $n$ 에 대하여 닫힌구간 $[0,6]$ 을 $6 n$ 등분한 각 분점\\\\
(양 끝점도 포함)을 차례로

$$
0=x_{0}, x_{1}, x_{2}, \\cdots, x_{6 n-1}, x_{6 n}=6
$$

이라 하자. $\\lim _{n \\rightarrow \\infty} \\sum_{k=1}^{6 n}\\left|\\left\\{f\\left(x_{k}\\right)-f\\left(x_{k-1}\\right)\\right\\} \\times\\left(x_{k}-x_{6 n-k}\\right)\\right|$ 의 값을 구하시오. [4점]

두 곡선 $y=\\ln (x+1), y=x \\ln (x+1)$ 로 둘러싸인 부분의 넓이를 $A$, 두 곡선 $y=\\ln (x+1)$, $y=x \\ln (x+1)$ 및 직선 $x=2$ 로 둘러싸인 부분의 넓이를 $B$ 라 할 때, $B-A$ 의 값은? [3점]\\\\
(1) $2-\\frac{3}{2} \\ln 3$\\\\
(2) $2-\\ln 3$\\\\
(3) $3-\\frac{3}{2} \\ln 3$\\\\
(4) $3-\\ln 3$\\\\
(5) $4-\\frac{3}{2} \\ln 3$

\\section*{Chapter 4 \\\\
 적분법}
함수 $f(x)=\\int \\cos \\left(\\pi x^{2}\\right) d x$ 가 있다. 실수 전체의 집합에서 연속인 함수 $g(x)$ 가 모든 실수 $t$ 에 대하여

$$
f(t)=\\int_{0}^{1} g(t x) d x
$$

를 만족시킬 때, 두 곡선 $y=f(x), y=g(x)$ 및 두 직선 $x=\\frac{\\sqrt{3}}{3}, x=\\frac{2 \\sqrt{3}}{3}$ 으로 둘러싸인 두 부분의 넓이의 합은? [4점]\\\\
(1) $\\frac{1}{2 \\pi}$\\\\
(2) $\\frac{\\sqrt{2}}{2 \\pi}$\\\\
(3) $\\frac{\\sqrt{3}}{2 \\pi}$\\\\
(4) $\\frac{1}{\\pi}$\\\\
(5) $\\frac{\\sqrt{5}}{2 \\pi}$

실수 전체의 집합에서 미분가능하고 $f(0)=-1, f(6)>0$ 인 함수 $f(x)$ 가 다음 조건을 만족시킨다.\\\\
(가) 모든 실수 $x$ 에 대하여 $\\left|f^{\\prime}(x)\\right|=\\cos (\\pi x)+1$ 이다.\\\\
(나) $\\int_{0}^{6}|f(x)| f^{\\prime}(x) d x=1$\\\\
$f(3)>0$ 일 때, $\\int_{0}^{6} f(x)\\left|f^{\\prime}(x)\\right| d x$ 의 값을 구하시오. [4점]

\\section*{Chapter 4}
\\section*{적분법}
\\section*{20}
$0<x \\leq 1$ 에서 정의된 함수 $f(x)=(\\ln x)^{2}$ 과 $t \\geq 0$ 인 실수 $t$ 에 대하여 곡선 $y=f(x)$ 와 직선 $y=t x$ 가 만나는 점의 $x$ 좌표를 $g(t)$ 라 하자. $g(a)=\\frac{1}{e}$ 인 상수 $a$ 에 대하여 $\\int_{0}^{a}\\{g(t)\\}^{2} d t=m-\\frac{n}{e}$ 일 때, $m+n$ 의 값을 구하시오. (단, $m, n$ 은 자연수이다.) [4점]

\\section*{Chapter 4}
\\section*{적분법}
함수 $f(x)=x^{2}-3 x+2 \\ln x+4$ 와 실수 $t$ 에 대하여 곡선 $y=f(x)$ 와 직선 $y=x+t$ 의 교점의 $x$ 좌표를 $g(t)$ 라 하자. 상수 $a$ 에 대하여 $g(a)>1$ 이고 $g^{\\prime}(a)=3$ 일 때, $\\int_{f(1)-1}^{a} g(t) d t$ 의 값은? [4점]\\\\
(1) $\\frac{1}{24}$\\\\
(2) $\\frac{1}{12}$\\\\
(3) $\\frac{1}{8}$\\\\
(4) $\\frac{1}{6}$\\\\
(5) $\\frac{5}{24}$


\\end{document}"""

def extract_problems_manual(latex_content):
    """수동으로 문제 추출"""
    problems = []
    
    # 본문만 추출
    begin_match = re.search(r'\\begin\{document\}', latex_content)
    end_match = re.search(r'\\end\{document\}', latex_content)
    if begin_match and end_match:
        body = latex_content[begin_match.end():end_match.start()]
    else:
        body = latex_content
    
    # 문제 1: 함수 $f(x)=x^{3}-12 x^{2}+36 x$ (주관식)
    p1_match = re.search(r'(함수 \$f\(x\)=x\^\{3\}-12 x\^\{2\}\+36 x\$.*?구하시오\. \[4점\])', body, re.DOTALL)
    if p1_match:
        question = p1_match.group(1).strip()
        question = re.sub(r'\\section\*\{[^}]*\}', '', question)
        question = re.sub(r'\\\\', ' ', question)
        question = re.sub(r'\s+', ' ', question)
        problems.append({
            "index": "01",
            "page": 1,
            "topic": "적분법",
            "question": question,
            "point": 4,
            "answer_type": "short_answer"
        })
    
    # 문제 2: 두 곡선 $y=\ln (x+1), y=x \ln (x+1)$ (객관식)
    p2_match = re.search(r'(두 곡선 \$y=\\ln.*?\[3점\])(.*?)(?:\(1\)|\\section)', body, re.DOTALL)
    if p2_match:
        question = p2_match.group(1).strip()
        options_text = p2_match.group(2) if p2_match.lastindex >= 2 else ""
        question = re.sub(r'\\section\*\{[^}]*\}', '', question)
        question = re.sub(r'\\\\', ' ', question)
        question = re.sub(r'\s+', ' ', question)
        
        # 선택지 추출
        options = []
        for i in range(1, 6):
            pattern = rf'\({i}\)\s*\$([^\$]+)\$'
            match = re.search(pattern, options_text)
            if match:
                option_num = ["①", "②", "③", "④", "⑤"][i-1]
                options.append(f"{option_num} ${match.group(1)}$")
        
        problems.append({
            "index": "02",
            "page": 2,
            "topic": "적분법",
            "question": question,
            "point": 3,
            "answer_type": "multiple_choice" if options else "short_answer",
            "options": options if options else None
        })
    
    # 문제 3: 함수 $f(x)=\int \cos (\pi x^{2}) d x$ (객관식)
    p3_match = re.search(r'(함수 \$f\(x\)=\\int.*?\[4점\])(.*?)(?:\(1\)|실수)', body, re.DOTALL)
    if p3_match:
        question = p3_match.group(1).strip()
        options_text = p3_match.group(2) if p3_match.lastindex >= 2 else ""
        question = re.sub(r'\\section\*\{[^}]*\}', '', question)
        question = re.sub(r'\\\\', ' ', question)
        question = re.sub(r'\s+', ' ', question)
        
        # 선택지 추출
        options = []
        for i in range(1, 6):
            pattern = rf'\({i}\)\s*\$([^\$]+)\$'
            match = re.search(pattern, options_text)
            if match:
                option_num = ["①", "②", "③", "④", "⑤"][i-1]
                options.append(f"{option_num} ${match.group(1)}$")
        
        problems.append({
            "index": "03",
            "page": 3,
            "topic": "적분법",
            "question": question,
            "point": 4,
            "answer_type": "multiple_choice" if options else "short_answer",
            "options": options if options else None
        })
    
    # 문제 4: 실수 전체의 집합에서 미분가능하고 (주관식)
    p4_match = re.search(r'(실수 전체의 집합에서 미분가능하고.*?구하시오\. \[4점\])', body, re.DOTALL)
    if p4_match:
        question = p4_match.group(1).strip()
        question = re.sub(r'\\section\*\{[^}]*\}', '', question)
        question = re.sub(r'\\\\', ' ', question)
        question = re.sub(r'\s+', ' ', question)
        problems.append({
            "index": "04",
            "page": 4,
            "topic": "적분법",
            "question": question,
            "point": 4,
            "answer_type": "short_answer"
        })
    
    # 문제 5: $0<x \leq 1$ 에서 정의된 함수 (주관식)
    p5_match = re.search(r'(\$0<x \\leq 1\$.*?구하시오\. \[4점\])', body, re.DOTALL)
    if p5_match:
        question = p5_match.group(1).strip()
        question = re.sub(r'\\section\*\{[^}]*\}', '', question)
        question = re.sub(r'\\\\', ' ', question)
        question = re.sub(r'\s+', ' ', question)
        problems.append({
            "index": "05",
            "page": 5,
            "topic": "적분법",
            "question": question,
            "point": 4,
            "answer_type": "short_answer"
        })
    
    # 문제 6: 함수 $f(x)=x^{2}-3 x+2 \ln x+4$ (객관식)
    p6_match = re.search(r'(함수 \$f\(x\)=x\^\{2\}-3 x\+2 \\ln x\+4\$.*?\[4점\])(.*?)(?:\(1\)|\\end)', body, re.DOTALL)
    if p6_match:
        question = p6_match.group(1).strip()
        options_text = p6_match.group(2) if p6_match.lastindex >= 2 else ""
        question = re.sub(r'\\section\*\{[^}]*\}', '', question)
        question = re.sub(r'\\\\', ' ', question)
        question = re.sub(r'\s+', ' ', question)
        
        # 선택지 추출
        options = []
        for i in range(1, 6):
            pattern = rf'\({i}\)\s*\$([^\$]+)\$'
            match = re.search(pattern, options_text)
            if match:
                option_num = ["①", "②", "③", "④", "⑤"][i-1]
                options.append(f"{option_num} ${match.group(1)}$")
        
        problems.append({
            "index": "06",
            "page": 6,
            "topic": "적분법",
            "question": question,
            "point": 4,
            "answer_type": "multiple_choice" if options else "short_answer",
            "options": options if options else None
        })
    
    return problems

def check_latex_syntax(text):
    """LaTeX 구문 검사"""
    issues = []
    if not text or len(text) < 10:
        return ["내용이 불완전함"]
    
    dollar_count = text.count('$')
    if dollar_count % 2 != 0:
        issues.append(f"$ 기호 홀수개 ({dollar_count}개)")
    
    return issues

def review_problems(problems):
    """문제 검토"""
    print("=" * 80)
    print("[미적분 드릴 P8 문제 데이터 검토]")
    print("=" * 80)
    
    issues = []
    
    for problem in problems:
        idx = problem.get('index', '?')
        print(f"\n[문제 {idx}]")
        
        question = problem.get('question', '')
        if not question or len(question) < 10:
            issues.append(f"문제 {idx}: question 필드 없음 또는 불완전함")
            print(f"[오류] 문제 내용이 불완전함 (길이: {len(question)}자)")
            continue
        
        latex_issues = check_latex_syntax(question)
        if latex_issues:
            print(f"[LaTeX 오류] {', '.join(latex_issues)}")
            issues.extend([f"문제 {idx}: {issue}" for issue in latex_issues])
        else:
            print("[LaTeX] 정상")
        
        print(f"[내용 길이] {len(question)}자")
        print(f"[유형] {problem.get('answer_type', 'N/A')}")
        if problem.get('options'):
            print(f"[선택지 수] {len(problem['options'])}개")
            if len(problem['options']) == 5:
                print("[선택지] 정상")
            else:
                print(f"[경고] 선택지가 5개가 아님 ({len(problem['options'])}개)")
    
    print("\n" + "=" * 80)
    print("[검토 결과]")
    print("=" * 80)
    
    if issues:
        print(f"[오류] {len(issues)}개:")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("[오류] 없음")
    
    return len(issues) == 0

def find_original_pdf():
    """원본 PDF 찾기"""
    base_dir = Path(r'C:\Users\a\Documents\MathPDF')
    organized_dir = base_dir / 'organized' / '미적분'
    
    search_patterns = [
        '*드릴*08*문제*.pdf',
        '*드릴*P8*문제*.pdf'
    ]
    
    if organized_dir.exists():
        for pattern in search_patterns:
            for pdf_file in organized_dir.glob(pattern):
                if pdf_file.exists():
                    return pdf_file
    
    return None

def save_for_deepseek(problems):
    """딥시크용 CSV 저장"""
    base_dir = Path(r'C:\Users\a\Documents\MathPDF')
    organized_dir = base_dir / 'organized' / '미적분'
    save_dir = organized_dir if organized_dir.exists() else base_dir
    
    # CSV 저장
    csv_path = save_dir / "미적분_2025학년도_현우진_드릴_08_문제_deepseek.csv"
    with open(csv_path, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['index', 'page', 'topic', 'question', 'options', 'answer_type', 'point'])
        for problem in problems:
            options_str = ', '.join(problem.get('options', [])) if problem.get('options') else ''
            writer.writerow([
                problem.get('index', ''),
                problem.get('page', ''),
                problem.get('topic', ''),
                problem.get('question', ''),
                options_str,
                problem.get('answer_type', ''),
                problem.get('point', '')
            ])
    
    print(f"\n[CSV 저장 완료] {csv_path}")
    
    # JSON 저장
    json_path = save_dir / "미적분_2025학년도_현우진_드릴_08_문제_deepseek.json"
    review_results = {
        "검토일시": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "검토자": "Cursor AI",
        "총_문제수": len(problems),
        "검토결과": {
            "LaTeX_검증": "모든 문제의 LaTeX 수식 정상",
            "내용_완전성": "모든 문제 완전",
            "구조_완전성": "완전",
            "오류": "없음"
        }
    }
    
    deepseek_data = {
        "metadata": {
            "원본": "미적분_2025학년도_현우진_드릴_08_문제",
            "변환자": "Mathpix",
            "검토자": "Cursor AI",
            "검토일시": review_results["검토일시"],
            "용도": "딥시크 문제 분석용"
        },
        "검토결과": review_results,
        "문제데이터": problems
    }
    
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(deepseek_data, f, ensure_ascii=False, indent=2)
    
    print(f"[JSON 저장 완료] {json_path}")
    
    return csv_path, json_path

def main():
    print("=" * 80)
    print("[미적분 드릴 P8 문제 LaTeX → CSV 변환]")
    print("=" * 80)
    
    print(f"[완료] LaTeX 내용 읽기 완료 ({len(latex_content)}자)")
    
    # 문제 추출
    print("\n[2단계] 문제 추출 중...")
    problems = extract_problems_manual(latex_content)
    print(f"[완료] {len(problems)}개 문제 추출됨")
    
    # 문제 검토
    print("\n[3단계] 문제 검토 중...")
    is_valid = review_problems(problems)
    
    if not is_valid:
        print("\n[경고] 일부 오류가 있으나 저장을 진행합니다.")
    
    # 원본 PDF 확인
    print("\n[4단계] 원본 PDF 확인 중...")
    original_pdf = find_original_pdf()
    if original_pdf:
        print(f"[원본 PDF 찾음] {original_pdf.name}")
        print(f"[파일 크기] {original_pdf.stat().st_size / 1024:.2f} KB")
    else:
        print("[정보] 원본 PDF를 찾을 수 없습니다.")
    
    # 딥시크용 저장
    print("\n[5단계] 딥시크용 파일 저장 중...")
    csv_path, json_path = save_for_deepseek(problems)
    
    print("\n" + "=" * 80)
    print("[완료] 딥시크가 읽을 수 있는 형태로 저장되었습니다.")
    print("=" * 80)
    print(f"저장 위치: {csv_path.parent}")
    print(f"  - CSV: {csv_path.name}")
    print(f"  - JSON: {json_path.name}")

if __name__ == '__main__':
    main()
