# extract_problem_solution_ocr.py
# 이미지 스캔본 PDF에서 OCR을 사용하여 문제와 해설 추출

import sys
import io
from pathlib import Path

# PyMuPDF를 사용하여 PDF를 이미지로 변환
try:
    import fitz  # PyMuPDF
    PYMUPDF_AVAILABLE = True
except ImportError:
    PYMUPDF_AVAILABLE = False
    try:
        from pdf2image import convert_from_path
        PDF2IMAGE_AVAILABLE = True
    except ImportError:
        PDF2IMAGE_AVAILABLE = False

try:
    import pytesseract
    TESSERACT_AVAILABLE = True
    # Tesseract 경로 자동 탐색 (Windows 일반 설치 경로)
    import os
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
except ImportError:
    TESSERACT_AVAILABLE = False

from PIL import Image

def extract_text_with_ocr(pdf_path, page_num=0):
    """PDF를 이미지로 변환 후 OCR로 텍스트 추출"""
    if not TESSERACT_AVAILABLE:
        print('[오류] pytesseract가 설치되지 않았습니다. pip install pytesseract')
        print('[참고] Tesseract OCR 엔진도 별도로 설치해야 합니다.')
        print('      Windows: https://github.com/UB-Mannheim/tesseract/wiki')
        return None
    
    try:
        image = None
        
        # 방법 1: PyMuPDF 사용 (우선)
        if PYMUPDF_AVAILABLE:
            try:
                print(f'[진행] PDF를 이미지로 변환 중... (PyMuPDF 사용, 페이지 {page_num + 1})')
                import fitz
                doc = fitz.open(pdf_path)
                if page_num >= len(doc):
                    print(f'[오류] 페이지 {page_num + 1}이 존재하지 않습니다. 총 페이지: {len(doc)}')
                    doc.close()
                    return None
                
                page = doc[page_num]
                # DPI 300으로 렌더링
                mat = fitz.Matrix(300/72, 300/72)  # 300 DPI
                pix = page.get_pixmap(matrix=mat)
                # PIL Image로 변환
                img_data = pix.tobytes("png")
                image = Image.open(io.BytesIO(img_data))
                doc.close()
                print('[완료] 이미지 변환 완료')
            except Exception as e:
                print(f'[경고] PyMuPDF 변환 실패: {e}')
                image = None
        
        # 방법 2: pdf2image 사용 (대안)
        if image is None and PDF2IMAGE_AVAILABLE:
            try:
                print(f'[진행] PDF를 이미지로 변환 중... (pdf2image 사용, 페이지 {page_num + 1})')
                # Poppler 경로 설정 (여러 가능한 경로 시도)
                possible_poppler_paths = [
                    r'C:\Users\a\Downloads\Release-25.12.0-0\poppler-25.12.0\Library\bin',
                    r'C:\Users\a\Downloads\Release-25.12.0-0\poppler-25.12.0\bin',
                    r'C:\Users\a\Downloads\Release-25.12.0-0\bin',
                    r'C:\Users\a\Downloads\Release-25.12.0-0\poppler-25.12.0',
                ]
                
                poppler_path = None
                for path in possible_poppler_paths:
                    if os.path.exists(path):
                        # pdftoppm.exe가 있는지 확인
                        pdftoppm_path = os.path.join(path, 'pdftoppm.exe')
                        if os.path.exists(pdftoppm_path):
                            poppler_path = path
                            print(f'[정보] Poppler 경로 찾음: {poppler_path}')
                            break
                
                if poppler_path:
                    images = convert_from_path(pdf_path, dpi=300, first_page=page_num + 1, last_page=page_num + 1, poppler_path=poppler_path)
                else:
                    print('[경고] Poppler 실행 파일을 찾을 수 없습니다. PATH에서 찾는 중...')
                    images = convert_from_path(pdf_path, dpi=300, first_page=page_num + 1, last_page=page_num + 1)
                if images:
                    image = images[0]
                    print('[완료] 이미지 변환 완료')
            except Exception as e:
                print(f'[경고] pdf2image 변환 실패: {e}')
                print('[참고] Poppler 설치가 필요할 수 있습니다.')
        
        if image is None:
            print('[오류] PDF를 이미지로 변환할 수 없습니다.')
            return None
        
        print('[진행] OCR 처리 중... (시간이 걸릴 수 있습니다)')
        
        # OCR로 텍스트 추출 (한국어 + 영어)
        text = pytesseract.image_to_string(image, lang='kor+eng')
        
        return text
    
    except Exception as e:
        print(f'[오류] OCR 처리 중 오류 발생: {e}')
        import traceback
        traceback.print_exc()
        return None

def analyze_problem_structure(text):
    """텍스트에서 문제와 해설 구분"""
    if not text:
        return '', ''
    
    lines = text.split('\n')
    
    # 문제와 해설을 구분하는 키워드
    solution_keywords = ['정답', '해설', '풀이', '답', '해답', 'Solution', 'Answer', '①', '②', '③', '④', '⑤']
    
    problem_lines = []
    solution_lines = []
    current_section = 'problem'  # 'problem' or 'solution'
    
    for i, line in enumerate(lines):
        line_stripped = line.strip()
        if not line_stripped:
            continue
        
        # 해설 섹션 시작 감지
        if any(keyword in line_stripped for keyword in solution_keywords):
            # "정답" 또는 "해설" 키워드가 나타나면 해설 섹션 시작
            if any(keyword in line_stripped for keyword in ['정답', '해설', '풀이']):
                current_section = 'solution'
        
        # 문제 섹션인 경우
        if current_section == 'problem':
            problem_lines.append(line)
        # 해설 섹션인 경우
        else:
            solution_lines.append(line)
    
    return '\n'.join(problem_lines), '\n'.join(solution_lines)

def main():
    # 파일 찾기
    base_dir = Path(r'C:\Users\a\Documents\MathPDF\organized\수1')
    pdf_path = None
    
    # P1 파일 찾기
    for pdf_file in base_dir.glob('*P1*.pdf'):
        pdf_path = pdf_file
        break
    
    if pdf_path is None or not pdf_path.exists():
        print(f'[오류] P1 파일을 찾을 수 없습니다.')
        print(f'검색 경로: {base_dir}')
        sys.exit(1)
    
    print(f'[파일 찾음] {pdf_path.name}\n')
    
    # OCR로 텍스트 추출
    text = extract_text_with_ocr(pdf_path, page_num=0)
    
    if not text:
        print('[오류] 텍스트를 추출할 수 없습니다.')
        print('\n[해결 방법]')
        print('1. Tesseract OCR 설치 필요: https://github.com/UB-Mannheim/tesseract/wiki')
        print('2. 또는 PDF가 텍스트 레이어를 포함하는지 확인')
        sys.exit(1)
    
    print('\n' + '=' * 60)
    print('[전체 페이지 내용 (OCR 결과)]')
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
        print(f'   - 총 {len(problem_text.split())} 단어 추출')
    else:
        print('[경고] 문제 내용을 명확히 구분할 수 없었습니다.')
    
    if solution_text:
        print('\n[해설로 인식한 부분]')
        print('   - "정답", "해설", "풀이", "답" 등의 키워드가 나타난 이후의 모든 내용')
        print('   - 정답 번호 및 상세 해설')
        print(f'   - 총 {len(solution_text.split())} 단어 추출')
    else:
        print('\n[경고] 해설 내용을 명확히 구분할 수 없었습니다.')
    
    print('\n[참고]')
    print('   - OCR 결과는 이미지 품질에 따라 정확도가 달라질 수 있습니다.')
    print('   - 수식이나 특수 기호는 인식이 어려울 수 있습니다.')
    print('   - 필요시 수동으로 문제와 해설을 구분해야 할 수 있습니다.')

if __name__ == '__main__':
    main()