# PostgreSQL + pgvector Dockerfile for Railway

Railway에 PostgreSQL + pgvector를 배포하기 위한 Dockerfile입니다.

## 사용 방법

### 1. Railway에서 새 서비스 생성

1. Railway 대시보드에서 **"New Project"** 또는 기존 프로젝트에 **"New Service"** 클릭
2. **"Deploy from Dockerfile"** 선택
3. GitHub 저장소 연결: `https://github.com/Keep-K/recope-ai.git`
4. **Root Directory**: `docker/postgres` (⚠️ 중요: `recipe_ai_system/docker/postgres`가 아님!)

### 2. 환경 변수 설정

Railway 서비스의 **Variables** 탭에서 다음 변수 설정:

```
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_secure_password_here
POSTGRES_DB=railway
```

### 3. 배포

Railway가 자동으로 Dockerfile을 빌드하고 배포합니다.

### 4. 연결 정보 확인

배포 완료 후 Railway 서비스의 **Connect** 탭에서 연결 정보 확인:
- `DATABASE_URL` 형식: `postgresql://postgres:password@hostname:port/railway`

### 5. FastAPI 서비스에 연결

FastAPI 서비스의 환경 변수에 `DATABASE_URL` 추가:
```
DATABASE_URL=postgresql://postgres:password@hostname:port/railway
```

## 로컬 테스트

```bash
# Docker 이미지 빌드
cd docker/postgres
docker build -t recipe-postgres:latest .

# 컨테이너 실행
docker run -d \
  --name recipe-postgres \
  -e POSTGRES_PASSWORD=testpass \
  -e POSTGRES_DB=recipe_ai \
  -p 5432:5432 \
  recipe-postgres:latest

# 연결 테스트
psql -h localhost -U postgres -d recipe_ai -c "SELECT * FROM recipes LIMIT 1;"
```

## 주의사항

- Railway의 PostgreSQL 서비스는 기본적으로 `railway` 데이터베이스를 사용합니다
- 비밀번호는 반드시 강력한 것으로 설정하세요
- `DATABASE_URL`은 Railway가 자동으로 생성하는 환경 변수를 사용할 수 있습니다

