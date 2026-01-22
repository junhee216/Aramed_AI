# compare_p4_with_solution.py
# 미적분 드릴 P4 문제와 해설 원본 대조

import sys
import os
from pathlib import Path

# Windows 콘솔 인코딩 설정
if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')

def extract_text_from_pdf(pdf_path):
    """PDF에서 텍스트 추출"""
    try:
        import pdfplumber
        with pdfplumber.open(pdf_path) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text() + "\n"
        return text
    except ImportError:
        try:
            import PyPDF2
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n"
            return text
        except ImportError:
            try:
                import fitz
                doc = fitz.open(pdf_path)
                text = ""
                for page in doc:
                    text += page.get_text() + "\n"
                doc.close()
                return text
            except ImportError:
                return None

def find_solution_pdf():
    """해설 PDF 찾기"""
    base_dir = Path(r'C:\Users\a\Documents\MathPDF')
    organized_dir = base_dir / 'organized' / '미적분'
    
    search_patterns = [
        '*드릴*04*해설*.pdf',
        '*드릴*P4*해설*.pdf'
    ]
    
    if organized_dir.exists():
        for pattern in search_patterns:
            for pdf_file in organized_dir.glob(pattern):
                if pdf_file.exists():
                    return pdf_file
    
    return None

def main():
    print("=" * 80)
    print("[미적분 드릴 P4 해설 원본 확인]")
    print("=" * 80)
    
    # 해설 PDF 찾기
    pdf_path = find_solution_pdf()
    if not pdf_path:
        print("\n[오류] 해설 PDF 파일을 찾을 수 없습니다.")
        return
    
    print(f"\n[해설 PDF 찾음] {pdf_path.name}")
    
    # PDF 텍스트 추출
    pdf_text = extract_text_from_pdf(pdf_path)
    if not pdf_text:
        print("[경고] PDF에서 텍스트를 추출할 수 없습니다.")
        print("[정보] 이미지 기반 PDF일 수 있습니다.")
        return
    
    print(f"[PDF 텍스트 추출 완료] {len(pdf_text)}자")
    
    # 샘플 출력
    print("\n[PDF 내용 샘플 (처음 500자)]")
    print("-" * 80)
    print(pdf_text[:500])
    print("-" * 80)
    
    # 핵심 키워드 확인
    print("\n[핵심 키워드 확인]")
    keywords = ["미분", "함수", "극값", "접선", "합성", "삼각함수", "지수함수"]
    found_keywords = [kw for kw in keywords if kw in pdf_text]
    print(f"발견된 키워드: {', '.join(found_keywords)}")
    
    print("\n[완료] 해설 PDF 확인 완료")
    print(f"[정보] PDF 파일 크기: {pdf_path.stat().st_size / 1024:.2f} KB")
    print(f"[정보] 추출된 텍스트 길이: {len(pdf_text)}자")

if __name__ == '__main__':
    main()
