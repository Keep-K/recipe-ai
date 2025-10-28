#!/bin/bash

# Recipe AI - 전체 자동화 스크립트
# 이 스크립트는 초기 설정부터 벡터화까지 모든 과정을 자동으로 실행합니다.

set -e  # 에러 발생 시 중단

# 색상 정의
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 스크립트 디렉토리
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo ""
echo "============================================================"
echo -e "${BLUE}🚀 Recipe AI 전체 자동화 시작${NC}"
echo "============================================================"
echo ""
echo "📁 프로젝트 경로: $PROJECT_ROOT"
echo ""

# 진행 상황 표시 함수
print_step() {
    echo ""
    echo "============================================================"
    echo -e "${YELLOW}📌 $1${NC}"
    echo "============================================================"
    echo ""
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Step 1: PostgreSQL 시작
print_step "Step 1: PostgreSQL 시작"

if pg_isready -h localhost -p 5432 > /dev/null 2>&1; then
    print_success "PostgreSQL이 이미 실행 중입니다"
else
    echo "PostgreSQL을 시작합니다..."
    sudo service postgresql start
    
    # 시작 대기
    sleep 2
    
    if pg_isready -h localhost -p 5432 > /dev/null 2>&1; then
        print_success "PostgreSQL 시작 완료"
    else
        print_error "PostgreSQL 시작 실패"
        exit 1
    fi
fi

# Step 2: pgvector 설치 확인 및 설치
print_step "Step 2: pgvector 확장 설치"

if [ -f "$SCRIPT_DIR/setup/install_pgvector.sh" ]; then
    echo "pgvector 설치 스크립트 실행 중..."
    bash "$SCRIPT_DIR/setup/install_pgvector.sh"
else
    print_error "install_pgvector.sh를 찾을 수 없습니다"
    exit 1
fi

# Step 3: 벡터 컬럼 추가
print_step "Step 3: 벡터 컬럼 추가"

if [ -f "$SCRIPT_DIR/database/add_vector_column.sh" ]; then
    echo "벡터 컬럼 추가 중..."
    bash "$SCRIPT_DIR/database/add_vector_column.sh"
else
    print_error "add_vector_column.sh를 찾을 수 없습니다"
    exit 1
fi

# Step 4: Python 가상환경 확인
print_step "Step 4: Python 환경 설정"

cd "$PROJECT_ROOT"

if [ ! -d "venv" ]; then
    echo "Python 가상환경 생성 중..."
    python3 -m venv venv
    print_success "가상환경 생성 완료"
else
    print_success "가상환경이 이미 존재합니다"
fi

# 가상환경 활성화
echo "가상환경 활성화 중..."
source venv/bin/activate

# Step 5: Python 패키지 설치
print_step "Step 5: Python 패키지 설치"

if [ -f "requirements.txt" ]; then
    echo "필수 패키지 설치 중..."
    pip install --upgrade pip > /dev/null 2>&1
    pip install -r requirements.txt
    
    # 벡터화 관련 추가 패키지
    echo ""
    echo "벡터화 관련 패키지 설치 중..."
    pip install openai sentence-transformers pgvector psycopg2-binary
    
    print_success "패키지 설치 완료"
else
    print_error "requirements.txt를 찾을 수 없습니다"
fi

# Step 6: 환경 확인
print_step "Step 6: 환경 확인"

echo "📊 시스템 상태 확인:"
echo ""

# PostgreSQL 상태
echo -n "PostgreSQL: "
if pg_isready -h localhost -p 5432 > /dev/null 2>&1; then
    echo -e "${GREEN}✅ 실행 중${NC}"
else
    echo -e "${RED}❌ 중지됨${NC}"
fi

# pgvector 확장
echo -n "pgvector: "
if psql -h localhost -d recipe_ai_db -U recipe_keep -c "\dx vector" 2>/dev/null | grep -q vector; then
    echo -e "${GREEN}✅ 설치됨${NC}"
else
    echo -e "${RED}❌ 미설치${NC}"
fi

# 벡터 컬럼
echo -n "벡터 컬럼: "
if psql -h localhost -d recipe_ai_db -U recipe_keep -c "\d recipes" 2>/dev/null | grep -q embedding; then
    echo -e "${GREEN}✅ 추가됨${NC}"
else
    echo -e "${RED}❌ 미추가${NC}"
fi

# Python 환경
echo -n "Python 가상환경: "
if [ -n "$VIRTUAL_ENV" ]; then
    echo -e "${GREEN}✅ 활성화됨${NC}"
else
    echo -e "${YELLOW}⚠️  비활성화됨${NC}"
fi

# 레시피 수
echo -n "레시피 수: "
RECIPE_COUNT=$(psql -h localhost -d recipe_ai_db -U recipe_keep -t -c "SELECT COUNT(*) FROM recipes;" 2>/dev/null | xargs)
if [ -n "$RECIPE_COUNT" ]; then
    echo -e "${GREEN}$RECIPE_COUNT개${NC}"
else
    echo -e "${YELLOW}0개${NC}"
fi

# 벡터화된 레시피 수
echo -n "벡터화된 레시피: "
VECTORIZED_COUNT=$(psql -h localhost -d recipe_ai_db -U recipe_keep -t -c "SELECT COUNT(*) FROM recipes WHERE embedding IS NOT NULL;" 2>/dev/null | xargs)
if [ -n "$VECTORIZED_COUNT" ]; then
    echo -e "${GREEN}$VECTORIZED_COUNT개${NC}"
else
    echo -e "${YELLOW}0개${NC}"
fi

# 최종 요약
echo ""
echo "============================================================"
echo -e "${GREEN}✅ 전체 자동화 완료!${NC}"
echo "============================================================"
echo ""
echo "🎯 다음 단계:"
echo ""
echo "1. 레시피 수집 (아직 안했다면):"
echo "   ./scripts/utils/run_batch_collection.sh"
echo ""
echo "2. 레시피 벡터화:"
echo "   python vectorize_recipes.py"
echo ""
echo "3. 레시피 검색 테스트:"
echo "   python search_recipes.py '닭가슴살 요리'"
echo ""
echo "4. 진행 상황 확인:"
echo "   ./scripts/utils/check_progress.sh"
echo ""
echo "============================================================"
echo ""

