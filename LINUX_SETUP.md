# Linux 데스크탑 설정 가이드

## 문제: "글씨가 한 글자 이상 안 써진다"

이 문제는 주로 **파일 경로 문제** 때문입니다. 스크립트에 Windows 절대 경로가 하드코딩되어 있어서 Linux에서 파일을 찾지 못합니다.

## 해결 방법

### 방법 1: 환경 변수 설정 (권장)

```bash
# .bashrc 또는 .zshrc에 추가
export MATHPDF_PATH="$HOME/Documents/MathPDF/organized"

# 또는 직접 설정
export MATHPDF_PATH="/home/사용자명/Documents/MathPDF/organized"
```

### 방법 2: 심볼릭 링크 생성

```bash
# Windows 경로와 유사한 구조 생성
mkdir -p ~/Documents/MathPDF/organized/현우진/기하_2024학년도_현우진_드릴

# 또는 실제 파일 위치로 심볼릭 링크
ln -s /실제/파일/경로 ~/Documents/MathPDF/organized
```

### 방법 3: 스크립트 경로 수정

스크립트 내의 하드코딩된 경로를 Linux 경로로 변경:

**Python 스크립트:**
```python
# 변경 전
base_dir = Path(r'C:\Users\a\Documents\MathPDF\organized\현우진\기하_2024학년도_현우진_드릴')

# 변경 후
from src.utils.path_utils import get_math_pdf_path
base_dir = get_math_pdf_path() / '현우진' / '기하_2024학년도_현우진_드릴'
```

**Node.js 스크립트:**
```javascript
// 변경 전
const problemPath = path.join('C:', 'Users', 'a', 'Documents', 'MathPDF', ...);

// 변경 후
import { getGeometryProblemPath } from './src/utils/path_utils.js';
const problemPath = getGeometryProblemPath('P5');
```

## 빠른 수정 (임시)

스크립트를 직접 수정:

### Python 스크립트 수정
```python
# 파일 상단에 추가
import os
from pathlib import Path

# 경로 설정
if os.name == 'nt':  # Windows
    BASE_DIR = Path(r'C:\Users\a\Documents\MathPDF\organized')
else:  # Linux
    BASE_DIR = Path.home() / 'Documents' / 'MathPDF' / 'organized'

# 사용
base_dir = BASE_DIR / '현우진' / '기하_2024학년도_현우진_드릴'
```

### Node.js 스크립트 수정
```javascript
// 파일 상단에 추가
import os from 'os';
import path from 'path';

// 경로 설정
const BASE_DIR = process.env.MATHPDF_PATH || 
    path.join(os.homedir(), 'Documents', 'MathPDF', 'organized');

// 사용
const problemPath = path.join(
    BASE_DIR,
    '현우진',
    '기하_2024학년도_현우진_드릴',
    '기하_2024학년도_현우진_드릴_P5_문제_deepseek.json'
);
```

## 파일 위치 확인

```bash
# 파일이 실제로 어디에 있는지 확인
find ~ -name "기하_2024학년도_현우진_드릴_P5_문제_deepseek.json" 2>/dev/null

# 찾은 경로를 환경 변수로 설정
export MATHPDF_PATH="$(dirname $(find ~ -name "기하_2024학년도_현우진_드릴_P5_문제_deepseek.json" 2>/dev/null | head -1))"
```

## 인코딩 문제 해결

```bash
# Python 스크립트 실행 시
export PYTHONIOENCODING=utf-8
python3 convert_geometry_p5_problems_deepseek.py

# Node.js 스크립트 실행 시
export NODE_ENV=utf-8
node review_and_fill_geometry_p5_notion.js
```

## 테스트

```bash
# 경로 확인
python3 -c "from pathlib import Path; import os; print(Path.home() / 'Documents' / 'MathPDF' / 'organized')"

# 파일 존재 확인
ls -la ~/Documents/MathPDF/organized/현우진/기하_2024학년도_현우진_드릴/
```

## 다음 단계

1. 파일 위치 확인
2. 환경 변수 설정 또는 경로 수정
3. 스크립트 실행 테스트
