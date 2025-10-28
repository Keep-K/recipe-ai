# 🚀 FastAPI 서버 실행 가이드

Recipe AI 채팅 서버를 로컬에서 실행하는 방법을 안내합니다.

---

## 📋 사전 준비

### 1. 가상환경 활성화
```bash
cd /home/keep/recipe-ai/recipe_ai_system
source venv/bin/activate
```

### 2. API 의존성 설치
```bash
pip install -r requirements_api.txt
```

### 3. 환경 변수 설정
```bash
# 환경 변수 파일 복사
cp config/env_template.txt config/.env

# API 키 설정
nano config/.env
```

**필수 환경 변수:**
```env
# OpenAI API 키 (필수)
OPENAI_API_KEY=sk-proj-your-api-key-here

# 데이터베이스 설정
DB_NAME=recipe_ai_db
DB_USER=recipe_keep
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432
```

---

## 🚀 서버 실행

### 기본 실행
```bash
python api_server.py
```

**성공 시 출력:**
```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

### 개발 모드 실행 (자동 재시작)
```bash
uvicorn api_server:app --reload --host 0.0.0.0 --port 8000
```

---

## 🔍 서버 확인

### 1. 헬스 체크
```bash
curl http://localhost:8000/health
```

**응답:**
```json
{"status": "healthy", "message": "Recipe AI API is running"}
```

### 2. API 문서 확인
브라우저에서 접속:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### 3. 채팅 테스트
```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "오늘 저녁으로 닭고기 요리 추천해줘",
    "user_id": "test",
    "spiciness": "normal",
    "saltiness": "normal"
  }'
```

---

## 🛠️ 문제 해결

### 포트 충돌 오류
```bash
# 포트 8000 사용 중인 프로세스 확인
lsof -i :8000

# 프로세스 종료
pkill -f "python api_server.py"
# 또는
pkill -f "uvicorn"
```

### 데이터베이스 연결 오류
```bash
# PostgreSQL 서비스 상태 확인
sudo systemctl status postgresql

# 서비스 시작
sudo systemctl start postgresql

# 데이터베이스 연결 테스트
psql -h localhost -U recipe_keep -d recipe_ai_db
```

### 의존성 오류
```bash
# 가상환경 재생성
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements_api.txt
```

---

## 📊 API 엔드포인트

### 주요 엔드포인트

| 메서드 | 경로 | 설명 |
|--------|------|------|
| `GET` | `/health` | 서버 상태 확인 |
| `POST` | `/chat` | AI 채팅 |
| `GET` | `/recipe/{id}` | 레시피 상세 정보 |
| `GET` | `/search` | 레시피 검색 |

### 채팅 API 예시

**요청:**
```json
{
  "message": "매운 닭고기 요리 추천해줘",
  "user_id": "user123",
  "spiciness": "more",
  "saltiness": "normal"
}
```

**응답:**
```json
{
  "message": "매운 닭고기 요리를 추천해드릴게요!",
  "markdown_message": "## 🔥 매운 닭고기 요리 추천\n\n...",
  "recipes": [
    {
      "id": 123,
      "title": "매운 닭볶음탕",
      "title_en": "Spicy Chicken Stew",
      "description_en": "매콤한 닭고기 볶음탕...",
      "cooking_time": "30분",
      "servings": "4인분",
      "similarity": 0.95
    }
  ],
  "suggestions": ["더 매운 요리", "덜 매운 요리"]
}
```

---

## 🔧 개발 팁

### 로그 확인
```bash
# 실시간 로그 확인
tail -f logs/api.log

# 에러 로그만 확인
grep "ERROR" logs/api.log
```

### 성능 모니터링
```bash
# 메모리 사용량 확인
ps aux | grep python

# CPU 사용량 확인
top -p $(pgrep -f api_server.py)
```

### 디버그 모드
```bash
# 디버그 로그 활성화
export LOG_LEVEL=DEBUG
python api_server.py
```

---

## 🚀 프로덕션 배포

### 1. Gunicorn 사용
```bash
pip install gunicorn
gunicorn api_server:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### 2. Docker 사용
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements_api.txt .
RUN pip install -r requirements_api.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "api_server:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 3. 환경 변수 설정
```bash
export OPENAI_API_KEY=your-production-key
export DB_PASSWORD=your-production-password
export LOG_LEVEL=INFO
```

---

## 📚 추가 리소스

- [FastAPI 공식 문서](https://fastapi.tiangolo.com/)
- [Uvicorn 설정 가이드](https://www.uvicorn.org/)
- [PostgreSQL 연결 설정](https://www.postgresql.org/docs/)

---

## 🆘 지원

문제가 발생하면:
1. 로그 파일 확인: `logs/api.log`
2. 환경 변수 확인: `config/.env`
3. 데이터베이스 연결 확인
4. 포트 충돌 확인

**연락처**: Recipe AI Team

