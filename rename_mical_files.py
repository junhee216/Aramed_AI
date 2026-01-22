# rename_mical_files.py
# 미적분_2025학년도_현우진_드릴 폴더의 파일명 마지막 숫자를 P1, P2 형식으로 변경

import os
import re
from pathlib import Path

# 폴더 경로
base_dir = Path(r'C:\Users\a\Documents\MathPDF\organized\현우진\미적분_2025학년도_현우진_드릴')

def rename_files():
    """파일명의 마지막 숫자를 P1, P2 형식으로 변경"""
    
    if not base_dir.exists():
        print(f"[오류] 폴더를 찾을 수 없습니다: {base_dir}")
        return
    
    print(f"폴더: {base_dir}\n")
    
    # 모든 파일 목록 가져오기
    files = list(base_dir.glob('*'))
    files = [f for f in files if f.is_file()]
    
    print(f"총 {len(files)}개 파일 발견\n")
    
    renamed_count = 0
    
    for file_path in files:
        old_name = file_path.name
        
        # 마지막 숫자 패턴 찾기 (예: _01, _02, _03 등)
        # 패턴: _숫자 (파일명 중간 또는 끝부분)
        # _01_문제, _01_해설, _01.pdf 등 모든 경우 처리
        pattern = r'_(\d{2})(?=_|\.|$)'
        
        match = re.search(pattern, old_name)
        if match:
            number = match.group(1)
            new_number = f'P{int(number)}'  # 01 -> P1, 02 -> P2
            
            # 새 파일명 생성 (첫 번째 매치만 변경)
            new_name = re.sub(pattern, f'_{new_number}', old_name, count=1)
            
            if old_name != new_name:
                new_path = file_path.parent / new_name
                
                # 파일명이 이미 존재하는지 확인
                if new_path.exists():
                    print(f"[건너뜀] 이미 존재: {new_name}")
                else:
                    try:
                        file_path.rename(new_path)
                        print(f"[변경] {old_name}")
                        print(f"       -> {new_name}")
                        renamed_count += 1
                    except Exception as e:
                        print(f"[오류] {old_name} -> {e}")
        else:
            # 숫자 패턴이 없는 파일은 건너뜀
            pass
    
    print(f"\n[완료] {renamed_count}개 파일 이름 변경됨")

if __name__ == '__main__':
    rename_files()
