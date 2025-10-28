#!/bin/bash

echo "============================================================"
echo "🔍 가상환경 상태 확인"
echo "============================================================"
echo ""

# 가상환경 활성화 여부
if [ -n "$VIRTUAL_ENV" ]; then
    echo "✅ 가상환경 활성화됨"
    echo "   경로: $VIRTUAL_ENV"
else
    echo "❌ 가상환경 비활성화됨"
    echo ""
    echo "활성화 방법:"
    echo "   source venv/bin/activate"
fi

echo ""

# Python 경로
echo "🐍 Python 경로:"
which python3

echo ""

# pip 경로
echo "📦 pip 경로:"
which pip

echo ""

# 설치된 패키지 확인
if [ -n "$VIRTUAL_ENV" ]; then
    echo "📚 설치된 주요 패키지:"
    pip list 2>/dev/null | grep -E "openai|sentence-transformers|pgvector|psycopg2" || echo "   (벡터화 관련 패키지 없음)"
fi

echo ""
echo "============================================================"
