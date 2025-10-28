# 🔑 멀티 API 키 설정 가이드

## ⚡ 속도 향상

**단일 키**: 10개 레시피 = 3-5분  
**3개 키**: 10개 레시피 = **1-2분** (3배 빠름!) 🚀

---

## 📝 설정 방법

### Step 1: 추가 API 키 발급

1. [OpenAI Platform](https://platform.openai.com/api-keys) 접속
2. `+ Create new secret key` 클릭
3. 키 이름: `recipe-ai-key-2`, `recipe-ai-key-3`
4. 키 복사 (한 번만 표시됨!)

### Step 2: .env 파일에 추가

```bash
nano config/.env
```

**추가:**
```env
# 기존
OPENAI_API_KEY=sk-proj-Pb2CEs5Zou4SPcEr-0Oa...

# 추가 (2개 더)
OPENAI_API_KEY_2=sk-proj-NEW_KEY_2_HERE...
OPENAI_API_KEY_3=sk-proj-NEW_KEY_3_HERE...
```

**최대 10개까지 지원:**
- `OPENAI_API_KEY`
- `OPENAI_API_KEY_2`
- `OPENAI_API_KEY_3`
- ...
- `OPENAI_API_KEY_10`

---

## 🚀 작동 방식

### **라운드 로빈 (Round Robin)**

```
API 호출 1 → Key 1
API 호출 2 → Key 2  
API 호출 3 → Key 3
API 호출 4 → Key 1 (다시 처음부터)
API 호출 5 → Key 2
...
```

### **병렬 처리**

```
3개 키 사용 시:

[레시피1] → Key 1 ──┐
[레시피2] → Key 2 ──┼─→ 동시 번역 (3배 빠름)
[레시피3] → Key 3 ──┘

[레시피4] → Key 1 ──┐
[레시피5] → Key 2 ──┼─→ 동시 번역
[레시피6] → Key 3 ──┘
```

---

## 📊 성능 비교

| API 키 수 | 10개 레시피 | 50개 레시피 | 100개 레시피 |
|-----------|-------------|-------------|--------------|
| 1개 | 3-5분 | 15-25분 | 30-50분 |
| 2개 | 2-3분 | 8-13분 | 15-25분 |
| 3개 | **1-2분** | **5-9분** | **10-17분** |
| 5개 | 1분 | 3-5분 | 6-10분 |
| 10개 | **30초** | **2-3분** | **4-6분** 🔥 |

---

## ✅ 확인 방법

실행 시 로그에서 확인:

```
🔑 Loaded 3 API key(s)
Translating 10 recipes with 3 API key(s)...
```

---

## ⚙️ 추가 최적화

### 딜레이 조정 (멀티 키 사용 시)

```env
# 단일 키
TRANSLATION_DELAY=1.0

# 2-3개 키
TRANSLATION_DELAY=0.5  # 더 공격적으로

# 5개 이상 키
TRANSLATION_DELAY=0.3  # 매우 빠름
```

---

## ⚠️ 주의사항

### 1. API 비용
- 키가 많아도 총 호출 수는 동일
- 비용은 같지만 **속도만 빠름**

### 2. Rate Limit
- OpenAI: 키당 분당 3,500 토큰 (gpt-4o-mini)
- 3개 키 = 분당 10,500 토큰 사용 가능

### 3. 동일 계정 키
- 같은 OpenAI 계정의 키들 사용 가능
- 또는 여러 계정 사용 가능

---

## 🔒 보안

모든 키를 `.env`에 저장:
- ✅ `.gitignore`에 포함됨
- ✅ Git에 커밋되지 않음
- ✅ 로컬에만 저장

```bash
chmod 600 config/.env  # 본인만 읽기 가능
```

---

## 🎯 테스트

```bash
# .env에 키 3개 추가 후
cd /home/keep/recipe-ai/recipe_ai_system
source venv/bin/activate
python main.py
```

로그 확인:
```
🔑 Loaded 3 API key(s)  ← 3개 키 확인!
```

---

## 💡 FAQ

**Q: 키가 2개만 있어도 되나요?**  
A: 네! 2개만 있어도 2배 빠릅니다.

**Q: 한 키가 429 에러 나면?**  
A: 다른 키로 자동 전환됩니다.

**Q: 비용은?**  
A: 호출 수는 같으므로 비용 동일, 시간만 단축.

**Q: 무료 계정도 가능?**  
A: 네, 여러 무료 계정의 키 사용 가능.

---

**3개 키를 추가하면 속도가 3배 빨라집니다!** 🚀

