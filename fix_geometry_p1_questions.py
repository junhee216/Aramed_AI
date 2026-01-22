# fix_geometry_p1_questions.py
# 기하 P1 문제에서 이전 문제의 선택지 제거

import json
from pathlib import Path

def fix_questions(problems):
    """문제 본문에서 이전 문제의 선택지 제거"""
    fixed_problems = []
    
    for problem in problems:
        question = problem.get('question', '')
        
        # 이전 문제의 선택지 패턴 제거
        # (1) $...$ (2) $...$ 형식
        patterns_to_remove = [
            r'\(1\)\s*\$[^$]+\$\s*\(2\)\s*\$[^$]+\$\s*\(3\)\s*\$[^$]+\$\s*\(4\)\s*\$[^$]+\$\s*\(5\)\s*\$[^$]+\$',
            r'\(1\)\s*[^원]+?\s*\(2\)\s*[^원]+?\s*\(3\)\s*[^원]+?\s*\(4\)\s*[^원]+?\s*\(5\)\s*[^원]+?',
        ]
        
        for pattern in patterns_to_remove:
            question = re.sub(pattern, '', question)
        
        # 더 간단한 방법: "원" 또는 "초점" 또는 "포물선"으로 시작하는 부분만 남기기
        # 문제는 보통 "원", "초점", "포물선", "타원" 등으로 시작
        question_lines = question.split()
        start_idx = 0
        for i, word in enumerate(question_lines):
            if any(keyword in word for keyword in ['원', '초점', '포물선', '타원', '두', '초점이']):
                start_idx = i
                break
        
        if start_idx > 0:
            question = ' '.join(question_lines[start_idx:])
        
        # 공백 정리
        question = re.sub(r'\s+', ' ', question).strip()
        
        fixed_problems.append({
            **problem,
            'question': question
        })
    
    return fixed_problems

import re

def main():
    json_path = Path(r'C:\Users\a\Documents\MathPDF\organized\현우진\기하_2024학년도_현우진_드릴\기하_2024학년도_현우진_드릴_P1_문제_deepseek.json')
    
    with open(json_path, 'r', encoding='utf-8') as f:
        problems = json.load(f)
    
    print(f"총 {len(problems)}개 문제 수정 중...\n")
    
    fixed_problems = []
    for problem in problems:
        question = problem.get('question', '')
        original_question = question
        
        # 이전 문제의 선택지 제거 (더 정확한 패턴)
        # (1) $...$ (2) $...$ (3) $...$ (4) $...$ (5) $...$ 형식
        question = re.sub(r'\(1\)\s*\$[^$]+\$\s*\(2\)\s*\$[^$]+\$\s*\(3\)\s*\$[^$]+\$\s*\(4\)\s*\$[^$]+\$\s*\(5\)\s*\$[^$]+\$', '', question)
        
        # (1) 숫자 (2) 숫자 형식
        question = re.sub(r'\(1\)\s*[0-9+\-√\s]+\s*\(2\)\s*[0-9+\-√\s]+\s*\(3\)\s*[0-9+\-√\s]+\s*\(4\)\s*[0-9+\-√\s]+\s*\(5\)\s*[0-9+\-√\s]+', '', question)
        
        # 문제 시작 키워드 찾기
        keywords = ['원', '초점', '포물선', '타원', '두 점', '두 초점', '두 포물선']
        for keyword in keywords:
            idx = question.find(keyword)
            if idx > 0 and idx < 200:  # 문제 시작 부분에 있어야 함
                question = question[idx:]
                break
        
        # 공백 정리
        question = re.sub(r'\s+', ' ', question).strip()
        
        if question != original_question:
            print(f"문제 {problem['index']}: 수정됨")
            print(f"  이전: {original_question[:80]}...")
            print(f"  이후: {question[:80]}...\n")
        
        fixed_problems.append({
            **problem,
            'question': question
        })
    
    # 저장
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(fixed_problems, f, ensure_ascii=False, indent=2)
    
    print("수정 완료!")

if __name__ == '__main__':
    main()
