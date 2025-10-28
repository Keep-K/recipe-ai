# 📋 10000recipe.com 카테고리 태그 참조표

스크립트에서 사용하는 카테고리 태그의 완전한 목록입니다.

---

## 🏷️ 종류별 (cat4 - recipe_type)

| 한국어 | 태그 | 사용 예시 |
|--------|------|----------|
| 밑반찬 | 63 | `RECIPE_TYPE=밑반찬` |
| 메인반찬 | 56 | `RECIPE_TYPE=메인반찬` |
| 국/탕 | 54 | `RECIPE_TYPE=국/탕` |
| 찌개 | 55 | `RECIPE_TYPE=찌개` |
| 디저트 | 60 | `RECIPE_TYPE=디저트` |
| 면/만두 | 53 | `RECIPE_TYPE=면/만두` |
| 밥/죽/떡 | 52 | `RECIPE_TYPE=밥/죽/떡` |
| 퓨전 | 61 | `RECIPE_TYPE=퓨전` |
| 양념/잼/소스 | 58 | `RECIPE_TYPE=양념/잼/소스` |
| 양식 | 65 | `RECIPE_TYPE=양식` |
| 샐러드 | 64 | `RECIPE_TYPE=샐러드` |
| 스프 | 68 | `RECIPE_TYPE=스프` |
| 빵 | 66 | `RECIPE_TYPE=빵` |
| 과자 | 69 | `RECIPE_TYPE=과자` |
| 차/음료/술 | 59 | `RECIPE_TYPE=차/음료/술` |

### 별칭 (자동 매핑)
- `일품요리` → 메인반찬 (56)
- `음료` → 차/음료/술 (59)

---

## 🎯 상황별 (cat2 - recipe_situation)

| 한국어 | 태그 | 사용 예시 |
|--------|------|----------|
| 일상 | 12 | `RECIPE_SITUATION=일상` |
| 초스피드 | 18 | `RECIPE_SITUATION=초스피드` |
| 손님접대 | 13 | `RECIPE_SITUATION=손님접대` |
| 술안주 | 19 | `RECIPE_SITUATION=술안주` |
| 다이어트 | 21 | `RECIPE_SITUATION=다이어트` |
| 도시락 | 15 | `RECIPE_SITUATION=도시락` |
| 영양식 | 43 | `RECIPE_SITUATION=영양식` |
| 간식 | 17 | `RECIPE_SITUATION=간식` |
| 야식 | 45 | `RECIPE_SITUATION=야식` |
| 명절 | 44 | `RECIPE_SITUATION=명절` |

---

## 🥩 재료별 (cat3 - recipe_ingredient)

### 육류
| 한국어 | 태그 |
|--------|------|
| 소고기 | 70 |
| 돼지고기 | 71 |
| 닭고기 | 72 |
| 육류 | 23 |
| 순대 | 71 |

### 해물류 (모두 24)
오징어, 낙지, 새우, 조개류, 전복, 문어, 해파리, 게, 생선류, 아귀, 복어, 미꾸라지, 명란, 명태, 황석어, 갈치, 조기, 가오리, 굴, 바지락, 재첩, 홍합

### 채소류 (모두 28)
가지, 호박, 오이, 감자, 고구마, 콩나물, 시금치, 파, 고사리, 도라지, 더덕, 마늘종, 청경채, 쑥갓, 취나물, 냉이, 달래, 부추, 상추, 배추, 미나리, 숙주, 깻잎, 브로콜리, 김치, 야채, 미역, 된장, 청국장, 고추장, 시래기, 아욱, 도토리묵, 청포묵, 파래, 톳, 다시마, 무, 갓, 열무

### 달걀/유제품 (모두 50)
계란, 우유, 치즈, 베이컨, 햄, 두부, 소시지

### 건어물류 (모두 25)
김, 참치, 멸치, 북어, 어묵

### 밀가루/면류 (모두 32)
밀가루, 면, 파스타, 만두, 빵, 당면

### 쌀/곡류
- 쌀: 47
- 밥: 47
- 잡곡: 47
- 현미: 47
- 보리: 47
- 떡: 47
- 곡류: 26
- 콩: 26
- 팥: 26
- 흑임자: 26
- 잣: 26
- 녹두: 26
- 엿기름: 26

### 버섯류 (모두 31)
버섯, 버섯류

### 과일류 (모두 48)
딸기, 바나나, 망고, 블루베리, 키위, 아보카도, 오렌지, 사과, 포도, 토마토, 당근, 레몬, 자몽, 과일, 유자, 대추, 매실, 모과, 계피, 꿀, 얼음

### 음료
- 커피: 59
- 녹차: 59
- 차: 59

---

## 🍳 방법별 (cat1 - recipe_method)

| 한국어 | 태그 | 별칭 |
|--------|------|------|
| 볶음 | 6 | 만들기, 갈기 |
| 끓이기 | 1 | 짓기, 데우기 |
| 부침 | 7 | - |
| 조림 | 36 | - |
| 무침 | 41 | - |
| 비빔 | 42 | - |
| 찜 | 8 | 찌기 |
| 절임 | 10 | 얼리기 |
| 튀김 | 9 | - |
| 삶기 | 38 | - |
| 굽기 | 67 | 구이 |
| 회 | 37 | - |

---

## 📌 사용 방법

### config/.env 파일 설정:

```env
# 예시 1: 소고기 볶음 밑반찬
RECIPE_TYPE=밑반찬        # cat4=63
RECIPE_SITUATION=일상     # cat2=12
RECIPE_INGREDIENT=소고기  # cat3=70
RECIPE_METHOD=볶음        # cat1=6

# 예시 2: 파스타 일품요리
RECIPE_TYPE=일품요리      # cat4=56 (메인반찬)
RECIPE_SITUATION=일상     # cat2=12
RECIPE_INGREDIENT=파스타  # cat3=32
RECIPE_METHOD=볶음        # cat1=6

# 예시 3: 김치찌개
RECIPE_TYPE=찌개          # cat4=55
RECIPE_SITUATION=일상     # cat2=12
RECIPE_INGREDIENT=김치    # cat3=28
RECIPE_METHOD=끓이기      # cat1=1

# 예시 4: 디저트 (케이크)
RECIPE_TYPE=디저트        # cat4=60
RECIPE_SITUATION=일상     # cat2=12
RECIPE_INGREDIENT=빵      # cat3=32
RECIPE_METHOD=굽기        # cat1=67
```

### 생성되는 URL:

```
https://www.10000recipe.com/recipe/list.html?cat1=6&cat2=12&cat3=70&cat4=63&order=reco
                                                    ↑     ↑     ↑      ↑
                                                  방법  상황  재료   종류
```

---

## ⚠️ 주의사항

### 태그 매핑이 중요합니다!

잘못된 조합:
```bash
# ❌ 빵을 '밑반찬'으로 분류
RECIPE_TYPE=밑반찬  # cat4=63
RECIPE_INGREDIENT=빵  # cat3=32
# → 결과: 빵 관련 밑반찬 (거의 없음)
```

올바른 조합:
```bash
# ✅ 빵을 '디저트' 또는 '빵'으로 분류
RECIPE_TYPE=디저트  # cat4=60 또는
RECIPE_TYPE=빵      # cat4=66
RECIPE_INGREDIENT=빵  # cat3=32
# → 결과: 다양한 빵 레시피
```

---

## 🎯 최적화 팁

### 1. 정확한 카테고리 사용
```bash
# 파스타는 '일품요리' 또는 '양식'
RECIPE_TYPE=일품요리
RECIPE_INGREDIENT=파스타

# 또는
RECIPE_TYPE=양식
RECIPE_INGREDIENT=파스타
```

### 2. 초스피드 활용
```bash
# 간단한 요리는 '초스피드'
RECIPE_SITUATION=초스피드
```

### 3. 구체적 재료 지정
```bash
# '해물류' 보다는 구체적으로
RECIPE_INGREDIENT=새우  # 새우 요리만
RECIPE_INGREDIENT=오징어  # 오징어 요리만
RECIPE_INGREDIENT=해물  # 해물 믹스
```

---

## 📊 카테고리 조합 예시

### 인기 조합 TOP 10

1. **소고기 볶음 밑반찬**
   ```
   밑반찬 + 일상 + 소고기 + 볶음
   ```

2. **파스타 일품요리**
   ```
   일품요리 + 일상 + 파스타 + 볶음
   ```

3. **김치찌개**
   ```
   찌개 + 일상 + 김치 + 끓이기
   ```

4. **닭강정 튀김**
   ```
   튀김 + 일상 + 닭고기 + 튀김
   ```

5. **떡볶이**
   ```
   일품요리 + 초스피드 + 떡 + 볶음
   ```

6. **케이크 디저트**
   ```
   디저트 + 일상 + 빵 + 굽기
   ```

7. **생선구이**
   ```
   밑반찬 + 일상 + 생선류 + 구이
   ```

8. **두부조림**
   ```
   밑반찬 + 일상 + 두부 + 조림
   ```

9. **샐러드**
   ```
   샐러드 + 초스피드 + 야채 + 무침
   ```

10. **커피**
    ```
    음료 + 초스피드 + 커피 + 만들기
    ```

---

## 🔍 태그 확인 방법

실제 10000recipe.com URL을 확인하여 태그 검증:

```bash
# 크롤러가 생성하는 URL 확인
cd /home/keep/recipe-ai/recipe_ai_system
source venv/bin/activate
python -c "
from src.crawler import build_category_url
url = build_category_url('밑반찬', '일상', '소고기', '볶음')
print(url)
"

# 브라우저에서 해당 URL 접속하여 결과 확인
```

---

**참조**: `/home/keep/recipe-ai/ref/datanalysis_recipe/p1_blog_analysis/crowling_next.py` (11-20줄)

