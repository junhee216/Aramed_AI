# extract_pages_to_png.py
# PDF에서 특정 페이지를 PNG 이미지로 추출

import sys
import os
import subprocess
import tempfile
from pathlib import Path

def find_poppler():
    """Poppler 경로 찾기"""
    poppler_paths = [
        r'C:\Users\a\Downloads\Release-25.12.0-0\poppler-25.12.0\Library\bin',
        r'C:\Program Files\poppler\bin',
        r'C:\poppler\bin',
    ]
    
    for path in poppler_paths:
        if os.path.exists(path):
            pdftocairo = os.path.join(path, 'pdftocairo.exe')
            if os.path.exists(pdftocairo):
                return path, pdftocairo
    
    return None, None

def extract_pages_to_png(pdf_path, page_numbers, output_dir=None, dpi=300):
    """
    PDF에서 특정 페이지를 PNG 이미지로 추출
    
    Args:
        pdf_path: PDF 파일 경로
        page_numbers: 추출할 페이지 번호 리스트 (1부터 시작)
        output_dir: 출력 디렉토리 (None이면 현재 디렉토리)
        dpi: 이미지 해상도 (기본 300)
    
    Returns:
        생성된 PNG 파일 경로 리스트
    """
    pdf_path = Path(pdf_path)
    if not pdf_path.exists():
        print(f'[오류] PDF 파일을 찾을 수 없습니다: {pdf_path}')
        return []
    
    poppler_bin, pdftocairo = find_poppler()
    if not pdftocairo:
        print('[오류] Poppler를 찾을 수 없습니다.')
        print('[안내] Poppler가 설치되어 있는지 확인해주세요.')
        return []
    
    print(f'[정보] Poppler 경로: {poppler_bin}')
    print(f'[정보] PDF 파일: {pdf_path.name}')
    print(f'[정보] 추출할 페이지: {page_numbers}')
    
    if output_dir is None:
        output_dir = Path.cwd()
    else:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
    
    output_files = []
    
    # 환경 변수 설정
    env = os.environ.copy()
    current_path = env.get('PATH', '')
    if poppler_bin not in current_path:
        env['PATH'] = poppler_bin + os.pathsep + current_path
    
    for page_num in page_numbers:
        # 페이지 번호는 1부터 시작하지만 pdftocairo는 0부터 시작하지 않음
        output_file = output_dir / f'page_{page_num}.png'
        
        cmd = [
            pdftocairo,
            '-png',
            '-r', str(dpi),  # DPI
            '-f', str(page_num),  # 첫 페이지
            '-l', str(page_num),  # 마지막 페이지
            str(pdf_path),
            str(output_file.with_suffix(''))  # 확장자 제거 (pdftocairo가 자동 추가)
        ]
        
        print(f'\n[진행] 페이지 {page_num} 추출 중...')
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                env=env,
                cwd=poppler_bin,
                timeout=30
            )
            
            if result.returncode != 0:
                print(f'[오류] 페이지 {page_num} 추출 실패 (코드: {result.returncode})')
                if result.stderr:
                    print(f'[오류 메시지] {result.stderr}')
                continue
            
            # pdftocairo는 파일명에 페이지 번호를 추가 (예: page_6-01.png)
            # 실제 생성된 파일 찾기
            pattern = output_file.stem + '*'
            created_files = list(output_dir.glob(pattern + '.png'))
            
            if created_files:
                # 파일명을 page_6.png로 변경
                created_file = created_files[0]
                final_file = output_dir / f'page_{page_num}.png'
                if created_file != final_file:
                    created_file.rename(final_file)
                output_files.append(final_file)
                print(f'[완료] 페이지 {page_num} 추출 완료: {final_file.name}')
            else:
                print(f'[경고] 페이지 {page_num} 이미지 파일을 찾을 수 없습니다.')
                print(f'[디버그] 출력 디렉토리 내용: {list(output_dir.glob("*.png"))}')
        
        except subprocess.TimeoutExpired:
            print(f'[오류] 페이지 {page_num} 추출 시간 초과')
        except Exception as e:
            print(f'[오류] 페이지 {page_num} 추출 중 오류: {e}')
    
    return output_files

def main():
    # PDF 파일 경로
    pdf_path = Path(r'C:\Users\a\Documents\MathPDF\organized\수1\수1_2025학년도_현우진_드릴_P1.pdf')
    
    # 추출할 페이지 번호 (6페이지, 7페이지)
    page_numbers = [6, 7]
    
    # 출력 디렉토리 (현재 디렉토리)
    output_dir = Path.cwd()
    
    print('=' * 60)
    print('PDF 페이지 추출 시작')
    print('=' * 60)
    
    output_files = extract_pages_to_png(pdf_path, page_numbers, output_dir, dpi=300)
    
    print('\n' + '=' * 60)
    print('추출 완료')
    print('=' * 60)
    
    if output_files:
        print(f'\n[생성된 파일]')
        for file in output_files:
            print(f'  - {file.absolute()}')
    else:
        print('\n[경고] 추출된 파일이 없습니다.')

if __name__ == '__main__':
    main()
