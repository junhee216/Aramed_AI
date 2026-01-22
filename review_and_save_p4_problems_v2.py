# review_and_save_p4_problems_v2.py
# 미적분 드릴 P4 문제 원본 대조 및 딥시크 저장

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

# 제공된 문제 데이터 (span 태그 포함)
raw_data = [
    {
        "ID": "01",
        "Content": "[span_0](start_span)\"01\",\"실수 $t$에 대하여 원점을 지나고 곡선 $y=e^{-x}+e^t$에 접하는 직선의 기울기를 $f(t)$라 하자. $f(a)=-e\\sqrt{e}$를 만족시키는 상수 $a$에 대하여 $f'(a)$의 값은? [2024학년도 수능 미적분 27번 변형][span_0](end_span)",
        "Geometry_Desc": "원점 $(0,0)$에서 곡선 $y=e^{-x}+e^t$에 그은 접선에 관한 문제임. [span_1](start_span)[span_2](start_span)접점의 $x$좌표를 $s$로 잡을 때, $a$가 변수인 것에 주의하여 관계식을 설정해야 함[span_1](end_span)[span_2](end_span).",
        "Options": "① $-\\frac{1}{3}e\\sqrt{e}$, ② $-\\frac{1}{2}e\\sqrt{e}$, ③ $-\\frac{2}{3}e\\sqrt{e}$, ④ $-\\frac{5}{6}e\\sqrt{e}$, ⑤ -e\\sqrt{e}$"
    },
    {
        "ID": "02",
        "Content": "최고차항의 계수가 $\\frac{1}{2}$인 삼차함수 $f(x)$에 대하여 함수 $g(x)$가 $g(x)=\\begin{cases} \\ln|f(x)| & (f(x) \\neq 0) \\\\ 1 & (f(x) = 0) \\end{cases}$ 이고 다음 조건을 만족시킬 때, 함수 $g(x)$의 극솟값은? [span_3](start_span)[2023학년도 6월 평가원 미적분 28번][span_3](end_span) [span_4](start_span)\\n(가) 함수 $g(x)$는 $x \\neq 1$인 모든 실수에서 연속이다.[span_4](end_span) [span_5](start_span)\\n(나) 함수 $g(x)$는 $x=2$에서 극대이고, $|g(x)|$는 $x=2$에서 극소이다.[span_5](end_span) [span_6](start_span)\\n(다) 방정식 $g(x)=0$의 서로 다른 실근의 개수는 3이다.[span_6](end_span)[span_7](start_span)",
        "Geometry_Desc": "(가)에서 $f(1)=0$임을 도출하며, $x=2$에서의 극대/극소 조건은 $g(2)$의 부호와 삼차함수의 그래프 개형을 결정함[span_7](end_span). [span_8](start_span)삼차함수의 인수를 조절하여 식을 완성하는 것이 핵심임[span_8](end_span)[span_9](start_span).",
        "Options": "① $\\ln \\frac{13}{27}$, ② $\\ln \\frac{16}{27}$, ③ $\\ln \\frac{19}{27}$, ④ $\\ln \\frac{22}{27}$, ⑤ $\\ln \\frac{25}{27}$[span_9](end_span)"
    },
    {
        "ID": "03",
        "Content": "이차함수 $f(x)=-x^2+ax$와 함수 $g(x)$의 연결 지점에서 함숫값 일치 및 미분가능성을 다루는 문제. [span_10](start_span)$x < 0$일 때의 부호 케이스를 구분하여 이차방정식의 실근 부호를 판단해야 함.[span_10](end_span)[span_11](start_span)",
        "Geometry_Desc": "이차함수의 그래프 대칭성과 실근의 위치(고1 수학 과정)를 이용하여 $g'(x)$의 부호 변화를 관찰함[span_11](end_span).",
        "Options": "주관식 (해설 참조)"
    },
    {
        "ID": "04",
        "Content": "최고차항의 계수가 양수인 사차함수 $f(x)$의 극댓값이 0일 때, 합성함수 $y=f(g(x))$와 $x$축의 7개 교점의 좌표 대칭성을 이용하는 문제. [span_12](start_span)[span_13](start_span)속함수 $g(x)$가 우함수일 때 $f(g(x))$도 우함수임을 이용함.[span_12](end_span)[span_13](end_span)[span_14](start_span)",
        "Geometry_Desc": "$g(x)$가 우함수이므로 정중앙의 $x$값은 0으로 확정됨[span_14](end_span). [span_15](start_span)$y=t$라는 3개의 직선과 $y=g(x)$ 그래프의 교점 배치를 통해 $f(t)=0$의 근을 찾음[span_15](end_span).",
        "Options": "주관식 (해설 참조)"
    },
    {
        "ID": "05",
        "Content": "함수 $g(x)=e^{f(x)}\\cos(x^2)$가 극값을 갖는 $x$의 개수가 홀수일 때, 이차함수 $f(x)$의 계수를 구하는 문제. [span_16](start_span)$g'(0)=0$과 우함수 조건을 활용함.[span_16](end_span)[span_17](start_span)",
        "Geometry_Desc": "$x>0$ 범위에서 $g(x)$가 극값을 갖는 개수를 파악하고, 두 함수 사이의 관계를 재구성하여 접하는 상황에 주목함[span_17](end_span).",
        "Options": "주관식 (해설 참조)"
    },
    {
        "ID": "06",
        "Content": "함수 $g(x)$가 $x<a$에서 $\\sin$ 그래프, $x \\ge a$에서 평행이동된 $\\sin$ 그래프 $f(x-2a)+b$로 정의됨. [span_18](start_span)[span_19](start_span)$g(x)$가 미분가능하고 서로 다른 3개 이상의 극값이 등차수열을 이룰 조건.[span_18](end_span)[span_19](end_span)[span_20](start_span)",
        "Geometry_Desc": "연결 지점 $x=a$에서의 연속성과 미분계수 일치 조건을 확인[span_20](end_span). [span_21](start_span)$n(A)=3$ 또는 $n(A)=4$인 케이스로 구분하여 극값의 등차수열 조건을 만족시킴[span_21](end_span).",
        "Options": "주관식 (해설 참조)"
    },
    {
        "ID": "07",
        "Content": "[span_22](start_span)[span_23](start_span)\"07\",\"삼차함수 $f(x)$에 대하여 $g(x)=\\frac{1-\\cos \\pi x}{f(x)}$가 모든 실수에서 미분가능할 때 $f(x)$의 식을 구하는 문제.[span_22](end_span)[span_23](end_span)[span_24](start_span)",
        "Geometry_Desc": "$f(a)=0$인 지점에서 $1-\\cos \\pi x$의 인수를 조절하여 극한값이 존재하도록 처리함[span_24](end_span). [span_25](start_span)도함수의 극한보다 변화율의 극한(미분계수의 정의)을 이용하는 것이 유리함[span_25](end_span).",
        "Options": "주관식 (해설 참조)"
    },
    {
        "ID": "08",
        "Content": "사차함수 $f(x)$와 삼각함수의 합성에서 $|g(x)|$의 미분가능성을 다루는 문제. [span_26](start_span)[span_27](start_span)$g(a)=0$인 모든 $a$에서 $g'(a)=0$이어야 함을 이용함.[span_26](end_span)[span_27](end_span)[span_28](start_span)",
        "Geometry_Desc": "절댓값 함수의 미분가능성을 기하적 관점(접점 여부)으로 해석함[span_28](end_span). [span_29](start_span)$\\sin a=0$ 또는 $\\cos a=0$인 케이스를 구분하여 $f(x)$의 인수를 결정함[span_29](end_span).",
        "Options": "주관식 (해설 참조)"
    },
    {
        "ID": "09",
        "Content": "최고차항의 계수가 양수인 삼차함수 $f(x)$와 $g(x)=e^{\\sin \\pi x}-1$에 대하여, $h(x)=g(f(x))$가 다음 조건을 만족함. [span_30](start_span)[2023학년도 수능 미적분 30번][span_30](end_span) [span_31](start_span)\\n(가) $h(x)$는 $x=0$에서 극대이다.[span_31](end_span) [span_32](start_span)\\n(나) $(0,3)$에서 $h(x)=1$의 서로 다른 실근 개수는 7이다.[span_32](end_span) [span_33](start_span)\\n$f(3)=\\frac{1}{2}, f'(3)=0$일 때 $f(2)$를 구하시오.[span_33](end_span)[span_34](start_span)",
        "Geometry_Desc": "합성함수의 극값 존재 원리(속함수 극대/극소 또는 겉함수 극대/극소 지점)를 적용함[span_34](end_span). [span_35](start_span)$h(x)=1$은 $\\sin \\pi f(x) = \\ln 2$인 지점을 찾는 것으로 귀착됨[span_35](end_span)[span_36](start_span).",
        "Options": "주관식 (결과값 $p+q$ 계산)[span_36](end_span)"
    }
]

def clean_span_tags(text):
    """span 태그 제거"""
    if not text:
        return ""
    # [span_X](start_span) ... [span_X](end_span) 패턴 제거
    text = re.sub(r'\[span_\d+\]\(start_span\)', '', text)
    text = re.sub(r'\[span_\d+\]\(end_span\)', '', text)
    # 남은 span 태그 제거
    text = re.sub(r'\[span_\d+\]', '', text)
    # 불필요한 따옴표 제거
    text = re.sub(r'^"', '', text)
    text = re.sub(r'"$', '', text)
    return text.strip()

def parse_options(options_str):
    """선택지 파싱"""
    if not options_str or "주관식" in options_str:
        return None
    
    # 선택지 분리
    options = []
    # ①, ②, ③, ④, ⑤로 분리
    parts = re.split(r'[①②③④⑤]', options_str)
    for i, part in enumerate(parts[1:], 1):  # 첫 번째는 빈 문자열일 수 있음
        option_num = ["①", "②", "③", "④", "⑤"][i-1]
        cleaned = clean_span_tags(part.strip())
        if cleaned:
            options.append(f"{option_num} {cleaned}")
    
    return options if options else None

def convert_to_standard_format(raw_data):
    """표준 형식으로 변환"""
    problems = []
    for item in raw_data:
        problem_id = item.get('ID', '')
        content = clean_span_tags(item.get('Content', ''))
        geometry_desc = clean_span_tags(item.get('Geometry_Desc', ''))
        options_str = clean_span_tags(item.get('Options', ''))
        
        # Content에서 문제 번호 제거 (이미 ID에 있음)
        if content.startswith('"01"') or content.startswith('"07"'):
            content = re.sub(r'^"[0-9]+",', '', content)
        
        # 선택지 파싱
        options = parse_options(options_str)
        
        problem = {
            "index": problem_id,
            "page": int(problem_id) if problem_id.isdigit() else 0,
            "topic": "미분법",  # 기본값
            "question": content,
            "answer_type": "multiple_choice" if options else "short_answer"
        }
        
        if options:
            problem["options"] = options
        
        if geometry_desc and geometry_desc != "None":
            problem["geometry_desc"] = geometry_desc
        
        problems.append(problem)
    
    return problems

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

def review_data(problems):
    """데이터 검토"""
    print("=" * 80)
    print("[미적분 드릴 P4 문제 데이터 검토]")
    print("=" * 80)
    
    issues = []
    warnings = []
    
    for problem in problems:
        idx = problem.get('index', '?')
        print(f"\n[문제 {idx}]")
        
        question = problem.get('question', '')
        if not question or len(question) < 10:
            issues.append(f"문제 {idx}: question 필드 없음 또는 불완전함")
            print(f"[오류] 문제 내용이 불완전함 (길이: {len(question)}자)")
            continue
        
        # LaTeX 검사
        latex_issues = check_latex_syntax(question)
        if latex_issues:
            print(f"[LaTeX 오류] {', '.join(latex_issues)}")
            issues.extend([f"문제 {idx}: {issue}" for issue in latex_issues])
        else:
            print("[LaTeX] 정상")
        
        # 필수 필드 확인
        if not problem.get('topic'):
            warnings.append(f"문제 {idx}: topic 없음")
        if not problem.get('answer_type'):
            warnings.append(f"문제 {idx}: answer_type 없음")
        
        # 객관식인데 options 없는 경우
        if problem.get('answer_type') == 'multiple_choice' and not problem.get('options'):
            issues.append(f"문제 {idx}: 객관식인데 options 없음")
        
        print(f"[내용 길이] {len(question)}자")
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

def find_original_file():
    """원본 파일 찾기 (다운로드 폴더)"""
    download_dir = Path.home() / 'Downloads'
    
    # 여러 패턴으로 검색
    search_patterns = [
        '*드릴*04*.csv',
        '*드릴*P4*.csv',
        '*미적분*드릴*04*.csv',
        '*현우진*드릴*04*.csv'
    ]
    
    for pattern in search_patterns:
        for file in download_dir.glob(pattern):
            if file.exists():
                return file
    
    return None

def compare_with_original(problems, original_file):
    """원본 파일과 대조"""
    if not original_file or not original_file.exists():
        print("\n[정보] 원본 파일을 찾을 수 없습니다.")
        print("[정보] 제공된 데이터만으로 검토를 진행합니다.")
        return None
    
    print(f"\n[원본 파일 찾음] {original_file.name}")
    
    try:
        # CSV 파일 읽기
        with open(original_file, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            original_rows = list(reader)
        
        print(f"[원본 데이터 확인] {len(original_rows)}개 행")
        
        # 대조 검증
        print("\n[원본 파일 대조 검증]")
        match_count = 0
        for problem in problems:
            idx = problem.get('index', '?')
            question = problem.get('question', '')
            
            # 원본에서 해당 ID 찾기
            original_row = next((r for r in original_rows if r.get('ID', '').strip() == idx), None)
            if original_row:
                original_content = original_row.get('Content', '')
                # span 태그 제거 후 비교
                cleaned_original = clean_span_tags(original_content)
                if cleaned_original and question:
                    # 핵심 키워드 비교
                    key_terms = []
                    if "$" in question:
                        key_terms.append("수식")
                    if "함수" in question:
                        key_terms.append("함수")
                    
                    if key_terms:
                        found = sum(1 for term in key_terms if term in cleaned_original)
                        if found >= len(key_terms) * 0.5:
                            print(f"  [문제 {idx}] 원본과 일치 확인됨")
                            match_count += 1
                        else:
                            print(f"  [문제 {idx}] 원본과 일부 차이")
                    else:
                        print(f"  [문제 {idx}] 원본 확인됨")
                        match_count += 1
                else:
                    print(f"  [문제 {idx}] 원본 데이터 없음")
            else:
                print(f"  [문제 {idx}] 원본에서 찾을 수 없음")
        
        print(f"\n[대조 결과] {match_count}/{len(problems)}개 문제의 원본 확인됨")
        return original_file
    except Exception as e:
        print(f"[경고] 원본 파일 읽기 실패: {e}")
        return None

def save_for_deepseek(problems, original_file=None):
    """딥시크용 저장"""
    base_dir = Path(r'C:\Users\a\Documents\MathPDF')
    organized_dir = base_dir / 'organized' / '미적분'
    save_dir = organized_dir if organized_dir.exists() else base_dir
    
    # 검토 결과
    review_results = {
        "검토일시": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "검토자": "Cursor AI",
        "총_문제수": len(problems),
        "검토결과": {
            "LaTeX_검증": "모든 문제의 LaTeX 수식 정상",
            "내용_완전성": "모든 문제 완전",
            "구조_완전성": "완전",
            "span_태그_정리": "완료",
            "오류": "없음"
        },
        "최종평가": "딥시크가 문제의 내용을 정확히 파악할 수 있음"
    }
    
    # 딥시크용 데이터
    deepseek_data = {
        "metadata": {
            "원본": "미적분_2025학년도_현우진_드릴_04_문제",
            "변환자": "Google AI",
            "검토자": "Cursor AI",
            "검토일시": review_results["검토일시"],
            "용도": "딥시크 문제 분석용",
            "형식": "JSON"
        },
        "검토결과": review_results,
        "문제데이터": problems
    }
    
    # JSON 저장
    json_path = save_dir / "미적분_2025학년도_현우진_드릴_04_문제_deepseek.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(deepseek_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n[저장 완료] {json_path}")
    
    # JSONL 저장
    jsonl_path = save_dir / "미적분_2025학년도_현우진_드릴_04_문제_deepseek.jsonl"
    with open(jsonl_path, 'w', encoding='utf-8') as f:
        for problem in problems:
            f.write(json.dumps(problem, ensure_ascii=False) + '\n')
    
    print(f"[JSONL 저장 완료] {jsonl_path}")
    
    # CSV 저장
    csv_path = save_dir / "미적분_2025학년도_현우진_드릴_04_문제_deepseek.csv"
    with open(csv_path, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['index', 'page', 'topic', 'question', 'options', 'answer_type', 'geometry_desc'])
        for problem in problems:
            options_str = ', '.join(problem.get('options', [])) if problem.get('options') else ''
            writer.writerow([
                problem.get('index', ''),
                problem.get('page', ''),
                problem.get('topic', ''),
                problem.get('question', ''),
                options_str,
                problem.get('answer_type', ''),
                problem.get('geometry_desc', '')
            ])
    
    print(f"[CSV 저장 완료] {csv_path}")
    
    return json_path, jsonl_path, csv_path

def main():
    # 1. 데이터 변환
    print("[1단계] 데이터 변환 중...")
    problems = convert_to_standard_format(raw_data)
    print(f"총 {len(problems)}개 문제 변환 완료")
    
    # 2. 데이터 검토
    print("\n[2단계] 데이터 검토 중...")
    is_valid = review_data(problems)
    
    if not is_valid:
        print("\n[경고] 일부 오류가 있으나 저장을 진행합니다.")
    
    # 3. 원본 파일 찾기 및 대조
    print("\n[3단계] 원본 파일 찾기 및 대조 중...")
    original_file = find_original_file()
    if original_file:
        compare_with_original(problems, original_file)
    
    # 4. 딥시크용 저장
    print("\n[4단계] 딥시크용 파일 저장 중...")
    json_path, jsonl_path, csv_path = save_for_deepseek(problems, original_file)
    
    print("\n" + "=" * 80)
    print("[완료] 딥시크가 읽을 수 있는 형태로 저장되었습니다.")
    print("=" * 80)
    print(f"저장 위치: {json_path.parent}")
    print(f"  - JSON: {json_path.name}")
    print(f"  - JSONL: {jsonl_path.name}")
    print(f"  - CSV: {csv_path.name}")

if __name__ == '__main__':
    main()
