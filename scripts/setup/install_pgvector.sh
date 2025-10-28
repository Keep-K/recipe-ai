#!/bin/bash
# pgvector 소스 설치 스크립트

set -e

echo "============================================================"
echo "🔧 pgvector 설치 시작"
echo "============================================================"

# PostgreSQL 버전 확인
echo "📌 PostgreSQL 버전 확인..."
psql --version

# 필수 패키지 설치
echo ""
echo "📦 빌드 도구 설치..."
sudo apt-get update
sudo apt-get install -y build-essential postgresql-server-dev-all git

# pgvector 다운로드
echo ""
echo "📥 pgvector 다운로드..."
cd /tmp
rm -rf pgvector
git clone --branch v0.5.1 https://github.com/pgvector/pgvector.git
cd pgvector

# 컴파일
echo ""
echo "🔨 pgvector 컴파일..."
make

# 설치
echo ""
echo "📦 pgvector 설치..."
sudo make install

# 설치 확인
echo ""
echo "✅ pgvector 설치 완료!"
echo ""
echo "============================================================"
echo "🔍 설치 확인"
echo "============================================================"

# DB에 확장 설치
echo "DB에 pgvector 확장 설치 중..."
PGPASSWORD='wkwjsrj4510*' psql -h localhost -d recipe_ai_db -U recipe_keep -c "CREATE EXTENSION IF NOT EXISTS vector;" 2>&1

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ pgvector 설치 및 활성화 성공!"
else
    echo ""
    echo "⚠️  수동으로 확장을 설치하세요:"
    echo "   PGPASSWORD='wkwjsrj4510*' psql -h localhost -d recipe_ai_db -U recipe_keep -c \"CREATE EXTENSION vector;\""
fi

echo ""
echo "============================================================"
echo "✨ 완료! 이제 벡터화를 진행할 수 있습니다."
echo "============================================================"

