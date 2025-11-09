#!/bin/bash
# Railway PostgreSQL 접속 환경 변수 설정 스크립트
# 사용법:
#   1) cp scripts/utils/railway.env.example scripts/utils/railway.env
#   2) railway.env 파일에서 USER / PASSWORD / PORT / DBNAME 수정
#   3) source scripts/utils/export_railway_env.sh

BASH_SOURCE_PATH="${BASH_SOURCE[0]:-$0}"
SCRIPT_DIR="$(cd "$(dirname "$BASH_SOURCE_PATH")" && pwd)"

DEFAULT_ENV="${SCRIPT_DIR}/railway.env"
ENV_FILE="${ENV_FILE:-$DEFAULT_ENV}"

if [ ! -f "$ENV_FILE" ]; then
  CWD_ENV="$(pwd)/railway.env"
  if [ -f "$CWD_ENV" ]; then
    ENV_FILE="$CWD_ENV"
  fi
fi

if [ ! -f "$ENV_FILE" ]; then
  echo "❌ ENV 파일을 찾을 수 없습니다: $ENV_FILE"
  echo "   먼저 cp scripts/utils/railway.env.example scripts/utils/railway.env 로 복사 후 값을 채워주세요."
  return 1 2>/dev/null || exit 1
fi

set -o allexport
# shellcheck disable=SC1090
source "$ENV_FILE"
set +o allexport

echo "✅ Railway DB 환경 변수를 설정했습니다."
echo "   DB_HOST=${DB_HOST:-'(미설정)'}"
echo "   DB_PORT=${DB_PORT:-'(미설정)'}"
echo "   DB_NAME=${DB_NAME:-'(미설정)'}"
echo "   DB_USER=${DB_USER:-'(미설정)'}"
echo ""
echo "📌 벡터화 실행 예시:"
if [ -n "${DATABASE_URL:-}" ]; then
  echo "   python vectorize_recipes.py --env-file $ENV_FILE"
else
  echo "   python vectorize_recipes.py --env-file $ENV_FILE"
fi

