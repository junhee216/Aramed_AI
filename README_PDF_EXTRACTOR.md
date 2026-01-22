# PDF 수학 문제집 단원별 정리 도구

PDF 파일에서 수학 문제집을 단원별로 추출하고 정리하는 Python 스크립트입니다.

## 📋 필요 사항

- Python 3.7 이상
- PDF 처리 라이브러리 (아래 중 하나)

## 🔧 설치 방법

### 1. Python 설치 확인
```bash
python --version
```

### 2. 필요한 라이브러리 설치

**권장: pdfplumber** (텍스트 추출 정확도가 높음)
```bash
pip install pdfplumber
```

또는

```bash
pip install -r requirements.txt
```

**다른 옵션들:**
- `PyPDF2`: 가볍지만 텍스트 추출 정확도가 낮을 수 있음
- `pymupdf` (fitz): 가장 빠르고 이미지 추출 가능

## 🚀 사용 방법

### 기본 사용법 (JSON 출력)
```bash
python pdf_math_extractor.py <PDF파일경로>
```

예시:
```bash
python pdf_math_extractor.py 수학문제집.pdf
```

### 텍스트 파일로 출력
```bash
python pdf_math_extractor.py 수학문제집.pdf text
```

## 📊 출력 형식

### JSON 형식 (기본)
- 파일명: `<PDF파일명>_extracted.json`
- 구조:
```json
{
  "source_file": "수학문제집.pdf",
  "extracted_at": "2026-01-11T...",
  "units": {
    "1단원: 함수": [
      {
        "number": 1,
        "content": "문제 내용...",
        "page": 1,
        "sub_problems": ["가) ...", "나) ..."]
      }
    ]
  }
}
```

### 텍스트 파일 형식
- 디렉토리: `<PDF파일명>_extracted/`
- 각 단원별로 `.txt` 파일 생성
- 파일명 예: `1단원_함수.txt`

## ⚙️ 주요 기능

1. **단원 자동 감지**
   - 제N단원, Unit N, Chapter N 등 다양한 패턴 지원
   - 정규표현식 기반 패턴 매칭

2. **문제 번호 인식**
   - 1번, 1., 1), (1), ①②③ 등 다양한 형식 지원

3. **하위 문제 추출**
   - 가), 나), 다) 형식의 하위 문제 자동 추출

4. **유연한 출력**
   - JSON 형식 (프로그래밍 처리용)
   - 텍스트 파일 형식 (읽기용)

## 🔍 단원 패턴 커스터마이징

PDF의 단원 패턴이 다르다면 `pdf_math_extractor.py`의 `detect_unit_patterns()` 메서드를 수정하세요:

```python
unit_patterns = [
    r'제?\s*(\d+)\s*단원[:\s]*([^\n]+)',  # 제1단원: 함수
    r'Unit\s*(\d+)[:\s]*([^\n]+)',        # Unit 1: Functions
    # 여기에 새로운 패턴 추가
]
```

## 💡 사용 팁

1. **PDF 품질**: 스캔된 이미지 PDF보다 텍스트가 추출 가능한 PDF가 더 정확합니다.

2. **패턴 조정**: 추출 결과가 부정확하다면 PDF의 실제 단원/문제 형식을 확인하고 정규표현식 패턴을 조정하세요.

3. **대량 처리**: 여러 PDF를 처리하려면 간단한 루프 스크립트를 작성하세요:

```python
import glob
from pdf_math_extractor import PDFMathExtractor

for pdf_file in glob.glob("*.pdf"):
    extractor = PDFMathExtractor(pdf_file)
    extractor.save_to_json()
```

## 📝 예시

```bash
# JSON 출력
python pdf_math_extractor.py 수학_1학년_1학기.pdf

# 텍스트 파일 출력
python pdf_math_extractor.py 수학_1학년_1학기.pdf text
```

## ⚠️ 주의사항

- PDF의 구조와 형식에 따라 추출 정확도가 달라질 수 있습니다.
- 복잡한 수식이나 이미지는 텍스트로 변환되지 않을 수 있습니다.
- 추출 결과를 반드시 확인하고 필요시 수동으로 보정하세요.

## 🐛 문제 해결

**Q: "PDF 처리 라이브러리가 설치되지 않았습니다" 오류**
A: `pip install pdfplumber` 실행

**Q: 단원이 제대로 감지되지 않아요**
A: PDF 파일을 열어 단원 표시 형식을 확인하고 `detect_unit_patterns()` 메서드의 정규표현식을 수정하세요.

**Q: 텍스트 추출이 부정확해요**
A: `pdfplumber` 대신 `pymupdf`를 시도하거나, PDF가 이미지 스캔본인 경우 OCR이 필요할 수 있습니다.

## 📚 관련 링크

- [pdfplumber 문서](https://github.com/jsvine/pdfplumber)
- [PyPDF2 문서](https://pypdf2.readthedocs.io/)
- [PyMuPDF 문서](https://pymupdf.readthedocs.io/)