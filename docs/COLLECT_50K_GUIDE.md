# 🚀 50,000개 레시피 대규모 수집 가이드

## 📊 개요

- **목표**: 50,000개 레시피 수집
- **배치 구성**: 500개 배치 × 100개 = 50,000개
- **예상 소요 시간**: 50-60시간 (2-3일)
- **예상 비용**: 약 $20 (OpenAI API)

---

## ⚡ 빠른 시작

```bash
# 1. PostgreSQL 시작
sudo service postgresql start

# 2. Screen 세션 시작 (SSH 연결 끊어도 계속 실행)
screen -S recipe_50k

# 3. 스크립트 실행
cd /home/keep/recipe-ai/recipe_ai_system
./scripts/utils/run_batch_50k.sh

# 4. Screen 세션 분리 (Ctrl+A, D)
# SSH 연결 끊어도 계속 실행됩니다!

# 5. 나중에 다시 연결
screen -r recipe_50k
```

---

## 📋 수집 구성 (500개 배치)

### Phase 1: 한식 메인 요리 (5,000개)
- 소고기 (1,000개): 볶음, 구이, 조림, 찜, 무침, 국, 전골, 장조림, 불고기, 육회
- 돼지고기 (1,000개): 볶음, 구이, 찜, 조림, 삼겹살, 목살, 갈비, 보쌈, 족발, 수육
- 닭고기 (1,000개): 구이, 조림, 볶음, 튀김, 가슴살, 삼계탕, 찜, 강정, 볶음탕, 치킨
- 해산물 (2,000개): 생선, 오징어, 낙지, 새우, 조개, 전복, 문어, 해파리, 게 등

### Phase 2: 채소 요리 (5,000개)
- 두부 (500개): 조림, 볶음, 구이, 찌개, 순두부찌개
- 버섯 (500개): 볶음, 조림, 구이, 느타리, 양송이
- 가지/호박/오이 (1,000개): 볶음, 나물, 전, 무침, 냉국, 소박이, 장아찌
- 감자/고구마 (500개): 조림, 볶음, 전, 샐러드, 찜
- 나물류 (2,500개): 콩나물, 시금치, 파, 고사리, 도라지, 더덕 등 25종

### Phase 3: 밥/면/일품 (10,000개)
- 볶음밥 (1,000개): 김치, 소고기, 새우, 야채, 참치, 계란 등
- 덮밥/비빔밥 (1,500개): 각종 덮밥, 비빔밥, 회덮밥, 낙지덮밥 등
- 국수/면 (3,000개): 잔치국수, 비빔국수, 칼국수, 냉면, 라면, 짜장면, 짬뽕, 우동, 파스타 등
- 죽/밥 (2,000개): 전복죽, 호박죽, 팥죽 등 각종 죽과 밥 종류
- 기타 일품 (2,500개): 떡볶이, 김밥, 만두, 샌드위치, 샐러드 등

### Phase 4: 국/탕/찌개 (10,000개)
- 소고기 국/탕 (2,000개): 소고기국, 무국, 미역국, 육개장, 갈비탕, 설렁탕, 곰탕 등
- 돼지고기 국/탕 (1,500개): 김치국, 감자탕, 뼈다귀해장국, 순대국 등
- 닭고기 국/탕 (1,000개): 삼계탕, 닭곰탕, 닭개장, 닭백숙 등
- 해산물 국/탕 (2,500개): 생선국, 조개국, 해물탕, 추어탕 등
- 채소 국/탕 (1,000개): 미역국, 된장국, 콩나물국 등
- 찌개 (2,000개): 김치찌개, 된장찌개, 순두부찌개, 부대찌개 등

### Phase 5: 특수 요리 (10,000개)
- 찜 요리 (2,000개): 갈비찜, 닭찜, 해물찜, 생선찜 등
- 튀김/전 (3,000개): 닭강정, 치킨, 탕수육, 돈까스, 각종 전 등
- 장아찌/절임/젓갈 (2,000개): 각종 장아찌, 젓갈, 게장 등
- 무침/조림 (3,000개): 멸치볶음, 어묵볶음, 장조림, 각종 무침, 김치 등

### Phase 6: 디저트/음료/빵 (10,000개)
- 디저트 (3,000개): 케이크, 쿠키, 마카롱, 푸딩, 아이스크림, 와플 등
- 빵/베이커리 (3,000개): 식빵, 바게트, 소보로빵, 피자 등
- 음료/스무디 (2,000개): 커피, 차, 스무디, 주스, 에이드 등
- 한식 떡/전통 (2,000개): 인절미, 송편, 경단, 백설기, 빙수 등

---

## 💰 예상 비용

### API 사용량 계산
```
총 레시피: 50,000개
레시피당 비용: $0.00039 (평균)
총 예상 비용: 50,000 × $0.00039 = $19.50

실제 예상: $18-$22 (캐싱 효과)
```

### 권장 잔액
- **최소**: $20
- **권장**: $25 (여유분 포함)
- **안전**: $30 (여유 충분)

---

## ⏱️ 예상 시간표

| 단계 | 누적 레시피 | 예상 시간 | 진행률 |
|------|------------|----------|--------|
| Phase 1 완료 | 5,000개 | ~5시간 | 10% |
| Phase 2 완료 | 10,000개 | ~10시간 | 20% |
| Phase 3 완료 | 20,000개 | ~20시간 | 40% |
| Phase 4 완료 | 30,000개 | ~30시간 | 60% |
| Phase 5 완료 | 40,000개 | ~40시간 | 80% |
| Phase 6 완료 | 50,000개 | ~50시간 | 100% ✅ |

**실제 시간**: 네트워크, API 응답 속도에 따라 변동 가능

---

## 🛡️ 안전한 실행 방법

### Screen 사용 (추천!)

```bash
# Screen 설치 (필요시)
sudo apt-get install screen

# Screen 세션 시작
screen -S recipe_50k

# 스크립트 실행
cd /home/keep/recipe-ai/recipe_ai_system
./scripts/utils/run_batch_50k.sh

# 세션 분리 (Ctrl+A, D)
# 이제 SSH를 끊어도 계속 실행됩니다!

# 다시 연결
screen -r recipe_50k

# 세션 목록 확인
screen -ls

# 세션 종료 (내부에서)
exit
```

### Tmux 사용 (대안)

```bash
# Tmux 설치
sudo apt-get install tmux

# Tmux 세션 시작
tmux new -s recipe_50k

# 스크립트 실행
cd /home/keep/recipe-ai/recipe_ai_system
./scripts/utils/run_batch_50k.sh

# 세션 분리 (Ctrl+B, D)

# 다시 연결
tmux attach -t recipe_50k
```

---

## 📊 실시간 모니터링

### 진행 상황 확인

```bash
# 터미널 1: Screen/Tmux에서 스크립트 실행 중

# 터미널 2: 현재 DB 레시피 수 확인
PGPASSWORD='wkwjsrj4510*' psql -h localhost -d recipe_ai_db -U recipe_keep -c "SELECT COUNT(*) FROM recipes;"

# 로그 실시간 확인
tail -f logs/batch_50k_*.log

# 시스템 리소스 확인
htop
```

### OpenAI 사용량 모니터링

https://platform.openai.com/usage

- 실시간 토큰 사용량 확인
- 비용 추정
- Rate Limit 확인

---

## 🔄 중단 후 재개

### 스크립트가 중단되었을 때

```bash
# 1. 현재 수집된 레시피 수 확인
PGPASSWORD='wkwjsrj4510*' psql -h localhost -d recipe_ai_db -U recipe_keep -c "SELECT COUNT(*) FROM recipes;"

# 2. 스크립트 편집
nano /home/keep/recipe-ai/recipe_ai_system/scripts/utils/run_batch_50k.sh

# 3. 완료된 배치 주석 처리
# 예: 3-1부터 3-50까지 완료되었다면 해당 라인들을 주석(#) 처리

# 4. 재실행 (DB 초기화 하지 않기!)
./scripts/utils/run_batch_50k.sh
# → "DB를 초기화하고 시작하시겠습니까?" → N 입력!
```

---

## 💾 자동 백업

### 백업 타이밍
- **5,000개마다 자동 백업**
- **최종 완료 시 전체 백업**

### 백업 위치
```
backups/
├── backup_50k_5000_20251024_120000.sql
├── backup_50k_10000_20251024_150000.sql
├── backup_50k_15000_20251024_180000.sql
├── ...
└── final_50k_20251025_100000.sql
```

### 수동 백업
```bash
# 현재 상태 백업
PGPASSWORD='wkwjsrj4510*' pg_dump -h localhost -U recipe_keep recipe_ai_db > backups/manual_$(date +%Y%m%d_%H%M%S).sql

# 복구 (필요시)
PGPASSWORD='wkwjsrj4510*' psql -h localhost -d recipe_ai_db -U recipe_keep < backups/backup_50k_25000_20251024_230000.sql
```

---

## ⚠️ 주의사항

### 시스템 요구사항
- **디스크 공간**: 최소 20GB 여유
- **메모리**: 최소 4GB RAM
- **안정적인 인터넷 연결**: 필수
- **전원 공급**: 중단 없는 전원 필요

### 실행 전 체크리스트
- [ ] PostgreSQL 실행 중
- [ ] OpenAI API 잔액 $25 이상
- [ ] 10개 API 키 설정 완료
- [ ] 디스크 공간 20GB 이상
- [ ] Screen 또는 Tmux 설치
- [ ] 절전 모드 해제

---

## 🎯 완료 후 다음 단계

### 1. 벡터화 (필수!)

```bash
# 50,000개 벡터화
python vectorize_recipes.py

# 예상 소요 시간: 10-15시간
# 예상 비용: $1 (Embeddings)
```

### 2. FastAPI 서버 테스트

```bash
python api_server.py

# 브라우저: http://localhost:8000/docs
# /search 엔드포인트로 검색 테스트
```

### 3. 데이터 품질 확인

```sql
-- 번역 완료율
SELECT 
    COUNT(*) as total,
    COUNT(*) FILTER (WHERE title_en IS NOT NULL) * 100.0 / COUNT(*) as translation_rate
FROM recipes;

-- 중복 확인
SELECT url, COUNT(*) 
FROM recipes 
GROUP BY url 
HAVING COUNT(*) > 1;
```

---

## 💡 최적화 팁

### 1. 네트워크 최적화
```bash
# DNS 캐시 비우기
sudo systemd-resolve --flush-caches

# 네트워크 설정 최적화
sudo sysctl -w net.ipv4.tcp_tw_reuse=1
```

### 2. PostgreSQL 최적화
```sql
-- 임시로 성능 향상 (수집 중에만)
ALTER SYSTEM SET shared_buffers = '1GB';
ALTER SYSTEM SET work_mem = '50MB';
SELECT pg_reload_conf();
```

### 3. Python 메모리 관리
```bash
# 주기적으로 Python 프로세스 재시작 (메모리 누수 방지)
# 10,000개마다 스크립트 재실행
```

---

## 📈 성능 벤치마크

### 예상 성능 (10개 API 키)
```
1시간당 레시피 수: ~1,000개
1일 레시피 수: ~20,000개
50,000개 완료: 2.5일
```

### 실제 성능 (테스트 결과)
```
평균 레시피당 시간: ~3.6초
시간당 레시피: ~1,000개
50,000개 실제 시간: 50-60시간
```

---

## 🆘 문제 해결

### API Rate Limit
```bash
# config/.env에서 딜레이 증가
TRANSLATION_DELAY=0.5
```

### 메모리 부족
```bash
# 배치 크기 줄이기 (스크립트 편집)
# 100 → 50으로 변경
```

### 디스크 공간 부족
```bash
# 로그 파일 정리
rm logs/batch_50k_*.log

# 오래된 백업 삭제
rm backups/backup_50k_5000_*.sql
```

### PostgreSQL 연결 끊김
```bash
# PostgreSQL 재시작
sudo service postgresql restart

# 연결 유지 설정
# postgresql.conf에 추가:
# tcp_keepalives_idle = 60
# tcp_keepalives_interval = 10
```

---

## 📊 최종 통계 예시

```
========================================
  🎉 50,000개 레시피 수집 완료!
========================================
총 수집: 50,000개 레시피
총 시간: 52시간 30분
평균: 3.78초/레시피
========================================

DB 최종 통계:
 total_recipes | total_ingredients | total_steps 
---------------+-------------------+-------------
        50,000 |           250,000 |     300,000
```

---

## 🎉 성공 사례

### 예상 결과
- ✅ 50,000개 레시피 수집
- ✅ 250,000개 재료 데이터
- ✅ 300,000개 조리 단계
- ✅ 완전한 한식+세계 요리 DB
- ✅ AI 검색 가능한 대규모 DB

---

## 🚀 시작하기

```bash
# Screen 세션 시작
screen -S recipe_50k

# PostgreSQL 시작
sudo service postgresql start

# 스크립트 실행
cd /home/keep/recipe-ai/recipe_ai_system
./scripts/utils/run_batch_50k.sh

# 세션 분리 (Ctrl+A, D)
# 2-3일 후 다시 연결해서 확인!
```

**행운을 빕니다! 50,000개 레시피 DB로 최고의 레시피 AI를 만드세요!** 🎉

---

**관련 문서**:
- [10,000개 수집 가이드](COLLECT_10K_GUIDE.md)
- [추가 레시피 수집](ADD_MORE_RECIPES.md)
- [벡터화 가이드](VECTORIZATION_GUIDE.md)

