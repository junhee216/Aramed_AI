# analyze_trends.py
# 수능 수학 문제 경향성 분석

import csv
import json
from pathlib import Path
from collections import Counter, defaultdict
import statistics

def analyze_trends():
    """수능 경향성 분석"""
    
    output_dir = Path(r'C:\Users\a\Documents\Aramed_AI\output')
    # 기본 분석 파일 사용
    csv_path = output_dir / 'csat_meta_analysis.csv'
    
    if not csv_path.exists():
        csv_path = output_dir / 'csat_deep_analysis.csv'
        if not csv_path.exists():
            print(f"[오류] 분석 결과 파일을 찾을 수 없습니다")
            return None
    
    results = []
    with open(csv_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get('출제년도'):  # 빈 행 제외
                results.append(row)
    
    if not results:
        print("[경고] 분석할 데이터가 없습니다.")
        return None
    
    print("="*70)
    print("[수능 수학 문제 경향성 분석 (2022-2026)]")
    print("="*70)
    print(f"\n총 분석 문제 수: {len(results)}개\n")
    
    trends = {}
    
    # 1. 연도별 출제 경향
    print("[1] 연도별 출제 경향")
    print("-"*70)
    year_data = defaultdict(list)
    for r in results:
        year = r.get('출제년도', '미상')
        if year != '미상':
            year_data[year].append(r)
    
    for year in sorted(year_data.keys()):
        problems = year_data[year]
        print(f"\n{year}년: {len(problems)}개 문제")
        
        # 평균 정답률
        rates = []
        for p in problems:
            try:
                rate = float(p.get('공식정답률', '0').replace('%', ''))
                if rate > 0:
                    rates.append(rate)
            except:
                pass
        
        if rates:
            avg_rate = statistics.mean(rates)
            print(f"  평균 정답률: {avg_rate:.1f}%")
        
        # 킬러 비율
        killer_count = sum(1 for p in problems if '킬러' in p.get('킬러여부판정', ''))
        print(f"  킬러 문항 비율: {killer_count/len(problems)*100:.1f}% ({killer_count}개)")
    
    trends['yearly'] = {year: len(problems) for year, problems in year_data.items()}
    
    # 2. 과목별 출제 경향
    print("\n[2] 과목별 출제 경향")
    print("-"*70)
    subject_data = defaultdict(list)
    for r in results:
        subject = r.get('과목구분', '미상')
        if subject != '미상':
            subject_data[subject].append(r)
    
    for subject in sorted(subject_data.keys()):
        problems = subject_data[subject]
        print(f"\n{subject}: {len(problems)}개 ({len(problems)/len(results)*100:.1f}%)")
        
        # 평균 정답률
        rates = []
        for p in problems:
            try:
                rate = float(p.get('공식정답률', '0').replace('%', ''))
                if rate > 0:
                    rates.append(rate)
            except:
                pass
        
        if rates:
            avg_rate = statistics.mean(rates)
            print(f"  평균 정답률: {avg_rate:.1f}%")
        
        # 주요 중단원
        minor_units = [p.get('중단원', '') for p in problems if p.get('중단원') != '미상']
        if minor_units:
            top_unit = Counter(minor_units).most_common(1)[0]
            print(f"  주요 중단원: {top_unit[0]} ({top_unit[1]}개)")
    
    trends['by_subject'] = {s: len(p) for s, p in subject_data.items()}
    
    # 3. 난이도 경향
    print("\n[3] 난이도 경향 분석")
    print("-"*70)
    difficulty_dist = Counter(r.get('난이도등급', '') for r in results)
    for diff in ['1등급컷용', '2-3등급용', '4-6등급용', '변별용', '킬러용']:
        count = difficulty_dist.get(diff, 0)
        if count > 0:
            print(f"  {diff}: {count}개 ({count/len(results)*100:.1f}%)")
    
    trends['difficulty'] = dict(difficulty_dist)
    
    # 4. 문제 형식 경향
    print("\n[4] 문제 형식 경향")
    print("-"*70)
    format_dist = Counter(r.get('문제형식', '') for r in results)
    for fmt, count in format_dist.most_common():
        print(f"  {fmt}: {count}개 ({count/len(results)*100:.1f}%)")
    
    trends['format'] = dict(format_dist)
    
    # 5. 중단원별 출제 빈도 (상위 15개)
    print("\n[5] 중단원별 출제 빈도 (상위 15개)")
    print("-"*70)
    minor_units = [r.get('중단원', '') for r in results if r.get('중단원') != '미상']
    unit_count = Counter(minor_units)
    for unit, count in unit_count.most_common(15):
        print(f"  {unit}: {count}개 ({count/len(results)*100:.1f}%)")
    
    trends['top_units'] = dict(unit_count.most_common(15))
    
    # 6. 함정 유형 경향
    print("\n[6] 함정 유형 경향")
    print("-"*70)
    trap_dist = Counter(r.get('함정유형', '') for r in results)
    for trap, count in trap_dist.most_common():
        print(f"  {trap}: {count}개 ({count/len(results)*100:.1f}%)")
    
    trends['trap_types'] = dict(trap_dist)
    
    # 7. 출제 의도 경향
    print("\n[7] 출제 의도 경향")
    print("-"*70)
    intent_dist = Counter(r.get('출제의도', '') for r in results)
    for intent, count in intent_dist.most_common():
        print(f"  {intent}: {count}개 ({count/len(results)*100:.1f}%)")
    
    trends['intent'] = dict(intent_dist)
    
    # 8. 최근 3년 경향 (2024-2026)
    print("\n[8] 최근 3년 경향 (2024-2026)")
    print("-"*70)
    recent_years = ['2024', '2025', '2026']
    recent_problems = [r for r in results if r.get('출제년도') in recent_years]
    
    if recent_problems:
        print(f"최근 3년 총 문제 수: {len(recent_problems)}개\n")
        
        # 평균 정답률
        recent_rates = []
        for p in recent_problems:
            try:
                rate = float(p.get('공식정답률', '0').replace('%', ''))
                if rate > 0:
                    recent_rates.append(rate)
            except:
                pass
        
        if recent_rates:
            print(f"평균 정답률: {statistics.mean(recent_rates):.1f}%")
        
        # 킬러 비율
        recent_killer = sum(1 for p in recent_problems if '킬러' in p.get('킬러여부판정', ''))
        print(f"킬러 문항 비율: {recent_killer/len(recent_problems)*100:.1f}%")
        
        # 주요 중단원
        recent_units = [p.get('중단원', '') for p in recent_problems if p.get('중단원') != '미상']
        if recent_units:
            top_recent = Counter(recent_units).most_common(5)
            print(f"\n주요 중단원 (최근 3년):")
            for unit, count in top_recent:
                print(f"  {unit}: {count}개")
    
    trends['recent_3years'] = {
        'total': len(recent_problems),
        'avg_answer_rate': statistics.mean(recent_rates) if recent_rates else 0,
        'killer_ratio': recent_killer/len(recent_problems)*100 if recent_problems else 0
    }
    
    # 9. 문항번호별 경향
    print("\n[9] 문항번호별 경향")
    print("-"*70)
    problem_ranges = {
        '1-15번 (기본)': (1, 15),
        '16-22번 (중급)': (16, 22),
        '23-28번 (고급)': (23, 28),
        '29-30번 (킬러)': (29, 30)
    }
    
    for range_name, (start, end) in problem_ranges.items():
        range_problems = [r for r in results 
                         if start <= int(r.get('문항번호', 0)) <= end]
        if range_problems:
            avg_rate = statistics.mean([
                float(p.get('공식정답률', '0').replace('%', ''))
                for p in range_problems
                if p.get('공식정답률', '0').replace('%', '').replace('.', '').isdigit()
            ]) if any(p.get('공식정답률', '0').replace('%', '').replace('.', '').isdigit() 
                     for p in range_problems) else 0
            print(f"  {range_name}: {len(range_problems)}개, 평균 정답률 {avg_rate:.1f}%")
    
    print("\n" + "="*70)
    print("[경향성 분석 완료]")
    print("="*70)
    
    # 결과 저장
    trends_path = output_dir / 'trends_analysis.json'
    with open(trends_path, 'w', encoding='utf-8') as f:
        json.dump(trends, f, ensure_ascii=False, indent=2)
    
    print(f"\n경향성 분석 결과 저장: {trends_path}")
    
    return trends

if __name__ == '__main__':
    analyze_trends()
