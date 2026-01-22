# Git Push 오류 해결

## 오류: "src refspec main does not match any"

이 오류는 다음 중 하나일 수 있습니다:
1. 현재 브랜치가 `main`이 아님
2. 아직 커밋이 없음

## 해결 방법

### 1단계: 현재 브랜치 확인

```bash
git branch
```

또는

```bash
git status
```

### 2단계: 커밋 확인

```bash
git log
```

커밋이 없다면 먼저 커밋해야 합니다.

### 3단계: 해결 방법

**방법 A: 커밋이 없는 경우**

```bash
# 파일 추가
git add .

# 커밋
git commit -m "Initial commit: Aramed_AI project"

# 브랜치를 main으로 설정
git branch -M main

# 푸시
git push -u origin main
```

**방법 B: 브랜치 이름이 다른 경우**

```bash
# 현재 브랜치 이름 확인
git branch

# 만약 master라면
git branch -M main
git push -u origin main

# 또는 현재 브랜치 이름 그대로 푸시
git push -u origin [현재브랜치이름]
```

**방법 C: 현재 브랜치 그대로 푸시**

```bash
# 현재 브랜치 확인 후
git push -u origin [현재브랜치이름]
```

## 빠른 확인

```bash
# 현재 상태 확인
git status

# 브랜치 확인
git branch

# 커밋 확인
git log --oneline
```
