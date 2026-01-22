# quick_workflow.py
# 빠른 워크플로우 실행 스크립트

"""
사용법:
python quick_workflow.py --problem "수2_2025학년도_현우진_드릴_P4_문제" --latex "LaTeX 내용"
python quick_workflow.py --full --problem-file "문제파일.tex" --solution-file "해설파일.tex"
"""

import argparse
import sys
from pathlib import Path
from integrated_workflow import IntegratedWorkflow

def main():
    parser = argparse.ArgumentParser(description='Mathpix-노션 통합 워크플로우')
    parser.add_argument('--problem', type=str, help='문제 LaTeX 내용')
    parser.add_argument('--solution', type=str, help='해설 LaTeX 내용')
    parser.add_argument('--problem-file', type=str, help='문제 LaTeX 파일 경로')
    parser.add_argument('--solution-file', type=str, help='해설 LaTeX 파일 경로')
    parser.add_argument('--filename', type=str, required=True, help='기본 파일명 (예: 수2_2025학년도_현우진_드릴_P4)')
    parser.add_argument('--subject', type=str, help='과목 (수1, 수2, 미적분, 확통)')
    parser.add_argument('--year', type=int, help='학년도')
    parser.add_argument('--full', action='store_true', help='전체 워크플로우 실행')
    parser.add_argument('--validate-only', action='store_true', help='검증만 실행')
    parser.add_argument('--fix-only', action='store_true', help='수정만 실행')
    
    args = parser.parse_args()
    
    workflow = IntegratedWorkflow()
    
    # LaTeX 내용 읽기
    problem_latex = args.problem
    solution_latex = args.solution
    
    if args.problem_file:
        with open(args.problem_file, 'r', encoding='utf-8') as f:
            problem_latex = f.read()
    
    if args.solution_file:
        with open(args.solution_file, 'r', encoding='utf-8') as f:
            solution_latex = f.read()
    
    # 실행 모드 선택
    if args.validate_only:
        print("노션 검증만 실행합니다...")
        result = workflow.validate_notion_fields(args.filename)
        return result.get('success', False)
    
    if args.fix_only:
        print("노션 자동 수정만 실행합니다...")
        result = workflow.auto_fix_notion_issues()
        return result.get('success', False)
    
    if args.full:
        print("전체 워크플로우를 실행합니다...")
        if not problem_latex or not solution_latex:
            print("❌ 문제와 해설 LaTeX가 모두 필요합니다.")
            return False
        
        results = workflow.full_workflow(
            problem_latex=problem_latex,
            solution_latex=solution_latex,
            filename_base=args.filename,
            subject=args.subject,
            year=args.year
        )
        
        # 성공 여부 확인
        all_success = all(
            r and r.get('success', False) 
            for r in results.values() 
            if r is not None
        )
        return all_success
    
    else:
        # 문제만 처리
        if problem_latex:
            result = workflow.process_mathpix_problem(
                problem_latex, 
                f"{args.filename}_문제",
                args.subject,
                args.year
            )
            return result.get('success', False)
        
        print("❌ 처리할 내용이 없습니다.")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
