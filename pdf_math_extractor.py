# pdf_math_extractor.py
# PDF 수학 문제집을 단원별로 정리하는 스크립트
# Python 3.7+ 필요

import re
import json
import os
from pathlib import Path
from typing import List, Dict, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime

try:
    import PyPDF2
    PDF_LIBRARY = 'PyPDF2'
except ImportError:
    try:
        import pdfplumber
        PDF_LIBRARY = 'pdfplumber'
    except ImportError:
        try:
            import fitz  # PyMuPDF
            PDF_LIBRARY = 'pymupdf'
        except ImportError:
            PDF_LIBRARY = None


@dataclass
class Problem:
    """수학 문제 데이터 구조"""
    unit: str  # 단원 이름
    number: int  # 문제 번호
    content: str  # 문제 내용
    page: int  # 페이지 번호
    sub_problems: List[str] = None  # 하위 문제들 (가), 나), 다) 등)

    def __post_init__(self):
        if self.sub_problems is None:
            self.sub_problems = []


class PDFMathExtractor:
    """PDF 수학 문제집 단원별 추출기"""
    
    def __init__(self, pdf_path: str):
        self.pdf_path = Path(pdf_path)
        if not self.pdf_path.exists():
            raise FileNotFoundError(f"PDF 파일을 찾을 수 없습니다: {pdf_path}")
        
        self.problems: List[Problem] = []
        self._check_library()
    
    def _check_library(self):
        """PDF 처리 라이브러리 확인"""
        if PDF_LIBRARY is None:
            raise ImportError(
                "PDF 처리 라이브러리가 설치되지 않았습니다.\n"
                "다음 중 하나를 설치해주세요:\n"
                "  pip install PyPDF2\n"
                "  pip install pdfplumber\n"
                "  pip install pymupdf"
            )
    
    def extract_text(self) -> List[Tuple[int, str]]:
        """PDF에서 텍스트 추출 (페이지 번호와 함께)"""
        pages_text = []
        
        if PDF_LIBRARY == 'PyPDF2':
            with open(self.pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page_num, page in enumerate(pdf_reader.pages, start=1):
                    text = page.extract_text()
                    pages_text.append((page_num, text))
        
        elif PDF_LIBRARY == 'pdfplumber':
            import pdfplumber
            with pdfplumber.open(self.pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages, start=1):
                    text = page.extract_text() or ''
                    pages_text.append((page_num, text))
        
        elif PDF_LIBRARY == 'pymupdf':
            import fitz
            doc = fitz.open(self.pdf_path)
            for page_num, page in enumerate(doc, start=1):
                text = page.get_text()
                pages_text.append((page_num, text))
            doc.close()
        
        return pages_text
    
    def detect_unit_patterns(self, text: str) -> List[Tuple[str, int]]:
        """텍스트에서 단원 패턴 감지"""
        unit_patterns = [
            # 일반적인 단원 패턴들
            r'제?\s*(\d+)\s*단원[:\s]*([^\n]+)',
            r'Unit\s*(\d+)[:\s]*([^\n]+)',
            r'Chapter\s*(\d+)[:\s]*([^\n]+)',
            r'(\d+)\.\s*([^\n]+단원)',
            r'단원\s*(\d+)[:\s]*([^\n]+)',
            # 숫자로 시작하는 제목 (단원으로 추정)
            r'^(\d+)\.\s*([^\n]+)$',
        ]
        
        units = []
        for pattern in unit_patterns:
            matches = re.finditer(pattern, text, re.MULTILINE | re.IGNORECASE)
            for match in matches:
                unit_name = match.group(2) if len(match.groups()) > 1 else match.group(0)
                # 간단한 단원 이름 정리
                unit_name = unit_name.strip().strip('.,:;')
                units.append((unit_name, match.start()))
        
        return units
    
    def detect_problem_patterns(self, text: str) -> List[Tuple[int, int]]:
        """문제 번호 패턴 감지 (예: 1번, (1), ① 등)"""
        problem_patterns = [
            r'(\d+)[번\.)]\s+',  # 1번, 1., 1)
            r'\((\d+)\)\s+',  # (1)
            r'[①②③④⑤⑥⑦⑧⑨⑩]',  # 원문자
            r'(\d+)\s*\.\s+[가-힣]',  # 1. 가)
        ]
        
        problems = []
        for pattern in problem_patterns:
            matches = re.finditer(pattern, text)
            for match in matches:
                if match.groups():
                    prob_num = int(match.group(1))
                else:
                    # 원문자의 경우
                    prob_num = ord(match.group(0)) - ord('①') + 1
                problems.append((prob_num, match.start()))
        
        # 위치 순으로 정렬
        problems.sort(key=lambda x: x[1])
        return problems
    
    def extract_by_units(self, unit_patterns: List[Tuple[str, int]], 
                         all_text: str, pages_text: List[Tuple[int, str]]) -> Dict[str, List[Problem]]:
        """단원별로 문제 추출"""
        units_problems: Dict[str, List[Problem]] = {}
        current_unit = "기타"
        
        # 전체 텍스트를 단원별로 분할
        unit_sections = {}
        for i, (unit_name, pos) in enumerate(unit_patterns):
            next_pos = unit_patterns[i + 1][1] if i + 1 < len(unit_patterns) else len(all_text)
            unit_sections[unit_name] = all_text[pos:next_pos]
        
        # 각 단원 섹션에서 문제 추출
        for unit_name, section_text in unit_sections.items():
            problems = self.extract_problems_from_text(section_text, unit_name)
            units_problems[unit_name] = problems
        
        return units_problems
    
    def extract_problems_from_text(self, text: str, unit_name: str, 
                                   start_page: int = 1) -> List[Problem]:
        """텍스트에서 문제 추출"""
        problems = []
        problem_positions = self.detect_problem_patterns(text)
        
        for i, (prob_num, pos) in enumerate(problem_positions):
            # 다음 문제까지의 내용
            next_pos = problem_positions[i + 1][1] if i + 1 < len(problem_positions) else len(text)
            content = text[pos:next_pos].strip()
            
            # 하위 문제 추출 (가), 나), 다) 등)
            sub_problems = re.findall(r'([가-힣])\)\s*([^\n]+)', content)
            sub_problems_text = [f"{sub[0]}) {sub[1]}" for sub in sub_problems]
            
            problem = Problem(
                unit=unit_name,
                number=prob_num,
                content=content,
                page=start_page,  # 페이지 추적 개선 필요
                sub_problems=sub_problems_text
            )
            problems.append(problem)
        
        return problems
    
    def process(self) -> Dict[str, List[Problem]]:
        """PDF 처리 메인 함수"""
        print(f"📄 PDF 파일 읽는 중: {self.pdf_path.name}")
        pages_text = self.extract_text()
        
        # 전체 텍스트 합치기
        all_text = '\n'.join([text for _, text in pages_text])
        
        print("🔍 단원 패턴 검색 중...")
        unit_patterns = self.detect_unit_patterns(all_text)
        
        if not unit_patterns:
            print("⚠️  단원 패턴을 찾지 못했습니다. 전체를 하나의 단원으로 처리합니다.")
            unit_patterns = [("전체", 0)]
        
        print(f"✅ {len(unit_patterns)}개의 단원을 찾았습니다:")
        for unit_name, _ in unit_patterns:
            print(f"   - {unit_name}")
        
        print("\n📝 문제 추출 중...")
        units_problems = self.extract_by_units(unit_patterns, all_text, pages_text)
        
        total_problems = sum(len(probs) for probs in units_problems.values())
        print(f"✅ 총 {total_problems}개의 문제를 추출했습니다.\n")
        
        return units_problems
    
    def save_to_json(self, output_path: str = None):
        """결과를 JSON 파일로 저장"""
        if output_path is None:
            output_path = self.pdf_path.stem + '_extracted.json'
        
        units_problems = self.process()
        
        # JSON 직렬화 가능한 형태로 변환
        result = {
            'source_file': str(self.pdf_path.name),
            'extracted_at': datetime.now().isoformat(),
            'units': {}
        }
        
        for unit_name, problems in units_problems.items():
            result['units'][unit_name] = [
                {
                    'number': p.number,
                    'content': p.content,
                    'page': p.page,
                    'sub_problems': p.sub_problems
                }
                for p in problems
            ]
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        print(f"💾 결과를 저장했습니다: {output_path}")
        return output_path
    
    def save_to_text_files(self, output_dir: str = None):
        """단원별로 텍스트 파일로 저장"""
        if output_dir is None:
            output_dir = self.pdf_path.stem + '_extracted'
        
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        units_problems = self.process()
        
        for unit_name, problems in units_problems.items():
            # 파일명에 사용할 수 없는 문자 제거
            safe_unit_name = re.sub(r'[<>:"/\\|?*]', '_', unit_name)
            file_path = output_path / f"{safe_unit_name}.txt"
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(f"단원: {unit_name}\n")
                f.write("=" * 50 + "\n\n")
                
                for problem in problems:
                    f.write(f"문제 {problem.number}\n")
                    f.write("-" * 30 + "\n")
                    f.write(problem.content)
                    f.write("\n\n")
                    
                    if problem.sub_problems:
                        for sub in problem.sub_problems:
                            f.write(f"  {sub}\n")
                        f.write("\n")
            
            print(f"💾 저장: {file_path}")
        
        return str(output_path)


def main():
    """메인 실행 함수"""
    import sys
    
    if len(sys.argv) < 2:
        print("사용법: python pdf_math_extractor.py <PDF파일경로> [출력형식]")
        print("출력형식: json (기본값) 또는 text")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    output_format = sys.argv[2] if len(sys.argv) > 2 else 'json'
    
    try:
        extractor = PDFMathExtractor(pdf_path)
        
        if output_format.lower() == 'text':
            extractor.save_to_text_files()
        else:
            extractor.save_to_json()
        
        print("\n✅ 처리가 완료되었습니다!")
    
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()