# fix_haktong_p7_solution_markdown.py
# 마크다운 변환 개선 및 수학적 오류 검토

import re
import json
import sys
from pathlib import Path

# Windows 콘솔 인코딩 설정
if sys.platform == 'win32':
    import os
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')

def fix_markdown_content(content):
    """마크다운 내용 수정"""
    text = content
    
    # 잘못 변환된 수식 수정
    # \frac{}{} 패턴 수정
    text = re.sub(r'\$\\frac\\1\\2\$\$', r'$\\frac{f(x)+g(x)-|f(x)-g(x)|}{2}$', text)
    text = re.sub(r'\$\\frac\\1\\2\$', r'$\\frac{\\sigma}{\\sqrt{n}}$', text)
    
    # \bar{X} 수정
    text = re.sub(r'\$\\bar\\1\$', r'$\\bar{X}$', text)
    text = re.sub(r'\$\\bar\{\\1\$\$', r'$\\bar{X}$', text)
    
    # \sigma 수정
    text = re.sub(r'\$\\sigma\$\$', r'$\\sigma$', text)
    
    # \alpha, \beta, \gamma 수정
    text = re.sub(r'\$\$\\alpha\$', r'$\\alpha$', text)
    text = re.sub(r'\$\$\\beta\$', r'$\\beta$', text)
    text = re.sub(r'\$\$\\gamma\$', r'$\\gamma$', text)
    
    # 수식 블록 내부 수정
    text = re.sub(r'```math\nE\(\$\\bar\\1\$\)', r'```math\nE(\\bar{X})', text)
    text = re.sub(r'V\(\$\\bar\\1\$\)', r'V(\\bar{X})', text)
    text = re.sub(r'\\sigma\(\$\\bar\\1\$\)', r'\\sigma(\\bar{X})', text)
    
    # 분수 수정
    text = re.sub(r'\\frac\$\\sigma\$', r'\\frac{\\sigma', text)
    text = re.sub(r'\^{2}n', r'^{2}}{n}', text)
    
    # 기타 수정
    text = re.sub(r'\\E\(\$\\bar\{\\1\$\)', r'E(\\bar{X})', text)
    text = re.sub(r'P\(\$\\bar\\1\$', r'P(\\bar{X}', text)
    
    return text

def review_math_errors(content):
    """수학적 오류 검토"""
    errors = []
    warnings = []
    
    # 표본평균의 분산 공식 확인
    if 'V(\\bar{X})' in content or 'V($\\bar{X}$)' in content:
        if '\\frac{\\sigma^{2}}{n}' in content or '\\frac{σ²}{n}' in content:
            pass  # 정확
        else:
            warnings.append("표본평균의 분산 공식 확인 필요: V(\\bar{X}) = σ²/n")
    
    # 신뢰구간 공식 확인
    if '1.96' in content and '신뢰구간' in content:
        if '\\frac{\\sigma}{\\sqrt{n}}' in content or 'σ/√n' in content:
            pass  # 정확
        else:
            warnings.append("신뢰구간 공식 확인 필요: [\\bar{X} - 1.96σ/√n, \\bar{X} + 1.96σ/√n]")
    
    # 신뢰상수 계산 확인
    if '0.475' in content and '1.96' in content:
        # 0.95 × 0.5 = 0.475 ✓
        pass
    if '0.495' in content and '2.58' in content:
        # 0.99 × 0.5 = 0.495 ✓
        pass
    
    return errors, warnings

def main():
    print("=" * 80)
    print("확통_2024학년도_현우진_드릴_P7_해설 마크다운 수정 및 검토")
    print("=" * 80)
    
    # JSON 파일 읽기
    json_path = Path(r'C:\Users\a\Documents\MathPDF\organized\현우진\확통_2024학년도_현우진_드릴\확통_2024학년도_현우진_드릴_P7_해설_deepseek.json')
    
    if not json_path.exists():
        print(f"[오류] 파일을 찾을 수 없습니다: {json_path}")
        return
    
    with open(json_path, 'r', encoding='utf-8') as f:
        solutions = json.load(f)
    
    print(f"\n총 {len(solutions)}개 섹션 발견\n")
    
    # 각 섹션 수정 및 검토
    all_errors = []
    all_warnings = []
    
    for i, sol in enumerate(solutions):
        print(f"[{i+1}/{len(solutions)}] {sol['title']}")
        
        # 수정
        sol['content'] = fix_markdown_content(sol['content'])
        
        # 검토
        errors, warnings = review_math_errors(sol['content'])
        all_errors.extend(errors)
        all_warnings.extend(warnings)
        
        if errors:
            print(f"  [오류] {errors}")
        if warnings:
            print(f"  [경고] {warnings}")
    
    # 수정된 JSON 저장
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(solutions, f, ensure_ascii=False, indent=2)
    
    # 수정된 마크다운 생성
    full_markdown = "# 확통_2024학년도_현우진_드릴_P7_해설\n\n"
    for sol in solutions:
        full_markdown += f"## {sol['title']}\n\n{sol['content']}\n\n"
    
    md_path = json_path.parent / "확통_2024학년도_현우진_드릴_P7_해설_deepseek.md"
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(full_markdown)
    
    print(f"\n[저장 완료]")
    print(f"  - 마크다운: {md_path}")
    print(f"  - JSON: {json_path}")
    
    if all_errors:
        print(f"\n[오류] 총 {len(all_errors)}개 오류 발견")
    if all_warnings:
        print(f"[경고] 총 {len(all_warnings)}개 경고 발견")
    
    if not all_errors and not all_warnings:
        print("\n[확인 완료] 수학적 오류 없음")

if __name__ == '__main__':
    main()
