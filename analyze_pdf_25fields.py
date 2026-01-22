# analyze_pdf_25fields.py
# PDF 파일을 읽어서 25개 필드 구조로 분석하고 CSV로 출력

import re
import csv
import json
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime

try:
    import PyPDF2
    PDF_LIBRARY = 'PyPDF2'
except ImportError:
    try:
        import fitz  # PyMuPDF
        PDF_LIBRARY = 'pymupdf'
    except ImportError:
        PDF_LIBRARY = None


class PDF25FieldAnalyzer:
    """PDF 파일을 25개 필드 구조로 분석하는 클래스"""
    
    def __init__(self, pdf_path: Path, base_filename: str):
        self.pdf_path = pdf_path
        self.base_filename = base_filename
        self.problems = []
        
    def extract_text_from_pdf(self) -> str:
        """PDF에서 텍스트 추출"""
        if PDF_LIBRARY == 'PyPDF2':
            with open(self.pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                return text
        elif PDF_LIBRARY == 'pymupdf':
            import fitz
            doc = fitz.open(self.pdf_path)
            text = ""
            for page in doc:
                text += page.get_text() + "\n"
            doc.close()
            return text
        else:
            raise ImportError("PDF 라이브러리가 설치되지 않았습니다.")
    
    def parse_problems(self, text: str) -> List[Dict]:
        """텍스트에서 문제들을 파싱"""
        problems = []
        
        # 문제 패턴: [4점] 또는 [점수]로 끝나는 문제 찾기
        # 문제는 보통 "---" 또는 페이지 번호로 구분됨
        problem_pattern = r'([^─]*?)(?:\[(\d+)점\]|\[점수\])'
        
        matches = list(re.finditer(problem_pattern, text, re.DOTALL))
        
        for i, match in enumerate(matches):
            problem_text = match.group(1).strip()
            score = match.group(2) if match.group(2) else "4"
            
            # 문제 번호 추출 (있는 경우)
            problem_num_match = re.search(r'(\d+)\s*번', problem_text)
            problem_num = problem_num_match.group(1) if problem_num_match else str(i + 1)
            
            # 선택지 추출
            choices = []
            choice_pattern = r'[①②③④⑤]\s*([-\d]+)'
            choice_matches = re.findall(choice_pattern, problem_text)
            if choice_matches:
                choices = choice_matches
            
            problems.append({
                'number': problem_num,
                'text': problem_text,
                'score': score,
                'choices': choices
            })
        
        return problems
    
    def analyze_problem(self, problem: Dict, problem_index: int) -> Dict:
        """단일 문제를 25개 필드로 분석"""
        text = problem['text']
        problem_num = problem['number']
        
        # 문제ID: 파일명_문제번호
        problem_id = f"{self.base_filename}_{problem_num}"
        
        # 기본 메타데이터 분석
        # 출처: 파일명에서 추출
        source = "자체교재"  # 기본값
        if "2025" in self.base_filename:
            source = "2025_자체교재"
        
        # 대단원: 수학I (파일명에 수1이 있으면)
        major_unit = "수학I"
        if "수2" in self.base_filename:
            major_unit = "수학II"
        elif "미적분" in self.base_filename:
            major_unit = "미적분"
        elif "기하" in self.base_filename:
            major_unit = "기하"
        elif "확률" in self.base_filename or "통계" in self.base_filename:
            major_unit = "확률과통계"
        
        # 중단원: 문제 텍스트에서 추출
        minor_unit = "수열"
        if "등차수열" in text:
            minor_unit = "수열"
        elif "등비수열" in text:
            minor_unit = "수열"
        elif "지수" in text or "로그" in text:
            minor_unit = "지수함수와로그함수"
        elif "삼각함수" in text or "삼각" in text:
            minor_unit = "삼각함수"
        
        # 소단원: 더 세부적으로
        sub_unit = "등차수열"
        if "등차수열" in text:
            if "합" in text or "∑" in text:
                sub_unit = "등차수열의합"
            elif "일반항" in text:
                sub_unit = "등차수열의일반항"
            else:
                sub_unit = "등차수열"
        elif "등비수열" in text:
            sub_unit = "등비수열"
        
        # 난이도: 문제 복잡도로 판단
        difficulty = "중"
        if len(problem['choices']) > 0:  # 선택형 문제
            if "최솟값" in text or "최댓값" in text:
                difficulty = "상"
            else:
                difficulty = "중"
        else:  # 서술형
            if "부등식" in text and "절댓값" in text:
                difficulty = "상"
            elif "합" in text and "절댓값" in text:
                difficulty = "상"
            else:
                difficulty = "중"
        
        # 핵심개념 추출
        core_concept = "등차수열"
        if "등차수열" in text:
            if "합" in text:
                core_concept = "등차수열의합"
            elif "일반항" in text:
                core_concept = "등차수열의일반항"
            elif "공차" in text:
                core_concept = "등차수열의공차"
        elif "등비수열" in text:
            core_concept = "등비수열"
        
        # LaTeX 예시 추출
        latex_example = "$a_n = a + (n-1)d$"
        latex_match = re.search(r'\$([^$]+)\$', text)
        if latex_match:
            latex_example = f"${latex_match.group(1)}$"
        
        # 문제구조
        problem_structure = "조건제시→일반항구하기→계산"
        if "부등식" in text:
            problem_structure = "조건제시→부등식해결→답계산"
        elif "합" in text:
            problem_structure = "조건제시→합공식적용→계산"
        elif "최솟값" in text or "최댓값" in text:
            problem_structure = "조건제시→식변형→최적화"
        
        # 핵심패턴
        core_pattern = "$a_n = a + (n-1)d$"
        if "부등식" in text and "절댓값" in text:
            core_pattern = "$(a_m)^2 - |a_m| - 2 \\leq 0$"
        elif "합" in text:
            core_pattern = "$S_n = \\frac{n(a_1+a_n)}{2}$"
        
        # 변형요소 (JSON 형식)
        variation_elements = {
            "첫째항": [-6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6],
            "공차": [1, 2, 3, 4, -1, -2, -3, -4, "4/3", "1/2", "-3"]
        }
        if "부등식" in text:
            variation_elements["부등식상수"] = [0, 1, 2, -1, -2]
        if "합" in text:
            variation_elements["항의개수"] = [10, 15, 20, 25, 30]
        
        variation_json = json.dumps(variation_elements, ensure_ascii=False)
        
        # 난이도조절
        difficulty_adjust = "쉽게=양수첫째항작은공차 / 어렵게=음수첫째항분수공차"
        
        # 함정설계
        trap_design = "1.공차부호실수 2.절댓값처리오류 3.부등식해결실수"
        if "부등식" in text:
            trap_design = "1.절댓값을케이스로나누지않음 2.부등식부호방향실수 3.자연수조건확인누락"
        elif "합" in text:
            trap_design = "1.합공식선택오류 2.항의개수계산실수 3.부호처리오류"
        elif "최솟값" in text:
            trap_design = "1.조건해석오류 2.최적화방법선택실수 3.정수조건확인누락"
        
        # 출제의도
        purpose = "등차수열의기본성질이해도측정"
        if "부등식" in text:
            purpose = "등차수열과부등식의결합능력측정"
        elif "합" in text:
            purpose = "등차수열의합공식활용능력측정"
        elif "최솟값" in text:
            purpose = "등차수열을이용한최적화문제해결능력"
        
        # 유사유형
        similar_types = "등차수열;수열합;일반항"
        if "부등식" in text:
            similar_types = "등차수열;부등식;절댓값"
        elif "합" in text:
            similar_types = "등차수열합;시그마;수열합"
        
        # 선행개념
        prerequisite = "등차수열정의;일반항공식"
        if "부등식" in text:
            prerequisite = "등차수열;부등식해법;절댓값성질"
        elif "합" in text:
            prerequisite = "등차수열;합공식;시그마"
        
        # 후행개념
        subsequent = "등비수열;수열응용"
        if "부등식" in text:
            subsequent = "수열부등식;최적화문제"
        elif "합" in text:
            subsequent = "등비수열합;수열극한"
        
        # 예상시간
        estimated_time = 3
        if difficulty == "상":
            estimated_time = 5
        elif difficulty == "하":
            estimated_time = 2
        
        # 실수포인트
        mistake_points = "1.공차부호실수 2.일반항계산오류 3.조건확인누락"
        if "부등식" in text:
            mistake_points = "1.절댓값케이스분리실수 2.부등식해결오류 3.자연수조건확인누락"
        elif "합" in text:
            mistake_points = "1.합공식선택오류 2.항의개수계산실수 3.부호처리오류"
        
        # 개념연결
        concept_connection = "중학교등차수열과연결"
        if "부등식" in text:
            concept_connection = "부등식단원과연결"
        elif "합" in text:
            concept_connection = "시그마기호와연결"
        
        # AI신뢰도
        ai_confidence = 90
        if "등차수열" in text and "공차" in text:
            ai_confidence = 95
        elif "부등식" in text and "절댓값" in text:
            ai_confidence = 88
        
        # 오늘 날짜
        today = datetime.now().strftime('%Y-%m-%d')
        
        return {
            '문제ID': problem_id,
            '출처': source,
            '대단원': major_unit,
            '중단원': minor_unit,
            '소단원': sub_unit,
            '난이도': difficulty,
            '핵심개념': core_concept,
            'LaTeX예시': latex_example,
            '문제구조': problem_structure,
            '핵심패턴': core_pattern,
            '변형요소': variation_json,
            '난이도조절': difficulty_adjust,
            '함정설계': trap_design,
            '출제의도': purpose,
            '유사유형': similar_types,
            '선행개념': prerequisite,
            '후행개념': subsequent,
            '예상시간': estimated_time,
            '실수포인트': mistake_points,
            '개념연결': concept_connection,
            '검증상태': '승인됨',
            'AI신뢰도': ai_confidence,
            '수정이력': f'{today}: Auto 초기생성',
            '사용빈도': 0,
            '학생반응': '미평가'
        }
    
    def analyze_all(self) -> List[Dict]:
        """PDF의 모든 문제를 분석"""
        print(f"[진행] PDF 파일 읽는 중: {self.pdf_path}")
        text = self.extract_text_from_pdf()
        
        print(f"[진행] 문제 파싱 중...")
        problems = self.parse_problems(text)
        
        print(f"[정보] 총 {len(problems)}개의 문제를 찾았습니다.")
        
        analyzed = []
        for i, problem in enumerate(problems, 1):
            print(f"[진행] 문제 {i}/{len(problems)} 분석 중...")
            analyzed_problem = self.analyze_problem(problem, i)
            analyzed.append(analyzed_problem)
        
        return analyzed
    
    def save_csv(self, output_path: Path):
        """분석 결과를 CSV로 저장"""
        if not self.problems:
            print("[경고] 저장할 데이터가 없습니다.")
            return
        
        fieldnames = [
            '문제ID', '출처', '대단원', '중단원', '소단원', '난이도', '핵심개념', 'LaTeX예시',
            '문제구조', '핵심패턴', '변형요소', '난이도조절', '함정설계', '출제의도', '유사유형',
            '선행개념', '후행개념', '예상시간', '실수포인트', '개념연결',
            '검증상태', 'AI신뢰도', '수정이력', '사용빈도', '학생반응'
        ]
        
        with open(output_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for problem in self.problems:
                # CSV에서 쉼표가 포함된 필드는 큰따옴표로 감싸기
                row = {}
                for field in fieldnames:
                    value = problem.get(field, '')
                    # 숫자는 그대로, 문자열은 필요시 따옴표 처리
                    if isinstance(value, (int, float)):
                        row[field] = value
                    else:
                        # JSON 필드는 이미 문자열이므로 그대로
                        row[field] = value
                writer.writerow(row)
        
        print(f"[완료] CSV 파일 저장 완료: {output_path}")
        print(f"[정보] 총 {len(self.problems)}개 문제 저장됨")


def main():
    """메인 실행 함수"""
    import sys
    
    # PDF 파일 경로
    pdf_filename = "수1_2025학년도_현우진_드릴_P6.pdf"
    pdf_path = Path(r'C:\Users\a\Documents\MathPDF\organized\수1') / pdf_filename
    
    if not pdf_path.exists():
        # 다른 경로 시도
        pdf_path = Path(r'C:\Users\a\Documents\MathPDF') / pdf_filename
        if not pdf_path.exists():
            print(f"[오류] PDF 파일을 찾을 수 없습니다: {pdf_filename}")
            print(f"[시도] {pdf_path}")
            return
    
    # 파일명에서 확장자 제거
    base_filename = pdf_path.stem
    
    print("=" * 60)
    print("[PDF 25개 필드 분석 도구]")
    print("=" * 60)
    print(f"[파일] {pdf_path}")
    print(f"[기본파일명] {base_filename}\n")
    
    try:
        # 분석기 생성
        analyzer = PDF25FieldAnalyzer(pdf_path, base_filename)
        
        # 모든 문제 분석
        analyzer.problems = analyzer.analyze_all()
        
        # CSV 저장
        output_path = Path.cwd() / f"{base_filename}_25fields.csv"
        analyzer.save_csv(output_path)
        
        print(f"\n[완료] 모든 작업이 완료되었습니다!")
        print(f"[출력] {output_path.absolute()}")
        
    except Exception as e:
        print(f"\n[오류] 발생: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
