# analyze_csat_deep.py
# 수능 수학 문제 심층 메타분석 (AI 활용)
# 제공된 프롬프트 기준에 따른 최고 수준 분석

import os
import re
import csv
import json
from pathlib import Path
from typing import Dict, List, Optional
import sys

# AI 분석을 위한 프롬프트 템플릿
META_ANALYSIS_PROMPT = """당신은 대한민국 수능 수학 출제 경향을 20년간 연구한 최고 전문가입니다.
아래 수능 문제를 25개 메타 분류 기준으로 심도 있게 분석하세요.

[문제 내용]
{problem_text}

[파일 정보]
- 출제년도: {year}
- 과목: {subject}
- 문항번호: {number}

[25개 메타 분류 기준]

A. 출제 식별 정보 (5개)
1. 출제년도: {year}
2. 시행월: {exam_month} (수능은 11월)
3. 문항번호: {number}
4. 배점: [문제에서 찾기 또는 추정]
5. 과목구분: {subject}

B. 난이도 지표 (5개)
6. 공식정답률: XX.X% (보수적으로 추정)
7. 난이도등급: 1등급컷용/2-3등급용/4-6등급용/변별용/킬러용
8. 풀이소요시간: X분 (중위권 4등급 학생 기준)
9. 오답률1위선지: ①/②/③/④/⑤ 또는 미상
10. 체감난이도: (풀이시간 × 100) / 정답률

C. 개념 분류 (5개)
11. 대단원: {subject}
12. 중단원: 세부 중단원명 (교과서 기준)
13. 핵심개념태그: 단일개념/융합개념/복합개념
14. 개념난이도: 교과서정의(하)/교과서응용(중)/심화응용(상)/창의융합(최상)
15. 필수선행개념: 없음/이전학년/다른단원/다른과목

D. 문제 구조 분석 (5개)
16. 문제형식: 단답형/선택형(계산)/선택형(이해)/선택형(추론)/선택형(증명)
17. 조건제시방식: 직접제시/함수정의/그래프제시/표/데이터/복합조건
18. 풀이단계수: 1-2단계/3-4단계/5-6단계/7단계+
19. 계산복잡도: 암산가능/간단계산/복잡계산/매우복잡
20. 함정유형: 없음/조건누락형/특수경우형/부호실수형/복합함정형

E. 출제 전략 분석 (5개)
21. 출제의도: 기본개념확인/계산능력측정/개념이해평가/응용능력측정/변별력확보/창의력평가
22. 출제빈도: 매년필수/자주출제/가끔출제/드물게/신유형
23. 연계여부: EBS 수특 연계/EBS 수완 연계/비연계/간접연계/미상
24. 변별력지수: 상위권변별/중위권변별/하위권변별/전체변별/변별없음
25. 킬러여부판정: 일반문항/준킬러/킬러/슈퍼킬러

[출력 형식]
JSON 형식으로 25개 항목을 모두 채워서 출력하세요.
각 항목에 대한 판단 근거도 간단히 포함하세요.

{
  "출제년도": "...",
  "시행월": "...",
  "문항번호": ...,
  "배점": ...,
  "과목구분": "...",
  "공식정답률": "XX.X%",
  "난이도등급": "...",
  "풀이소요시간": "X분",
  "오답률1위선지": "...",
  "체감난이도": "XX.X",
  "대단원": "...",
  "중단원": "...",
  "핵심개념태그": "...",
  "개념난이도": "...",
  "필수선행개념": "...",
  "문제형식": "...",
  "조건제시방식": "...",
  "풀이단계수": "...",
  "계산복잡도": "...",
  "함정유형": "...",
  "출제의도": "...",
  "출제빈도": "...",
  "연계여부": "...",
  "변별력지수": "...",
  "킬러여부판정": "...",
  "판단근거": "..."
}
"""

class DeepCSATAnalyzer:
    """심층 수능 메타분석 시스템"""
    
    def __init__(self):
        self.base_dir = Path(r'C:\Users\a\Documents\MathPDF\organized\기출')
        self.output_dir = Path(r'C:\Users\a\Documents\Aramed_AI\output')
        self.output_dir.mkdir(exist_ok=True)
        
        # 기본 분석 결과 로드
        self.basic_results = self.load_basic_results()
    
    def load_basic_results(self) -> List[Dict]:
        """기본 분석 결과 로드"""
        csv_path = self.output_dir / 'csat_meta_analysis.csv'
        if not csv_path.exists():
            return []
        
        results = []
        with open(csv_path, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                results.append(row)
        return results
    
    def extract_text_from_pdf(self, pdf_path: Path) -> str:
        """PDF에서 텍스트 추출"""
        try:
            import pdfplumber
            text_parts = []
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        text_parts.append(text)
            return '\n'.join(text_parts)
        except:
            try:
                import fitz
                doc = fitz.open(pdf_path)
                text_parts = [page.get_text() for page in doc]
                doc.close()
                return '\n'.join(text_parts)
            except:
                return ""
    
    def extract_problem_text(self, full_text: str, problem_number: int) -> str:
        """특정 문제 번호의 텍스트 추출"""
        # 문제 번호 패턴
        pattern = re.compile(rf'^{problem_number}\.\s+', re.MULTILINE)
        match = pattern.search(full_text)
        
        if not match:
            return ""
        
        start_pos = match.start()
        
        # 다음 문제 번호 찾기
        next_pattern = re.compile(rf'^{problem_number + 1}\.\s+', re.MULTILINE)
        next_match = next_pattern.search(full_text, start_pos)
        
        if next_match:
            end_pos = next_match.start()
        else:
            # 마지막 문제인 경우
            end_pos = len(full_text)
        
        return full_text[start_pos:end_pos].strip()
    
    def analyze_with_ai(self, problem_text: str, file_info: Dict, problem_number: int) -> Dict:
        """AI를 활용한 심층 분석"""
        # 실제로는 AI API를 호출해야 하지만, 여기서는 향상된 규칙 기반 분석 사용
        # 나중에 Claude/GPT API 연동 가능
        
        analysis = {}
        
        # A. 출제 식별 정보
        analysis['출제년도'] = file_info.get('year', '미상')
        analysis['시행월'] = file_info.get('exam_month', '11월')
        analysis['문항번호'] = problem_number
        
        # 배점 추정 (더 정확하게)
        score_match = re.search(r'\[(\d+)점\]', problem_text)
        if score_match:
            analysis['배점'] = int(score_match.group(1))
        else:
            # 문항번호 기반 정확한 추정
            if problem_number <= 15:
                analysis['배점'] = 2
            elif problem_number <= 22:
                analysis['배점'] = 3
            else:
                analysis['배점'] = 4
        
        analysis['과목구분'] = file_info.get('subject', '미상')
        
        # B. 난이도 지표 (더 정확한 추정)
        answer_rate = self.estimate_answer_rate_advanced(problem_text, problem_number)
        analysis['공식정답률'] = f"{answer_rate:.1f}%"
        analysis['난이도등급'] = self.determine_difficulty_grade(answer_rate)
        
        solving_time = self.estimate_solving_time_advanced(problem_text, problem_number)
        analysis['풀이소요시간'] = f"{solving_time}분"
        analysis['오답률1위선지'] = '미상'  # 실제 통계 필요
        analysis['체감난이도'] = f"{(solving_time * 100) / answer_rate:.1f}" if answer_rate > 0 else "0"
    
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
        
        # C. 개념 분류 (더 정확하게)
        concept_info = self.analyze_concepts_advanced(problem_text, analysis['과목구분'])
        analysis.update(concept_info)
        
        # D. 문제 구조 (더 정확하게)
        structure_info = self.analyze_structure_advanced(problem_text)
        analysis.update(structure_info)
        
        # E. 출제 전략 (더 정확하게)
        strategy_info = self.analyze_strategy_advanced(problem_text, answer_rate, problem_number)
        analysis.update(strategy_info)
        
        return analysis
    
    def estimate_answer_rate_advanced(self, problem_text: str, problem_number: int) -> float:
        """정답률 고급 추정"""
        # 기본 추정
        if problem_number <= 15:
            base = 92.0 - (problem_number - 1) * 1.5
        elif problem_number <= 22:
            base = 75.0 - (problem_number - 16) * 4
        elif problem_number <= 28:
            base = 55.0 - (problem_number - 23) * 4
        else:
            base = 25.0 - (problem_number - 29) * 5
        
        # 복잡도 조정
        complexity_penalty = 0
        
        # 고난도 키워드
        if any(kw in problem_text for kw in ['극한', '미분', '적분', '함수']):
            complexity_penalty += 3
        if '그래프' in problem_text:
            complexity_penalty += 2
        if '증명' in problem_text or '설명' in problem_text:
            complexity_penalty += 5
        if len(problem_text) > 400:
            complexity_penalty += 2
        if '조건' in problem_text and problem_text.count('조건') > 2:
            complexity_penalty += 3
        
        return max(5.0, min(95.0, base - complexity_penalty))
    
    def estimate_solving_time_advanced(self, problem_text: str, problem_number: int) -> int:
        """풀이시간 고급 추정"""
        # 기본 시간
        if problem_number <= 15:
            base = 2
        elif problem_number <= 22:
            base = 4
        elif problem_number <= 28:
            base = 6
        else:
            base = 8
        
        # 복잡도 추가
        if '계산' in problem_text:
            base += 1
        if '그래프' in problem_text:
            base += 1
        if '증명' in problem_text:
            base += 2
        if '추론' in problem_text:
            base += 2
        if '함수' in problem_text:
            base += 1
        if '미분' in problem_text or '적분' in problem_text:
            base += 1
        if '극한' in problem_text:
            base += 1
        
        # 텍스트 길이
        if len(problem_text) > 300:
            base += 1
        if len(problem_text) > 500:
            base += 1
        
        return min(10, max(1, base))
    
    def analyze_concepts_advanced(self, problem_text: str, subject: str) -> Dict:
        """개념 분류 고급 분석"""
        result = {}
        result['대단원'] = subject
        
        # 중단원 정확히 추정
        minor_unit_map = {
            '미적분': {
                '수열의극한': ['수열', '극한', '급수'],
                '미분법': ['미분', '도함수', '접선'],
                '적분법': ['적분', '넓이', '부피']
            },
            '기하': {
                '이차곡선': ['포물선', '타원', '쌍곡선'],
                '평면벡터': ['벡터', '내적', '외적'],
                '공간도형': ['공간', '도형', '좌표']
            },
            '확률과통계': {
                '경우의수': ['경우', '순열', '조합'],
                '확률': ['확률', '사건', '조건부'],
                '통계': ['평균', '분산', '표준편차']
            }
        }
        
        result['중단원'] = '미상'
        if subject in minor_unit_map:
            best_match = None
            best_score = 0
            for unit, keywords in minor_unit_map[subject].items():
                score = sum(1 for kw in keywords if kw in problem_text)
                if score > best_score:
                    best_score = score
                    best_match = unit
            if best_match:
                result['중단원'] = best_match
        
        # 핵심개념태그
        concept_count = self.count_concepts_advanced(problem_text)
        if concept_count == 1:
            result['핵심개념태그'] = '단일개념'
        elif concept_count == 2:
            result['핵심개념태그'] = '융합개념'
        else:
            result['핵심개념태그'] = '복합개념'
        
        # 개념난이도
        result['개념난이도'] = self.determine_concept_difficulty_advanced(problem_text)
        
        # 필수선행개념
        result['필수선행개념'] = self.determine_prerequisites_advanced(problem_text, subject)
        
        return result
    
    def count_concepts_advanced(self, text: str) -> int:
        """핵심 개념 개수 고급 추정"""
        concepts = set()
        
        concept_keywords = {
            '함수': ['함수', 'f(x)', 'g(x)'],
            '미분': ['미분', '도함수', 'f\'(x)'],
            '적분': ['적분', '∫', '넓이'],
            '극한': ['극한', 'lim', '수렴'],
            '수열': ['수열', '등차', '등비'],
            '확률': ['확률', 'P(', '사건'],
            '통계': ['평균', '분산', '표준편차'],
            '벡터': ['벡터', '내적', '외적'],
            '곡선': ['포물선', '타원', '쌍곡선'],
            '로그': ['로그', 'log'],
            '지수': ['지수', 'a^x'],
            '삼각': ['삼각', 'sin', 'cos', 'tan']
        }
        
        for concept, keywords in concept_keywords.items():
            if any(kw in text for kw in keywords):
                concepts.add(concept)
        
        return len(concepts) if concepts else 1
    
    def determine_concept_difficulty_advanced(self, text: str) -> str:
        """개념난이도 고급 결정"""
        # 복잡도 지표
        has_definition = '정의' in text and len(text) < 200
        has_application = '응용' in text or '활용' in text
        has_combination = '조합' in text or '복합' in text or '융합' in text
        is_complex = len(text) > 400 and ('추론' in text or '증명' in text)
        
        if has_definition and not has_application:
            return '교과서정의(하)'
        elif has_combination or is_complex:
            return '창의융합(최상)'
        elif has_application:
            return '심화응용(상)'
        else:
            return '교과서응용(중)'
    
    def determine_prerequisites_advanced(self, text: str, subject: str) -> str:
        """필수선행개념 고급 결정"""
        if '수학II' in text or '수2' in text:
            return '수학II'
        elif '수학I' in text or '수1' in text:
            return '수학I'
        elif subject == '미적분' and ('함수' in text or '극한' in text):
            return '수학II'
        elif len(text) < 150 and '정의' in text:
            return '없음'
        else:
            return '이전학년'
    
    def analyze_structure_advanced(self, problem_text: str) -> Dict:
        """문제 구조 고급 분석"""
        result = {}
        
        # 문제형식
        if '①' in problem_text or '②' in problem_text:
            if '계산' in problem_text or '값' in problem_text:
                result['문제형식'] = '선택형(계산)'
            elif '이해' in problem_text or '의미' in problem_text:
                result['문제형식'] = '선택형(이해)'
            elif '추론' in problem_text or '논리' in problem_text:
                result['문제형식'] = '선택형(추론)'
            elif '증명' in problem_text or '참' in problem_text and '거짓' in problem_text:
                result['문제형식'] = '선택형(증명)'
            else:
                result['문제형식'] = '선택형(계산)'
        else:
            result['문제형식'] = '단답형'
        
        # 조건제시방식
        if '그래프' in problem_text or '그림' in problem_text:
            if '함수' in problem_text or 'f(x)' in problem_text:
                result['조건제시방식'] = '복합조건'
            else:
                result['조건제시방식'] = '그래프제시'
        elif '표' in problem_text or '데이터' in problem_text:
            result['조건제시방식'] = '표/데이터'
        elif 'f(x)' in problem_text or '함수' in problem_text and '=' in problem_text:
            result['조건제시방식'] = '함수정의'
        elif '함수' in problem_text or '=' in problem_text:
            result['조건제시방식'] = '직접제시'
        else:
            result['조건제시방식'] = '직접제시'
        
        # 풀이단계수
        steps = self.estimate_solving_steps_advanced(problem_text)
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
        result['함정유형'] = self.determine_trap_type_advanced(problem_text)
        
        return result
    
    def estimate_solving_steps_advanced(self, text: str) -> int:
        """풀이단계수 고급 추정"""
        base = 3
        
        # 단계 지시어
        if '→' in text:
            base += text.count('→')
        if '단계' in text:
            base += 1
        if '조건' in text:
            base += text.count('조건') // 2
        if '구하기' in text or '찾기' in text:
            base += 1
        if '증명' in text:
            base += 2
        if '설명' in text:
            base += 1
        
        # 복잡도
        if len(text) > 300:
            base += 1
        if '함수' in text and '미분' in text:
            base += 1
        if '적분' in text:
            base += 1
        
        return min(8, max(2, base))
    
    def determine_trap_type_advanced(self, text: str) -> str:
        """함정유형 고급 결정"""
        trap_indicators = {
            '특수경우형': ['특수', '경우', '예외'],
            '부호실수형': ['부호', '+', '-', '양수', '음수'],
            '조건누락형': ['조건', '단', '단,'],
            '복합함정형': ['조건', '특수', '부호']
        }
        
        scores = {}
        for trap_type, keywords in trap_indicators.items():
            score = sum(1 for kw in keywords if kw in text)
            if score > 0:
                scores[trap_type] = score
        
        if not scores:
            return '없음'
        
        # 가장 높은 점수의 함정 유형
        best_trap = max(scores.items(), key=lambda x: x[1])
        if best_trap[1] >= 2:
            return best_trap[0]
        elif '조건' in text and len(text) > 300:
            return '복합함정형'
        elif '조건' in text:
            return '조건누락형'
        else:
            return '없음'
    
    def analyze_strategy_advanced(self, problem_text: str, answer_rate: float, problem_number: int) -> Dict:
        """출제 전략 고급 분석"""
        result = {}
        
        # 출제의도
        if answer_rate >= 85:
            result['출제의도'] = '기본개념확인'
        elif answer_rate >= 60:
            result['출제의도'] = '계산능력측정'
        elif answer_rate >= 40:
            result['출제의도'] = '개념이해평가'
        elif answer_rate >= 25:
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
    
    def run_deep_analysis(self):
        """심층 분석 실행"""
        pdf_files = list(self.base_dir.glob('*.pdf'))
        
        if not pdf_files:
            print(f"[오류] PDF 파일을 찾을 수 없습니다: {self.base_dir}")
            return
        
        print(f"[심층 분석 시작] 총 {len(pdf_files)}개 PDF 파일\n")
        
        all_results = []
        
        for i, pdf_path in enumerate(pdf_files, 1):
            print(f"[{i}/{len(pdf_files)}] {pdf_path.name} 심층 분석 중...")
            
            try:
                # 파일 정보
                year_match = re.search(r'(\d{4})학년도', pdf_path.name)
                year = year_match.group(1) if year_match else '미상'
                
                subject = '미상'
                if '기하' in pdf_path.name:
                    subject = '기하'
                elif '미적' in pdf_path.name:
                    subject = '미적분'
                elif '확률' in pdf_path.name:
                    subject = '확률과통계'
                
                file_info = {
                    'year': year,
                    'subject': subject,
                    'exam_month': '11월'
                }
                
                # PDF 텍스트 추출
                text = self.extract_text_from_pdf(pdf_path)
                
                if not text:
                    print(f"  [경고] 텍스트 추출 실패")
                    continue
                
                # 문제 번호 추출
                problem_numbers = re.findall(r'^(\d+)\.\s+', text, re.MULTILINE)
                problem_numbers = [int(n) for n in problem_numbers if n.isdigit()]
                problem_numbers = sorted(set(problem_numbers))
                
                print(f"  [발견] {len(problem_numbers)}개 문제")
                
                # 각 문제 심층 분석
                for num in problem_numbers:
                    problem_text = self.extract_problem_text(text, num)
                    
                    if not problem_text:
                        continue
                    
                    analysis = self.analyze_with_ai(problem_text, file_info, num)
                    all_results.append(analysis)
                
                print(f"  [완료] {len(problem_numbers)}개 문제 심층 분석 완료\n")
                
            except Exception as e:
                print(f"  [오류] {e}\n")
                import traceback
                traceback.print_exc()
                continue
        
        # 결과 저장
        self.save_deep_results(all_results)
        
        print(f"\n[완료] 총 {len(all_results)}개 문제 심층 분석 완료")
        print(f"결과 저장 위치: {self.output_dir}")
    
    def save_deep_results(self, results: List[Dict]):
        """심층 분석 결과 저장"""
        if not results:
            return
        
        headers = [
            '출제년도', '시행월', '문항번호', '배점', '과목구분',
            '공식정답률', '난이도등급', '풀이소요시간', '오답률1위선지', '체감난이도',
            '대단원', '중단원', '핵심개념태그', '개념난이도', '필수선행개념',
            '문제형식', '조건제시방식', '풀이단계수', '계산복잡도', '함정유형',
            '출제의도', '출제빈도', '연계여부', '변별력지수', '킬러여부판정'
        ]
        
        csv_path = self.output_dir / 'csat_deep_analysis.csv'
        with open(csv_path, 'w', encoding='utf-8-sig', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            for result in results:
                if result:  # None 체크
                    # 모든 필드가 있는지 확인하고 없으면 기본값 추가
                    clean_result = {}
                    for header in headers:
                        clean_result[header] = result.get(header, '미상')
                    writer.writerow(clean_result)
        
        print(f"[저장] 심층 분석 CSV: {csv_path}")
        
        json_path = self.output_dir / 'csat_deep_analysis.json'
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        print(f"[저장] 심층 분석 JSON: {json_path}")

if __name__ == '__main__':
    analyzer = DeepCSATAnalyzer()
    analyzer.run_deep_analysis()
