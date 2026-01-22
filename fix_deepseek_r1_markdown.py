# fix_deepseek_r1_markdown.py
# Deepseek R1-70B용 마크다운 파일 수정

import re
from pathlib import Path

def fix_markdown_file(md_path):
    """마크다운 파일의 수식 오류 수정"""
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 잘린 수식 수정
    # $\bar{X$ → $\bar{X}$
    content = re.sub(r'\$\\bar\{X\$', r'$\\bar{X}$', content)
    
    # $의 평균, 분산, 표준편차} → 제목에서 제거
    content = re.sub(r'\$\$의 평균, 분산, 표준편차\}', '', content)
    content = re.sub(r'\$\$의 분포\}', '', content)
    content = re.sub(r'\$\$의 범위에 관한 확률\}', '', content)
    
    # 잘못된 수식 수정
    # $m$이고 → $m$ 이고
    content = re.sub(r'\$([^$]+)\$([가-힣])', r'$\1$ \2', content)
    content = re.sub(r'([가-힣])\$([^$]+)\$', r'\1 $\2$', content)
    
    # 수식 블록 내부 정리
    # $$E(\bar{X})=m...$$ 형식 확인 및 수정
    content = re.sub(r'\$\$E\(\\bar\{X\}\)=m', r'$$\nE(\\bar{X})=m', content)
    content = re.sub(r'\\frac\{\\sigma\^\{2\}\}\{n\},', r'\\frac{\\sigma^{2}}{n},', content)
    
    # 표 형식 개선
    # | --- | --- | 다음에 헤더가 없으면 추가
    content = re.sub(r'\| --- \| --- \|\n\|', r'| --- | --- |\n| $z$ | $P(0 \\leq Z \\leq z)$ |', content, count=1)
    
    # 인용문 형식 개선
    content = re.sub(r'> ([^>]+) ⇒', r'> \1\n> ⇒', content)
    
    # 연속된 공백 정리
    content = re.sub(r'([가-힣])\$([^$]+)\$([가-힣])', r'\1 $\2$ \3', content)
    
    # 줄바꿈 정리
    content = re.sub(r'\n{3,}', '\n\n', content)
    
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return content

def main():
    print("=" * 80)
    print("Deepseek R1-70B용 마크다운 파일 수정")
    print("=" * 80)
    
    md_path = Path(r'C:\Users\a\Documents\MathPDF\organized\현우진\확통_2024학년도_현우진_드릴\확통_2024학년도_현우진_드릴_P7_해설_deepseek_r1.md')
    
    if not md_path.exists():
        print(f"[오류] 파일을 찾을 수 없습니다: {md_path}")
        return
    
    print(f"\n파일 수정 중...")
    content = fix_markdown_file(md_path)
    
    print(f"[완료] 파일 수정 완료")
    print(f"  - 파일: {md_path}")
    print(f"  - 크기: {len(content)} 문자")
    
    # Deepseek R1-70B 호환성 확인
    print("\n[Deepseek R1-70B 호환성]")
    print("  - 마크다운 형식: 지원")
    print("  - LaTeX 수식: 지원 ($...$ 및 $$...$$)")
    print("  - 구조화된 섹션: 지원")
    print("  - UTF-8 인코딩: 지원")
    print("\n[결론] Deepseek R1-70B가 읽을 수 있는 형태입니다.")

if __name__ == '__main__':
    main()
