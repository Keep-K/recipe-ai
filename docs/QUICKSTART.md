# ⚡ Quick Start - Recipe AI System

## 🚀 3분 완성 가이드

### 1. DB 생성 (1분)

```bash
cd /home/keep/recipe-ai/recipe_ai_system

# 새 데이터베이스 및 사용자 생성
sudo -u postgres psql -f db/init.sql

# 스키마 생성
psql -d recipe_ai_db -f db/schema.sql
```

### 2. API 키 설정 (30초)

```bash
# .env 파일 확인 및 수정
nano config/.env
```

**필수**: `OPENAI_API_KEY=your-actual-key-here` 입력

### 3. 실행 (1분 30초)

```bash
# 가상환경 활성화
source venv/bin/activate

# 전체 파이프라인 실행
python main.py
```

**자동으로 실행되는 것:**
- ✅ 10개 레시피 크롤링
- ✅ 한글만 선택 번역
- ✅ DB에 저장
- ✅ JSON 파일로도 백업

---

## 🔍 결과 확인

### 터미널에서
```bash
psql -d recipe_ai_db -c "SELECT id, title_en, difficulty FROM recipes LIMIT 5;"
```

### DBeaver에서
```
Database: recipe_ai_db
Username: recipe_keep
Password: wkwjsrj4510*
```

---

## ⚙️ 설정 변경

`config/.env` 파일 수정:

```env
MAX_RECIPES=20            # 더 많은 레시피
RECIPE_INGREDIENT=닭고기   # 재료 변경
OPENAI_MODEL=gpt-3.5-turbo # 모델 변경
```

---

## 📊 로그 확인

```bash
tail -f logs/main.log
```

---

## 🔄 DB 초기화

```bash
psql -d recipe_ai_db -c "TRUNCATE recipes CASCADE;"
```

---

**완료! 이제 AI 레시피 검색 시스템을 구축할 준비가 되었습니다.** 🎉

