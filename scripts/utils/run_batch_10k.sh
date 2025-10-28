#!/bin/bash
# 10,000개 레시피 자동 수집 스크립트 (확장판)

set -e  # 에러 발생 시 중단

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR/../.."

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

# PostgreSQL 비밀번호 환경변수 설정
export PGPASSWORD='wkwjsrj4510*'

# DB 초기화 확인
read -p "DB를 초기화하고 시작하시겠습니까? (y/N): " reset_db
if [[ $reset_db =~ ^[Yy]$ ]]; then
    log_info "DB 초기화 중..."
    psql -h localhost -d recipe_ai_db -U recipe_keep -c "TRUNCATE recipes CASCADE;" 2>&1 | grep -v "^$"
    log_success "DB 초기화 완료"
fi

# 수집 설정 배열 - 10,000개 목표
# 형식: "Phase:이름:종류:상황:재료:방법:개수"
declare -a COLLECTIONS=(
    # ===== Phase 1: 메인 단백질 요리 (2000개) =====
    # 소고기 (500개)
    "1-1:소고기볶음:밑반찬:일상:소고기:볶음:100"
    "1-2:소고기구이:밑반찬:일상:소고기:구이:100"
    "1-3:소고기조림:밑반찬:일상:소고기:조림:100"
    "1-4:소고기찜:밑반찬:일상:소고기:찜:100"
    "1-5:소고기무침:밑반찬:일상:소고기:무침:100"
    
    # 돼지고기 (500개)
    "1-6:돼지고기볶음:밑반찬:일상:돼지고기:볶음:100"
    "1-7:돼지고기구이:밑반찬:일상:돼지고기:구이:100"
    "1-8:돼지고기찜:밑반찬:일상:돼지고기:찜:100"
    "1-9:돼지고기조림:밑반찬:일상:돼지고기:조림:100"
    "1-10:삼겹살요리:밑반찬:일상:돼지고기:굽기:100"
    
    # 닭고기 (500개)
    "1-11:닭고기구이:밑반찬:일상:닭고기:구이:100"
    "1-12:닭고기조림:밑반찬:일상:닭고기:조림:100"
    "1-13:닭고기볶음:밑반찬:일상:닭고기:볶음:100"
    "1-14:닭고기튀김:밑반찬:일상:닭고기:튀김:100"
    "1-15:닭가슴살요리:밑반찬:초스피드:닭고기:볶음:100"
    
    # 해산물 (500개)
    "1-16:생선구이:밑반찬:일상:생선류:구이:100"
    "1-17:생선조림:밑반찬:일상:생선류:조림:100"
    "1-18:오징어볶음:밑반찬:일상:오징어:볶음:100"
    "1-19:새우볶음:밑반찬:일상:새우:볶음:100"
    "1-20:조개찜:밑반찬:일상:조개류:찜:100"
    
    # ===== Phase 2: 야채 & 두부 요리 (1500개) =====
    # 두부 (300개)
    "2-1:두부조림:밑반찬:일상:두부:조림:100"
    "2-2:두부볶음:밑반찬:일상:두부:볶음:100"
    "2-3:두부구이:밑반찬:일상:두부:구이:100"
    
    # 버섯 (300개)
    "2-4:버섯볶음:밑반찬:일상:버섯:볶음:100"
    "2-5:표고버섯조림:밑반찬:일상:버섯:조림:100"
    "2-6:새송이버섯구이:밑반찬:일상:버섯:구이:100"
    
    # 가지/호박 (300개)
    "2-7:가지볶음:밑반찬:일상:가지:볶음:100"
    "2-8:호박볶음:밑반찬:일상:호박:볶음:100"
    "2-9:애호박나물:밑반찬:일상:호박:볶음:100"
    
    # 감자/고구마 (300개)
    "2-10:감자조림:밑반찬:일상:감자:조림:100"
    "2-11:감자볶음:밑반찬:일상:감자:볶음:100"
    "2-12:고구마요리:밑반찬:일상:고구마:찜:100"
    
    # 기타 야채 (300개)
    "2-13:콩나물무침:밑반찬:초스피드:콩나물:무침:100"
    "2-14:시금치나물:밑반찬:초스피드:시금치:무침:100"
    "2-15:파채무침:밑반찬:초스피드:파:무침:100"
    
    # ===== Phase 3: 밥/면/일품 요리 (2000개) =====
    # 볶음밥 (400개)
    "3-1:김치볶음밥:일품요리:일상:김치:볶음:100"
    "3-2:소고기볶음밥:일품요리:일상:소고기:볶음:100"
    "3-3:새우볶음밥:일품요리:일상:새우:볶음:100"
    "3-4:야채볶음밥:일품요리:초스피드:야채:볶음:100"
    
    # 덮밥 (400개)
    "3-5:소고기덮밥:일품요리:일상:소고기:볶음:100"
    "3-6:돼지고기덮밥:일품요리:일상:돼지고기:볶음:100"
    "3-7:닭고기덮밥:일품요리:일상:닭고기:볶음:100"
    "3-8:야채덮밥:일품요리:초스피드:야채:볶음:100"
    
    # 면 요리 (600개)
    "3-9:파스타:일품요리:초스피드:파스타:볶음:100"
    "3-10:스파게티:일품요리:일상:파스타:볶음:100"
    "3-11:볶음면:일품요리:초스피드:면:볶음:100"
    "3-12:잔치국수:일품요리:일상:면:끓이기:100"
    "3-13:비빔국수:일품요리:초스피드:면:무침:100"
    "3-14:칼국수:일품요리:일상:면:끓이기:100"
    
    # 기타 일품 (600개)
    "3-15:떡볶이:일품요리:초스피드:떡:볶음:100"
    "3-16:김밥:일품요리:일상:김:만들기:100"
    "3-17:만두:일품요리:일상:만두:찜:100"
    "3-18:전:밑반찬:일상:부침가루:부침:100"
    "3-19:샌드위치:일품요리:초스피드:빵:만들기:100"
    "3-20:샐러드:일품요리:초스피드:야채:무침:100"
    
    # ===== Phase 4: 국/탕/찌개 (2000개) =====
    # 국/탕 (1000개)
    "4-1:소고기국:국/탕:일상:소고기:끓이기:100"
    "4-2:소고기무국:국/탕:일상:소고기:끓이기:100"
    "4-3:돼지고기국:국/탕:일상:돼지고기:끓이기:100"
    "4-4:돼지고기김치국:국/탕:일상:돼지고기:끓이기:100"
    "4-5:생선국:국/탕:일상:생선류:끓이기:100"
    "4-6:조개국:국/탕:일상:조개류:끓이기:100"
    "4-7:미역국:국/탕:일상:미역:끓이기:100"
    "4-8:된장국:국/탕:일상:된장:끓이기:100"
    "4-9:콩나물국:국/탕:초스피드:콩나물:끓이기:100"
    "4-10:계란국:국/탕:초스피드:계란:끓이기:100"
    
    # 찌개 (1000개)
    "4-11:김치찌개:찌개:일상:김치:끓이기:100"
    "4-12:된장찌개:찌개:일상:된장:끓이기:100"
    "4-13:순두부찌개:찌개:일상:두부:끓이기:100"
    "4-14:부대찌개:찌개:일상:소시지:끓이기:100"
    "4-15:청국장찌개:찌개:일상:청국장:끓이기:100"
    "4-16:고추장찌개:찌개:일상:고추장:끓이기:100"
    "4-17:해물찌개:찌개:일상:해물:끓이기:100"
    "4-18:생선찌개:찌개:일상:생선류:끓이기:100"
    "4-19:동태찌개:찌개:일상:생선류:끓이기:100"
    "4-20:버섯찌개:찌개:일상:버섯:끓이기:100"
    
    # ===== Phase 5: 특수 요리 (1500개) =====
    # 찜 요리 (500개)
    "5-1:갈비찜:찜:일상:소고기:찜:100"
    "5-2:닭찜:찜:일상:닭고기:찜:100"
    "5-3:돼지갈비찜:찜:일상:돼지고기:찜:100"
    "5-4:계란찜:찜:초스피드:계란:찜:100"
    "5-5:해물찜:찜:일상:해물:찜:100"
    
    # 튀김/전 (500개)
    "5-6:닭강정:튀김:일상:닭고기:튀김:100"
    "5-7:탕수육:튀김:일상:돼지고기:튀김:100"
    "5-8:생선튀김:튀김:일상:생선류:튀김:100"
    "5-9:야채튀김:튀김:일상:야채:튀김:100"
    "5-10:김치전:부침:일상:김치:부침:100"
    
    # 무침/겉절이 (500개)
    "5-11:오이무침:밑반찬:초스피드:오이:무침:100"
    "5-12:파무침:밑반찬:초스피드:파:무침:100"
    "5-13:상추겉절이:밑반찬:초스피드:상추:무침:100"
    "5-14:배추겉절이:밑반찬:초스피드:배추:무침:100"
    "5-15:열무김치:김치:일상:열무:무침:100"
    
    # ===== Phase 6: 디저트/간식 (1000개) =====
    # 디저트 (500개)
    "6-1:케이크:디저트:일상:빵:굽기:100"
    "6-2:쿠키:디저트:일상:빵:굽기:100"
    "6-3:빵:디저트:일상:빵:굽기:100"
    "6-4:호떡:디저트:일상:밀가루:부침:100"
    "6-5:팬케이크:디저트:초스피드:밀가루:부침:100"
    
    # 음료/스무디 (500개)
    "6-6:스무디:음료:초스피드:과일:갈기:100"
    "6-7:주스:음료:초스피드:과일:갈기:100"
    "6-8:차:음료:초스피드:차:끓이기:100"
    "6-9:라떼:음료:초스피드:우유:만들기:100"
    "6-10:에이드:음료:초스피드:과일:만들기:100"
)

TOTAL=${#COLLECTIONS[@]}
CURRENT=0
TOTAL_RECIPES=0
START_TIME=$(date +%s)

log_info "=========================================="
log_info "  10,000개 레시피 자동 수집 시작"
log_info "=========================================="
log_info "총 ${TOTAL}개 배치 작업"
log_info "예상 소요 시간: 약 10-12시간"
log_info ""
log_warning "⚠️  장시간 작업입니다. 컴퓨터가 꺼지지 않도록 주의하세요!"
log_warning "⚠️  중간에 중단하려면 Ctrl+C를 누르세요."
echo ""
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
    
    if python main.py --no-prompt 2>&1 | tee "logs/batch_10k_${phase}_${name}.log"; then
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
        log_info "수집: $TOTAL_RECIPES개 레시피"
        log_info "경과: $((ELAPSED/60))분 | 예상 남은 시간: $((ETA/60))분 (~$((ETA/3600))시간)"
        
        # 백업 (1000개마다)
        if [ $((TOTAL_RECIPES % 1000)) -eq 0 ]; then
            log_info "백업 생성 중... ($TOTAL_RECIPES개)"
            pg_dump -h localhost -U recipe_keep recipe_ai_db > "backups/backup_${TOTAL_RECIPES}_$(date +%Y%m%d_%H%M%S).sql" 2>/dev/null || true
            log_success "백업 완료"
        fi
        
        # 잠시 대기 (서버 부하 방지)
        log_info "다음 배치까지 5초 대기..."
        sleep 5
    else
        log_error "Phase $phase 실패!"
        log_warning "계속하시겠습니까? (y/N)"
        read -p "> " continue_on_error
        if [[ ! $continue_on_error =~ ^[Yy]$ ]]; then
            log_error "작업 중단 (현재까지 수집: $TOTAL_RECIPES개)"
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
log_success "총 시간: $((TOTAL_TIME/60))분 (~$((TOTAL_TIME/3600))시간)"
log_success "평균: $((TOTAL_TIME/TOTAL_RECIPES))초/레시피"
log_success "=========================================="

# DB 통계
log_info ""
log_info "DB 최종 통계:"
psql -h localhost -d recipe_ai_db -U recipe_keep -c "
SELECT 
    COUNT(*) as total_recipes,
    (SELECT COUNT(*) FROM ingredients) as total_ingredients,
    (SELECT COUNT(*) FROM cooking_steps) as total_steps,
    (SELECT COUNT(*) FROM recipes WHERE embedding IS NOT NULL) as vectorized_recipes
FROM recipes;
" 2>&1 | grep -v "^$"

# 최종 백업
log_info ""
log_info "최종 백업 생성 중..."
pg_dump -h localhost -U recipe_keep recipe_ai_db > "backups/final_10k_$(date +%Y%m%d_%H%M%S).sql" 2>/dev/null || true
log_success "최종 백업 완료"

log_info ""
log_success "🎉 10,000개 레시피 수집 완료!"
log_success "✅ 다음 단계: 벡터화 (python vectorize_recipes.py)"

