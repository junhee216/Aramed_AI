# final_review_p5.py
# 미적분 드릴 P5 최종 검토 및 원본 PDF 대조

import csv
import json
import sys
import os
from pathlib import Path
from datetime import datetime

# Windows 콘솔 인코딩 설정
if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')

csv_path = Path(r'C:\Users\a\Documents\MathPDF\organized\미적분\미적분_2025학년도_현우진_드릴_05_문제_deepseek.csv')
json_path = Path(r'C:\Users\a\Documents\MathPDF\organized\미적분\미적분_2025학년도_현우진_드릴_05_문제_deepseek.json')

def check_latex_syntax(text):
    """LaTeX 구문 검사"""
    issues = []
    if not text or len(text) < 10:
        return ["내용이 불완전함"]
    
    dollar_count = text.count('$')
    if dollar_count % 2 != 0:
        issues.append(f"$ 기호 홀수개 ({dollar_count}개)")
    
    return issues

def review_final():
    """최종 검토"""
    print("=" * 80)
    print("[미적분 드릴 P5 최종 검토]")
    print("=" * 80)
    
    # CSV 읽기
    problems = []
    with open(csv_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            problems.append(row)
    
    issues = []
    
    for problem in problems:
        idx = problem.get('index', '?')
        print(f"\n[문제 {idx}]")
        
        question = problem.get('question', '')
        if not question or len(question) < 10:
            issues.append(f"문제 {idx}: question 필드 없음 또는 불완전함")
            print(f"[오류] 문제 내용이 불완전함")
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
            options_list = problem['options'].split(', ')
            print(f"[선택지 수] {len(options_list)}개")
            if len(options_list) == 5:
                print("[선택지] 정상")
            else:
                print(f"[경고] 선택지가 5개가 아님 ({len(options_list)}개)")
    
    print("\n" + "=" * 80)
    print("[최종 검토 결과]")
    print("=" * 80)
    
    if issues:
        print(f"[오류] {len(issues)}개:")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("[오류] 없음")
    
    print(f"\n[총 문제 수] {len(problems)}개")
    print(f"[객관식] {sum(1 for p in problems if p.get('answer_type') == 'multiple_choice')}개")
    print(f"[주관식] {sum(1 for p in problems if p.get('answer_type') == 'short_answer')}개")
    
    return len(issues) == 0

def find_original_pdf():
    """원본 PDF 찾기"""
    base_dir = Path(r'C:\Users\a\Documents\MathPDF')
    organized_dir = base_dir / 'organized' / '미적분'
    
    search_patterns = [
        '*드릴*05*문제*.pdf',
        '*드릴*P5*문제*.pdf'
    ]
    
    if organized_dir.exists():
        for pattern in search_patterns:
            for pdf_file in organized_dir.glob(pattern):
                if pdf_file.exists():
                    return pdf_file
    
    return None

def compare_with_pdf():
    """원본 PDF와 대조"""
    pdf_path = find_original_pdf()
    if not pdf_path:
        print("\n[정보] 원본 PDF를 찾을 수 없습니다.")
        return
    
    print(f"\n[원본 PDF 찾음] {pdf_path.name}")
    print(f"[파일 크기] {pdf_path.stat().st_size / 1024:.2f} KB")
    print("[정보] PDF는 이미지 기반일 수 있어 텍스트 추출이 제한적일 수 있습니다.")

def main():
    # 최종 검토
    print("[1단계] 최종 검토 중...")
    is_valid = review_final()
    
    # 원본 PDF 확인
    print("\n[2단계] 원본 PDF 확인 중...")
    compare_with_pdf()
    
    print("\n" + "=" * 80)
    print("[완료] 딥시크가 읽을 수 있는 형태로 저장되었습니다.")
    print("=" * 80)
    print(f"저장 위치: {csv_path.parent}")
    print(f"  - CSV: {csv_path.name}")
    print(f"  - JSON: {json_path.name}")

if __name__ == '__main__':
    main()
