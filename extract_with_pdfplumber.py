# extract_with_pdfplumber.py
# pdfplumber를 사용하여 PDF에서 이미지 추출 후 OCR

import sys
import io
from pathlib import Path

try:
    import pdfplumber
    PDFPLUMBER_AVAILABLE = True
except ImportError:
    PDFPLUMBER_AVAILABLE = False

try:
    import pytesseract
    import os
    # Tesseract 경로 설정
    possible_paths = [
        r'C:\Program Files\Tesseract-OCR\tesseract.exe',
        r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
        r'C:\Users\{}\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'.format(os.getenv('USERNAME', '')),
    ]
    for path in possible_paths:
        if os.path.exists(path):
            pytesseract.pytesseract.tesseract_cmd = path
            print(f'[정보] Tesseract 경로 설정: {path}')
            break
    TESSERACT_AVAILABLE = True
except ImportError:
    TESSERACT_AVAILABLE = False

from PIL import Image

def extract_text_with_ocr(pdf_path, page_num=0):
    """PDF를 이미지로 변환 후 OCR로 텍스트 추출"""
    if not PDFPLUMBER_AVAILABLE:
        print('[오류] pdfplumber가 설치되지 않았습니다.')
        return None
    
    if not TESSERACT_AVAILABLE:
        print('[오류] pytesseract가 설치되지 않았습니다.')
        return None
    
    try:
        print(f'[진행] PDF 열기... (페이지 {page_num + 1})')
        with pdfplumber.open(pdf_path) as pdf:
            if page_num >= len(pdf.pages):
                print(f'[오류] 페이지 {page_num + 1}이 존재하지 않습니다. 총 페이지: {len(pdf.pages)}')
                return None
            
            page = pdf.pages[page_num]
            
            # 방법 1: 텍스트 추출 시도
            text = page.extract_text()
            if text and len(text.strip()) > 0:
                print('[정보] 텍스트 레이어에서 추출 성공')
                return text
            
            # 방법 2: 이미지로 변환 후 OCR
            print('[진행] 이미지로 변환 후 OCR 처리...')
            
            # 페이지를 이미지로 렌더링
            # pdfplumber는 직접 이미지 추출이 어려우므로, 페이지 객체에서 이미지 추출 시도
            images = page.images
            if images:
                print(f'[정보] 페이지에서 {len(images)}개의 이미지를 찾았습니다.')
                # 첫 번째 이미지 사용
                # pdfplumber는 이미지 추출이 제한적이므로 다른 방법 필요
            
            # 대안: 페이지를 이미지로 저장하는 다른 방법 시도
            # pdfplumber는 이미지 추출이 어려우므로, PyMuPDF나 pdf2image가 필요합니다
            
            print('[경고] pdfplumber로는 이미지 추출이 어렵습니다.')
            print('[해결] Poppler 설치 또는 PyMuPDF DLL 문제 해결이 필요합니다.')
            return None
            
    except Exception as e:
        print(f'[오류] 처리 중 오류 발생: {e}')
        import traceback
        traceback.print_exc()
        return None

def analyze_problem_structure(text):
    """텍스트에서 문제와 해설 구분"""
    if not text:
        return '', ''
    
    lines = text.split('\n')
    
    solution_keywords = ['정답', '해설', '풀이', '답', '해답', 'Solution', 'Answer', '①', '②', '③', '④', '⑤']
    
    problem_lines = []
    solution_lines = []
    current_section = 'problem'
    
    for line in lines:
        line_stripped = line.strip()
        if not line_stripped:
            continue
        
        if any(keyword in line_stripped for keyword in solution_keywords):
            if any(keyword in line_stripped for keyword in ['정답', '해설', '풀이']):
                current_section = 'solution'
        
        if current_section == 'problem':
            problem_lines.append(line)
        else:
            solution_lines.append(line)
    
    return '\n'.join(problem_lines), '\n'.join(solution_lines)

def main():
    base_dir = Path(r'C:\Users\a\Documents\MathPDF\organized\수1')
    pdf_path = None
    
    for pdf_file in base_dir.glob('*P1*.pdf'):
        pdf_path = pdf_file
        break
    
    if pdf_path is None or not pdf_path.exists():
        print(f'[오류] P1 파일을 찾을 수 없습니다.')
        sys.exit(1)
    
    print(f'[파일 찾음] {pdf_path.name}\n')
    
    text = extract_text_with_ocr(pdf_path, page_num=0)
    
    if not text:
        print('\n[해결 방법]')
        print('Poppler 설치가 필요합니다:')
        print('1. https://github.com/oschwartz10612/poppler-windows/releases 에서 다운로드')
        print('2. 압축 해제 후 bin 폴더를 PATH에 추가')
        print('3. 또는 PyMuPDF DLL 문제를 해결')
        sys.exit(1)
    
    print('\n' + '=' * 60)
    print('[전체 페이지 내용]')
    print('=' * 60)
    print(text)
    print('\n' + '=' * 60)
    
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
    if solution_text:
        print('\n[해설로 인식한 부분]')
        print('   - "정답", "해설", "풀이", "답" 등의 키워드가 나타난 이후의 모든 내용')

if __name__ == '__main__':
    main()