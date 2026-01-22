# mathpix_latex_processor.py
# Mathpix LaTeX 자동 처리 시스템 (업데이트: 자동 저장 및 최적화)

import re
import sys
import os
from pathlib import Path
from latex_utils import (
    extract_body, diagnose_latex_structure, find_keyword_positions,
    extract_options_generic, extract_problem_with_options,
    clean_latex_text, test_pattern
)
from convert_template import review_problems, save_for_deepseek
from mathpix_utils import (
    detect_problem_type, detect_topic_from_content,
    extract_point_value, find_problem_boundaries,
    clean_problem_text, validate_problem_structure
)

# Windows 콘솔 인코딩 설정
if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')


class MathpixLatexProcessor:
    """Mathpix LaTeX 자동 처리 클래스"""
    
    def __init__(self, latex_content, output_dir, base_filename, auto_diagnose=True, auto_save=True):
        self.latex_content = latex_content
        self.output_dir = output_dir
        self.base_filename = base_filename
        self.body = extract_body(latex_content)
        self.problems = []
        self.diagnosis = None
        self.auto_save = auto_save  # 자동 저장 옵션
        
        # 사전 컴파일된 정규식 (성능 향상)
        self.point_pattern = re.compile(r'\[([34])점\]|［([34])점］')
        self.options_pattern = re.compile(r'\([1-5]\)|①|②|③|④|⑤')
        
        if auto_diagnose:
            self.diagnose()
    
    def diagnose(self):
        """LaTeX 구조 자동 진단"""
        print("=" * 60)
        print("[Mathpix LaTeX 자동 진단]")
        print("=" * 60)
        self.diagnosis = {
            'body_length': len(self.body),
            'has_backslash_escape': '\\$' in self.body,
            'has_fullwidth_brackets': '［' in self.body or '（' in self.body,
            'has_sections': '\\section' in self.body,
            'has_images': '\\includegraphics' in self.body,
        }
        
        diagnose_latex_structure(self.body, max_chars=300)
        
        # 키워드 위치 찾기
        keywords = ['보기', 'section', 'Chapter', '문제', '해설']
        find_keyword_positions(self.body, keywords)
        
        print("\n[진단 요약]")
        for key, value in self.diagnosis.items():
            print(f"  {key}: {value}")
        print("=" * 60)
        print()
    
    def auto_detect_problem_patterns(self):
        """문제 패턴 자동 감지"""
        patterns = {
            'multiple_choice': [
                r'\(1\)\s*[\\$]',  # (1) 로 시작하는 선택지
                r'①\s*[\\$]',      # ① 로 시작하는 선택지
            ],
            'short_answer': [
                r'구하시오\.?\s*\[[0-9]점\]',  # "구하시오. [4점]"
                r'값은\?.*?\[[0-9]점\]',       # "값은? [4점]"
            ],
            'point_markers': [
                r'\[4점\]', r'\[3점\]', r'\[5점\]',
                r'［4점］', r'［3점］', r'［5점］',
            ]
        }
        
        detected = {}
        for pattern_type, pattern_list in patterns.items():
            detected[pattern_type] = []
            for pattern in pattern_list:
                if re.search(pattern, self.body):
                    detected[pattern_type].append(pattern)
        
        return detected
    
    def extract_problem_01_pattern(self):
        """문제 1번 추출 (첫 번째 문제, 일반적으로 문서 시작 부분)"""
        # Mathpix LaTeX의 일반적인 첫 문제 패턴
        # 시작: 문서 시작 또는 첫 번째 문제
        # 종료: \section 또는 \end
        
        # 패턴 1: $...$ 로 시작하는 문제
        pattern1 = r'(\\?\$[^$]+\\?\$.*?\[[0-9]점[\]］])(.*?)(?=\\section|\\end|\n\\section)'
        match = re.search(pattern1, self.body, re.DOTALL)
        
        if match:
            question = match.group(1).strip()
            options_text = match.group(2).strip() if match.lastindex >= 2 else ""
            
            question = clean_latex_text(question)
            
            # 선택지 추출
            options = extract_options_generic(options_text)
            
            if len(options) == 5:
                return {
                    "index": "01",
                    "page": 1,
                    "topic": self._detect_topic(),
                    "question": question,
                    "point": self._extract_point(question),
                    "answer_type": "multiple_choice",
                    "options": options
                }
            elif len(options) == 0:
                return {
                    "index": "01",
                    "page": 1,
                    "topic": self._detect_topic(),
                    "question": question,
                    "point": self._extract_point(question),
                    "answer_type": "short_answer"
                }
        
        return None
    
    def _detect_topic(self):
        """주제 자동 감지"""
        topics = {
            '지수함수': ['지수함수', 'a^{x}', 'a^x'],
            '로그함수': ['로그함수', '\\log', 'log'],
            '미분법': ['미분법', '도함수', '미분'],
            '적분법': ['적분법', '적분', '정적분'],
            '수열': ['수열', '급수', '극한'],
        }
        
        for topic, keywords in topics.items():
            for keyword in keywords:
                if keyword in self.body[:1000]:  # 처음 1000자만 확인
                    return topic
        
        return "기타"
    
    def _extract_point(self, question):
        """점수 추출"""
        point_match = re.search(r'\[([0-9])점[\]］]', question)
        if point_match:
            return int(point_match.group(1))
        return 4  # 기본값
    
    def smart_extract_all_problems(self, max_problems=20):
        """모든 문제를 스마트하게 추출"""
        print("[스마트 문제 추출 시작]")
        
        # 점수 마커로 문제 구분
        point_pattern = r'\[([0-9])점[\]］]'
        point_positions = []
        
        for match in re.finditer(point_pattern, self.body):
            point_positions.append({
                'pos': match.start(),
                'point': int(match.group(1)),
                'context': self.body[max(0, match.start()-50):match.end()+50]
            })
        
        print(f"[발견] {len(point_positions)}개의 점수 마커 발견")
        
        # 각 점수 마커 주변에서 문제 추출 시도
        problems_found = []
        for i, pos_info in enumerate(point_positions[:max_problems]):
            start = max(0, pos_info['pos'] - 500)
            end = min(len(self.body), pos_info['pos'] + 500)
            context = self.body[start:end]
            
            # 문제 시작 찾기 (역방향)
            problem_start = start
            for j in range(pos_info['pos'], max(0, pos_info['pos'] - 500), -1):
                if j > 0 and self.body[j-1] in ['\n', '\\']:
                    problem_start = j
                    break
            
            # 문제 끝 찾기
            problem_end = pos_info['pos'] + 200
            next_section = self.body.find('\\section', pos_info['pos'])
            if next_section != -1:
                problem_end = min(problem_end, next_section)
            
            problem_text = self.body[problem_start:problem_end]
            
            # 선택지 확인
            has_options = bool(re.search(r'\([1-5]\)|①|②|③|④|⑤', problem_text))
            
            # 문제 추출
            question = clean_latex_text(problem_text[:problem_text.find('[')])
            options = []
            if has_options:
                options_text = problem_text[problem_text.find('['):]
                options = extract_options_generic(options_text)
            
            if len(question) > 50:  # 최소 길이 확인
                problems_found.append({
                    "index": f"{i+1:02d}",
                    "page": (i // 2) + 1,
                    "topic": self._detect_topic(),
                    "question": question,
                    "point": pos_info['point'],
                    "answer_type": "multiple_choice" if len(options) == 5 else "short_answer",
                    "options": options if options else []
                })
        
        return problems_found
    
    def process(self, mode='auto', custom_extractor=None):
        """LaTeX 처리 메인 함수"""
        print("=" * 60)
        print(f"[Mathpix LaTeX 처리] {self.base_filename}")
        print("=" * 60)
        
        if mode == 'auto':
            # 자동 모드: 스마트 추출 시도
            self.problems = self.smart_extract_all_problems()
        elif custom_extractor:
            # 커스텀 추출기 사용
            self.problems = custom_extractor(self.body)
        else:
            # 수동 모드: extract_problems_from_latex 구현 필요
            print("[경고] 수동 모드이지만 추출기가 정의되지 않았습니다.")
            return
        
        print(f"\n[추출 완료] {len(self.problems)}개 문제")
        
        # 검토
        is_valid = review_problems(self.problems)
        
        # 저장 (자동 저장 옵션 추가)
        if is_valid or len(self.problems) > 0:
            save_for_deepseek(self.problems, self.output_dir, self.base_filename)
            print(f"\n[완료] 저장 위치: {self.output_dir}")
        else:
            print("\n[경고] 추출된 문제가 없거나 검토에 실패했습니다.")
        
        return self.problems


def quick_process_mathpix_latex(latex_content, output_dir, base_filename, 
                                custom_extractor=None, debug=True, auto_save=True):
    """
    Mathpix LaTeX 빠른 처리 함수
    
    사용법:
        from mathpix_latex_processor import quick_process_mathpix_latex
        
        # Mathpix에서 온 LaTeX 내용
        latex_content = "..."  
        output_dir = r"C:\\Users\\a\\Documents\\..."
        base_filename = "파일명"
        
        # 자동 모드
        problems = quick_process_mathpix_latex(latex_content, output_dir, base_filename)
        
        # 커스텀 추출기 사용
        def my_extractor(body):
            # 여기에 문제 추출 로직 작성
            return problems
        
        problems = quick_process_mathpix_latex(
            latex_content, output_dir, base_filename, 
            custom_extractor=my_extractor
        )
    """
    processor = MathpixLatexProcessor(
        latex_content, output_dir, base_filename, 
        auto_diagnose=debug, auto_save=auto_save
    )
    
    if custom_extractor:
        return processor.process(mode='custom', custom_extractor=custom_extractor)
    else:
        return processor.process(mode='auto')


if __name__ == '__main__':
    # 사용 예시
    print("Mathpix LaTeX 처리 시스템")
    print("사용법: quick_process_mathpix_latex() 함수 사용")
