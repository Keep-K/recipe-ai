# Railway 배포 문제 해결

## 현재 문제
Railway가 `docker/postgres/Dockerfile`을 찾지 못합니다.

## 해결 방법

### 1. GitHub에 푸시 (필수)

```bash
cd /home/keep/recipe-ai/recipe_ai_system
git push
```

### 2. Railway Root Directory 설정 확인

Railway PostgreSQL 서비스의 **Settings** 탭에서:

**옵션 A: Root Directory를 `docker/postgres`로 설정**
- 이 경우 Railway는 `Dockerfile`을 직접 찾습니다 (같은 디렉토리)
- ✅ 권장 방법

**옵션 B: Root Directory를 비워두거나 `.`로 설정**
- 이 경우 Railway는 `docker/postgres/Dockerfile`을 찾습니다
- ❌ 현재 오류 발생

### 3. Railway 설정 확인 단계

1. Railway 대시보드 → PostgreSQL 서비스 선택
2. **Settings** 탭 클릭
3. **Root Directory** 필드 확인:
   - 올바른 값: `docker/postgres` (또는 `docker/postgres/`)
   - 잘못된 값: 비어있음, `.`, `recipe_ai_system/docker/postgres`
4. 수정 후 **Save** 클릭
5. **Deployments** 탭 → **Redeploy** 클릭

### 4. 확인 사항

재배포 후 로그에서 다음을 확인:
- ✅ `[internal] load build definition from Dockerfile`
- ✅ `[4/4] COPY ./init-db.sql /docker-entrypoint-initdb.d/01-init-schema.sql`

### 5. 여전히 오류가 발생하면

Railway가 캐시를 사용하고 있을 수 있습니다:
1. **Settings** → **Clear Build Cache** 클릭 (있는 경우)
2. 또는 **Deployments** → 이전 배포 삭제 → 새로 배포

## 중요 참고사항

GitHub 저장소 구조:
```
recipe_ai_system/          <- 저장소 루트
  docker/
    postgres/
      Dockerfile           <- 여기에 있음
      init-db.sql
```

따라서 Root Directory는 `docker/postgres`여야 합니다.


