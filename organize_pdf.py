# organize_pdf.py
# PDF 수학 문제집 파일 정리 및 분할 스크립트 (전면 수정 버전)
# 6개 폴더 분류 (수1, 수2, 미적분, 확률, 통계, 기하) + 미분류
# 파일명 표준화: [과목]_[교재명]_[파트].pdf
# 페이지 수 기록 및 15MB 초과 시 10MB 단위로 분할

import os
import re
import csv
import shutil
from pathlib import Path
from typing import Optional, Tuple, List
from datetime import datetime

try:
    import PyPDF2
    PDF_LIBRARY = 'PyPDF2'
except ImportError:
    try:
        import fitz  # PyMuPDF
        PDF_LIBRARY = 'pymupdf'
    except ImportError:
        PDF_LIBRARY = None


class PDFOrganizer:
    """PDF 파일 정리 및 분할 클래스 (단순화된 버전)"""
    
    # 6개 대분류 폴더 (키워드 매핑)
    SUBJECT_KEYWORDS = {
        '수1': ['수1', '수학1', '수학 1', '수i', '수i', '-수1-'],
        '수2': ['수2', '수학2', '수학 2', '수ii', '수ii', '-수2-'],
        '미적분': ['미적분', '미적', '미분', '적분', 'calculus'],
        '확률': ['확률', '확률과통계', '확통'],
        '통계': ['통계'],
        '기하': ['기하', '공간도형', '벡터', 'geometry']
    }
    
    MAX_SIZE_MB = 8  # 분할 기준 크기 (MB)
    SPLIT_SIZE_MB = 8  # 분할 단위 크기 (MB)
    
    # 고정 경로
    BASE_DIR = Path(r'C:\Users\a\Documents\MathPDF')
    
    def __init__(self, source_dir: str = None):
        """
        Args:
            source_dir: PDF 파일이 있는 원본 폴더 경로 (없으면 BASE_DIR 사용)
        """
        if source_dir:
            self.source_dir = Path(source_dir)
        else:
            self.source_dir = self.BASE_DIR
        
        if not self.source_dir.exists():
            raise FileNotFoundError(f"원본 폴더를 찾을 수 없습니다: {self.source_dir}")
        
        # 정리된 파일은 항상 BASE_DIR/organized에 저장
        self.target_dir = self.BASE_DIR / 'organized'
        self.target_dir.mkdir(parents=True, exist_ok=True)
        
        self.processed_files = []  # 처리 완료된 파일 목록
        
        self._check_library()
    
    def _check_library(self):
        """PDF 처리 라이브러리 확인"""
        if PDF_LIBRARY is None:
            raise ImportError(
                "PDF 처리 라이브러리가 설치되지 않았습니다.\n"
                "다음 중 하나를 설치해주세요:\n"
                "  pip install PyPDF2\n"
                "  pip install pymupdf"
            )
    
    def extract_subject(self, filename: str) -> str:
        """파일명에서 과목 추출 (6개 폴더만)"""
        filename_lower = filename.lower()
        
        for subject, keywords in self.SUBJECT_KEYWORDS.items():
            for keyword in keywords:
                if keyword.lower() in filename_lower:
                    return subject
        
        return '미분류'
    
    def get_total_pages(self, pdf_path: Path) -> int:
        """PDF 파일의 총 페이지 수 반환"""
        try:
            if PDF_LIBRARY == 'PyPDF2':
                with open(pdf_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    return len(pdf_reader.pages)
            elif PDF_LIBRARY == 'pymupdf':
                import fitz
                doc = fitz.open(pdf_path)
                page_count = len(doc)
                doc.close()
                return page_count
        except Exception as e:
            print(f"    [경고] 페이지 수 계산 실패: {e}")
            return 0
        
        return 0
    
    def standardize_filename(self, original_filename: str, subject: str) -> str:
        """파일명 표준화: [과목]_[교재명]_[파트].pdf"""
        # 확장자 제거
        name_without_ext = Path(original_filename).stem
        
        # 파일명에서 과목 키워드 제거 (중복 방지)
        cleaned_name = name_without_ext
        for keywords in self.SUBJECT_KEYWORDS.values():
            for keyword in keywords:
                # 키워드를 제거 (대소문자 무시)
                pattern = re.compile(re.escape(keyword), re.IGNORECASE)
                cleaned_name = pattern.sub('', cleaned_name)
        
        # 특수문자 정리
        cleaned_name = re.sub(r'[-_]{2,}', '_', cleaned_name)  # 연속된 -_ 제거
        cleaned_name = re.sub(r'[^\w가-힣]', '_', cleaned_name)  # 특수문자를 _로
        cleaned_name = re.sub(r'_+', '_', cleaned_name)  # 연속된 _를 하나로
        cleaned_name = cleaned_name.strip('_')  # 앞뒤 _ 제거
        
        # 교재명 추출 (파일명의 나머지 부분)
        textbook_name = cleaned_name if cleaned_name else '기타'
        
        # 표준화된 파일명 생성
        standardized = f"{subject}_{textbook_name}.pdf"
        
        return standardized
    
    def get_file_size_mb(self, file_path: Path) -> float:
        """파일 크기를 MB 단위로 반환"""
        return file_path.stat().st_size / (1024 * 1024)
    
    def split_pdf(self, pdf_path: Path, output_dir: Path, base_name: str) -> List[Path]:
        """PDF 파일을 10MB 단위로 분할"""
        file_size_mb = self.get_file_size_mb(pdf_path)
        total_pages = self.get_total_pages(pdf_path)
        
        if total_pages == 0:
            raise ValueError("페이지 수를 계산할 수 없습니다.")
        
        # 10MB당 페이지 수 계산 (근사치)
        pages_per_split = max(1, int((self.SPLIT_SIZE_MB / file_size_mb) * total_pages))
        
        split_files = []
        
        if PDF_LIBRARY == 'PyPDF2':
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                total_pages = len(pdf_reader.pages)
                
                split_num = 1
                for start_page in range(0, total_pages, pages_per_split):
                    end_page = min(start_page + pages_per_split, total_pages)
                    
                    pdf_writer = PyPDF2.PdfWriter()
                    for page_num in range(start_page, end_page):
                        pdf_writer.add_page(pdf_reader.pages[page_num])
                    
                    split_filename = f"{base_name}_P{split_num}.pdf"
                    split_path = output_dir / split_filename
                    
                    with open(split_path, 'wb') as output_file:
                        pdf_writer.write(output_file)
                    
                    # 실제 크기 확인
                    actual_size = self.get_file_size_mb(split_path)
                    if actual_size > self.MAX_SIZE_MB:
                        # 여전히 크면 더 작게 분할
                        os.remove(split_path)
                        temp_pdf = output_dir / f"temp_{split_num}.pdf"
                        with open(temp_pdf, 'wb') as temp_file:
                            pdf_writer.write(temp_file)
                        smaller_splits = self.split_pdf(temp_pdf, output_dir, f"{base_name}_P{split_num}")
                        os.remove(temp_pdf)
                        split_files.extend(smaller_splits)
                    else:
                        split_files.append(split_path)
                    
                    split_num += 1
        
        elif PDF_LIBRARY == 'pymupdf':
            import fitz
            doc = fitz.open(pdf_path)
            total_pages = len(doc)
            
            split_num = 1
            for start_page in range(0, total_pages, pages_per_split):
                end_page = min(start_page + pages_per_split, total_pages)
                
                new_doc = fitz.open()
                new_doc.insert_pdf(doc, from_page=start_page, to_page=end_page - 1)
                
                split_filename = f"{base_name}_P{split_num}.pdf"
                split_path = output_dir / split_filename
                
                new_doc.save(split_path)
                new_doc.close()
                
                # 실제 크기 확인
                actual_size = self.get_file_size_mb(split_path)
                if actual_size > self.MAX_SIZE_MB:
                    os.remove(split_path)
                    temp_pdf = output_dir / f"temp_{split_num}.pdf"
                    new_doc.save(temp_pdf)
                    new_doc.close()
                    smaller_splits = self.split_pdf(temp_pdf, output_dir, f"{base_name}_P{split_num}")
                    os.remove(temp_pdf)
                    split_files.extend(smaller_splits)
                else:
                    split_files.append(split_path)
                
                split_num += 1
            
            doc.close()
        
        return split_files
    
    def organize_file(self, pdf_path: Path) -> dict:
        """단일 PDF 파일 정리"""
        original_filename = pdf_path.name
        file_size_mb = self.get_file_size_mb(pdf_path)
        
        # 과목 추출 (6개 폴더만)
        subject = self.extract_subject(original_filename)
        
        # 대상 폴더 경로 생성 (과목별 폴더만)
        target_folder = self.target_dir / subject
        target_folder.mkdir(parents=True, exist_ok=True)
        
        # 전체 페이지 수 계산
        total_pages = self.get_total_pages(pdf_path)
        
        # 파일명 표준화 (확장자 제외한 부분)
        base_standardized = self.standardize_filename(original_filename, subject)
        standardized_name = Path(base_standardized).stem  # 확장자 제거
        
        result_info = {
            'original_filename': original_filename,
            'standardized_filename': base_standardized,
            'subject': subject,
            'size_mb': round(file_size_mb, 2),
            'total_pages': total_pages,
            'status': '',
            'new_location': '',
            'split_count': 0
        }
        
        # 8MB 초과 시 분할
        if file_size_mb > self.MAX_SIZE_MB:
            print(f"  [경고] 파일 크기 {file_size_mb:.2f}MB > 8MB, 분할 중...")
            
            split_files = self.split_pdf(pdf_path, target_folder, standardized_name)
            
            result_info['status'] = '분할됨'
            result_info['split_count'] = len(split_files)
            result_info['new_location'] = str(target_folder)
            
            # 분할된 파일들의 페이지 수도 기록
            print(f"  [완료] {len(split_files)}개 파일로 분할 완료 (총 {total_pages}페이지)")
        
        else:
            # 파일명 표준화
            target_path = target_folder / base_standardized
            
            # 같은 이름의 파일이 이미 있으면 이름 변경
            if target_path.exists():
                base_name = Path(base_standardized).stem
                extension = Path(base_standardized).suffix
                counter = 1
                while target_path.exists():
                    new_name = f"{base_name}_{counter}{extension}"
                    target_path = target_folder / new_name
                    counter += 1
                result_info['standardized_filename'] = target_path.name
            
            shutil.copy2(pdf_path, target_path)
            result_info['status'] = '이동됨'
            result_info['new_location'] = str(target_path)
            
            print(f"  [완료] 이동 완료: {target_path.name} ({total_pages}페이지)")
        
        return result_info
    
    def process_all(self):
        """폴더 내 모든 PDF 파일 처리"""
        # PDF 파일 찾기
        pdf_files = list(self.source_dir.glob('*.pdf'))
        pdf_files.extend(list(self.source_dir.glob('*.PDF')))
        
        # organized 폴더는 제외
        pdf_files = [f for f in pdf_files if 'organized' not in str(f)]
        
        if not pdf_files:
            print(f"[경고] PDF 파일을 찾을 수 없습니다: {self.source_dir}")
            return
        
        total_files = len(pdf_files)
        print(f"\n[찾음] 총 {total_files}개의 PDF 파일을 찾았습니다.\n")
        print("=" * 60)
        
        for idx, pdf_file in enumerate(pdf_files, 1):
            print(f"\n[{idx}/{total_files}] 처리 중: {pdf_file.name}")
            
            try:
                result_info = self.organize_file(pdf_file)
                self.processed_files.append(result_info)
            
            except Exception as e:
                print(f"  [오류] 발생: {e}")
                self.processed_files.append({
                    'original_filename': pdf_file.name,
                    'standardized_filename': pdf_file.name,
                    'subject': '오류',
                    'size_mb': round(self.get_file_size_mb(pdf_file), 2),
                    'total_pages': 0,
                    'status': f'오류: {str(e)}',
                    'new_location': '',
                    'split_count': 0
                })
        
        print("\n" + "=" * 60)
        print(f"\n[완료] 모든 파일 처리 완료!\n")
    
    def save_file_list(self, output_filename: str = 'file_list.csv'):
        """처리 완료된 파일 목록을 CSV로 저장"""
        if not self.processed_files:
            print("[경고] 저장할 파일 목록이 없습니다.")
            return
        
        output_path = self.BASE_DIR / output_filename
        
        # CSV 헤더
        fieldnames = [
            '원본파일명', '표준화파일명', '과목', '크기(MB)', '전체페이지수',
            '상태', '새위치', '분할개수', '처리일시'
        ]
        
        with open(output_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for file_info in self.processed_files:
                writer.writerow({
                    '원본파일명': file_info['original_filename'],
                    '표준화파일명': file_info['standardized_filename'],
                    '과목': file_info['subject'],
                    '크기(MB)': file_info['size_mb'],
                    '전체페이지수': file_info['total_pages'],
                    '상태': file_info['status'],
                    '새위치': file_info['new_location'],
                    '분할개수': file_info['split_count'],
                    '처리일시': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                })
        
        print(f"[저장] 파일 목록 저장 완료: {output_path}")
        print(f"   총 {len(self.processed_files)}개 파일 정보 저장됨")


def main():
    """메인 실행 함수"""
    import sys
    
    print("=" * 60)
    print("[PDF 수학 문제집 정리 도구 - 단순화 버전]")
    print("=" * 60)
    
    # 경로 고정: C:\Users\a\Documents\MathPDF
    base_dir = Path(r'C:\Users\a\Documents\MathPDF')
    print(f"\n[기본 경로] {base_dir}")
    
    try:
        # PDF Organizer 생성 (경로 고정)
        organizer = PDFOrganizer()
        print(f"[원본 폴더] {organizer.source_dir}")
        print(f"[대상 폴더] {organizer.target_dir}\n")
        
        # 모든 파일 처리
        organizer.process_all()
        
        # 파일 목록 저장
        organizer.save_file_list()
        
        print("\n[완료] 모든 작업이 완료되었습니다!")
    
    except Exception as e:
        print(f"\n[오류] 발생: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()