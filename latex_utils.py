# latex_utils.py
# LaTeX 파싱을 위한 재사용 가능한 유틸리티 함수들

import re
import sys
import os

# Windows 콘솔 인코딩 설정
if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')


def extract_body(latex_content):
    """LaTeX 본문만 추출 (\\begin{document} ~ \\end{document})"""
    begin_match = re.search(r'\\begin\{document\}', latex_content)
    end_match = re.search(r'\\end\{document\}', latex_content)
    if begin_match and end_match:
        return latex_content[begin_match.end():end_match.start()]
    return latex_content


def diagnose_latex_structure(body, max_chars=500):
    """LaTeX 본문 구조 진단 (디버깅용)"""
    print("=" * 60)
    print("[LaTeX 구조 진단]")
    print("=" * 60)
    print(f"[본문 길이] {len(body)}자")
    print(f"[처음 {max_chars}자]")
    print(repr(body[:max_chars]))
    print()
    
    # 백슬래시 패턴 확인
    backslash_count = body.count('\\')
    dollar_count = body.count('$')
    escaped_dollar = body.count('\\$')
    print(f"[백슬래시] 총 {backslash_count}개")
    print(f"[달러 기호] 총 {dollar_count}개 (이스케이프: {escaped_dollar}개)")
    print()
    
    # 전각/반각 문자 확인
    fullwidth_bracket = body.count('［')
    halfwidth_bracket = body.count('[')
    fullwidth_paren = body.count('（')
    halfwidth_paren = body.count('(')
    print(f"[괄호] 반각 [ : {halfwidth_bracket}개, 전각 ［ : {fullwidth_bracket}개")
    print(f"[괄호] 반각 ( : {halfwidth_paren}개, 전각 （ : {fullwidth_paren}개")
    print()
    
    # 줄바꿈 패턴 확인
    newline_count = body.count('\n')
    double_backslash = body.count('\\\\')
    print(f"[줄바꿈] \\n: {newline_count}개, \\\\: {double_backslash}개")
    print("=" * 60)
    print()


def find_keyword_positions(body, keywords):
    """키워드들의 위치 찾기"""
    positions = {}
    for keyword in keywords:
        pos = body.find(keyword)
        positions[keyword] = pos
        if pos != -1:
            print(f"[키워드] '{keyword}' 위치: {pos}")
        else:
            print(f"[키워드] '{keyword}' 없음")
    return positions


def extract_options_generic(options_text, num_options=5):
    """일반적인 선택지 추출 (분수, 정수, 제곱근 등)"""
    options = []
    
    for i in range(1, num_options + 1):
        option_num = ["①", "②", "③", "④", "⑤"][i-1]
        
        # 다양한 패턴 시도
        patterns = [
            # 분수: (1) $\frac{15}{16}$ 또는 (1) \$\frac{15}{16}\$
            rf'\({i}\)\s*\\?\$\\?frac{{([0-9]+)}}\{{([0-9]+)}}\\?\$',
            # 제곱근: (1) $\sqrt{2}$ 또는 (1) \$\sqrt{2}\$
            rf'\({i}\)\s*\\?\$\\?sqrt{{([0-9]+)}}\\?\$',
            # 정수: (2) 1 또는 (2) 1\\
            rf'\({i}\)\s*([0-9]+)(?=\\\\|\s|$)',
            # 전각 괄호: （1）...
            rf'[（(]{i}[）)]\s*([^（(\\]+)',
        ]
        
        match = None
        for pattern in patterns:
            match = re.search(pattern, options_text)
            if match:
                break
        
        if match:
            if len(match.groups()) == 2 and match.group(1).isdigit() and match.group(2).isdigit():
                # 분수
                opt_text = f"\\frac{{{match.group(1)}}}{{{match.group(2)}}}"
                options.append(f"{option_num} ${opt_text}$")
            elif len(match.groups()) == 1 and match.group(1).isdigit():
                # 제곱근 또는 정수
                if 'sqrt' in pattern:
                    opt_text = f"\\sqrt{{{match.group(1)}}}"
                    options.append(f"{option_num} ${opt_text}$")
                else:
                    options.append(f"{option_num} {match.group(1)}")
            else:
                # 기타 텍스트
                opt_text = match.group(1).strip()
                opt_text = re.sub(r'\\\\+', '', opt_text)
                opt_text = re.sub(r'\\\$', '', opt_text)
                options.append(f"{option_num} {opt_text}")
        else:
            # 패턴 매칭 실패 시 디버깅
            print(f"[경고] 선택지 {i}번 추출 실패")
            # 해당 부분 출력
            pattern = rf'\({i}\)'
            match_pos = re.search(pattern, options_text)
            if match_pos:
                start = max(0, match_pos.start() - 20)
                end = min(len(options_text), match_pos.end() + 50)
                print(f"  주변 텍스트: {repr(options_text[start:end])}")
    
    return options


def extract_problem_with_options(body, question_pattern, boundary_pattern, 
                                  options_extractor=None, debug=False):
    """문제와 선택지를 함께 추출하는 범용 함수"""
    # 문제 본문 찾기
    match = re.search(question_pattern, body, re.DOTALL)
    if not match:
        if debug:
            print(f"[패턴 매칭 실패] {question_pattern[:50]}...")
        return None
    
    question = match.group(1).strip() if match.lastindex >= 1 else ""
    options_text = match.group(2).strip() if match.lastindex >= 2 else ""
    
    # 문제 본문 정리
    question = re.sub(r'\\\\', ' ', question)
    question = re.sub(r'\s+', ' ', question)
    
    # 선택지 추출
    options = []
    if options_extractor:
        options = options_extractor(options_text)
    elif options_text:
        options = extract_options_generic(options_text)
    
    return {
        "question": question,
        "options": options,
        "options_text": options_text  # 디버깅용
    }


def create_problem_pattern(start_keywords, end_keywords, point_markers=None):
    """문제 패턴 생성 헬퍼 함수"""
    if point_markers is None:
        point_markers = [r'\[4점\]', r'\[3점\]', r'［4점］', r'［3점］']
    
    point_pattern = '|'.join(point_markers)
    
    # 시작 키워드 패턴
    start_pattern = '|'.join([re.escape(kw) for kw in start_keywords])
    
    # 종료 키워드 패턴
    end_pattern = '|'.join([re.escape(kw) for kw in end_keywords])
    
    # 전체 패턴
    pattern = rf'({start_pattern}.*?{point_pattern})(.*?)(?={end_pattern}|$)'
    
    return pattern


def clean_latex_text(text):
    """LaTeX 텍스트 정리 (불필요한 백슬래시, 줄바꿈 등 제거)"""
    # 이중 백슬래시를 공백으로
    text = re.sub(r'\\\\+', ' ', text)
    # 이미지 포함 제거
    text = re.sub(r'\\includegraphics.*?}', '', text)
    # 연속 공백 정리
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def test_pattern(pattern, body, context_chars=100):
    """패턴 테스트 및 매칭 결과 출력"""
    match = re.search(pattern, body, re.DOTALL)
    if match:
        print(f"[패턴 매칭 성공]")
        print(f"  매칭 위치: {match.start()} ~ {match.end()}")
        print(f"  매칭 길이: {match.end() - match.start()}자")
        if match.groups():
            print(f"  그룹 수: {len(match.groups())}")
            for i, group in enumerate(match.groups(), 1):
                print(f"  그룹 {i}: {repr(group[:context_chars])}")
        # 주변 텍스트 출력
        start = max(0, match.start() - context_chars)
        end = min(len(body), match.end() + context_chars)
        print(f"  주변 텍스트: {repr(body[start:end])}")
        return True
    else:
        print(f"[패턴 매칭 실패]")
        return False
