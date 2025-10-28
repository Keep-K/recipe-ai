# 🚀 10,000개 레시피 수집 가이드

Recipe AI 시스템으로 대규모 레시피 데이터베이스를 구축하는 완벽한 가이드입니다.

---

## ⚡ 빠른 시작

```bash
# 1. PostgreSQL 시작 (WSL2)
sudo service postgresql start

# 2. 스크립트 실행 (비밀번호 입력 자동화됨!)
cd /home/keep/recipe-ai/recipe_ai_system
./scripts/utils/run_batch_10k.sh
```

**예상 소요 시간**: 약 10-12시간 ⏰  
**추천**: 밤에 시작하고 다음 날 아침에 확인하세요!

**참고**: PostgreSQL 비밀번호는 스크립트에 자동으로 설정되므로 입력할 필요 없습니다! ✅

---

## 📊 수집 구성 (100개 단위로 10,000개)

### Phase 1: 메인 단백질 요리 (2,000개)
- 소고기 요리 (500개): 볶음, 구이, 조림, 찜, 무침
- 돼지고기 요리 (500개): 볶음, 구이, 찜, 조림, 삼겹살
- 닭고기 요리 (500개): 구이, 조림, 볶음, 튀김, 닭가슴살
- 해산물 요리 (500개): 생선, 오징어, 새우, 조개

### Phase 2: 야채 & 두부 요리 (1,500개)
- 두부 (300개): 조림, 볶음, 구이
- 버섯 (300개): 볶음, 조림, 구이
- 가지/호박 (300개): 볶음, 나물
- 감자/고구마 (300개): 조림, 볶음, 찜
- 기타 야채 (300개): 콩나물, 시금치, 파채

### Phase 3: 밥/면/일품 요리 (2,000개)
- 볶음밥 (400개): 김치, 소고기, 새우, 야채
- 덮밥 (400개): 소고기, 돼지고기, 닭고기, 야채
- 면 요리 (600개): 파스타, 스파게티, 볶음면, 국수, 칼국수
- 기타 일품 (600개): 떡볶이, 김밥, 만두, 전, 샌드위치, 샐러드

### Phase 4: 국/탕/찌개 (2,000개)
- 국/탕 (1,000개): 소고기국, 돼지고기국, 생선국, 조개국, 미역국 등
- 찌개 (1,000개): 김치찌개, 된장찌개, 순두부찌개, 부대찌개 등

### Phase 5: 특수 요리 (1,500개)
- 찜 요리 (500개): 갈비찜, 닭찜, 계란찜, 해물찜
- 튀김/전 (500개): 닭강정, 탕수육, 생선튀김, 김치전
- 무침/겉절이 (500개): 오이무침, 파무침, 상추겉절이, 김치

### Phase 6: 디저트/간식 (1,000개)
- 디저트 (500개): 케이크, 쿠키, 빵, 호떡, 팬케이크
- 음료/스무디 (500개): 스무디, 주스, 차, 라떼, 에이드

---

## 🎯 실행 전 체크리스트

### ✅ 필수 준비사항
- [ ] **PostgreSQL 실행 중** (`sudo service postgresql start`)
- [ ] **10개 OpenAI API 키** 설정 완료 (`config/.env`)
- [ ] **가상환경 활성화** (`source venv/bin/activate`)
- [ ] **충분한 디스크 공간** (최소 5GB 이상)
- [ ] **안정적인 인터넷 연결**
- [ ] **컴퓨터 절전 모드 해제** (10시간 이상 실행)

### ⚙️ 설정 확인
```bash
# 1. PostgreSQL 확인
sudo service postgresql status

# 2. API 키 개수 확인 (10개여야 함)
cat config/.env | grep "^OPENAI_API_KEY" | wc -l

# 3. DB 연결 테스트
PGPASSWORD='wkwjsrj4510*' psql -h localhost -d recipe_ai_db -U recipe_keep -c "\dt"

# 4. 디스크 공간 확인
df -h /home/keep/recipe-ai
```

---

## 🚀 실행 방법

### 자동 실행 (추천)
```bash
cd /home/keep/recipe-ai/recipe_ai_system
./scripts/utils/run_batch_10k.sh
```

스크립트가 다음을 자동으로 처리합니다:
1. DB 초기화 여부 확인
2. 100개 단위로 순차 수집
3. 1,000개마다 자동 백업
4. 진행 상황 실시간 표시
5. 예상 남은 시간 계산
6. 최종 통계 및 백업

### 수동 실행 (세밀한 제어)
```bash
# 1. 가상환경 활성화
source venv/bin/activate

# 2. 환경 변수 설정
nano config/.env

# 예시:
# RECIPE_TYPE=밑반찬
# RECIPE_INGREDIENT=소고기
# RECIPE_METHOD=볶음
# MAX_RECIPES=100

# 3. 실행
python main.py --no-prompt

# 4. 다음 카테고리로 변경 후 반복
```

---

## 📊 진행 상황 모니터링

### 실시간 로그 확인
```bash
# 터미널 1: 스크립트 실행
./scripts/utils/run_batch_10k.sh

# 터미널 2: 로그 모니터링
tail -f logs/batch_10k_*.log
```

### 현재 DB 통계 확인
```bash
PGPASSWORD='wkwjsrj4510*' psql -h localhost -d recipe_ai_db -U recipe_keep -c "
SELECT 
    COUNT(*) as total_recipes,
    (SELECT COUNT(*) FROM ingredients) as ingredients,
    (SELECT COUNT(*) FROM cooking_steps) as steps
FROM recipes;
"
```

### DBeaver에서 실시간 확인
1. DBeaver 실행
2. recipe_ai_db 연결
3. recipes 테이블 선택
4. F5 키로 새로고침 (주기적으로)

---

## ⏱️ 예상 시간표

| 단계 | 누적 레시피 | 예상 시간 | 진행률 |
|------|------------|-----------|--------|
| Phase 1 완료 | 2,000개 | ~2시간 | 20% |
| Phase 2 완료 | 3,500개 | ~3.5시간 | 35% |
| Phase 3 완료 | 5,500개 | ~5.5시간 | 55% |
| Phase 4 완료 | 7,500개 | ~7.5시간 | 75% |
| Phase 5 완료 | 9,000개 | ~9시간 | 90% |
| Phase 6 완료 | 10,000개 | ~10시간 | 100% ✅ |

**실제 시간은 API 응답 속도, 네트워크 상태에 따라 달라질 수 있습니다.**

---

## 🔄 중단 후 재개

스크립트가 중단되었을 때:

```bash
# 1. 현재 DB 레시피 수 확인
PGPASSWORD='wkwjsrj4510*' psql -h localhost -d recipe_ai_db -U recipe_keep -c "SELECT COUNT(*) FROM recipes;"

# 2. 스크립트 편집
nano scripts/utils/run_batch_10k.sh

# 3. 완료된 Phase 라인들을 주석 처리 (#으로 시작)
# 예시: Phase 1-10까지 완료되었다면
# "1-1:소고기볶음..." → # "1-1:소고기볶음..."

# 4. 재실행 (DB 초기화 안 함!)
./scripts/utils/run_batch_10k.sh
# → "DB를 초기화하고 시작하시겠습니까?" → N 입력
```

---

## 💾 자동 백업

스크립트는 자동으로 백업을 생성합니다:

### 백업 타이밍
- 1,000개마다 자동 백업
- 최종 완료 시 전체 백업

### 백업 위치
```
recipe_ai_system/backups/
├── backup_1000_20251024_120000.sql
├── backup_2000_20251024_140000.sql
├── ...
└── final_10k_20251024_220000.sql
```

### 수동 백업
```bash
# 백업 생성
pg_dump -h localhost -U recipe_keep recipe_ai_db > backups/manual_backup_$(date +%Y%m%d_%H%M%S).sql

# 복구 (필요시)
PGPASSWORD='wkwjsrj4510*' psql -h localhost -d recipe_ai_db -U recipe_keep < backups/backup_5000_20251024_180000.sql
```

---

## ⚠️ 문제 해결

### API Rate Limit (429 에러)
```bash
# config/.env에서 딜레이 증가
TRANSLATION_DELAY=0.5  # 0.3에서 0.5로 증가
```

### DB 연결 끊김
```bash
# PostgreSQL 재시작
sudo service postgresql restart

# 연결 테스트
psql -h localhost -U recipe_keep -d recipe_ai_db
```

### 메모리 부족
```bash
# 배치 크기 줄이기 (스크립트 편집)
nano scripts/utils/run_batch_10k.sh

# 100 → 50으로 변경
"1-1:소고기볶음:밑반찬:일상:소고기:볶음:50"
```

### 디스크 공간 부족
```bash
# 공간 확인
df -h

# 로그 파일 정리
rm logs/batch_10k_*.log

# 오래된 백업 삭제
rm backups/backup_1000_*.sql
```

### 스크립트 강제 종료
```bash
# Python 프로세스 종료
pkill -f "python main.py"

# DB 통계로 현재 상태 확인
PGPASSWORD='wkwjsrj4510*' psql -h localhost -d recipe_ai_db -U recipe_keep -c "SELECT COUNT(*) FROM recipes;"
```

---

## 🎉 완료 후 다음 단계

### 1. 최종 통계 확인
```bash
PGPASSWORD='wkwjsrj4510*' psql -h localhost -d recipe_ai_db -U recipe_keep -c "
SELECT 
    COUNT(*) as total_recipes,
    COUNT(DISTINCT SUBSTRING(url FROM 'recipe/([0-9]+)')) as unique_recipes,
    (SELECT COUNT(*) FROM ingredients) as total_ingredients,
    (SELECT COUNT(*) FROM cooking_steps) as total_steps,
    (SELECT COUNT(*) FROM recipes WHERE title_en IS NOT NULL) as translated_recipes
FROM recipes;
"
```

### 2. 벡터화 (AI 검색용)
```bash
# 전체 레시피 벡터화 (약 2-3시간 소요)
python vectorize_recipes.py

# 진행 상황 확인
PGPASSWORD='wkwjsrj4510*' psql -h localhost -d recipe_ai_db -U recipe_keep -c "
SELECT 
    COUNT(*) as total,
    COUNT(*) FILTER (WHERE embedding IS NOT NULL) as vectorized,
    COUNT(*) FILTER (WHERE embedding IS NULL) as remaining
FROM recipes;
"
```

### 3. FastAPI 서버로 테스트
```bash
# 서버 실행
python api_server.py

# 브라우저에서 http://localhost:8000/docs 접속
# /search 엔드포인트로 검색 테스트
```

### 4. 프론트엔드 연동
```bash
# React 앱 실행
cd /home/keep/recipe-ai/recipe_web/recipe-chat-app
npm run dev

# 브라우저에서 http://localhost:5173 접속
# 채팅으로 레시피 검색 테스트
```

---

## 📈 성능 최적화

### 속도 향상 방법
1. **API 키 10개 사용**: 10배 빠름 ⚡
2. **배치 크기 조정**: 네트워크 상황에 맞게
3. **딜레이 감소**: 안정적이면 0.2초까지 가능
4. **병렬 실행**: 여러 터미널에서 다른 카테고리 동시 수집

### 예상 성능
- **10개 API 키**: 약 10시간
- **5개 API 키**: 약 15시간
- **1개 API 키**: 약 50시간

---

## 💡 팁

### 밤에 실행 추천
```bash
# 저녁 10시에 시작
./scripts/utils/run_batch_10k.sh

# 다음 날 아침 8시에 완료! ✅
```

### Screen 사용 (SSH 환경)
```bash
# screen 세션 시작
screen -S recipe_collection

# 스크립트 실행
./scripts/utils/run_batch_10k.sh

# Ctrl+A, D로 세션 분리
# SSH 연결 끊어도 계속 실행됨

# 나중에 다시 연결
screen -r recipe_collection
```

### Tmux 사용 (WSL2)
```bash
# tmux 세션 시작
tmux new -s recipe

# 스크립트 실행
./scripts/utils/run_batch_10k.sh

# Ctrl+B, D로 세션 분리

# 나중에 다시 연결
tmux attach -t recipe
```

---

## 📊 데이터 품질 체크

수집 완료 후 품질 확인:

```sql
-- 번역 완료율
SELECT 
    COUNT(*) as total,
    COUNT(*) FILTER (WHERE title_en IS NOT NULL) * 100.0 / COUNT(*) as translation_rate
FROM recipes;

-- 중복 확인
SELECT url, COUNT(*) 
FROM recipes 
GROUP BY url 
HAVING COUNT(*) > 1;

-- 빈 필드 확인
SELECT 
    COUNT(*) FILTER (WHERE title IS NULL) as no_title,
    COUNT(*) FILTER (WHERE description IS NULL) as no_description,
    COUNT(*) FILTER (WHERE cooking_time IS NULL) as no_time
FROM recipes;
```

---

## 🚀 시작하기

```bash
cd /home/keep/recipe-ai/recipe_ai_system
./scripts/utils/run_batch_10k.sh
```

**커피 한 잔 하고... 아니, 푹 주무시고 내일 확인하세요! 😴**  
**약 10시간 후 10,000개 레시피가 준비됩니다!** 🎉

---

## 📚 관련 문서

- [1,000개 수집 가이드](START_1000.md)
- [벡터화 가이드](VECTORIZATION_GUIDE.md)
- [FastAPI 서버 가이드](FASTAPI_SERVER_GUIDE.md)
- [성능 최적화](PERFORMANCE.md)

