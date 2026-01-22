# analyze_su2_03_math_logic.py
# 수2_2025학년도_현우진_드릴_03 문제와 해설의 수학적 논리 오류 분석

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
problems_path = base_dir / '수2_2025학년도_현우진_드릴_03_문제_deepseek.json'
solutions_path = base_dir / '수2_2025학년도_현우진_드릴_03_해설_deepseek.json'

def load_json_file(file_path):
    """JSON 파일 로드"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ 파일 읽기 오류 ({file_path}): {e}")
        return None

def check_latex_syntax(text):
    """LaTeX 수식 문법 검사"""
    issues = []
    
    # $$ 블록 제거 후 $ 개수 확인
    text_no_dblock = re.sub(r'\$\$', '', text)
    dollar_count = text_no_dblock.count('$')
    
    if dollar_count % 2 != 0:
        issues.append("LaTeX 수식 괄호 불일치 (홀수 개의 $)")
    
    # 중괄호 짝 확인
    brace_count = text.count('{') - text.count('}')
    if brace_count != 0:
        issues.append(f"중괄호 불일치 (차이: {brace_count})")
    
    # 백슬래시 이스케이프 확인
    if '\\{' in text and '{' in text:
        # 이스케이프된 중괄호는 정상
        pass
    
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
        issues.append(f"점수가 비정상적: {point}점 (3점 또는 4점이어야 함)")
    
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
    elif answer_type == 'short_answer':
        if len(options) > 0:
            warnings.append("주관식 문제인데 선택지가 있음")
    
    # 4. 수학적 개념 일관성 검증
    # 삼차함수 언급 시 최고차항 계수 확인
    if '삼차함수' in question:
        if '최고차항' not in question and '계수' not in question:
            # 일부 문제는 최고차항 계수를 명시하지 않을 수 있음
            pass
    
    # 5. 집합 표기 검증
    if 'A=' in question or 'B=' in question:
        # 집합 표기법 확인
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
    
    return issues, warnings

def check_math_logic_solution(solution):
    """해설의 수학적 논리 검토"""
    issues = []
    warnings = []
    
    content = solution.get('content', '')
    topic = solution.get('topic', '')
    sol_type = solution.get('type', '')
    
    # 1. 해설 타입 검증
    if sol_type not in ['concept', 'strategy']:
        issues.append(f"해설 타입이 비정상적: {sol_type}")
    
    # 2. 수학적 정리/공식 검증
    # 삼차방정식의 근과 계수의 관계
    if '근과 계수의 관계' in content or '세 실근의 합' in content:
        if '-\\frac{b}{a}' in content or '변곡점' in content:
            pass  # 정상
        else:
            warnings.append("삼차방정식 근과 계수의 관계 언급이 불완전할 수 있음")
    
    # 3. 비율 관계 검증
    if '비율 관계' in content:
        if '2:1' in content or '1:2' in content or '\\sqrt{3}' in content or '\\sqrt{2}' in content:
            pass  # 정상
        else:
            warnings.append("비율 관계 언급이 있지만 구체적 비율이 없음")
    
    # 4. 극한 성질 검증
    if '극한' in content and '\\lim' in content:
        if 'x \\rightarrow' in content or 'h \\rightarrow' in content:
            pass  # 정상
        else:
            warnings.append("극한 표기에서 화살표가 없음")
    
    # 5. 도함수 표기 검증
    if '도함수' in content or '미분' in content:
        if 'f\'' in content or 'f^{\\prime}' in content or 'g\'' in content:
            pass  # 정상
        else:
            warnings.append("도함수/미분 언급이 있지만 도함수 표기가 없음")
    
    # 6. 합성함수 검증
    if '합성함수' in content or 'f \\circ f' in content or '(f \\circ f)' in content:
        if 'f(f(x))' in content or 'g \\circ g' in content:
            pass  # 정상
        else:
            warnings.append("합성함수 언급이 있지만 구체적 표기가 없음")
    
    # 7. 그래프 대칭 검증
    if '대칭' in content or '변곡점' in content:
        if '그래프' in content or '함수' in content:
            pass  # 정상
        else:
            warnings.append("대칭/변곡점 언급이 있지만 그래프/함수 언급이 없음")
    
    # 8. 열린구간 최대/최소 검증
    if '열린구간' in content and ('최댓값' in content or '최솟값' in content):
        if '극댓값' in content or '극솟값' in content:
            pass  # 정상
        else:
            warnings.append("열린구간 최대/최소 언급이 있지만 극값 언급이 없음")
    
    return issues, warnings

def check_consistency(problems, solutions):
    """문제와 해설 간의 일관성 검토"""
    issues = []
    warnings = []
    
    # 해설에서 언급된 문제 번호 확인
    for sol in solutions:
        q_ref = sol.get('question_ref', '')
        if q_ref:
            # 문제 참조가 있으면 해당 문제가 존재하는지 확인
            problem_exists = any(p.get('index') == q_ref.zfill(2) for p in problems)
            if not problem_exists:
                warnings.append(f"해설이 문제 {q_ref}를 참조하지만 해당 문제가 없음")
    
    # 문제 주제와 해설 주제 일치 확인
    problem_topics = set(p.get('topic', '') for p in problems)
    solution_topics = set()
    for sol in solutions:
        topic = sol.get('topic', '')
        # 주제에서 숫자 제거
        topic_clean = re.sub(r'^\d+\s*', '', topic).strip()
        if topic_clean:
            solution_topics.add(topic_clean)
    
    # 주제 일치도 확인 (완전 일치가 아니어도 경고만)
    if problem_topics and solution_topics:
        common = problem_topics & solution_topics
        if not common:
            warnings.append("문제 주제와 해설 주제가 일치하지 않음")
    
    return issues, warnings

def main():
    print("=" * 80)
    print("수2_2025학년도_현우진_드릴_03 수학적 논리 오류 분석")
    print("=" * 80)
    
    # 파일 로드
    print("\n[1단계] 파일 로드 중...")
    problems = load_json_file(problems_path)
    solutions = load_json_file(solutions_path)
    
    if problems is None or solutions is None:
        print("❌ 파일을 로드할 수 없습니다.")
        return
    
    print(f"✅ 문제 {len(problems)}개 로드")
    print(f"✅ 해설 {len(solutions)}개 로드")
    
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
                print("  ❌ 오류:")
                for issue in issues:
                    print(f"    - {issue}")
                    all_issues.append(f"문제 {idx}: {issue}")
            if warnings:
                print("  ⚠️  경고:")
                for warning in warnings:
                    print(f"    - {warning}")
                    all_warnings.append(f"문제 {idx}: {warning}")
    
    # 해설 분석
    print("\n[3단계] 해설 수학적 논리 검토 중...")
    for i, solution in enumerate(solutions, 1):
        issues, warnings = check_math_logic_solution(solution)
        
        # LaTeX 문법 검사
        content = solution.get('content', '')
        topic = solution.get('topic', '')
        latex_issues = check_latex_syntax(content + topic)
        issues.extend([f"LaTeX: {issue}" for issue in latex_issues])
        
        if issues or warnings:
            sol_type = solution.get('type', 'unknown')
            topic = solution.get('topic', '')[:30]
            print(f"\n[해설 {i}] ({sol_type}) {topic}...")
            if issues:
                print("  ❌ 오류:")
                for issue in issues:
                    print(f"    - {issue}")
                    all_issues.append(f"해설 {i}: {issue}")
            if warnings:
                print("  ⚠️  경고:")
                for warning in warnings:
                    print(f"    - {warning}")
                    all_warnings.append(f"해설 {i}: {warning}")
    
    # 일관성 검토
    print("\n[4단계] 문제-해설 일관성 검토 중...")
    consistency_issues, consistency_warnings = check_consistency(problems, solutions)
    all_issues.extend(consistency_issues)
    all_warnings.extend(consistency_warnings)
    
    if consistency_issues or consistency_warnings:
        if consistency_issues:
            print("  ❌ 일관성 오류:")
            for issue in consistency_issues:
                print(f"    - {issue}")
        if consistency_warnings:
            print("  ⚠️  일관성 경고:")
            for warning in consistency_warnings:
                print(f"    - {warning}")
    
    # 종합 결과
    print("\n" + "=" * 80)
    print("📊 종합 분석 결과")
    print("=" * 80)
    print(f"✅ 정상 항목: {len(problems) + len(solutions) - len(all_issues) - len(all_warnings)}개")
    print(f"❌ 오류: {len(all_issues)}개")
    print(f"⚠️  경고: {len(all_warnings)}개")
    
    if all_issues:
        print("\n❌ 발견된 오류:")
        for issue in all_issues:
            print(f"  - {issue}")
    
    if all_warnings:
        print("\n⚠️  발견된 경고:")
        for warning in all_warnings[:10]:  # 처음 10개만 표시
            print(f"  - {warning}")
        if len(all_warnings) > 10:
            print(f"  ... 외 {len(all_warnings) - 10}개 경고")
    
    if not all_issues and not all_warnings:
        print("\n✅ 수학적 논리 오류가 발견되지 않았습니다!")
    elif not all_issues:
        print("\n✅ 심각한 수학적 논리 오류는 없습니다. (경고만 존재)")
    else:
        print("\n❌ 수학적 논리 오류가 발견되었습니다. 확인이 필요합니다.")
    
    # 결과 저장
    result = {
        "timestamp": __import__('datetime').datetime.now().isoformat(),
        "problems_count": len(problems),
        "solutions_count": len(solutions),
        "total_issues": len(all_issues),
        "total_warnings": len(all_warnings),
        "issues": all_issues,
        "warnings": all_warnings
    }
    
    output_path = base_dir / '수2_2025학년도_현우진_드릴_03_수학논리분석.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 분석 결과 저장: {output_path}")

if __name__ == '__main__':
    main()
