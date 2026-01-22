# Linux-Windows 연결 작업 후 문제 해결

## 문제 상황
- 처음 Linux 시작 시에는 정상 작동
- Linux Cursor AI가 Windows와 연결하기 위한 작업 후 문제 발생
- 오른쪽 하단 화살표가 계속 켜져 있음
- 영어도 입력이 안 됨

## Linux Cursor AI가 했을 수 있는 작업들

### 1. Git 설정 변경
```bash
# 확인
git config --list --global
git config --list --local

# Git 설정 파일 확인
cat ~/.gitconfig
cat .git/config
```

### 2. 환경 변수 추가
```bash
# 확인
env | grep -i "GTK\|QT\|XMOD\|IME\|CURSOR\|GIT"

# .bashrc, .zshrc 확인
grep -i "export\|GTK\|QT\|XMOD\|IME\|CURSOR\|GIT" ~/.bashrc ~/.zshrc ~/.profile
```

### 3. Cursor 설정 변경
```bash
# 확인
cat ~/.config/Cursor/User/settings.json

# 최근 변경 확인
ls -lt ~/.config/Cursor/User/settings.json
stat ~/.config/Cursor/User/settings.json
```

### 4. 프로젝트 경로 관련 설정
```bash
# 확인
echo $MATHPDF_PATH
echo $PATH
cat .env 2>/dev/null
cat .env.example 2>/dev/null
```

### 5. 스크립트 생성
```bash
# 확인
ls -la ~/bin/cursor* 2>/dev/null
ls -la *.sh 2>/dev/null
find . -name "*.sh" -type f
```

## 즉시 해결 방법

### 방법 1: Cursor 완전 재시작 (환경 변수 초기화)
```bash
# Cursor 완전 종료
pkill -f cursor

# 환경 변수 초기화
unset GTK_IM_MODULE
unset QT_IM_MODULE
unset XMODIFIERS
unset MATHPDF_PATH

# Cursor 재시작
cursor
```

### 방법 2: 최근 변경 사항 확인
```bash
# Cursor 설정 파일 백업 확인
ls -lt ~/.config/Cursor/User/settings.json*

# Git 변경 사항 확인
cd ~/Documents/Aramed_AI  # 또는 프로젝트 경로
git status
git diff
git log --oneline -10

# 최근 수정된 파일 확인
find . -type f -mtime -1 -ls
```

### 방법 3: Cursor 설정 초기화
```bash
# 설정 파일 백업
cp ~/.config/Cursor/User/settings.json ~/.config/Cursor/User/settings.json.backup.$(date +%Y%m%d_%H%M%S)

# 최소 설정으로 시작
cat > ~/.config/Cursor/User/settings.json << 'EOF'
{
  "editor.fontSize": 14,
  "editor.fontFamily": "Consolas, 'Courier New', monospace"
}
EOF

# Cursor 재시작
pkill -f cursor
cursor
```

### 방법 4: 환경 변수 제거
```bash
# .bashrc 또는 .zshrc에서 최근 추가된 내용 확인
tail -20 ~/.bashrc
tail -20 ~/.zshrc

# IME 관련 설정 주석 처리 또는 제거
# export GTK_IM_MODULE=ibus
# export QT_IM_MODULE=ibus
# export XMODIFIERS=@im=ibus

# 변경 후
source ~/.bashrc  # 또는 source ~/.zshrc
```

## Linux Cursor AI에게 전달할 메시지

```
긴급: Windows-Linux 연결 작업 후 입력 문제 발생!

상황:
- 처음 Linux 시작 시에는 정상 작동
- Windows와 연결하기 위한 작업 후 문제 발생
- 오른쪽 하단 화살표가 계속 켜져 있음
- 영어도 입력이 안 됨

확인 요청:
1. Windows-Linux 연결을 위해 변경한 설정
   - Git 설정 (git config)
   - 환경 변수 (.bashrc, .zshrc)
   - Cursor 설정 (settings.json)
   - 생성한 스크립트 파일
2. 최근에 실행한 명령어
   - Git 관련 명령어
   - 환경 변수 설정 명령어
   - Cursor 설정 변경 명령어

되돌리기 요청:
1. 변경한 모든 설정을 원래대로 되돌려주세요
2. 또는 변경 사항 목록을 알려주세요 (직접 수정하겠습니다)
3. Git 작업을 했다면, 변경 사항을 되돌리는 방법을 알려주세요

지금 당장 입력이 안 되어서 작업을 진행할 수 없습니다.
빠른 해결 방법을 알려주세요!
```

## 확인 체크리스트

1. ✅ Git 설정 확인 (`git config --list`)
2. ✅ 환경 변수 확인 (`env | grep -i "GTK\|QT\|XMOD"`)
3. ✅ .bashrc/.zshrc 확인 (`tail -20 ~/.bashrc`)
4. ✅ Cursor 설정 확인 (`cat ~/.config/Cursor/User/settings.json`)
5. ✅ 최근 생성된 스크립트 확인 (`ls -la ~/bin/cursor*`)
6. ✅ Git 변경 사항 확인 (`git status`, `git diff`)
7. ✅ Cursor 재시작 (환경 변수 없이)

## 빠른 복구 명령어

```bash
# 한 번에 실행
pkill -f cursor && \
unset GTK_IM_MODULE QT_IM_MODULE XMODIFIERS && \
cursor
```

## 참고

- Windows-Linux 연결 작업은 보통 Git 설정, 환경 변수, 프로젝트 경로 설정을 포함
- IME 관련 설정이 실수로 추가되었을 가능성
- Cursor 설정이 변경되었을 가능성
