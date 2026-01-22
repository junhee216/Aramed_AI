# check_downloads_original.py
# 다운로드 폴더에서 원본 파일 확인

from pathlib import Path
import csv
import sys

def find_original_files():
    """다운로드 폴더에서 원본 파일 찾기"""
    downloads = Path.home() / 'Downloads'
    
    print("="*70)
    print("[다운로드 폴더 원본 파일 확인]")
    print("="*70)
    print(f"\n검색 경로: {downloads}\n")
    
    # P3 관련 파일 찾기
    p3_files = []
    for pattern in ['*P3*.csv', '*p3*.csv', '*P3*.CSV', '*p3*.CSV']:
        p3_files.extend(downloads.glob(pattern))
    
    # 미적분 2025 관련 파일 찾기
    calc_files = []
    for pattern in ['*미적*.csv', '*2025*.csv']:
        calc_files.extend(downloads.glob(pattern))
    
    all_files = list(set(p3_files + calc_files))
    
    print(f"[P3 또는 미적분 관련 CSV 파일]")
    print("-"*70)
    
    if not all_files:
        print("  파일을 찾을 수 없습니다.")
        return None
    
    # 파일명에 P3가 포함된 파일 우선
    p3_related = [f for f in all_files if 'P3' in f.name or 'p3' in f.name.lower()]
    
    if p3_related:
        print(f"\n[P3 관련 파일 {len(p3_related)}개 발견]:")
        for f in p3_related:
            print(f"  - {f.name}")
            print(f"    크기: {f.stat().st_size / 1024:.1f} KB")
            print(f"    수정일: {f.stat().st_mtime}")
            print()
        return p3_related[0]  # 첫 번째 파일 반환
    
    # 전체 파일 목록
    print(f"\n[전체 관련 파일 {len(all_files)}개]:")
    for f in all_files[:10]:
        print(f"  - {f.name}")
    
    if all_files:
        return all_files[0]
    
    return None

def read_csv_file(file_path):
    """CSV 파일 읽기"""
    try:
        with open(file_path, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        return rows
    except:
        try:
            with open(file_path, 'r', encoding='cp949') as f:
                reader = csv.DictReader(f)
                rows = list(reader)
            return rows
        except Exception as e:
            print(f"[오류] 파일 읽기 실패: {e}")
            return None

if __name__ == '__main__':
    file_path = find_original_files()
    
    if file_path:
        print(f"\n[파일 내용 확인: {file_path.name}]")
        print("-"*70)
        
        rows = read_csv_file(file_path)
        
        if rows:
            print(f"총 {len(rows)}개 행 발견\n")
            
            # 첫 3개 행 확인
            print("[첫 3개 행 샘플]:")
            for i, row in enumerate(rows[:3], 1):
                print(f"\n[{i}]")
                if '문제ID' in row:
                    print(f"  문제ID: {row.get('문제ID', '')}")
                if '변형요소' in row:
                    variation = row.get('변형요소', '')
                    print(f"  변형요소: {variation[:50]}..." if len(variation) > 50 else f"  변형요소: {variation}")
                if 'LaTeX예시' in row:
                    latex = row.get('LaTeX예시', '')
                    print(f"  LaTeX예시: {latex[:50]}..." if len(latex) > 50 else f"  LaTeX예시: {latex}")
            
            print(f"\n[파일 정보]")
            print(f"  경로: {file_path}")
            print(f"  총 행 수: {len(rows)}")
            print(f"  컬럼: {', '.join(rows[0].keys()[:5])}...")
        else:
            print("파일을 읽을 수 없습니다.")
    else:
        print("\n[오류] 원본 파일을 찾을 수 없습니다.")
