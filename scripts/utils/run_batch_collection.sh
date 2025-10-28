#!/bin/bash
# 1000개 레시피 자동 수집 스크립트

set -e  # 에러 발생 시 중단

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# 색상
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 로그 함수
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

log_error() {
    echo -e "${RED}[✗]${NC} $1"
}

# 환경 체크
if [ ! -f "config/.env" ]; then
    log_error "config/.env not found!"
    exit 1
fi

if [ ! -d "venv" ]; then
    log_error "venv not found! Run: python -m venv venv"
    exit 1
fi

# Virtual env 활성화
source venv/bin/activate

# DB 초기화 확인
read -p "DB를 초기화하고 시작하시겠습니까? (y/N): " reset_db
if [[ $reset_db =~ ^[Yy]$ ]]; then
    log_info "DB 초기화 중..."
    PGPASSWORD='wkwjsrj4510*' psql -h localhost -d recipe_ai_db -U recipe_keep -c "TRUNCATE recipes CASCADE;" 2>&1 | grep -v "^$"
    log_success "DB 초기화 완료"
fi

# 수집 설정 배열
declare -a COLLECTIONS=(
    # Phase 1: 메인 단백질 (400개)
    "1-1:소고기볶음:밑반찬:일상:소고기:볶음:50"
    "1-2:소고기구이:밑반찬:일상:소고기:구이:50"
    "1-3:돼지고기볶음:밑반찬:일상:돼지고기:볶음:50"
    "1-4:돼지고기찜:밑반찬:일상:돼지고기:찜:50"
    "1-5:닭고기구이:밑반찬:일상:닭고기:구이:50"
    "1-6:닭고기조림:밑반찬:일상:닭고기:조림:50"
    "1-7:생선구이:밑반찬:일상:생선류:구이:50"
    "1-8:오징어볶음:밑반찬:일상:오징어:볶음:50"
    
    # Phase 2: 야채 & 두부 (200개)
    "2-1:두부조림:밑반찬:일상:두부:조림:50"
    "2-2:두부볶음:밑반찬:일상:두부:볶음:50"
    "2-3:버섯볶음:밑반찬:일상:버섯:볶음:50"
    "2-4:가지볶음:밑반찬:일상:가지:볶음:50"
    
    # Phase 3: 밥/면 요리 (200개)
    "3-1:소고기볶음밥:일품요리:일상:소고기:볶음:50"
    "3-2:김치볶음밥:일품요리:일상:김치:볶음:50"
    "3-3:면볶음:일품요리:초스피드:면:볶음:50"
    "3-4:파스타:일품요리:초스피드:파스타:볶음:50"
    
    # Phase 4: 국/찌개 (200개)
    "4-1:소고기국:국/탕:일상:소고기:끓이기:50"
    "4-2:생선국:국/탕:일상:생선류:끓이기:50"
    "4-3:돼지고기찌개:찌개:일상:돼지고기:끓이기:50"
    "4-4:두부찌개:찌개:일상:두부:끓이기:50"
)

TOTAL=${#COLLECTIONS[@]}
CURRENT=0
TOTAL_RECIPES=0
START_TIME=$(date +%s)

log_info "=========================================="
log_info "  1000개 레시피 자동 수집 시작"
log_info "=========================================="
log_info "총 ${TOTAL}개 배치 작업"
log_info ""

# 메인 루프
for collection in "${COLLECTIONS[@]}"; do
    CURRENT=$((CURRENT + 1))
    
    IFS=':' read -r phase name type situation ingredient method count <<< "$collection"
    
    echo ""
    log_info "=========================================="
    log_info "[$CURRENT/$TOTAL] Phase $phase: $name"
    log_info "=========================================="
    log_info "Type: $type | Situation: $situation"
    log_info "Ingredient: $ingredient | Method: $method"
    log_info "Count: $count"
    log_info ""
    
    # .env 파일 업데이트 (구분자를 | 로 변경하여 / 문자 허용)
    sed -i "s|^RECIPE_TYPE=.*|RECIPE_TYPE=$type|" config/.env
    sed -i "s|^RECIPE_SITUATION=.*|RECIPE_SITUATION=$situation|" config/.env
    sed -i "s|^RECIPE_INGREDIENT=.*|RECIPE_INGREDIENT=$ingredient|" config/.env
    sed -i "s|^RECIPE_METHOD=.*|RECIPE_METHOD=$method|" config/.env
    sed -i "s|^MAX_RECIPES=.*|MAX_RECIPES=$count|" config/.env
    
    # 실행 (--no-prompt: DB 초기화 프롬프트 건너뛰기)
    BATCH_START=$(date +%s)
    
    if python main.py --no-prompt 2>&1 | tee "logs/batch_${phase}_${name}.log"; then
        BATCH_END=$(date +%s)
        BATCH_TIME=$((BATCH_END - BATCH_START))
        TOTAL_RECIPES=$((TOTAL_RECIPES + count))
        
        log_success "Phase $phase 완료! (소요: ${BATCH_TIME}초)"
        
        # 현재 통계
        CURRENT_TIME=$(date +%s)
        ELAPSED=$((CURRENT_TIME - START_TIME))
        AVG_TIME=$((ELAPSED / CURRENT))
        REMAINING=$((TOTAL - CURRENT))
        ETA=$((AVG_TIME * REMAINING))
        
        log_info "진행: $CURRENT/$TOTAL 완료 | 수집: $TOTAL_RECIPES개"
        log_info "경과: ${ELAPSED}초 | 예상 남은 시간: ${ETA}초 (~$((ETA/60))분)"
        
        # 잠시 대기 (서버 부하 방지)
        log_info "다음 배치까지 5초 대기..."
        sleep 5
    else
        log_error "Phase $phase 실패!"
        log_warning "계속하시겠습니까? (y/N)"
        read -p "> " continue_on_error
        if [[ ! $continue_on_error =~ ^[Yy]$ ]]; then
            log_error "작업 중단"
            exit 1
        fi
    fi
done

# 최종 통계
END_TIME=$(date +%s)
TOTAL_TIME=$((END_TIME - START_TIME))

echo ""
log_success "=========================================="
log_success "  모든 수집 완료!"
log_success "=========================================="
log_success "총 수집: $TOTAL_RECIPES개 레시피"
log_success "총 시간: $TOTAL_TIME초 (~$((TOTAL_TIME/60))분)"
log_success "평균: $((TOTAL_TIME/TOTAL_RECIPES))초/레시피"
log_success "=========================================="

# DB 통계
log_info ""
log_info "DB 통계:"
PGPASSWORD='wkwjsrj4510*' psql -h localhost -d recipe_ai_db -U recipe_keep -c "
SELECT 
    COUNT(*) as recipes,
    (SELECT COUNT(*) FROM ingredients) as ingredients,
    (SELECT COUNT(*) FROM cooking_steps) as steps
FROM recipes;
" 2>&1 | grep -v "^$"

log_info ""
log_success "✅ 작업 완료! DBeaver에서 확인하세요."

