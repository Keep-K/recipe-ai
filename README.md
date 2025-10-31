# 🍳 Recipe AI System

한국 레시피 자동 수집, 번역 및 AI 추천 시스템

---

## ⚡ 빠른 시작

```bash
# 1. 설치
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 2. 환경 설정
cp config/env_template.txt config/.env
nano config/.env  # API 키 입력

# 3. DB 설정
psql -h localhost -d recipe_ai_db -U recipe_keep -f db/schema.sql

# 4. 실행
python main.py
```

**상세 가이드**: [docs/QUICKSTART.md](docs/QUICKSTART.md)

---

## 🎯 주요 기능

### ✅ **고속 크롤링**
- 10000recipe.com에서 레시피 자동 수집
- 카테고리별 필터링 지원
- 병렬 처리로 빠른 수집

### ✅ **AI 번역**
- 10개 API 키 병렬 처리
- 한국어만 선택 번역 (토큰 절약)
- 자동 캐싱으로 중복 방지
- **Thread-safe 병렬 처리** (딕셔너리 동시 접근 안전)
- **번역 누락 자동 수정** (JSON에서 자동 복구)
- **성능**: 10개 레시피 = 41초 ⚡

### ✅ **PostgreSQL 저장**
- 정규화된 스키마 (recipes, ingredients, cooking_steps)
- 중복 체크 자동화
- 영문 번역 별도 컬럼

### ✅ **AI 벡터 검색** 🆕
- OpenAI Embeddings 또는 SentenceTransformers
- pgvector로 빠른 유사도 검색
- 자연어 쿼리 지원
- 하이브리드 검색 (키워드 + 의미)
- 유사 레시피 추천

---

## 📊 성능

| 설정 | 10개 | 100개 | 1000개 |
|------|------|-------|--------|
| 단일 API 키 | 7분 | 70분 | 700분 |
| **10개 API 키 + 병렬** | **41초** ⚡ | **7분** ⚡ | **70분** ⚡ |

**개선율**: 10배 빠름 🔥

**상세 정보**: [docs/PERFORMANCE.md](docs/PERFORMANCE.md)

---

## 📚 문서 목록

### 🚀 시작하기
- **[빠른 시작](docs/QUICKSTART.md)** - 5분 안에 시작하기
- **[DB 설정 가이드](docs/DB_SETUP_GUIDE.md)** - PostgreSQL 설정
- **[멀티 API 키 설정](docs/MULTI_API_KEYS.md)** - 성능 10배 향상
- **[번역 누락 자동 수정](docs/TRANSLATION_FIXER.md)** - 자동 복구 시스템
- **[벡터화 빠른 시작](docs/VECTORIZATION_QUICKSTART.md)** 🆕 - AI 검색 구축
- **[FastAPI 서버 가이드](docs/FASTAPI_SERVER_GUIDE.md)** 🆕 - 채팅 AI 서버 실행

### 📖 대량 수집
- **[1000개 수집 가이드](docs/START_1000.md)** - 자동화 스크립트
- **[10,000개 수집 가이드](docs/COLLECT_10K_GUIDE.md)** 🆕 - 대규모 DB 구축 (10시간)
- **[추가 레시피 수집 가이드](docs/ADD_MORE_RECIPES.md)** 🆕 - 기존 DB에 레시피 추가
- **[수집 계획](docs/COLLECTION_PLAN.md)** - 카테고리별 전략

### ⚙️ 고급
- **[성능 최적화](docs/PERFORMANCE.md)** - 병렬 처리 & 최적화
- **[벡터화 가이드](docs/VECTORIZATION_GUIDE.md)** 🆕 - AI 임베딩 상세 가이드

---

## 🗂️ 프로젝트 구조

```
recipe_ai_system/
├── main.py                 # 메인 실행 파일
├── src/                    # 소스 코드
│   ├── crawler.py          # 크롤러
│   ├── translator.py       # 번역기 (멀티 API 키)
│   └── database.py         # DB 관리
├── config/                 # 설정
│   ├── .env                # 환경 변수 (비밀)
│   └── env_template.txt    # 템플릿
├── db/                     # 데이터베이스
│   ├── schema.sql          # 테이블 스키마
│   └── init.sql            # 초기화
├── docs/                   # 📚 문서
│   ├── QUICKSTART.md
│   ├── DB_SETUP_GUIDE.md
│   ├── MULTI_API_KEYS.md
│   ├── PERFORMANCE.md
│   ├── START_1000.md
│   └── COLLECTION_PLAN.md
├── data/                   # JSON 백업
├── logs/                   # 실행 로그
└── backups/                # DB 백업
```

---

## 🛠️ 기술 스택

- **언어**: Python 3.8+
- **크롤링**: requests, BeautifulSoup4
- **번역**: OpenAI API (gpt-4o-mini)
- **데이터베이스**: PostgreSQL 14+
- **병렬 처리**: ThreadPoolExecutor

---

## 📋 환경 변수

```env
# OpenAI API (10개까지)
OPENAI_API_KEY=sk-proj-...
OPENAI_API_KEY_2=sk-proj-...
...
OPENAI_API_KEY_10=sk-proj-...

# 모델 설정
OPENAI_MODEL=gpt-4o-mini
TRANSLATION_DELAY=0.3

# DB 설정
DB_NAME=recipe_ai_db
DB_USER=recipe_keep
DB_PASSWORD=wkwjsrj4510*

# 크롤링 설정
MAX_RECIPES=10
RECIPE_TYPE=밑반찬
RECIPE_INGREDIENT=소고기
RECIPE_METHOD=볶음
```

**전체 설정**: [config/env_template.txt](config/env_template.txt)

---

## 🎯 사용 예시

### 10개 레시피 수집 (대화형)
```bash
python main.py
# DB 초기화 여부 선택 가능
```

### 10개 레시피 수집 (DB 초기화)
```bash
python main.py --reset-db
```

### 10개 레시피 수집 (프롬프트 없이)
```bash
python main.py --no-prompt
# DB 유지, 중복 자동 건너뛰기
```

### 1000개 자동 수집
```bash
./run_batch_collection.sh
# 배치 스크립트에서 DB 초기화 한 번만 물어봄
# 이후 main.py는 자동으로 --no-prompt로 실행
```

### 🚀 FastAPI 서버 실행 (채팅 AI)
```bash
# 1. 가상환경 활성화
source venv/bin/activate

# 2. API 의존성 설치
pip install -r requirements_api.txt

# 3. 환경 변수 설정
cp config/env_template.txt config/.env
nano config/.env  # OpenAI API 키 입력

# 4. 서버 실행
python api_server.py
# 서버가 http://localhost:8000 에서 실행됩니다

# 5. API 문서 확인
# 브라우저에서 http://localhost:8000/docs 접속
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

---

## 🔧 유지보수

### DB 초기화
```bash
PGPASSWORD='wkwjsrj4510*' psql -h localhost -d recipe_ai_db -U recipe_keep -c "TRUNCATE recipes CASCADE;"
```

### 캐시 정리
```bash
rm -f logs/translation_cache.json
```

### 백업
```bash
pg_dump -h localhost -U recipe_keep recipe_ai_db > backups/backup_$(date +%Y%m%d).sql
```

---

## 📊 현재 상태

- ✅ 크롤러: 완성
- ✅ 번역기: 10배 최적화 완료 (Thread-safe)
- ✅ DB: 중복 체크 + 번역 누락 자동 수정
- ✅ 자동화: 1000개 배치 스크립트
- ✅ AI 검색: pgvector + OpenAI Embeddings 완성
- ✅ API 서버: FastAPI 채팅 AI 완성
- 🚧 영양소 데이터: 개발 예정

---

## 🎯 다음 단계

1. **AI 검색 시스템** (pgvector + OpenAI Embeddings)
   - "간단한 단백질 요리" → 관련 레시피 추천
   
2. **영양소 데이터베이스**
   - 식품영양성분 DB 연동
   - 칼로리, 단백질 자동 계산

3. **API 서버** ✅
   - FastAPI 구축 완료
   - RESTful API 제공
   - 채팅 AI 인터페이스

---

## 📄 라이선스

MIT License

---

## 👤 작성자

Recipe AI Team

---

## 🙏 감사

- [10000recipe.com](https://www.10000recipe.com) - 레시피 데이터
- OpenAI - GPT API
- PostgreSQL - 데이터베이스

---

**시작하기**: [docs/QUICKSTART.md](docs/QUICKSTART.md) 📖
# recope-ai
