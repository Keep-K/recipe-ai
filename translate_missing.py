#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DB에서 번역 안 된 레시피를 찾아서 직접 번역하고 업데이트
"""

import os
import logging
from dotenv import load_dotenv

from src.database import RecipeDB
from src.translator import RecipeTranslator

load_dotenv('config/.env')

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def main():
    logger.info("=" * 60)
    logger.info("🔧 DB 내 번역 누락 레시피 직접 번역")
    logger.info("=" * 60)
    
    # DB 연결
    db_name = os.getenv('DB_NAME', 'recipe_ai_db')
    db_user = os.getenv('DB_USER', 'recipe_keep')
    
    db = RecipeDB(db_name, db_user)
    db.connect()
    
    # 번역 안 된 레시피 찾기
    db.cursor.execute("""
        SELECT id, title, description
        FROM recipes 
        WHERE title = title_en OR title_en IS NULL
        ORDER BY id
    """)
    missing_recipes = db.cursor.fetchall()
    
    # 번역 안 된 조리 단계 찾기
    db.cursor.execute("""
        SELECT recipe_id, id, step_number, description
        FROM cooking_steps 
        WHERE description = description_en OR description_en IS NULL
        ORDER BY recipe_id, step_number
    """)
    missing_steps = db.cursor.fetchall()
    
    if not missing_recipes and not missing_steps:
        logger.info("✅ 모든 레시피와 조리 단계가 번역되어 있습니다!")
        db.close()
        return
    
    logger.info(f"🔍 번역 누락 레시피: {len(missing_recipes)}개")
    logger.info(f"🔍 번역 누락 조리 단계: {len(missing_steps)}개")
    
    # Translator 초기화
    api_keys = []
    for i in range(1, 11):
        key_name = f'OPENAI_API_KEY_{i}' if i > 1 else 'OPENAI_API_KEY'
        key = os.getenv(key_name)
        if key and key != 'your-api-key-here':
            api_keys.append(key)
    
    translator = RecipeTranslator(
        api_keys=api_keys,
        model=os.getenv('OPENAI_MODEL', 'gpt-4o-mini'),
        delay=float(os.getenv('TRANSLATION_DELAY', '0.3'))
    )
    
    # 각 레시피 번역
    recipe_success = 0
    for recipe_id, title, description in missing_recipes:
        logger.info(f"\n번역 중 [{recipe_id}]: {title[:50]}...")
        
        try:
            # 제목 번역
            title_en = translator._translate_single(title) if translator._has_korean(title) else title
            
            # 설명 번역
            desc_en = translator._translate_single(description) if description and translator._has_korean(description) else description
            
            # DB 업데이트
            db.cursor.execute("""
                UPDATE recipes 
                SET title_en = %s, description_en = %s
                WHERE id = %s
            """, (title_en, desc_en, recipe_id))
            
            db.conn.commit()
            
            logger.info(f"✅ [{recipe_id}] {title[:40]}")
            logger.info(f"   EN: {title_en[:60]}")
            recipe_success += 1
            
        except Exception as e:
            logger.error(f"❌ [{recipe_id}] 실패: {e}")
            db.conn.rollback()
    
    # 각 조리 단계 번역
    step_success = 0
    for recipe_id, step_id, step_number, description in missing_steps:
        logger.info(f"\n조리 단계 번역 중 [{recipe_id}-{step_number}]: {description[:50]}...")
        
        try:
            # 조리 단계 번역
            step_en = translator._translate_single(description) if translator._has_korean(description) else description
            
            # DB 업데이트
            db.cursor.execute("""
                UPDATE cooking_steps 
                SET description_en = %s
                WHERE id = %s
            """, (step_en, step_id))
            
            db.conn.commit()
            
            logger.info(f"✅ [{recipe_id}-{step_number}] {description[:40]}")
            logger.info(f"   EN: {step_en[:60]}")
            step_success += 1
            
        except Exception as e:
            logger.error(f"❌ [{recipe_id}-{step_number}] 실패: {e}")
            db.conn.rollback()
    
    db.close()
    
    logger.info("\n" + "=" * 60)
    logger.info(f"📊 결과:")
    logger.info(f"   레시피: {recipe_success}/{len(missing_recipes)}개 번역 완료")
    logger.info(f"   조리 단계: {step_success}/{len(missing_steps)}개 번역 완료")
    logger.info("=" * 60)
    
    if recipe_success > 0 or step_success > 0:
        logger.info("\n✅ 번역이 완료되었습니다!")


if __name__ == '__main__':
    main()

