# solution_utils.py
# 해설(solution) 처리 관련 재사용 가능한 유틸리티 함수들

import re
import csv
import json
from pathlib import Path
from datetime import datetime


def review_solutions(solutions, check_math_logic=True):
    """
    해설 데이터 검토 (수학적 논리 포함)
    
    Args:
        solutions: 해설 리스트
        check_math_logic: 수학적 논리 검사 여부
    
    Returns:
        검토 통과 여부 (bool)
    """
    print("=" * 60)
    print("[해설 데이터 검토]")
    print("=" * 60)
    
    issues = []
    math_errors = []
    
    for i, sol in enumerate(solutions, 1):
        sol_type = sol.get("type", "")
        print(f"\n[해설 {i}] 타입: {sol_type}")
        
        if sol_type == "concept":
            topic = sol.get("topic", "")
            print(f"[주제] {topic}")
        elif sol_type == "strategy":
            q_ref = sol.get("question_ref", "")
            print(f"[문제 참조] {q_ref}")
        
        content = sol.get("content", "")
        print(f"[내용 길이] {len(content)}자")
        
        # LaTeX 검사
        dollar_count = content.count('$')
        content_no_dblock = re.sub(r'\$\$', '', content)
        dollar_count_single = content_no_dblock.count('$')
        
        topic_dollar = sol.get("topic", "").count('$')
        topic_no_dblock = re.sub(r'\$\$', '', sol.get("topic", ""))
        topic_dollar_single = topic_no_dblock.count('$')
        
        total_dollar_single = dollar_count_single + topic_dollar_single
        
        if total_dollar_single % 2 != 0:
            issues.append(f"해설 {i}: LaTeX 수식 괄호 불일치")
            print("[LaTeX] 오류: 수식 괄호 불일치")
        else:
            print("[LaTeX] 정상")
        
        # 수학적 논리 검토
        if check_math_logic:
            # 삼각함수 범위 확인
            if 'sin' in content or 'cos' in content:
                if 'sin' in content and ('> 1' in content or '< -1' in content):
                    if '최댓값' not in content and '최솟값' not in content and '범위' not in content:
                        math_errors.append(f"해설 {i}: sin 함수 범위 오류 가능성")
            
            # 코사인법칙 공식 확인
            if '코사인법칙' in content or 'cos' in content:
                if 'c^{2}' in content or 'c^2' in content:
                    if 'a^{2}' in content or 'a^2' in content:
                        if 'b^{2}' in content or 'b^2' in content:
                            if '2ab' not in content and '2 a b' not in content:
                                math_errors.append(f"해설 {i}: 코사인법칙 공식 구조 확인 필요")
            
            # 사인법칙 공식 확인
            if '사인법칙' in content:
                if 'sin' in content and '/' in content:
                    pass  # 공식 구조 정상
    
    print("\n" + "=" * 60)
    print("[검토 결과]")
    print("=" * 60)
    print(f"[총 해설 수] {len(solutions)}개")
    
    concept_count = sum(1 for s in solutions if s.get("type") == "concept")
    strategy_count = sum(1 for s in solutions if s.get("type") == "strategy")
    print(f"[개념] {concept_count}개")
    print(f"[전략] {strategy_count}개")
    
    if issues:
        print("\n[LaTeX 오류]")
        for issue in issues:
            print(f"  - {issue}")
    
    if math_errors:
        print("\n[수학적 논리 오류 가능성]")
        for error in math_errors:
            print(f"  - {error}")
    
    if not issues and not math_errors:
        print("\n[오류] 없음")
        print("[수학적 논리] 정상")
    
    return len(issues) == 0 and len(math_errors) == 0


def save_solutions_for_deepseek(solutions, output_dir, base_filename):
    """
    해설을 딥시크용 CSV/JSON으로 저장
    
    Args:
        solutions: 해설 리스트
        output_dir: 출력 디렉토리
        base_filename: 기본 파일명 (확장자 제외)
    
    Returns:
        (csv_path, json_path) 튜플
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # CSV 저장
    csv_path = output_path / f"{base_filename}_deepseek.csv"
    with open(csv_path, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['type', 'topic', 'question_ref', 'content'])
        for solution in solutions:
            writer.writerow([
                solution.get('type', ''),
                solution.get('topic', ''),
                solution.get('question_ref', ''),
                solution.get('content', '')
            ])
    
    print(f"\n[CSV 저장 완료] {csv_path}")
    
    # JSON 저장
    json_path = output_path / f"{base_filename}_deepseek.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(solutions, f, ensure_ascii=False, indent=2)
    
    print(f"[JSON 저장 완료] {json_path}")
    
    return csv_path, json_path
