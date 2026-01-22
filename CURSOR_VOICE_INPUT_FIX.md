# Cursor 음성 입력 문제 해결

## 문제 증상
- Cursor 채팅창에서 마이크 아이콘이 불이 들어옴
- 한글 입력이 사라짐 (키보드 입력이 차단됨)
- 음성 입력 모드가 실수로 활성화됨

## 해결 방법

### 방법 1: 음성 입력 비활성화 (가장 빠름)

**단축키:**
- `Esc` 키 누르기
- 또는 마이크 아이콘 클릭하여 비활성화

### 방법 2: Cursor 설정에서 음성 입력 비활성화

**설정 파일 수정:**
```bash
# Cursor 설정 파일 열기
~/.config/Cursor/User/settings.json
```

**추가할 설정:**
```json
{
  "cursor.chat.voiceInput.enabled": false,
  "cursor.chat.voiceInput.autoActivate": false
}
```

### 방법 3: 단축키 변경

음성 입력 단축키가 실수로 눌리는 경우:
- 설정에서 음성 입력 단축키를 변경하거나 비활성화

### 방법 4: Cursor 재시작

```bash
# Cursor 완전 종료
pkill -f cursor

# 재시작
cursor
```

## Linux Cursor AI에게 전달할 메시지

```
Cursor 채팅창에서 마이크 아이콘이 활성화되면서 한글 입력이 사라지는 문제가 있습니다.

증상:
- 채팅창 마이크 아이콘이 불이 들어옴
- 한글 입력이 사라짐
- 키보드 입력이 차단됨

해결 방법:
1. Esc 키로 음성 입력 모드 종료
2. 마이크 아이콘 클릭하여 비활성화
3. Cursor 설정에서 음성 입력 기능 비활성화
   - settings.json에 "cursor.chat.voiceInput.enabled": false 추가

음성 입력 기능을 완전히 비활성화하는 방법을 알려주세요.
```

## 빠른 해결

**지금 당장:**
1. `Esc` 키 누르기
2. 마이크 아이콘 클릭하여 끄기

**영구 해결:**
- Cursor 설정에서 음성 입력 기능 비활성화
