#!/bin/bash

echo "============================================================"
echo "🚀 레시피 벡터 컬럼 추가 마이그레이션"
echo "============================================================"
echo ""

# 색상 정의
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# PostgreSQL 연결 정보
DB_NAME="recipe_ai_db"
DB_USER="recipe_keep"
MIGRATION_FILE="/home/keep/recipe-ai/recipe_ai_system/db/migrations/001_add_vector_column.sql"

# Step 1: PostgreSQL 상태 확인
echo "📌 Step 1: PostgreSQL 상태 확인"
if pg_isready -h localhost -p 5432 > /dev/null 2>&1; then
    echo -e "${GREEN}✅ PostgreSQL이 실행 중입니다${NC}"
else
    echo -e "${RED}❌ PostgreSQL이 실행되지 않습니다${NC}"
    echo "실행 명령어: sudo service postgresql start"
    exit 1
fi
echo ""

# Step 2: pgvector 확장 확인
echo "📌 Step 2: pgvector 확장 설치 확인"
if psql -h localhost -d "$DB_NAME" -U "$DB_USER" -c "SELECT * FROM pg_available_extensions WHERE name = 'vector';" -t | grep -q vector; then
    echo -e "${GREEN}✅ pgvector 확장이 설치되어 있습니다${NC}"
else
    echo -e "${RED}❌ pgvector 확장이 설치되지 않았습니다${NC}"
    echo "설치 명령어: ./install_pgvector.sh"
    exit 1
fi
echo ""

# Step 3: 마이그레이션 파일 확인
echo "📌 Step 3: 마이그레이션 파일 확인"
if [ ! -f "$MIGRATION_FILE" ]; then
    echo -e "${RED}❌ 마이그레이션 파일을 찾을 수 없습니다: $MIGRATION_FILE${NC}"
    exit 1
else
    echo -e "${GREEN}✅ 마이그레이션 파일 발견${NC}"
fi
echo ""

# Step 4: 현재 테이블 구조 확인
echo "📌 Step 4: 현재 recipes 테이블 구조"
psql -h localhost -d "$DB_NAME" -U "$DB_USER" -c "\d recipes" 2>/dev/null | head -20
echo ""

# Step 5: 마이그레이션 실행
echo "============================================================"
echo "🔧 벡터 컬럼 추가 실행 중..."
echo "============================================================"
echo ""

psql -h localhost -d "$DB_NAME" -U "$DB_USER" -f "$MIGRATION_FILE"

if [ $? -eq 0 ]; then
    echo ""
    echo "============================================================"
    echo -e "${GREEN}✅ 마이그레이션 완료!${NC}"
    echo "============================================================"
    echo ""
    
    # Step 6: 결과 확인
    echo "📊 업데이트된 테이블 구조:"
    psql -h localhost -d "$DB_NAME" -U "$DB_USER" -c "\d recipes" 2>/dev/null | grep -A 20 "Column"
    echo ""
    
    echo "📊 인덱스 확인:"
    psql -h localhost -d "$DB_NAME" -U "$DB_USER" -c "\di idx_recipes_embedding" 2>/dev/null
    echo ""
    
    echo "============================================================"
    echo "🎯 다음 단계:"
    echo "============================================================"
    echo "1. Python 의존성 설치:"
    echo "   pip install openai sentence-transformers pgvector psycopg2-binary"
    echo ""
    echo "2. 벡터화 스크립트 작성:"
    echo "   src/vectorizer.py"
    echo ""
    echo "3. 레시피 벡터화 실행:"
    echo "   python src/vectorizer.py"
    echo "============================================================"
else
    echo ""
    echo -e "${RED}❌ 마이그레이션 실패${NC}"
    exit 1
fi

