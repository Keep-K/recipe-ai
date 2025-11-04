# Railway Docker 배포 가이드

PostgreSQL + pgvector와 FastAPI를 Dockerfile로 Railway에 배포하는 방법입니다.

## 📦 배포 순서

### 1단계: PostgreSQL + pgvector 서비스 배포

#### Railway에서 새 서비스 생성

1. Railway 대시보드 → 프로젝트 선택 → **"New Service"** 클릭
2. **"Deploy from Dockerfile"** 선택
3. **Source**: GitHub 저장소 연결
   - 저장소: `Keep-K/recope-ai` (또는 본인 저장소)
   - **Root Directory**: `recipe_ai_system/docker/postgres`
4. **Service Name**: `postgres` (또는 원하는 이름)

#### 환경 변수 설정

**Variables** 탭에서 추가:
```
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_secure_password_here
POSTGRES_DB=railway
```

#### 배포

- Railway가 자동으로 빌드 및 배포 시작
- 배포 완료까지 약 5-10분 소요

#### 연결 정보 확인

배포 완료 후:
1. **Connect** 탭 → **"Postgres"** 클릭
2. 연결 정보 복사:
   ```
   postgresql://postgres:password@hostname:port/railway
   ```
3. 또는 **Variables** 탭에서 `DATABASE_URL` 확인

---

### 2단계: FastAPI 서비스 배포

#### Railway에서 새 서비스 생성

1. 같은 프로젝트에서 **"New Service"** 클릭
2. **"Deploy from Dockerfile"** 선택
3. **Source**: 같은 GitHub 저장소
   - **Root Directory**: `recipe_ai_system`
4. **Service Name**: `api` (또는 원하는 이름)

#### 환경 변수 설정

**Variables** 탭에서 추가:

1. **DATABASE_URL**: PostgreSQL 서비스의 연결 정보
   - 방법 A: PostgreSQL 서비스의 `DATABASE_URL` 변수 값을 그대로 복사
   - 방법 B: 내부 네트워크 사용 시:
     ```
     DATABASE_URL=postgresql://postgres:password@postgres:5432/railway
     ```
     (여기서 `postgres`는 PostgreSQL 서비스 이름)

2. **OPENAI_API_KEY**: OpenAI API 키
   ```
   OPENAI_API_KEY=sk-your-openai-key-here
   ```

#### 배포

- Railway가 자동으로 빌드 및 배포 시작
- 배포 완료까지 약 3-5분 소요

---

### 3단계: 테스트

#### PostgreSQL 연결 테스트

```bash
# Railway CLI 사용
railway connect postgres

# 또는 직접 연결
psql $DATABASE_URL

# pgvector 확장 확인
\dx vector

# 테이블 확인
\dt
```

#### FastAPI 헬스 체크

```bash
# Railway가 제공하는 URL 확인 (서비스의 Settings 탭)
curl https://your-api-service.up.railway.app/health

# 또는 Railway CLI
railway run curl http://localhost:$PORT/health
```

---

## 🔧 문제 해결

### PostgreSQL 배포 실패

**증상**: `pgvector` 설치 실패

**해결**:
1. Dockerfile에서 PostgreSQL 버전 확인 (17 사용 중)
2. 빌드 로그에서 오류 확인
3. 필요 시 `docker/postgres/Dockerfile` 수정

### FastAPI에서 DB 연결 실패

**증상**: `connection refused` 또는 `relation does not exist`

**해결**:
1. `DATABASE_URL` 확인:
   ```bash
   railway variables --service api
   ```
2. PostgreSQL 서비스가 실행 중인지 확인
3. 내부 네트워크 사용 시 서비스 이름 확인:
   - PostgreSQL 서비스 이름이 `postgres`인지 확인
   - `DATABASE_URL`에서 호스트명을 서비스 이름으로 변경

### 포트 에러

**증상**: `Option '--port' requires an argument`

**해결**:
- Dockerfile에서 `${PORT:-8000}` 형식 사용 (이미 적용됨)
- Railway가 자동으로 `$PORT` 환경 변수 설정

---

## 📝 추가 설정

### PostgreSQL 서비스 이름 변경 시

만약 PostgreSQL 서비스 이름을 `postgres`가 아닌 다른 이름으로 설정했다면:

1. FastAPI 서비스의 `DATABASE_URL`에서 호스트명 변경
2. 예: 서비스 이름이 `recipe-db`인 경우
   ```
   DATABASE_URL=postgresql://postgres:password@recipe-db:5432/railway
   ```

### 로컬에서 테스트

```bash
# PostgreSQL 테스트
cd recipe_ai_system/docker/postgres
docker build -t recipe-postgres .
docker run -d -p 5432:5432 \
  -e POSTGRES_PASSWORD=testpass \
  -e POSTGRES_DB=recipe_ai \
  recipe-postgres

# FastAPI 테스트
cd recipe_ai_system
docker build -t recipe-api .
docker run -d -p 8000:8000 \
  -e DATABASE_URL=postgresql://postgres:testpass@host.docker.internal:5432/recipe_ai \
  -e OPENAI_API_KEY=your_key \
  recipe-api
```

---

## ✅ 체크리스트

배포 전:
- [ ] GitHub 저장소에 코드 푸시 완료
- [ ] PostgreSQL Dockerfile 확인
- [ ] FastAPI Dockerfile 확인

PostgreSQL 배포:
- [ ] 서비스 생성 및 Root Directory 설정
- [ ] 환경 변수 설정 (POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB)
- [ ] 배포 완료 확인
- [ ] DATABASE_URL 확인

FastAPI 배포:
- [ ] 서비스 생성 및 Root Directory 설정
- [ ] DATABASE_URL 환경 변수 설정
- [ ] OPENAI_API_KEY 환경 변수 설정
- [ ] 배포 완료 확인
- [ ] /health 엔드포인트 테스트

---

## 🚀 다음 단계

배포가 완료되면:
1. `/health` 엔드포인트로 서버 상태 확인
2. `/search` 엔드포인트로 레시피 검색 테스트
3. Firebase 프론트엔드에서 `VITE_API_BASE_URL` 업데이트

