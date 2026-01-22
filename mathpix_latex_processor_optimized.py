# mathpix_latex_processor_optimized.py
# Mathpix LaTeX 자동 처리 시스템 (최적화 버전 - 더 빠른 처리)

import re
import sys
import os
from pathlib import Path
from functools import lru_cache
from concurrent.futures import ThreadPoolExecutor, as_completed
from latex_utils import (
    extract_body, extract_options_generic, clean_latex_text
)
from convert_template import review_problems, save_for_deepseek

# Windows 콘솔 인코딩 설정
if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')


class OptimizedMathpixProcessor:
    """최적화된 Mathpix LaTeX 처리 클래스"""
    
    def __init__(self, latex_content, output_dir, base_filename, auto_diagnose=False):
        self.latex_content = latex_content
        self.output_dir = output_dir
        self.base_filename = base_filename
        self.body = extract_body(latex_content)
        self.problems = []
        self.auto_diagnose = auto_diagnose
        
        # 사전 컴파일된 정규식 (더 빠른 매칭)
        self.point_pattern = re.compile(r'\[([34])점\]|［([34])점］')
        self.options_pattern = re.compile(r'\([1-5]\)|①|②|③|④|⑤')
        self.section_pattern = re.compile(r'\\section\*?\{[^}]*\}')
        
        if auto_diagnose:
            self._quick_diagnose()
    
    def _quick_diagnose(self):
        """빠른 진단 (최소한의 정보만)"""
        print(f"[진단] 본문 길이: {len(self.body)}자")
        point_count = len(self.point_pattern.findall(self.body))
        print(f"[진단] 점수 마커: {point_count}개")
    
    @lru_cache(maxsize=100)
    def _detect_topic_cached(self, body_snippet):
        """주제 감지 (캐싱)"""
        topics = {
            '수열': ['수열', '등차수열', '등비수열', 'Chapter 3'],
            '기하': ['삼각형', '원', '선분', '각', '기하'],
            '삼각함수': ['삼각함수', 'sin', 'cos', 'tan'],
            '미적분': ['미분', '적분', '도함수'],
        }
        
        for topic, keywords in topics.items():
            if any(keyword in body_snippet for keyword in keywords):
                return topic
        return "기타"
    
    def _extract_single_problem(self, marker_pos, marker_point, body, problem_index, sections=None):
        """단일 문제 추출 (병렬 처리용) - 개선 버전"""
        try:
            # 이전 마커 찾기
            prev_marker = None
            for pattern in [r'\[4점\]', r'［4점］', r'\[3점\]', r'［3점］']:
                matches = list(re.finditer(pattern, body[:marker_pos]))
                if matches:
                    prev_marker = matches[-1].start()
                    break
            
            # 다음 마커 찾기
            next_marker = None
            for pattern in [r'\[4점\]', r'［4점］', r'\[3점\]', r'［3점］']:
                match = re.search(pattern, body[marker_pos + 50:])
                if match:
                    next_marker = marker_pos + 50 + match.start()
                    break
            
            # 보기 문제 확인 (경계 찾기 전에)
            check_text = body[max(0, marker_pos-200):marker_pos+200]
            is_boogi_problem = '고른 것은' in check_text or '〈보기〉' in check_text
            
            # 문제 경계 찾기 (개선된 함수 사용)
            from mathpix_utils import find_problem_boundaries
            start, end = find_problem_boundaries(
                body, marker_pos, 
                prev_marker_pos=prev_marker, 
                next_marker_pos=next_marker,
                sections=sections,
                is_boogi_problem=is_boogi_problem
            )
            
            problem_text = body[start:end]
            
            # 보기 문제 확인 ("고른 것은?"이 있으면 객관식)
            is_boogi_problem = is_boogi_problem or '〈보기〉' in problem_text or '보기' in problem_text or '고른 것은' in problem_text
            
            # 선택지 확인 (사전 컴파일된 패턴 사용)
            has_options = bool(self.options_pattern.search(problem_text))
            
            # 주관식/객관식 판단 개선
            if '고른 것은' in problem_text or is_boogi_problem:
                # 보기 문제는 무조건 객관식
                has_options = True
            elif '구하시오' in problem_text:
                # options_text에서 선택지 패턴이 실제로 있는지 확인
                actual_options = self.options_pattern.findall(problem_text)
                if len(actual_options) == 0:
                    has_options = False
            
            # 문제 본문 추출
            question_end = problem_text.find('[4점]')
            if question_end == -1:
                question_end = problem_text.find('［4점］')
            if question_end == -1:
                question_end = problem_text.find('[3점]')
            if question_end == -1:
                question_end = problem_text.find('［3점］')
            
            if question_end == -1:
                question = problem_text.strip()
                options_text = ""
            else:
                question = problem_text[:question_end].strip()
                options_text = problem_text[question_end:] if has_options else ""
            
            # 텍스트 정리 (개선된 함수 사용)
            from mathpix_utils import clean_problem_text
            question = clean_problem_text(question, body_context=body, problem_start=start)
            
            if len(question) < 30:
                return None
            
            # 주제 감지 (개선된 함수 사용)
            from mathpix_utils import detect_topic_from_content
            topic = detect_topic_from_content(problem_text[:200])
            
            # 선택지 추출 (보기 문제 처리 개선)
            options = []
            if has_options and options_text:
                # 보기 문제 확인
                if '〈보기〉' in options_text or '보기' in question or '\\section\\*\\{〈보기〉' in options_text or is_boogi_problem:
                    from mathpix_utils import extract_boogi_options
                    # 보기 문제는 선택지가 다음 섹션에 있을 수 있으므로 확장 검색
                    if next_marker:
                        extended_search = body[start:min(next_marker, end + 500)]
                    else:
                        extended_search = body[start:min(len(body), end + 500)]
                    options, boogi_content = extract_boogi_options(options_text, extended_search_text=extended_search)
                    if boogi_content:
                        question += f" 〈보기〉 {boogi_content}"
                else:
                    options = extract_options_generic(options_text, num_options=5)
                    
                # 선택지가 제대로 추출되지 않았고 "구하시오"가 있으면 주관식으로 변경
                if len(options) == 0 and '구하시오' in question:
                    has_options = False
            
            # 문제 객체 생성
            if has_options and len(options) > 0:
                return {
                    "index": f"{problem_index:02d}",
                    "page": (problem_index // 2) + 1,
                    "topic": topic,
                    "question": question,
                    "point": marker_point,
                    "answer_type": "multiple_choice",
                    "options": options
                }
            elif len(question) > 50:
                return {
                    "index": f"{problem_index:02d}",
                    "page": (problem_index // 2) + 1,
                    "topic": topic,
                    "question": question,
                    "point": marker_point,
                    "answer_type": "short_answer"
                }
            
            return None
        except Exception as e:
            print(f"[경고] 문제 {problem_index} 추출 중 오류: {e}")
            return None
    
    def extract_problems_parallel(self, max_workers=4):
        """병렬 처리로 모든 문제 추출 (더 빠름) - 개선 버전"""
        print("[병렬 문제 추출 시작]")
        
        # 모든 점수 마커 찾기 (사전 컴파일된 패턴 사용)
        markers = []
        for match in self.point_pattern.finditer(self.body):
            point = int(match.group(1) or match.group(2))
            markers.append((match.start(), point))
        
        # 섹션 헤더 위치 찾기 (개선)
        sections = []
        for match in self.section_pattern.finditer(self.body):
            sections.append(match.start())
        
        print(f"[발견] {len(markers)}개의 점수 마커, {len(sections)}개의 섹션")
        
        if not markers:
            return []
        
        # 병렬 처리로 문제 추출
        problems = []
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(
                    self._extract_single_problem,
                    pos, point, self.body, i+1, sections
                ): (i+1, pos, point)
                for i, (pos, point) in enumerate(markers)
            }
            
            # 결과 수집 (순서 보장)
            results = {}
            for future in as_completed(futures):
                problem_index, pos, point = futures[future]
                try:
                    problem = future.result()
                    if problem:
                        results[problem_index] = problem
                except Exception as e:
                    print(f"[경고] 문제 {problem_index} 처리 중 오류: {e}")
            
            # 인덱스 순서로 정렬
            problems = [results[i] for i in sorted(results.keys())]
        
        return problems
    
    def extract_problems_fast(self):
        """빠른 순차 처리 (병렬 오버헤드 없음) - 개선 버전"""
        print("[빠른 문제 추출 시작]")
        
        # 모든 점수 마커 찾기
        markers = []
        for match in self.point_pattern.finditer(self.body):
            point = int(match.group(1) or match.group(2))
            markers.append((match.start(), point))
        
        # 섹션 헤더 위치 찾기 (개선)
        sections = []
        for match in self.section_pattern.finditer(self.body):
            sections.append(match.start())
        
        print(f"[발견] {len(markers)}개의 점수 마커, {len(sections)}개의 섹션")
        
        if not markers:
            return []
        
        problems = []
        for i, (pos, point) in enumerate(markers):
            problem = self._extract_single_problem(pos, point, self.body, i+1, sections)
            if problem:
                problems.append(problem)
        
        return problems
    
    def process(self, mode='fast', max_workers=4):
        """LaTeX 처리 메인 함수"""
        print("=" * 60)
        print(f"[Mathpix LaTeX 처리 (최적화)] {self.base_filename}")
        print("=" * 60)
        
        # 문제 추출
        if mode == 'parallel':
            self.problems = self.extract_problems_parallel(max_workers=max_workers)
        else:  # 'fast' 모드 (기본)
            self.problems = self.extract_problems_fast()
        
        print(f"\n[추출 완료] {len(self.problems)}개 문제")
        
        # 검토 (간소화)
        is_valid = review_problems(self.problems)
        
        # 자동 저장 (검토 통과 시)
        if is_valid or len(self.problems) > 0:
            save_for_deepseek(self.problems, self.output_dir, self.base_filename)
            print(f"\n[완료] 저장 위치: {self.output_dir}")
        
        return self.problems


def quick_process_mathpix_latex_optimized(latex_content, output_dir, base_filename, 
                                         mode='fast', max_workers=4, debug=False):
    """
    Mathpix LaTeX 빠른 처리 함수 (최적화 버전)
    
    Args:
        latex_content: Mathpix에서 온 LaTeX 내용
        output_dir: 출력 디렉토리
        base_filename: 기본 파일명
        mode: 'fast' (순차, 빠름) 또는 'parallel' (병렬, 더 빠름)
        max_workers: 병렬 모드일 때 워커 수 (기본 4)
        debug: 진단 모드 활성화 여부
    
    Returns:
        추출된 문제 리스트
    """
    processor = OptimizedMathpixProcessor(
        latex_content, output_dir, base_filename, 
        auto_diagnose=debug
    )
    
    return processor.process(mode=mode, max_workers=max_workers)


if __name__ == '__main__':
    print("Mathpix LaTeX 처리 시스템 (최적화 버전)")
    print("사용법: quick_process_mathpix_latex_optimized() 함수 사용")
    print("\n모드:")
    print("  - 'fast': 순차 처리 (빠름, 기본)")
    print("  - 'parallel': 병렬 처리 (더 빠름, CPU 사용량 증가)")
