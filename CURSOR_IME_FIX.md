# Cursor IME 입력 문제 해결 (오른쪽 하단 화살표)

## 문제 증상
- 오른쪽 하단에 화살표가 계속 켜져 있음
- 영어도 입력이 안 됨
- 한 글자 이상 타이핑이 안 되고, 알파벳만 바뀜
- IME(입력기)가 활성화되어 입력이 제대로 처리되지 않음

## 즉시 해결 방법

### 방법 1: 한영 전환 키 (가장 빠름)
- **Right Alt** 키 누르기
- 또는 **Space + Shift** (설정에 따라 다름)
- 또는 **한영 전환 키** (키보드에 따라 다름)

### 방법 2: Enter 키로 입력 확정
- 타이핑 후 **Enter** 키를 눌러 입력 확정
- IME 입력 모드에서 입력을 확정하지 않으면 글자가 바뀌기만 함

### 방법 3: Esc 키로 입력 취소 후 재시도
- **Esc** 키로 현재 입력 취소
- 다시 타이핑

## 영구 해결 방법

### 방법 1: Cursor를 IME 없이 실행

**스크립트 생성:**
```bash
# ~/bin/cursor-no-ime.sh 생성
#!/bin/bash
unset GTK_IM_MODULE
unset QT_IM_MODULE
unset XMODIFIERS
/usr/bin/cursor "$@"

# 실행 권한 부여
chmod +x ~/bin/cursor-no-ime.sh
```

**실행:**
```bash
~/bin/cursor-no-ime.sh
```

### 방법 2: 환경 변수로 IME 비활성화

**터미널에서:**
```bash
# IME 환경 변수 제거
unset GTK_IM_MODULE
unset QT_IM_MODULE
unset XMODIFIERS

# Cursor 실행
cursor
```

**영구 설정 (.bashrc 또는 .zshrc에 추가):**
```bash
# Cursor 전용 IME 비활성화 함수
cursor-no-ime() {
    unset GTK_IM_MODULE
    unset QT_IM_MODULE
    unset XMODIFIERS
    cursor "$@"
}

# 사용: cursor-no-ime
```

### 방법 3: Cursor 설정에서 IME 비활성화

**설정 파일:**
```bash
~/.config/Cursor/User/settings.json
```

**추가할 설정:**
```json
{
  "editor.quickSuggestions": {
    "other": true,
    "comments": false,
    "strings": false
  },
  "editor.acceptSuggestionOnCommitCharacter": false,
  "editor.acceptSuggestionOnEnter": "on"
}
```

### 방법 4: IME 입력기 완전 비활성화

**ibus 비활성화:**
```bash
# ibus 데몬 종료
ibus exit

# 자동 시작 비활성화
# ~/.config/autostart/ibus.desktop 삭제 또는 수정
```

## Linux Cursor AI에게 전달할 메시지

```
중요한 문제입니다! Cursor 채팅창에서 입력이 전혀 안 됩니다.

증상:
- 오른쪽 하단에 화살표가 계속 켜져 있음
- 영어도 입력이 안 됨
- 한 글자 이상 타이핑이 안 되고, 알파벳만 바뀜
- IME(입력기)가 활성화되어 입력이 제대로 처리되지 않는 것 같음

시도한 것:
- 한영 전환 키 (Right Alt, Space+Shift 등)
- Enter 키로 입력 확정
- Esc 키로 입력 취소

필요한 해결:
1. IME를 완전히 비활성화하여 Cursor를 실행하는 방법
2. Cursor 설정에서 IME 관련 설정 변경
3. 환경 변수로 IME 비활성화하는 방법

지금 당장 입력이 안 되어서 작업을 진행할 수 없습니다.
빠른 해결 방법을 알려주세요!
```

## 빠른 해결 체크리스트

1. ✅ **Right Alt** 키 눌러보기
2. ✅ **Space + Shift** 눌러보기
3. ✅ 타이핑 후 **Enter** 키 눌러보기
4. ✅ **Esc** 키로 입력 취소 후 재시도
5. ✅ Cursor 재시작 (IME 환경 변수 없이)

## 참고

- 오른쪽 하단 화살표는 IME 입력 모드 표시
- IME가 활성화되면 입력이 완료되지 않고 글자만 바뀜
- Cursor는 Electron 기반이라 IME와 충돌할 수 있음
