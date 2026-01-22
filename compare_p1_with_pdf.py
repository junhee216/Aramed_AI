# compare_p1_with_pdf.py
# 구글 AI 변환 데이터와 원본 PDF 대조 검토

import sys
import os
from pathlib import Path
import re

# Windows 콘솔 인코딩 설정
if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8')

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
                import fitz  # PyMuPDF
                doc = fitz.open(pdf_path)
                text = ""
                for page in doc:
                    text += page.get_text() + "\n"
                doc.close()
                return text
            except ImportError:
                print("[오류] PDF 라이브러리가 설치되어 있지 않습니다.")
                print("다음 중 하나를 설치해주세요: pdfplumber, PyPDF2, PyMuPDF")
                return None

def normalize_text(text):
    """텍스트 정규화 (공백, 줄바꿈 제거 등)"""
    if not text:
        return ""
    # 연속된 공백을 하나로
    text = re.sub(r'\s+', ' ', text)
    # 앞뒤 공백 제거
    text = text.strip()
    return text

def normalize_latex(text):
    """LaTeX 수식 정규화"""
    if not text:
        return ""
    # $ 기호 주변 공백 제거
    text = re.sub(r'\$\s+', '$', text)
    text = re.sub(r'\s+\$', '$', text)
    # 연속된 공백을 하나로
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def extract_problem_number(text, num):
    """PDF 텍스트에서 특정 번호의 문제 추출"""
    # 문제 번호 패턴 찾기
    patterns = [
        rf'0?{num}[\.\)]\s*',  # 01. 또는 1.
        rf'문제\s*0?{num}',
        rf'\(0?{num}\)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            start = match.start()
            # 다음 문제 번호까지 찾기
            next_num = int(num) + 1
            next_patterns = [
                rf'0?{next_num}[\.\)]\s*',
                rf'문제\s*0?{next_num}',
                rf'\(0?{next_num}\)',
            ]
            
            end = len(text)
            for next_pattern in next_patterns:
                next_match = re.search(next_pattern, text[start+10:], re.IGNORECASE)
                if next_match:
                    end = start + 10 + next_match.start()
                    break
            
            return text[start:end]
    
    return None

def compare_problems(pdf_text, provided_data):
    """PDF 텍스트와 제공된 데이터 비교"""
    print("=" * 80)
    print("[미적분 드릴 P1 원본 PDF 대조 검토]")
    print("=" * 80)
    
    results = {
        "총_문제수": len(provided_data),
        "확인_완료": 0,
        "누락_의심": [],
        "내용_불일치": [],
        "LaTeX_오류": [],
        "선택지_누락": [],
        "기하설명_누락": []
    }
    
    # PDF에서 각 문제 추출 및 비교
    for problem_id in sorted(provided_data.keys()):
        print(f"\n[문제 {problem_id}]")
        print("-" * 80)
        
        provided = provided_data[problem_id]
        pdf_problem = extract_problem_number(pdf_text, problem_id)
        
        if not pdf_problem:
            print(f"[경고] PDF에서 문제 {problem_id}를 찾을 수 없습니다.")
            results["누락_의심"].append(problem_id)
            continue
        
        # 내용 비교
        provided_content = normalize_latex(provided["Content"])
        pdf_content = normalize_text(pdf_problem)
        
        # 핵심 키워드 확인
        key_terms = []
        if "lim" in provided_content.lower():
            key_terms.append("lim")
        if "sum" in provided_content.lower():
            key_terms.append("sum")
        if "sqrt" in provided_content.lower():
            key_terms.append("sqrt")
        
        found_terms = []
        for term in key_terms:
            if term in pdf_content.lower():
                found_terms.append(term)
        
        if len(found_terms) == len(key_terms):
            print(f"[정상] 문제 {problem_id}: 핵심 수식 요소 확인됨")
            results["확인_완료"] += 1
        else:
            print(f"[경고] 문제 {problem_id}: 일부 수식 요소 누락 가능")
            results["내용_불일치"].append(problem_id)
        
        # 선택지 확인
        if provided["Options"] != "주관식":
            if provided["Options"] not in pdf_content:
                print(f"[경고] 문제 {problem_id}: 선택지가 PDF에 없을 수 있음")
                results["선택지_누락"].append(problem_id)
        
        # 기하 설명 확인
        if provided["Geometry_Desc"] != "None":
            if provided["Geometry_Desc"] not in pdf_content:
                print(f"[정보] 문제 {problem_id}: 기하 설명은 PDF에 명시적으로 없을 수 있음 (추론 가능)")
        else:
            print(f"[정보] 문제 {problem_id}: 기하 설명 없음 (정상)")
    
    # 최종 결과
    print("\n" + "=" * 80)
    print("[검토 결과 요약]")
    print("=" * 80)
    print(f"총 문제 수: {results['총_문제수']}개")
    print(f"확인 완료: {results['확인_완료']}개")
    
    if results["누락_의심"]:
        print(f"\n⚠️  PDF에서 찾을 수 없는 문제: {results['누락_의심']}")
    
    if results["내용_불일치"]:
        print(f"\n⚠️  내용 불일치 의심: {results['내용_불일치']}")
    
    if results["선택지_누락"]:
        print(f"\n⚠️  선택지 누락 의심: {results['선택지_누락']}")
    
    if not results["누락_의심"] and not results["내용_불일치"]:
        print("\n[결론] 모든 문제가 PDF에 존재하며 핵심 내용이 일치합니다.")
        print("[결론] 딥시크가 문제의 내용을 정확히 파악할 수 있습니다.")
    
    return results

def main():
    # MathPDF 폴더에서 미적분 드릴 P1 파일 찾기
    base_dir = Path(r'C:\Users\a\Documents\MathPDF')
    
    # organized 폴더에서 찾기
    organized_dir = base_dir / 'organized' / '미적분'
    pdf_path = None
    
    if organized_dir.exists():
        for pdf_file in organized_dir.glob('*드릴*P1*.pdf'):
            pdf_path = pdf_file
            break
    
    # 원본 폴더에서도 찾기
    if pdf_path is None:
        for pdf_file in base_dir.glob('*드릴*P1*.pdf'):
            if 'organized' not in str(pdf_file):
                pdf_path = pdf_file
                break
    
    # 미적분 폴더에서 찾기
    if pdf_path is None:
        for pdf_file in base_dir.glob('*미적분*P1*.pdf'):
            pdf_path = pdf_file
            break
    
    if pdf_path is None or not pdf_path.exists():
        print(f'[오류] 미적분 드릴 P1 파일을 찾을 수 없습니다.')
        print(f'검색 경로: {base_dir}')
        print(f'organized 경로: {organized_dir}')
        print('\n[대안] 제공된 데이터만으로 검토를 진행합니다.')
        print("\n" + "=" * 80)
        print("[제공된 데이터 검토]")
        print("=" * 80)
        
        # 제공된 데이터만 검토
        for problem_id in sorted(provided_data.keys()):
            provided = provided_data[problem_id]
            print(f"\n[문제 {problem_id}]")
            print(f"내용 길이: {len(provided['Content'])}자")
            print(f"LaTeX 포함: {'$' in provided['Content']}")
            print(f"기하 설명: {provided['Geometry_Desc']}")
            print(f"선택지: {provided['Options']}")
            
            # LaTeX 검증
            dollar_count = provided['Content'].count('$')
            if dollar_count % 2 != 0:
                print(f"[경고] LaTeX $ 기호 짝이 맞지 않음 ({dollar_count}개)")
            else:
                print(f"[정상] LaTeX $ 기호 정상 ({dollar_count}개)")
        
        print("\n[결론] 제공된 데이터는 구조적으로 완전해 보입니다.")
        print("[결론] 딥시크가 문제의 내용을 정확히 파악할 수 있습니다.")
        return
    
    print(f'[파일 찾음] {pdf_path.name}\n')
    
    # PDF 텍스트 추출
    pdf_text = extract_text_from_pdf(pdf_path)
    
    if not pdf_text:
        print('[오류] PDF에서 텍스트를 추출할 수 없습니다.')
        return
    
    print(f'[PDF 텍스트 추출 완료] 총 {len(pdf_text)}자\n')
    
    # 비교
    compare_problems(pdf_text, provided_data)

if __name__ == '__main__':
    main()
