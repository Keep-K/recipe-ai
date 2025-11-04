# Railway Dockerfile 배포 설정 가이드

## 현재 문제
Railway가 `docker/postgres/Dockerfile`을 찾지 못합니다.

## 해결 방법

### 방법 1: Root Directory + Dockerfile 경로 명시 (권장)

Railway PostgreSQL 서비스의 **Settings** 탭:

1. **Root Directory**: `docker/postgres`
2. **Dockerfile Path**: `Dockerfile` (또는 비워두기)
   - ⚠️ `docker/postgres/Dockerfile`이 아님! Root Directory가 `docker/postgres`이므로 `Dockerfile`만 지정

### 방법 2: Root Directory 비우기 + 전체 경로

1. **Root Directory**: `.` (또는 비워두기)
2. **Dockerfile Path**: `docker/postgres/Dockerfile`

### 방법 3: Railway CLI로 확인

```bash
railway status
railway variables
```

## Railway 설정 확인 체크리스트

- [ ] GitHub 저장소 연결됨: `Keep-K/recope-ai`
- [ ] Root Directory 설정 확인
- [ ] Dockerfile Path 설정 확인
- [ ] 환경 변수 설정:
  - [ ] `POSTGRES_USER=postgres`
  - [ ] `POSTGRES_PASSWORD=your_password`
  - [ ] `POSTGRES_DB=railway`

## 중요 참고사항

Railway의 Root Directory 동작:
- Root Directory가 `docker/postgres`면 → 그 디렉토리가 빌드 컨텍스트
- Dockerfile은 그 디렉토리 안에 있어야 함
- Dockerfile Path는 상대 경로 (Root Directory 기준)

## 문제 해결

여전히 오류가 발생하면:
1. Railway 서비스를 삭제하고 새로 생성
2. 또는 Settings → Clear Build Cache
3. GitHub에 최신 코드가 푸시되었는지 확인


