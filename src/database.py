#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
효율적인 DB 관리자
- PostgreSQL 연결 및 CRUD
- 레시피 전용 스키마
"""

import os
import psycopg2
from psycopg2.extras import execute_values
import logging
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)


class RecipeDB:
    """레시피 데이터베이스 관리"""
    
    def __init__(self, db_name: str = 'recipe_ai_db', user: str = 'keep'):
        self.db_name = db_name
        self.user = user
        self.conn = None
        self.cursor = None
    
    def connect(self):
        """DB 연결: 우선순위 1) DATABASE_URL, 2) 로컬 기본값"""
        try:
            database_url = os.getenv('DATABASE_URL')
            if database_url:
                # Railway/클라우드 환경: DATABASE_URL 사용
                self.conn = psycopg2.connect(database_url)
            else:
                # 로컬 개발 환경: 명시적 파라미터 사용
                self.conn = psycopg2.connect(
                    host=os.getenv('DB_HOST', 'localhost'),
                    database=self.db_name,
                    user=self.user,
                    password=os.getenv('DB_PASSWORD', '')
                )
            self.cursor = self.conn.cursor()
            logger.info("✅ Connected to database")
        except Exception as e:
            logger.error(f"❌ DB connection failed: {e}")
            raise
    
    def close(self):
        """연결 종료"""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        logger.info("DB connection closed")
    
    def insert_recipe(self, recipe: Dict) -> Optional[int]:
        """레시피 삽입 (중복 체크)"""
        try:
            # recipe_id 생성
            recipe_id = recipe['url'].split('/')[-1] if recipe.get('url') else None
            
            # 중복 체크
            self.cursor.execute(
                "SELECT id FROM recipes WHERE recipe_id = %s",
                (recipe_id,)
            )
            existing = self.cursor.fetchone()
            if existing:
                logger.warning(f"⚠️  Skipped duplicate: {recipe.get('title')} (ID: {recipe_id})")
                return None
            
            self.cursor.execute("""
                INSERT INTO recipes (
                    recipe_id, title, title_en, description, description_en,
                    url, servings, cooking_time, difficulty
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'medium')
                RETURNING id
            """, (
                recipe_id,
                recipe.get('title'),
                recipe.get('title_en'),
                recipe.get('description'),
                recipe.get('description_en'),
                recipe.get('url'),
                recipe.get('servings'),
                recipe.get('cooking_time')
            ))
            
            db_id = self.cursor.fetchone()[0]
            
            # 재료 삽입
            self._insert_ingredients(db_id, recipe.get('ingredients', []), 
                                    recipe.get('ingredients_en', []))
            
            # 조리 단계 삽입
            self._insert_steps(db_id, recipe.get('cooking_steps', []),
                              recipe.get('cooking_steps_en', []))
            
            self.conn.commit()
            logger.info(f"✅ Inserted recipe ID {db_id}: {recipe.get('title')}")
            return db_id
            
        except Exception as e:
            logger.error(f"❌ Insert failed: {e}")
            self.conn.rollback()
            return None
    
    def _insert_ingredients(self, recipe_id: int, ingredients: List, 
                           ingredients_en: List):
        """재료 삽입"""
        for i, ing in enumerate(ingredients):
            ing_name = ing if isinstance(ing, str) else str(ing)
            ing_en = ingredients_en[i] if i < len(ingredients_en) else ing_name
            
            self.cursor.execute("""
                INSERT INTO ingredients (recipe_id, name, name_en, amount)
                VALUES (%s, %s, %s, %s)
            """, (recipe_id, ing_name, ing_en, ing_name))
    
    def _insert_steps(self, recipe_id: int, steps: List, steps_en: List):
        """조리 단계 삽입"""
        for i, step in enumerate(steps, 1):
            step_text = step.get('text', '') if isinstance(step, dict) else step
            step_en = steps_en[i-1] if i-1 < len(steps_en) else step_text
            step_img = step.get('image', '') if isinstance(step, dict) else ''
            
            self.cursor.execute("""
                INSERT INTO cooking_steps (
                    recipe_id, step_number, description, description_en, image_url
                )
                VALUES (%s, %s, %s, %s, %s)
            """, (recipe_id, i, step_text, step_en, step_img))
    
    def insert_batch(self, recipes: List[Dict]) -> int:
        """배치 삽입"""
        success = 0
        for recipe in recipes:
            if self.insert_recipe(recipe):
                success += 1
        logger.info(f"Batch insert complete: {success}/{len(recipes)}")
        return success
    
    def get_recipes(self, limit: int = 10) -> List[Dict]:
        """레시피 조회"""
        self.cursor.execute("""
            SELECT id, title, title_en, difficulty, cooking_time
            FROM recipes
            ORDER BY id DESC
            LIMIT %s
        """, (limit,))
        
        return [
            {
                'id': row[0],
                'title': row[1],
                'title_en': row[2],
                'difficulty': row[3],
                'cooking_time': row[4]
            }
            for row in self.cursor.fetchall()
        ]

