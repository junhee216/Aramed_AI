# mathpix_utils.py
# Mathpix LaTeX 처리 공통 유틸리티 함수 (개선 버전)

import re
from pathlib import Path
from latex_utils import extract_body, clean_latex_text, extract_options_generic


def detect_problem_type(body_snippet):
    """문제 유형 자동 감지"""
    if re.search(r'\([1-5]\)|（[1-5]）|①|②|③|④|⑤', body_snippet):
        return "multiple_choice"
    elif re.search(r'구하시오|값은\?|값을 구하시오', body_snippet):
        return "short_answer"
    return "unknown"


def detect_topic_from_content(body_snippet):
    """본문 내용으로 주제 자동 감지 (개선 버전 - 확통 포함)"""
    topics = {
        '경우의 수': [
            '경우의 수', '순열', '조합', '원순열', '중복순열', '중복조합',
            '이웃', '이웃하지', '부정방정식', '음이 아닌 정수',
            '함수의 개수', '치역', '정의역'
        ],
        '확률': [
            '확률', '사건', '독립', '종속', '조건부확률', '여사건',
            '독립시행', '이항분포', 'P(', '확률변수'
        ],
        '통계': [
            '통계', '확률변수', '확률질량함수', '확률밀도함수',
            '평균', '분산', '표준편차', 'E(', 'V(',
            '정규분포', '표준정규분포', 'N('
        ],
        '함수의 극한과 연속': ['극한', '연속', '불연속', '\\lim', 'Chapter 1'],
        '미분': ['미분', '도함수', 'f\'', 'f^{\\prime}', 'Chapter 2'],
        '적분': ['적분', '\\int', '정적분', '부정적분', 'Chapter 3'],
        '수열': ['수열', '등차수열', '등비수열', 'Chapter 3', '점화식'],
        '기하': ['삼각형', '원', '선분', '각', '기하'],
        '삼각함수': ['삼각함수', 'sin', 'cos', 'tan'],
    }
    
    # 우선순위: 확통 > 미분 > 적분 > 극한과 연속
    priority_order = [
        '경우의 수', '확률', '통계',  # 확통 우선
        '미분', '적분', '함수의 극한과 연속', 
        '수열', '삼각함수', '기하'
    ]
    
    for topic in priority_order:
        if topic in topics:
            keywords = topics[topic]
            if any(keyword in body_snippet for keyword in keywords):
                return topic
    
    return "기타"


def extract_point_value(text):
    """점수 추출"""
    point_match = re.search(r'\[([34])점\]|［([34])점］', text)
    if point_match:
        return int(point_match.group(1) or point_match.group(2))
    return 4  # 기본값


def find_problem_boundaries(body, marker_pos, prev_marker_pos=None, next_marker_pos=None, sections=None, is_boogi_problem=False):
    """문제 경계 찾기 (개선 버전 - 섹션 헤더 활용, 보기 문제 지원)"""
    # 시작 위치
    if prev_marker_pos is not None:
        start = prev_marker_pos + 100
        # 이전 문제의 선택지 끝 찾기
        search_area = body[max(0, prev_marker_pos - 300):prev_marker_pos + 200]
        last_option_match = None
        for opt_num in range(5, 0, -1):
            pattern = rf'（{opt_num}）|\({opt_num}\)'
            match = re.search(pattern, search_area)
            if match:
                last_option_match = max(0, prev_marker_pos - 300) + match.end()
                break
        if last_option_match:
            start = last_option_match + 50
    else:
        start = max(0, marker_pos - 1500)
    
    # 섹션 헤더 위치 활용 (개선)
    if sections:
        for sec_pos in reversed(sections):
            if sec_pos < marker_pos and sec_pos >= start - 200:
                # 섹션 헤더 끝 찾기
                section_end = body.find('}', sec_pos)
                if section_end != -1:
                    # 섹션 이후에 문제 시작 패턴 찾기
                    after_section = body[section_end+1:marker_pos]
                    problem_start_patterns = [
                        r'다항함수 \$f\(x\)',
                        r'함수 \$f\(x\)',
                        r'삼차함수 \$f\(x\)',
                        r'이차함수 \$f\(x\)',
                        r'최고차항의 계수가',
                        r'상수 \$a',
                        r'최고차항의 계수가 양수',
                        r'최고차항의 계수가 1',
                        r'최고차항의 계수가 음수',
                        r'두 양수',
                        r'실수 전체의 집합',
                        r'\$0<a<1\$',
                    ]
                    for pattern in problem_start_patterns:
                        match = re.search(pattern, after_section)
                        if match:
                            start = section_end + 1 + match.start()
                            break
                    if start < section_end + 1:
                        start = section_end + 1
                break
    
    # 문제 시작 패턴 찾기 (개선 - 문제 본문 시작 인식)
    search_start = max(0, start - 300)
    search_end = marker_pos + 200
    temp_text = body[search_start:search_end]
    
    question_start_patterns = [
        r'다항함수 \$f\(x\)',
        r'함수 \$f\(x\)',
        r'삼차함수 \$f\(x\)',
        r'이차함수 \$f\(x\)',
        r'최고차항의 계수가',
        r'상수 \$a',
        r'최고차항의 계수가 양수',
        r'최고차항의 계수가 1',
        r'최고차항의 계수가 음수',
        r'두 양수',
        r'실수 전체의 집합',
        r'\$0<a<1\$',
    ]
    
    for pattern in question_start_patterns:
        match = re.search(pattern, temp_text)
        if match:
            found_start = search_start + match.start()
            if found_start > start:
                start = found_start
            break
    
    # 끝 위치 (보기 문제는 범위 확장)
    if next_marker_pos is not None:
        if is_boogi_problem:
            # 보기 문제는 선택지가 다음 섹션에 있을 수 있으므로 범위 확장
            end = next_marker_pos + 300
        else:
            end = next_marker_pos - 50
    else:
        end = min(len(body), marker_pos + 800)
        if is_boogi_problem:
            end = min(len(body), marker_pos + 1200)  # 보기 문제는 더 넓게
        next_section = body.find('\\section', marker_pos + 100)
        if next_section != -1:
            end = min(end, next_section)
    
    return start, end


def clean_problem_text(text, body_context=None, problem_start=None):
    """문제 텍스트 정리 (이미지, 불필요한 LaTeX 제거) - 개선 버전"""
    # 이미지 제거
    text = re.sub(r'\\includegraphics.*?}', '', text)
    text = re.sub(r'\\begin\{figure\}.*?\\end\{figure\}', '', text, flags=re.DOTALL)
    text = re.sub(r'\\begin\{center\}.*?\\end\{center\}', '', text, flags=re.DOTALL)
    text = re.sub(r'\\begin\{tabular\}.*?\\end\{tabular\}', '', text, flags=re.DOTALL)
    text = re.sub(r'\\begin\{enumerate\}.*?\\end\{enumerate\}', '', text, flags=re.DOTALL)
    text = re.sub(r'\\begin\{array\}.*?\\end\{array\}', '', text, flags=re.DOTALL)
    text = re.sub(r'\\begin\{aligned\}.*?\\end\{aligned\}', '', text, flags=re.DOTALL)
    text = re.sub(r'\\begin\{cases\}.*?\\end\{cases\}', '', text, flags=re.DOTALL)
    
    # caption 제거
    text = re.sub(r'\\caption\{[^}]+\}', '', text)
    text = re.sub(r'\\captionsetup\{[^}]+\}', '', text)
    
    # 섹션 헤더 제거 (개선)
    text = re.sub(r'\\section\*?\{[^}]*\}', '', text)
    text = re.sub(r'Chapter \d+[^가-힣]*미분', '', text)
    text = re.sub(r'Chapter \d+[^가-힣]*적분', '', text)
    text = re.sub(r'Chapter \d+[^가-힣]*', '', text)
    text = re.sub(r'^적분\s+', '', text)  # 시작 부분의 "적분" 제거
    
    # LaTeX 정리
    text = clean_latex_text(text)
    
    # 문제 시작 부분이 잘린 경우 복구 시도 (개선)
    if (text.startswith('}+') or text.startswith('}$') or 
        text.startswith('ction*') or text.startswith('}+9') or
        text.startswith('f(x)$') or text.startswith(')=x') or
        len(text) < 50):
        if body_context and problem_start:
            # 이전 텍스트에서 문제 시작 찾기 (범위 확장)
            search_back = body_context[max(0, problem_start - 400):problem_start]
            func_patterns = [
                r'함수 \$f\(x\)=[^$]+',
                r'삼차함수 \$f\(x\)',
                r'다항함수 \$f\(x\)',
                r'이차함수 \$f\(x\)',
                r'최고차항의 계수가',
                r'상수 \$a',
                r'최고차항의 계수가 양수',
                r'최고차항의 계수가 1',
                r'최고차항의 계수가 음수',
                r'두 양수',
                r'실수 전체의 집합',
                r'\$0<a<1\$',
            ]
            for pattern in func_patterns:
                match = re.search(pattern, search_back)
                if match:
                    # 찾은 부분부터 현재까지
                    full_question = search_back[match.start():] + text
                    text = clean_latex_text(full_question)
                    text = re.sub(r'\\section\*?\{[^}]*\}', '', text)
                    text = re.sub(r'Chapter \d+[^가-힣]*', '', text)
                    text = re.sub(r'^적분\s+', '', text)
                    break
    
    return text.strip()


def extract_boogi_options(options_text, extended_search_text=None):
    """보기 문제 선택지 추출 (개선 버전 - 확장 검색 지원)"""
    options = []
    
    # 보기 내용 추출 (섹션 헤더 포함)
    boogi_patterns = [
        r'\\section\*\{〈보기〉\}(.*?)(?=（[1-5]）|$|\\section)',
        r'〈보기〉(.*?)(?=（[1-5]）|$|\\section)',
    ]
    boogi_content = ""
    search_text = extended_search_text if extended_search_text else options_text
    
    for pattern in boogi_patterns:
        boogi_match = re.search(pattern, search_text, re.DOTALL)
        if boogi_match:
            boogi_content = clean_latex_text(boogi_match.group(1))
            break
    
    # 선택지 (1)~(5) 추출 (전각/반각 괄호 모두 처리)
    # 확장 검색 텍스트 사용 (다음 섹션까지 포함)
    found_options = {}
    for opt_num in range(1, 6):
        # 전각 괄호: （1）~（5）
        pattern1 = rf'（{opt_num}）\s*([^（]+?)(?=（[1-5]）|$|\\section|\\end)'
        # 반각 괄호: (1)~(5)
        pattern2 = rf'\({opt_num}\)\s*([^(]+?)(?=\([1-5]\)|$|\\section|\\end)'
        
        # 확장 검색 텍스트에서도 검색
        match = re.search(pattern1, search_text, re.DOTALL) or re.search(pattern2, search_text, re.DOTALL)
        if match:
            option_text = clean_latex_text(match.group(1))
            # 보기 내용이 선택지에 포함되지 않도록 확인
            # 선택지가 ㄱ,ㄴ,ㄷ 조합이어야 함
            if ('ㄱ' in option_text or 'ㄴ' in option_text or 'ㄷ' in option_text or 
                'ᄀ' in option_text or 'ᄂ' in option_text or 'ᄃ' in option_text):
                found_options[opt_num] = option_text
    
    # 순서대로 정렬
    for opt_num in sorted(found_options.keys()):
        options.append(f"{['①', '②', '③', '④', '⑤'][opt_num-1]} {found_options[opt_num]}")
    
    return options, boogi_content


def validate_problem_structure(problem):
    """문제 구조 검증"""
    required_fields = ['index', 'topic', 'question', 'point', 'answer_type']
    
    for field in required_fields:
        if field not in problem:
            return False, f"필수 필드 누락: {field}"
    
    if problem['answer_type'] == 'multiple_choice':
        if 'options' not in problem or len(problem.get('options', [])) < 5:
            return False, "객관식 문제는 최소 5개 선택지 필요"
    
    if len(problem.get('question', '')) < 30:
        return False, "문제 본문이 너무 짧음"
    
    return True, "정상"


def auto_save_path(subject, year, book_name, part_name, problem_or_solution="문제"):
    """자동 저장 경로 생성"""
    base_dir = Path(r'C:\Users\a\Documents\MathPDF\organized\현우진')
    
    if subject == "수1":
        dir_name = f"수1_{year}학년도_현우진_드릴"
    elif subject == "수2":
        # 수2는 기존 폴더 경로 사용 (수2_2005학년도_현우진_드릴)
        dir_name = "수2_2005학년도_현우진_드릴"
    else:
        dir_name = f"{subject}_{year}학년도_현우진_드릴"
    
    save_dir = base_dir / dir_name
    # 폴더가 이미 존재하므로 mkdir은 선택적
    if not save_dir.exists():
        save_dir.mkdir(parents=True, exist_ok=True)
    
    # 파일명은 실제 년도 사용
    if subject == "수2":
        filename = f"수2_{year}학년도_현우진_드릴_{part_name}_{problem_or_solution}"
    else:
        filename = f"{dir_name}_{part_name}_{problem_or_solution}"
    
    return save_dir, filename
