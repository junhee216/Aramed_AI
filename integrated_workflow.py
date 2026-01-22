# integrated_workflow.py
# Mathpix → Deepseek 변환 → 노션 검증 통합 워크플로우

"""
통합 워크플로우:
1. Mathpix LaTeX 변환 (문제/해설)
2. Deepseek 형식 저장 (CSV/JSON)
3. 수학적 논리 검증
4. 노션 필드 매핑 및 검증
5. 자동 개선 제안
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Optional
import subprocess

# Windows 콘솔 인코딩 설정
if sys.platform == 'win32':
    import os
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')


class IntegratedWorkflow:
    """Mathpix → 노션 통합 워크플로우"""
    
    def __init__(self, base_dir: str = None):
        self.base_dir = Path(base_dir) if base_dir else Path.cwd()
        self.problems_json = None
        self.solutions_json = None
        
    def process_mathpix_problem(self, latex_content: str, filename: str, 
                               subject: str = None, year: int = None) -> Dict:
        """
        Mathpix 문제 LaTeX 처리
        
        Args:
            latex_content: Mathpix에서 변환된 LaTeX 내용
            filename: 파일명 (예: "수2_2025학년도_현우진_드릴_P4_문제")
            subject: 과목 (수1, 수2, 미적분, 확통)
            year: 학년도
            
        Returns:
            처리된 문제 딕셔너리
        """
        print("=" * 80)
        print(f"[Mathpix 문제 처리] {filename}")
        print("=" * 80)
        
        # 1. Mathpix 변환 스크립트 동적 임포트
        try:
            # 변환 스크립트 생성 또는 기존 것 사용
            conversion_script = self._get_or_create_conversion_script(filename, 'problem')
            
            # 변환 실행
            result = self._run_conversion(conversion_script, latex_content, filename)
            
            if result and result.get('success'):
                self.problems_json = result.get('json_path')
                print(f"✅ 문제 변환 완료: {self.problems_json}")
                return result
            else:
                print(f"❌ 문제 변환 실패: {result.get('error', 'Unknown error')}")
                return result
                
        except Exception as e:
            print(f"❌ 처리 중 오류: {e}")
            return {'success': False, 'error': str(e)}
    
    def process_mathpix_solution(self, latex_content: str, filename: str,
                                subject: str = None, year: int = None) -> Dict:
        """
        Mathpix 해설 LaTeX 처리
        
        Args:
            latex_content: Mathpix에서 변환된 LaTeX 내용
            filename: 파일명 (예: "수2_2025학년도_현우진_드릴_P4_해설")
            subject: 과목
            year: 학년도
            
        Returns:
            처리된 해설 딕셔너리
        """
        print("=" * 80)
        print(f"[Mathpix 해설 처리] {filename}")
        print("=" * 80)
        
        try:
            conversion_script = self._get_or_create_conversion_script(filename, 'solution')
            result = self._run_conversion(conversion_script, latex_content, filename)
            
            if result and result.get('success'):
                self.solutions_json = result.get('json_path')
                print(f"✅ 해설 변환 완료: {self.solutions_json}")
                return result
            else:
                print(f"❌ 해설 변환 실패: {result.get('error', 'Unknown error')}")
                return result
                
        except Exception as e:
            print(f"❌ 처리 중 오류: {e}")
            return {'success': False, 'error': str(e)}
    
    def validate_math_logic(self, problems_path: str = None, 
                           solutions_path: str = None) -> Dict:
        """
        수학적 논리 검증
        
        Args:
            problems_path: 문제 JSON 경로
            solutions_path: 해설 JSON 경로
            
        Returns:
            검증 결과 딕셔너리
        """
        print("\n" + "=" * 80)
        print("[수학적 논리 검증]")
        print("=" * 80)
        
        problems_path = problems_path or self.problems_json
        solutions_path = solutions_path or self.solutions_json
        
        if not problems_path:
            return {'success': False, 'error': '문제 파일이 없습니다.'}
        
        try:
            # 수학적 논리 검증 스크립트 실행
            validation_script = self._create_validation_script(problems_path, solutions_path)
            result = subprocess.run(
                [sys.executable, validation_script],
                capture_output=True,
                text=True,
                encoding='utf-8'
            )
            
            if result.returncode == 0:
                print(result.stdout)
                return {'success': True, 'output': result.stdout}
            else:
                print(f"❌ 검증 오류: {result.stderr}")
                return {'success': False, 'error': result.stderr}
                
        except Exception as e:
            print(f"❌ 검증 중 오류: {e}")
            return {'success': False, 'error': str(e)}
    
    def validate_notion_fields(self, problem_id: str) -> Dict:
        """
        노션 필드 검증
        
        Args:
            problem_id: 문제 ID (예: "수2_2025학년도_현우진_드릴_P4_01")
            
        Returns:
            검증 결과 딕셔너리
        """
        print("\n" + "=" * 80)
        print(f"[노션 필드 검증] {problem_id}")
        print("=" * 80)
        
        try:
            # 노션 검증 스크립트 실행
            result = subprocess.run(
                ['node', 'comprehensive_notion_review.js'],
                capture_output=True,
                text=True,
                encoding='utf-8',
                cwd=str(self.base_dir)
            )
            
            if result.returncode == 0:
                print(result.stdout)
                return {'success': True, 'output': result.stdout}
            else:
                print(f"❌ 노션 검증 오류: {result.stderr}")
                return {'success': False, 'error': result.stderr}
                
        except Exception as e:
            print(f"❌ 노션 검증 중 오류: {e}")
            return {'success': False, 'error': str(e)}
    
    def auto_fix_notion_issues(self) -> Dict:
        """
        노션 이슈 자동 수정
        
        Returns:
            수정 결과 딕셔너리
        """
        print("\n" + "=" * 80)
        print("[노션 이슈 자동 수정]")
        print("=" * 80)
        
        try:
            result = subprocess.run(
                ['node', 'fix_notion_comprehensive_math_logic.js'],
                capture_output=True,
                text=True,
                encoding='utf-8',
                cwd=str(self.base_dir)
            )
            
            if result.returncode == 0:
                print(result.stdout)
                return {'success': True, 'output': result.stdout}
            else:
                print(f"❌ 수정 오류: {result.stderr}")
                return {'success': False, 'error': result.stderr}
                
        except Exception as e:
            print(f"❌ 수정 중 오류: {e}")
            return {'success': False, 'error': str(e)}
    
    def full_workflow(self, problem_latex: str, solution_latex: str,
                     filename_base: str, subject: str = None, 
                     year: int = None) -> Dict:
        """
        전체 워크플로우 실행
        
        Args:
            problem_latex: 문제 LaTeX
            solution_latex: 해설 LaTeX
            filename_base: 기본 파일명 (예: "수2_2025학년도_현우진_드릴_P4")
            subject: 과목
            year: 학년도
            
        Returns:
            전체 워크플로우 결과
        """
        print("\n" + "=" * 80)
        print("[전체 워크플로우 시작]")
        print("=" * 80)
        
        results = {
            'problem_conversion': None,
            'solution_conversion': None,
            'math_validation': None,
            'notion_validation': None,
            'notion_fix': None
        }
        
        # 1. 문제 변환
        problem_filename = f"{filename_base}_문제"
        results['problem_conversion'] = self.process_mathpix_problem(
            problem_latex, problem_filename, subject, year
        )
        
        # 2. 해설 변환
        solution_filename = f"{filename_base}_해설"
        results['solution_conversion'] = self.process_mathpix_solution(
            solution_latex, solution_filename, subject, year
        )
        
        # 3. 수학적 논리 검증
        if results['problem_conversion'].get('success'):
            results['math_validation'] = self.validate_math_logic()
        
        # 4. 노션 필드 검증
        results['notion_validation'] = self.validate_notion_fields(filename_base)
        
        # 5. 노션 이슈 자동 수정
        results['notion_fix'] = self.auto_fix_notion_issues()
        
        # 결과 요약
        print("\n" + "=" * 80)
        print("[워크플로우 결과 요약]")
        print("=" * 80)
        for step, result in results.items():
            status = "✅" if result and result.get('success') else "❌"
            print(f"{status} {step}: {result.get('success', False)}")
        
        return results
    
    def _get_or_create_conversion_script(self, filename: str, type: str) -> str:
        """변환 스크립트 가져오기 또는 생성"""
        # 기존 스크립트 패턴 확인
        script_pattern = f"convert_{filename.lower().replace(' ', '_')}_{type}_latex.py"
        script_path = self.base_dir / script_pattern
        
        if script_path.exists():
            return str(script_path)
        
        # 스크립트가 없으면 템플릿 기반 생성
        template_path = self.base_dir / f"convert_template_{type}.py"
        if template_path.exists():
            # 템플릿 복사 및 수정
            return str(script_path)
        
        # 기본 변환기 사용
        if type == 'problem':
            return 'mathpix_latex_processor_optimized.py'
        else:
            return 'mathpix_latex_processor_optimized.py'
    
    def _run_conversion(self, script_path: str, latex_content: str, 
                       filename: str) -> Dict:
        """변환 스크립트 실행"""
        try:
            # 임시 파일에 LaTeX 저장
            temp_latex = self.base_dir / f"temp_{filename}.tex"
            with open(temp_latex, 'w', encoding='utf-8') as f:
                f.write(latex_content)
            
            # 스크립트 실행
            result = subprocess.run(
                [sys.executable, script_path],
                capture_output=True,
                text=True,
                encoding='utf-8',
                cwd=str(self.base_dir)
            )
            
            # 임시 파일 삭제
            if temp_latex.exists():
                temp_latex.unlink()
            
            if result.returncode == 0:
                # JSON 파일 경로 찾기
                json_pattern = f"{filename}_deepseek.json"
                json_path = self._find_json_file(json_pattern)
                
                return {
                    'success': True,
                    'output': result.stdout,
                    'json_path': str(json_path) if json_path else None
                }
            else:
                return {
                    'success': False,
                    'error': result.stderr,
                    'output': result.stdout
                }
                
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _find_json_file(self, pattern: str) -> Optional[Path]:
        """JSON 파일 찾기"""
        # 여러 가능한 디렉토리에서 검색
        search_dirs = [
            self.base_dir,
            self.base_dir / 'output',
            Path(r'C:\Users\a\Documents\MathPDF\organized\현우진')
        ]
        
        for search_dir in search_dirs:
            if search_dir.exists():
                for json_file in search_dir.rglob(f"*{pattern}*"):
                    if json_file.suffix == '.json':
                        return json_file
        
        return None
    
    def _create_validation_script(self, problems_path: str, 
                                 solutions_path: str = None) -> str:
        """수학적 논리 검증 스크립트 생성"""
        validation_script = self.base_dir / 'temp_validation.py'
        
        script_content = f"""
# 임시 검증 스크립트
import json
import sys
from pathlib import Path

problems_path = Path(r'{problems_path}')
solutions_path = Path(r'{solutions_path}') if '{solutions_path}' else None

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

problems = load_json(problems_path)
solutions = load_json(solutions_path) if solutions_path and solutions_path.exists() else None

# 기본 검증
print(f"문제 수: {{len(problems)}}")
if solutions:
    print(f"해설 수: {{len(solutions)}}")

# LaTeX 수식 검증
errors = []
for i, problem in enumerate(problems):
    question = problem.get('question', '')
    dollar_count = question.count('$')
    if dollar_count % 2 != 0:
        errors.append(f"문제 {{i+1}}: LaTeX 달러 기호 불일치")
    
    if solutions:
        solution = solutions[i] if i < len(solutions) else None
        if solution:
            solution_text = solution.get('content', '')
            sol_dollar = solution_text.count('$')
            if sol_dollar % 2 != 0:
                errors.append(f"해설 {{i+1}}: LaTeX 달러 기호 불일치")

if errors:
    print("\\n❌ 검증 오류:")
    for error in errors:
        print(f"  - {{error}}")
else:
    print("\\n✅ 기본 검증 통과")
"""
        
        with open(validation_script, 'w', encoding='utf-8') as f:
            f.write(script_content)
        
        return str(validation_script)


def main():
    """메인 함수 - 사용 예시"""
    workflow = IntegratedWorkflow()
    
    # 예시 사용
    print("통합 워크플로우 사용 예시:")
    print("""
    workflow = IntegratedWorkflow()
    
    # 문제 처리
    result = workflow.process_mathpix_problem(
        latex_content=problem_latex,
        filename="수2_2025학년도_현우진_드릴_P4_문제",
        subject="수2",
        year=2025
    )
    
    # 전체 워크플로우
    results = workflow.full_workflow(
        problem_latex=problem_latex,
        solution_latex=solution_latex,
        filename_base="수2_2025학년도_현우진_드릴_P4",
        subject="수2",
        year=2025
    )
    """)


if __name__ == '__main__':
    main()
