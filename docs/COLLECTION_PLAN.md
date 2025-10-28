# 🎯 1000개 레시피 수집 계획

## 📊 Phase 1: 메인 단백질 (400개)
**타겟**: 일상 식단의 핵심

### 1-1. 소고기 (100개)
```env
RECIPE_TYPE=밑반찬
RECIPE_SITUATION=일상
RECIPE_INGREDIENT=소고기
RECIPE_METHOD=볶음
MAX_RECIPES=50
```
```env
RECIPE_METHOD=구이
MAX_RECIPES=50
```

### 1-2. 돼지고기 (100개)
```env
RECIPE_INGREDIENT=돼지고기
RECIPE_METHOD=볶음
MAX_RECIPES=50
```
```env
RECIPE_METHOD=찜
MAX_RECIPES=50
```

### 1-3. 닭고기 (100개)
```env
RECIPE_INGREDIENT=닭고기
RECIPE_METHOD=구이
MAX_RECIPES=50
```
```env
RECIPE_METHOD=조림
MAX_RECIPES=50
```

### 1-4. 해산물 (100개)
```env
RECIPE_INGREDIENT=생선류
RECIPE_METHOD=구이
MAX_RECIPES=50
```
```env
RECIPE_INGREDIENT=오징어
RECIPE_METHOD=볶음
MAX_RECIPES=50
```

---

## 🥗 Phase 2: 야채 & 두부 (200개)

### 2-1. 두부/콩 (100개)
```env
RECIPE_INGREDIENT=두부
RECIPE_METHOD=조림
MAX_RECIPES=50
```
```env
RECIPE_METHOD=볶음
MAX_RECIPES=50
```

### 2-2. 버섯/채소 (100개)
```env
RECIPE_INGREDIENT=버섯
RECIPE_METHOD=볶음
MAX_RECIPES=50
```
```env
RECIPE_INGREDIENT=가지
RECIPE_METHOD=볶음
MAX_RECIPES=50
```

---

## 🍚 Phase 3: 밥/면 요리 (200개)

### 3-1. 밥 요리 (100개)
```env
RECIPE_TYPE=일품요리
RECIPE_INGREDIENT=소고기
RECIPE_METHOD=볶음
MAX_RECIPES=50
```
```env
RECIPE_INGREDIENT=김치
RECIPE_METHOD=볶음
MAX_RECIPES=50
```

### 3-2. 면 요리 (100개)
```env
RECIPE_TYPE=일품요리
RECIPE_SITUATION=초스피드
RECIPE_INGREDIENT=면
RECIPE_METHOD=볶음
MAX_RECIPES=50
```
```env
RECIPE_INGREDIENT=파스타
RECIPE_METHOD=볶음
MAX_RECIPES=50
```

---

## 🍲 Phase 4: 국/찌개 (200개)

### 4-1. 국 (100개)
```env
RECIPE_TYPE=국/탕
RECIPE_INGREDIENT=소고기
RECIPE_METHOD=끓이기
MAX_RECIPES=50
```
```env
RECIPE_INGREDIENT=생선류
RECIPE_METHOD=끓이기
MAX_RECIPES=50
```

### 4-2. 찌개 (100개)
```env
RECIPE_TYPE=찌개
RECIPE_INGREDIENT=돼지고기
RECIPE_METHOD=끓이기
MAX_RECIPES=50
```
```env
RECIPE_INGREDIENT=두부
RECIPE_METHOD=끓이기
MAX_RECIPES=50
```

---

## 🎯 수집 우선순위 이유

1. **소고기/돼지고기/닭고기**: 가장 자주 검색되는 재료
2. **볶음/구이**: 가장 일반적인 조리법
3. **일상/밑반찬**: 가장 많이 만드는 타입
4. **해산물/두부**: 건강식 수요 증가
5. **밥/면**: 한 끼 식사 완성 요리
6. **국/찌개**: 한식 필수 카테고리

---

## ⏱️ 예상 시간

- **10개**: 41초
- **50개**: 약 3-4분
- **100개**: 약 7-8분
- **1000개**: **약 70-80분 (1시간 10분)**

---

## 🔄 실행 방법

### 자동화 스크립트 사용 (추천)
```bash
cd /home/keep/recipe-ai/recipe_ai_system
./run_batch_collection.sh
```

### 수동 실행
```bash
# config/.env 수정
nano config/.env

# 실행
python main.py

# 다음 카테고리로 변경 후 반복
```

---

## 📊 진행 추적

- [ ] Phase 1-1: 소고기 볶음 (50개)
- [ ] Phase 1-1: 소고기 구이 (50개)
- [ ] Phase 1-2: 돼지고기 볶음 (50개)
- [ ] Phase 1-2: 돼지고기 찜 (50개)
- [ ] Phase 1-3: 닭고기 구이 (50개)
- [ ] Phase 1-3: 닭고기 조림 (50개)
- [ ] Phase 1-4: 생선 구이 (50개)
- [ ] Phase 1-4: 오징어 볶음 (50개)
- [ ] ... (계속)

---

## 💾 데이터 백업

각 Phase 완료 후:
```bash
pg_dump -h localhost -U recipe_keep recipe_ai_db > backup_phase1.sql
```

