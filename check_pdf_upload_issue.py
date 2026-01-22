# check_pdf_upload_issue.py
# PDF 파일 업로드 문제 진단

from pathlib import Path
import os

def check_pdf_upload_issues():
    """PDF 업로드 문제 진단"""
    
    print("=" * 60)
    print("[PDF 업로드 문제 진단]")
    print("=" * 60)
    print()
    
    base_dir = Path(r'C:\Users\a\Documents\MathPDF')
    
    # 1. 폴더 존재 확인
    print("[1단계] 폴더 구조 확인")
    print("-" * 60)
    print(f"MathPDF 폴더: {'존재' if base_dir.exists() else '없음'}")
    print(f"organized 폴더: {'존재' if (base_dir / 'organized').exists() else '없음'}")
    
    if (base_dir / 'organized').exists():
        try:
            subdirs = [d for d in os.listdir(base_dir / 'organized') 
                      if os.path.isdir(base_dir / 'organized' / d)]
            print(f"하위 폴더: {subdirs}")
        except Exception as e:
            print(f"[오류] 폴더 읽기 오류: {e}")
    
    print()
    
    # 2. PDF 파일 확인
    print("[2단계] PDF 파일 확인")
    print("-" * 60)
    
    # 루트 폴더의 PDF
    root_pdfs = list(base_dir.glob('*.pdf')) + list(base_dir.glob('*.PDF'))
    print(f"MathPDF 루트 폴더의 PDF: {len(root_pdfs)}개")
    if root_pdfs:
        for pdf in root_pdfs[:5]:
            size_mb = pdf.stat().st_size / (1024 * 1024)
            print(f"  - {pdf.name} ({size_mb:.2f} MB)")
    
    # organized 폴더의 PDF
    organized_pdfs = []
    if (base_dir / 'organized').exists():
        for subdir in (base_dir / 'organized').iterdir():
            if subdir.is_dir():
                pdfs = list(subdir.glob('*.pdf')) + list(subdir.glob('*.PDF'))
                organized_pdfs.extend(pdfs)
                if pdfs:
                    print(f"\n{subdir.name}/ 폴더: {len(pdfs)}개 PDF")
                    for pdf in pdfs[:3]:
                        size_mb = pdf.stat().st_size / (1024 * 1024)
                        print(f"  - {pdf.name} ({size_mb:.2f} MB)")
    
    print()
    
    # 3. 가능한 문제 원인
    print("[3단계] 가능한 문제 원인")
    print("-" * 60)
    
    issues = []
    
    # 문제 1: 루트 폴더에 PDF가 없음
    if len(root_pdfs) == 0:
        issues.append("[문제] MathPDF 루트 폴더에 PDF 파일이 없습니다.")
        issues.append("   -> 해결: PDF 파일을 C:\\Users\\a\\Documents\\MathPDF 폴더에 복사하세요.")
    
    # 문제 2: 파일 크기 문제
    large_files = [f for f in root_pdfs if f.stat().st_size > 8 * 1024 * 1024]
    if large_files:
        issues.append(f"[주의] 8MB를 초과하는 파일 {len(large_files)}개 발견")
        issues.append("   -> 해결: organize_pdf.py를 실행하면 자동으로 분할됩니다.")
    
    # 문제 3: 권한 문제
    try:
        test_file = base_dir / 'test_write.txt'
        test_file.write_text('test')
        test_file.unlink()
    except Exception as e:
        issues.append(f"[문제] 폴더 쓰기 권한 문제: {e}")
        issues.append("   -> 해결: 폴더 권한을 확인하거나 관리자 권한으로 실행하세요.")
    
    # 문제 4: 라이브러리 문제
    try:
        import PyPDF2
        print("[확인] PyPDF2 라이브러리 설치됨")
    except ImportError:
        try:
            import fitz
            print("[확인] PyMuPDF 라이브러리 설치됨")
        except ImportError:
            issues.append("[문제] PDF 처리 라이브러리가 설치되지 않았습니다.")
            issues.append("   -> 해결: pip install PyPDF2 또는 pip install pymupdf")
    
    if issues:
        print("\n발견된 문제:")
        for issue in issues:
            print(f"  {issue}")
    else:
        print("[확인] 특별한 문제가 발견되지 않았습니다.")
    
    print()
    
    # 4. 권장 사항
    print("[4단계] 권장 사항")
    print("-" * 60)
    print("1. PDF 파일을 C:\\Users\\a\\Documents\\MathPDF 폴더에 직접 복사하세요.")
    print("2. organize_pdf.py를 실행하여 자동으로 분류 및 분할하세요.")
    print("3. 파일 크기가 8MB를 초과하면 자동으로 8MB 단위로 분할됩니다.")
    print("4. organized 폴더에 이미 정리된 파일이 있다면, 루트 폴더에 새 파일을 넣으세요.")
    print()
    
    # 5. 현재 상태 요약
    print("=" * 60)
    print("[현재 상태 요약]")
    print("=" * 60)
    print(f"루트 폴더 PDF: {len(root_pdfs)}개")
    print(f"organized 폴더 PDF: {len(organized_pdfs)}개")
    print(f"총 PDF 파일: {len(root_pdfs) + len(organized_pdfs)}개")
    print()

if __name__ == '__main__':
    check_pdf_upload_issues()
