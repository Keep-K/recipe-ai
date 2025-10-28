# ⚡ 성능 최적화 가이드

## 📊 현재 성능

- 10개 레시피 처리 시간: **약 3-5분**
- 병목: 번역 API 호출 (2초 딜레이 × 많은 호출)

---

## 🚀 속도 개선 방법

### **1. 번역 딜레이 감소** (즉시 적용 가능)

#### 옵션 A: 안전한 개선 (30% 빠름)
```env
# config/.env
TRANSLATION_DELAY=1.0  # 2.0 → 1.0
```
- 예상 시간: 5분 → 3.5분
- 위험도: 낮음

#### 옵션 B: 공격적 개선 (60% 빠름)
```env
TRANSLATION_DELAY=0.5  # 2.0 → 0.5
```
- 예상 시간: 5분 → 2분
- 위험도: 429 에러 가능성 있음

#### 옵션 C: 최대 속도 (70% 빠름, 위험)
```env
TRANSLATION_DELAY=0.3
```
- 예상 시간: 5분 → 1.5분
- 위험도: 높음 (429 에러 자주 발생)

---

### **2. 크롤링 딜레이 감소**

```env
# config/.env
CRAWLING_DELAY=0.5  # 1.0 → 0.5
```
- 크롤링 시간: 10초 → 5초
- 전체 시간: 5초 절약

---

### **3. 더 빠른 모델 사용**

```env
# 현재
OPENAI_MODEL=gpt-4o-mini

# 변경 (더 빠르고 저렴, 품질 약간 낮음)
OPENAI_MODEL=gpt-3.5-turbo
```

---

### **4. 병렬 처리** (코드 수정 필요)

#### 개선된 번역기 (멀티스레딩)

```python
# src/translator.py에 추가
from concurrent.futures import ThreadPoolExecutor

def translate_all(self, recipes: List[Dict]) -> List[Dict]:
    """병렬 번역 (5배 빠름)"""
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(self.translate_recipe, recipes))
    return results
```

**주의**: API rate limit 초과 위험

---

### **5. 캐시 활용 극대화** (이미 적용됨 ✅)

- ✅ 중복 텍스트 재번역 방지
- ✅ 디스크 캐시로 재실행 시 빠름

---

## 💡 **권장 설정 (균형잡힌 속도 + 안정성)**

```env
# config/.env 
TRANSLATION_DELAY=1.0      # 2.0 → 1.0 (안전한 개선)
CRAWLING_DELAY=0.5         # 1.0 → 0.5
OPENAI_MODEL=gpt-4o-mini   # 유지 (품질 좋음)
OPENAI_MAX_TOKENS=500      # 700 → 500 (속도 향상)
```

**예상 시간**: 5분 → **2.5분** (50% 개선)

---

## 🔥 **최대 속도 설정 (위험 감수)**

```env
TRANSLATION_DELAY=0.3
CRAWLING_DELAY=0.3
OPENAI_MODEL=gpt-3.5-turbo
OPENAI_MAX_TOKENS=300
```

**예상 시간**: 5분 → **1분** (80% 개선)  
**위험**: 429 에러, 품질 저하 가능

---

## 📈 **성능 비교표**

| 설정 | 예상 시간 | 안정성 | 품질 | 비용 |
|------|-----------|--------|------|------|
| 현재 (DELAY=2.0) | 5분 | ⭐⭐⭐ | ⭐⭐⭐ | 💰💰 |
| 권장 (DELAY=1.0) | 2.5분 | ⭐⭐⭐ | ⭐⭐⭐ | 💰💰 |
| 빠름 (DELAY=0.5) | 2분 | ⭐⭐ | ⭐⭐⭐ | 💰💰 |
| 최대 (DELAY=0.3) | 1분 | ⭐ | ⭐⭐ | 💰 |

---

## 🎯 **즉시 적용**

<function_calls>
<invoke name="search_replace">
<parameter name="file_path">/home/keep/recipe-ai/recipe_ai_system/config/env_template.txt
