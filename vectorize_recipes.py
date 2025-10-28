#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
모든 레시피를 벡터화하고 DB에 저장
"""

import os
import logging
from dotenv import load_dotenv
from src.database import RecipeDB
from src.vectorizer import RecipeVectorizer

load_dotenv('config/.env')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/vectorization.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def main():
    logger.info("=" * 60)
    logger.info("🤖 레시피 벡터화 시작")
    logger.info("=" * 60)
    
    # 환경 변수 확인
    use_openai = os.getenv('USE_OPENAI_EMBEDDINGS', 'true').lower() == 'true'
    batch_size = int(os.getenv('VECTORIZATION_BATCH_SIZE', '100'))
    
    logger.info(f"Embedding 모델: {'OpenAI' if use_openai else 'SentenceTransformers'}")
    logger.info(f"Batch size: {batch_size}")
    
    # DB 연결
    db_name = os.getenv('DB_NAME', 'recipe_ai_db')
    db_user = os.getenv('DB_USER', 'recipe_keep')
    
    db = RecipeDB(db_name, db_user)
    db.connect()
    
    # 벡터화되지 않은 레시피 찾기
    db.cursor.execute("""
        SELECT id, title, title_en, description_en
        FROM recipes
        WHERE embedding IS NULL
        ORDER BY id
    """)
    missing_recipes = db.cursor.fetchall()
    
    if not missing_recipes:
        logger.info("✅ 모든 레시피가 이미 벡터화되어 있습니다!")
        db.close()
        return
    
    logger.info(f"🔍 벡터화 대상: {len(missing_recipes)}개 레시피")
    
    # Vectorizer 초기화
    vectorizer = RecipeVectorizer(use_openai=use_openai)
    
    # 각 레시피의 재료와 조리 단계를 가져와서 벡터화
    success = 0
    failed = 0
    
    for recipe_id, title, title_en, description_en in missing_recipes:
        try:
            # 재료 가져오기
            db.cursor.execute("""
                SELECT name_en FROM ingredients WHERE recipe_id = %s
            """, (recipe_id,))
            ingredients_en = [row[0] for row in db.cursor.fetchall() if row[0]]
            
            # 조리 단계 가져오기
            db.cursor.execute("""
                SELECT description_en FROM cooking_steps 
                WHERE recipe_id = %s 
                ORDER BY step_number
            """, (recipe_id,))
            steps_en = [row[0] for row in db.cursor.fetchall() if row[0]]
            
            # 레시피 딕셔너리 구성
            recipe = {
                'title_en': title_en or title,
                'description_en': description_en or '',
                'ingredients_en': ingredients_en,
                'cooking_steps_en': steps_en
            }
            
            # 벡터화
            embedding = vectorizer.vectorize_recipe(recipe)
            
            # DB 업데이트
            db.cursor.execute("""
                UPDATE recipes
                SET embedding = %s
                WHERE id = %s
            """, (embedding, recipe_id))
            
            db.conn.commit()
            
            success += 1
            if success % 10 == 0:
                logger.info(f"✅ 진행: {success}/{len(missing_recipes)}")
            
        except Exception as e:
            logger.error(f"❌ [{recipe_id}] {title[:30]}... 실패: {e}")
            db.conn.rollback()
            failed += 1
    
    db.close()
    
    logger.info("\n" + "=" * 60)
    logger.info("📊 벡터화 결과:")
    logger.info(f"   성공: {success}/{len(missing_recipes)}개")
    logger.info(f"   실패: {failed}개")
    logger.info("=" * 60)
    
    if success > 0:
        logger.info("\n✅ 벡터화 완료!")
        logger.info("\n🔍 이제 다음 명령으로 검색할 수 있습니다:")
        logger.info("   python search_recipes.py 'spicy chicken dish'")


if __name__ == '__main__':
    main()

