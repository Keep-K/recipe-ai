# 🚀 1000개 레시피 수집 시작 가이드

## ⚡ 빠른 시작 (자동화)

```bash
cd /home/keep/recipe-ai/recipe_ai_system
./run_batch_collection.sh
```

**예상 시간**: 약 70-80분 (1시간 10분)

---

## 📊 수집 계획

### **Phase 1: 메인 단백질 (400개)**
- 소고기 볶음/구이 (100개)
- 돼지고기 볶음/찜 (100개)
- 닭고기 구이/조림 (100개)
- 해산물 구이/볶음 (100개)

### **Phase 2: 야채 & 두부 (200개)**
- 두부 조림/볶음 (100개)
- 버섯/가지 볶음 (100개)

### **Phase 3: 밥/면 요리 (200개)**
- 볶음밥 (100개)
- 면 요리 (100개)

### **Phase 4: 국/찌개 (200개)**
- 국/탕 (100개)
- 찌개 (100개)

---

## 🎯 실행 전 체크리스트

### ✅ 필수 사항
- [ ] 10개 API 키 설정 완료 (`config/.env`)
- [ ] DB 접속 확인 (recipe_ai_db)
- [ ] 가상환경 활성화 (`venv`)
- [ ] 충분한 디스크 공간 (최소 500MB)

### ⚙️ 설정 확인
```bash
# API 키 개수 확인
cat config/.env | grep "^OPENAI_API_KEY" | wc -l
# 결과: 10

# DB 연결 확인
PGPASSWORD='wkwjsrj4510*' psql -h localhost -d recipe_ai_db -U recipe_keep -c "\dt"
```

---

## 🔧 수동 실행 (세밀한 제어)

### 1단계: DB 초기화 (선택)
```bash
PGPASSWORD='wkwjsrj4510*' psql -h localhost -d recipe_ai_db -U recipe_keep -c "TRUNCATE recipes CASCADE;"
```

### 2단계: 카테고리 설정
```bash
nano config/.env
```

**수정:**
```env
RECIPE_TYPE=밑반찬
RECIPE_SITUATION=일상
RECIPE_INGREDIENT=소고기
RECIPE_METHOD=볶음
MAX_RECIPES=50
```

### 3단계: 실행
```bash
source venv/bin/activate
python main.py
```

### 4단계: 다음 카테고리
`config/.env`를 다음 카테고리로 수정 후 반복

---

## 📊 진행 상황 모니터링

### 실시간 로그 확인
```bash
tail -f logs/main.log
```

### DB 통계 확인
```bash
PGPASSWORD='wkwjsrj4510*' psql -h localhost -d recipe_ai_db -U recipe_keep -c "
SELECT 
    COUNT(*) as recipes,
    (SELECT COUNT(*) FROM ingredients) as ingredients,
    (SELECT COUNT(*) FROM cooking_steps) as steps
FROM recipes;
"
```

### DBeaver에서 확인
1. DBeaver 실행
2. recipe_ai_db 연결
3. recipes 테이블 → F5 (새로고침)

---

## ⏱️ 예상 시간표

| 시점 | 누적 | 예상 시간 | 진행률 |
|------|------|-----------|--------|
| Phase 1 완료 | 400개 | ~30분 | 40% |
| Phase 2 완료 | 600개 | ~45분 | 60% |
| Phase 3 완료 | 800개 | ~60분 | 80% |
| Phase 4 완료 | 1000개 | ~75분 | 100% ✅ |

---

## 🔄 중단 후 재개

스크립트가 중단되면:

```bash
# 현재 DB 개수 확인
PGPASSWORD='wkwjsrj4510*' psql -h localhost -d recipe_ai_db -U recipe_keep -c "SELECT COUNT(*) FROM recipes;"

# 스크립트 편집하여 완료된 Phase 제거
nano run_batch_collection.sh

# 재실행
./run_batch_collection.sh
```

---

## 💾 백업

각 Phase 완료 후 백업 (추천):

```bash
# 백업
pg_dump -h localhost -U recipe_keep recipe_ai_db > backups/phase1_$(date +%Y%m%d_%H%M%S).sql

# 복구 (필요시)
PGPASSWORD='wkwjsrj4510*' psql -h localhost -d recipe_ai_db -U recipe_keep < backups/phase1_20251018_020000.sql
```

---

## ⚠️ 문제 해결

### API 429 에러 (Rate Limit)
- 10개 키로 분산되므로 거의 없음
- 발생 시: `TRANSLATION_DELAY=0.5`로 증가

### DB 연결 끊김
```bash
# PostgreSQL 재시작
sudo service postgresql restart
```

### 메모리 부족
- 배치 크기 줄이기: `MAX_RECIPES=25`

---

## 🎉 완료 후

### 1. 최종 통계 확인
```bash
PGPASSWORD='wkwjsrj4510*' psql -h localhost -d recipe_ai_db -U recipe_keep -c "
SELECT 
    COUNT(*) as total_recipes,
    COUNT(DISTINCT SUBSTRING(url FROM 'recipe/([0-9]+)')) as unique_ids,
    (SELECT COUNT(*) FROM ingredients) as total_ingredients,
    (SELECT COUNT(*) FROM cooking_steps) as total_steps
FROM recipes;
"
```

### 2. 데이터 품질 확인
- DBeaver에서 샘플 레시피 확인
- title_en 필드 번역 확인
- ingredients_en, cooking_steps_en 확인

### 3. 다음 단계
- [ ] AI 검색 시스템 구축 (pgvector)
- [ ] 영양소 데이터 추가
- [ ] API 서버 구축

---

## 🚀 **시작하기**

```bash
cd /home/keep/recipe-ai/recipe_ai_system
./run_batch_collection.sh
```

**커피 한 잔 하고 오세요! ☕**  
**약 1시간 10분 후 1000개 레시피가 준비됩니다!** 🎉

