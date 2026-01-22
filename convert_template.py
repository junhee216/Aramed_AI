# convert_template.py
# LaTeX → CSV 변환 템플릿 (재사용 가능한 구조)

import re
import csv
import json
import sys
import os
from pathlib import Path
from datetime import datetime
from latex_utils import (
    extract_body, diagnose_latex_structure, find_keyword_positions,
    extract_options_generic, extract_problem_with_options,
    clean_latex_text, test_pattern
)

# Windows 콘솔 인코딩 설정
if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')


def extract_problems_from_latex(latex_content, debug=False):
    """
    LaTeX에서 문제 추출 (템플릿 함수)
    이 함수를 각 파일에 맞게 수정하여 사용
    """
    problems = []
    
    # 본문 추출
    body = extract_body(latex_content)
    
    # 디버깅: 구조 진단
    if debug:
        diagnose_latex_structure(body)
        find_keyword_positions(body, ['보기', 'section', 'Chapter'])
    
    # TODO: 여기에 각 파일에 맞는 문제 추출 로직 추가
    # 예시:
    # problem_1 = extract_problem_with_options(
    #     body,
    #     r'(문제 시작 패턴.*?\[4점\])',
    #     r'(\\section|\\end)',
    #     options_extractor=extract_options_generic,
    #     debug=debug
    # )
    # if problem_1 and len(problem_1['options']) == 5:
    #     problems.append({
    #         "index": "01",
    #         "page": 1,
    #         "topic": "주제",
    #         "question": problem_1['question'],
    #         "point": 4,
    #         "answer_type": "multiple_choice",
    #         "options": problem_1['options']
    #     })
    
    return problems


def review_problems(problems):
    """문제 데이터 검토"""
    print("=" * 60)
    print("[문제 데이터 검토]")
    print("=" * 60)
    
    issues = []
    
    for prob in problems:
        idx = prob.get("index", "?")
        print(f"\n[문제 {idx}]")
        
        # LaTeX 검사
        question = prob.get("question", "")
        if '$' in question and question.count('$') % 2 != 0:
            issues.append(f"문제 {idx}: LaTeX 수식 괄호 불일치")
            print("[LaTeX] 오류: 수식 괄호 불일치")
        else:
            print("[LaTeX] 정상")
        
        print(f"[내용 길이] {len(question)}자")
        
        # 유형 확인
        answer_type = prob.get("answer_type", "")
        print(f"[유형] {answer_type}")
        
        if answer_type == "multiple_choice":
            options = prob.get("options", [])
            print(f"[선택지 수] {len(options)}개")
            if len(options) == 5:
                print("[선택지] 정상")
            else:
                issues.append(f"문제 {idx}: 선택지 수 오류 ({len(options)}개)")
                print(f"[선택지] 오류: {len(options)}개 (5개여야 함)")
    
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


def save_for_deepseek(problems, output_dir, base_filename):
    """딥시크용 CSV/JSON 저장"""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # CSV 저장
    csv_path = output_path / f"{base_filename}_deepseek.csv"
    with open(csv_path, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['index', 'page', 'topic', 'question', 
                                                'point', 'answer_type', 'options'])
        writer.writeheader()
        for prob in problems:
            row = prob.copy()
            if 'options' in row:
                row['options'] = ' | '.join(row['options']) if row['options'] else ''
            writer.writerow(row)
    
    print(f"\n[CSV 저장 완료] {csv_path}")
    
    # JSON 저장
    json_path = output_path / f"{base_filename}_deepseek.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(problems, f, ensure_ascii=False, indent=2)
    
    print(f"[JSON 저장 완료] {json_path}")
    
    return csv_path, json_path


def main(latex_content, output_dir, base_filename, debug=False):
    """메인 실행 함수"""
    print("=" * 60)
    print("[LaTeX → CSV 변환]")
    print("=" * 60)
    
    # 1단계: LaTeX 읽기
    print(f"\n[1단계] LaTeX 내용 읽기 완료 ({len(latex_content)}자)")
    
    # 2단계: 문제 추출
    print("\n[2단계] 문제 추출 중...")
    problems = extract_problems_from_latex(latex_content, debug=debug)
    print(f"[완료] {len(problems)}개 문제 추출됨")
    
    # 3단계: 검토
    print("\n[3단계] 문제 검토 중...")
    is_valid = review_problems(problems)
    
    if not is_valid:
        print("\n[경고] 일부 문제에 오류가 있습니다. 확인 후 저장하세요.")
        response = input("그래도 저장하시겠습니까? (y/n): ")
        if response.lower() != 'y':
            return
    
    # 4단계: 저장
    print("\n[4단계] 딥시크용 파일 저장 중...")
    csv_path, json_path = save_for_deepseek(problems, output_dir, base_filename)
    
    print("\n" + "=" * 60)
    print("[완료] 딥시크가 읽을 수 있는 형태로 저장되었습니다.")
    print("=" * 60)
    print(f"저장 위치: {output_dir}")
    print(f"  - CSV: {csv_path.name}")
    print(f"  - JSON: {json_path.name}")


if __name__ == '__main__':
    # 사용 예시
    # latex_content = """..."""
    # output_dir = r"C:\Users\a\Documents\MathPDF-현우진-수1_2025학년도_현우진_드릴"
    # base_filename = "수1_2025학년도_현우진_드릴_P2_문제"
    # main(latex_content, output_dir, base_filename, debug=True)
    pass
