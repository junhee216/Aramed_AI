# test_pdf_extract.py
import fitz
from pathlib import Path

pdf_path = Path(r'C:\Users\a\Documents\MathPDF\organized\수1\수1_2025년도_수능_기출_P1.pdf')

if pdf_path.exists():
    print(f'파일 찾음: {pdf_path.name}')
    doc = fitz.open(pdf_path)
    print(f'총 페이지: {len(doc)}')
    
    if len(doc) > 0:
        page = doc[0]
        text = page.get_text()
        print('\n' + '='*60)
        print('1페이지 내용:')
        print('='*60)
        print(text)
        print('='*60)
    doc.close()
else:
    print('파일을 찾을 수 없습니다')