# path_utils.py
# 크로스 플랫폼 경로 유틸리티

import os
from pathlib import Path

def get_math_pdf_path():
    """MathPDF organized 디렉토리 경로 가져오기"""
    env_path = os.environ.get('MATHPDF_PATH')
    if env_path:
        return Path(env_path)
    
    # OS별 기본 경로
    home_dir = Path.home()
    
    if os.name == 'nt':  # Windows
        return home_dir / 'Documents' / 'MathPDF' / 'organized'
    else:  # Linux, macOS
        return home_dir / 'Documents' / 'MathPDF' / 'organized'

def get_geometry_problem_path(part):
    """기하 문제 파일 경로 가져오기"""
    base_path = get_math_pdf_path()
    return base_path / '현우진' / '기하_2024학년도_현우진_드릴' / f'기하_2024학년도_현우진_드릴_{part}_문제_deepseek.json'

def get_geometry_solution_path(part):
    """기하 해설 파일 경로 가져오기"""
    base_path = get_math_pdf_path()
    return base_path / '현우진' / '기하_2024학년도_현우진_드릴' / f'기하_2024학년도_현우진_드릴_{part}_해설_deepseek_r1.md'
