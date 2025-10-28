# 🗄️ PostgreSQL DB 설정 완벽 가이드

## 📋 **전체 과정 요약**

1. **postgres 사용자로 전환** → DB 및 사용자 생성
2. **스키마 생성** → 테이블 생성
3. **연결 테스트** → 정상 작동 확인

---

## 🚀 **Step 1: 새 데이터베이스 및 사용자 생성**

### 명령어 실행:

```bash
sudo -u postgres psql
```

### PostgreSQL 프롬프트에서 실행:

```sql
-- 1. 새 데이터베이스 생성
CREATE DATABASE recipe_ai_db;

-- 2. 새 사용자 생성 (비밀번호 설정)
CREATE USER recipe_keep WITH PASSWORD 'wkwjsrj4510*' CREATEDB;

-- 3. 데이터베이스 권한 부여
GRANT ALL PRIVILEGES ON DATABASE recipe_ai_db TO recipe_ai;

-- 4. recipe_ai_db로 전환
\c recipe_ai_db

-- 5. 스키마 권한 부여
GRANT ALL ON SCHEMA public TO recipe_keep;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO recipe_keep;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO recipe_keep;

-- 6. 확인
\du

-- 7. 종료
\q
```

---

## 🏗️ **Step 2: 스키마(테이블) 생성**

```bash
cd /home/keep/recipe-ai/recipe_ai_system
psql -d recipe_ai_db -U recipe_ai -f db/schema.sql
```

**비밀번호 입력**: `wkwjsrj4510*`

---

## ✅ **Step 3: 연결 테스트**

```bash
# 연결 테스트
psql -d recipe_ai_db -U recipe_ai -c "\dt"
```

**비밀번호 입력**: `wkwjsrj4510*`

**예상 출력:**
```
           List of relations
 Schema |      Name      | Type  |   Owner   
--------+----------------+-------+-----------
 public | cooking_steps  | table | recipe_ai
 public | ingredients    | table | recipe_ai
 public | recipes        | table | recipe_ai
(3 rows)
```

---

## 🎯 **한 번에 실행하기 (자동화)**

위의 모든 과정을 파일로 만들어서 한 번에 실행:

```bash
cd /home/keep/recipe-ai/recipe_ai_system

# DB 생성 및 사용자 생성
sudo -u postgres psql -f db/init.sql

# 스키마 생성
psql -d recipe_ai_db -U recipe_ai -f db/schema.sql
# 비밀번호: wkwjsrj4510*
```

---

## 🔍 **생성된 것 확인**

### 데이터베이스 확인
```bash
psql -d postgres -c "\l" | grep recipe_ai_db
```

### 사용자 확인
```bash
psql -d postgres -c "\du" | grep recipe_ai
```

### 테이블 확인
```bash
psql -d recipe_ai_db -U recipe_ai -c "\dt"
```

### 테이블 구조 확인
```bash
psql -d recipe_ai_db -U recipe_ai -c "\d recipes"
psql -d recipe_ai_db -U recipe_ai -c "\d ingredients"
psql -d recipe_ai_db -U recipe_ai -c "\d cooking_steps"
```

---

## 📊 **스키마 상세 설명**

### **1. recipes 테이블 (1개 레시피 = 1개 행)**

| 컬럼명 | 타입 | 설명 | 예시 |
|--------|------|------|------|
| `id` | SERIAL | 자동 증가 ID | 1, 2, 3, ... |
| `recipe_id` | VARCHAR(20) | 원본 ID | "6854979" |
| `title` | VARCHAR(300) | 한글 제목 | "소고기두부볶음" |
| `title_en` | VARCHAR(300) | 영문 제목 | "Beef Tofu Stir-fry" |
| `description` | TEXT | 한글 설명 | "맛있는 반찬..." |
| `description_en` | TEXT | 영문 설명 | "Delicious side dish..." |
| `difficulty` | ENUM | 난이도 | easy/medium/hard |

### **2. ingredients 테이블 (1개 재료 = 1개 행)**

**예시: 레시피 ID 1의 재료들**

| id | recipe_id | name | name_en |
|----|-----------|------|---------|
| 1 | **1** | 두부 1/2모 | Tofu 1/2 piece |
| 2 | **1** | 소고기 140g | Beef 140g |
| 3 | **1** | 간장 1큰술 | Soy sauce 1 tbsp |

→ `recipe_id = 1`로 묶여있음 (외래키)

### **3. cooking_steps 테이블 (1개 단계 = 1개 행)**

**예시: 레시피 ID 1의 조리 단계**

| id | recipe_id | step_number | description | description_en |
|----|-----------|-------------|-------------|----------------|
| 1 | **1** | **1** | 1. 소고기 준비 | 1. Prepare beef |
| 2 | **1** | **2** | 2. 야채 썰기 | 2. Cut vegetables |
| 3 | **1** | **3** | 3. 팬에 볶기 | 3. Stir-fry in pan |

→ `recipe_id = 1`, `step_number`로 순서 보장

---

## 🔗 **관계 도식화**

```
recipes (id=1)
├─ title: "소고기두부볶음"
├─ title_en: "Beef Tofu Stir-fry"
├─ difficulty: "medium"
│
├─ ingredients (recipe_id=1)
│   ├─ (id=1) 두부 1/2모
│   ├─ (id=2) 소고기 140g
│   └─ (id=3) 간장 1큰술
│
└─ cooking_steps (recipe_id=1)
    ├─ (step 1) 소고기 준비
    ├─ (step 2) 야채 썰기
    └─ (step 3) 팬에 볶기
```

---

## 💡 **왜 이렇게 나눴나요?**

### **장점:**

1. **정규화**: 재료와 조리단계를 별도 테이블로 분리
2. **확장성**: 레시피당 재료/단계 개수 제한 없음
3. **검색 최적화**: 인덱스로 빠른 조회
4. **데이터 무결성**: 외래키로 관계 보장

### **조회 예시:**

```sql
-- 레시피 1의 모든 정보 가져오기
SELECT 
    r.title,
    r.title_en,
    r.difficulty,
    i.name as ingredient,
    i.name_en as ingredient_en
FROM recipes r
LEFT JOIN ingredients i ON r.id = i.recipe_id
WHERE r.id = 1;

-- 조리 단계 순서대로 가져오기
SELECT 
    r.title,
    cs.step_number,
    cs.description,
    cs.description_en
FROM recipes r
JOIN cooking_steps cs ON r.id = cs.recipe_id
WHERE r.id = 1
ORDER BY cs.step_number;
```

---

## 🎯 **실행 순서 정리**

```bash
# 1. postgres 사용자로 전환하여 DB 생성
sudo -u postgres psql -f db/init.sql

# 2. 생성한 사용자로 스키마 생성
psql -d recipe_ai_db -U recipe_ai -f db/schema.sql
# 비밀번호: wkwjsrj4510*

# 3. 확인
psql -d recipe_ai_db -U recipe_ai -c "\dt"
# 비밀번호: wkwjsrj4510*
```

---

**이제 위의 명령어들을 순서대로 실행하시면 됩니다!** 🚀

궁금한 점 있으시면 언제든지 물어보세요!

