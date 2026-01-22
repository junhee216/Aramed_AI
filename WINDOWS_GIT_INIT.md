# Windows에서 Git 초기화 가이드

## 단계별 진행

### 1단계: Git 설치 확인

**PowerShell에서 확인:**
```powershell
git --version
```

**설치되어 있지 않으면:**
- https://git-scm.com/download/win 에서 다운로드
- 또는 Chocolatey 사용: `choco install git`

### 2단계: Git 저장소 초기화

**PowerShell에서 실행:**
```powershell
# 프로젝트 디렉토리로 이동
cd C:\Users\a\Documents\Aramed_AI

# Git 저장소 초기화
git init

# 모든 파일 추가
git add .

# 첫 커밋
git commit -m "Initial commit: Aramed_AI project"
```

### 3단계: 원격 저장소 설정

**옵션 1: GitHub 사용 (권장)**

1. GitHub에 로그인
2. 새 저장소 생성 (New repository)
   - Repository name: `Aramed_AI`
   - Public 또는 Private 선택
   - README, .gitignore, license는 추가하지 않기 (이미 있음)
3. 저장소 생성 후 URL 복사

**PowerShell에서 실행:**
```powershell
# 원격 저장소 추가
git remote add origin https://github.com/[사용자명]/Aramed_AI.git

# 기본 브랜치를 main으로 설정 (필요시)
git branch -M main

# 원격 저장소에 푸시
git push -u origin main
```

**옵션 2: GitLab 사용**

1. GitLab에 로그인
2. 새 프로젝트 생성
3. 저장소 URL 복사 후 위와 동일하게 진행

**옵션 3: Bitbucket 사용**

1. Bitbucket에 로그인
2. 새 저장소 생성
3. 저장소 URL 복사 후 위와 동일하게 진행

### 4단계: Linux에 저장소 URL 전달

**Windows에서 원격 저장소 설정 완료 후:**
- 저장소 URL을 복사
- Linux Cursor AI에게 전달

**저장소 URL 확인:**
```powershell
git remote -v
```

## 주의사항

### .env 파일 처리

**.env 파일은 Git에 포함되지 않도록:**
- `.gitignore`에 이미 포함되어 있음
- 확인: `cat .gitignore | grep .env`

### 민감한 정보 확인

**커밋 전 확인:**
```powershell
# 커밋할 파일 목록 확인
git status

# .env 파일이 포함되지 않았는지 확인
git status | Select-String ".env"
```

## 문제 해결

### Git 사용자 정보 설정 (처음 사용 시)

```powershell
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### 인증 문제 (GitHub)

**Personal Access Token 사용:**
1. GitHub → Settings → Developer settings → Personal access tokens
2. Generate new token (classic)
3. 권한: repo (전체)
4. 토큰 복사
5. 푸시 시 비밀번호 대신 토큰 사용

## 다음 단계

1. ✅ Git 설치 확인
2. ✅ Git 저장소 초기화
3. ✅ 원격 저장소 설정
4. ✅ 원격 저장소에 푸시
5. ⏳ Linux에서 클론 (저장소 URL 전달 후)

## Linux에 전달할 정보

**원격 저장소 설정 완료 후:**
- 저장소 URL: `https://github.com/[사용자명]/Aramed_AI.git`
- 또는 `git@github.com:[사용자명]/Aramed_AI.git` (SSH)

**이 정보를 Linux Cursor AI에게 전달하면 클론 진행합니다.**
