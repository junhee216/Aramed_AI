# Git 설정 및 Windows-Linux 동기화 가이드

## Git 사용의 장점

1. **버전 관리**: 코드 변경 이력 추적
2. **다중 기기 동기화**: Windows 노트북 ↔ Linux 데스크탑 간 코드 공유
3. **백업**: 코드 안전하게 보관
4. **협업**: 여러 환경에서 작업 가능

## 현재 프로젝트 상태

- 프로젝트 위치: `C:\Users\a\Documents\Aramed_AI` (Windows)
- 데스크탑: Linux 환경
- 주요 작업 파일:
  - Python 스크립트 (LaTeX 변환, 검증)
  - Node.js 스크립트 (Notion API 연동)
  - 설정 파일 (.env, .gitignore)

## Git 초기화 방법

### Windows에서 Git 설치 및 초기화

1. **Git 설치** (아직 설치되지 않은 경우)
   ```powershell
   # Chocolatey 사용 시
   choco install git
   
   # 또는 공식 사이트에서 다운로드
   # https://git-scm.com/download/win
   ```

2. **Git 저장소 초기화**
   ```bash
   cd C:\Users\a\Documents\Aramed_AI
   git init
   git add .
   git commit -m "Initial commit: Aramed_AI project"
   ```

3. **원격 저장소 설정** (선택사항)
   - GitHub, GitLab, 또는 자체 Git 서버 사용
   ```bash
   git remote add origin <원격저장소URL>
   git push -u origin main
   ```

### Linux 데스크탑에서 동기화

1. **저장소 클론** (원격 저장소 사용 시)
   ```bash
   git clone <원격저장소URL> ~/Aramed_AI
   cd ~/Aramed_AI
   ```

2. **또는 직접 복사 후 Git 초기화**
   ```bash
   # Windows에서 파일 복사 후
   cd ~/Aramed_AI
   git init
   git remote add origin <원격저장소URL>
   git pull origin main
   ```

## .gitignore 권장 설정

현재 `.gitignore` 파일이 있지만, 다음 항목들이 포함되어야 합니다:

```
# 환경 변수 (중요!)
.env
.env.local
.env.*.local

# 로그 파일
logs/
*.log

# Python 캐시
__pycache__/
*.py[cod]
*$py.class
*.so
.Python

# Node.js
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# IDE 설정
.vscode/
.idea/
*.swp
*.swo
*~

# OS 파일
.DS_Store
Thumbs.db

# 임시 파일
*.tmp
*.temp
output/
data/temp/

# 개인 정보가 포함된 파일
*.key
*.pem
secrets/
```

## Windows ↔ Linux 동기화 방법

### 방법 1: Git 원격 저장소 사용 (권장)

**장점:**
- 자동 동기화
- 버전 관리
- 백업 기능
- 충돌 해결 용이

**작업 흐름:**
```bash
# Windows에서 작업 후
git add .
git commit -m "작업 내용 설명"
git push

# Linux에서 최신 버전 가져오기
git pull

# Linux에서 작업 후
git add .
git commit -m "작업 내용 설명"
git push

# Windows에서 최신 버전 가져오기
git pull
```

### 방법 2: 직접 파일 복사 (간단하지만 위험)

**장점:**
- Git 설치 불필요
- 즉시 동기화

**단점:**
- 버전 관리 없음
- 충돌 위험
- 백업 없음

**사용 시 주의사항:**
- 항상 백업 후 복사
- 파일 덮어쓰기 주의

### 방법 3: 네트워크 공유 폴더

**Windows에서 공유 폴더 설정:**
```powershell
# 공유 폴더 생성
New-Item -Path "C:\Users\a\Documents\Aramed_AI_Shared" -ItemType Directory
# 공유 설정 (GUI에서 설정)
```

**Linux에서 마운트:**
```bash
# SMB/CIFS 마운트
sudo mkdir /mnt/aramed_ai
sudo mount -t cifs //WINDOWS_IP/Aramed_AI_Shared /mnt/aramed_ai -o username=user,password=pass
```

## 중요한 파일 관리

### 반드시 Git에 포함해야 할 파일
- ✅ 모든 `.js`, `.py` 스크립트
- ✅ `package.json`, `requirements.txt` (의존성)
- ✅ `.gitignore`
- ✅ `README.md`
- ✅ 설정 파일 템플릿 (`.env.example`)

### Git에 포함하면 안 되는 파일
- ❌ `.env` (API 키, 비밀번호 포함)
- ❌ `node_modules/` (너무 큼)
- ❌ 로그 파일
- ❌ 개인 정보 파일

### .env 파일 관리

`.env.example` 파일을 만들어서 템플릿 제공:
```bash
# .env.example
NOTION_API_KEY=your_notion_api_key_here
NOTION_DATABASE_ID=your_database_id_here
```

각 기기에서 `.env` 파일을 직접 생성:
```bash
cp .env.example .env
# .env 파일 편집하여 실제 값 입력
```

## 작업 흐름 예시

### 시나리오: Windows에서 작업 시작 → Linux에서 이어가기

1. **Windows에서 작업**
   ```bash
   # 새 기능 개발
   git checkout -b feature/new-converter
   # 코드 작성...
   git add .
   git commit -m "Add new converter script"
   git push origin feature/new-converter
   ```

2. **Linux에서 이어가기**
   ```bash
   git fetch origin
   git checkout feature/new-converter
   # 작업 계속...
   git add .
   git commit -m "Complete converter script"
   git push origin feature/new-converter
   ```

3. **Windows에서 최신 버전 확인**
   ```bash
   git pull origin feature/new-converter
   ```

## 충돌 해결

두 기기에서 동시에 같은 파일을 수정한 경우:

```bash
git pull
# 충돌 발생 시
# <<<<<<< HEAD
# Windows에서 수정한 내용
# =======
# Linux에서 수정한 내용
# >>>>>>> branch-name

# 충돌 해결 후
git add .
git commit -m "Resolve merge conflict"
git push
```

## 권장 Git 워크플로우

### 브랜치 전략
- `main`: 안정적인 버전
- `develop`: 개발 중인 기능
- `feature/*`: 개별 기능 개발
- `fix/*`: 버그 수정

### 커밋 메시지 규칙
```
feat: 새로운 기능 추가
fix: 버그 수정
docs: 문서 수정
style: 코드 포맷팅
refactor: 코드 리팩토링
test: 테스트 추가
chore: 빌드 설정 등
```

예시:
```bash
git commit -m "feat: Add P5 geometry problem converter"
git commit -m "fix: Fix problem number extraction for P5"
```

## Linux 데스크탑에서 DeepSeek 사용 시

### 환경 설정
1. **Python 환경**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Node.js 환경**
   ```bash
   npm install
   ```

3. **환경 변수**
   ```bash
   cp .env.example .env
   # .env 파일 편집
   ```

### 스크립트 실행
```bash
# Python 스크립트
python3 convert_geometry_p5_problems_deepseek.py

# Node.js 스크립트
node review_and_fill_geometry_p5_notion.js
```

## 주의사항

1. **.env 파일은 절대 Git에 커밋하지 마세요**
   - API 키가 노출될 수 있습니다
   - `.gitignore`에 반드시 포함

2. **대용량 파일 주의**
   - `node_modules/`, `__pycache__/` 등은 제외
   - 필요시 Git LFS 사용

3. **정기적인 커밋**
   - 작업 단위별로 커밋
   - 의미 있는 커밋 메시지 작성

4. **정기적인 백업**
   - 원격 저장소에 push
   - 로컬 백업도 유지

## 다음 단계

1. Git 설치 (Windows)
2. Git 저장소 초기화
3. 원격 저장소 설정 (GitHub/GitLab 등)
4. Linux에서 클론
5. `.env` 파일 각 기기에서 설정
6. 작업 시작!

## 도움이 필요하시면

- Git 기본 사용법: https://git-scm.com/doc
- GitHub 가이드: https://guides.github.com
- Git 브랜치 전략: https://nvie.com/posts/a-successful-git-branching-model/
