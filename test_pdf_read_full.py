# test_pdf_read_full.py
# PDF 파일 전체 내용 읽기 테스트

from pathlib import Path
import sys

def test_pdf_reading():
    """PDF 파일 읽기 테스트"""
    
    base_dir = Path(r'C:\Users\a\Documents\MathPDF')
    
    # 2022 수능 기하 파일 찾기
    pdf_files = list(base_dir.glob('*2022*수능*.pdf'))
    pdf_files.extend(list(base_dir.glob('*기하*2022*.pdf')))
    
    if not pdf_files:
        print("[오류] 2022 수능 기하 PDF 파일을 찾을 수 없습니다.")
        print(f"검색 경로: {base_dir}")
        return False
    
    pdf_path = pdf_files[0]
    print(f"[성공] 파일 발견: {pdf_path.name}")
    print(f"   크기: {pdf_path.stat().st_size / (1024 * 1024):.2f} MB\n")
    
    # 여러 라이브러리로 시도
    libraries = []
    
    # 1. PyPDF2 시도
    try:
        import PyPDF2
        libraries.append(('PyPDF2', PyPDF2))
    except ImportError:
        pass
    
    # 2. PyMuPDF 시도
    try:
        import fitz  # PyMuPDF
        libraries.append(('PyMuPDF', fitz))
    except ImportError:
        pass
    
    # 3. pdfplumber 시도
    try:
        import pdfplumber
        libraries.append(('pdfplumber', pdfplumber))
    except ImportError:
        pass
    
    if not libraries:
        print("[오류] PDF 읽기 라이브러리가 설치되어 있지 않습니다.")
        print("   설치 필요: pip install PyPDF2 pymupdf pdfplumber")
        return False
    
    print(f"[사용 가능한 라이브러리]: {[lib[0] for lib in libraries]}\n")
    
    # 각 라이브러리로 읽기 테스트
    results = {}
    
    for lib_name, lib in libraries:
        print(f"[{lib_name}] 테스트 중...")
        try:
            if lib_name == 'PyPDF2':
                with open(pdf_path, 'rb') as f:
                    reader = PyPDF2.PdfReader(f)
                    total_pages = len(reader.pages)
                    text_content = []
                    for i, page in enumerate(reader.pages):
                        text = page.extract_text()
                        text_content.append(f"=== 페이지 {i+1} ===\n{text}\n")
                    results[lib_name] = {
                        'success': True,
                        'pages': total_pages,
                        'text': '\n'.join(text_content),
                        'char_count': sum(len(t) for t in text_content)
                    }
                    
            elif lib_name == 'PyMuPDF':
                doc = fitz.open(pdf_path)
                total_pages = len(doc)
                text_content = []
                for i in range(total_pages):
                    page = doc[i]
                    text = page.get_text()
                    text_content.append(f"=== 페이지 {i+1} ===\n{text}\n")
                doc.close()
                results[lib_name] = {
                    'success': True,
                    'pages': total_pages,
                    'text': '\n'.join(text_content),
                    'char_count': sum(len(t) for t in text_content)
                }
                
            elif lib_name == 'pdfplumber':
                with pdfplumber.open(pdf_path) as pdf:
                    total_pages = len(pdf.pages)
                    text_content = []
                    for i, page in enumerate(pdf.pages):
                        text = page.extract_text()
                        if text:
                            text_content.append(f"=== 페이지 {i+1} ===\n{text}\n")
                    results[lib_name] = {
                        'success': True,
                        'pages': total_pages,
                        'text': '\n'.join(text_content),
                        'char_count': sum(len(t) for t in text_content)
                    }
            
            print(f"  [성공] {results[lib_name]['pages']}페이지, {results[lib_name]['char_count']:,}자 추출")
            
        except Exception as e:
            print(f"  [실패] {e}")
            results[lib_name] = {'success': False, 'error': str(e)}
    
    print("\n" + "="*70)
    print("[결과 요약]")
    print("="*70)
    
    successful = [name for name, result in results.items() if result.get('success')]
    
    if successful:
        print(f"[성공한 라이브러리]: {', '.join(successful)}")
        
        # 가장 많은 텍스트를 추출한 라이브러리 선택
        best_lib = max(successful, key=lambda x: results[x]['char_count'])
        best_result = results[best_lib]
        
        print(f"\n[최적 라이브러리]: {best_lib}")
        print(f"   - 총 페이지: {best_result['pages']}페이지")
        print(f"   - 추출된 텍스트: {best_result['char_count']:,}자")
        
        # 전체 내용을 파일로 저장
        output_file = base_dir / 'pdf_extract_test.txt'
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(best_result['text'])
            print(f"\n[전체 내용 저장 완료]")
            print(f"   저장 위치: {output_file}")
            print(f"   - 전체 텍스트 길이: {best_result['char_count']:,}자")
            print(f"   - 총 페이지: {best_result['pages']}페이지")
        except Exception as e:
            print(f"\n[저장 실패]: {e}")
        
        # 전체 내용 저장 여부 확인
        print(f"\n[PDF 읽기 능력 확인]")
        print(f"   - 전체 내용 추출: 가능")
        print(f"   - 페이지별 분리: 가능")
        print(f"   - 텍스트 추출: {best_result['char_count']:,}자")
        print(f"   - 수식 인식: 부분 가능 (LaTeX 변환 필요)")
        print(f"   - 그림/표: 추출 가능 (라이브러리별 차이)")
        
        return True
    else:
        print("[오류] 모든 라이브러리에서 읽기 실패")
        return False

if __name__ == '__main__':
    success = test_pdf_reading()
    sys.exit(0 if success else 1)
