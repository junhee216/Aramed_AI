# extract_problem_solution.py
# PDF에서 문제와 해설 추출

import sys
from pathlib import Path

# 우선순위: pdfplumber > PyPDF2 (pymupdf는 DLL 오류로 제외)
PDF_LIBRARY = None
try:
    import pdfplumber
    PDF_LIBRARY = 'pdfplumber'
except ImportError:
    try:
        import PyPDF2
        PDF_LIBRARY = 'PyPDF2'
    except ImportError:
        PDF_LIBRARY = None

def extract_text_from_pdf(pdf_path, page_num=0):
    """PDF에서 특정 페이지의 텍스트 추출"""
    try:
        if PDF_LIBRARY == 'pymupdf':
            import fitz
            doc = fitz.open(pdf_path)
            if page_num >= len(doc):
                print(f'[경고] 페이지 {page_num}이 존재하지 않습니다. 총 페이지: {len(doc)}')
                doc.close()
                return None
            page = doc[page_num]
            text = page.get_text()
            doc.close()
            if not text or len(text.strip()) == 0:
                print('[경고] pymupdf로 텍스트를 추출할 수 없습니다. PDF가 이미지 스캔본일 수 있습니다.')
            return text
        
        elif PDF_LIBRARY == 'pdfplumber':
            import pdfplumber
            with pdfplumber.open(pdf_path) as pdf:
                if page_num >= len(pdf.pages):
                    print(f'[경고] 페이지 {page_num}이 존재하지 않습니다. 총 페이지: {len(pdf.pages)}')
                    return None
                page = pdf.pages[page_num]
                text = page.extract_text()
                if not text or len(text.strip()) == 0:
                    print('[경고] pdfplumber로 텍스트를 추출할 수 없습니다.')
                    print('[정보] PDF가 이미지 스캔본이거나 텍스트 레이어가 없을 수 있습니다.')
                    # 테이블 추출 시도
                    tables = page.extract_tables()
                    if tables:
                        print(f'[정보] {len(tables)}개의 테이블을 찾았습니다.')
                return text
        
        elif PDF_LIBRARY == 'PyPDF2':
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                if page_num >= len(pdf_reader.pages):
                    print(f'[경고] 페이지 {page_num}이 존재하지 않습니다. 총 페이지: {len(pdf_reader.pages)}')
                    return None
                page = pdf_reader.pages[page_num]
                text = page.extract_text()
                if not text or len(text.strip()) == 0:
                    print('[경고] PyPDF2로 텍스트를 추출할 수 없습니다.')
                return text
    except Exception as e:
        print(f'[오류] 텍스트 추출 중 오류 발생: {e}')
        return None
    
    return None

def analyze_problem_structure(text):
    """텍스트에서 문제와 해설 구분"""
    lines = text.split('\n')
    
    # 문제와 해설을 구분하는 키워드
    problem_keywords = ['문제', '문항', '다음', '위의', '제시된']
    solution_keywords = ['정답', '해설', '풀이', '답', '해답', 'Solution', 'Answer']
    
    problem_lines = []
    solution_lines = []
    current_section = 'problem'  # 'problem' or 'solution'
    
    for i, line in enumerate(lines):
        line_stripped = line.strip()
        if not line_stripped:
            continue
        
        # 해설 섹션 시작 감지
        if any(keyword in line_stripped for keyword in solution_keywords):
            current_section = 'solution'
        
        # 문제 섹션인 경우
        if current_section == 'problem':
            problem_lines.append(line)
        # 해설 섹션인 경우
        else:
            solution_lines.append(line)
    
    return '\n'.join(problem_lines), '\n'.join(solution_lines)

def main():
    # MathPDF 폴더에서 P1 파일 찾기
    base_dir = Path(r'C:\Users\a\Documents\MathPDF')
    pdf_path = None
    
    # organized 폴더에서 P1 파일 찾기
    organized_dir = base_dir / 'organized' / '수1'
    if organized_dir.exists():
        for pdf_file in organized_dir.glob('*P1*.pdf'):
            pdf_path = pdf_file
            break
    
    # 원본 폴더에서도 찾기
    if pdf_path is None:
        for pdf_file in base_dir.glob('*P1*.pdf'):
            if 'organized' not in str(pdf_file):
                pdf_path = pdf_file
                break
    
    if pdf_path is None or not pdf_path.exists():
        print(f'[오류] P1 파일을 찾을 수 없습니다.')
        print(f'검색 경로: {base_dir}')
        print(f'organized 경로: {organized_dir}')
        sys.exit(1)
    
    print(f'[파일 읽는 중] {pdf_path.name}\n')
    
    # 1페이지 (인덱스 0) 추출
    text = extract_text_from_pdf(pdf_path, page_num=0)
    
    if not text:
        print('[오류] 텍스트를 추출할 수 없습니다.')
        sys.exit(1)
    
    print('=' * 60)
    print('[전체 페이지 내용]')
    print('=' * 60)
    print(text)
    print('\n' + '=' * 60)
    
    # 문제와 해설 구분
    problem_text, solution_text = analyze_problem_structure(text)
    
    print('\n[추출된 문제 내용]')
    print('=' * 60)
    print(problem_text if problem_text else '(문제 내용을 찾을 수 없습니다)')
    print('=' * 60)
    
    print('\n[추출된 해설 내용]')
    print('=' * 60)
    print(solution_text if solution_text else '(해설 내용을 찾을 수 없습니다)')
    print('=' * 60)
    
    print('\n\n[분석 설명]')
    print('=' * 60)
    if problem_text:
        print('[문제로 인식한 부분]')
        print('   - "정답", "해설", "풀이", "답" 등의 키워드가 나타나기 전까지의 모든 내용')
        print('   - 첫 번째 문항의 문제 지문과 보기')
    else:
        print('[경고] 문제 내용을 명확히 구분할 수 없었습니다.')
    
    if solution_text:
        print('\n[해설로 인식한 부분]')
        print('   - "정답", "해설", "풀이", "답" 등의 키워드가 나타난 이후의 모든 내용')
        print('   - 정답 번호 및 상세 해설')
    else:
        print('\n[경고] 해설 내용을 명확히 구분할 수 없었습니다.')
    
    print('\n[참고]')
    print('   - PDF의 레이아웃에 따라 자동 구분이 정확하지 않을 수 있습니다.')
    print('   - 필요시 수동으로 문제와 해설을 구분해야 할 수 있습니다.')

if __name__ == '__main__':
    main()