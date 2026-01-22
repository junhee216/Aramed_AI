# pdf_utils.py
# PDF 처리 관련 재사용 가능한 유틸리티 함수들

import sys
import os
from pathlib import Path

# Windows 콘솔 인코딩 설정
if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')


def extract_text_from_pdf(pdf_path, page_num=None):
    """
    PDF에서 텍스트 추출 (전체 또는 특정 페이지)
    
    Args:
        pdf_path: PDF 파일 경로
        page_num: 페이지 번호 (None이면 전체 페이지)
    
    Returns:
        추출된 텍스트 (실패 시 None)
    """
    try:
        import pdfplumber
        with pdfplumber.open(pdf_path) as pdf:
            if page_num is not None:
                if page_num >= len(pdf.pages):
                    print(f'[경고] 페이지 {page_num}이 존재하지 않습니다. 총 페이지: {len(pdf.pages)}')
                    return None
                return pdf.pages[page_num].extract_text()
            else:
                text = ""
                for page in pdf.pages:
                    text += page.extract_text() + "\n"
                return text
    except ImportError:
        try:
            import PyPDF2
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                if page_num is not None:
                    if page_num >= len(reader.pages):
                        print(f'[경고] 페이지 {page_num}이 존재하지 않습니다. 총 페이지: {len(reader.pages)}')
                        return None
                    return reader.pages[page_num].extract_text()
                else:
                    text = ""
                    for page in reader.pages:
                        text += page.extract_text() + "\n"
                    return text
        except ImportError:
            try:
                import fitz
                doc = fitz.open(pdf_path)
                if page_num is not None:
                    if page_num >= len(doc):
                        print(f'[경고] 페이지 {page_num}이 존재하지 않습니다. 총 페이지: {len(doc)}')
                        doc.close()
                        return None
                    text = doc[page_num].get_text()
                    doc.close()
                    return text
                else:
                    text = ""
                    for page in doc:
                        text += page.get_text() + "\n"
                    doc.close()
                    return text
            except ImportError:
                print('[경고] PDF 라이브러리를 찾을 수 없습니다. (pdfplumber, PyPDF2, pymupdf 중 하나 설치 필요)')
                return None
    except Exception as e:
        print(f'[오류] 텍스트 추출 중 오류 발생: {e}')
        return None


def find_pdf(base_dir=None, filename_patterns=None):
    """
    원본 PDF 파일 찾기
    
    Args:
        base_dir: 검색할 기본 디렉토리 (None이면 일반적인 경로들 검색)
        filename_patterns: 파일명 패턴 리스트 (None이면 기본 패턴 사용)
    
    Returns:
        찾은 PDF 파일 경로 (Path 객체, 없으면 None)
    """
    if filename_patterns is None:
        filename_patterns = [
            '*P*.pdf',
            '*문제*.pdf',
            '*해설*.pdf',
            '*.pdf'
        ]
    
    search_dirs = []
    if base_dir:
        search_dirs.append(Path(base_dir))
    else:
        # 일반적인 검색 경로들
        search_dirs.extend([
            Path(r'C:\Users\a\Documents\MathPDF\organized\현우진'),
            Path(r'C:\Users\a\Documents\MathPDF'),
            Path.cwd(),
        ])
    
    for search_dir in search_dirs:
        if not search_dir.exists():
            continue
        
        for pattern in filename_patterns:
            matches = list(search_dir.rglob(pattern))
            if matches:
                # 가장 최근 수정된 파일 반환
                return max(matches, key=lambda p: p.stat().st_mtime)
    
    return None
