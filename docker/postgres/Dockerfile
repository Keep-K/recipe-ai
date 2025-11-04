# PostgreSQL 17 with pgvector extension
FROM postgres:17

# pgvector 설치를 위한 빌드 의존성
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    postgresql-server-dev-17 \
    && rm -rf /var/lib/apt/lists/*

# pgvector 설치
RUN cd /tmp && \
    git clone --branch v0.7.2 https://github.com/pgvector/pgvector.git && \
    cd pgvector && \
    make && \
    make install && \
    cd .. && \
    rm -rf pgvector

# 초기화 스크립트 복사
COPY init-db.sql /docker-entrypoint-initdb.d/01-init-schema.sql

# 포트 노출
EXPOSE 5432

