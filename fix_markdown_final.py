# fix_markdown_final.py
# 마크다운 파일 최종 수정

import re
from pathlib import Path

def fix_markdown(md_path):
    """마크다운 파일의 수식 오류 최종 수정"""
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 잘린 수식 수정
    # $\bar{X$ → $\bar{X}$
    content = re.sub(r'\$\\bar\{X\$', r'$\\bar{X}$', content)
    
    # 제목에서 잘못된 부분 제거
    content = re.sub(r'## Drill 표본평균 \$\$\\bar\{X\$', r'## Drill 표본평균 $\\bar{X}$', content)
    content = re.sub(r'\$\$의 평균, 분산, 표준편차\}', '의 평균, 분산, 표준편차', content)
    content = re.sub(r'\$\$의 분포\}', '의 분포', content)
    content = re.sub(r'\$\$의 범위에 관한 확률\}', '의 범위에 관한 확률', content)
    
    # 수식 블록 앞뒤 공백 추가
    content = re.sub(r'([가-힣])\$\$', r'\1\n\n$$', content)
    content = re.sub(r'\$\$([가-힣])', r'$$\n\n\1', content)
    
    # 인라인 수식과 한글 사이 공백 추가
    content = re.sub(r'\$([^$]+)\$([가-힣])', r'$\1$ \2', content)
    content = re.sub(r'([가-힣])\$([^$]+)\$', r'\1 $\2$', content)
    
    # 표 형식 개선
    content = re.sub(r'\| --- \| --- \|\n\| \$z\$', r'| $z$ | $P(0 \\leq Z \\leq z)$ |\n| --- | --- |', content)
    
    # 줄바꿈 정리
    content = re.sub(r'\n{3,}', '\n\n', content)
    
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return content

def main():
    md_path = Path(r'C:\Users\a\Documents\MathPDF\organized\현우진\확통_2024학년도_현우진_드릴\확통_2024학년도_현우진_드릴_P7_해설_deepseek_r1.md')
    fix_markdown(md_path)
    print("수정 완료")

if __name__ == '__main__':
    main()
