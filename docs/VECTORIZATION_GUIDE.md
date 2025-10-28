# 🤖 레시피 벡터화 가이드

## 📋 목차
1. [벡터화란?](#벡터화란)
2. [아키텍처 설계](#아키텍처-설계)
3. [기술 스택](#기술-스택)
4. [구현 단계](#구현-단계)
5. [사용 시나리오](#사용-시나리오)

---

## 🎯 벡터화란?

**벡터화(Vector Embedding)**는 텍스트 데이터를 고차원 숫자 벡터로 변환하여 AI가 의미를 이해하고 유사도를 계산할 수 있게 하는 기술입니다.

### **왜 필요한가?**

```
기존 키워드 검색:
  "닭가슴살 요리" 검색 → "닭가슴살"이 포함된 레시피만 찾음
  
벡터 검색 (의미 기반):
  "다이어트 단백질 요리" 검색 → 닭가슴살, 두부, 해산물 레시피 모두 찾음
  "매운 음식" 검색 → 고추장, 청양고추, 매운 양념 레시피 찾음
  "간단한 요리" 검색 → 조리 시간 짧고 재료 적은 레시피 찾음
```

---

## 🏗️ 아키텍처 설계

### **1. 데이터 구조**

```
레시피 벡터화 대상:
  ✅ 제목 (title_en)
  ✅ 설명 (description_en)
  ✅ 재료 목록 (ingredients_en)
  ✅ 조리 단계 (cooking_steps_en)
  
→ 통합 텍스트 생성 → 벡터 임베딩 → PostgreSQL 저장
```

### **2. 벡터 DB 선택**

**옵션 A: PostgreSQL + pgvector (추천)**
- ✅ 기존 DB에 통합 가능
- ✅ 설치 간단
- ✅ SQL로 벡터 검색 가능
- ✅ 하이브리드 검색 (키워드 + 벡터) 가능

**옵션 B: Pinecone / Weaviate**
- ❌ 별도 서비스 필요
- ❌ 추가 비용
- ✅ 대규모 데이터에 최적화

**옵션 C: ChromaDB**
- ✅ 경량
- ✅ Python 네이티브
- ❌ PostgreSQL과 분리

**→ 선택: PostgreSQL + pgvector**

---

## 🛠️ 기술 스택

### **임베딩 모델**

**옵션 1: OpenAI Embeddings (추천)**
```python
model: text-embedding-3-small
차원: 1536
가격: $0.02 / 1M tokens
속도: 빠름
품질: 매우 우수
```

**옵션 2: SentenceTransformers (무료)**
```python
model: all-MiniLM-L6-v2
차원: 384
가격: 무료
속도: 매우 빠름 (로컬)
품질: 우수
```

**옵션 3: Cohere Embeddings**
```python
model: embed-multilingual-v3.0
차원: 1024
가격: $0.10 / 1M tokens
품질: 다국어 지원 우수
```

**→ 추천: OpenAI (유료) + SentenceTransformers (백업)**

---

## 📦 구현 단계

### **Step 1: pgvector 설치**

```bash
# PostgreSQL에 pgvector 확장 설치 (소스에서 빌드)
sudo apt-get update
sudo apt-get install -y postgresql-server-dev-15 git build-essential

# pgvector 다운로드 및 설치
cd /tmp
git clone --branch v0.5.1 https://github.com/pgvector/pgvector.git
cd pgvector
make
sudo make install

# DB에 확장 활성화
psql -h localhost -d recipe_ai_db -U recipe_keep -c "CREATE EXTENSION IF NOT EXISTS vector;"
```

### **Step 2: 벡터 컬럼 추가**

```sql
-- recipes 테이블에 벡터 컬럼 추가
ALTER TABLE recipes ADD COLUMN embedding vector(1536);

-- 벡터 인덱스 생성 (빠른 검색)
CREATE INDEX ON recipes USING ivfflat (embedding vector_cosine_ops);
```

### **Step 3: Python 의존성 설치**

```bash
pip install openai sentence-transformers pgvector
```

### **Step 4: 벡터화 스크립트 작성**

```python
# src/vectorizer.py
from openai import OpenAI
from sentence_transformers import SentenceTransformer

class RecipeVectorizer:
    def __init__(self, use_openai=True):
        if use_openai:
            self.client = OpenAI()
            self.model = "text-embedding-3-small"
        else:
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
    
    def create_recipe_text(self, recipe):
        """레시피를 하나의 텍스트로 통합"""
        parts = [
            f"Title: {recipe['title_en']}",
            f"Description: {recipe['description_en']}",
            f"Ingredients: {', '.join(recipe['ingredients_en'])}",
            f"Steps: {' '.join(recipe['cooking_steps_en'])}"
        ]
        return "\n".join(parts)
    
    def vectorize(self, text):
        """텍스트를 벡터로 변환"""
        if isinstance(self.model, str):
            # OpenAI
            response = self.client.embeddings.create(
                model=self.model,
                input=text
            )
            return response.data[0].embedding
        else:
            # SentenceTransformers
            return self.model.encode(text).tolist()
```

### **Step 5: DB에 벡터 저장**

```python
# 모든 레시피 벡터화 및 저장
vectorizer = RecipeVectorizer(use_openai=True)

for recipe in recipes:
    text = vectorizer.create_recipe_text(recipe)
    embedding = vectorizer.vectorize(text)
    
    cursor.execute("""
        UPDATE recipes 
        SET embedding = %s
        WHERE id = %s
    """, (embedding, recipe['id']))
```

### **Step 6: 벡터 검색 구현**

```python
def search_recipes(query, top_k=10):
    """자연어 쿼리로 레시피 검색"""
    # 1. 쿼리를 벡터로 변환
    query_vector = vectorizer.vectorize(query)
    
    # 2. 코사인 유사도로 검색
    cursor.execute("""
        SELECT id, title, title_en, 
               1 - (embedding <=> %s::vector) as similarity
        FROM recipes
        WHERE embedding IS NOT NULL
        ORDER BY embedding <=> %s::vector
        LIMIT %s
    """, (query_vector, query_vector, top_k))
    
    return cursor.fetchall()
```

---

## 🎯 사용 시나리오

### **시나리오 1: 자연어 검색**

```python
# 사용자 쿼리: "건강한 단백질 요리"
results = search_recipes("healthy protein dishes", top_k=5)

# 결과:
# 1. 닭가슴살 샐러드 (similarity: 0.92)
# 2. 두부 스테이크 (similarity: 0.89)
# 3. 연어 구이 (similarity: 0.87)
# 4. 소고기 볶음 (similarity: 0.85)
# 5. 해산물 찜 (similarity: 0.83)
```

### **시나리오 2: 하이브리드 검색**

```python
# 벡터 검색 + 필터링
cursor.execute("""
    SELECT id, title, title_en, cooking_time,
           1 - (embedding <=> %s::vector) as similarity
    FROM recipes
    WHERE cooking_time <= 30  -- 30분 이내
      AND servings >= 2       -- 2인분 이상
    ORDER BY embedding <=> %s::vector
    LIMIT 10
""", (query_vector, query_vector))
```

### **시나리오 3: 유사 레시피 추천**

```python
def find_similar_recipes(recipe_id, top_k=5):
    """특정 레시피와 유사한 레시피 찾기"""
    cursor.execute("""
        SELECT r2.id, r2.title_en,
               1 - (r1.embedding <=> r2.embedding) as similarity
        FROM recipes r1, recipes r2
        WHERE r1.id = %s AND r2.id != %s
        ORDER BY r1.embedding <=> r2.embedding
        LIMIT %s
    """, (recipe_id, recipe_id, top_k))
    
    return cursor.fetchall()
```

---

## 🚀 성능 최적화

### **1. 배치 임베딩**

```python
# 한 번에 여러 레시피 처리
texts = [vectorizer.create_recipe_text(r) for r in recipes]
embeddings = vectorizer.vectorize_batch(texts)  # 배치 처리
```

### **2. 캐싱**

```python
# 이미 벡터화된 레시피는 건너뛰기
cursor.execute("SELECT COUNT(*) FROM recipes WHERE embedding IS NULL")
missing_count = cursor.fetchone()[0]

if missing_count == 0:
    print("✅ 모든 레시피가 이미 벡터화되었습니다!")
```

### **3. 인덱스 최적화**

```sql
-- IVFFlat 인덱스 (빠른 근사 검색)
CREATE INDEX ON recipes USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

-- HNSW 인덱스 (더 빠름, PostgreSQL 15+)
CREATE INDEX ON recipes USING hnsw (embedding vector_cosine_ops);
```

---

## 💰 비용 추정

### **OpenAI Embeddings**

```
레시피 136개 × 평균 500 토큰 = 68,000 토큰
68,000 토큰 ÷ 1,000,000 × $0.02 = $0.0014 (약 2원)

1,000개 레시피 = 약 $0.01 (약 14원)
10,000개 레시피 = 약 $0.10 (약 140원)
```

**→ 매우 저렴! OpenAI 사용 추천**

### **SentenceTransformers (무료)**

```
비용: $0
속도: 더 빠름 (로컬 처리)
품질: OpenAI보다 약간 낮음 (하지만 충분히 우수)
```

---

## 📚 다음 단계

1. **벡터화 구현** → `src/vectorizer.py` 작성
2. **pgvector 설치** → PostgreSQL 확장 활성화
3. **DB 마이그레이션** → 벡터 컬럼 추가
4. **벡터화 실행** → 모든 레시피 임베딩
5. **검색 API 구현** → REST API 서버 구축
6. **프론트엔드 연동** → 검색 UI 구축

---

## 🎯 최종 목표

```
사용자 입력: "매운 닭고기 요리 30분 이내"

AI 시스템:
  1. 자연어 이해 (벡터 검색)
  2. 필터 적용 (cooking_time <= 30)
  3. 유사도 순 정렬
  4. 추천 제공
  
결과:
  ✅ 매운 닭볶음 (25분, 유사도: 0.95)
  ✅ 닭가슴살 고추장볶음 (20분, 유사도: 0.92)
  ✅ 매운 닭강정 (30분, 유사도: 0.89)
```

---

**🚀 준비되셨나요? 벡터화 스크립트를 작성하겠습니다!**

