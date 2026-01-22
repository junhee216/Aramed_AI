# generate_analysis_summary.py
# 수능 메타분석 결과 요약 리포트 생성

import csv
import json
from pathlib import Path
from collections import Counter, defaultdict

def generate_summary():
    """분석 결과 요약 리포트 생성"""
    
    output_dir = Path(r'C:\Users\a\Documents\Aramed_AI\output')
    csv_path = output_dir / 'csat_deep_analysis.csv'
    
    if not csv_path.exists():
        print(f"[오류] 분석 결과 파일을 찾을 수 없습니다: {csv_path}")
        return
    
    results = []
    with open(csv_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            results.append(row)
    
    print("="*70)
    print("[수능 수학 문제 메타분석 결과 요약]")
    print("="*70)
    print(f"\n총 분석 문제 수: {len(results)}개\n")
    
    # 1. 연도별 통계
    print("[1] 연도별 분포")
    print("-"*70)
    year_count = Counter(r['출제년도'] for r in results)
    for year in sorted(year_count.keys()):
        print(f"  {year}년: {year_count[year]}개")
    
    # 2. 과목별 통계
    print("\n[2] 과목별 분포")
    print("-"*70)
    subject_count = Counter(r['과목구분'] for r in results)
    for subject in sorted(subject_count.keys()):
        print(f"  {subject}: {subject_count[subject]}개")
    
    # 3. 난이도 등급별 통계
    print("\n[3] 난이도 등급별 분포")
    print("-"*70)
    difficulty_count = Counter(r['난이도등급'] for r in results)
    for diff in ['1등급컷용', '2-3등급용', '4-6등급용', '변별용', '킬러용']:
        if diff in difficulty_count:
            print(f"  {diff}: {difficulty_count[diff]}개 ({difficulty_count[diff]/len(results)*100:.1f}%)")
    
    # 4. 킬러 여부 통계
    print("\n[4] 킬러 여부 분포")
    print("-"*70)
    killer_count = Counter(r['킬러여부판정'] for r in results)
    for killer_type in ['일반문항', '준킬러', '킬러', '슈퍼킬러']:
        if killer_type in killer_count:
            print(f"  {killer_type}: {killer_count[killer_type]}개 ({killer_count[killer_type]/len(results)*100:.1f}%)")
    
    # 5. 평균 정답률
    print("\n[5] 평균 정답률 분석")
    print("-"*70)
    answer_rates = []
    for r in results:
        try:
            rate_str = r['공식정답률'].replace('%', '')
            rate = float(rate_str)
            answer_rates.append(rate)
        except:
            pass
    
    if answer_rates:
        print(f"  전체 평균: {sum(answer_rates)/len(answer_rates):.1f}%")
        print(f"  최고 정답률: {max(answer_rates):.1f}%")
        print(f"  최저 정답률: {min(answer_rates):.1f}%")
    
    # 6. 평균 풀이 시간
    print("\n[6] 평균 풀이 시간 분석")
    print("-"*70)
    solving_times = []
    for r in results:
        try:
            time_str = r['풀이소요시간'].replace('분', '')
            time = int(time_str)
            solving_times.append(time)
        except:
            pass
    
    if solving_times:
        print(f"  전체 평균: {sum(solving_times)/len(solving_times):.1f}분")
        print(f"  최대 시간: {max(solving_times)}분")
        print(f"  최소 시간: {min(solving_times)}분")
    
    # 7. 중단원별 분포
    print("\n[7] 중단원별 분포 (상위 10개)")
    print("-"*70)
    minor_unit_count = Counter(r['중단원'] for r in results if r['중단원'] != '미상')
    for unit, count in minor_unit_count.most_common(10):
        print(f"  {unit}: {count}개")
    
    # 8. 문제 형식별 분포
    print("\n[8] 문제 형식별 분포")
    print("-"*70)
    format_count = Counter(r['문제형식'] for r in results)
    for fmt, count in format_count.most_common():
        print(f"  {fmt}: {count}개 ({count/len(results)*100:.1f}%)")
    
    # 9. 함정 유형별 분포
    print("\n[9] 함정 유형별 분포")
    print("-"*70)
    trap_count = Counter(r['함정유형'] for r in results)
    for trap, count in trap_count.most_common():
        print(f"  {trap}: {count}개 ({count/len(results)*100:.1f}%)")
    
    # 10. 출제 의도별 분포
    print("\n[10] 출제 의도별 분포")
    print("-"*70)
    intent_count = Counter(r['출제의도'] for r in results)
    for intent, count in intent_count.most_common():
        print(f"  {intent}: {count}개 ({count/len(results)*100:.1f}%)")
    
    print("\n" + "="*70)
    print("[요약 완료]")
    print("="*70)
    print(f"\n상세 결과는 다음 파일에서 확인하세요:")
    print(f"  - CSV: {csv_path}")
    print(f"  - JSON: {output_dir / 'csat_deep_analysis.json'}")

if __name__ == '__main__':
    generate_summary()
