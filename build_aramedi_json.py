# build_aramedi_json.py
# 문제 분석 결과를 바탕으로 3단계 힌트와 3가지 해설을 생성하는 JSON 파일 생성기

import json
import re
from pathlib import Path
from typing import Dict, List, Optional

class AramedProblemGenerator:
    """
    Aramed AI 문제 해설 생성기
    20년 경력의 수능 수학 전문 강사 스타일로 힌트와 해설을 생성
    """
    
    def __init__(self, problem_id: str, problem_text: str, choices: List[str], 
                 solution_hints: Optional[str] = None):
        """
        Args:
            problem_id: 문제 번호 (예: "01")
            problem_text: 문제 지문
            choices: 선택지 리스트 (예: ["-26", "-24", "-22", "-20", "-18"])
            solution_hints: 해설 페이지에서 제공된 힌트 (선택사항)
        """
        self.problem_id = problem_id
        self.problem_text = problem_text
        self.choices = choices
        self.solution_hints = solution_hints
        
    def generate_hint1(self) -> str:
        """힌트1: 개념 확인"""
        # 문제 텍스트에서 핵심 개념 추출 시도
        concepts = []
        if "n제곱근" in self.problem_text or "거듭제곱근" in self.problem_text:
            concepts.append("실수인 n제곱근의 개수")
        if "등차수열" in self.problem_text:
            concepts.append("등차수열")
        if "등비수열" in self.problem_text:
            concepts.append("등비수열")
        if "로그" in self.problem_text:
            concepts.append("로그함수")
        if "지수" in self.problem_text:
            concepts.append("지수함수")
        
        if concepts:
            concept_str = ", ".join(concepts)
            return f"이 문제를 풀기 위해 알아야 할 핵심 개념은 '{concept_str}'입니다. 이 개념의 기본 성질을 정확히 알고 있나요? 특히 문제에서 제시된 조건과 어떻게 연결되는지 생각해보세요."
        else:
            return "이 문제를 풀기 위해 알아야 할 핵심 개념이 무엇인지 생각해보세요. 문제에서 제시된 조건들을 하나씩 분석해보면 어떤 개념을 사용해야 하는지 알 수 있을 것입니다."
    
    def generate_hint2(self) -> str:
        """힌트2: 접근 방향"""
        # 문제 유형에 따라 접근 방향 제시
        if "합" in self.problem_text or "∑" in self.problem_text:
            return "문제에서 주어진 합의 조건을 어떻게 활용할 수 있을까요? 먼저 케이스를 나누어 생각해보세요. 예를 들어, 홀수와 짝수로 나누거나, 부호에 따라 나누는 것이 도움이 될 수 있습니다."
        elif "등차수열" in self.problem_text:
            return "등차수열의 일반항을 먼저 구해보세요. 그리고 문제에서 주어진 조건을 등차수열의 성질과 연결시켜 생각해보면 풀이 방향이 보일 것입니다."
        else:
            return "문제를 단계별로 나누어 생각해보세요. 먼저 주어진 조건을 정리하고, 그 다음 각 조건이 의미하는 바를 파악한 후, 마지막으로 조건들을 종합하여 답을 구해보세요."
    
    def generate_hint3(self) -> str:
        """힌트3: 구체적 실마리"""
        # 문제의 핵심 조건을 찾아서 실마리 제공
        if "합" in self.problem_text:
            return "합의 조건을 만족하려면 각 항의 값이 어떻게 분배되어야 할까요? 특히 특정 값이 0이 되는 경우나 부호가 바뀌는 지점을 찾아보세요."
        elif "등차수열" in self.problem_text and "공차" not in self.problem_text:
            return "등차수열의 공차를 구하는 것이 핵심입니다. 문제에서 주어진 조건을 이용해 공차를 구할 수 있는 방정식을 세워보세요."
        else:
            return "문제의 핵심 조건을 만족하는 특별한 경우를 찾아보세요. 예를 들어, 어떤 값이 0이 되는 경우나, 부호가 바뀌는 지점을 찾으면 문제가 풀릴 수 있습니다."
    
    def generate_solution1_beginner(self) -> Dict:
        """정석 풀이 (초보자용)"""
        steps = [
            "1. 개념 확인: 문제에서 사용되는 핵심 개념을 정리합니다.",
            "   - 문제에서 제시된 조건들을 하나씩 분석",
            "   - 필요한 수학적 개념과 공식 정리",
            "",
            "2. 조건 정리: 주어진 조건을 수식으로 표현합니다.",
            "   - 문제에서 주어진 모든 조건을 수식으로 변환",
            "   - 조건들 간의 관계 파악",
            "",
            "3. 케이스 분리: 문제를 해결하기 위해 경우를 나눕니다.",
            "   - 필요한 경우 케이스를 나누어 생각",
            "   - 각 케이스에서 조건을 만족하는지 확인",
            "",
            "4. 계산: 조건을 만족하는 값을 구합니다.",
            "   - 수식을 정리하여 미지수 구하기",
            "   - 계산 과정을 단계별로 확인",
            "",
            "5. 검증: 구한 답이 조건을 만족하는지 확인합니다.",
            "   - 모든 조건에 대입하여 확인",
            "   - 선택지와 비교",
            "",
            "6. 답: 최종 답을 선택합니다."
        ]
        
        return {
            "title": "정석 풀이 (초보자용)",
            "steps": steps,
            "time_estimate": "8분",
            "difficulty": "쉬움"
        }
    
    def generate_solution2_practical(self) -> Dict:
        """실전 풀이 (중급자용)"""
        key_idea = "문제의 핵심 조건을 빠르게 파악하고, 불필요한 케이스를 제거하여 효율적으로 풀이합니다."
        
        quick_steps = [
            "1. 핵심 조건 파악",
            "2. 불필요한 케이스 제거",
            "3. 핵심 방정식 설정",
            "4. 빠른 계산",
            "5. 답 확인"
        ]
        
        tip = "선택지를 먼저 확인하여 풀이 방향을 정하고, 문제의 핵심 조건만 집중하여 빠르게 해결하세요."
        
        return {
            "title": "실전 풀이 (중급자용)",
            "key_idea": key_idea,
            "quick_steps": quick_steps,
            "time_estimate": "4분",
            "tip": tip
        }
    
    def generate_solution3_advanced(self) -> Dict:
        """개념 확장 (심화용)"""
        why = "이 문제는 핵심 개념을 정확히 이해하고, 조건을 종합하여 해를 구할 수 있는지 확인하는 문제입니다."
        
        concept_details = [
            "1. 문제의 핵심 개념:",
            "   - 문제에서 사용되는 수학적 개념의 본질 이해",
            "   - 개념 간의 연결 관계 파악",
            "",
            "2. 조건의 의미:",
            "   - 각 조건이 수학적으로 의미하는 바",
            "   - 조건들 간의 관계",
            "",
            "3. 해의 유일성:",
            "   - 문제 조건이 유일한 해를 보장하는 이유",
            "   - 출제자의 의도"
        ]
        
        variation_details = [
            "1. 조건 변경:",
            "   - 문제의 조건을 약간 변경하면 어떻게 달라지는지",
            "",
            "2. 범위 확장:",
            "   - 문제의 범위를 확장하거나 축소하면 어떻게 되는지",
            "",
            "3. 다른 수열로 변형:",
            "   - 등차수열을 등비수열로, 또는 다른 수열로 변형"
        ]
        
        pitfall_details = [
            "1. 조건 해석 오류:",
            "   - 문제의 조건을 잘못 이해하여 오답",
            "",
            "2. 계산 실수:",
            "   - 중간 계산 과정에서의 실수",
            "",
            "3. 케이스 누락:",
            "   - 필요한 케이스를 빠뜨려서 오답",
            "",
            "4. 검증 누락:",
            "   - 구한 답이 모든 조건을 만족하는지 확인하지 않음"
        ]
        
        return {
            "title": "개념 확장 (심화용)",
            "why": why,
            "concept": "수학적 의미:",
            "concept_details": concept_details,
            "variation": "유사 문제 예시:",
            "variation_details": variation_details,
            "pitfall": "주의사항:",
            "pitfall_details": pitfall_details
        }
    
    def generate_json(self) -> Dict:
        """전체 JSON 구조 생성"""
        return {
            "problem_id": self.problem_id,
            "hints": {
                "hint1": self.generate_hint1(),
                "hint2": self.generate_hint2(),
                "hint3": self.generate_hint3()
            },
            "solutions": {
                "solution1_beginner": self.generate_solution1_beginner(),
                "solution2_practical": self.generate_solution2_practical(),
                "solution3_advanced": self.generate_solution3_advanced()
            }
        }
    
    def save_json(self, output_path: str, indent: int = 2):
        """JSON 파일로 저장"""
        json_data = self.generate_json()
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=indent)
        print(f"[완료] JSON 파일이 생성되었습니다: {output_path}")


def parse_problem_analysis_file(file_path: str) -> Dict:
    """
    problem_analysis_*.md 파일을 파싱하여 문제 정보 추출
    
    Returns:
        {
            "problem_id": str,
            "problem_text": str,
            "choices": List[str],
            "solution_hints": str
        }
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 문제 번호 추출
    problem_id_match = re.search(r'\*\*(\d+)번\*\*', content)
    problem_id = problem_id_match.group(1) if problem_id_match else "01"
    
    # 문제 지문 추출
    problem_text_match = re.search(r'### 문제 지문\s*\n(.*?)(?=\n###|\n---|\Z)', content, re.DOTALL)
    problem_text = problem_text_match.group(1).strip() if problem_text_match else ""
    
    # 선택지 추출
    choices_match = re.search(r'### 선택지\s*\n(.*?)(?=\n---|\n##|\Z)', content, re.DOTALL)
    choices = []
    if choices_match:
        choices_text = choices_match.group(1)
        # 다양한 선택지 패턴 지원
        choice_patterns = [
            r'[①②③④⑤]\s*\$?([-\d]+)\$?',  # ① -26 또는 ① $-26$
            r'[①②③④⑤]\s*([-\d]+)',  # ① -26
            r'(\d+)\.\s*([-\d]+)',  # 1. -26
        ]
        for pattern in choice_patterns:
            found = re.findall(pattern, choices_text)
            if found:
                # 패턴이 그룹을 반환하는 경우
                if isinstance(found[0], tuple):
                    choices = [f[1] if len(f) > 1 else f[0] for f in found]
                else:
                    choices = found
                break
    
    # 해설 및 힌트 추출
    solution_hints_match = re.search(r'## 📚 해설 및 힌트.*?\n(.*?)(?=\n##|\Z)', content, re.DOTALL)
    solution_hints = solution_hints_match.group(1).strip() if solution_hints_match else ""
    
    return {
        "problem_id": problem_id,
        "problem_text": problem_text,
        "choices": choices,
        "solution_hints": solution_hints
    }


def main():
    """메인 실행 함수"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='문제 분석 결과를 바탕으로 Aramed AI 형식의 JSON 파일 생성'
    )
    parser.add_argument(
        'input_file',
        type=str,
        nargs='?',
        default='problem_analysis_01.md',
        help='문제 분석 결과 파일 경로 (기본값: problem_analysis_01.md)'
    )
    parser.add_argument(
        '-o', '--output',
        type=str,
        default=None,
        help='출력 JSON 파일 경로 (기본값: problem_{problem_id}_hints_solutions.json)'
    )
    
    args = parser.parse_args()
    
    # 입력 파일 확인
    input_path = Path(args.input_file)
    if not input_path.exists():
        print(f'[오류] 파일을 찾을 수 없습니다: {input_path}')
        return
    
    # 문제 정보 파싱
    print(f'[진행] 문제 분석 파일 읽는 중: {input_path}')
    try:
        problem_data = parse_problem_analysis_file(str(input_path))
    except Exception as e:
        print(f'[오류] 파일 파싱 실패: {e}')
        return
    
    print(f'[정보] 문제 번호: {problem_data["problem_id"]}')
    print(f'[정보] 선택지 개수: {len(problem_data["choices"])}')
    
    # JSON 생성기 초기화
    generator = AramedProblemGenerator(
        problem_id=problem_data["problem_id"],
        problem_text=problem_data["problem_text"],
        choices=problem_data["choices"],
        solution_hints=problem_data["solution_hints"]
    )
    
    # 출력 파일 경로 결정
    if args.output:
        output_path = args.output
    else:
        output_path = f'problem_{problem_data["problem_id"]}_hints_solutions.json'
    
    # JSON 생성 및 저장
    print(f'[진행] JSON 파일 생성 중...')
    generator.save_json(output_path)
    
    print(f'\n[완료] 작업이 완료되었습니다!')
    print(f'[파일] {Path(output_path).absolute()}')


if __name__ == '__main__':
    main()
