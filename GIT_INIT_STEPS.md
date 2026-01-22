# Git 초기화 단계별 가이드

## 현재 상태 확인

✅ **.gitignore 파일**: 이미 존재하고 올바르게 설정되어 있습니다.
- .env 파일 제외됨
- node_modules, __pycache__ 등 제외됨
- 모든 필요한 항목 포함됨

❌ **Git 설치**: 아직 설치되지 않았습니다.

## 1단계: Git 설치

### 방법 1: 공식 사이트에서 다운로드 (권장)
1. https://git-scm.com/download/win 방문
2. Windows용 Git 다운로드 및 설치
3. 설치 중 기본 옵션 사용 권장

### 방법 2: Chocolatey 사용 (이미 설치되어 있다면)
```powershell
choco install git
```

## 2단계: Git 설치 확인

**PowerShell에서:**
```powershell
git --version
```

설치가 완료되면 버전 정보가 표시됩니다.

## 3단계: Git 사용자 정보 설정 (처음 사용 시)

```powershell
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

## 4단계: Git 저장소 초기화

**PowerShell에서 실행:**
```powershell
# 프로젝트 디렉토리로 이동
cd C:\Users\a\Documents\Aramed_AI

# Git 저장소 초기화
git init

# 모든 파일 추가
git add .

# 커밋 전 확인 (중요!)
git status

# .env 파일이 제외되었는지 확인
git status | Select-String ".env"
# 아무것도 나오지 않으면 정상 (제외됨)

# 첫 커밋
git commit -m "Initial commit: Aramed_AI project"
```

## 5단계: 원격 저장소 설정

### GitHub 사용 (권장)

1. **GitHub에 로그인**
2. **새 저장소 생성**
   - 오른쪽 상단 + 버튼 → New repository
   - Repository name: `Aramed_AI`
   - Public 또는 Private 선택
   - ⚠️ **중요**: README, .gitignore, license는 추가하지 않기 (이미 있음)
3. **저장소 생성 후 URL 복사**

**PowerShell에서 실행:**
```powershell
# 원격 저장소 추가 (YOUR_USERNAME을 실제 사용자명으로 변경)
git remote add origin https://github.com/YOUR_USERNAME/Aramed_AI.git

# 기본 브랜치를 main으로 설정
git branch -M main

# 원격 저장소에 푸시
git push -u origin main
```

### GitLab 사용

1. **GitLab에 로그인**
2. **새 프로젝트 생성**
3. **저장소 URL 복사 후:**
```powershell
git remote add origin https://gitlab.com/YOUR_USERNAME/Aramed_AI.git
git branch -M main
git push -u origin main
```

## 6단계: 원격 저장소 확인

```powershell
git remote -v
```

## 주의사항

### .env 파일 확인

**.gitignore에 .env가 포함되어 있는지 확인:**
```powershell
Get-Content .gitignore | Select-String ".env"
```

**커밋 전 .env 파일이 제외되었는지 확인:**
```powershell
git status | Select-String ".env"
```
- 아무것도 나오지 않으면 정상 (제외됨)
- .env 파일이 나오면 `.gitignore`를 확인하세요

### 인증 문제 (GitHub)

**Personal Access Token 사용:**
1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token (classic)
3. 권한: `repo` (전체) 선택
4. 토큰 생성 후 복사
5. 푸시 시 비밀번호 대신 토큰 사용

## 문제 해결

### "git: command not found" 오류
- Git이 설치되지 않았거나 PATH에 추가되지 않음
- Git 재설치 또는 PATH 확인

### "Permission denied" 오류
- Personal Access Token 사용 필요 (GitHub)
- 또는 SSH 키 설정

### ".env 파일이 커밋됨" 문제
- `.gitignore`에 `.env`가 포함되어 있는지 확인
- 이미 커밋된 경우: `git rm --cached .env` 후 재커밋

## 다음 단계

1. ✅ Git 설치
2. ✅ Git 사용자 정보 설정
3. ✅ Git 저장소 초기화
4. ✅ 원격 저장소 설정
5. ✅ 원격 저장소에 푸시
6. ⏳ Linux에서 클론 (저장소 URL 전달 후)

## Linux에 전달할 정보

**원격 저장소 설정 완료 후:**
- 저장소 URL: `https://github.com/[사용자명]/Aramed_AI.git`
- 또는 `git@github.com:[사용자명]/Aramed_AI.git` (SSH)

**이 정보를 Linux Cursor AI에게 전달하면 클론 진행합니다.**
