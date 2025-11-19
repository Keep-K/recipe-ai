# FastAPI Application Dockerfile for Railway
FROM python:3.11.14-slim

# 작업 디렉토리 설정
WORKDIR /app

# 시스템 의존성 설치
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Python 의존성 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY . .

# 환경 변수 설정
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# 포트 노출 (Railway가 $PORT 환경 변수 사용)
EXPOSE $PORT

# FastAPI 서버 실행
CMD sh -c 'uvicorn api_server:app --host 0.0.0.0 --port ${PORT:-8000}'

