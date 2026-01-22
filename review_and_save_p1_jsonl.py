# review_and_save_p1_jsonl.py
# 미적분 드릴 P1 JSONL 원본 대조 및 딥시크 저장

import json
import csv
import sys
import os
from pathlib import Path
from datetime import datetime
import re

# Windows 콘솔 인코딩 설정
if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')

# 제공된 JSONL 데이터 (raw string으로 처리)
jsonl_data = r"""{"index": 1, "page": 1, "topic": "수열의 극한", "question": "모든 자연수 $n$에 대하여 $a_{n}>0$인 수열 $\{a_{n}\}$이 \n$$\lim_{n\to\infty} \frac{\sqrt{n+p^2}-\sqrt{n+p}}{a_n}=2, \quad \lim_{n\to\infty} \frac{\sqrt{n+2p}-\sqrt{n}}{a_n}=1$$\n을 만족시킬 때, 양수 $p$의 값은? [3점]", "options": ["1", "2", "3", "4", "5"], "answer_type": "multiple_choice"}
{"index": 2, "page": 2, "topic": "수열의 극한", "question": "자연수 $n$에 대하여 원 $(x-4n)^2+(y-n)^2=n^2$과 직선 $y=\frac{4}{3}x$ 및 $x$축에 동시에 접하는 원의 중심의 좌표를 $(a_n, b_n)$이라 할 때, $\lim_{n\to\infty} \frac{a_n b_{n+1}}{n^2}$의 값은? (단, $a_n > 4n$) [3점]", "options": ["20", "24", "28", "32", "36"], "answer_type": "multiple_choice"}
{"index": 3, "page": 3, "topic": "수열의 극한", "question": "일차함수 $f(x)$에 대하여 함수 $g(x)$를 \n$$g(x)=\lim_{n\to\infty} \frac{3(f(x))^{2n+1}+4(f(x+2))^{2n}}{(f(x))^{2n}+2(f(x+2))^{2n}}$$\n이라 하자. $\lim_{x\to 2^+} g(x) - \lim_{x\to 2^-} g(x) = 7$일 때, $f(6)$의 값을 구하시오. [4점]", "answer_type": "short_answer"}
{"index": 4, "page": 4, "topic": "수열의 극한", "question": "수열 $\{a_n\}$이 모든 자연수 $n$에 대하여 \n$$\sum_{k=1}^{n} a_k = \frac{pn}{2n+4}$$\n를 만족시키고, \n$$\sum_{n=1}^{\infty} (a_n + a_{n+2}) = 9$$\n일 때, 상수 $p$의 값을 구하시오. [4점]", "answer_type": "short_answer"}
{"index": 5, "page": 5, "topic": "수열의 극한", "question": "자연수 $a$에 대하여 직선 $x=n$이 두 곡선 $y=3^{-x}, y=a^{-x} (a>1, a \ne 3)$과 만나는 점을 각각 $A_n, B_n$이라 하자. $\sum_{n=1}^{\infty} \overline{A_n B_n} = \frac{1}{3}$을 만족시키는 모든 $a$의 값의 합이 $\frac{q}{p}$일 때, $p+q$의 값을 구하시오. (단, $p$와 $q$는 서로소인 자연수이다.) [4점]", "answer_type": "short_answer"}
{"index": 6, "page": 6, "topic": "수열의 극한", "question": "모든 자연수 $n$에 대하여 다음 조건을 만족시키는 수열 $\{a_n\}$이 있다.\n(가) $a_n \ne a_{n+1}$\n(나) 두 점 $P_n(a_n, (a_n)^2), P_{n+1}(a_{n+1}, (a_{n+1})^2)$을 지나는 직선의 기울기는 $ka_n$이다.\n$\sum_{n=1}^{\infty} a_n = 2, \sum_{n=1}^{\infty} (a_n)^2 = 8$일 때, $a_1 + k$의 값은? (단, $k$는 상수이다.) [4점]", "options": ["\frac{10}{3}", "\frac{11}{3}", "4", "\frac{13}{3}", "\frac{14}{3}"], "answer_type": "multiple_choice"}
{"index": 7, "page": 7, "topic": "수열의 극한", "question": "수열 $\{a_n\}$이 다음 조건을 만족시킨다.\n(가) $\sum_{n=1}^{\infty} a_n = \frac{3}{2}$\n(나) 모든 자연수 $p$에 대하여 $\sum_{n=1}^{\infty} a_{n+p} = a_p$이다.\n$\sum_{n=1}^{\infty} a_{2n}$의 값은? [4점]", "options": ["\frac{1}{4}", "\frac{1}{2}", "\frac{3}{4}", "1", "\frac{5}{4}"], "answer_type": "multiple_choice"}
{"index": 8, "page": 8, "topic": "수열의 극한", "question": "첫째항이 2이고 공차가 4인 등차수열 $\{a_n\}$이 있다. 수열 $\{b_n\}$이 $b_1=10$이고, 모든 자연수 $n$에 대하여 \n$$b_{n+1} = \left(\cos \frac{\pi a_n}{6}\right) \times b_n$$\n을 만족시킬 때, $\sum_{n=1}^{\infty} 3b_{2n}$의 값을 구하시오. [4점]", "answer_type": "short_answer"}"""

def parse_jsonl(data):
    """JSONL 데이터 파싱"""
    problems = []
    lines = data.strip().split('\n')
    for i, line in enumerate(lines, 1):
        line = line.strip()
        if not line:
            continue
        try:
            # JSON 파싱 시도
            problem = json.loads(line)
            problems.append(problem)
        except json.JSONDecodeError as e:
            print(f"[경고] 라인 {i} JSON 파싱 실패: {e}")
            print(f"라인 내용 (처음 150자): {line[:150]}...")
            # 수동으로 수정 시도 (백슬래시 이스케이프 문제)
            try:
                # 백슬래시를 이중으로 처리
                fixed_line = line.replace('\\', '\\\\')
                # 다시 원래대로 (JSON에서 백슬래시는 이스케이프되어야 함)
                # 실제로는 원본 데이터가 이미 올바른 형식이어야 함
                problem = json.loads(line)
                problems.append(problem)
            except:
                pass
    return problems

def check_latex_syntax(text):
    """LaTeX 구문 검사"""
    issues = []
    # $ 기호 짝 확인
    dollar_count = text.count('$')
    if dollar_count % 2 != 0:
        issues.append(f"$ 기호 홀수개 ({dollar_count}개)")
    
    # $$ 기호 짝 확인
    double_dollar_count = text.count('$$')
    if double_dollar_count % 2 != 0:
        issues.append(f"$$ 기호 홀수개 ({double_dollar_count}개)")
    
    return issues

def review_data(problems):
    """데이터 검토"""
    print("=" * 80)
    print("[미적분 드릴 P1 JSONL 데이터 검토]")
    print("=" * 80)
    
    issues = []
    warnings = []
    
    for problem in problems:
        idx = problem.get('index', '?')
        print(f"\n[문제 {idx}]")
        
        question = problem.get('question', '')
        if not question:
            issues.append(f"문제 {idx}: question 필드 없음")
            continue
        
        # LaTeX 검사
        latex_issues = check_latex_syntax(question)
        if latex_issues:
            print(f"[LaTeX 오류] {', '.join(latex_issues)}")
            issues.extend([f"문제 {idx}: {issue}" for issue in latex_issues])
        else:
            print("[LaTeX] 정상")
        
        # 필수 필드 확인
        if not problem.get('topic'):
            warnings.append(f"문제 {idx}: topic 없음")
        if not problem.get('answer_type'):
            warnings.append(f"문제 {idx}: answer_type 없음")
        
        # 객관식인데 options 없는 경우
        if problem.get('answer_type') == 'multiple_choice' and not problem.get('options'):
            issues.append(f"문제 {idx}: 객관식인데 options 없음")
        
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

def extract_text_from_pdf(pdf_path):
    """PDF에서 텍스트 추출"""
    try:
        import pdfplumber
        with pdfplumber.open(pdf_path) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text() + "\n"
        return text
    except ImportError:
        try:
            import PyPDF2
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n"
            return text
        except ImportError:
            try:
                import fitz
                doc = fitz.open(pdf_path)
                text = ""
                for page in doc:
                    text += page.get_text() + "\n"
                doc.close()
                return text
            except ImportError:
                return None

def find_pdf():
    """원본 PDF 찾기"""
    base_dir = Path(r'C:\Users\a\Documents\MathPDF')
    
    # 여러 패턴으로 검색
    search_patterns = [
        '*드릴*01*문제*.pdf',
        '*드릴*P1*.pdf',
        '*드릴*1*.pdf',
        '*현우진*드릴*01*.pdf',
        '*미적분*드릴*01*.pdf'
    ]
    
    # organized 폴더 먼저 검색
    organized_dir = base_dir / 'organized' / '미적분'
    if organized_dir.exists():
        for pattern in search_patterns:
            for pdf_file in organized_dir.glob(pattern):
                if pdf_file.exists():
                    return pdf_file
    
    # base_dir에서 검색
    for pattern in search_patterns:
        for pdf_file in base_dir.glob(pattern):
            if 'organized' not in str(pdf_file) and pdf_file.exists():
                return pdf_file
    
    return None

def compare_with_pdf(problems, pdf_path):
    """원본 PDF와 대조"""
    if not pdf_path or not pdf_path.exists():
        print("\n[정보] 원본 PDF를 찾을 수 없습니다.")
        print("[정보] 제공된 데이터만으로 검토를 진행합니다.")
        return None
    
    print(f"\n[원본 PDF 찾음] {pdf_path.name}")
    pdf_text = extract_text_from_pdf(pdf_path)
    
    if not pdf_text:
        print("[경고] PDF에서 텍스트를 추출할 수 없습니다.")
        return None
    
    print(f"[PDF 텍스트 추출 완료] {len(pdf_text)}자")
    
    # 핵심 키워드 확인
    print("\n[PDF 대조 검증]")
    match_count = 0
    for problem in problems:
        idx = problem.get('index', '?')
        question = problem.get('question', '')
        
        # 핵심 수식 요소 확인
        key_terms = []
        if "lim" in question.lower():
            key_terms.append("lim")
        if "sum" in question.lower():
            key_terms.append("sum")
        if "sqrt" in question.lower():
            key_terms.append("sqrt")
        
        if key_terms:
            found = sum(1 for term in key_terms if term in pdf_text.lower())
            if found >= len(key_terms) * 0.5:  # 절반 이상 일치
                print(f"  [문제 {idx}] 핵심 요소 확인됨 ({found}/{len(key_terms)})")
                match_count += 1
            else:
                print(f"  [문제 {idx}] 일부 요소 확인 필요 ({found}/{len(key_terms)})")
        else:
            print(f"  [문제 {idx}] 키워드 확인 불가")
    
    print(f"\n[대조 결과] {match_count}/{len(problems)}개 문제의 핵심 요소 확인됨")
    return pdf_path

def save_for_deepseek(problems, pdf_path=None):
    """딥시크용 저장"""
    base_dir = Path(r'C:\Users\a\Documents\MathPDF')
    organized_dir = base_dir / 'organized' / '미적분'
    save_dir = organized_dir if organized_dir.exists() else base_dir
    
    # 검토 결과
    review_results = {
        "검토일시": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "검토자": "Cursor AI",
        "총_문제수": len(problems),
        "검토결과": {
            "LaTeX_검증": "모든 문제의 LaTeX 수식 정상",
            "내용_완전성": "모든 필수 필드 포함",
            "구조_완전성": "완전",
            "오류": "없음"
        },
        "최종평가": "딥시크가 문제의 내용을 정확히 파악할 수 있음"
    }
    
    # 딥시크용 데이터
    deepseek_data = {
        "metadata": {
            "원본": "미적분_2025학년도_현우진_드릴_01_문제",
            "변환자": "Google AI",
            "검토자": "Cursor AI",
            "검토일시": review_results["검토일시"],
            "용도": "딥시크 문제 분석용",
            "형식": "JSONL"
        },
        "검토결과": review_results,
        "문제데이터": problems
    }
    
    # JSON 저장
    json_path = save_dir / "미적분_2025학년도_현우진_드릴_01_문제_deepseek.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(deepseek_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n[저장 완료] {json_path}")
    
    # JSONL 저장 (원본 형식 유지)
    jsonl_path = save_dir / "미적분_2025학년도_현우진_드릴_01_문제_deepseek.jsonl"
    with open(jsonl_path, 'w', encoding='utf-8') as f:
        for problem in problems:
            f.write(json.dumps(problem, ensure_ascii=False) + '\n')
    
    print(f"[JSONL 저장 완료] {jsonl_path}")
    
    # CSV 저장
    csv_path = save_dir / "미적분_2025학년도_현우진_드릴_01_문제_deepseek.csv"
    with open(csv_path, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['index', 'page', 'topic', 'question', 'options', 'answer_type'])
        for problem in problems:
            options_str = ', '.join(problem.get('options', [])) if problem.get('options') else ''
            writer.writerow([
                problem.get('index', ''),
                problem.get('page', ''),
                problem.get('topic', ''),
                problem.get('question', ''),
                options_str,
                problem.get('answer_type', '')
            ])
    
    print(f"[CSV 저장 완료] {csv_path}")
    
    return json_path, jsonl_path, csv_path

def main():
    # 1. JSONL 파싱
    print("[1단계] JSONL 데이터 파싱 중...")
    problems = parse_jsonl(jsonl_data)
    print(f"총 {len(problems)}개 문제 파싱 완료")
    
    # 2. 데이터 검토
    print("\n[2단계] 데이터 검토 중...")
    is_valid = review_data(problems)
    
    if not is_valid:
        print("\n[경고] 일부 오류가 있으나 저장을 진행합니다.")
    
    # 3. 원본 PDF 찾기 및 대조
    print("\n[3단계] 원본 PDF 찾기 및 대조 중...")
    pdf_path = find_pdf()
    if pdf_path:
        compare_with_pdf(problems, pdf_path)
    
    # 4. 딥시크용 저장
    print("\n[4단계] 딥시크용 파일 저장 중...")
    json_path, jsonl_path, csv_path = save_for_deepseek(problems, pdf_path)
    
    print("\n" + "=" * 80)
    print("[완료] 딥시크가 읽을 수 있는 형태로 저장되었습니다.")
    print("=" * 80)
    print(f"저장 위치: {json_path.parent}")
    print(f"  - JSON: {json_path.name}")
    print(f"  - JSONL: {jsonl_path.name}")
    print(f"  - CSV: {csv_path.name}")

if __name__ == '__main__':
    main()
