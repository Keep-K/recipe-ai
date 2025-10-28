#!/bin/bash
# 추가 레시피 수집 스크립트 - 기존 DB에 이어서 추가

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR/../.."

# 색상
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# 로그 함수
log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[✓]${NC} $1"; }
log_warning() { echo -e "${YELLOW}[!]${NC} $1"; }
log_error() { echo -e "${RED}[✗]${NC} $1"; }

# 환경 체크
if [ ! -f "config/.env" ]; then
    log_error "config/.env not found!"
    exit 1
fi

if [ ! -d "venv" ]; then
    log_error "venv not found!"
    exit 1
fi

# Virtual env 활성화
source venv/bin/activate

# PostgreSQL 비밀번호 환경변수 설정
export PGPASSWORD='wkwjsrj4510*'

log_info "=========================================="
log_info "  추가 레시피 수집 시작"
log_info "=========================================="

# 현재 DB 레시피 수 확인
CURRENT_COUNT=$(psql -h localhost -d recipe_ai_db -U recipe_keep -t -c "SELECT COUNT(*) FROM recipes;" 2>/dev/null | tr -d ' ')
log_info "현재 DB 레시피 수: ${CURRENT_COUNT}개"
log_info ""

# 추가 수집 배열 - 자유롭게 편집하세요!
declare -a COLLECTIONS=(
    # ===== Phase 7: 한식 전통 밑반찬 (2,000개) =====
    "7-1:장아찌:밑반찬:일상:무:절임:100"
    "7-2:젓갈:밑반찬:일상:새우:절임:100"
    "7-3:장조림:밑반찬:일상:소고기:조림:100"
    "7-4:북어채:밑반찬:일상:북어:무침:100"
    "7-5:해파리냉채:밑반찬:일상:해파리:무침:100"
    "7-6:묵무침:밑반찬:초스피드:도토리묵:무침:100"
    "7-7:김무침:밑반찬:초스피드:김:무침:100"
    "7-8:미나리무침:밑반찬:초스피드:미나리:무침:100"
    "7-9:숙주나물:밑반찬:초스피드:숙주:무침:100"
    "7-10:고사리나물:밑반찬:일상:고사리:볶음:100"
    "7-11:도라지무침:밑반찬:일상:도라지:무침:100"
    "7-12:더덕구이:밑반찬:일상:더덕:구이:100"
    "7-13:마늘종볶음:밑반찬:일상:마늘종:볶음:100"
    "7-14:청경채볶음:밑반찬:초스피드:청경채:볶음:100"
    "7-15:쑥갓무침:밑반찬:초스피드:쑥갓:무침:100"
    "7-16:취나물:밑반찬:일상:취나물:볶음:100"
    "7-17:냉이나물:밑반찬:일상:냉이:무침:100"
    "7-18:달래무침:밑반찬:초스피드:달래:무침:100"
    "7-19:부추무침:밑반찬:초스피드:부추:무침:100"
    "7-20:양파장아찌:밑반찬:일상:양파:절임:100"
)

TOTAL=${#COLLECTIONS[@]}
CURRENT=0
TOTAL_RECIPES=0
START_TIME=$(date +%s)

log_info "총 ${TOTAL}개 배치 작업"
log_info "예상 추가: $((TOTAL * 100))개 레시피"
log_info "예상 소요 시간: 약 $((TOTAL * 2))시간"
log_info ""

read -p "계속하시겠습니까? (y/N): " confirm
if [[ ! $confirm =~ ^[Yy]$ ]]; then
    log_error "작업 취소"
    exit 0
fi

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
    
    # .env 파일 업데이트
    sed -i "s|^RECIPE_TYPE=.*|RECIPE_TYPE=$type|" config/.env
    sed -i "s|^RECIPE_SITUATION=.*|RECIPE_SITUATION=$situation|" config/.env
    sed -i "s|^RECIPE_INGREDIENT=.*|RECIPE_INGREDIENT=$ingredient|" config/.env
    sed -i "s|^RECIPE_METHOD=.*|RECIPE_METHOD=$method|" config/.env
    sed -i "s|^MAX_RECIPES=.*|MAX_RECIPES=$count|" config/.env
    
    # 실행
    BATCH_START=$(date +%s)
    
    if python main.py --no-prompt 2>&1 | tee "logs/batch_add_${phase}_${name}.log"; then
        BATCH_END=$(date +%s)
        BATCH_TIME=$((BATCH_END - BATCH_START))
        TOTAL_RECIPES=$((TOTAL_RECIPES + count))
        
        log_success "Phase $phase 완료! (소요: ${BATCH_TIME}초 = $((BATCH_TIME/60))분)"
        
        # 현재 통계
        CURRENT_TIME=$(date +%s)
        ELAPSED=$((CURRENT_TIME - START_TIME))
        AVG_TIME=$((ELAPSED / CURRENT))
        REMAINING=$((TOTAL - CURRENT))
        ETA=$((AVG_TIME * REMAINING))
        
        log_info "진행: $CURRENT/$TOTAL 완료 ($((CURRENT*100/TOTAL))%)"
        log_info "추가된 레시피: $TOTAL_RECIPES개"
        log_info "경과: $((ELAPSED/60))분 | 예상 남은 시간: $((ETA/60))분"
        
        # 백업 (1000개마다)
        if [ $((TOTAL_RECIPES % 1000)) -eq 0 ]; then
            log_info "백업 생성 중... (추가 $TOTAL_RECIPES개)"
            pg_dump -h localhost -U recipe_keep recipe_ai_db > "backups/backup_add_${TOTAL_RECIPES}_$(date +%Y%m%d_%H%M%S).sql" 2>/dev/null || true
            log_success "백업 완료"
        fi
        
        # 잠시 대기
        log_info "다음 배치까지 5초 대기..."
        sleep 5
    else
        log_error "Phase $phase 실패!"
        log_warning "계속하시겠습니까? (y/N)"
        read -p "> " continue_on_error
        if [[ ! $continue_on_error =~ ^[Yy]$ ]]; then
            log_error "작업 중단 (현재까지 추가: $TOTAL_RECIPES개)"
            exit 1
        fi
    fi
done

# 최종 통계
END_TIME=$(date +%s)
TOTAL_TIME=$((END_TIME - START_TIME))

echo ""
log_success "=========================================="
log_success "  추가 수집 완료!"
log_success "=========================================="
log_success "추가된 레시피: $TOTAL_RECIPES개"
log_success "총 소요 시간: $((TOTAL_TIME/60))분 (~$((TOTAL_TIME/3600))시간)"
log_success "=========================================="

# DB 최종 통계
log_info ""
log_info "DB 최종 통계:"
psql -h localhost -d recipe_ai_db -U recipe_keep -c "
SELECT 
    COUNT(*) as total_recipes,
    (SELECT COUNT(*) FROM ingredients) as total_ingredients,
    (SELECT COUNT(*) FROM cooking_steps) as total_steps
FROM recipes;
" 2>&1 | grep -v "^$"

# 최종 백업
log_info ""
log_info "최종 백업 생성 중..."
FINAL_COUNT=$(psql -h localhost -d recipe_ai_db -U recipe_keep -t -c "SELECT COUNT(*) FROM recipes;" 2>/dev/null | tr -d ' ')
pg_dump -h localhost -U recipe_keep recipe_ai_db > "backups/final_${FINAL_COUNT}_$(date +%Y%m%d_%H%M%S).sql" 2>/dev/null || true
log_success "최종 백업 완료"

log_info ""
log_success "🎉 추가 수집 완료!"
log_success "✅ 총 레시피: ${FINAL_COUNT}개"
log_success "✅ 다음 단계: 벡터화 (python vectorize_recipes.py)"

