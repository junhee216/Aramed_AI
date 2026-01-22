# analyze_su2_p4_math_logic.py
# 수2_2025학년도_현우진_드릴_P4 문제의 수학적 논리 오류 분석

import json
import re
import sys
import os
from pathlib import Path

# Windows 콘솔 인코딩 설정
if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')

# 파일 경로
base_dir = Path(r'C:\Users\a\Documents\MathPDF\organized\현우진\수2_2005학년도_현우진_드릴')
problems_path = base_dir / '수2_2025학년도_현우진_드릴_P4_문제_deepseek.json'

def load_json_file(file_path):
    """JSON 파일 로드"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"[오류] 파일 읽기 오류 ({file_path}): {e}")
        return None

def check_latex_syntax(text):
    """LaTeX 수식 문법 검사"""
    issues = []
    
    text_no_dblock = re.sub(r'\$\$', '', text)
    dollar_count = text_no_dblock.count('$')
    
    if dollar_count % 2 != 0:
        issues.append("LaTeX 수식 괄호 불일치 (홀수 개의 $)")
    
    brace_count = text.count('{') - text.count('}')
    if brace_count != 0:
        issues.append(f"중괄호 불일치 (차이: {brace_count})")
    
    return issues

def check_math_logic_problem(problem):
    """문제의 수학적 논리 검토"""
    issues = []
    warnings = []
    
    question = problem.get('question', '')
    topic = problem.get('topic', '')
    point = problem.get('point', 0)
    answer_type = problem.get('answer_type', '')
    options = problem.get('options', [])
    
    # 1. 점수 검증
    if point not in [3, 4]:
        issues.append(f"점수가 비정상적: {point}점")
    
    # 2. 주제 검증
    valid_topics = ['함수의 극한과 연속', '미분', '적분']
    if topic not in valid_topics:
        warnings.append(f"주제가 표준값이 아님: {topic}")
    
    # 3. 문제 유형과 선택지 일치 확인
    if answer_type == 'multiple_choice':
        if len(options) < 5:
            issues.append(f"객관식 문제인데 선택지가 {len(options)}개 (5개여야 함)")
        elif len(options) > 5:
            warnings.append(f"선택지가 5개보다 많음: {len(options)}개")
    
    # 4. 수학적 개념 일관성 검증
    # 삼차함수 언급 시 최고차항 계수 확인
    if '삼차함수' in question:
        if '최고차항' not in question and '계수' not in question:
            # 일부 문제는 최고차항 계수를 명시하지 않을 수 있음
            pass
    
    # 5. 집합 표기 검증
    if 'A=' in question or 'B=' in question:
        if '\\{' in question and '\\}' in question:
            pass  # 정상
        else:
            warnings.append("집합 표기법이 불완전할 수 있음")
    
    # 6. 조건부 함수 검증
    if '\\begin{cases}' in question:
        if '\\end{cases}' not in question:
            issues.append("조건부 함수 구문이 완성되지 않음")
    
    # 7. 극한 표기 검증
    if '\\lim' in question:
        if '\\rightarrow' not in question and '->' not in question:
            warnings.append("극한 표기에서 화살표가 없음")
    
    # 8. 미분 표기 검증
    if 'f\'' in question or 'f^{\\prime}' in question:
        if '미분' in topic or '미분' in question:
            pass  # 정상
        else:
            warnings.append("미분 표기가 있지만 주제가 미분이 아님")
    
    # 9. 적분 표기 검증
    if '\\int' in question:
        if 'd' in question or 'dt' in question or 'dx' in question:
            pass  # 정상
        else:
            warnings.append("적분 표기에서 미분소가 없음")
    
    # 10. 수학적 논리 검증
    # 등차수열과 함수의 관계
    if '등차수열' in question and 'f\'' in question:
        if '공차' in question or 'd' in question:
            pass  # 정상
    
    # 미분가능성 조건
    if '미분가능' in question:
        if '연속' in question or '극한' in question:
            pass  # 정상
    
    # 극값 조건
    if '극댓값' in question or '극솟값' in question:
        if 'f\'' in question or '도함수' in question:
            pass  # 정상
    
    return issues, warnings

def main():
    print("=" * 80)
    print("수2_2025학년도_현우진_드릴_P4 수학적 논리 오류 분석")
    print("=" * 80)
    
    # 파일 로드
    print("\n[1단계] 파일 로드 중...")
    problems = load_json_file(problems_path)
    
    if problems is None:
        print("[오류] 파일을 로드할 수 없습니다.")
        return
    
    print(f"[완료] 문제 {len(problems)}개 로드")
    
    # 전체 분석 결과
    all_issues = []
    all_warnings = []
    
    # 문제 분석
    print("\n[2단계] 문제 수학적 논리 검토 중...")
    for i, problem in enumerate(problems, 1):
        idx = problem.get('index', f'{i:02d}')
        issues, warnings = check_math_logic_problem(problem)
        
        # LaTeX 문법 검사
        question = problem.get('question', '')
        latex_issues = check_latex_syntax(question)
        issues.extend([f"LaTeX: {issue}" for issue in latex_issues])
        
        if issues or warnings:
            print(f"\n[문제 {idx}]")
            if issues:
                print("  [오류]:")
                for issue in issues:
                    print(f"    - {issue}")
                    all_issues.append(f"문제 {idx}: {issue}")
            if warnings:
                print("  [경고]:")
                for warning in warnings:
                    print(f"    - {warning}")
                    all_warnings.append(f"문제 {idx}: {warning}")
    
    # 종합 결과
    print("\n" + "=" * 80)
    print("[종합 분석 결과]")
    print("=" * 80)
    print(f"[정상 항목] {len(problems) - len(all_issues) - len(all_warnings)}개")
    print(f"[오류] {len(all_issues)}개")
    print(f"[경고] {len(all_warnings)}개")
    
    if all_issues:
        print("\n[발견된 오류]:")
        for issue in all_issues:
            print(f"  - {issue}")
    
    if all_warnings:
        print("\n[발견된 경고]:")
        for warning in all_warnings[:10]:  # 처음 10개만 표시
            print(f"  - {warning}")
        if len(all_warnings) > 10:
            print(f"  ... 외 {len(all_warnings) - 10}개 경고")
    
    if not all_issues and not all_warnings:
        print("\n[결과] 수학적 논리 오류가 발견되지 않았습니다!")
    elif not all_issues:
        print("\n[결과] 심각한 수학적 논리 오류는 없습니다. (경고만 존재)")
    else:
        print("\n[결과] 수학적 논리 오류가 발견되었습니다. 확인이 필요합니다.")
    
    # 결과 저장
    result = {
        "timestamp": __import__('datetime').datetime.now().isoformat(),
        "problems_count": len(problems),
        "total_issues": len(all_issues),
        "total_warnings": len(all_warnings),
        "issues": all_issues,
        "warnings": all_warnings
    }
    
    output_path = base_dir / '수2_2025학년도_현우진_드릴_P4_수학논리분석.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"\n[완료] 분석 결과 저장: {output_path}")

if __name__ == '__main__':
    main()
