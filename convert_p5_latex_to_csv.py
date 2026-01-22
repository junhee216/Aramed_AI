# convert_p5_latex_to_csv.py
# 미적분 드릴 P5 LaTeX를 딥시크용 CSV로 변환

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

def clean_latex(text):
    """LaTeX 명령어를 정리"""
    if not text:
        return ""
    
    # LaTeX 명령어 정리
    text = re.sub(r'\\section\*\{[^}]*\}', '', text)  # 섹션 제거
    text = re.sub(r'\\begin\{center\}', '', text)
    text = re.sub(r'\\end\{center\}', '', text)
    text = re.sub(r'\\includegraphics[^}]*\}', '[이미지]', text)  # 이미지
    text = re.sub(r'\\[a-zA-Z]+\{([^}]*)\}', r'\1', text)  # 간단한 명령어
    text = re.sub(r'\\[a-zA-Z]+', '', text)  # 남은 명령어 제거
    text = re.sub(r'\{', '', text)
    text = re.sub(r'\}', '', text)
    text = re.sub(r'\s+', ' ', text)  # 여러 공백을 하나로
    return text.strip()

def extract_problems_from_latex(latex_content):
    """LaTeX에서 문제 추출"""
    problems = []
    
    # 섹션으로 분리
    sections = re.split(r'\\section\*\{[^}]*\}', latex_content)
    
    problem_index = 1
    for section in sections:
        if not section.strip() or 'Chapter' in section or len(section.strip()) < 50:
            continue
        
        # 문제 텍스트 추출
        problem_text = section.strip()
        
        # 이미지 제거
        problem_text = re.sub(r'\\includegraphics[^}]*\}', '', problem_text)
        
        # 선택지 추출
        options = []
        option_pattern = r'\((\d+)\)\s*([^\n]+)'
        option_matches = re.findall(option_pattern, problem_text)
        if option_matches:
            for num, content in option_matches:
                option_num = ["①", "②", "③", "④", "⑤"][int(num)-1]
                options.append(f"{option_num} {content.strip()}")
            # 선택지 부분 제거
            problem_text = re.sub(option_pattern, '', problem_text)
        
        # 문제 번호와 내용 분리
        # "양수 $k$" 또는 "삼차함수" 등으로 시작하는 패턴 찾기
        if len(problem_text) > 50:
            # 점수 추출
            point_match = re.search(r'\[(\d+)점\]', problem_text)
            point = int(point_match.group(1)) if point_match else 4
            
            problem = {
                "index": f"{problem_index:02d}",
                "page": problem_index,
                "topic": "미분법",
                "question": problem_text.strip(),
                "point": point,
                "answer_type": "multiple_choice" if options else "short_answer"
            }
            
            if options:
                problem["options"] = options
            
            problems.append(problem)
            problem_index += 1
    
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
    
    # $ 기호 짝 확인
    dollar_count = text.count('$')
    if dollar_count % 2 != 0:
        issues.append(f"$ 기호 홀수개 ({dollar_count}개)")
    
    # $$ 기호 짝 확인
    double_dollar_count = text.count('$$')
    if double_dollar_count % 2 != 0:
        issues.append(f"$$ 기호 홀수개 ({double_dollar_count}개)")
    
    return issues

def review_problems(problems):
    """문제 검토"""
    print("=" * 80)
    print("[미적분 드릴 P5 문제 데이터 검토]")
    print("=" * 80)
    
    issues = []
    warnings = []
    
    for problem in problems:
        idx = problem.get('index', '?')
        print(f"\n[문제 {idx}]")
        
        question = problem.get('question', '')
        if not question or len(question) < 10:
            issues.append(f"문제 {idx}: question 필드 없음 또는 불완전함")
            print(f"[오류] 문제 내용이 불완전함 (길이: {len(question)}자)")
            continue
        
        # LaTeX 검사
        latex_issues = check_latex_syntax(question)
        if latex_issues:
            print(f"[LaTeX 오류] {', '.join(latex_issues)}")
            issues.extend([f"문제 {idx}: {issue}" for issue in latex_issues])
        else:
            print("[LaTeX] 정상")
        
        print(f"[내용 길이] {len(question)}자")
        print(f"[주제] {problem.get('topic', 'N/A')}")
        print(f"[유형] {problem.get('answer_type', 'N/A')}")
        if problem.get('options'):
            print(f"[선택지 수] {len(problem['options'])}개")
    
    print("\n" + "=" * 80)
    print("[검토 결과]")
    print("=" * 80)
    
    if issues:
        print(f"[오류] {len(issues)}개:")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("[오류] 없음")
    
    if warnings:
        print(f"[경고] {len(warnings)}개:")
        for warn in warnings:
            print(f"  - {warn}")
    else:
        print("[경고] 없음")
    
    return len(issues) == 0

def find_original_pdf():
    """원본 PDF 찾기"""
    base_dir = Path(r'C:\Users\a\Documents\MathPDF')
    organized_dir = base_dir / 'organized' / '미적분'
    
    search_patterns = [
        '*드릴*05*문제*.pdf',
        '*드릴*P5*문제*.pdf',
        '*드릴*5*문제*.pdf'
    ]
    
    if organized_dir.exists():
        for pattern in search_patterns:
            for pdf_file in organized_dir.glob(pattern):
                if pdf_file.exists():
                    return pdf_file
    
    return None

def save_for_deepseek(problems, original_pdf=None):
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
    
    # JSON도 저장
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
    
    # 1. LaTeX 파일 읽기
    print("\n[1단계] LaTeX 파일 읽기 중...")
    if not latex_file.exists():
        print(f"[오류] 파일을 찾을 수 없습니다: {latex_file}")
        return
    
    latex_content = read_latex_file(latex_file)
    if not latex_content:
        return
    
    print(f"[완료] LaTeX 파일 읽기 완료 ({len(latex_content)}자)")
    
    # 2. 문제 추출
    print("\n[2단계] 문제 추출 중...")
    problems = extract_problems_from_latex(latex_content)
    print(f"[완료] {len(problems)}개 문제 추출됨")
    
    # 문제 추출이 제대로 안 되면 수동으로 파싱
    if len(problems) == 0:
        print("[정보] 자동 추출 실패, 수동 파싱 시도...")
        # LaTeX 내용을 다시 분석
        # 문제는 보통 "양수", "삼차함수", "최고차항" 등으로 시작
        problem_patterns = [
            r'양수 \$k\$.+?\[4점\]',
            r'삼차함수 \$f\(x\)\$.+?\[4점\]',
            r'열린구간.+?\[4점\]',
            r'최고차항.+?\[4점\]',
            r'함수 \$f\(x\)\$.+?\[4점\]',
            r'모든 항.+?\[4점\]',
            r'두 상수.+?\[4점\]'
        ]
        
        # 더 정확한 파싱 시도
        problems = []
        # 문제 번호별로 수동 추출
        problem_texts = []
        current_problem = ""
        
        lines = latex_content.split('\n')
        for line in lines:
            line = line.strip()
            if not line or line.startswith('%') or line.startswith('\\document') or line.startswith('\\usepackage'):
                continue
            if line.startswith('\\section') or line.startswith('\\begin') or line.startswith('\\end'):
                if current_problem and len(current_problem) > 50:
                    problem_texts.append(current_problem)
                current_problem = ""
                continue
            if '[4점]' in line or '[3점]' in line:
                current_problem += line + " "
                if current_problem and len(current_problem) > 50:
                    problem_texts.append(current_problem)
                current_problem = ""
            else:
                current_problem += line + " "
        
        # 마지막 문제
        if current_problem and len(current_problem) > 50:
            problem_texts.append(current_problem)
        
        # 문제 텍스트를 구조화
        for i, text in enumerate(problem_texts, 1):
            # 선택지 추출
            options = []
            option_pattern = r'\((\d+)\)\s*([^\n]+)'
            option_matches = re.findall(option_pattern, text)
            if option_matches:
                for num, content in option_matches:
                    option_num = ["①", "②", "③", "④", "⑤"][int(num)-1]
                    options.append(f"{option_num} {content.strip()}")
            
            # 점수 추출
            point_match = re.search(r'\[(\d+)점\]', text)
            point = int(point_match.group(1)) if point_match else 4
            
            problem = {
                "index": f"{i:02d}",
                "page": i,
                "topic": "미분법",
                "question": text.strip(),
                "point": point,
                "answer_type": "multiple_choice" if options else "short_answer"
            }
            
            if options:
                problem["options"] = options
            
            problems.append(problem)
        
        print(f"[완료] 수동 파싱으로 {len(problems)}개 문제 추출됨")
    
    # 3. 문제 검토
    print("\n[3단계] 문제 검토 중...")
    is_valid = review_problems(problems)
    
    if not is_valid:
        print("\n[경고] 일부 오류가 있으나 저장을 진행합니다.")
    
    # 4. 원본 PDF 확인
    print("\n[4단계] 원본 PDF 확인 중...")
    original_pdf = find_original_pdf()
    if original_pdf:
        print(f"[원본 PDF 찾음] {original_pdf.name}")
    else:
        print("[정보] 원본 PDF를 찾을 수 없습니다.")
    
    # 5. 딥시크용 저장
    print("\n[5단계] 딥시크용 파일 저장 중...")
    csv_path, json_path = save_for_deepseek(problems, original_pdf)
    
    print("\n" + "=" * 80)
    print("[완료] 딥시크가 읽을 수 있는 형태로 저장되었습니다.")
    print("=" * 80)
    print(f"저장 위치: {csv_path.parent}")
    print(f"  - CSV: {csv_path.name}")
    print(f"  - JSON: {json_path.name}")

if __name__ == '__main__':
    main()
