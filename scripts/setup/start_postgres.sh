#!/bin/bash

echo "============================================================"
echo "🚀 PostgreSQL 시작 가이드"
echo "============================================================"
echo ""

# Check PostgreSQL status
echo "📌 Step 1: PostgreSQL 상태 확인"
echo "실행할 명령어:"
echo "  sudo service postgresql status"
echo ""

# Start PostgreSQL
echo "📌 Step 2: PostgreSQL 시작"
echo "실행할 명령어:"
echo "  sudo service postgresql start"
echo ""

# Verify connection
echo "📌 Step 3: 연결 확인"
echo "실행할 명령어:"
echo "  pg_isready -h localhost -p 5432"
echo ""

# Enable pgvector
echo "📌 Step 4: pgvector 확장 활성화"
echo "실행할 명령어:"
echo "  psql -h localhost -d recipe_ai_db -U recipe_keep -c \"CREATE EXTENSION IF NOT EXISTS vector;\""
echo ""

echo "============================================================"
echo "💡 WSL2 팁: PostgreSQL 자동 시작 설정"
echo "============================================================"
echo ""
echo "매번 수동으로 시작하기 귀찮다면:"
echo "1. ~/.bashrc 파일에 다음 추가:"
echo "   sudo service postgresql start 2>/dev/null"
echo ""
echo "2. sudo 비밀번호 없이 PostgreSQL 시작하려면:"
echo "   sudo visudo"
echo "   마지막에 추가: $USER ALL=(ALL) NOPASSWD: /usr/sbin/service postgresql *"
echo ""
echo "============================================================"

# Quick commands
echo "🔧 빠른 명령어:"
echo ""
echo "# PostgreSQL 시작"
echo "sudo service postgresql start"
echo ""
echo "# PostgreSQL 중지"
echo "sudo service postgresql stop"
echo ""
echo "# PostgreSQL 재시작"
echo "sudo service postgresql restart"
echo ""

