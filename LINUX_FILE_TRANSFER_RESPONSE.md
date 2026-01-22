# Linux Cursor AI에게 전달할 답변

## 복사해서 Linux Cursor에 붙여넣으세요!

```
프로젝트 파일 전달 방법에 대해 답변드리겠습니다.

## 현재 상황
- Windows 노트북: C:\Users\a\Documents\Aramed_AI
- Linux 데스크탑: ~/Documents/Aramed_AI (또는 원하는 위치)
- 두 컴퓨터는 별도의 기기입니다

## 권장 방법: Git 사용 (가장 깔끔함)

### 방법 1: Git 저장소 생성 및 동기화 (권장)

**Windows에서:**
1. Git 저장소 초기화 (아직 안 했다면)
2. GitHub/GitLab 등에 푸시
3. Linux에서 클론

**또는 직접 동기화:**
- Windows에서 Git 저장소 초기화
- Linux에서 직접 pull (SSH 또는 HTTPS)

### 방법 2: USB/외장 저장장치
- Windows에서 프로젝트 폴더를 USB에 복사
- Linux에서 USB 마운트 후 복사
- 간단하지만 수동 작업 필요

### 방법 3: 네트워크 공유
- Windows에서 네트워크 공유 설정
- Linux에서 SMB로 접근하여 복사
- 또는 SFTP 사용

### 방법 4: 클라우드 스토리지
- Google Drive, Dropbox 등에 업로드
- Linux에서 다운로드
- 편리하지만 대용량 시 시간 소요

## 제안하는 방법

**가장 깔끔한 방법: Git 사용**

1. **Windows에서 Git 저장소 초기화 (아직 안 했다면)**
   ```bash
   # Windows PowerShell에서
   cd C:\Users\a\Documents\Aramed_AI
   git init
   git add .
   git commit -m "Initial commit"
   ```

2. **원격 저장소 설정 (GitHub/GitLab 등)**
   - GitHub에 새 저장소 생성
   - 또는 GitLab, Bitbucket 등 사용

3. **Linux에서 클론**
   ```bash
   cd ~/Documents
   git clone [저장소 URL]
   ```

**또는 직접 전송이 필요하면:**

**USB 사용 (가장 빠름):**
1. Windows에서 프로젝트 폴더를 USB에 복사
2. Linux에서 USB 마운트
3. 프로젝트 폴더를 ~/Documents/Aramed_AI로 복사

## 필수 도구 설치

**Linux에서 필요한 도구:**
- Git (프로젝트 동기화용)
- Python 3 (스크립트 실행용)
- Node.js (Notion 연동용)
- pip, npm (패키지 관리)

**설치 명령어 (Ubuntu/Debian 기준):**
```bash
sudo apt update
sudo apt install -y git python3 python3-pip nodejs npm
```

**설치 확인:**
```bash
git --version
python3 --version
node --version
npm --version
```

## 프로젝트 경로 정보

**Windows 경로:**
- C:\Users\a\Documents\Aramed_AI

**Linux 경로 (제안):**
- ~/Documents/Aramed_AI
- 또는 ~/Aramed_AI

## 다음 단계

1. **파일 전달 방법 선택**
   - Git 사용 (권장)
   - USB 사용
   - 네트워크 공유
   - 클라우드 스토리지

2. **선택한 방법에 따라 진행**
   - 제가 선택한 방법에 맞춰 단계별로 안내해주세요

3. **필수 도구 설치**
   - 설치 진행해도 됩니다 (sudo 권한 있음)
   - 또는 설치 명령어를 알려주시면 직접 진행하겠습니다

어떤 방법으로 진행하시겠습니까?
```

## 빠른 선택 가이드

### Git 사용 (권장) - 장점:
- ✅ 버전 관리 가능
- ✅ 두 기기 간 동기화 용이
- ✅ 변경 사항 추적 가능
- ⚠️ GitHub/GitLab 계정 필요

### USB 사용 - 장점:
- ✅ 빠르고 간단
- ✅ 인터넷 불필요
- ⚠️ 수동 작업 필요

### 네트워크 공유 - 장점:
- ✅ 실시간 동기화 가능
- ⚠️ 네트워크 설정 필요

### 클라우드 스토리지 - 장점:
- ✅ 편리함
- ⚠️ 대용량 시 시간 소요

## 제안

**가장 깔끔한 방법: Git 사용**
- 이미 `GIT_SETUP_GUIDE.md` 문서가 있음
- 버전 관리와 동기화를 한 번에 해결
- 향후 작업에도 유용

**가장 빠른 방법: USB 사용**
- 지금 당장 파일이 필요하면 USB 사용
- 나중에 Git으로 전환 가능

어떤 방법을 선호하시나요?
