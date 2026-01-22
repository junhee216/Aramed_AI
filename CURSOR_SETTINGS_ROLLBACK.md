# Cursor 설정 되돌리기 가이드

## 문제 상황
- Linux Cursor AI와 작업 후 입력 문제 발생
- 오른쪽 하단 화살표가 계속 켜져 있음
- 영어도 입력이 안 됨
- 이전에는 정상 작동했음

## 확인해야 할 설정 파일

### 1. Cursor 설정 파일 확인
```bash
# 설정 파일 위치
~/.config/Cursor/User/settings.json

# 최근 변경 확인
ls -lt ~/.config/Cursor/User/settings.json
```

**확인할 설정:**
- `cursor.chat.voiceInput.*` 관련 설정
- `editor.*` 관련 IME 설정
- `input.*` 관련 설정

**되돌리기:**
```bash
# 백업이 있다면
cp ~/.config/Cursor/User/settings.json.backup ~/.config/Cursor/User/settings.json

# 또는 문제가 되는 설정 제거
# settings.json에서 다음 항목 제거:
# - "cursor.chat.voiceInput.enabled"
# - "cursor.chat.voiceInput.autoActivate"
# - IME 관련 설정
```

### 2. 환경 변수 확인
```bash
# 현재 환경 변수 확인
echo $GTK_IM_MODULE
echo $QT_IM_MODULE
echo $XMODIFIERS

# .bashrc 또는 .zshrc 확인
grep -i "GTK_IM_MODULE\|QT_IM_MODULE\|XMODIFIERS" ~/.bashrc ~/.zshrc
```

**되돌리기:**
```bash
# .bashrc 또는 .zshrc에서 IME 관련 설정 제거
# 또는 주석 처리
# export GTK_IM_MODULE=ibus
# export QT_IM_MODULE=ibus
# export XMODIFIERS=@im=ibus

# 변경 후
source ~/.bashrc  # 또는 source ~/.zshrc
```

### 3. Cursor 실행 스크립트 확인
```bash
# 실행 스크립트 확인
ls -la ~/bin/cursor*.sh
cat ~/bin/cursor*.sh
```

**되돌리기:**
```bash
# 문제가 되는 스크립트 삭제 또는 이름 변경
mv ~/bin/cursor-korean.sh ~/bin/cursor-korean.sh.backup
```

### 4. Cursor 재시작
```bash
# Cursor 완전 종료
pkill -f cursor

# 환경 변수 없이 재시작
unset GTK_IM_MODULE
unset QT_IM_MODULE
unset XMODIFIERS
cursor
```

## Linux Cursor AI에게 전달할 메시지

```
중요: 설정 변경 후 입력 문제가 발생했습니다.

상황:
- 이전에는 정상 작동했음
- Linux Cursor AI와 작업 후 문제 발생
- 오른쪽 하단 화살표가 계속 켜져 있음
- 영어도 입력이 안 됨

확인 요청:
1. 최근에 변경한 Cursor 설정 파일 내용
   - ~/.config/Cursor/User/settings.json
2. 최근에 추가한 환경 변수
   - .bashrc 또는 .zshrc에 추가한 내용
3. 최근에 생성한 스크립트
   - ~/bin/ 디렉토리의 cursor 관련 스크립트

되돌리기 요청:
1. 변경한 설정을 원래대로 되돌려주세요
2. 또는 변경 사항을 알려주세요 (직접 수정하겠습니다)
3. 기본 설정으로 복원하는 방법을 알려주세요

지금 당장 입력이 안 되어서 작업을 진행할 수 없습니다.
```

## 빠른 해결 방법

### 방법 1: Cursor 설정 파일 초기화
```bash
# 설정 파일 백업
cp ~/.config/Cursor/User/settings.json ~/.config/Cursor/User/settings.json.backup

# 최소 설정으로 시작
cat > ~/.config/Cursor/User/settings.json << EOF
{
  "editor.fontSize": 14
}
EOF

# Cursor 재시작
pkill -f cursor
cursor
```

### 방법 2: 환경 변수 초기화
```bash
# 현재 세션에서만
unset GTK_IM_MODULE
unset QT_IM_MODULE
unset XMODIFIERS

# Cursor 실행
cursor
```

### 방법 3: Cursor 완전 재설치 (최후의 수단)
```bash
# Cursor 완전 제거
rm -rf ~/.config/Cursor
rm -rf ~/.cursor

# 재설치
# (설치 방법은 배포판에 따라 다름)
```

## 확인 체크리스트

1. ✅ Cursor 설정 파일 확인 (`~/.config/Cursor/User/settings.json`)
2. ✅ 환경 변수 확인 (`echo $GTK_IM_MODULE` 등)
3. ✅ .bashrc/.zshrc 확인 (IME 관련 설정)
4. ✅ 실행 스크립트 확인 (`~/bin/cursor*.sh`)
5. ✅ Cursor 재시작 (환경 변수 없이)
