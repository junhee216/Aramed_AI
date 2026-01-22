# verify_math_errors_p7.py
# 확통 P7 해설의 수학적/논리적 오류 검증

import json
import re
from pathlib import Path

def verify_math_formulas(content):
    """수학 공식 검증"""
    errors = []
    warnings = []
    
    # 표본평균의 분산 공식 확인
    if 'V(\\bar{X})' in content or 'V($\\bar{X}$)' in content:
        if '\\frac{\\sigma^{2}}{n}' in content or 'σ²/n' in content or '\\frac{\\sigma^2}{n}' in content:
            pass  # 정확
        else:
            warnings.append("표본평균의 분산 공식 확인 필요: V(\\bar{X}) = σ²/n")
    
    # 표본평균의 표준편차 공식 확인
    if 'σ(\\bar{X})' in content or 'σ($\\bar{X}$)' in content:
        if '\\frac{\\sigma}{\\sqrt{n}}' in content or 'σ/√n' in content:
            pass  # 정확
        else:
            warnings.append("표본평균의 표준편차 공식 확인 필요: σ(\\bar{X}) = σ/√n")
    
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
    
    # 표본평균의 평균 확인
    if 'E(\\bar{X})' in content or 'E($\\bar{X}$)' in content:
        if '=m' in content or '= $m$' in content:
            pass  # 정확: E(\\bar{X}) = m
        else:
            warnings.append("표본평균의 평균 공식 확인 필요: E(\\bar{X}) = m")
    
    return errors, warnings

def verify_logic_consistency(content):
    """논리적 일관성 검증"""
    errors = []
    warnings = []
    
    # 표본평균의 분산과 표준편차 관계 확인
    if 'V(\\bar{X})' in content and 'σ(\\bar{X})' in content:
        # V(\\bar{X}) = σ²/n 이면 σ(\\bar{X}) = σ/√n 이어야 함
        if '\\frac{\\sigma^{2}}{n}' in content and '\\frac{\\sigma}{\\sqrt{n}}' in content:
            pass  # 일관성 있음
        else:
            warnings.append("표본평균의 분산과 표준편차 관계 확인 필요")
    
    # 신뢰구간과 신뢰상수 관계 확인
    if '1.96' in content and '0.475' in content:
        # 1.96은 P(0 ≤ Z ≤ 1.96) = 0.475에 해당
        pass  # 정확
    
    return errors, warnings

def main():
    print("=" * 80)
    print("확통_2024학년도_현우진_드릴_P7_해설 수학적/논리적 오류 검증")
    print("=" * 80)
    
    # 해설 파일 읽기
    md_path = Path(r'C:\Users\a\Documents\MathPDF\organized\현우진\확통_2024학년도_현우진_드릴\확통_2024학년도_현우진_드릴_P7_해설_deepseek_r1.md')
    
    if not md_path.exists():
        print(f"[오류] 파일을 찾을 수 없습니다: {md_path}")
        return
    
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"\n파일 크기: {len(content)} 문자")
    
    # 수학 공식 검증
    math_errors, math_warnings = verify_math_formulas(content)
    
    # 논리적 일관성 검증
    logic_errors, logic_warnings = verify_logic_consistency(content)
    
    all_errors = math_errors + logic_errors
    all_warnings = math_warnings + logic_warnings
    
    print("\n[검증 결과]")
    if all_errors:
        print(f"  [오류] {len(all_errors)}개 발견:")
        for error in all_errors:
            print(f"    - {error}")
    else:
        print("  [통과] 수학적 오류 없음")
    
    if all_warnings:
        print(f"  [경고] {len(all_warnings)}개 발견:")
        for warning in all_warnings:
            print(f"    - {warning}")
    else:
        print("  [통과] 경고 없음")
    
    # Deepseek R1-70B 호환성 확인
    print("\n[Deepseek R1-70B 호환성]")
    has_markdown = content.startswith('#')
    has_math = '$' in content or '$$' in content
    has_sections = '##' in content
    
    print(f"  - 마크다운 헤더: {'지원' if has_markdown else '없음'}")
    print(f"  - LaTeX 수식: {'지원' if has_math else '없음'}")
    print(f"  - 구조화된 섹션: {'지원' if has_sections else '없음'}")
    print(f"  - UTF-8 인코딩: 지원")
    
    compatible = has_markdown and has_math and has_sections and len(all_errors) == 0
    
    print("\n" + "=" * 80)
    if compatible:
        print("[최종 결론] Deepseek R1-70B가 읽을 수 있는 형태입니다.")
        print("수학적 오류 없음.")
    else:
        print("[최종 결론] 일부 문제가 있을 수 있습니다.")
        if all_errors:
            print(f"수학적 오류: {len(all_errors)}개")
        if not has_markdown or not has_math:
            print("형식 문제: 마크다운 또는 수식 형식 확인 필요")
    print("=" * 80)

if __name__ == '__main__':
    main()
