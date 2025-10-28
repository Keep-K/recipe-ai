#!/bin/bash
# 진행 상황 체크 스크립트

echo "============================================================"
echo "📊 Recipe AI System - Progress Check"
echo "============================================================"
echo ""

cd "$(dirname "$0")"

# 프로세스 확인
if ps aux | grep "[p]ython main.py" > /dev/null; then
    echo "✅ Process is running"
else
    echo "❌ Process is not running"
fi
echo ""

# 로그 확인
if [ -f "logs/main.log" ]; then
    echo "📝 Latest log entries:"
    echo "---"
    tail -10 logs/main.log | grep -E "(Crawling|Translated|Inserted|Summary)"
    echo ""
    
    echo "📊 Progress:"
    crawled=$(grep -c "✅ Success:" logs/main.log 2>/dev/null || echo "0")
    translated=$(grep -c "✅ Translated:" logs/main.log 2>/dev/null || echo "0")
    inserted=$(grep -c "✅ Inserted recipe ID" logs/main.log 2>/dev/null || echo "0")
    
    echo "   Crawled: $crawled recipes"
    echo "   Translated: $translated recipes"
    echo "   Saved to DB: $inserted recipes"
else
    echo "❌ No log file found"
fi
echo ""

# DB 확인
echo "🗄️  Database status:"
PGPASSWORD='wkwjsrj4510*' psql -h localhost -d recipe_ai_db -U recipe_keep -c "
SELECT 
    'recipes' as table_name, COUNT(*) as count FROM recipes
UNION ALL
SELECT 'ingredients', COUNT(*) FROM ingredients
UNION ALL
SELECT 'cooking_steps', COUNT(*) FROM cooking_steps;
" 2>/dev/null || echo "   ❌ Cannot connect to database"

echo ""
echo "============================================================"


