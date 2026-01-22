# generate_csat_problem.py
# 수능 경향 기반 문제 생성 시스템

import json
from pathlib import Path

class CSATProblemGenerator:
    """수능 경향 기반 문제 생성기"""
    
    def __init__(self):
        self.output_dir = Path(r'C:\Users\a\Documents\Aramed_AI\output')
        self.guideline_path = Path(r'C:\Users\a\Documents\Aramed_AI\problem_generation_guideline.md')
        self.trends_path = self.output_dir / 'trends_analysis.json'
        
        # 경향성 데이터 로드
        self.trends = self.load_trends()
        
    def load_trends(self):
        """경향성 데이터 로드"""
        if self.trends_path.exists():
            with open(self.trends_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def get_problem_specs(self, problem_number: int, subject: str = None):
        """문항번호에 따른 문제 생성 사양 반환"""
        
        if problem_number <= 15:
            return {
                'target_answer_rate': 77.0,
                'difficulty_grade': '2-3등급용',
                'solving_time': '2-3분',
                'problem_format': '선택형(계산)',
                'trap_type': '없음',
                'intent': '기본개념확인',
                'concept_type': '단일개념',
                'calculation_complexity': '간단계산',
                'solving_steps': '2-3단계',
                'score': 2
            }
        elif problem_number <= 22:
            return {
                'target_answer_rate': 55.3,
                'difficulty_grade': '4-6등급용',
                'solving_time': '3-5분',
                'problem_format': '선택형(계산)',
                'trap_type': '조건누락형',
                'intent': '계산능력측정',
                'concept_type': '융합개념',
                'calculation_complexity': '복잡계산',
                'solving_steps': '3-5단계',
                'score': 3
            }
        elif problem_number <= 28:
            return {
                'target_answer_rate': 38.5,
                'difficulty_grade': '변별용',
                'solving_time': '5-7분',
                'problem_format': '선택형(추론)',
                'trap_type': '복합함정형',
                'intent': '변별력확보',
                'concept_type': '복합개념',
                'calculation_complexity': '매우복잡',
                'solving_steps': '5-7단계',
                'score': 4
            }
        else:  # 29-30번
            return {
                'target_answer_rate': 15.2,
                'difficulty_grade': '킬러용',
                'solving_time': '8-10분',
                'problem_format': '선택형(추론)',
                'trap_type': '복합함정형',
                'intent': '창의력평가',
                'concept_type': '복합개념',
                'calculation_complexity': '매우복잡',
                'solving_steps': '7단계 이상',
                'score': 4
            }
    
    def generate_prompt(self, problem_number: int, subject: str, minor_unit: str = None):
        """문제 생성 프롬프트 생성"""
        
        specs = self.get_problem_specs(problem_number, subject)
        
        prompt = f"""당신은 수능 수학 문제 출제 전문가입니다.
최근 5년(2022-2026) 수능 경향을 분석한 결과를 바탕으로 다음 조건에 맞는 수능 수학 문제를 생성하세요.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[생성 조건]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. 문항번호: {problem_number}번
2. 목표 정답률: {specs['target_answer_rate']:.1f}%
3. 과목: {subject}
4. 중단원: {minor_unit if minor_unit else '해당 과목의 주요 중단원'}
5. 배점: {specs['score']}점
6. 문제 형식: {specs['problem_format']}
7. 풀이 시간: {specs['solving_time']}
8. 함정 유형: {specs['trap_type']}
9. 출제 의도: {specs['intent']}
10. 핵심개념: {specs['concept_type']}
11. 계산복잡도: {specs['calculation_complexity']}
12. 풀이단계수: {specs['solving_steps']}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[경향성 기준 (2022-2026, 299개 문제 분석)]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

• 평균 정답률: 58-61% (연도별)
• 킬러 문항 비율: 17-20%
• 문제 형식: 선택형(계산) 68.9%, 단답형 31.1%
• 함정 유형: 없음 79.9%, 복합함정형 9.4%
• 출제 의도: 계산능력측정 44.5%, 기본개념확인 26.1%

문항번호별 경향:
• 1-15번: 평균 정답률 77.0%, 기본 개념 확인
• 16-22번: 평균 정답률 55.3%, 계산 능력 측정
• 23-28번: 평균 정답률 38.5%, 개념 이해 평가
• 29-30번: 평균 정답률 15.2%, 창의력 평가

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[출력 형식]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

다음 형식으로 문제를 생성하세요:

[문제]
[문제 지문]

[보기] (5지선다형인 경우)
① [보기1]
② [보기2]
③ [보기3]
④ [보기4]
⑤ [보기5]

[정답]
[정답 번호]

[풀이]
[단계별 풀이 과정]

[출제 의도]
{specs['intent']} - {specs['intent']}에 맞게 출제

[검증 체크리스트]
- 목표 정답률 {specs['target_answer_rate']:.1f}%에 부합하는가?
- 풀이 시간 {specs['solving_time']} 내에 해결 가능한가?
- 함정 유형이 {specs['trap_type']}인가?
- {specs['concept_type']} 개념을 사용하는가?

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[중요 원칙]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. 정확성 최우선: 추측 금지, 확실한 것만
2. 일관성 유지: 동일 기준으로 평가
3. 근거 제시: 판단의 이유 명시
4. 통계적 사고: 정량화 가능한 것은 수치로
5. 트렌드 인식: 최근 5년 출제 경향 반영

문제를 생성하세요."""

        return prompt
    
    def save_prompt(self, prompt: str, filename: str = 'csat_problem_generation_prompt.txt'):
        """프롬프트를 파일로 저장"""
        output_path = self.output_dir / filename
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(prompt)
        print(f"[저장] 문제 생성 프롬프트: {output_path}")
        return output_path

def main():
    """메인 함수"""
    generator = CSATProblemGenerator()
    
    print("="*70)
    print("[수능 경향 기반 문제 생성 시스템]")
    print("="*70)
    print("\n사용 예시:")
    print("  generator = CSATProblemGenerator()")
    print("  prompt = generator.generate_prompt(problem_number=25, subject='미적분', minor_unit='미분법')")
    print("  generator.save_prompt(prompt)")
    print("\n또는 직접 프롬프트를 생성하려면:")
    print("  python generate_csat_problem.py --number 25 --subject 미적분 --unit 미분법")
    
    # 예시 프롬프트 생성
    print("\n[예시] 25번 미적분 문제 생성 프롬프트 생성 중...")
    prompt = generator.generate_prompt(25, '미적분', '미분법')
    generator.save_prompt(prompt, 'example_csat_problem_prompt.txt')
    
    print("\n[완료] 문제 생성 준비 완료!")
    print("\n다음 명령으로 문제를 생성하세요:")
    print("  '다음 조건에 맞는 수능 수학 문제를 생성해주세요:'")
    print("  그리고 위의 프롬프트를 참고하세요.")

if __name__ == '__main__':
    main()
