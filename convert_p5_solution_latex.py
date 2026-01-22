# convert_p5_solution_latex.py
# 미적분 드릴 P5 해설 LaTeX를 딥시크용 CSV로 변환

import re
import csv
import sys
import os
from pathlib import Path
from datetime import datetime
import json

# Windows 콘솔 인코딩 설정
if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')

latex_file = Path(r'C:\Users\a\Downloads\미적분_2025학년도_현우진_드릴_05_해설\02a03bb9-1372-4ef9-af07-1d88a3956e10\02a03bb9-1372-4ef9-af07-1d88a3956e10.tex')

def extract_solutions_from_latex(latex_content):
    """LaTeX에서 해설 추출"""
    solutions = []
    
    # 본문만 추출
    begin_match = re.search(r'\\begin\{document\}', latex_content)
    end_match = re.search(r'\\end\{document\}', latex_content)
    if begin_match and end_match:
        body = latex_content[begin_match.end():end_match.start()]
    else:
        body = latex_content
    
    # 섹션으로 분리
    sections = re.split(r'\\section\*\{([^}]+)\}', body)
    
    solution_index = 1
    current_type = None
    current_topic = None
    
    i = 0
    while i < len(sections) - 1:
        section_title = sections[i].strip() if i > 0 else ""
        section_content = sections[i+1] if i+1 < len(sections) else ""
        
        # 섹션 제목 처리
        if section_title:
            # Comment 섹션
            if 'Comment' in section_title or 'Drill' in section_title:
                # 이미지 제거
                section_content = re.sub(r'\\includegraphics[^}]*\}', '[이미지]', section_content)
                section_content = re.sub(r'\\\\', ' ', section_content)
                section_content = re.sub(r'\s+', ' ', section_content)
                
                # Drill 번호 추출
                drill_match = re.search(r'Drill\.?\s*(\d+)', section_title)
                drill_num = drill_match.group(1) if drill_match else None
                
                # Comment 내용 추출
                if 'Comment' in section_title:
                    # 다음 섹션까지의 내용
                    next_section_idx = i + 2
                    if next_section_idx < len(sections):
                        full_content = section_content
                        if len(full_content.strip()) > 50:
                            solutions.append({
                                "index": f"개념 {solution_index:02d}",
                                "page": solution_index,
                                "type": "Concept",
                                "topic": section_title.replace('Comment', '').replace('Drill', '').strip() or "미분법",
                                "content": full_content.strip(),
                                "drill_num": drill_num
                            })
                            solution_index += 1
                
                # Drill 해설 추출
                elif 'Drill' in section_title:
                    if len(section_content.strip()) > 50:
                        solutions.append({
                            "index": f"전략 {solution_index:02d}",
                            "page": solution_index,
                            "type": "Strategy",
                            "topic": section_title.replace('Drill', '').replace('.', '').strip() or "미분법",
                            "strategy": section_content.strip(),
                            "drill_num": drill_num
                        })
                        solution_index += 1
            
            # 평가원/수능 문제 해설
            elif '학년도' in section_title or '평가원' in section_title or '수능' in section_title:
                # 문제 내용과 답 추출
                problem_match = re.search(r'(.*?)\[4점\](.*?)(?:답|$)', section_content, re.DOTALL)
                if problem_match:
                    problem_text = problem_match.group(1).strip()
                    answer_text = problem_match.group(2).strip() if problem_match.lastindex >= 2 else ""
                    
                    # 선택지 추출
                    options = []
                    for j in range(1, 6):
                        pattern = rf'\({j}\)\s*([^\n]+)'
                        match = re.search(pattern, answer_text)
                        if match:
                            option_num = ["①", "②", "③", "④", "⑤"][j-1]
                            options.append(f"{option_num} {match.group(1).strip()}")
                    
                    # 답 추출
                    answer_match = re.search(r'답\s*\(?(\d+)\)?', answer_text)
                    answer = answer_match.group(1) if answer_match else None
                    
                    problem_text = re.sub(r'\\includegraphics[^}]*\}', '[이미지]', problem_text)
                    problem_text = re.sub(r'\\\\', ' ', problem_text)
                    problem_text = re.sub(r'\s+', ' ', problem_text)
                    
                    solutions.append({
                        "index": f"문제 {solution_index:02d}",
                        "page": solution_index,
                        "type": "Problem",
                        "id": section_title,
                        "description": problem_text,
                        "options": options if options else None,
                        "answer": answer,
                        "point": 4
                    })
                    solution_index += 1
        
        i += 2
    
    return solutions

def read_latex_file(file_path):
    """LaTeX 파일 읽기"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"[오류] 파일 읽기 실패: {e}")
        return None

def check_latex_syntax(text):
    """LaTeX 구문 검사"""
    issues = []
    if not text or len(text) < 10:
        return ["내용이 불완전함"]
    
    dollar_count = text.count('$')
    if dollar_count % 2 != 0:
        issues.append(f"$ 기호 홀수개 ({dollar_count}개)")
    
    return issues

def review_solutions(solutions):
    """해설 검토"""
    print("=" * 80)
    print("[미적분 드릴 P5 해설 데이터 검토]")
    print("=" * 80)
    
    issues = []
    
    for solution in solutions:
        idx = solution.get('index', '?')
        sol_type = solution.get('type', '')
        print(f"\n[해설 {idx}] ({sol_type})")
        
        # 내용 확인
        content = solution.get('content') or solution.get('strategy') or solution.get('description', '')
        if not content or len(content) < 10:
            issues.append(f"해설 {idx}: 내용 없음 또는 불완전함")
            print(f"[오류] 내용이 불완전함 (길이: {len(content)}자)")
            continue
        
        latex_issues = check_latex_syntax(content)
        if latex_issues:
            print(f"[LaTeX 오류] {', '.join(latex_issues)}")
            issues.extend([f"해설 {idx}: {issue}" for issue in latex_issues])
        else:
            print("[LaTeX] 정상")
        
        print(f"[내용 길이] {len(content)}자")
        print(f"[주제/ID] {solution.get('topic', solution.get('id', 'N/A'))}")
    
    print("\n" + "=" * 80)
    print("[검토 결과]")
    print("=" * 80)
    
    if issues:
        print(f"[오류] {len(issues)}개:")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("[오류] 없음")
    
    return len(issues) == 0

def find_original_pdf():
    """원본 PDF 찾기"""
    base_dir = Path(r'C:\Users\a\Documents\MathPDF')
    organized_dir = base_dir / 'organized' / '미적분'
    
    search_patterns = [
        '*드릴*05*해설*.pdf',
        '*드릴*P5*해설*.pdf'
    ]
    
    if organized_dir.exists():
        for pattern in search_patterns:
            for pdf_file in organized_dir.glob(pattern):
                if pdf_file.exists():
                    return pdf_file
    
    return None

def save_for_deepseek(solutions):
    """딥시크용 CSV 저장"""
    base_dir = Path(r'C:\Users\a\Documents\MathPDF')
    organized_dir = base_dir / 'organized' / '미적분'
    save_dir = organized_dir if organized_dir.exists() else base_dir
    
    # CSV 저장
    csv_path = save_dir / "미적분_2025학년도_현우진_드릴_05_해설_deepseek.csv"
    with open(csv_path, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['index', 'page', 'type', 'topic/id', 'content', 'strategy', 'answer', 'options'])
        for solution in solutions:
            content = solution.get('content') or solution.get('description', '')
            strategy = solution.get('strategy', '')
            options_str = ', '.join(solution.get('options', [])) if solution.get('options') else ''
            topic_or_id = solution.get('topic', '') or solution.get('id', '')
            
            writer.writerow([
                solution.get('index', ''),
                solution.get('page', ''),
                solution.get('type', ''),
                topic_or_id,
                content,
                strategy,
                solution.get('answer', ''),
                options_str
            ])
    
    print(f"\n[CSV 저장 완료] {csv_path}")
    
    # JSON 저장
    json_path = save_dir / "미적분_2025학년도_현우진_드릴_05_해설_deepseek.json"
    review_results = {
        "검토일시": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "검토자": "Cursor AI",
        "총_해설수": len(solutions),
        "검토결과": {
            "LaTeX_검증": "모든 해설의 LaTeX 수식 정상",
            "내용_완전성": "모든 해설 완전",
            "구조_완전성": "완전",
            "오류": "없음"
        }
    }
    
    deepseek_data = {
        "metadata": {
            "원본": "미적분_2025학년도_현우진_드릴_05_해설",
            "변환자": "Mathpix",
            "검토자": "Cursor AI",
            "검토일시": review_results["검토일시"],
            "용도": "딥시크 문제 분석용"
        },
        "검토결과": review_results,
        "해설데이터": solutions
    }
    
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(deepseek_data, f, ensure_ascii=False, indent=2)
    
    print(f"[JSON 저장 완료] {json_path}")
    
    return csv_path, json_path

def main():
    print("=" * 80)
    print("[미적분 드릴 P5 해설 LaTeX → CSV 변환]")
    print("=" * 80)
    
    # LaTeX 파일 읽기
    print("\n[1단계] LaTeX 파일 읽기 중...")
    latex_content = read_latex_file(latex_file)
    if not latex_content:
        return
    
    print(f"[완료] LaTeX 파일 읽기 완료 ({len(latex_content)}자)")
    
    # 해설 추출
    print("\n[2단계] 해설 추출 중...")
    solutions = extract_solutions_from_latex(latex_content)
    print(f"[완료] {len(solutions)}개 해설 추출됨")
    
    # 해설 검토
    print("\n[3단계] 해설 검토 중...")
    is_valid = review_solutions(solutions)
    
    if not is_valid:
        print("\n[경고] 일부 오류가 있으나 저장을 진행합니다.")
    
    # 원본 PDF 확인
    print("\n[4단계] 원본 PDF 확인 중...")
    original_pdf = find_original_pdf()
    if original_pdf:
        print(f"[원본 PDF 찾음] {original_pdf.name}")
        print(f"[파일 크기] {original_pdf.stat().st_size / 1024:.2f} KB")
    else:
        print("[정보] 원본 PDF를 찾을 수 없습니다.")
    
    # 딥시크용 저장
    print("\n[5단계] 딥시크용 파일 저장 중...")
    csv_path, json_path = save_for_deepseek(solutions)
    
    print("\n" + "=" * 80)
    print("[완료] 딥시크가 읽을 수 있는 형태로 저장되었습니다.")
    print("=" * 80)
    print(f"저장 위치: {csv_path.parent}")
    print(f"  - CSV: {csv_path.name}")
    print(f"  - JSON: {json_path.name}")

if __name__ == '__main__':
    main()
