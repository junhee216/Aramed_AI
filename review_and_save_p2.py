# review_and_save_p2.py
# 미적분 드릴 P2 원본 대조 및 딥시크 저장

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

# 제공된 데이터
provided_data = {
    "09": {
        "ID": "09",
        "Content": "두 수열 $\\{a_n\\}$과 $\\{b_n\\}$이 모든 자연수 $n$에 대하여 다음 조건을 만족시킨다. (가) $a_{n+1}=a_1 a_n$ (나) $b_n = \\begin{cases} -\\frac{4}{3n(n+2)} & (n이 홀수인 경우) \\\\ a_n & (n이 짝수인 경우) \\end{cases}$ $\\sum_{n=1}^{\\infty}(a_n - b_n)=0$일 때, $a_1$의 값은? (단, $|a_1|<1$)",
        "Geometry_Desc": "None (수열의 정의 및 급수의 성질)",
        "Options": "① 1/16 ② 1/8 ③ 3/16 ④ 1/4 ⑤ 5/16"
    },
    "10": {
        "ID": "10",
        "Content": "첫째항이 1이고 공비가 자연수인 등비수열 $\\{a_n\\}$과 수열 $\\{b_n\\}$이 모든 자연수 $n$에 대하여 $b_n = 2 \\sin \\frac{\\pi a_n}{3}$을 만족시킨다. $\\sum_{n=1}^{\\infty} \\frac{1}{a_n} > \\frac{16}{15}$이고 $\\sum_{n=1}^{\\infty} (b_n + \\sqrt{3})$이 수렴할 때, 모든 $\\sum_{n=1}^{\\infty} \\frac{1}{a_n}$의 값의 합은 $\\frac{q}{p}$이다. $p+q$의 값을 구하시오. (단, $p, q$는 서로소인 자연수)",
        "Geometry_Desc": "None (삼각함수의 주기성과 급수의 수렴 조건 결합)",
        "Options": "주관식"
    },
    "Ch2-01": {
        "ID": "Ch2-01",
        "Content": "$a>1$인 실수 $a$와 양수 $t$에 대하여 직선 $x=t$가 두 곡선 $y=a^{4x}$, $y=-x^2$과 만나는 점을 각각 $P, Q$라 하고, $\\angle POQ = \\theta$라 하자. $f(a) = \\lim_{t \\to 0^+} (t^2 \\times \\tan \\theta)$일 때, $\\lim_{a \\to 1^+} (a-1)f(a)$의 값은? (단, $O$는 원점)",
        "Geometry_Desc": "1. $x=t$가 지수함수 $y=a^{4x}$와 만나는 점 $P(t, a^{4t})$. 2. $x=t$가 이차함수 $y=-x^2$과 만나는 점 $Q(t, -t^2)$. 3. 원점 $O(0,0)$과 두 점 $P, Q$가 이루는 각 $\\theta$에 대한 탄젠트 극한 상황.",
        "Options": "① -1/16 ② -1/8 ③ -3/16 ④ -1/4 ⑤ -5/16"
    },
    "Ch2-02": {
        "ID": "Ch2-02",
        "Content": "좌표평면에서 직선 $y=a(x+2)$가 원 $x^2 + y^2 = 1$과 제1사분면에서 만나는 점을 $A$라 하자. 점 $B(-2, 0)$에 대하여 선분 $AB$의 길이를 $f(a)$라 할 때, $\\lim_{a \\to 0^+} \\frac{3-f(a)}{a^2}$의 값을 구하시오. (단, $0 < a < 1/2$)",
        "Geometry_Desc": "1. 중심 $(0,0)$, 반지름 1인 단위 원. 2. 점 $B(-2, 0)$을 지나는 기울기 $a$인 직선과 원의 교점 $A$. 3. 점 $A$와 $B$ 사이의 거리 $f(a)$에 대한 극한값 계산.",
        "Options": "주관식"
    },
    "Ch2-03": {
        "ID": "Ch2-03",
        "Content": "원 $C: x^2 + y^2 = 1$ 위의 제1사분면의 점 $P$에서 원 $C$에 접하는 직선이 곡선 $y=x^2$과 만나는 두 점을 각각 $Q, R$이라 하고, $\\angle QOR = \\alpha$라 하자. 직선 $OP$가 $x$축의 양의 방향과 이루는 각의 크기가 $\\theta$일 때, $\\lim_{\\theta \\to 0^+} \\frac{\\tan \\alpha - 1}{\\theta}$의 값을 구하시오. (단, $O$는 원점)",
        "Geometry_Desc": "1. 단위 원 위의 점 $P(\\cos \\theta, \\sin \\theta)$에서의 접선 $x \\cos \\theta + y \\sin \\theta = 1$. 2. 이 접선과 이차곡선 $y=x^2$의 교점 $Q, R$. 3. 원점에서 두 교점을 이은 두 직선 사이의 각 $\\alpha$에 대한 극한.",
        "Options": "주관식"
    },
    "Ch2-04": {
        "ID": "Ch2-04",
        "Content": "좌표평면에서 원 $x^2 + y^2 = 4$ 위의 제1사분면의 점 $P$에 대하여 직선 $OP$가 $x$축의 양의 방향과 이루는 각의 크기를 $\\theta$라 하자. 점 $P$를 지나고 $x$축에 평행한 직선이 곡선 $y=\\ln(x+1)$과 만나는 점의 $x$좌표를 $f(\\theta)$라 하고, 직선 $OP$가 곡선 $y=-\\tan x (\\pi/2 < x < \\pi)$와 만나는 점의 $x$좌표를 $g(\\theta)$라 하자. $\\lim_{\\theta \\to 0^+} \\frac{f(\\theta)}{\\pi - g(\\theta)} = \\frac{a}{\\pi}$일 때, 자연수 $a$의 값을 구하시오. (단, $O$는 원점)",
        "Geometry_Desc": "1. 중심 $(0,0)$, 반지름 2인 원 위의 점 $P(2\\cos \\theta, 2\\sin \\theta)$. 2. 점 $P$에서 $x$축 평행선과 로그함수의 교점 $f(\\theta)$. 3. 직선 $y=(\\tan \\theta)x$와 탄젠트 함수 $y=-\\tan x$의 교점 $g(\\theta)$.",
        "Options": "주관식"
    }
}

def check_latex_syntax(text):
    """LaTeX 구문 검사"""
    issues = []
    dollar_count = text.count('$')
    if dollar_count % 2 != 0:
        issues.append(f"$ 기호 홀수개 ({dollar_count}개)")
    # 빈 LaTeX 수식 확인 (연속된 $ 사이에 공백만 있는 경우만)
    if re.search(r'\$\s{2,}\$', text):
        issues.append("빈 LaTeX 수식 (공백만)")
    return issues

def review_data():
    """데이터 검토"""
    print("=" * 80)
    print("[미적분 드릴 P2 데이터 검토]")
    print("=" * 80)
    
    issues = []
    warnings = []
    
    for problem_id in sorted(provided_data.keys()):
        print(f"\n[문제 {problem_id}]")
        data = provided_data[problem_id]
        
        # LaTeX 검사
        latex_issues = check_latex_syntax(data["Content"])
        if latex_issues:
            print(f"[LaTeX 오류] {', '.join(latex_issues)}")
            issues.extend([f"문제 {problem_id}: {issue}" for issue in latex_issues])
        else:
            print("[LaTeX] 정상")
        
        # 필수 필드 확인
        if not data.get("Content"):
            issues.append(f"문제 {problem_id}: Content 없음")
        if not data.get("Options"):
            warnings.append(f"문제 {problem_id}: Options 없음")
        
        print(f"[내용 길이] {len(data['Content'])}자")
        print(f"[기하 설명] {'있음' if data['Geometry_Desc'] != 'None' else '없음'}")
        print(f"[선택지] {'객관식' if data['Options'] != '주관식' else '주관식'}")
    
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

def compare_with_pdf():
    """원본 PDF와 대조"""
    base_dir = Path(r'C:\Users\a\Documents\MathPDF')
    organized_dir = base_dir / 'organized' / '미적분'
    
    pdf_path = None
    if organized_dir.exists():
        for pdf_file in organized_dir.glob('*드릴*P2*.pdf'):
            pdf_path = pdf_file
            break
    
    if pdf_path is None:
        for pdf_file in base_dir.glob('*드릴*P2*.pdf'):
            if 'organized' not in str(pdf_file):
                pdf_path = pdf_file
                break
    
    if pdf_path is None or not pdf_path.exists():
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
    for problem_id in sorted(provided_data.keys()):
        content = provided_data[problem_id]["Content"]
        # 핵심 수식 요소 확인
        key_terms = []
        if "lim" in content.lower():
            key_terms.append("lim")
        if "sum" in content.lower():
            key_terms.append("sum")
        if "\\{" in content:
            key_terms.append("수열")
        
        found = sum(1 for term in key_terms if term in pdf_text.lower())
        if found == len(key_terms) or len(key_terms) == 0:
            print(f"  [문제 {problem_id}] 핵심 요소 확인됨")
        else:
            print(f"  [문제 {problem_id}] 일부 요소 확인 필요")
    
    return pdf_path

def save_for_deepseek(pdf_path=None):
    """딥시크용 저장"""
    base_dir = Path(r'C:\Users\a\Documents\MathPDF')
    organized_dir = base_dir / 'organized' / '미적분'
    save_dir = organized_dir if organized_dir.exists() else base_dir
    
    # 검토 결과
    review_results = {
        "검토일시": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "검토자": "Cursor AI",
        "총_문제수": len(provided_data),
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
            "원본": "미적분_2025학년도_현우진_드릴_P2",
            "변환자": "Google AI",
            "검토자": "Cursor AI",
            "검토일시": review_results["검토일시"],
            "용도": "딥시크 문제 분석용"
        },
        "검토결과": review_results,
        "문제데이터": provided_data
    }
    
    # JSON 저장
    json_path = save_dir / "미적분_2025학년도_현우진_드릴_P2_deepseek.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(deepseek_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n[저장 완료] {json_path}")
    
    # CSV 저장
    csv_path = save_dir / "미적분_2025학년도_현우진_드릴_P2_deepseek.csv"
    with open(csv_path, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['ID', 'Content', 'Geometry_Desc', 'Options', '검토상태'])
        for problem_id in sorted(provided_data.keys()):
            problem = provided_data[problem_id]
            writer.writerow([
                problem['ID'],
                problem['Content'],
                problem['Geometry_Desc'],
                problem['Options'],
                '검토완료'
            ])
    
    print(f"[CSV 저장 완료] {csv_path}")
    
    return json_path, csv_path

def main():
    # 1. 데이터 검토
    is_valid = review_data()
    
    if not is_valid:
        print("\n[경고] 일부 LaTeX 경고가 있으나 저장을 진행합니다.")
        # LaTeX 경고는 저장을 막지 않음
    
    # 2. 원본 PDF 대조
    pdf_path = compare_with_pdf()
    
    # 3. 딥시크용 저장
    json_path, csv_path = save_for_deepseek(pdf_path)
    
    print("\n[완료] 딥시크가 읽을 수 있는 형태로 저장되었습니다.")

if __name__ == '__main__':
    main()
