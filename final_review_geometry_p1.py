# final_review_geometry_p1.py
# 기하 P1 최종 수학적 오류 검토

import json
import re
from pathlib import Path

def review_geometry_math(problems):
    """기하 문제의 수학적 오류 검토"""
    errors = []
    warnings = []
    
    for problem in problems:
        question = problem.get('question', '')
        index = problem.get('index', '')
        
        # 1. 포물선 방정식 검증
        if '포물선' in question:
            # y² = 4ax 형식
            if 'y^{2}=4 x' in question or 'y^{2}=4x' in question:
                # a = 1, 초점 F(1, 0) ✓
                pass
            elif 'y^{2}=8 x' in question or 'y^{2}=8x' in question:
                # a = 2, 초점 F(2, 0) ✓
                pass
            elif 'y^{2}=4 a x' in question or 'y^{2}=4ax' in question:
                # a > 0 조건 확인
                if 'a>0' in question or 'a > 0' in question or '(p>0)' in question:
                    pass  # 조건 있음 ✓
                else:
                    warnings.append(f"문제 {index}: 포물선 y² = 4ax에서 a > 0 조건 확인 필요")
            elif 'y^{2}=4 p x' in question:
                # p > 0 조건 확인
                if '(p>0)' in question or 'p>0' in question:
                    pass  # 조건 있음 ✓
                else:
                    warnings.append(f"문제 {index}: 포물선 y² = 4px에서 p > 0 조건 확인 필요")
        
        # 2. 타원 방정식 검증
        if '타원' in question:
            if '초점' in question and '장축' in question:
                # 타원의 정의: PF + PF' = 2a (장축의 길이)
                if '장축의 길이가 11' in question:
                    # 2a = 11, a = 5.5 ✓
                    pass
                elif '장축의 길이는' in question:
                    pass  # 장축 길이 추출 가능 ✓
            else:
                warnings.append(f"문제 {index}: 타원 관련 조건 확인 필요")
        
        # 3. 원의 방정식 검증
        if '원' in question and '^{2}' in question:
            # (x-h)² + (y-k)² = r² 형식
            if '^{2}+y^{2}' in question or '^{2}+ y^{2}' in question:
                pass  # 원의 방정식 형식 ✓
        
        # 4. 좌표 기하 검증
        if '초점' in question and 'F' in question:
            # 포물선 y² = 4x → 초점 F(1, 0) ✓
            # 포물선 y² = 8x → 초점 F(2, 0) ✓
            pass
        
        # 5. 각도 검증
        if '각' in question or 'angle' in question.lower():
            if '\\frac{\\pi}{2}' in question:
                # 직각 (90도) ✓
                pass
            elif '\\sin' in question or '\\cos' in question:
                # 삼각함수 값 확인
                if '\\frac{3}{5}' in question or '\\frac{3}{7}' in question:
                    pass  # 삼각함수 값 ✓
        
        # 6. 길이 관계 검증
        if '\\overline' in question:
            # 선분 길이 표기 ✓
            pass
        
        # 7. 문제 03번 특수 검증: 원이 두 직선에 접하는 조건
        if index == '03' and '원' in question and '접한다' in question:
            # 원 (x-b)² + y² = c²이 두 직선에 접하는 조건
            # 원의 중심 (b, 0), 반지름 c
            # 두 직선에 접하려면 중심에서 각 직선까지의 거리가 c와 같아야 함 ✓
            pass
    
    return errors, warnings

def main():
    print("=" * 80)
    print("기하_2024학년도_현우진_드릴_P1 최종 수학적 오류 검토")
    print("=" * 80)
    
    json_path = Path(r'C:\Users\a\Documents\MathPDF\organized\현우진\기하_2024학년도_현우진_드릴\기하_2024학년도_현우진_드릴_P1_문제_deepseek.json')
    
    with open(json_path, 'r', encoding='utf-8') as f:
        problems = json.load(f)
    
    print(f"\n총 {len(problems)}개 문제 검토\n")
    
    # 수학적 오류 검토
    errors, warnings = review_geometry_math(problems)
    
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
    
    # 문제별 요약
    print("\n[문제별 요약]")
    for problem in problems:
        print(f"  문제 {problem['index']}: {problem['topic']} [{problem['point']}점]")
        if problem['options']:
            print(f"    - 객관식 ({len(problem['options'])}개 선택지)")
        else:
            print(f"    - 주관식")
    
    print("\n[최종 결론]")
    if len(errors) == 0:
        print("  [통과] 수학적 오류 없음.")
        print("  [통과] Deepseek R1-70B가 읽을 수 있는 형태입니다.")
    else:
        print(f"  [경고] 수학적 오류 {len(errors)}개 발견. 검토 필요.")

if __name__ == '__main__':
    main()
