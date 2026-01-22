# Git Bash에서 사용할 명령어

## 현재 상황
- Git Bash를 사용 중입니다
- PowerShell 명령어 대신 Bash 명령어를 사용해야 합니다

## 경고 메시지에 대해
- `warning: could not open directory` 경고는 무시해도 됩니다
- Git이 홈 디렉토리를 스캔할 때 발생하는 정상적인 경고입니다
- 프로젝트 파일에는 영향을 주지 않습니다

## Git Bash에서 실행할 명령어

### 1단계: 프로젝트 디렉토리로 이동
```bash
cd /c/Users/a/Documents/Aramed_AI
```

### 2단계: Git 저장소 초기화 (아직 안 했다면)
```bash
git init
```

### 3단계: 파일 추가
```bash
git add .
```

### 4단계: 커밋 전 확인
```bash
git status
```

### 5단계: .env 파일이 제외되었는지 확인 (Bash 버전)
```bash
git status | grep ".env"
```
- 아무것도 나오지 않으면 정상 (제외됨)
- `.env` 파일이 나오면 `.gitignore`를 확인하세요

### 6단계: 첫 커밋
```bash
git commit -m "Initial commit: Aramed_AI project"
```

## 원격 저장소 설정

### GitHub 사용
```bash
# 원격 저장소 추가 (YOUR_USERNAME을 실제 사용자명으로 변경)
git remote add origin https://github.com/YOUR_USERNAME/Aramed_AI.git

# 기본 브랜치를 main으로 설정
git branch -M main

# 원격 저장소에 푸시
git push -u origin main
```

## .gitignore 확인

**.gitignore 파일 내용 확인:**
```bash
cat .gitignore | grep ".env"
```

**.env 파일이 실제로 제외되는지 확인:**
```bash
git check-ignore .env
```
- `.env`가 출력되면 정상 (제외됨)

## 문제 해결

### 경고 메시지 제거 (선택사항)
홈 디렉토리 스캔을 피하려면:
```bash
git config --global core.excludesfile ~/.gitignore_global
```

또는 Git Bash에서:
```bash
export HOME=/c/Users/a
```

### .env 파일이 커밋에 포함된 경우
```bash
# 이미 추가된 경우 제거
git rm --cached .env

# 다시 커밋
git commit -m "Remove .env from tracking"
```
