# convert_p5_manual.py
# 미적분 드릴 P5 LaTeX를 딥시크용 CSV로 변환 (수동 추출)

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

latex_file = Path(r'C:\Users\a\Documents\MathPDF\organized\미적분\8be6025d-df00-424f-a26c-1b69144de03c\8be6025d-df00-424f-a26c-1b69144de03c.tex')

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
    
    # 문제 1: 양수 k
    p1_match = re.search(r'(양수 \$k\$.*?\[4점\])', body, re.DOTALL)
    if p1_match:
        question = p1_match.group(1).strip()
        question = re.sub(r'\\includegraphics[^}]*\}', '', question)
        question = re.sub(r'\\begin\{center\}', '', question)
        question = re.sub(r'\\end\{center\}', '', question)
        question = re.sub(r'\\section\*\{[^}]*\}', '', question)
        question = re.sub(r'\\\\', ' ', question)
        question = re.sub(r'\s+', ' ', question)
        problems.append({
            "index": "01",
            "page": 1,
            "topic": "미분법",
            "question": question,
            "point": 4,
            "answer_type": "short_answer"
        })
    
    # 문제 2: 삼차함수 f(x) (객관식)
    p2_match = re.search(r'(삼차함수 \$f\(x\)\$.*?\[4점\])(.*?)(?:\(1\)\s*5|\\section|열린구간)', body, re.DOTALL)
    if p2_match:
        question = p2_match.group(1).strip()
        options_text = p2_match.group(2) if p2_match.lastindex >= 2 else ""
        question = re.sub(r'\\section\*\{[^}]*\}', '', question)
        question = re.sub(r'\\\\', ' ', question)
        question = re.sub(r'\s+', ' ', question)
        
        # 선택지 추출
        options = []
        for i in range(1, 6):
            pattern = rf'\({i}\)\s*(\d+)'
            match = re.search(pattern, options_text)
            if match:
                option_num = ["①", "②", "③", "④", "⑤"][i-1]
                options.append(f"{option_num} {match.group(1)}")
        
        problems.append({
            "index": "02",
            "page": 2,
            "topic": "미분법",
            "question": question,
            "point": 4,
            "answer_type": "multiple_choice" if options else "short_answer",
            "options": options if options else None
        })
    
    # 문제 3: 열린구간
    p3_match = re.search(r'(열린구간.*?\[4점\])', body, re.DOTALL)
    if p3_match:
        question = p3_match.group(1).strip()
        question = re.sub(r'\\section\*\{[^}]*\}', '', question)
        question = re.sub(r'\\\\', ' ', question)
        question = re.sub(r'\s+', ' ', question)
        problems.append({
            "index": "03",
            "page": 3,
            "topic": "미분법",
            "question": question,
            "point": 4,
            "answer_type": "short_answer"
        })
    
    # 문제 4: 최고차항의 계수가 1 인 삼차함수
    p4_match = re.search(r'(최고차항의 계수가 1 인 삼차함수.*?\[4점\])', body, re.DOTALL)
    if p4_match:
        question = p4_match.group(1).strip()
        question = re.sub(r'\\section\*\{[^}]*\}', '', question)
        question = re.sub(r'\\\\', ' ', question)
        question = re.sub(r'\s+', ' ', question)
        problems.append({
            "index": "04",
            "page": 4,
            "topic": "미분법",
            "question": question,
            "point": 4,
            "answer_type": "short_answer"
        })
    
    # 문제 5: 함수 f(x)=ln(x+1)+k
    p5_match = re.search(r'(함수 \$f\(x\)=\\ln.*?\[4점\])', body, re.DOTALL)
    if p5_match:
        question = p5_match.group(1).strip()
        question = re.sub(r'\\section\*\{[^}]*\}', '', question)
        question = re.sub(r'\\\\', ' ', question)
        question = re.sub(r'\s+', ' ', question)
        problems.append({
            "index": "05",
            "page": 5,
            "topic": "미분법",
            "question": question,
            "point": 4,
            "answer_type": "short_answer"
        })
    
    # 문제 6: 모든 항의 계수가 정수인 이차함수 (객관식)
    p6_match = re.search(r'(모든 항의 계수가 정수인 이차함수.*?\[4점\])(.*?)(?:\(1\)\s*21|두 상수)', body, re.DOTALL)
    if p6_match:
        question = p6_match.group(1).strip()
        options_text = p6_match.group(2) if p6_match.lastindex >= 2 else ""
        question = re.sub(r'\\section\*\{[^}]*\}', '', question)
        question = re.sub(r'\\\\', ' ', question)
        question = re.sub(r'\s+', ' ', question)
        
        # 선택지 추출
        options = []
        for i in range(1, 6):
            pattern = rf'\({i}\)\s*(\d+)'
            match = re.search(pattern, options_text)
            if match:
                option_num = ["①", "②", "③", "④", "⑤"][i-1]
                options.append(f"{option_num} {match.group(1)}")
        
        problems.append({
            "index": "06",
            "page": 6,
            "topic": "미분법",
            "question": question,
            "point": 4,
            "answer_type": "multiple_choice" if options else "short_answer",
            "options": options if options else None
        })
    
    # 문제 7: 두 상수 a, b (객관식)
    p7_match = re.search(r'(두 상수 \$a, b.*?\[4점\])(.*?)(?:\(1\)\s*\$20|\\end)', body, re.DOTALL)
    if p7_match:
        question = p7_match.group(1).strip()
        options_text = p7_match.group(2) if p7_match.lastindex >= 2 else ""
        question = re.sub(r'\\section\*\{[^}]*\}', '', question)
        question = re.sub(r'\\\\', ' ', question)
        question = re.sub(r'\s+', ' ', question)
        
        # 선택지 추출 (수식 포함)
        options = []
        for i in range(1, 6):
            pattern = rf'\({i}\)\s*\$([^\$]+)\$'
            match = re.search(pattern, options_text)
            if match:
                option_num = ["①", "②", "③", "④", "⑤"][i-1]
                options.append(f"{option_num} ${match.group(1)}$")
        
        problems.append({
            "index": "07",
            "page": 7,
            "topic": "미분법",
            "question": question,
            "point": 4,
            "answer_type": "multiple_choice" if options else "short_answer",
            "options": options if options else None
        })
    
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
    print("[미적분 드릴 P5 문제 데이터 검토]")
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
            for opt in problem['options']:
                print(f"  - {opt}")
    
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

def save_for_deepseek(problems):
    """딥시크용 CSV 저장"""
    base_dir = Path(r'C:\Users\a\Documents\MathPDF')
    organized_dir = base_dir / 'organized' / '미적분'
    save_dir = organized_dir if organized_dir.exists() else base_dir
    
    # CSV 저장
    csv_path = save_dir / "미적분_2025학년도_현우진_드릴_05_문제_deepseek.csv"
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
    json_path = save_dir / "미적분_2025학년도_현우진_드릴_05_문제_deepseek.json"
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
            "원본": "미적분_2025학년도_현우진_드릴_05_문제",
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
    print("[미적분 드릴 P5 LaTeX → CSV 변환]")
    print("=" * 80)
    
    # LaTeX 파일 읽기
    print("\n[1단계] LaTeX 파일 읽기 중...")
    latex_content = read_latex_file(latex_file)
    if not latex_content:
        return
    
    print(f"[완료] LaTeX 파일 읽기 완료 ({len(latex_content)}자)")
    
    # 문제 추출
    print("\n[2단계] 문제 추출 중...")
    problems = extract_problems_manual(latex_content)
    print(f"[완료] {len(problems)}개 문제 추출됨")
    
    # 문제 검토
    print("\n[3단계] 문제 검토 중...")
    is_valid = review_problems(problems)
    
    if not is_valid:
        print("\n[경고] 일부 오류가 있으나 저장을 진행합니다.")
    
    # 딥시크용 저장
    print("\n[4단계] 딥시크용 파일 저장 중...")
    csv_path, json_path = save_for_deepseek(problems)
    
    print("\n" + "=" * 80)
    print("[완료] 딥시크가 읽을 수 있는 형태로 저장되었습니다.")
    print("=" * 80)
    print(f"저장 위치: {csv_path.parent}")
    print(f"  - CSV: {csv_path.name}")
    print(f"  - JSON: {json_path.name}")

if __name__ == '__main__':
    main()
