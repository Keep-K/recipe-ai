# Railway 환경 변수 설정 가이드

## 🔵 PostgreSQL 서비스 Variables

```
POSTGRES_USER=keep_ai
POSTGRES_PASSWORD=Pwkwjsrj4510*
POSTGRES_DB=recipe_ai
```

## 🟢 FastAPI 서비스 Variables

### 필수 변수

```
# PostgreSQL 연결 (내부 호스트 사용)
DATABASE_URL=postgresql://keep_ai:Pwkwjsrj4510*@recipe-ai-db.railway.internal:5432/recipe_ai

# OpenAI API 키
OPENAI_API_KEY=sk-...본인의_OpenAI_API_키
```

### 선택 변수 (기본값 있음)

```
# OpenAI 모델 (기본값: gpt-4o-mini)
OPENAI_MODEL=gpt-4o-mini

# OpenAI Embeddings 사용 여부 (기본값: true)
USE_OPENAI_EMBEDDINGS=true
```

## 📝 Railway 설정 방법

### FastAPI 서비스 Variables 탭에서:

1. **Raw Editor** 클릭
2. 아래 형식으로 입력:
   ```
   DATABASE_URL=postgresql://keep_ai:Pwkwjsrj4510*@recipe-ai-db.railway.internal:5432/recipe_ai
   OPENAI_API_KEY=sk-your-actual-openai-key-here
   OPENAI_MODEL=gpt-4o-mini
   USE_OPENAI_EMBEDDINGS=true
   ```
3. **Save** 클릭

## ⚠️ 중요 참고사항

- `DATABASE_URL`의 호스트는 PostgreSQL 서비스 이름에 따라 변경될 수 있습니다
  - 서비스 이름이 다르면: `<서비스-이름>.railway.internal`
- `OPENAI_API_KEY`는 실제 키를 입력해야 합니다
- `DATABASE_URL`에 특수문자(`*`)가 포함되어 있으므로 URL 인코딩 필요할 수 있음
  - `*` → `%2A`
  - 예: `Pwkwjsrj4510*` → `Pwkwjsrj4510%2A`

## 🔗 자동 연결 방법 (권장)

Railway에서 FastAPI 서비스 → Settings → Connect to Other Services → PostgreSQL 서비스 선택
- Railway가 자동으로 `DATABASE_URL` 생성
- 수동으로 추가할 필요 없음!

