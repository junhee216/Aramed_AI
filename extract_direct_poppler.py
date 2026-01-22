# extract_direct_poppler.py
# Poppler를 직접 사용하여 PDF를 이미지로 변환 후 OCR

import sys
import os
import subprocess
import tempfile
from pathlib import Path
from PIL import Image

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

def extract_text_with_ocr(pdf_path, page_num=0):
    """Poppler를 직접 사용하여 PDF를 이미지로 변환 후 OCR"""
    if not TESSERACT_AVAILABLE:
        print('[오류] pytesseract가 설치되지 않았습니다.')
        return None
    
    poppler_bin = r'C:\Users\a\Downloads\Release-25.12.0-0\poppler-25.12.0\Library\bin'
    
    # pdftocairo 시도 (더 안정적일 수 있음)
    pdftocairo_exe = os.path.join(poppler_bin, 'pdftocairo.exe')
    pdftoppm_exe = os.path.join(poppler_bin, 'pdftoppm.exe')
    
    exe_to_use = None
    if os.path.exists(pdftocairo_exe):
        exe_to_use = pdftocairo_exe
        print('[정보] pdftocairo 사용')
    elif os.path.exists(pdftoppm_exe):
        exe_to_use = pdftoppm_exe
        print('[정보] pdftoppm 사용')
    else:
        print(f'[오류] Poppler 실행 파일을 찾을 수 없습니다.')
        return None
    
    try:
        # 임시 디렉토리 생성
        with tempfile.TemporaryDirectory() as temp_dir:
            output_file = os.path.join(temp_dir, f'page-{page_num + 1}.png')
            
            print(f'[진행] PDF를 이미지로 변환 중... (페이지 {page_num + 1})')
            
            # pdftocairo 또는 pdftoppm 실행 (DPI 600으로 높게 설정)
            if 'pdftocairo' in exe_to_use:
                cmd = [
                    exe_to_use,
                    '-png',
                    '-r', '600',  # DPI 600 (OCR 정확도 향상)
                    '-f', str(page_num + 1),  # 첫 페이지
                    '-l', str(page_num + 1),  # 마지막 페이지
                    str(pdf_path),
                    output_file.replace('.png', '')  # 확장자 제거 (pdftocairo가 자동 추가)
                ]
            else:
                cmd = [
                    exe_to_use,
                    '-png',
                    '-r', '300',  # DPI
                    '-f', str(page_num + 1),  # 첫 페이지
                    '-l', str(page_num + 1),  # 마지막 페이지
                    str(pdf_path),
                    output_file.replace('.png', '')  # 확장자 제거
                ]
            
            # 환경 변수에 Poppler bin 경로 추가 (DLL 찾기 위해)
            env = os.environ.copy()
            current_path = env.get('PATH', '')
            if poppler_bin not in current_path:
                env['PATH'] = poppler_bin + os.pathsep + current_path
            
            # 작업 디렉토리를 Poppler bin으로 설정하여 DLL을 찾을 수 있도록
            # shell=True로 시도 (Windows에서 더 안정적일 수 있음)
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, env=env, cwd=poppler_bin, shell=False, timeout=30)
            except subprocess.TimeoutExpired:
                print('[오류] pdftoppm 실행 시간 초과')
                return None
            except FileNotFoundError:
                # 절대 경로로 재시도
                cmd[0] = exe_to_use
                result = subprocess.run(cmd, capture_output=True, text=True, env=env, cwd=poppler_bin, shell=False, timeout=30)
            
            if result.returncode != 0:
                print(f'[오류] pdftoppm 실행 실패 (코드: {result.returncode})')
                if result.stdout:
                    print(f'[출력] {result.stdout}')
                if result.stderr:
                    print(f'[오류 메시지] {result.stderr}')
                return None
            
            if result.stdout:
                print(f'[정보] pdftoppm 출력: {result.stdout}')
            
            # 생성된 이미지 파일 찾기
            if 'pdftocairo' in exe_to_use:
                # pdftocairo는 파일명에 페이지 번호를 추가 (예: page-1-01.png)
                image_files = list(Path(temp_dir).glob('*.png'))
            else:
                image_files = list(Path(temp_dir).glob('page-*.png'))
            
            if not image_files:
                print('[오류] 이미지 파일이 생성되지 않았습니다.')
                print(f'[디버그] 임시 디렉토리 내용: {list(Path(temp_dir).iterdir())}')
                return None
            
            image_file = image_files[0]
            print(f'[완료] 이미지 생성 완료: {image_file.name}')
            
            # OCR 처리
            print('[진행] OCR 처리 중... (시간이 걸릴 수 있습니다)')
            try:
                image = Image.open(image_file)
                print(f'[정보] 원본 이미지 크기: {image.size}, 모드: {image.mode}')
                
                # 이미지 전처리: 흑백 변환 및 대비 향상
                # 1. 그레이스케일 변환
                if image.mode != 'L':
                    image = image.convert('L')
                    print('[전처리] 그레이스케일 변환 완료')
                
                # 2. 대비 향상 (ImageEnhance 사용)
                enhancer = ImageEnhance.Contrast(image)
                image = enhancer.enhance(2.0)  # 대비 2배 증가
                print('[전처리] 대비 향상 완료 (2.0x)')
                
                # 3. 선명도 향상 (선택적)
                enhancer_sharp = ImageEnhance.Sharpness(image)
                image = enhancer_sharp.enhance(1.5)  # 선명도 1.5배 증가
                print('[전처리] 선명도 향상 완료 (1.5x)')
                
                print(f'[정보] 전처리 후 이미지 크기: {image.size}')
                
                # 사용 가능한 언어 확인
                try:
                    available_langs = pytesseract.get_languages()
                    print(f'[정보] 사용 가능한 언어: {available_langs}')
                except:
                    pass
                
                # Tesseract 설정: --oem 3 --psm 6 (문단 구조 강제 인식)
                tesseract_config = '--oem 3 --psm 6'
                print(f'[설정] Tesseract 옵션: {tesseract_config}')
                
                # 먼저 한국어+영어 시도
                text = None
                lang_options = ['kor+eng', 'kor', 'eng']
                for lang_option in lang_options:
                    try:
                        print(f'[시도] 언어: {lang_option}')
                        text = pytesseract.image_to_string(image, lang=lang_option, config=tesseract_config)
                        if text and len(text.strip()) > 50:  # 의미있는 텍스트가 추출되었는지 확인
                            print(f'[성공] 언어 {lang_option}로 OCR 완료: {len(text)} 문자')
                            break
                        else:
                            print(f'[경고] 언어 {lang_option} 결과가 너무 짧음: {len(text) if text else 0} 문자')
                    except Exception as lang_error:
                        print(f'[경고] 언어 {lang_option} 실패: {lang_error}')
                        continue
                
                if not text:
                    print('[오류] 모든 언어 옵션 실패')
                    return None
                
                print(f'[최종] OCR 결과 길이: {len(text)} 문자')
                
                if not text or len(text.strip()) == 0:
                    print('[경고] OCR 결과가 비어있습니다.')
                    print('[디버그] 이미지 파일을 확인해보세요.')
                    # 이미지 파일을 현재 디렉토리에 복사 (디버깅용)
                    debug_image = Path('debug_page1.png')
                    import shutil
                    shutil.copy(image_file, debug_image)
                    print(f'[디버그] 이미지 저장: {debug_image.absolute()}')
                    return None
                
                return text
            except Exception as e:
                print(f'[오류] OCR 처리 실패: {e}')
                import traceback
                traceback.print_exc()
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
        print('[오류] 텍스트를 추출할 수 없습니다.')
        sys.exit(1)
    
    print('\n' + '=' * 60)
    print('[전체 페이지 내용 (OCR 결과)]')
    print('=' * 60)
    # 인코딩 오류 방지
    try:
        print(text)
    except UnicodeEncodeError:
        print(text.encode('utf-8', errors='replace').decode('utf-8', errors='replace'))
    print('\n' + '=' * 60)
    
    problem_text, solution_text = analyze_problem_structure(text)
    
    print('\n[추출된 문제 내용]')
    print('=' * 60)
    problem_output = problem_text if problem_text else '(문제 내용을 찾을 수 없습니다)'
    try:
        print(problem_output)
    except UnicodeEncodeError:
        print(problem_output.encode('utf-8', errors='replace').decode('utf-8', errors='replace'))
    print('=' * 60)
    
    print('\n[추출된 해설 내용]')
    print('=' * 60)
    solution_output = solution_text if solution_text else '(해설 내용을 찾을 수 없습니다)'
    try:
        print(solution_output)
    except UnicodeEncodeError:
        print(solution_output.encode('utf-8', errors='replace').decode('utf-8', errors='replace'))
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

if __name__ == '__main__':
    main()