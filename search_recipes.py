#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
벡터 검색으로 레시피 찾기
"""

import os
import sys
import logging
from dotenv import load_dotenv
from src.database import RecipeDB
from src.vectorizer import RecipeVectorizer

load_dotenv('config/.env')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def search_recipes(query: str, top_k: int = 10, min_similarity: float = 0.0):
    """
    자연어 쿼리로 레시피 검색
    
    Args:
        query: 검색 쿼리 (예: "spicy chicken dish")
        top_k: 반환할 결과 수
        min_similarity: 최소 유사도 (0~1)
    
    Returns:
        검색 결과 리스트
    """
    # DB 연결
    db_name = os.getenv('DB_NAME', 'recipe_ai_db')
    db_user = os.getenv('DB_USER', 'recipe_keep')
    
    db = RecipeDB(db_name, db_user)
    db.connect()
    
    # Vectorizer 초기화
    use_openai = os.getenv('USE_OPENAI_EMBEDDINGS', 'true').lower() == 'true'
    vectorizer = RecipeVectorizer(use_openai=use_openai)
    
    # 쿼리를 벡터로 변환
    logger.info(f"🔍 검색 쿼리: '{query}'")
    query_vector = vectorizer.vectorize(query)
    
    # 벡터 검색
    db.cursor.execute("""
        SELECT 
            id, 
            title, 
            title_en, 
            description_en,
            cooking_time,
            servings,
            1 - (embedding <=> %s::vector) as similarity
        FROM recipes
        WHERE embedding IS NOT NULL
          AND 1 - (embedding <=> %s::vector) >= %s
        ORDER BY embedding <=> %s::vector
        LIMIT %s
    """, (query_vector, query_vector, min_similarity, query_vector, top_k))
    
    results = db.cursor.fetchall()
    db.close()
    
    return results


def print_results(results):
    """검색 결과를 예쁘게 출력"""
    if not results:
        print("\n❌ 검색 결과가 없습니다.")
        return
    
    print("\n" + "=" * 80)
    print(f"✅ 검색 결과: {len(results)}개")
    print("=" * 80)
    
    for i, (recipe_id, title_kr, title_en, desc_en, cooking_time, servings, similarity) in enumerate(results, 1):
        print(f"\n{i}. [{recipe_id}] {title_en or title_kr}")
        print(f"   한글: {title_kr}")
        print(f"   설명: {desc_en[:100] if desc_en else 'N/A'}...")
        print(f"   조리 시간: {cooking_time}분 | 인분: {servings}인분")
        print(f"   유사도: {similarity:.3f} ({similarity*100:.1f}%)")
    
    print("\n" + "=" * 80)


def main():
    if len(sys.argv) < 2:
        print("\n사용법: python search_recipes.py '<검색 쿼리>' [결과 수]")
        print("\n예시:")
        print("  python search_recipes.py 'spicy chicken dish'")
        print("  python search_recipes.py 'healthy protein recipe' 5")
        print("  python search_recipes.py 'quick and easy dinner'")
        print("  python search_recipes.py '매운 닭고기 요리'")
        return
    
    query = sys.argv[1]
    top_k = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    
    results = search_recipes(query, top_k=top_k)
    print_results(results)


if __name__ == '__main__':
    main()

