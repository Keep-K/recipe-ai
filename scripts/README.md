# 🚀 Recipe AI 자동화 스크립트 모음

모든 자동화 스크립트가 체계적으로 정리되어 있습니다.

## 📁 폴더 구조

```
scripts/
├── setup/                    # 초기 설정 스크립트
│   ├── install_pgvector.sh   # pgvector 확장 설치
│   ├── start_postgres.sh     # PostgreSQL 시작 가이드
│   └── setup.sh              # 전체 환경 설정
│
├── database/                 # 데이터베이스 관련 스크립트
│   └── add_vector_column.sh  # 벡터 컬럼 추가
│
├── utils/                    # 유틸리티 스크립트
│   ├── check_progress.sh     # 작업 진행 상황 확인
│   └── run_batch_collection.sh  # 배치 수집 실행
│
└── run_all.sh               # 전체 자동화 실행 (원클릭)
```

---

## 🎯 빠른 시작 (처음 설치하는 경우)

### 1️⃣ 전체 자동화 실행
```bash
cd /home/keep/recipe-ai/recipe_ai_system/scripts
./run_all.sh
```

이 스크립트는 다음을 자동으로 실행합니다:
1. PostgreSQL 시작
2. pgvector 설치
3. 벡터 컬럼 추가
4. Python 패키지 설치
5. 환경 설정 확인

---

## 📦 개별 스크립트 사용법

### 🔧 Setup (초기 설정)

#### PostgreSQL 시작
```bash
cd setup
./start_postgres.sh
```
- PostgreSQL 시작 방법 안내
- 자동 시작 설정 팁

#### pgvector 설치
```bash
cd setup
./install_pgvector.sh
```
- pgvector 확장 다운로드
- 컴파일 및 설치
- 데이터베이스에 확장 활성화

#### 전체 환경 설정
```bash
cd setup
./setup.sh
```
- Python 가상환경 생성
- 의존성 패키지 설치
- 환경 변수 설정

---

### 🗄️ Database (데이터베이스)

#### 벡터 컬럼 추가
```bash
cd database
./add_vector_column.sh
```
- recipes 테이블에 embedding 컬럼 추가
- 벡터 검색용 인덱스 생성
- 마이그레이션 실행 및 확인

---

### 🛠️ Utils (유틸리티)

#### 진행 상황 확인
```bash
cd utils
./check_progress.sh
```
- 레시피 수집 진행 상황
- 번역 완료 상태
- 데이터베이스 통계

#### 배치 수집 실행
```bash
cd utils
./run_batch_collection.sh
```
- 레시피 대량 수집
- 자동 재시도
- 로그 저장

---

## 🔄 일반적인 워크플로우

### 처음 설치 시
```bash
# 1. 전체 자동화 실행
./scripts/run_all.sh

# 2. 레시피 수집
./scripts/utils/run_batch_collection.sh

# 3. 벡터화 실행
python vectorize_recipes.py
```

### 일상적인 사용
```bash
# PostgreSQL 시작
./scripts/setup/start_postgres.sh

# 진행 상황 확인
./scripts/utils/check_progress.sh

# 레시피 검색
python search_recipes.py "닭가슴살 요리"
```

---

## 💡 팁

### PostgreSQL 자동 시작 설정
```bash
# ~/.bashrc에 추가
echo 'sudo service postgresql start 2>/dev/null' >> ~/.bashrc
```

### 빠른 명령어 별칭 설정
```bash
# ~/.bashrc에 추가
alias recipe-start='sudo service postgresql start'
alias recipe-status='./scripts/utils/check_progress.sh'
alias recipe-collect='./scripts/utils/run_batch_collection.sh'
```

---

## 🐛 문제 해결

### PostgreSQL 연결 오류
```bash
# PostgreSQL 시작
sudo service postgresql start

# 연결 확인
pg_isready -h localhost -p 5432
```

### pgvector 설치 오류
```bash
# 의존성 재설치
sudo apt-get update
sudo apt-get install -y postgresql-server-dev-15 git build-essential

# pgvector 재설치
./scripts/setup/install_pgvector.sh
```

### Python 패키지 오류
```bash
# 가상환경 활성화
source venv/bin/activate

# 패키지 재설치
pip install -r requirements.txt
```

---

## 📞 도움말

각 스크립트는 `--help` 또는 `-h` 옵션을 지원합니다:

```bash
./setup/install_pgvector.sh --help
./database/add_vector_column.sh --help
```

---

**🚀 시작하려면: `./run_all.sh`**

