#!/bin/bash
# Recipe AI System - 자동 설정 스크립트

echo "============================================================"
echo "🚀 Recipe AI System Setup"
echo "============================================================"

cd "$(dirname "$0")"

# 1. 가상환경 생성
echo "📦 Creating virtual environment..."
python3 -m venv venv 2>/dev/null || virtualenv venv
source venv/bin/activate

# 2. 의존성 설치
echo "📚 Installing dependencies..."
pip install -r requirements.txt -q

# 3. .env 파일 생성
if [ ! -f "config/.env" ]; then
    echo "⚙️ Creating .env file..."
    cp config/.env.template config/.env
    echo "⚠️ Please edit config/.env and set your OPENAI_API_KEY"
fi

# 4. DB 초기화
echo "🗄️ Initializing database..."
read -p "Create new database? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    sudo -u postgres psql -f db/init.sql
    psql -d recipe_ai_db -f db/schema.sql
    echo "✅ Database initialized!"
fi

echo ""
echo "============================================================"
echo "✅ Setup complete!"
echo "============================================================"
echo ""
echo "Next steps:"
echo "  1. Edit config/.env and set OPENAI_API_KEY"
echo "  2. Run: source venv/bin/activate"
echo "  3. Run: python main.py"
echo ""

