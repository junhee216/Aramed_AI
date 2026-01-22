# Linux Cursor AI에게 전달할 메시지

## 현재 상황

Windows 노트북에서 작업한 Aramed_AI 프로젝트를 Linux 데스크탑에서 이어서 작업하려고 합니다.

**문제:**
- Cursor 재설치 후에도 동일한 입력 문제 발생
- 오른쪽 하단 화살표가 계속 켜져 있음
- 영어도 입력이 안 됨
- **메모장(텍스트 에디터)에 작성 후 복사 붙이기로 작업 중**

## 프로젝트 상태

### 완료된 작업
- 기하_2024학년도_현우진_드릴_P5 작업 완료
  - 문제 변환: `convert_geometry_p5_problems_deepseek.py`
  - 해설 변환: `convert_geometry_p5_solution_deepseek.py`
  - Notion 필드 채우기: `review_and_fill_geometry_p5_notion.js`

### 주요 파일
- 모든 스크립트 파일 준비됨
- 문서: `README.md`, `GIT_SETUP_GUIDE.md`, `WORK_STATUS.md`, `LINUX_SETUP.md`

## 입력 문제 해결 요청 (긴급!)

### 문제 1: IME 입력 모드 활성화 (현재 문제)
- **오른쪽 하단에 화살표가 계속 켜져 있음**
- **영어도 입력이 안 됨**
- 한 글자 이상 타이핑이 안 되고, 알파벳만 바뀜
- IME(입력기)가 활성화되어 입력이 제대로 처리되지 않음
- 한영 전환 키를 눌러도 해결되지 않음

### 문제 2: 음성 입력 모드 활성화
- Cursor 채팅창에서 마이크 아이콘이 불이 들어옴
- 한글 입력이 사라짐 (키보드 입력이 차단됨)
- 음성 입력 모드가 실수로 활성화되는 것 같음

### 문제 3: 일반 한글 입력
- Cursor 채팅창에서 한글이 한 글자 이상 입력되지 않음

### 해결 방법 제안

**긴급 해결: IME 입력 모드 비활성화 (현재 문제)**
1. **Right Alt** 키로 한영 전환 시도
2. **Space + Shift** 키로 한영 전환 시도
3. 타이핑 후 **Enter** 키로 입력 확정 시도
4. **Esc** 키로 입력 취소 후 재시도
5. Cursor를 IME 없이 실행:
   ```bash
   # 터미널에서
   unset GTK_IM_MODULE
   unset QT_IM_MODULE
   unset XMODIFIERS
   cursor
   ```
6. Cursor 설정에서 IME 관련 설정 변경 필요

**음성 입력 모드 비활성화:**
1. `Esc` 키로 음성 입력 모드 종료
2. 마이크 아이콘 클릭하여 비활성화
3. Cursor 설정에서 음성 입력 기능 비활성화:
   ```json
   // ~/.config/Cursor/User/settings.json
   {
     "cursor.chat.voiceInput.enabled": false,
     "cursor.chat.voiceInput.autoActivate": false
   }
   ```

**한글 입력 문제 해결:**

1. **IME 환경 변수 확인 및 설정**
   ```bash
   # 현재 설정 확인
   echo $GTK_IM_MODULE
   echo $QT_IM_MODULE
   echo $XMODIFIERS
   
   # 설정 (ibus 사용 시)
   export GTK_IM_MODULE=ibus
   export QT_IM_MODULE=ibus
   export XMODIFIERS=@im=ibus
   
   # .bashrc 또는 .zshrc에 추가
   echo 'export GTK_IM_MODULE=ibus' >> ~/.bashrc
   echo 'export QT_IM_MODULE=ibus' >> ~/.bashrc
   echo 'export XMODIFIERS=@im=ibus' >> ~/.bashrc
   ```

2. **한글 입력기 설치 확인**
   ```bash
   # ibus-hangul 설치 확인
   which ibus
   ibus version
   
   # 설치되어 있지 않으면
   # Ubuntu/Debian: sudo apt install ibus-hangul
   # Arch: sudo pacman -S ibus-hangul
   # Fedora: sudo dnf install ibus-hangul
   ```

3. **Cursor 실행 스크립트 생성**
   ```bash
   # ~/bin/cursor-korean.sh 생성
   #!/bin/bash
   export GTK_IM_MODULE=ibus
   export QT_IM_MODULE=ibus
   export XMODIFIERS=@im=ibus
   /usr/bin/cursor "$@"
   
   # 실행 권한 부여
   chmod +x ~/bin/cursor-korean.sh
   ```

4. **Cursor 설정 확인**
   - `~/.config/Cursor/User/settings.json` 확인
   - 입력 관련 설정 추가 필요 여부 확인

5. **대안: 영어로 작업**
   - 한글 입력이 안 되면 영어로 질문하고 답변도 영어로 받기
   - 코드 주석은 나중에 한글로 수정

## 다음 작업 시 참고사항

### 파일 경로 문제
- 스크립트에 Windows 절대 경로(`C:\Users\a\Documents\...`)가 하드코딩되어 있음
- Linux에서는 환경 변수 `MATHPDF_PATH` 설정 필요
- 또는 스크립트 내 경로를 Linux 경로로 수정 필요

### 환경 설정
```bash
# .env 파일 생성
cp .env.example .env
# .env 파일 편집하여 Notion API 키 입력

# 의존성 설치
npm install
pip install -r requirements.txt
```

### 스크립트 실행
```bash
# Python 스크립트
python3 convert_geometry_p5_problems_deepseek.py

# Node.js 스크립트
node review_and_fill_geometry_p5_notion.js
```

## 긴급 질문

**중요: Windows-Linux 연결 작업 후 문제 발생!**

**상황:**
- **처음 Linux 시작 시에는 정상 작동했음**
- **Windows와 연결하기 위한 작업 후 문제 발생**
- 오른쪽 하단 화살표가 계속 켜져 있음
- 영어도 입력이 안 됨
- 한 글자 이상 타이핑이 안 되고, 알파벳만 바뀜
- IME가 활성화되어 입력이 제대로 처리되지 않음

**시도한 것:**
- 한영 전환 키 (Right Alt, Space+Shift 등)
- Enter 키로 입력 확정
- Esc 키로 입력 취소

**확인 요청:**
1. Windows-Linux 연결을 위해 변경한 설정
   - Git 설정 (`git config`)
   - 환경 변수 (`.bashrc`, `.zshrc`)
   - Cursor 설정 (`settings.json`)
   - 생성한 스크립트 파일
2. 최근에 실행한 명령어
   - Git 관련 명령어
   - 환경 변수 설정 명령어
   - Cursor 설정 변경 명령어
3. 최근에 생성한 파일
   - `~/bin/` 디렉토리의 스크립트
   - 프로젝트 내 스크립트

**되돌리기 요청:**
1. 변경한 모든 설정을 원래대로 되돌려주세요
2. 또는 변경 사항 목록을 알려주세요 (직접 수정하겠습니다)
3. Git 작업을 했다면, 변경 사항을 되돌리는 방법을 알려주세요
4. 기본 설정으로 복원하는 방법을 알려주세요

**필요한 해결:**
1. IME를 완전히 비활성화하여 Cursor를 실행하는 방법
2. Cursor 설정에서 IME 관련 설정 변경 방법
3. 환경 변수로 IME 비활성화하는 방법
4. **지금 당장 입력이 안 되어서 작업을 진행할 수 없습니다. 빠른 해결 방법을 알려주세요!**

## 일반 질문

1. Cursor에서 한글 입력 문제를 해결할 수 있는 방법이 있나요?
2. IME 설정이나 Cursor 설정을 변경해야 하나요?
3. 아니면 영어로 작업하는 것이 더 나을까요?

## 참고 문서

- `LINUX_SETUP.md`: Linux 설정 가이드
- `GIT_SETUP_GUIDE.md`: Git 동기화 가이드
- `WORK_STATUS.md`: 현재 작업 상태

## 메모장으로 작업하는 경우

**현재 워크플로우:**
1. 텍스트 에디터(gedit, nano 등)에서 질문 작성
2. 복사(Ctrl+C) 후 Cursor 채팅창에 붙여넣기(Ctrl+V)
3. Cursor 답변 확인 및 필요시 저장

**효율적인 작업을 위해:**
- 질문을 명확하게 작성
- 단계별로 작업 요청
- 답변도 텍스트 파일로 저장하여 참고

---

**복사해서 Linux Cursor에 붙여넣으세요!**

**또는 `START_LINUX_CURSOR.md` 파일의 첫 메시지를 사용하세요!**
