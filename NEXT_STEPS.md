# 🚀 다음 단계: AI 벡터 검색 구축

## 📋 현재 상태

✅ **완료된 작업**:
- 136개 레시피 수집
- 한영 자동 번역 (100% 완료)
- PostgreSQL DB 저장
- 벡터화 시스템 구축

🚧 **다음 작업**:
- pgvector 설치
- 레시피 벡터화
- 검색 시스템 테스트

---

## 🔧 Step 1: 패키지 설치

```bash
cd /home/keep/recipe-ai/recipe_ai_system
source venv/bin/activate

# 필수 패키지 설치
pip install sentence-transformers pgvector torch numpy
```

**예상 시간**: 3-5분

---

## 🔧 Step 2: pgvector 설치

### Ubuntu/Debian

```bash
# PostgreSQL 버전 확인
psql --version

# pgvector 설치 (PostgreSQL 15)
sudo apt-get update
sudo apt-get install postgresql-15-pgvector
```

### 설치 확인

```bash
PGPASSWORD='wkwjsrj4510*' psql -h localhost -d recipe_ai_db -U recipe_keep -c "CREATE EXTENSION IF NOT EXISTS vector;"
```

---

## 🔧 Step 3: DB에 벡터 컬럼 추가

```bash
PGPASSWORD='wkwjsrj4510*' psql -h localhost -d recipe_ai_db -U recipe_keep -f db/add_vector_column.sql
```

**예상 출력**:
```
CREATE EXTENSION
ALTER TABLE
CREATE INDEX
 column_name |   data_type   
-------------+---------------
 embedding   | USER-DEFINED
```

---

## 🔧 Step 4: 레시피 벡터화

### Option A: OpenAI Embeddings (추천)

```bash
# config/.env 확인
cat config/.env | grep USE_OPENAI_EMBEDDINGS
# USE_OPENAI_EMBEDDINGS=true

# 벡터화 실행
python vectorize_recipes.py
```

**예상 시간**: 2-3분 (136개 레시피)  
**예상 비용**: $0.002 (약 3원)

### Option B: SentenceTransformers (무료)

```bash
# config/.env 수정
nano config/.env
# USE_OPENAI_EMBEDDINGS=false

# 벡터화 실행
python vectorize_recipes.py
```

**예상 시간**: 30초-1분  
**비용**: 무료

---

## 🔧 Step 5: 검색 테스트

### 기본 검색

```bash
python search_recipes.py 'spicy chicken dish'
```

### 다양한 쿼리 테스트

```bash
# 건강한 요리
python search_recipes.py 'healthy protein recipe' 5

# 빠른 요리
python search_recipes.py 'quick and easy dinner'

# 매운 요리
python search_recipes.py 'spicy food'

# 다이어트 요리
python search_recipes.py 'diet low calorie recipe'
```

---

## 📊 예상 결과

```
================================================================================
✅ 검색 결과: 5개
================================================================================

1. [124] Stir-fried chicken breast with mushrooms~~
   한글: 다이어트하시분들!!닭가슴살 버섯볶음~~
   설명: A healthy and delicious chicken breast and mushroom stir-fry...
   조리 시간: 20분 | 인분: 2인분
   유사도: 0.887 (88.7%)

2. [125] Simple side dish making, stir-fried chicken breast with garlic shoots
   한글: 간단한 밑반찬 만들기, 닭가슴살 마늘쫑 볶음
   설명: Quick and easy chicken breast recipe...
   조리 시간: 15분 | 인분: 2인분
   유사도: 0.856 (85.6%)

...
```

---

## 🛠️ 문제 해결

### pgvector 설치 실패

```bash
# 소스에서 컴파일
cd /tmp
git clone --branch v0.5.1 https://github.com/pgvector/pgvector.git
cd pgvector
make
sudo make install
```

### torch 설치 너무 느림

```bash
# CPU 전용 torch (크기 작음)
pip install torch --index-url https://download.pytorch.org/whl/cpu
```

### SentenceTransformers 모델 다운로드 느림

```bash
# 처음 실행 시 모델 다운로드 (약 100MB)
# 다운로드 진행률이 표시됩니다
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"
```

---

## 🎯 다음 단계 (향후 개발)

### 1. REST API 서버 구축
- FastAPI 또는 Flask
- `/search` 엔드포인트
- `/recommend` 엔드포인트

### 2. 프론트엔드 개발
- React 또는 Vue.js
- 검색 UI
- 레시피 상세 페이지

### 3. 추천 시스템
- 사용자 기반 추천
- 콘텐츠 기반 추천
- 하이브리드 추천

### 4. 데이터 확장
- 1000개 레시피 수집
- 영양소 정보 추가
- 사용자 리뷰 수집

---

## 📚 참고 문서

- **[벡터화 빠른 시작](docs/VECTORIZATION_QUICKSTART.md)** - 상세 가이드
- **[벡터화 가이드](docs/VECTORIZATION_GUIDE.md)** - 기술 문서
- **[README](README.md)** - 프로젝트 개요

---

## ✅ 체크리스트

- [ ] 패키지 설치 완료
- [ ] pgvector 설치 완료
- [ ] DB에 벡터 컬럼 추가 완료
- [ ] 레시피 벡터화 완료
- [ ] 검색 테스트 성공

**모두 체크했다면 축하합니다! 🎉**

이제 `python search_recipes.py '원하는 검색어'`로 AI 검색을 사용할 수 있습니다!
