# Docker 배포 가이드

Railway에서 Dockerfile을 사용하여 배포하는 방법입니다.

## 구조

```
docker/
├── postgres/          # PostgreSQL + pgvector Dockerfile
│   ├── Dockerfile
│   ├── init-db.sql
│   └── README.md
└── README.md          # 이 파일

recipe_ai_system/
├── Dockerfile         # FastAPI 앱 Dockerfile
└── ...
```

## 배포 방법

### 방법 1: Railway UI에서 배포

#### PostgreSQL 서비스 배포

1. Railway 대시보드 → **New Service** → **Deploy from Dockerfile**
2. **Source**: GitHub 저장소 연결 또는 로컬 디렉토리
3. **Root Directory**: `recipe_ai_system/docker/postgres`
4. **Environment Variables**:
   ```
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=your_secure_password
   POSTGRES_DB=railway
   ```
5. 배포 완료 후 **Connect** 탭에서 `DATABASE_URL` 확인

#### FastAPI 서비스 배포

1. Railway 대시보드 → **New Service** → **Deploy from Dockerfile**
2. **Source**: GitHub 저장소 연결 또는 로컬 디렉토리
3. **Root Directory**: `recipe_ai_system`
4. **Environment Variables**:
   ```
   DATABASE_URL=postgresql://postgres:password@postgres-service:5432/railway
   OPENAI_API_KEY=your_openai_key
   ```
5. 배포 완료

### 방법 2: Railway CLI로 배포

```bash
# PostgreSQL 배포
cd recipe_ai_system/docker/postgres
railway up --dockerfile Dockerfile

# FastAPI 배포
cd recipe_ai_system
railway up --dockerfile Dockerfile
```

## 서비스 연결

Railway에서 두 서비스를 같은 프로젝트에 배포하면:
- PostgreSQL 서비스의 내부 호스트명: `postgres-service` (서비스 이름)
- FastAPI에서 `DATABASE_URL`을 `postgres-service`로 설정

## 로컬 테스트

### PostgreSQL 테스트
```bash
cd docker/postgres
docker build -t recipe-postgres .
docker run -d -p 5432:5432 \
  -e POSTGRES_PASSWORD=testpass \
  recipe-postgres
```

### FastAPI 테스트
```bash
cd recipe_ai_system
docker build -t recipe-api .
docker run -d -p 8000:8000 \
  -e DATABASE_URL=postgresql://postgres:testpass@host.docker.internal:5432/railway \
  -e OPENAI_API_KEY=your_key \
  recipe-api
```

## 주의사항

1. **포트**: Railway는 `$PORT` 환경 변수를 사용합니다. Dockerfile에서 `${PORT:-8000}` 형식으로 기본값 설정
2. **DATABASE_URL**: Railway 내부 네트워크에서는 서비스 이름으로 연결 가능
3. **환경 변수**: 민감한 정보는 Railway Variables에 저장

