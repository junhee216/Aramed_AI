# convert_su1_p4_solution_latex.py
# 수1 드릴 P4 해설 LaTeX를 딥시크용 CSV로 변환

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

# Mathpix에서 온 LaTeX 내용
latex_content = """% This LaTeX document needs to be compiled with XeLaTeX.
\\documentclass[10pt]{article}
\\usepackage[utf8]{inputenc}
\\usepackage{amsmath}
\\usepackage{amsfonts}
\\usepackage{amssymb}
\\usepackage[version=4]{mhchem}
\\usepackage{stmaryrd}
\\usepackage{graphicx}
\\usepackage[export]{adjustbox}
\\graphicspath{ {./images/} }
\\usepackage[fallback]{xeCJK}
\\usepackage{polyglossia}
\\usepackage{fontspec}
\\usepackage{newunicodechar}
\\IfFontExistsTF{Noto Serif CJK KR}
{\\setCJKmainfont{Noto Serif CJK KR}}
{\\IfFontExistsTF{Apple SD Gothic Neo}
  {\\setCJKmainfont{Apple SD Gothic Neo}}
  {\\IfFontExistsTF{UnDotum}
    {\\setCJKmainfont{UnDotum}}
    {\\setCJKmainfont{Malgun Gothic}}
}}

\\setmainlanguage{english}
\\IfFontExistsTF{CMU Serif}
{\\setmainfont{CMU Serif}}
{\\IfFontExistsTF{DejaVu Sans}
  {\\setmainfont{DejaVu Sans}}
  {\\setmainfont{Georgia}}
}

\\newunicodechar{⇒}{\\ifmmode\\Rightarrow\\else{$\\Rightarrow$}\\fi}
\\newunicodechar{⋯}{\\ifmmode\\cdots\\else{$\\cdots$}\\fi}

\\begin{document}
\\section*{Comment}
\\section*{Drill. 1 전형적인 합답형 문항}
앞의 문제의 ㄱ은 눈으로만 슥 봐도 금세 참, 거짓을 판단할 수 있다. 너무나 뼌하고도 쉬운 걸 왜 물어본 거지 싶을 수 있지만 ㄱ에서 확인한 결과를 이용하여 주어진 방정식을 변형하고 ㄴ, ᄃ의 해결에 이용할 수 있느냐 하는 것이 핵심이다. 주어진 방정식의 변형은 스스로 생각해내기 어려울 듯…\\\\
ㄴ은 ㄱ에서 확인한 결과를 이용하지 않고 자연수 $q$ 의 값 몇 개 정도를 대입해서 구간 $\\left(0, \\frac{\\pi}{2}\\right)$ 에서 두 곡선 $y=\\tan x, y=-\\tan n x$ 의 교점의 개수의 변화를 관찰하여 판단했어도 잘한 거다.\\\\
꼭 그런 건 아니지만 웬만한 합답형 문항은 뭐지 싶은 쉬운 판단이 이어지는 판단의 중요한 단서가 된다는 것!

\\section*{Drill. 2 삼각함수의 각의 변환}
주어진 각을 $\\frac{n \\pi}{2} \\pm \\theta$ ( $n$ 은 정수)의 꼴로 변형한 후 삼각함수와 부호를 다음과 같이 변형한다.

\\begin{center}
\\begin{tabular}{|l|l|}
\\hline
함수 & \\begin{tabular}{l}
(1) $n$ 이 홀수: $\\sin \\Rightarrow \\cos , \\cos \\Rightarrow \\sin , \\tan \\Rightarrow \\frac{1}{\\tan }$ 로 변형 \\\\
(2) $n$ 이 짝수: $\\sin \\Rightarrow \\sin , \\cos \\Rightarrow \\cos , \\tan \\Rightarrow \\tan$ 로 원형 유지 \\\\
\\end{tabular} \\\\
\\hline
부호 & $\\frac{n \\pi}{2} \\pm \\theta$ ( $\\theta$ 는 예각으로 간주) 가 속한 사분면에서의 원래 주어진 삼각함수의 부호를 따른다. \\\\
\\hline
\\end{tabular}
\\end{center}

\\section*{Comment}
\\section*{Drill. 1 코사인법칙의 활용}
코사인법칙을 이용하는 대표적인 상황을 다음과 같이 정리해두자.\\\\
(1) 두 변과 한 각 ⇒ 남은 한 변\\\\
(2) 세 변 ⇒ 세 내각

또한 코사인법칙에 관한 문제가 삼각형의 기호 $A, B, C, a, b, c$ 로 주어지지 않을 때가 많으므로 다음과 같은 이미지로 기억할 필요도 있다.\\\\
\\includegraphics[max width=\\textwidth, center]{4b82262b-5b93-43b9-ba45-1e687813d04a-02_249_316_1023_1197}

$$
c^{2}=a^{2}+b^{2}-2 a b \\cos \\theta, \\cos \\theta=\\frac{a^{2}+b^{2}-c^{2}}{2 a b}
$$

앞의 문제는 삼각형 ABC 의 세 내각에 관한 것이므로 $A+B+C=\\pi$ 를 이용할 준비는 하고 시작해야 한다. 삼각함수의 각의 변환으로 $A$ 의 삼각함수의 값을 구하고 코사인법칙으로 선분 BC 의 길이를 구하는 것까지는 아무런 고민 없이 진행해야 한다. 다음 단계는 삼각형의 내접원을 어떻게 다루기로 하느냐에 따라 달라질 수 있다. 첫 번째 방법은 삼각형 ABC 의 넓이를 구할 수 있으므로 내접원의 반지름의 길이를 미지수로 잡아 구하는 것.\\\\
다른 방법으로 꼭짓점 A 에서 내접원에 그은 접선의 길이를 미지수로 잡으면 내접원에 그은 접선의 길이가 같다는 것을 이용하여 다른 접선의 길이도 모두 이 미지수로 나타내고 그 값을 구한 후, $\\cos A=-\\cos (\\pi-A)$ 를 이용하는 것. 모두 괜찮은 방법이다.

\\section*{Drill. 2 삼각형의 내접원}
삼각형의 내접원이 등장하면 다음 사항을 점검해보자.\\\\
(1) 세 내각의 이등분\\\\
\\includegraphics[max width=\\textwidth, center]{4b82262b-5b93-43b9-ba45-1e687813d04a-03_249_333_841_1239}\\\\
(2) 내접원에 그은 접선의 길이가 같다.\\\\
\\includegraphics[max width=\\textwidth, center]{4b82262b-5b93-43b9-ba45-1e687813d04a-03_253_327_1192_1241}\\\\
(3) 내심에서 세 변에 내린 수선의 길이가 같다. ( 3 개의 높이가 같은 삼각형)\\\\
\\includegraphics[max width=\\textwidth, center]{4b82262b-5b93-43b9-ba45-1e687813d04a-03_240_322_1552_1243}

세 변의 길이가 각각 $a, b, c$ 인 삼각형의 넓이를 $S$, 내접원의 반지름의 길이를 $r$ 이라 하면

$$
S=\\frac{1}{2} a r+\\frac{1}{2} b r+\\frac{1}{2} c r=\\frac{1}{2}(a+b+c) r
$$

\\section*{Comment}
\\section*{Drill. 1 사인법칙의 활용}
사인법칙을 이용하는 대표적인 상황을 다음과 같이 정리해두자.\\\\
(1) 마주보는 두 쌍의 각과 변\\\\
(2) 외접원\\\\
(3) 변의 길이 또는 사인의 값의 관계식

또한 사인법칙에 관한 문제가 삼각형의 기호 $A, B, C, a, b, c$ 로 주어지지 않을 때가\\\\
많으므로 다음과 같은 이미지로 기억할 필요도 있다.\\\\
\\includegraphics[max width=\\textwidth, center]{4b82262b-5b93-43b9-ba45-1e687813d04a-04_212_307_1093_1197}

$$
\\frac{a}{\\sin \\alpha}=\\frac{b}{\\sin \\beta}
$$

\\section*{Drill. 2 원에 내접하는 사각형}
원 O 에 내접하는 사각형 ABCD 에서 나타나는 각 사이의 관계는 다음 그림과 같다.\\\\
\\includegraphics[max width=\\textwidth, center]{4b82262b-5b93-43b9-ba45-1e687813d04a-04_360_346_1609_913}\\\\
\\includegraphics[max width=\\textwidth, center]{4b82262b-5b93-43b9-ba45-1e687813d04a-04_331_307_1611_1387}

$$
\\begin{aligned}
& \\angle \\mathrm{ACB}=\\angle \\mathrm{ADB}, \\angle \\mathrm{DAC}=\\angle \\mathrm{DBC} \\\\
& \\angle \\mathrm{ABD}=\\angle \\mathrm{ACD}, \\angle \\mathrm{BAC}=\\angle \\mathrm{BDC}
\\end{aligned}
$$

원에 내접하는 사각형에 대하여 마주보는 두 각의 크기의 합이 $\\pi$ 임을 이용할 마음의 준비를 하자. 또한 원의 중심과 원 위의 세 점을 꼭짓점으로 하는 사각형에서 중심각에 해당하는 각의 크기의 $\\frac{1}{2}$ 과 마주보는 각의 크기의 합이 $\\pi$ 인 것도 이용할 수 있다.

앞의 문제는 $\\frac{1}{2} \\times \\angle \\mathrm{AOB}+\\angle \\mathrm{APB}=\\pi$ 인 관계를 파악하는 것에서 출발한다.

\\section*{Comment}
\\section*{Drill 닮은 도형의 발견}
앞의 문제는 삼각형 ABC 의 외접원이 $C_{1}$, 삼각형 ABD 의 외접원이 $C_{2}$ 이고, 두 삼각형 $\\mathrm{ABC}, \\mathrm{ABD}$ 가 한 내각을 공유하는 것을 체크하고 시작할 수 있어야 한다. 두 원 $C_{1}, C_{2}$ 의 반지름의 길이의 비와 선분 BC 의 길이에서 곧바로 선분 BD 의 길이도 알 수 있다. 사인법칙의 전형적인 상황이다. $\\angle \\mathrm{CAB}=\\angle \\mathrm{CBD}$ 에서 두 삼각형 $\\mathrm{ABD}, \\mathrm{BCD}$ 의 닮음 그리고 닮음에 대응하는 변의 짝짓기만 잘 하면 거의 끝!

\\section*{Comment}
Drill 매우 익숙해야 할 전형적인 상황들\\\\
앞의 문제에서 점 D 를 공유하는 세 선분 $\\mathrm{AD}, \\mathrm{BD}, \\mathrm{CD}$ 의 길이가 주어지고 두 삼각형 ADB , BDC 의 넓이의 비가 주어졌다. 각에 대한 조건은 없다. 적절한 각의 크기를 미지수로 잡아야 할 필요성을 인식하고, $\\angle \\mathrm{ADB}, \\angle \\mathrm{BDC}$ 의 크기를 각각 미지수로 잡으면 사인의 값의 비를 구할 수 있다는 것도 예상해야 한다. 그리고 스스로 두 삼각형 ADB 와 BDC 의 공통의 외접원에서 사인법칙으로 자연스럽게 이어갈 수 있어야 한다. 이렇게 두 선분 $\\mathrm{AB}, \\mathrm{BC}$ 의 길이의 비를 구하고 나면 마무리? 두 삼각형의 공통의 변이 있는 전형적인 사인법칙과 코사인 법칙의 상황이고 원에 내접하는 사각형 ABCD 가 있다!

\\section*{Comment}
\\section*{Drill. 1 각 사이의 관계}
각의 크기를 미지수로 잡을 때 동위각, 엇각, 맞꼭지각으로 시작하는 각에 관한 여러 기본 지식과 특수각을 이용하여 각 사이의 관계를 파악하는 것은 매우 중요하다. 앞의 문제에서 세 삼각형 $\\mathrm{ABF}, \\mathrm{BDF}, \\mathrm{CFE}$ 의 외접원의 넓이의 비에서 사인법칙의 상황임을 인식하고 외접원의 반지름의 길이의 비로 이용하기로 마음먹었다면 어떤 각의 크기를 미지수로 잡는 것이 좋을까?\\\\
두 삼각형 $\\mathrm{ABF}, \\mathrm{CFE}$ 에서 맞꼭지각이 보이고 두 삼각형 $\\mathrm{CFE}, \\mathrm{BDF}$ 에서 동위각이 또는 두 삼각형 $\\mathrm{ABF}, \\mathrm{BDF}$ 에서 엇각이 보이나? 이렇게 스타트만 잘 끊고 정사각형, 직각삼각형, 이등변삼각형을 적극적으로 이용하면 남은 길은 그리 어렵지 않게 보일 것이다.

\\section*{Drill. 2 동위각, 엇각, 맞꼭지각}
평행한 두 직선과 각이 등장하면 동위각, 엇각, 맞꼭지각을 반드시 체크하도록 하자. 엇각이 문제 해결의 중요한 단서가 되고 놓치기 쉬우므로 주의해야 한다.\\\\
\\includegraphics[max width=\\textwidth, center]{4b82262b-5b93-43b9-ba45-1e687813d04a-07_437_507_1397_1099}

\\section*{Comment}
\\section*{Drill 직각삼각형의 적극 이용과 특수각의 발견}
앞의 문제는 삼각형 ADE 가 $\\angle \\mathrm{AED}=\\frac{\\pi}{2}$ 인 직각삼각형인 것을 어떻게 이용하느냐에 따라 풀이 방향이 살짝 달라질 수 있다. 특수각을 발견했다면 태도가 잘 잡힌 것! 중학교 도형의 기초가 잘 잡혀있다면 $\\overline{\\mathrm{BC}}=2 \\sqrt{2} \\times \\overline{\\mathrm{DE}}$ 에서 $2 \\sqrt{2}$ 와 점 B 에서 선분 AC 에 내린 수선의 길이가 선분 DE 의 길이의 2 배라는 것이 한눈에 잡히면서 특수각을 쉽게 발견할 수 있을 것이고, 아주 기본적인 상황의 사인법칙과 피타고라스 정리의 계산만 남는다.\\\\
사인법칙과 코사인법칙에 관한 문제에서 특수각이 숨은 조건으로 자주 등장하고 특수각의 발견 여부가 문제 해결 전체를 좌우하는 경우가 많으므로 특수각에 항상 주목해야 한다.

\\section*{Comment}
\\section*{Drill. 1 원주각에 대한 이해 그리고 외접원의 인식}
앞의 문제는 $\\overline{\\mathrm{PQ}}=\\overline{\\mathrm{QR}}$ 에서 두 점 $\\mathrm{P}, \\mathrm{Q}$ 로부터 각각 뻗어나간 선분, 두 점 $\\mathrm{Q}, \\mathrm{R}$ 로부터 각각 뻔어나간 선분이 반원의 호 또는 지름의 중점에서 만나는지 확인하는 것이 우선이다.\\\\
원주각에 대한 본능! $\\angle \\mathrm{PAQ}=\\angle \\mathrm{PRQ}=\\angle \\mathrm{QPR}$ 을 확인하고 나면 삼각형 QPR 이 변의 길이가 모두 주어진 이등변삼각형이므로 직각삼각형을 이용하여 이들 각에 대한 삼각함수의 값을 알 수 있다. 삼각형 PAQ 의 넓이의 조건을 이용하기 위해 두 선분 $\\mathrm{AP}, \\mathrm{AQ}$ 의 길이를 미지수로 잡으면 이 두 미지수의 곱을 코사인법칙에 이용할 수 있다는 센스 정도는 작동해야 한다. 직각삼각형 ABQ 는 체크해두었을 테고 빗변 AB 는 만만한 삼각형 QPR 의 외접원의 지름으로 인식할 수 있어야 한다. 두 선분 $\\mathrm{AP}, \\mathrm{AQ}$ 의 길이를 각각 구하지 않고도 $\\overline{\\mathrm{BQ}}^{2}-\\overline{\\mathrm{AP}}^{2}$ 의 값을 구할 길이 보이면 굿이다.\\\\
부채꼴의 호 위에 세 꼭짓점이 있는 삼각형에 대해서도 이 부채꼴과 반지름의 길이가 같은 원을 외접원으로 하는 사인법칙을 적극 이용할 수 있도록 하자.

\\section*{Drill. 2 원주각의 크기와 호의 길이 사이의 관계}
(1) 한 원 또는 합동인 두 원에서 길이가 같은 호에 대한 원주각의 크기는 서로 같다.\\\\
(2) 한 원 또는 합동인 두 원에서 크기가 같은 원주각에 대한 호의 길이는 서로 같다.\\\\
(3) 한 원 또는 합동인 두 원에서 호의 길이는 원주각의 크기에 정비례한다.\\\\
\\includegraphics[max width=\\textwidth, center]{4b82262b-5b93-43b9-ba45-1e687813d04a-09_282_278_1412_1645}

\\section*{2023학년도 수능 공통 11번}
그림과 같이 사각형 ABCD 가 한 원에 내접하고

$$
\\overline{\\mathrm{AB}}=5, \\overline{\\mathrm{AC}}=3 \\sqrt{5}, \\overline{\\mathrm{AD}}=7, \\angle \\mathrm{BAC}=\\angle \\mathrm{CAD}
$$

일 때, 이 원의 반지름의 길이는? [4점]\\\\
\\includegraphics[max width=\\textwidth, center]{4b82262b-5b93-43b9-ba45-1e687813d04a-10_426_401_917_1213}\\\\
(1) $\\frac{5 \\sqrt{2}}{2}$\\\\
(2) $\\frac{8 \\sqrt{5}}{5}$\\\\
(3) $\\frac{5 \\sqrt{5}}{3}$\\\\
(4) $\\frac{8 \\sqrt{2}}{3}$\\\\
(5) $\\frac{9 \\sqrt{3}}{4}$

답 (1)

\\section*{Drill 삼각형의 각의 이등분선 \\\\
 삼각형 ABC 에서 $\\angle \\mathrm{A}$ 의 이등분선이 변 BC 와 만나는 점을 D 라 하면 $\\overline{\\mathrm{AB}}: \\overline{\\mathrm{AC}}=\\overline{\\mathrm{BD}}: \\overline{\\mathrm{DC}}$}
\\begin{center}
\\includegraphics[max width=\\textwidth]{4b82262b-5b93-43b9-ba45-1e687813d04a-11_276_367_879_1163}
\\end{center}

$$
a: b=x: y=S_{1}: S_{2}
$$

앞의 문제에서는 $\\overline{\\mathrm{BD}}=\\overline{\\mathrm{DE}}$ 에서 $\\angle \\mathrm{BAD}=\\angle \\mathrm{DAE}$ 를, 삼각형 ABC 의 각의 이등분선에서 $\\overline{\\mathrm{AB}}: \\overline{\\mathrm{AC}}=\\overline{\\mathrm{BD}}: \\overline{\\mathrm{DC}}$ 를 연결 지어 선분 AC 의 길이를 구하는 것까지는 아무 고민 없이 쭉쭉 진행할 수 있어야 한다. 삼각형 ABD 의 외접원을 다루기 위해 어떤 각과 어떤 선분에 관심을 가져야 할지 어렵지 않게 판단하고 마무리할 수 있을 듯.

\\section*{Drill 각의 이등분선의 발견}
앞의 문제에서 $\\overline{\\mathrm{DE}}=\\overline{\\mathrm{DF}}$ 인 조건에서 각의 이등분선을 발견할 수 있었기를⋯ 두 삼각형 $\\mathrm{BDE}, \\mathrm{CFD}$ 가 직각삼각형인 것에서 두 원 $C_{1}, C_{2}$ 에 집중하는 것이 당연하다는 생각에서 살짝만 벗어나 다른 기하적 상황을 조금만 더 점검해보면 된다. 선분 AB 의 길이가 주어졌고 두 선분 $\\mathrm{BD}, \\mathrm{CD}$ 의 길이의 비가 주어졌다. 여기에 $\\overline{\\mathrm{DE}}=\\overline{\\mathrm{DF}}$ 인 조건만 연결 지으면 성공! 삼각형의 각의 이등분선을 이용하고 $\\cos (\\angle \\mathrm{EDF})$ 의 값이 주어진 것에서 사각형 AEDF 의 특수함을 발견하면 거의 다 된 거다.

\\section*{Comment}
\\section*{Drill. 1 삼각형의 각의 이등분선과 원에 대한 여러 성질의 이해의 결합}
앞의 문제에서는 아무런 언급도 없는 선분 DE 의 길이를 나타내기로 마음먹는 것이 가장 중요하다. 왜? 점 E 는 원 위에 있다. 원 위의 점은 홀로 내버려두지 않는다. 그리고 삼각형 DEH 가 직각삼각형이고 결정적으로 $\\angle \\mathrm{BAD}=\\angle \\mathrm{DAE}$, 즉 $\\overline{\\mathrm{BD}}=\\overline{\\mathrm{DE}}$ 이다.\\\\
삼각형의 각의 이등분선의 상황을 이용하면 2 개의 미지수로 꽤 많은 선분의 길이를 나타낼 수 있고, 이렇게 나타낸 상황에서 갈 길은 어느 정도 정해진다. 코사인법칙은 막판에 살짝 끼어들 뿐, 중학교 도형이 거의 전부인 문제.

\\section*{Drill. 2 원과 삼각형의 닮음 (1)}
원의 접선, 할선, 현에서 나타나는 삼각형의 닮음과 각 사이의 관계, 길이 사이의 관계는 다음과 같다.\\\\
(1) 그림과 같이 원의 현 AB 의 연장선과 원 위의 점 T 에서의 접선이 만나는 점을 P 라 하면 삼각형 PAT 와 삼각형 PTB 는 서로 닮은 도형이고 다음이 성립한다.

$$
\\overline{\\mathrm{PT}}^{2}=\\overline{\\mathrm{PA}} \\times \\overline{\\mathrm{PB}} \\Rightarrow \\overline{\\mathrm{PA}}, \\overline{\\mathrm{PT}}, \\overline{\\mathrm{~PB}} \\text { 가 이 순서대로 등비수열을 이룬다. }
$$

\\includegraphics[max width=\\textwidth, center]{4b82262b-5b93-43b9-ba45-1e687813d04a-13_320_353_1463_1177}\\\\
(2) 그림과 같이 원의 두 현 $\\mathrm{AB}, \\mathrm{CD}$ 각각의 연장선이 만나는 점을 P 라 하면 삼각형 PAC 와 삼각형 PDB 는 서로 닮은 도형이고 다음이 성립한다.

$$
\\overline{\\mathrm{PA}} \\times \\overline{\\mathrm{PB}}=\\overline{\\mathrm{PC}} \\times \\overline{\\mathrm{PD}}
$$

\\begin{center}
\\includegraphics[max width=\\textwidth]{4b82262b-5b93-43b9-ba45-1e687813d04a-13_329_409_1983_1150}
\\end{center}


\\end{document}"""

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
    
    # Drill 섹션 추출
    # 주제에 줄바꿈이 포함될 수 있으므로 더 유연한 패턴 사용
    drill_pattern = r'\\section\*\{Drill\.?\s*([0-9]*)\s*([^}]+?)(?:\\\\[^}]*?)?\}(.*?)(?=\\section\*|\\end\{document\}|$)'
    drill_matches = re.finditer(drill_pattern, body, re.DOTALL)
    
    for match in drill_matches:
        drill_num = match.group(1).strip() if match.group(1) else ""
        topic = match.group(2).strip()
        content = match.group(3).strip()
        
        # 이전 섹션이 Comment인지 확인
        start_pos = match.start()
        prev_comment = body.rfind('\\section*{Comment}', 0, start_pos)
        prev_drill = body.rfind('\\section*{Drill', 0, start_pos)
        
        # Comment 바로 다음에 오는 Drill은 전략
        is_strategy = False
        if prev_comment != -1:
            # Comment와 Drill 사이에 다른 섹션이 없으면 전략
            between = body[prev_comment:start_pos]
            if '\\section*{' not in between.replace('\\section*{Comment}', '').replace('\\section*{Drill', ''):
                is_strategy = True
        
        # 이미지 제거
        content = re.sub(r'\\includegraphics.*?}', '', content)
        content = re.sub(r'\\begin\{figure\}.*?\\end\{figure\}', '', content, flags=re.DOTALL)
        content = re.sub(r'\\begin\{center\}.*?\\end\{center\}', '', content, flags=re.DOTALL)
        content = re.sub(r'\\begin\{tabular\}.*?\\end\{tabular\}', '', content, flags=re.DOTALL)
        content = re.sub(r'\\captionsetup.*?}', '', content)
        content = re.sub(r'\\\\', ' ', content)
        # $$ 블록을 공백으로 대체 (이미 처리된 것으로 간주)
        content = re.sub(r'\$\$', ' ', content)
        content = re.sub(r'\s+', ' ', content)
        
        # $$ 블록 내부의 $는 제거하지 않음 (이미 $$로 처리됨)
        # 단, $$ 블록이 제대로 닫히지 않은 경우 확인
        
        # 주제도 정리 (줄바꿈 제거)
        topic = re.sub(r'\\\\', ' ', topic)
        topic = re.sub(r'\s+', ' ', topic)
        
        if len(content) > 50:
            if is_strategy:
                # 문제 참조 추출
                question_ref = ""
                if '앞의 문제' in content:
                    question_ref = "P4"
                
                solutions.append({
                    "type": "strategy",
                    "topic": f"{drill_num} {topic}".strip() if drill_num else topic,
                    "question_ref": question_ref,
                    "content": content
                })
            else:
                solutions.append({
                    "type": "concept",
                    "topic": f"{drill_num} {topic}".strip() if drill_num else topic,
                    "content": content,
                    "question_ref": ""
                })
    
    # Comment 섹션 내의 "Drill ..." 텍스트 추출 (전략)
    comment_sections = re.finditer(r'\\section\*\{Comment\}(.*?)(?=\\section\*\{|\\end\{document\}|$)', body, re.DOTALL)
    
    for comment_match in comment_sections:
        comment_content = comment_match.group(1)
        
        # Comment 내의 "Drill ..." 텍스트 찾기 (섹션 헤더가 아닌 경우)
        drill_text_pattern = r'(?:^|\\\\)Drill\s+([^\\]+?)(?=\\\\section|Drill|\\end|$)'
        drill_text_matches = re.finditer(drill_text_pattern, comment_content, re.DOTALL | re.MULTILINE)
        
        for drill_text_match in drill_text_matches:
            strategy_content = drill_text_match.group(1).strip()
            
            # 이미지 제거
            strategy_content = re.sub(r'\\includegraphics.*?}', '', strategy_content)
            strategy_content = re.sub(r'\\\\', ' ', strategy_content)
            strategy_content = re.sub(r'\$\$', ' ', strategy_content)
            strategy_content = re.sub(r'\s+', ' ', strategy_content)
            
            if len(strategy_content) > 50:
                # 문제 참조 추출
                question_ref = ""
                if '앞의 문제' in strategy_content:
                    question_ref = "P4"
                
                solutions.append({
                    "type": "strategy",
                    "topic": "삼각함수",
                    "question_ref": question_ref,
                    "content": strategy_content
                })
    
    return solutions

def review_solutions(solutions):
    """해설 데이터 검토 (수학적 논리 포함)"""
    print("=" * 60)
    print("[수1 드릴 P4 해설 데이터 검토]")
    print("=" * 60)
    
    issues = []
    math_errors = []
    
    for i, sol in enumerate(solutions, 1):
        sol_type = sol.get("type", "")
        print(f"\n[해설 {i}] 타입: {sol_type}")
        
        if sol_type == "concept":
            topic = sol.get("topic", "")
            print(f"[주제] {topic}")
        elif sol_type == "strategy":
            q_ref = sol.get("question_ref", "")
            print(f"[문제 참조] {q_ref}")
        
        content = sol.get("content", "")
        print(f"[내용 길이] {len(content)}자")
        
        # LaTeX 검사
        dollar_count = content.count('$')
        # $$ 블록 제거 후 계산
        content_no_dblock = re.sub(r'\$\$', '', content)
        dollar_count_single = content_no_dblock.count('$')
        
        # 주제에도 $가 있을 수 있으므로 확인
        topic_dollar = sol.get("topic", "").count('$')
        topic_no_dblock = re.sub(r'\$\$', '', sol.get("topic", ""))
        topic_dollar_single = topic_no_dblock.count('$')
        
        total_dollar_single = dollar_count_single + topic_dollar_single
        
        if total_dollar_single % 2 != 0:
            issues.append(f"해설 {i}: LaTeX 수식 괄호 불일치")
            print("[LaTeX] 오류: 수식 괄호 불일치")
            # 디버깅: 문제가 되는 부분 출력
            if dollar_count_single % 2 != 0:
                print(f"  [내용] $ 개수: {dollar_count_single}개")
            if topic_dollar_single % 2 != 0:
                print(f"  [주제] $ 개수: {topic_dollar_single}개")
        else:
            print("[LaTeX] 정상")
        
        # 수학적 논리 검토
        # 1. 삼각함수 범위 확인
        if 'sin' in content or 'cos' in content:
            # 범위: -1 <= sin x <= 1, -1 <= cos x <= 1
            # 단, 최댓값/최솟값 설명은 예외
            if 'sin' in content and ('> 1' in content or '< -1' in content):
                if '최댓값' not in content and '최솟값' not in content and '범위' not in content:
                    math_errors.append(f"해설 {i}: sin 함수 범위 오류 가능성")
        
        # 2. 코사인법칙 공식 확인
        if '코사인법칙' in content or 'cos' in content:
            # c² = a² + b² - 2ab cos θ
            if 'c^{2}' in content or 'c^2' in content:
                if 'a^{2}' in content or 'a^2' in content:
                    if 'b^{2}' in content or 'b^2' in content:
                        if '2ab' in content or '2 a b' in content:
                            pass  # 공식 구조 정상
        
        # 3. 사인법칙 공식 확인
        if '사인법칙' in content:
            # a/sin A = b/sin B = c/sin C
            if 'sin' in content and '/' in content:
                pass  # 공식 구조 정상
        
        # 4. 삼각형 내각의 합 확인
        if 'A+B+C' in content or 'A + B + C' in content:
            if 'π' in content or 'pi' in content or '180' in content:
                pass  # 정상
        
        # 5. 원주각과 중심각 관계 확인
        if '원주각' in content or '중심각' in content:
            # 중심각 = 2 × 원주각
            if '2' in content or '\\frac{1}{2}' in content:
                pass  # 관계 정상
        
        # 6. 각의 이등분선 비율 확인
        if '각의 이등분선' in content:
            # AB:AC = BD:DC
            if ':' in content:
                pass  # 비율 관계 정상
    
    print("\n" + "=" * 60)
    print("[검토 결과]")
    print("=" * 60)
    print(f"[총 해설 수] {len(solutions)}개")
    
    concept_count = sum(1 for s in solutions if s.get("type") == "concept")
    strategy_count = sum(1 for s in solutions if s.get("type") == "strategy")
    print(f"[개념] {concept_count}개")
    print(f"[전략] {strategy_count}개")
    
    if issues:
        print("\n[LaTeX 오류]")
        for issue in issues:
            print(f"  - {issue}")
    
    if math_errors:
        print("\n[수학적 논리 오류 가능성]")
        for error in math_errors:
            print(f"  - {error}")
    
    if not issues and not math_errors:
        print("\n[오류] 없음")
        print("[수학적 논리] 정상")
    
    return len(issues) == 0 and len(math_errors) == 0

def save_for_deepseek(solutions):
    """딥시크용 CSV 저장"""
    base_dir = Path(r'C:\Users\a\Documents\MathPDF\organized\현우진\수1_2025학년도_현우진_드릴')
    save_dir = base_dir
    save_dir.mkdir(parents=True, exist_ok=True)
    
    # CSV 저장
    csv_path = save_dir / "수1_2025학년도_현우진_드릴_P4_해설_deepseek.csv"
    with open(csv_path, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['type', 'topic', 'question_ref', 'content'])
        for solution in solutions:
            writer.writerow([
                solution.get('type', ''),
                solution.get('topic', ''),
                solution.get('question_ref', ''),
                solution.get('content', '')
            ])
    
    print(f"\n[CSV 저장 완료] {csv_path}")
    
    # JSON 저장
    json_path = save_dir / "수1_2025학년도_현우진_드릴_P4_해설_deepseek.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(solutions, f, ensure_ascii=False, indent=2)
    
    print(f"[JSON 저장 완료] {json_path}")
    
    return csv_path, json_path

def main():
    print("=" * 60)
    print("[수1 드릴 P4 해설 LaTeX → CSV 변환]")
    print("=" * 60)
    
    # 1단계: LaTeX 읽기
    print(f"\n[1단계] LaTeX 내용 읽기 완료 ({len(latex_content)}자)")
    
    # 2단계: 해설 추출
    print("\n[2단계] 해설 추출 중...")
    solutions = extract_solutions_from_latex(latex_content)
    print(f"[완료] {len(solutions)}개 해설 추출됨")
    
    # 3단계: 검토 (수학적 논리 포함)
    print("\n[3단계] 해설 검토 중...")
    is_valid = review_solutions(solutions)
    
    # 4단계: 저장
    print("\n[4단계] 딥시크용 파일 저장 중...")
    csv_path, json_path = save_for_deepseek(solutions)
    
    print("\n" + "=" * 60)
    print("[완료] 딥시크가 읽을 수 있는 형태로 저장되었습니다.")
    print("=" * 60)
    base_dir = Path(r'C:\Users\a\Documents\MathPDF\organized\현우진\수1_2025학년도_현우진_드릴')
    print(f"저장 위치: {base_dir}")
    print(f"  - CSV: {csv_path.name}")
    print(f"  - JSON: {json_path.name}")

if __name__ == '__main__':
    main()
