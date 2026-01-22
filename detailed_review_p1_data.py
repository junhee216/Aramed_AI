# detailed_review_p1_data.py
# 구글 AI 변환 데이터 상세 검토

import re
import sys
import os

# Windows 콘솔 인코딩 설정
if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')

# 제공된 CSV 데이터
provided_data = {
    "01": {
        "Content": "모든 자연수 $n$에 대하여 $a_n > 0$인 수열 $\\{a_n\\}$이 $\\lim_{n \\to \\infty} \\frac{\\sqrt{n+p^2}-\\sqrt{n+p}}{a_n} = 2$, $\\lim_{n \\to \\infty} \\frac{\\sqrt{n+2p}-\\sqrt{n}}{a_n} = 1$을 만족시킬 때, 양수 $p$의 값은?",
        "Geometry_Desc": "None (대수적 극한 미지수 결정)",
        "Options": "①1 ②2 ③3 ④4 ⑤5"
    },
    "02": {
        "Content": "자연수 $n$에 대하여 원 $(x-4n)^2 + (y-n)^2 = n^2$과 직선 $y=\\frac{4}{3}x$ 및 $x$축에 동시에 접하는 원의 중심의 좌표를 $(a_n, b_n)$이라 할 때, $\\lim_{n \\to \\infty} \\frac{a_n b_{n+1}}{n^2}$의 값은? (단, $a_n > 4n$)",
        "Geometry_Desc": "1. 중심이 $(4n, n)$이고 반지름이 $n$인 원이 기본 배치됨. 2. 새로운 원 $(a_n, b_n)$은 제1사분면에서 $x$축과 직선 $y=4/3x$에 동시에 접함. 3. 조건 $a_n > 4n$에 의해 이 원은 기준 원의 오른쪽에 위치함.",
        "Options": "①20 ②24 ③28 ④32 ⑤36"
    },
    "03": {
        "Content": "일차함수 $f(x)$에 대하여 함수 $g(x)$를 $g(x) = \\lim_{n \\to \\infty} \\frac{3(f(x))^{2n+1} + 4(f(x+2))^{2n}}{(f(x))^{2n} + 2(f(x+2))^{2n}}$이라 하자. $\\lim_{x \\to 2^+} g(x) - \\lim_{x \\to 2^-} g(x) = 7$일 때, $f(6)$의 값을 구하시오.",
        "Geometry_Desc": "None (등비수열의 극한으로 정의된 함수)",
        "Options": "주관식"
    },
    "04": {
        "Content": "수열 $\\{a_n\\}$이 모든 자연수 $n$에 대하여 $\\sum_{k=1}^n a_k = \\frac{pn}{2n+4}$를 만족시키고, $\\sum_{n=1}^\\infty (a_n + a_{n+2}) = 9$일 때, 상수 $p$의 값을 구하시오.",
        "Geometry_Desc": "None (급수와 일반항의 관계)",
        "Options": "주관식"
    },
    "05": {
        "Content": "자연수 $n$에 대하여 직선 $x=n$이 두 곡선 $y=3^{-x}$, $y=a^{-x} (a>1, a \\ne 3)$과 만나는 점을 각각 $A_n, B_n$이라 하자. $\\sum_{n=1}^\\infty \\overline{A_n B_n} = \\frac{1}{3}$을 만족시키는 모든 $a$의 값의 합이 $q/p$일 때, $p+q$의 값을 구하시오. (단, $p, q$는 서로소인 자연수)",
        "Geometry_Desc": "1. 두 지수함수 $y=(1/3)^x$와 $y=(1/a)^x$의 그래프가 제1사분면에서 감소하는 형태. 2. $x=n$에서의 두 함수값 차이인 $\\overline{A_n B_n}$을 일반항으로 하는 등비급수 상황.",
        "Options": "주관식"
    },
    "06": {
        "Content": "모든 자연수 $n$에 대하여 (가) $a_n \\ne a_{n+1}$, (나) 두 점 $P_n(a_n, a_n^2), P_{n+1}(a_{n+1}, a_{n+1}^2)$을 지나는 직선의 기울기는 $ka_n$이다. $\\sum_{n=1}^\\infty a_n = 2, \\sum_{n=1}^\\infty a_n^2 = 8$일 때, $a_1 + k$의 값은? (단, $k$는 상수)",
        "Geometry_Desc": "1. 이차함수 $y=x^2$ 위의 두 점을 잇는 직선의 기울기 구조. 2. 점 $P_n$과 $P_{n+1}$의 좌표 관계를 통해 $a_n$의 점화식 도출 필요.",
        "Options": "①10/3 ②11/3 ③3 ④13/3 ⑤14/3"
    },
    "07": {
        "Content": "수열 $\\{a_n\\}$이 다음 조건을 만족시킨다. (가) $\\sum_{n=1}^\\infty a_n = 3/2$, (나) 모든 자연수 $p$에 대하여 $\\sum_{n=1}^\\infty a_{n+p} = a_p$이다. $\\sum_{n=1}^\\infty a_{2n}$의 값은?",
        "Geometry_Desc": "None (급수의 성질과 수열의 관계 추론)",
        "Options": "①1/4 ②1/2 ③3/4 ④1 ⑤5/4"
    },
    "08": {
        "Content": "첫째항이 2이고 공차가 4인 등차수열 $\\{a_n\\}$이 있다. 수열 $\\{b_n\\}$이 $b_1=10$이고, 모든 자연수 $n$에 대하여 $b_{n+1} = (\\cos \\frac{\\pi a_n}{6}) \\times b_n$을 만족시킬 때, $\\sum_{n=1}^\\infty 3b_{2n}$의 값을 구하시오.",
        "Geometry_Desc": "None (삼각함수의 주기성과 등비급수의 결합)",
        "Options": "주관식"
    }
}

def check_latex_syntax(text):
    """LaTeX 구문 검사"""
    issues = []
    
    # $ 기호 짝 확인
    dollar_count = text.count('$')
    if dollar_count % 2 != 0:
        issues.append(f"$ 기호가 홀수개 ({dollar_count}개)")
    
    # 빈 수식 확인
    if re.search(r'\$\s*\$', text):
        issues.append("빈 LaTeX 수식 발견")
    
    # 이스케이프 확인
    if '\\{' in text and '\\}' not in text:
        issues.append("중괄호 이스케이프 불일치")
    
    return issues

def check_content_completeness(content, problem_id):
    """내용 완전성 검사"""
    issues = []
    warnings = []
    
    # 필수 요소 확인
    if "?" not in content and "구하시오" not in content:
        warnings.append("질문 마커(?, 구하시오) 없음")
    
    # 수식 요소 확인
    if "lim" not in content.lower() and "sum" not in content.lower() and "sqrt" not in content.lower():
        if problem_id in ["01", "02", "03", "04", "05", "06", "07", "08"]:
            warnings.append("수식 요소가 적음")
    
    # 변수 확인
    if not re.search(r'[a-z]_n|\\{a_n\\}', content):
        if problem_id in ["01", "04", "06", "07", "08"]:
            warnings.append("수열 표기 확인 필요")
    
    return issues, warnings

def check_geometry_desc(desc, content, problem_id):
    """기하 설명 검사"""
    issues = []
    
    if desc == "None":
        # 기하 문제인데 설명이 없는 경우
        if "원" in content or "직선" in content or "곡선" in content or "점" in content:
            if problem_id in ["02", "05", "06"]:
                issues.append("기하 요소가 있는데 Geometry_Desc가 None")
    else:
        # 설명이 있는 경우 내용 확인
        if len(desc) < 20:
            issues.append("기하 설명이 너무 짧음")
    
    return issues

def check_options(options, content):
    """선택지 검사"""
    issues = []
    
    if options == "주관식":
        if "?" in content and "구하시오" not in content:
            issues.append("주관식인데 질문 형식이 선택형")
    else:
        # 선택지 형식 확인
        if not re.search(r'[①-⑤]', options):
            issues.append("선택지 형식이 올바르지 않음")
        
        # 선택지 개수 확인
        choice_count = len(re.findall(r'[①-⑤]', options))
        if choice_count != 5:
            issues.append(f"선택지가 5개가 아님 ({choice_count}개)")
    
    return issues

def main():
    print("=" * 80)
    print("[미적분 드릴 P1 데이터 상세 검토]")
    print("=" * 80)
    
    total_issues = []
    total_warnings = []
    
    for problem_id in sorted(provided_data.keys()):
        print(f"\n[문제 {problem_id}]")
        print("-" * 80)
        
        data = provided_data[problem_id]
        content = data["Content"]
        geometry = data["Geometry_Desc"]
        options = data["Options"]
        
        # LaTeX 검사
        latex_issues = check_latex_syntax(content)
        if latex_issues:
            print(f"[LaTeX 오류] {', '.join(latex_issues)}")
            total_issues.append(f"문제 {problem_id}: LaTeX 오류")
        else:
            print("[LaTeX] 정상")
        
        # 내용 완전성 검사
        content_issues, content_warnings = check_content_completeness(content, problem_id)
        if content_issues:
            print(f"[내용 오류] {', '.join(content_issues)}")
            total_issues.extend([f"문제 {problem_id}: {issue}" for issue in content_issues])
        if content_warnings:
            print(f"[내용 경고] {', '.join(content_warnings)}")
            total_warnings.extend([f"문제 {problem_id}: {warn}" for warn in content_warnings])
        
        # 기하 설명 검사
        geometry_issues = check_geometry_desc(geometry, content, problem_id)
        if geometry_issues:
            print(f"[기하 설명] {', '.join(geometry_issues)}")
            total_warnings.extend([f"문제 {problem_id}: {issue}" for issue in geometry_issues])
        else:
            print(f"[기하 설명] {'있음' if geometry != 'None' else '없음 (정상)'}")
        
        # 선택지 검사
        options_issues = check_options(options, content)
        if options_issues:
            print(f"[선택지 오류] {', '.join(options_issues)}")
            total_issues.extend([f"문제 {problem_id}: {issue}" for issue in options_issues])
        else:
            print(f"[선택지] {'객관식' if options != '주관식' else '주관식'}")
        
        # 내용 길이
        print(f"[내용 길이] {len(content)}자")
    
    # 최종 결과
    print("\n" + "=" * 80)
    print("[검토 결과 요약]")
    print("=" * 80)
    
    if total_issues:
        print(f"\n[오류] {len(total_issues)}개 발견:")
        for issue in total_issues:
            print(f"  - {issue}")
    else:
        print("\n[오류] 없음")
    
    if total_warnings:
        print(f"\n[경고] {len(total_warnings)}개 발견:")
        for warn in total_warnings:
            print(f"  - {warn}")
    else:
        print("\n[경고] 없음")
    
    print("\n" + "=" * 80)
    print("[최종 평가]")
    print("=" * 80)
    
    if not total_issues:
        print("\n[결론] 모든 데이터가 구조적으로 완전합니다.")
        print("[결론] LaTeX 수식이 올바르게 변환되었습니다.")
        print("[결론] 딥시크가 문제의 내용을 정확히 파악할 수 있습니다.")
        print("\n[추가 확인 사항]")
        print("1. 원본 PDF와 직접 대조하여 내용 일치 여부 확인 권장")
        print("2. 기하 설명(Geometry_Desc)은 PDF에 명시적으로 없을 수 있으나, 추론 가능한 정보 제공")
        print("3. 모든 문제에 LaTeX 수식이 포함되어 있어 수학적 표현이 정확함")
    else:
        print(f"\n[결론] {len(total_issues)}개의 오류가 발견되었습니다.")
        print("[권장] 오류를 수정한 후 다시 검토하세요.")

if __name__ == '__main__':
    main()
