# Linux Cursor 재설치 가이드

## 오늘 발생한 문제 요약
- 처음 Linux 시작 시에는 정상 작동
- Windows-Linux 연결 작업 후 입력 문제 발생
- 오른쪽 하단 화살표가 계속 켜져 있음
- 영어도 입력이 안 됨
- IME 입력 모드가 활성화되어 입력이 제대로 처리되지 않음
- 결국 Cursor 삭제 후 내일 재설치 예정

## 내일 재설치 시 주의사항

### 1. Cursor 설치 후 즉시 확인할 사항

**설치 직후:**
```bash
# Cursor 실행
cursor

# 입력 테스트
# - 채팅창에서 영어 입력 테스트
# - 한글 입력 테스트
# - 오른쪽 하단 화살표 확인
```

### 2. 환경 변수 설정 주의

**설치 직후에는 환경 변수를 설정하지 마세요!**
- 기본 설정으로 먼저 테스트
- 입력이 정상 작동하는지 확인
- 문제가 없을 때만 필요한 설정 추가

**확인 명령어:**
```bash
# 현재 환경 변수 확인
echo $GTK_IM_MODULE
echo $QT_IM_MODULE
echo $XMODIFIERS

# 비어있어야 정상 (설치 직후)
```

### 3. Windows-Linux 연결 작업 시 주의

**연결 작업 전:**
1. Cursor 입력이 정상 작동하는지 확인
2. Git 설정만 변경 (IME 관련 설정은 건드리지 않기)
3. 환경 변수는 프로젝트 경로(`MATHPDF_PATH`)만 설정

**연결 작업 후:**
1. 즉시 입력 테스트
2. 문제 발생 시 즉시 되돌리기
3. IME 관련 설정은 절대 추가하지 않기

### 4. 안전한 설정 순서

**1단계: Cursor 기본 설치 및 테스트**
```bash
# Cursor 설치
# (배포판에 따라 다름)

# 기본 실행 및 테스트
cursor
# → 입력 정상 작동 확인
```

**2단계: 프로젝트 설정 (필요시)**
```bash
# 프로젝트 경로 환경 변수만 설정
export MATHPDF_PATH=/path/to/MathPDF/organized
# 또는 .env 파일 사용
```

**3단계: Git 설정 (필요시)**
```bash
# Git 설정만 변경
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

**4단계: IME 관련 설정은 하지 않기**
- `GTK_IM_MODULE`, `QT_IM_MODULE`, `XMODIFIERS` 설정하지 않기
- Cursor 실행 스크립트에 IME 관련 설정 추가하지 않기
- `.bashrc` 또는 `.zshrc`에 IME 관련 설정 추가하지 않기

### 5. 문제 발생 시 즉시 조치

**입력 문제 발생 시:**
```bash
# 1. Cursor 종료
pkill -f cursor

# 2. 환경 변수 확인 및 제거
unset GTK_IM_MODULE
unset QT_IM_MODULE
unset XMODIFIERS

# 3. Cursor 재시작
cursor
```

**여전히 문제가 있으면:**
```bash
# Cursor 설정 파일 확인
cat ~/.config/Cursor/User/settings.json

# 최소 설정으로 초기화
cat > ~/.config/Cursor/User/settings.json << 'EOF'
{
  "editor.fontSize": 14
}
EOF

# 재시작
pkill -f cursor
cursor
```

### 6. 권장 설치 방법

**Ubuntu/Debian:**
```bash
# 공식 설치 방법 사용
# IME 관련 설정은 하지 않기
```

**설치 후 확인:**
- [ ] Cursor 실행 확인
- [ ] 영어 입력 테스트
- [ ] 한글 입력 테스트 (정상 작동 시)
- [ ] 오른쪽 하단 화살표 없음 확인
- [ ] 채팅창 입력 정상 확인

### 7. Windows-Linux 연결 작업 체크리스트

**작업 전:**
- [ ] Cursor 입력 정상 작동 확인
- [ ] Git 설치 확인
- [ ] 프로젝트 경로 확인

**작업 중:**
- [ ] Git 설정만 변경
- [ ] 환경 변수는 `MATHPDF_PATH`만 설정
- [ ] IME 관련 설정은 절대 추가하지 않기

**작업 후:**
- [ ] 즉시 입력 테스트
- [ ] 문제 발생 시 즉시 되돌리기

### 8. 참고 문서

- `MESSAGE_FOR_LINUX_CURSOR.md`: Linux Cursor AI에게 전달할 메시지
- `LINUX_CONNECTION_ROLLBACK.md`: 연결 작업 후 문제 해결
- `CURSOR_IME_FIX.md`: IME 입력 문제 해결
- `CURSOR_SETTINGS_ROLLBACK.md`: 설정 되돌리기

## 핵심 원칙

1. **설치 직후 기본 설정으로 테스트**
2. **IME 관련 설정은 절대 추가하지 않기**
3. **문제 발생 시 즉시 되돌리기**
4. **Windows-Linux 연결 작업은 최소한의 설정만**

## 내일 작업 순서

1. Cursor 재설치
2. 기본 실행 및 입력 테스트
3. 정상 작동 확인 후 프로젝트 작업 시작
4. Windows-Linux 연결 작업 시 주의 깊게 진행

---

**행운을 빕니다! 내일은 문제없이 작동하기를 바랍니다.**
