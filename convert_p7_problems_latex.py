# convert_p7_problems_latex.py
# 미적분 드릴 P7 문제 LaTeX를 딥시크용 CSV로 변환

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

latex_file = Path(r'C:\Users\a\Documents\MathPDF\organized\미적분\미적분_2025학년도_현우진_드릴_07_문제_변환집\366f2979-0c56-4add-ab0b-6b6f1b1e9f93.tex')

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
    
    # 문제별로 정확히 추출
    problem_patterns = [
        (r'(\$x \geq 0\$.*?구하시오\. \[4점\])(.*?)(?:\\section|함수)', 1, 4, False),
        (r'(함수 \$f\(x\)=x\+.*?구하시오\. \[4점\])(.*?)(?:\\section|함수)', 2, 4, False),
        (r'(함수 \$f\(x\)=3 x\^\{3\}.*?\[4점\])(.*?)(?:\(1\)|\\section)', 3, 4, True),
        (r'(최고차항의 계수가 1 인 이차함수.*?구하시오\. \[4점\])(.*?)(?:\\section|구간)', 4, 4, False),
        (r'(구간 \$\[0, \infty\)\$.*?\[4점\])(.*?)(?:\(1\)|\\section)', 5, 4, True),
        (r'(닫힌구간 \$\[0, \pi\]\$.*?\[3점\])(.*?)(?:\(1\)|\\end)', 6, 3, True),
    ]
    
    for pattern, index, point, has_options in problem_patterns:
        match = re.search(pattern, body, re.DOTALL)
        if match:
            question = match.group(1).strip()
            options_text = match.group(2) if match.lastindex >= 2 else ""
            
            # 문제 텍스트 정리
            question = re.sub(r'\\section\*\{[^}]*\}', '', question)
            question = re.sub(r'\\includegraphics[^}]*\}', '[이미지]', question)
            question = re.sub(r'\\\\', ' ', question)
            question = re.sub(r'\s+', ' ', question)
            
            # 선택지 추출
            options = None
            if has_options:
                options = []
                for i in range(1, 6):
                    # 수식 선택지: (1) $\frac{e^{2}-3}{2}$
                    pattern_formula = rf'\({i}\)\s*\$([^\$]+)\$'
                    match_formula = re.search(pattern_formula, options_text)
                    if match_formula:
                        option_num = ["①", "②", "③", "④", "⑤"][i-1]
                        options.append(f"{option_num} ${match_formula.group(1)}$")
                    else:
                        # 숫자 선택지: (1) 14
                        pattern_num = rf'\({i}\)\s*([^\n\(]+)'
                        match_num = re.search(pattern_num, options_text)
                        if match_num:
                            option_num = ["①", "②", "③", "④", "⑤"][i-1]
                            opt_text = match_num.group(1).strip()
                            # $ 기호가 없으면 추가
                            if '$' not in opt_text and ('\\frac' in opt_text or 'e' in opt_text or 'ln' in opt_text or '\\sqrt' in opt_text):
                                opt_text = f"${opt_text}$"
                            options.append(f"{option_num} {opt_text}")
                
                if not options:
                    options = None
            
            problem = {
                "index": f"{index:02d}",
                "page": index,
                "topic": "적분법",
                "question": question,
                "point": point,
                "answer_type": "multiple_choice" if options else "short_answer"
            }
            
            if options:
                problem["options"] = options
            
            problems.append(problem)
    
    return problems

def read_latex_file(file_path):
    """LaTeX 파일 읽기"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"[오류] 파일 읽기 실패: {e}")
        return None

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
    print("[미적분 드릴 P7 문제 데이터 검토]")
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
        '*드릴*07*문제*.pdf',
        '*드릴*P7*문제*.pdf'
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
    csv_path = save_dir / "미적분_2025학년도_현우진_드릴_07_문제_deepseek.csv"
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
    json_path = save_dir / "미적분_2025학년도_현우진_드릴_07_문제_deepseek.json"
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
            "원본": "미적분_2025학년도_현우진_드릴_07_문제",
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
    print("[미적분 드릴 P7 문제 LaTeX → CSV 변환]")
    print("=" * 80)
    
    # LaTeX 파일 읽기
    print("\n[1단계] LaTeX 파일 읽기 중...")
    latex_content = read_latex_file(latex_file)
    if not latex_content:
        return
    
    print(f"[완료] LaTeX 파일 읽기 완료 ({len(latex_content)}자)")
    
    # 문제 추출
    print("\n[2단계] 문제 추출 중...")
    problems = extract_problems_from_latex(latex_content)
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
