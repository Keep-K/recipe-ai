# 📖 사용 가이드

Recipe AI System의 다양한 사용 방법

---

## 🎯 실행 방법

### **방법 1: 대화형 모드 (추천)**

```bash
cd /home/keep/recipe-ai/recipe_ai_system
source venv/bin/activate
python main.py
```

**실행 화면:**
```
============================================================
🍳 Recipe AI System
============================================================

⚠️  DB를 초기화하고 시작하시겠습니까? (y/N): 
```

**선택:**
- `y` 또는 `yes` → DB 초기화 후 시작
- `n` 또는 Enter → DB 유지하고 시작 (중복 자동 건너뛰기)

---

### **방법 2: 명령행 옵션**

#### DB 초기화하고 시작
```bash
python main.py --reset-db
```

#### DB 유지 (프롬프트 없이)
```bash
python main.py --no-prompt
# 중복 자동 건너뛰기
```

#### DB 유지 (대화형)
```bash
python main.py
# Enter 또는 'n' 입력
```

---

### **방법 3: 대량 수집 (자동화)**

```bash
./run_batch_collection.sh
```

**프롬프트 (한 번만):**
```
DB를 초기화하고 시작하시겠습니까? (y/N): 
```

**이후 자동 실행:**
- 배치 스크립트가 `python main.py --no-prompt` 호출
- 20개 배치를 중단 없이 자동 실행
- 중복 레시피는 자동으로 건너뛰기

---

## 📊 실행 시나리오

### **시나리오 1: 처음 시작 (DB 비어있음)**

```bash
python main.py
# → 'n' 입력 (DB 유지)
```

**결과:**
```
✅ Crawled 10 recipes
✅ Translated 10 recipes
✅ Saved 10/10 recipes to DB
```

---

### **시나리오 2: 계속 수집 (DB에 데이터 있음)**

```bash
python main.py
# → 'n' 입력 (DB 유지)
```

**결과:**
```
✅ Crawled 10 recipes
✅ Translated 10 recipes
⚠️  Skipped duplicate: 소고기볶음 (ID: 7014545)
⚠️  Skipped duplicate: 돼지고기볶음 (ID: 6957821)
✅ Saved 8/10 recipes to DB (2개 중복)
```

**자동으로 중복 건너뛰기!** ✨

---

### **시나리오 3: 새로 시작 (기존 데이터 삭제)**

```bash
python main.py
# → 'y' 입력 (DB 초기화)
```

**결과:**
```
🗑️  DB 초기화 중...
✅ DB 초기화 완료

✅ Crawled 10 recipes
✅ Translated 10 recipes
✅ Saved 10/10 recipes to DB
```

---

### **시나리오 4: 1000개 대량 수집**

```bash
./run_batch_collection.sh
# → 'y' 입력 (DB 초기화)
```

**결과:**
```
[1/20] Phase 1-1: 소고기볶음
✅ Saved 50/50 recipes to DB

[2/20] Phase 1-2: 소고기구이
✅ Saved 50/50 recipes to DB

...

진행: 20/20 완료 | 수집: 1000개
✅ 작업 완료!
```

---

## 🔄 중복 처리

### **자동 중복 체크**

DB에 이미 있는 레시피는 자동으로 건너뜁니다:

```python
# database.py
def insert_recipe(self, recipe: Dict):
    # 중복 체크
    if self.cursor.fetchone():
        logger.warning(f"⚠️  Skipped duplicate: {title}")
        return None
```

**장점:**
- ✅ 같은 카테고리 재수집 가능
- ✅ 에러 없이 부드럽게 건너뛰기
- ✅ 로그에서 중복 확인 가능

---

## 🛠️ 고급 사용법

### **1. 특정 카테고리만 수집**

```bash
# config/.env 수정
nano config/.env
```

```env
RECIPE_TYPE=밑반찬
RECIPE_INGREDIENT=닭고기
RECIPE_METHOD=구이
MAX_RECIPES=50
```

```bash
python main.py
```

---

### **2. 여러 카테고리 순차 수집**

```bash
# 소고기 볶음
sed -i 's/RECIPE_INGREDIENT=.*/RECIPE_INGREDIENT=소고기/' config/.env
python main.py  # DB 유지 ('n')

# 돼지고기 볶음
sed -i 's/RECIPE_INGREDIENT=.*/RECIPE_INGREDIENT=돼지고기/' config/.env
python main.py  # DB 유지 ('n')

# 닭고기 볶음
sed -i 's/RECIPE_INGREDIENT=.*/RECIPE_INGREDIENT=닭고기/' config/.env
python main.py  # DB 유지 ('n')
```

**결과:** 3개 카테고리 모두 DB에 누적

---

### **3. 번역 수정만 실행**

```bash
python fix_missing_translations.py
```

---

### **4. 번역 캐시 초기화**

```bash
rm -f logs/translation_cache.json
python main.py
```

번역을 처음부터 다시 수행

---

## 🚫 DB 초기화 시 주의사항

### **언제 초기화해야 하나요?**

✅ **초기화하는 경우:**
- 완전히 새로 시작
- 테스트 데이터 제거
- 카테고리 변경 후 재수집

❌ **초기화하지 않는 경우:**
- 다른 카테고리 추가 수집
- 번역 누락 수정
- 중복 레시피 확인

### **백업 먼저!**

```bash
# DB 백업
pg_dump -h localhost -U recipe_keep recipe_ai_db > backups/backup_$(date +%Y%m%d_%H%M%S).sql

# 백업 복구 (필요시)
psql -h localhost -d recipe_ai_db -U recipe_keep < backups/backup_20251018_020000.sql
```

---

## 📊 진행 상황 확인

### **실시간 로그 확인**

```bash
# 터미널 1: 실행
python main.py

# 터미널 2: 로그 모니터링
tail -f logs/main.log
```

---

### **DB 통계 확인**

```bash
PGPASSWORD='wkwjsrj4510*' psql -h localhost -d recipe_ai_db -U recipe_keep -c "
SELECT 
    COUNT(*) as total_recipes,
    (SELECT COUNT(*) FROM ingredients) as total_ingredients,
    (SELECT COUNT(*) FROM cooking_steps) as total_steps
FROM recipes;
"
```

---

### **번역 상태 확인**

```bash
PGPASSWORD='wkwjsrj4510*' psql -h localhost -d recipe_ai_db -U recipe_keep -c "
SELECT 
    COUNT(*) as total,
    COUNT(title_en) as translated,
    COUNT(*) - COUNT(title_en) as missing
FROM recipes;
"
```

---

## 🔧 문제 해결

### **Q: "DB를 초기화하고 시작하시겠습니까?" 프롬프트가 안 나타납니다**

**원인**: 배경 실행 또는 리다이렉션

**해결:**
```bash
# 대화형으로 직접 실행
python main.py

# 또는 명령행 옵션 사용
python main.py --reset-db
```

---

### **Q: 중복 레시피가 계속 수집됩니다**

**확인:**
```bash
# 로그 확인
grep "Skipped duplicate" logs/main.log
```

**원인**: URL이 다른 같은 레시피

**해결**: 정상 동작 (URL 기준으로 중복 체크)

---

### **Q: 번역이 누락되었습니다**

**자동 수정:**
```bash
python main.py  # 자동으로 Step 4에서 수정
```

**또는:**
```bash
python fix_missing_translations.py
```

---

## 🎯 모범 사례

### **1. 처음 시작**
```bash
# 1. DB 초기화하고 시작
python main.py --reset-db

# 2. 10개 테스트
# 3. DBeaver에서 확인
# 4. 문제 없으면 대량 수집
./run_batch_collection.sh
```

---

### **2. 카테고리별 수집**
```bash
# DB 유지하면서 다양한 카테고리 누적
for ingredient in 소고기 돼지고기 닭고기; do
    sed -i "s/RECIPE_INGREDIENT=.*/RECIPE_INGREDIENT=$ingredient/" config/.env
    python main.py  # 'n' 입력 (DB 유지)
done
```

---

### **3. 안전한 대량 수집**
```bash
# 1. 백업
pg_dump -h localhost -U recipe_keep recipe_ai_db > backups/before_collection.sql

# 2. 수집
./run_batch_collection.sh

# 3. 확인
# SELECT COUNT(*) FROM recipes;

# 4. 문제 발생 시 복구
# psql ... < backups/before_collection.sql
```

---

## 📚 관련 문서

- [빠른 시작](QUICKSTART.md) - 첫 실행 가이드
- [번역 수정](TRANSLATION_FIXER.md) - 번역 누락 해결
- [멀티 API 키](MULTI_API_KEYS.md) - 성능 향상
- [1000개 수집](START_1000.md) - 대량 수집

---

**이제 안전하게 레시피를 수집하세요!** 🎉

