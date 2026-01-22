# analyze_csat_meta.py
# 수능 수학 문제 메타분석 전문가 시스템
# 25개 메타 분류 기준에 따른 심층 분석

import os
import re
import csv
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime

try:
    import pdfplumber
    PDF_LIBRARY = 'pdfplumber'
except ImportError:
    try:
        import fitz  # PyMuPDF
        PDF_LIBRARY = 'pymupdf'
    except ImportError:
        try:
            import PyPDF2
            PDF_LIBRARY = 'pypdf2'
        except ImportError:
            PDF_LIBRARY = None

class CSATMetaAnalyzer:
    """수능 수학 문제 메타분석 전문가"""
    
    def __init__(self):
        self.base_dir = Path(r'C:\Users\a\Documents\MathPDF\organized\기출')
        self.output_dir = Path(r'C:\Users\a\Documents\Aramed_AI\output')
        self.output_dir.mkdir(exist_ok=True)
        
    def extract_text_from_pdf(self, pdf_path: Path) -> str:
        """PDF에서 텍스트 추출"""
        if PDF_LIBRARY == 'pdfplumber':
            text_parts = []
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        text_parts.append(text)
            return '\n'.join(text_parts)
        
        elif PDF_LIBRARY == 'pymupdf':
            doc = fitz.open(pdf_path)
            text_parts = []
            for page in doc:
                text_parts.append(page.get_text())
            doc.close()
            return '\n'.join(text_parts)
        
        elif PDF_LIBRARY == 'pypdf2':
            with open(pdf_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                text_parts = []
                for page in reader.pages:
                    text_parts.append(page.extract_text())
            return '\n'.join(text_parts)
        
        return ""
    
    def parse_filename(self, filename: str) -> Dict[str, str]:
        """파일명에서 정보 추출"""
        # 예: 수학영역(기하)_2022학년도_수능기출.pdf
        info = {
            'year': None,
            'subject': None,
            'exam_type': '수능'  # 기본값
        }
        
        # 년도 추출
        year_match = re.search(r'(\d{4})학년도', filename)
        if year_match:
            info['year'] = year_match.group(1)
        
        # 과목 추출
        if '기하' in filename:
            info['subject'] = '기하'
        elif '미적' in filename:
            info['subject'] = '미적분'
        elif '확률과통계' in filename or '확통' in filename:
            info['subject'] = '확률과통계'
        elif '수1' in filename or '수학I' in filename:
            info['subject'] = '수학I'
        elif '수2' in filename or '수학II' in filename:
            info['subject'] = '수학II'
        
        # 시행월 추출 (파일명에 없으면 기본값)
        if '6월' in filename or '1차' in filename:
            info['exam_month'] = '6월'
        elif '9월' in filename or '2차' in filename:
            info['exam_month'] = '9월'
        elif '11월' in filename or '수능' in filename:
            info['exam_month'] = '11월'
        else:
            info['exam_month'] = '11월'  # 수능 기본값
        
        return info
    
    def extract_problems(self, text: str) -> List[Dict]:
        """텍스트에서 문제 추출"""
        problems = []
        
        # 문제 번호 패턴 (1. 2. 3. 또는 ① ② ③)
        problem_pattern = re.compile(r'(\d+)\.\s+', re.MULTILINE)
        
        lines = text.split('\n')
        current_problem = None
        current_number = None
        
        for i, line in enumerate(lines):
            # 문제 번호 찾기
            match = problem_pattern.match(line.strip())
            if match:
                # 이전 문제 저장
                if current_problem:
                    problems.append(current_problem)
                
                # 새 문제 시작
                current_number = int(match.group(1))
                current_problem = {
                    'number': current_number,
                    'text': line,
                    'full_text': line,
                    'start_line': i
                }
            elif current_problem:
                # 문제 내용 계속 추가
                current_problem['full_text'] += '\n' + line
                current_problem['text'] += '\n' + line
        
        # 마지막 문제 저장
        if current_problem:
            problems.append(current_problem)
        
        return problems
    
    def analyze_problem_meta(self, problem: Dict, file_info: Dict, problem_text: str) -> Dict:
        """25개 메타 분류 기준으로 문제 분석"""
        
        analysis = {}
        
        # A. 출제 식별 정보 (5개)
        analysis['출제년도'] = file_info.get('year', '미상')
        analysis['시행월'] = file_info.get('exam_month', '11월')
        analysis['문항번호'] = problem.get('number', 0)
        
        # 배점 추정 (문제 텍스트에서 찾기)
        score_match = re.search(r'\[(\d+)점\]', problem_text)
        if score_match:
            analysis['배점'] = int(score_match.group(1))
        else:
            # 문항번호 기반 추정
            if analysis['문항번호'] <= 15:
                analysis['배점'] = 2
            elif analysis['문항번호'] <= 22:
                analysis['배점'] = 3
            else:
                analysis['배점'] = 4
        
        analysis['과목구분'] = file_info.get('subject', '미상')
        
        # B. 난이도 지표 (5개)
        # 공식정답률 추정
        answer_rate = self.estimate_answer_rate(analysis['문항번호'], problem_text)
        analysis['공식정답률'] = f"{answer_rate:.1f}%"
        
        # 난이도등급
        analysis['난이도등급'] = self.determine_difficulty_grade(answer_rate)
        
        # 풀이소요시간 추정
        solving_time = self.estimate_solving_time(problem_text, analysis['문항번호'])
        analysis['풀이소요시간'] = f"{solving_time}분"
        
        # 오답률1위선지 (추정 불가능하므로 미상)
        analysis['오답률1위선지'] = '미상'
        
        # 체감난이도
        perceived_difficulty = (solving_time * 100) / answer_rate if answer_rate > 0 else 0
        analysis['체감난이도'] = f"{perceived_difficulty:.1f}"
        
        # C. 개념 분류 (5개)
        concept_info = self.analyze_concepts(problem_text, analysis['과목구분'])
        analysis.update(concept_info)
        
        # D. 문제 구조 분석 (5개)
        structure_info = self.analyze_structure(problem_text)
        analysis.update(structure_info)
        
        # E. 출제 전략 분석 (5개)
        strategy_info = self.analyze_strategy(problem_text, answer_rate, analysis['문항번호'])
        analysis.update(strategy_info)
        
        return analysis
    
    def estimate_answer_rate(self, problem_number: int, problem_text: str) -> float:
        """정답률 추정"""
        # 문항번호 기반 기본 추정
        if problem_number <= 15:
            base_rate = 90.0 - (problem_number - 1) * 2
        elif problem_number <= 22:
            base_rate = 70.0 - (problem_number - 16) * 5
        elif problem_number <= 28:
            base_rate = 50.0 - (problem_number - 23) * 5
        else:
            base_rate = 20.0 - (problem_number - 29) * 5
        
        # 문제 복잡도로 조정
        if '극한' in problem_text or '미분' in problem_text or '적분' in problem_text:
            base_rate -= 5
        if len(problem_text) > 500:
            base_rate -= 3
        
        return max(5.0, min(95.0, base_rate))
    
    def determine_difficulty_grade(self, answer_rate: float) -> str:
        """난이도등급 결정"""
        if answer_rate >= 95:
            return '1등급컷용'
        elif answer_rate >= 80:
            return '2-3등급용'
        elif answer_rate >= 50:
            return '4-6등급용'
        elif answer_rate >= 30:
            return '변별용'
        else:
            return '킬러용'
    
    def estimate_solving_time(self, problem_text: str, problem_number: int) -> int:
        """풀이소요시간 추정 (분)"""
        # 기본 시간 (문항번호 기반)
        if problem_number <= 15:
            base_time = 2
        elif problem_number <= 22:
            base_time = 4
        elif problem_number <= 28:
            base_time = 6
        else:
            base_time = 8
        
        # 문제 복잡도로 조정
        complexity_factors = {
            '계산': 1,
            '그래프': 1,
            '증명': 2,
            '추론': 2,
            '함수': 1,
            '미분': 1,
            '적분': 2,
            '극한': 1
        }
        
        for factor, time_add in complexity_factors.items():
            if factor in problem_text:
                base_time += time_add
        
        # 텍스트 길이로 조정
        if len(problem_text) > 300:
            base_time += 1
        
        return min(10, max(1, base_time))
    
    def analyze_concepts(self, problem_text: str, subject: str) -> Dict:
        """개념 분류 분석"""
        result = {}
        
        # 대단원
        result['대단원'] = subject
        
        # 중단원 추정 (키워드 기반)
        minor_units = {
            '미적분': ['수열의극한', '미분법', '적분법'],
            '기하': ['이차곡선', '평면벡터', '공간도형'],
            '확률과통계': ['경우의수', '확률', '통계']
        }
        
        result['중단원'] = '미상'  # 기본값
        if subject in minor_units:
            for unit in minor_units[subject]:
                if unit in problem_text:
                    result['중단원'] = unit
                    break
        
        # 핵심개념태그
        concept_count = self.count_concepts(problem_text)
        if concept_count == 1:
            result['핵심개념태그'] = '단일개념'
        elif concept_count == 2:
            result['핵심개념태그'] = '융합개념'
        else:
            result['핵심개념태그'] = '복합개념'
        
        # 개념난이도
        result['개념난이도'] = self.determine_concept_difficulty(problem_text)
        
        # 필수선행개념
        result['필수선행개념'] = self.determine_prerequisites(problem_text, subject)
        
        return result
    
    def count_concepts(self, text: str) -> int:
        """핵심 개념 개수 추정"""
        concept_keywords = [
            '함수', '미분', '적분', '극한', '수열', '확률', '통계',
            '벡터', '곡선', '도형', '로그', '지수', '삼각'
        ]
        count = sum(1 for keyword in concept_keywords if keyword in text)
        return max(1, min(5, count))
    
    def determine_concept_difficulty(self, text: str) -> str:
        """개념난이도 결정"""
        if '정의' in text and len(text) < 200:
            return '교과서정의(하)'
        elif '응용' in text or '활용' in text:
            if '조합' in text or '복합' in text:
                return '창의융합(최상)'
            else:
                return '심화응용(상)'
        else:
            return '교과서응용(중)'
    
    def determine_prerequisites(self, text: str, subject: str) -> str:
        """필수선행개념 결정"""
        if '수학II' in text or '수2' in text:
            return '수학II'
        elif '수학I' in text or '수1' in text:
            return '수학I'
        elif len(text) < 150:
            return '없음'
        else:
            return '이전학년'
    
    def analyze_structure(self, problem_text: str) -> Dict:
        """문제 구조 분석"""
        result = {}
        
        # 문제형식
        if '선택' in problem_text or '①' in problem_text:
            if '계산' in problem_text:
                result['문제형식'] = '선택형(계산)'
            elif '이해' in problem_text:
                result['문제형식'] = '선택형(이해)'
            elif '추론' in problem_text:
                result['문제형식'] = '선택형(추론)'
            else:
                result['문제형식'] = '선택형(계산)'
        else:
            result['문제형식'] = '단답형'
        
        # 조건제시방식
        if '그래프' in problem_text or '그림' in problem_text:
            result['조건제시방식'] = '그래프제시'
        elif '표' in problem_text or '데이터' in problem_text:
            result['조건제시방식'] = '표/데이터'
        elif 'f(x)' in problem_text or '함수' in problem_text:
            result['조건제시방식'] = '함수정의'
        else:
            result['조건제시방식'] = '직접제시'
        
        # 풀이단계수
        steps = self.estimate_solving_steps(problem_text)
        result['풀이단계수'] = steps
        
        # 계산복잡도
        if steps <= 2:
            result['계산복잡도'] = '암산가능'
        elif steps <= 4:
            result['계산복잡도'] = '간단계산'
        elif steps <= 6:
            result['계산복잡도'] = '복잡계산'
        else:
            result['계산복잡도'] = '매우복잡'
        
        # 함정유형
        result['함정유형'] = self.determine_trap_type(problem_text)
        
        return result
    
    def estimate_solving_steps(self, text: str) -> int:
        """풀이단계수 추정"""
        base_steps = 3
        
        # 키워드로 단계 추가
        if '→' in text or '단계' in text:
            base_steps += 2
        if '조건' in text and '구하기' in text:
            base_steps += 1
        if '증명' in text or '설명' in text:
            base_steps += 2
        
        return min(8, max(2, base_steps))
    
    def determine_trap_type(self, text: str) -> str:
        """함정유형 결정"""
        if '특수' in text or '경우' in text:
            return '특수경우형'
        elif '부호' in text or '+' in text and '-' in text:
            return '부호실수형'
        elif '조건' in text and len(text) > 300:
            return '복합함정형'
        elif '조건' in text:
            return '조건누락형'
        else:
            return '없음'
    
    def analyze_strategy(self, problem_text: str, answer_rate: float, problem_number: int) -> Dict:
        """출제 전략 분석"""
        result = {}
        
        # 출제의도
        if answer_rate >= 80:
            result['출제의도'] = '기본개념확인'
        elif answer_rate >= 50:
            result['출제의도'] = '계산능력측정'
        elif answer_rate >= 30:
            result['출제의도'] = '변별력확보'
        else:
            result['출제의도'] = '창의력평가'
        
        # 출제빈도
        if problem_number <= 15:
            result['출제빈도'] = '매년필수'
        elif problem_number <= 22:
            result['출제빈도'] = '자주출제'
        elif problem_number <= 28:
            result['출제빈도'] = '가끔출제'
        else:
            result['출제빈도'] = '드물게'
        
        # 연계여부
        result['연계여부'] = '미상'
        
        # 변별력지수
        if answer_rate >= 80:
            result['변별력지수'] = '변별없음'
        elif answer_rate >= 50:
            result['변별력지수'] = '하위권변별'
        elif answer_rate >= 30:
            result['변별력지수'] = '중위권변별'
        else:
            result['변별력지수'] = '상위권변별'
        
        # 킬러여부판정
        if answer_rate >= 40:
            result['킬러여부판정'] = '일반문항'
        elif answer_rate >= 30:
            result['킬러여부판정'] = '준킬러'
        elif answer_rate >= 20:
            result['킬러여부판정'] = '킬러'
        else:
            result['킬러여부판정'] = '슈퍼킬러'
        
        return result
    
    def analyze_all_pdfs(self):
        """모든 PDF 파일 분석"""
        if not PDF_LIBRARY:
            print("[오류] PDF 읽기 라이브러리가 설치되어 있지 않습니다.")
            print("설치: pip install pdfplumber pymupdf PyPDF2")
            return
        
        pdf_files = list(self.base_dir.glob('*.pdf'))
        
        if not pdf_files:
            print(f"[오류] PDF 파일을 찾을 수 없습니다: {self.base_dir}")
            return
        
        print(f"[시작] 총 {len(pdf_files)}개 PDF 파일 분석 시작\n")
        
        all_results = []
        
        for i, pdf_path in enumerate(pdf_files, 1):
            print(f"[{i}/{len(pdf_files)}] {pdf_path.name} 분석 중...")
            
            try:
                # 파일 정보 추출
                file_info = self.parse_filename(pdf_path.name)
                
                # PDF 텍스트 추출
                text = self.extract_text_from_pdf(pdf_path)
                
                if not text:
                    print(f"  [경고] 텍스트 추출 실패")
                    continue
                
                # 문제 추출
                problems = self.extract_problems(text)
                
                print(f"  [발견] {len(problems)}개 문제 추출")
                
                # 각 문제 분석
                for problem in problems:
                    analysis = self.analyze_problem_meta(
                        problem, file_info, problem['full_text']
                    )
                    all_results.append(analysis)
                
                print(f"  [완료] {len(problems)}개 문제 분석 완료\n")
                
            except Exception as e:
                print(f"  [오류] {e}\n")
                continue
        
        # 결과 저장
        self.save_results(all_results)
        
        print(f"\n[완료] 총 {len(all_results)}개 문제 분석 완료")
        print(f"결과 저장 위치: {self.output_dir}")
    
    def save_results(self, results: List[Dict]):
        """결과를 CSV로 저장"""
        if not results:
            print("[경고] 저장할 결과가 없습니다.")
            return
        
        # CSV 헤더 (25개 항목 순서대로)
        headers = [
            '출제년도', '시행월', '문항번호', '배점', '과목구분',
            '공식정답률', '난이도등급', '풀이소요시간', '오답률1위선지', '체감난이도',
            '대단원', '중단원', '핵심개념태그', '개념난이도', '필수선행개념',
            '문제형식', '조건제시방식', '풀이단계수', '계산복잡도', '함정유형',
            '출제의도', '출제빈도', '연계여부', '변별력지수', '킬러여부판정'
        ]
        
        # CSV 파일 저장
        csv_path = self.output_dir / 'csat_meta_analysis.csv'
        with open(csv_path, 'w', encoding='utf-8-sig', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            for result in results:
                writer.writerow(result)
        
        print(f"[저장] CSV 파일: {csv_path}")
        
        # JSON 파일도 저장 (상세 정보용)
        json_path = self.output_dir / 'csat_meta_analysis.json'
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        print(f"[저장] JSON 파일: {json_path}")

if __name__ == '__main__':
    analyzer = CSATMetaAnalyzer()
    analyzer.analyze_all_pdfs()
