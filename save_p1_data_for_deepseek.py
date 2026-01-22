# save_p1_data_for_deepseek.py
# 구글 AI 변환 데이터 + 검토 결과를 딥시크가 읽을 수 있는 형태로 저장

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

# 구글 AI 변환 데이터
google_ai_data = {
    "01": {
        "ID": "01",
        "Content": "모든 자연수 $n$에 대하여 $a_n > 0$인 수열 $\\{a_n\\}$이 $\\lim_{n \\to \\infty} \\frac{\\sqrt{n+p^2}-\\sqrt{n+p}}{a_n} = 2$, $\\lim_{n \\to \\infty} \\frac{\\sqrt{n+2p}-\\sqrt{n}}{a_n} = 1$을 만족시킬 때, 양수 $p$의 값은?",
        "Geometry_Desc": "None (대수적 극한 미지수 결정)",
        "Options": "①1 ②2 ③3 ④4 ⑤5"
    },
    "02": {
        "ID": "02",
        "Content": "자연수 $n$에 대하여 원 $(x-4n)^2 + (y-n)^2 = n^2$과 직선 $y=\\frac{4}{3}x$ 및 $x$축에 동시에 접하는 원의 중심의 좌표를 $(a_n, b_n)$이라 할 때, $\\lim_{n \\to \\infty} \\frac{a_n b_{n+1}}{n^2}$의 값은? (단, $a_n > 4n$)",
        "Geometry_Desc": "1. 중심이 $(4n, n)$이고 반지름이 $n$인 원이 기본 배치됨. 2. 새로운 원 $(a_n, b_n)$은 제1사분면에서 $x$축과 직선 $y=4/3x$에 동시에 접함. 3. 조건 $a_n > 4n$에 의해 이 원은 기준 원의 오른쪽에 위치함.",
        "Options": "①20 ②24 ③28 ④32 ⑤36"
    },
    "03": {
        "ID": "03",
        "Content": "일차함수 $f(x)$에 대하여 함수 $g(x)$를 $g(x) = \\lim_{n \\to \\infty} \\frac{3(f(x))^{2n+1} + 4(f(x+2))^{2n}}{(f(x))^{2n} + 2(f(x+2))^{2n}}$이라 하자. $\\lim_{x \\to 2^+} g(x) - \\lim_{x \\to 2^-} g(x) = 7$일 때, $f(6)$의 값을 구하시오.",
        "Geometry_Desc": "None (등비수열의 극한으로 정의된 함수)",
        "Options": "주관식"
    },
    "04": {
        "ID": "04",
        "Content": "수열 $\\{a_n\\}$이 모든 자연수 $n$에 대하여 $\\sum_{k=1}^n a_k = \\frac{pn}{2n+4}$를 만족시키고, $\\sum_{n=1}^\\infty (a_n + a_{n+2}) = 9$일 때, 상수 $p$의 값을 구하시오.",
        "Geometry_Desc": "None (급수와 일반항의 관계)",
        "Options": "주관식"
    },
    "05": {
        "ID": "05",
        "Content": "자연수 $n$에 대하여 직선 $x=n$이 두 곡선 $y=3^{-x}$, $y=a^{-x} (a>1, a \\ne 3)$과 만나는 점을 각각 $A_n, B_n$이라 하자. $\\sum_{n=1}^\\infty \\overline{A_n B_n} = \\frac{1}{3}$을 만족시키는 모든 $a$의 값의 합이 $q/p$일 때, $p+q$의 값을 구하시오. (단, $p, q$는 서로소인 자연수)",
        "Geometry_Desc": "1. 두 지수함수 $y=(1/3)^x$와 $y=(1/a)^x$의 그래프가 제1사분면에서 감소하는 형태. 2. $x=n$에서의 두 함수값 차이인 $\\overline{A_n B_n}$을 일반항으로 하는 등비급수 상황.",
        "Options": "주관식"
    },
    "06": {
        "ID": "06",
        "Content": "모든 자연수 $n$에 대하여 (가) $a_n \\ne a_{n+1}$, (나) 두 점 $P_n(a_n, a_n^2), P_{n+1}(a_{n+1}, a_{n+1}^2)$을 지나는 직선의 기울기는 $ka_n$이다. $\\sum_{n=1}^\\infty a_n = 2, \\sum_{n=1}^\\infty a_n^2 = 8$일 때, $a_1 + k$의 값은? (단, $k$는 상수)",
        "Geometry_Desc": "1. 이차함수 $y=x^2$ 위의 두 점을 잇는 직선의 기울기 구조. 2. 점 $P_n$과 $P_{n+1}$의 좌표 관계를 통해 $a_n$의 점화식 도출 필요.",
        "Options": "①10/3 ②11/3 ③3 ④13/3 ⑤14/3"
    },
    "07": {
        "ID": "07",
        "Content": "수열 $\\{a_n\\}$이 다음 조건을 만족시킨다. (가) $\\sum_{n=1}^\\infty a_n = 3/2$, (나) 모든 자연수 $p$에 대하여 $\\sum_{n=1}^\\infty a_{n+p} = a_p$이다. $\\sum_{n=1}^\\infty a_{2n}$의 값은?",
        "Geometry_Desc": "None (급수의 성질과 수열의 관계 추론)",
        "Options": "①1/4 ②1/2 ③3/4 ④1 ⑤5/4"
    },
    "08": {
        "ID": "08",
        "Content": "첫째항이 2이고 공차가 4인 등차수열 $\\{a_n\\}$이 있다. 수열 $\\{b_n\\}$이 $b_1=10$이고, 모든 자연수 $n$에 대하여 $b_{n+1} = (\\cos \\frac{\\pi a_n}{6}) \\times b_n$을 만족시킬 때, $\\sum_{n=1}^\\infty 3b_{2n}$의 값을 구하시오.",
        "Geometry_Desc": "None (삼각함수의 주기성과 등비급수의 결합)",
        "Options": "주관식"
    }
}

# 검토 결과
review_results = {
    "검토일시": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "검토자": "Cursor AI",
    "총_문제수": 8,
    "검토결과": {
        "LaTeX_검증": "모든 문제의 LaTeX 수식 정상 (12-20개 $ 기호, 짝 일치)",
        "내용_완전성": "모든 문제에 질문 마커, 수식 요소, 변수 표기 포함",
        "선택지_구분": "객관식 4개(01,02,06,07), 주관식 4개(03,04,05,08) - 정확",
        "기하설명": "기하 요소 있는 문제(02,05,06)에 적절한 설명 제공",
        "구조_완전성": "모든 필드(ID, Content, Geometry_Desc, Options) 완전",
        "오류": "없음",
        "경고": "없음"
    },
    "최종평가": "딥시크가 문제의 내용을 정확히 파악할 수 있음"
}

def save_for_deepseek():
    """딥시크가 읽을 수 있는 형태로 저장"""
    
    # MathPDF 폴더 찾기
    base_dir = Path(r'C:\Users\a\Documents\MathPDF')
    organized_dir = base_dir / 'organized' / '미적분'
    
    # 저장 위치 결정
    save_dir = organized_dir if organized_dir.exists() else base_dir
    
    # 딥시크용 데이터 구조
    deepseek_data = {
        "metadata": {
            "원본": "미적분_2025학년도_현우진_드릴_P1",
            "변환자": "Google AI",
            "검토자": "Cursor AI",
            "검토일시": review_results["검토일시"],
            "용도": "딥시크 문제 분석용"
        },
        "검토결과": review_results,
        "문제데이터": google_ai_data
    }
    
    # JSON 파일로 저장
    json_path = save_dir / "미적분_2025학년도_현우진_드릴_P1_deepseek.json"
    
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(deepseek_data, f, ensure_ascii=False, indent=2)
    
    print(f"[저장 완료] {json_path}")
    print(f"총 {len(google_ai_data)}개 문제 저장됨")
    print(f"검토 결과 포함됨")
    
    # CSV 파일도 저장 (딥시크가 읽기 쉬운 형태)
    csv_path = save_dir / "미적분_2025학년도_현우진_드릴_P1_deepseek.csv"
    
    import csv
    with open(csv_path, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['ID', 'Content', 'Geometry_Desc', 'Options', '검토상태'])
        for problem_id in sorted(google_ai_data.keys()):
            problem = google_ai_data[problem_id]
            writer.writerow([
                problem['ID'],
                problem['Content'],
                problem['Geometry_Desc'],
                problem['Options'],
                '검토완료'
            ])
    
    print(f"[CSV 저장 완료] {csv_path}")
    
    return json_path, csv_path

if __name__ == '__main__':
    try:
        json_path, csv_path = save_for_deepseek()
        print("\n[완료] 딥시크가 읽을 수 있는 형태로 저장되었습니다.")
    except Exception as e:
        print(f"[오류] {e}")
        import traceback
        traceback.print_exc()
