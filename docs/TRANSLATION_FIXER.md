# 🔧 번역 누락 자동 수정 가이드

번역이 누락된 레시피를 자동으로 찾아서 수정하는 시스템

---

## ✨ 주요 기능

### **자동 통합**
- ✅ `main.py` 실행 시 자동으로 번역 누락 검사 및 수정
- ✅ JSON 파일에서 번역 자동 검색
- ✅ DB에 자동 업데이트
- ✅ Thread-safe 처리

### **수동 실행 (선택사항)**
- 번역 수정만 별도로 실행 가능
- 기존 레시피 재검증

---

## 🚀 사용 방법

### **방법 1: 자동 실행 (추천)**

```bash
# main.py 실행 시 자동으로 번역 누락 체크 및 수정
python main.py
```

**출력 예시:**
```
📖 Step 1: Crawling recipes...
✅ Crawled 10 recipes

🌐 Step 2: Translating recipes...
✅ Translated 10 recipes

💾 Step 3: Saving to database...
✅ Saved 10/10 recipes to DB

🔧 Step 4: Fixing missing translations...
🔍 번역 누락된 레시피: 3개
✅ [4] 볶음밥, 주먹밥 어디든 잘 어울리는 '만능 소고기볶음'... - title, 8 ingredients, 4 steps
✅ [8] 오이소고기볶음... - title, 11 ingredients, 11 steps
✅ [16] 소고기표고버섯볶음 쫄깃하고 맛있는 밑반찬 ... - title, 10 ingredients, 4 steps

📊 번역 수정 결과
   총 누락: 3개
   ✅ 수정 완료: 3개
   ⚠️  JSON 없음: 0개
   ❌ 실패: 0개
```

---

### **방법 2: 수동 실행 (선택사항)**

번역 수정만 별도로 하고 싶을 때:

```bash
python fix_missing_translations.py
```

---

## 🔍 작동 원리

### **1. 번역 누락 검사**
```sql
SELECT id, title 
FROM recipes 
WHERE title_en IS NULL OR title_en = ''
```

### **2. JSON에서 번역 찾기**
```python
# data/ 폴더의 모든 JSON 파일 검색
for json_file in glob('data/recipes_*.json'):
    # 제목으로 매칭
    if recipe['title'] == db_title:
        if recipe['title_en']:
            # 번역 발견!
```

### **3. DB 업데이트**
```python
# 제목 번역
UPDATE recipes SET title_en = ...

# 재료 번역
UPDATE ingredients SET name_en = ...

# 조리 단계 번역
UPDATE cooking_steps SET description_en = ...
```

---

## 📊 수정 항목

각 레시피에 대해 다음 항목을 자동 수정합니다:

1. **제목** (`title_en`)
2. **설명** (`description_en`)
3. **재료** (`ingredients.name_en`)
4. **조리 단계** (`cooking_steps.description_en`)

---

## ⚙️ 설정

### **자동 실행 비활성화**

`main.py`에서 자동 실행을 끄고 싶다면:

```python
# main.py 수정
system.run(
    save_json=True,
    fix_translations=False  # 비활성화
)
```

---

## 🛠️ 고급 사용

### **독립 모듈로 사용**

```python
from src.database import RecipeDB
from src.translation_fixer import TranslationFixer

# DB 연결
db = RecipeDB('recipe_ai_db', 'recipe_keep')
db.connect()

# 번역 수정
fixer = TranslationFixer(db)
result = fixer.fix_all_missing_translations()

print(f"수정 완료: {result['fixed']}개")

db.close()
```

---

## 📋 결과 해석

### **성공 케이스**
```
✅ [25] 소고기 다짐육 요리... - title, 10 ingredients, 10 steps
```
- 제목, 10개 재료, 10개 조리 단계 번역 완료

### **JSON 없음**
```
⚠️  [76] 만들어두면 유용한 고추장돼지고기볶음... - JSON에서 찾을 수 없음
```
- 해당 레시피의 번역이 JSON 파일에 없음
- 원인: 원본 수집 시 번역 실패
- 해결: 레시피를 다시 수집하거나 수동 번역

### **실패 케이스**
```
❌ [100] 레시피 제목... - 실패: error message
```
- DB 업데이트 중 오류 발생
- 로그에서 상세 오류 확인

---

## 🔧 문제 해결

### **Q: JSON 파일에서 번역을 찾을 수 없다고 나옵니다**

**원인**: 해당 레시피가 번역되지 않았거나 JSON 파일이 없음

**해결책**:
1. 레시피를 다시 수집
2. 또는 수동으로 번역 추가

---

### **Q: 모든 레시피가 "JSON 없음"으로 나옵니다**

**원인**: `data/` 폴더에 JSON 파일이 없음

**확인**:
```bash
ls -l data/recipes_*.json
```

**해결책**:
- `main.py`를 한 번 실행하여 JSON 파일 생성
- 또는 기존 JSON 파일을 `data/` 폴더에 복사

---

### **Q: 번역이 이상하게 수정됩니다**

**원인**: 잘못된 JSON 파일 또는 매칭 오류

**확인**:
```bash
# JSON 파일 확인
cat data/recipes_YYYYMMDD_HHMMSS.json | grep "title_en"
```

---

## 📊 성능

- **검사 속도**: 초당 ~1000개 레시피
- **수정 속도**: 초당 ~50개 레시피
- **메모리**: JSON 파일 크기에 비례 (~100MB/10,000개)

---

## 🎯 모범 사례

### **1. 정기적인 검증**
```bash
# 주기적으로 실행하여 누락 확인
python fix_missing_translations.py
```

### **2. JSON 백업**
```bash
# 번역된 JSON 파일은 삭제하지 말고 보관
ls data/recipes_*.json
```

### **3. 로그 확인**
```bash
# 수정 내역 확인
tail -f logs/main.log
```

---

## 🔒 안전성

- ✅ **Transaction 기반**: 실패 시 자동 롤백
- ✅ **중복 체크**: 같은 레시피 중복 수정 방지
- ✅ **Read-only JSON**: JSON 파일은 수정하지 않음
- ✅ **원본 보존**: 한글 원문은 그대로 유지

---

## 📈 통계 확인

```bash
# 번역 상태 확인
PGPASSWORD='wkwjsrj4510*' psql -h localhost -d recipe_ai_db -U recipe_keep -c "
SELECT 
    COUNT(*) as total,
    COUNT(title_en) as translated,
    COUNT(*) - COUNT(title_en) as missing
FROM recipes;
"
```

**결과 예시:**
```
 total | translated | missing 
-------+------------+---------
   100 |         98 |       2
```

---

## 🎉 요약

### **기본 사용**
```bash
# 자동으로 처리됨!
python main.py
```

### **수동 실행**
```bash
# 번역 수정만
python fix_missing_translations.py
```

### **상태 확인**
```bash
# SQL로 확인
psql -h localhost -d recipe_ai_db -U recipe_keep -c "
SELECT COUNT(*) FROM recipes WHERE title_en IS NULL;
"
```

---

**번역 누락은 이제 자동으로 해결됩니다!** ✨


