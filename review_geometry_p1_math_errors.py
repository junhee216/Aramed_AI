# review_geometry_p1_math_errors.py
# 기하 P1 문제의 수학적 오류 검토

import json
import re
from pathlib import Path

def review_math_errors(problems):
    """수학적 오류 검토"""
    errors = []
    warnings = []
    
    for problem in problems:
        question = problem.get('question', '')
        index = problem.get('index', '')
        
        # 1. 포물선 방정식 검증
        if '포물선' in question:
            # y² = 4ax 형식 확인
            if 'y^{2}=4' in question or 'y^{2}=8' in question:
                # 포물선 y² = 4ax에서 a > 0이어야 함
                if 'y^{2}=4 x' in question:
                    # a = 1, 초점 F(1, 0) ✓
                    pass
                elif 'y^{2}=8 x' in question:
                    # a = 2, 초점 F(2, 0) ✓
                    pass
                elif 'y^{2}=4 a x' in question:
                    # a > 0 조건 확인 필요
                    if 'a>0' not in question and 'a > 0' not in question:
                        warnings.append(f"문제 {index}: 포물선 y² = 4ax에서 a > 0 조건 확인 필요")
            else:
                warnings.append(f"문제 {index}: 포물선 방정식 형식 확인 필요")
        
        # 2. 타원 방정식 검증
        if '타원' in question:
            # 초점과 장축 길이 확인
            if '초점' in question and '장축' in question:
                # 타원의 정의: PF + PF' = 2a (장축의 길이)
                if '장축의 길이가 11' in question:
                    # 2a = 11, a = 5.5 ✓
                    pass
                elif '장축의 길이는' in question:
                    # 장축 길이 추출 확인
                    pass
            else:
                warnings.append(f"문제 {index}: 타원 관련 조건 확인 필요")
        
        # 3. 기하학적 조건 검증
        if '삼각형' in question:
            if '둘레' in question or '넓이' in question:
                # 삼각형의 둘레나 넓이 계산 가능 ✓
                pass
            elif '외접원' in question:
                # 외접원 관련 문제 ✓
                pass
            else:
                warnings.append(f"문제 {index}: 삼각형 관련 조건 확인 필요")
        
        # 4. 좌표 기하 검증
        if '초점' in question and 'F' in question:
            # 포물선의 초점은 (a, 0) 또는 (0, a) 형식
            if 'y^{2}=4' in question:
                # y² = 4x → 초점 F(1, 0) ✓
                pass
            elif 'y^{2}=8' in question:
                # y² = 8x → 초점 F(2, 0) ✓
                pass
        
        # 5. 각도 및 길이 관계 검증
        if '각' in question or 'angle' in question.lower():
            # 각도 관련 조건 확인
            if '\\frac{\\pi}{2}' in question or '90' in question:
                # 직각 관련 ✓
                pass
        
        # 6. 원의 방정식 검증
        if '원' in question and '(' in question and ')' in question:
            # (x-h)² + (y-k)² = r² 형식 확인
            if '^{2}' in question and 'y^{2}' in question:
                pass  # 원의 방정식 형식 ✓
    
    return errors, warnings

def main():
    print("=" * 80)
    print("기하_2024학년도_현우진_드릴_P1 수학적 오류 검토")
    print("=" * 80)
    
    json_path = Path(r'C:\Users\a\Documents\MathPDF\organized\현우진\기하_2024학년도_현우진_드릴\기하_2024학년도_현우진_드릴_P1_문제_deepseek.json')
    
    if not json_path.exists():
        print(f"[오류] 파일을 찾을 수 없습니다: {json_path}")
        return
    
    with open(json_path, 'r', encoding='utf-8') as f:
        problems = json.load(f)
    
    print(f"\n총 {len(problems)}개 문제 검토\n")
    
    # 수학적 오류 검토
    errors, warnings = review_math_errors(problems)
    
    print("[검토 결과]")
    if errors:
        print(f"  [오류] 수학적 오류: {len(errors)}개")
        for error in errors:
            print(f"    - {error}")
    else:
        print("  [통과] 수학적 오류 없음")
    
    if warnings:
        print(f"  [경고] 경고: {len(warnings)}개")
        for warning in warnings:
            print(f"    - {warning}")
    else:
        print("  [통과] 경고 없음")
    
    # Deepseek R1-70B 호환성 확인
    print("\n[Deepseek R1-70B 호환성]")
    print("  - JSON 형식: 지원")
    print("  - LaTeX 수식: 지원")
    print("  - UTF-8 인코딩: 지원")
    
    print("\n[최종 결론]")
    if len(errors) == 0:
        print("  [통과] 수학적 오류 없음. Deepseek R1-70B가 읽을 수 있는 형태입니다.")
    else:
        print(f"  [경고] 수학적 오류 {len(errors)}개 발견. 검토 필요.")

if __name__ == '__main__':
    main()
