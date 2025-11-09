#!/bin/bash
# 로컬 DB 데이터를 Railway DB로 업로드하는 스크립트

set -e

# 색상
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[✓]${NC} $1"; }
log_warning() { echo -e "${YELLOW}[!]${NC} $1"; }
log_error() { echo -e "${RED}[✗]${NC} $1"; }

# 로컬 DB 설정
LOCAL_DB_HOST="localhost"
LOCAL_DB_NAME="recipe_ai_db"
LOCAL_DB_USER="recipe_keep"
LOCAL_DB_PASSWORD="wkwjsrj4510*"

# Railway DB 설정 (터미널에서 본 정보)
RAILWAY_DB_URL="postgresql://postgres:SwGl5Zv8F0Qv69Pd6qmwQcvqxeBPQAt-@interchange.proxy.rlwy.net:23740/railway"

log_info "=========================================="
log_info "  로컬 DB → Railway DB 업로드"
log_info "=========================================="
log_info ""

# 1. 로컬 DB 데이터 확인
log_info "1️⃣ 로컬 DB 데이터 확인 중..."
export PGPASSWORD="$LOCAL_DB_PASSWORD"
LOCAL_COUNT=$(psql -h "$LOCAL_DB_HOST" -d "$LOCAL_DB_NAME" -U "$LOCAL_DB_USER" -t -c "SELECT COUNT(*) FROM recipes;" 2>/dev/null | tr -d ' ')

if [ -z "$LOCAL_COUNT" ] || [ "$LOCAL_COUNT" -eq 0 ]; then
    log_error "로컬 DB에 레시피 데이터가 없습니다!"
    exit 1
fi

log_success "로컬 DB 레시피 수: ${LOCAL_COUNT}개"
log_info ""

# 2. Railway DB 확인
log_info "2️⃣ Railway DB 연결 확인 중..."
RAILWAY_COUNT=$(psql "$RAILWAY_DB_URL" -t -c "SELECT COUNT(*) FROM recipes;" 2>/dev/null | tr -d ' ')

if [ -z "$RAILWAY_COUNT" ]; then
    log_error "Railway DB 연결 실패!"
    exit 1
fi

log_success "Railway DB 현재 레시피 수: ${RAILWAY_COUNT}개"
log_info ""

# 3. 확인 메시지
if [ "$RAILWAY_COUNT" -gt 0 ]; then
    log_warning "⚠️  Railway DB에 이미 ${RAILWAY_COUNT}개 레시피가 있습니다!"
    read -p "기존 데이터를 삭제하고 새로 업로드하시겠습니까? (y/N): " reset_railway
    if [[ $reset_railway =~ ^[Yy]$ ]]; then
        log_info "Railway DB 초기화 중..."
        psql "$RAILWAY_DB_URL" -c "TRUNCATE recipes CASCADE;" 2>&1 | grep -v "^$" || true
        log_success "Railway DB 초기화 완료"
    else
        log_info "기존 데이터 유지하고 추가 업로드합니다."
    fi
fi

log_info ""

# 4. 데이터 덤프 및 업로드
log_info "3️⃣ 데이터 덤프 및 업로드 중..."
log_warning "⚠️  대용량 데이터라면 시간이 오래 걸릴 수 있습니다!"

# 방법 1: pg_dump + psql (권장)
TEMP_DUMP="/tmp/recipe_dump_$(date +%Y%m%d_%H%M%S).sql"

log_info "로컬 DB 덤프 생성 중..."
export PGPASSWORD="$LOCAL_DB_PASSWORD"
pg_dump -h "$LOCAL_DB_HOST" -U "$LOCAL_DB_USER" -d "$LOCAL_DB_NAME" \
    --no-owner --no-acl \
    --data-only \
    --table=recipes \
    --table=ingredients \
    --table=cooking_steps \
    > "$TEMP_DUMP" 2>&1

if [ $? -ne 0 ]; then
    log_error "덤프 생성 실패!"
    rm -f "$TEMP_DUMP"
    exit 1
fi

DUMP_SIZE=$(du -h "$TEMP_DUMP" | cut -f1)
log_success "덤프 생성 완료 (크기: $DUMP_SIZE)"

log_info ""
log_info "Railway DB에 업로드 중..."
psql "$RAILWAY_DB_URL" < "$TEMP_DUMP" 2>&1 | grep -v "^$" || true

if [ $? -eq 0 ]; then
    log_success "업로드 완료!"
else
    log_error "업로드 실패!"
    rm -f "$TEMP_DUMP"
    exit 1
fi

# 임시 파일 삭제
rm -f "$TEMP_DUMP"

log_info ""

# 5. 최종 확인
log_info "4️⃣ 최종 확인 중..."
FINAL_COUNT=$(psql "$RAILWAY_DB_URL" -t -c "SELECT COUNT(*) FROM recipes;" 2>/dev/null | tr -d ' ')
INGREDIENTS_COUNT=$(psql "$RAILWAY_DB_URL" -t -c "SELECT COUNT(*) FROM ingredients;" 2>/dev/null | tr -d ' ')
STEPS_COUNT=$(psql "$RAILWAY_DB_URL" -t -c "SELECT COUNT(*) FROM cooking_steps;" 2>/dev/null | tr -d ' ')

log_info ""
log_success "=========================================="
log_success "  업로드 완료!"
log_success "=========================================="
log_success "레시피: ${FINAL_COUNT}개"
log_success "재료: ${INGREDIENTS_COUNT}개"
log_success "조리 단계: ${STEPS_COUNT}개"
log_success "=========================================="

log_info ""
log_warning "⚠️  다음 단계: 벡터화가 필요합니다!"
log_info "Railway에서 벡터화를 실행하거나, 로컬에서 벡터화 후 다시 업로드하세요."

