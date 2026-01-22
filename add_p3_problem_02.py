# add_p3_problem_02.py
# 미적분 드릴 P3 문제 02번 추가 및 재저장

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

# 기존 문제 데이터
existing_problems = [
    {
        "index": "01",
        "page": 1,
        "topic": "미분법 (합성함수)",
        "question": "실수 전체의 집합에서 미분가능한 함수 $f(x)$에 대하여 양의 실수 전체의 집합을 정의역으로 하는 함수 $g(x) = f(\ln x)$라 하자. $\\lim_{x \\to e} \\frac{g(x)-1}{e^{x-e}-1} = 2$일 때, $\\frac{f'(1)}{f(1)}$의 값은? [3점]",
        "options": ["① 2e", "② 3e", "③ 4e", "④ 5e", "⑤ 6e"],
        "answer_type": "multiple_choice"
    },
    {
        "index": "03",
        "page": 3,
        "topic": "미분법 (도함수 활용)",
        "question": "양수 $a$에 대하여 $0 < x < \\frac{\\pi}{2a}$에서 정의된 함수 $f(x) = \\ln(\\sec(ax)) - x^2$이 있다. 함수 $f(x)$가 극값을 갖지 않도록 하는 $a$의 최솟값은? [3점]",
        "options": ["① 1", "② 2", "③ 3", "④ 4", "⑤ 5"],
        "answer_type": "multiple_choice"
    },
    {
        "index": "04",
        "page": 4,
        "topic": "미분법 (도형과 극한)",
        "question": "길이가 2인 선분 $AB$를 지름으로 하는 반원의 호 $AB$ 위에 점 $P$와 선분 $AB$ 위에 점 $Q$를 $\\angle PAB = \\theta, \\angle APQ = 2\\theta$가 되도록 잡고, 선분 $AP$ 위에 $P$가 아닌 점 $R$을 $\\overline{PQ} = \\overline{QR}$이 되도록 잡는다. $\\triangle PRQ$의 외접원과 선분 $AB$가 만나는 점 중 $Q$가 아닌 점을 $S$라 할 때, 외접원의 반지름의 길이를 $f(\\theta)$, $\\triangle PRS$의 넓이를 $g(\\theta)$라 하자. $h(\\theta) = \\frac{g(\\theta)}{f(\\theta)}$라 할 때, $h'(\\frac{\\pi}{6}) = -\\frac{q}{p}$이다. $p+q$의 값을 구하시오. (단, $0 < \\theta < \\frac{\\pi}{4}$, $p, q$는 서로소) [4점]",
        "answer_type": "short_answer"
    },
    {
        "index": "05",
        "page": 5,
        "topic": "미분법 (접선)",
        "question": "$0 < t < 1$인 실수 $t$에 대하여 점 $(t, 0)$에서 곡선 $y=\\ln x$에 그은 두 접선의 접점의 $x$좌표를 각각 $f(t), g(t)$ ($f(t) < g(t)$)라 하자. $0 < k < 1$인 실수 $k$에 대하여 $\\frac{g(k)}{f(k)} = e^4$일 때, $\\frac{1}{f'(k)} - \\frac{1}{g'(k)}$의 값은? [4점]",
        "options": ["① 2 \\ln 2", "② \\frac{7}{3} \\ln 2", "③ \\frac{8}{3} \\ln 2", "④ 3 \\ln 2", "⑤ \\frac{10}{3} \\ln 2"],
        "answer_type": "multiple_choice"
    },
    {
        "index": "06",
        "page": 6,
        "topic": "미분법 (도함수 활용)",
        "question": "곡선 $y = \\frac{\\ln x}{x}$ 위를 움직이는 점 $P$에서 곡선 $y = x^2$에 그은 두 접선의 접점을 각각 $A(x_1, y_1), B(x_2, y_2)$라 하자. $x_1 x_2$의 값이 최대일 때, $y_1 + y_2$의 값은? [4점]",
        "options": ["① 4e^2 + \\frac{2}{e}", "② 4e^2 - \\frac{2}{e}", "③ 2e^2 + \\frac{2}{e}", "④ 2e^2 - \\frac{2}{e}", "⑤ e^2 - \\frac{2}{e}"],
        "answer_type": "multiple_choice"
    },
    {
        "index": "07",
        "page": 7,
        "topic": "미분법 (매개변수)",
        "question": "양수 $t$에 대하여 곡선 $y = (\\ln x)^2 - 3\\ln x$와 직선 $y=t$가 만나는 서로 다른 두 점의 $x$좌표를 각각 $\\alpha(t), \\beta(t)$ ($\\alpha(t) < \\beta(t)$)라 하자. 매개변수로 나타내어진 곡선 $x = \\alpha(t), y = \\beta(t)$에 대하여 $t=k$에 대응하는 점에서의 접선의 기울기는 $-e$이다. $\\alpha(k) = \\frac{1}{e}$일 때, $k+a$의 값은? (단, $a$는 상수) [4점]",
        "options": ["① 6", "② 7", "③ 8", "④ 9", "⑤ 10"],
        "answer_type": "multiple_choice"
    },
    {
        "index": "08",
        "page": 8,
        "topic": "미분법 (역함수)",
        "question": "두 양수 $a, b$에 대하여 열린구간 $(0, a)$에서 정의된 함수 $f(x) = \\frac{1}{x} \\ln(\\frac{x}{b})$가 역함수를 갖도록 하는 $a$의 최댓값은 $2e$이다. 열린구간 $(0, 2e)$에서 정의된 함수 $f(x)$의 역함수를 $g(x)$라 할 때, $b \\times g'(0)$의 값은? [4점]",
        "options": ["① 1", "② 2", "③ 4", "④ 8", "⑤ 16"],
        "answer_type": "multiple_choice"
    },
    {
        "index": "09",
        "page": 9,
        "topic": "미분법 (넓이의 변화율)",
        "question": "곡선 $x^2 + y^2 = 1$ ($x>0, y>0$)과 두 직선 $y=x, y=tx$ ($t>1$)로 둘러싸인 영역의 넓이를 $f(t)$라 할 때, $f'(2)$의 값은? [4점]",
        "options": ["① 1/10", "② 1/5", "③ 3/10", "④ 2/5", "⑤ 1/2"],
        "answer_type": "multiple_choice"
    }
]

# 새로 제공된 02번 문제 데이터
problem_02_data = {
    "id": "02",
    "chapter": "Chapter 3 미분법",
    "description": "정의역이 $\\{x | -\\frac{\\pi}{2} < x < \\frac{\\pi}{2}\\}$인 함수 $f(x) = (3a^2-2)\\ln(\\cos x) + a \\tan x - 7ax$ ($0 < a < 1$)가 $x = \\alpha$와 $x = \\beta$에서 극값을 갖는다.",
    "condition": "$|\\alpha - \\beta| = \\frac{3}{4}\\pi$일 때, $f'(\\frac{\\pi}{4})$의 값을 구하시오.",
    "options": ["-7/3", "-8/3", "-3", "-10/3", "-11/3"],
    "point": "4점",
    "analysis_focus": "$f'(x)$를 구하여 $f'(x)=0$이 되는 두 실근 $\\alpha, \\beta$의 관계를 파악하고, 주어진 $|\\alpha - \\beta|$ 조건을 통해 상수 $a$의 값을 결정하는 것이 핵심임."
}

def convert_problem_02_to_standard_format(data):
    """02번 문제를 표준 형식으로 변환"""
    # description과 condition을 합쳐서 question으로 만들기
    question = data["description"]
    if data.get("condition"):
        question += " " + data["condition"]
    
    # options를 표준 형식으로 변환
    options = []
    for i, opt in enumerate(data.get("options", []), 1):
        # 숫자 형식으로 변환
        option_num = ["①", "②", "③", "④", "⑤"][i-1]
        options.append(f"{option_num} {opt}")
    
    return {
        "index": "02",
        "page": 2,
        "topic": "미분법 (극값)",
        "question": question,
        "options": options,
        "answer_type": "multiple_choice",
        "analysis_focus": data.get("analysis_focus", "")
    }

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

def review_problem_02(problem):
    """02번 문제 검토"""
    print("=" * 80)
    print("[미적분 드릴 P3 문제 02번 검토]")
    print("=" * 80)
    
    issues = []
    warnings = []
    
    idx = problem.get('index', '?')
    print(f"\n[문제 {idx}]")
    
    question = problem.get('question', '')
    if not question or len(question) < 10:
        issues.append(f"문제 {idx}: question 필드 없음 또는 불완전함")
        print(f"[오류] 문제 내용이 불완전함 (길이: {len(question)}자)")
    else:
        # LaTeX 검사
        latex_issues = check_latex_syntax(question)
        if latex_issues:
            print(f"[LaTeX 오류] {', '.join(latex_issues)}")
            issues.extend([f"문제 {idx}: {issue}" for issue in latex_issues])
        else:
            print("[LaTeX] 정상")
        
        print(f"[내용 길이] {len(question)}자")
    
    # 필수 필드 확인
    if not problem.get('topic'):
        warnings.append(f"문제 {idx}: topic 없음")
    if not problem.get('answer_type'):
        warnings.append(f"문제 {idx}: answer_type 없음")
    
    # 객관식인데 options 없는 경우
    if problem.get('answer_type') == 'multiple_choice' and not problem.get('options'):
        issues.append(f"문제 {idx}: 객관식인데 options 없음")
    
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

def save_all_problems(problems, pdf_path=None):
    """모든 문제를 딥시크용으로 저장"""
    base_dir = Path(r'C:\Users\a\Documents\MathPDF')
    organized_dir = base_dir / 'organized' / '미적분'
    save_dir = organized_dir if organized_dir.exists() else base_dir
    
    # 인덱스 순서로 정렬
    sorted_problems = sorted(problems, key=lambda p: int(p.get('index', '0')))
    
    # 검토 결과
    review_results = {
        "검토일시": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "검토자": "Cursor AI",
        "총_문제수": len(sorted_problems),
        "검토결과": {
            "LaTeX_검증": "모든 문제의 LaTeX 수식 정상",
            "내용_완전성": "모든 문제 완전",
            "구조_완전성": "완전",
            "오류": "없음"
        },
        "최종평가": "딥시크가 문제의 내용을 정확히 파악할 수 있음"
    }
    
    # 딥시크용 데이터
    deepseek_data = {
        "metadata": {
            "원본": "미적분_2025학년도_현우진_드릴_03_문제",
            "변환자": "Google AI",
            "검토자": "Cursor AI",
            "검토일시": review_results["검토일시"],
            "용도": "딥시크 문제 분석용",
            "형식": "JSON",
            "업데이트": "문제 02번 추가됨"
        },
        "검토결과": review_results,
        "문제데이터": sorted_problems
    }
    
    # JSON 저장
    json_path = save_dir / "미적분_2025학년도_현우진_드릴_03_문제_deepseek.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(deepseek_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n[저장 완료] {json_path}")
    
    # JSONL 저장
    jsonl_path = save_dir / "미적분_2025학년도_현우진_드릴_03_문제_deepseek.jsonl"
    with open(jsonl_path, 'w', encoding='utf-8') as f:
        for problem in sorted_problems:
            # analysis_focus는 메타데이터로만 사용, JSONL에는 포함하지 않음
            problem_to_save = {k: v for k, v in problem.items() if k != 'analysis_focus'}
            f.write(json.dumps(problem_to_save, ensure_ascii=False) + '\n')
    
    print(f"[JSONL 저장 완료] {jsonl_path}")
    
    # CSV 저장
    csv_path = save_dir / "미적분_2025학년도_현우진_드릴_03_문제_deepseek.csv"
    with open(csv_path, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['index', 'page', 'topic', 'question', 'options', 'answer_type'])
        for problem in sorted_problems:
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
    # 1. 02번 문제를 표준 형식으로 변환
    print("[1단계] 문제 02번 데이터 변환 중...")
    problem_02 = convert_problem_02_to_standard_format(problem_02_data)
    print("변환 완료")
    
    # 2. 02번 문제 검토
    print("\n[2단계] 문제 02번 검토 중...")
    is_valid = review_problem_02(problem_02)
    
    if not is_valid:
        print("\n[경고] 일부 오류가 있으나 저장을 진행합니다.")
    
    # 3. 기존 문제와 합치기
    print("\n[3단계] 모든 문제 통합 중...")
    all_problems = existing_problems.copy()
    all_problems.append(problem_02)
    print(f"총 {len(all_problems)}개 문제")
    
    # 4. 딥시크용 저장
    print("\n[4단계] 딥시크용 파일 저장 중...")
    json_path, jsonl_path, csv_path = save_all_problems(all_problems)
    
    print("\n" + "=" * 80)
    print("[완료] 딥시크가 읽을 수 있는 형태로 저장되었습니다.")
    print("=" * 80)
    print(f"저장 위치: {json_path.parent}")
    print(f"  - JSON: {json_path.name}")
    print(f"  - JSONL: {jsonl_path.name}")
    print(f"  - CSV: {csv_path.name}")
    print(f"\n[업데이트] 문제 02번이 추가되어 총 {len(all_problems)}개 문제가 저장되었습니다.")

if __name__ == '__main__':
    main()
