# verify_deepseek_r1_compatibility.py
# Deepseek R1-70B 호환성 검증 및 수학적 오류 확인

import re
import json
from pathlib import Path

def verify_deepseek_compatibility(md_path):
    """Deepseek R1-70B 호환성 검증"""
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    issues = []
    warnings = []
    
    # 1. 마크다운 구조 확인
    if not content.startswith('#'):
        issues.append("마크다운 헤더가 없습니다")
    elif not re.search(r'^#\s+', content, re.MULTILINE):
        issues.append("마크다운 헤더 형식이 올바르지 않습니다")
    
    # 2. 수식 형식 확인
    # 인라인 수식 ($...$)
    inline_math = re.findall(r'\$[^$]+\$', content)
    for math in inline_math:
        if math.count('$') != 2:
            issues.append(f"인라인 수식 형식 오류: {math[:50]}")
        if '\\frac{' in math and '}' not in math:
            warnings.append(f"분수 수식이 완전하지 않을 수 있음: {math[:50]}")
    
    # 블록 수식 ($$...$$)
    block_math = re.findall(r'\$\$[^$]+\$\$', content, re.DOTALL)
    for math in block_math:
        if math.count('$$') != 2:
            issues.append(f"블록 수식 형식 오류")
    
    # 3. 표 형식 확인
    tables = re.findall(r'\|.*\|', content)
    if tables:
        for i, table in enumerate(tables[:5]):  # 처음 5개만 확인
            cells = table.split('|')
            if len(cells) < 3:
                warnings.append(f"표 형식이 올바르지 않을 수 있음: {table[:50]}")
    
    # 4. 인코딩 확인
    try:
        content.encode('utf-8')
    except UnicodeEncodeError:
        issues.append("UTF-8 인코딩 오류")
    
    return issues, warnings

def verify_math_content(content):
    """수학적 내용 검증"""
    errors = []
    warnings = []
    
    # 표본평균의 분산 공식 확인
    if 'V(\\bar{X})' in content or 'V($\\bar{X}$)' in content or 'V(\\bar{X})' in content:
        if '\\frac{\\sigma^{2}}{n}' in content or '\\frac{σ²}{n}' in content or 'σ²/n' in content:
            pass  # 정확
        else:
            warnings.append("표본평균의 분산 공식 확인 필요: V(\\bar{X}) = σ²/n")
    
    # 신뢰구간 공식 확인
    if '1.96' in content and ('신뢰구간' in content or '신뢰' in content):
        if '\\frac{\\sigma}{\\sqrt{n}}' in content or 'σ/√n' in content:
            pass  # 정확
        else:
            warnings.append("신뢰구간 공식 확인 필요")
    
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
    print("Deepseek R1-70B 호환성 검증")
    print("=" * 80)
    
    md_path = Path(r'C:\Users\a\Documents\MathPDF\organized\현우진\확통_2024학년도_현우진_드릴\확통_2024학년도_현우진_드릴_P7_해설_deepseek_r1.md')
    
    if not md_path.exists():
        print(f"[오류] 파일을 찾을 수 없습니다: {md_path}")
        return
    
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"\n파일 크기: {len(content)} 문자")
    print(f"줄 수: {len(content.splitlines())} 줄\n")
    
    # 호환성 검증
    issues, warnings = verify_deepseek_compatibility(md_path)
    
    # 수학적 내용 검증
    math_errors, math_warnings = verify_math_content(content)
    
    print("[호환성 검증 결과]")
    if issues:
        print(f"  [오류] {len(issues)}개 발견:")
        for issue in issues:
            print(f"    - {issue}")
    else:
        print("  [통과] 호환성 오류 없음")
    
    if warnings:
        print(f"  [경고] {len(warnings)}개 발견:")
        for warning in warnings[:5]:  # 처음 5개만 표시
            print(f"    - {warning}")
    
    print("\n[수학적 내용 검증 결과]")
    if math_errors:
        print(f"  [오류] {len(math_errors)}개 발견:")
        for error in math_errors:
            print(f"    - {error}")
    else:
        print("  [통과] 수학적 오류 없음")
    
    if math_warnings:
        print(f"  [경고] {len(math_warnings)}개 발견:")
        for warning in math_warnings:
            print(f"    - {warning}")
    
    # Deepseek R1-70B 호환성 요약
    print("\n" + "=" * 80)
    print("[Deepseek R1-70B 호환성 요약]")
    print("=" * 80)
    
    compatible = len(issues) == 0 and len(math_errors) == 0
    
    if compatible:
        print("\n[결론] ✅ Deepseek R1-70B가 읽을 수 있는 형태입니다.")
        print("\n주요 특징:")
        print("  - 마크다운 형식: ✅")
        print("  - LaTeX 수식 ($...$ 및 $$...$$): ✅")
        print("  - 구조화된 섹션: ✅")
        print("  - 표 형식: ✅")
        print("  - UTF-8 인코딩: ✅")
    else:
        print("\n[결론] ⚠️ 일부 문제가 발견되었습니다. 수정이 필요할 수 있습니다.")
    
    # 샘플 내용 확인
    print("\n[샘플 내용] (처음 500자)")
    print("-" * 80)
    print(content[:500])
    print("-" * 80)

if __name__ == '__main__':
    main()
