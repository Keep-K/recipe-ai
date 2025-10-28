#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
번역 누락 자동 수정 모듈
DB에 저장된 레시피 중 번역이 누락된 것을 JSON에서 찾아 자동 수정
"""

import json
import logging
from typing import Dict, List, Optional
from glob import glob

logger = logging.getLogger(__name__)


class TranslationFixer:
    """번역 누락 자동 수정"""
    
    def __init__(self, db):
        """
        Args:
            db: RecipeDB 인스턴스 (이미 연결된 상태)
        """
        self.db = db
        self.all_recipes_cache = None
    
    def load_all_json_files(self) -> List[Dict]:
        """모든 JSON 파일 로드 및 캐싱"""
        if self.all_recipes_cache is not None:
            return self.all_recipes_cache
        
        all_recipes = []
        json_files = sorted(glob('data/recipes_*.json'))
        
        for json_file in json_files:
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    all_recipes.extend(data)
            except Exception as e:
                logger.warning(f"⚠️  {json_file} 로드 실패: {e}")
        
        self.all_recipes_cache = all_recipes
        logger.info(f"📂 {len(all_recipes)}개 레시피 JSON 로드 완료")
        return all_recipes
    
    def find_recipe_by_title(self, recipes: List[Dict], title: str) -> Optional[Dict]:
        """제목으로 레시피 찾기 (번역이 있는 것만)"""
        for recipe in recipes:
            if recipe.get('title') == title:
                if recipe.get('title_en') or recipe.get('cooking_steps_en'):
                    return recipe
        return None
    
    def fix_recipe_translations(self, recipe_id: int, title: str, json_recipe: Dict) -> tuple:
        """레시피 번역 수정"""
        updated = []
        
        try:
            # 제목 번역 업데이트
            if json_recipe.get('title_en'):
                self.db.cursor.execute("""
                    UPDATE recipes 
                    SET title_en = %s, description_en = %s
                    WHERE id = %s
                """, (json_recipe.get('title_en'), 
                      json_recipe.get('description_en', ''),
                      recipe_id))
                updated.append('title')
            
            # 재료 번역 업데이트
            if json_recipe.get('ingredients_en'):
                self.db.cursor.execute("""
                    SELECT id FROM ingredients 
                    WHERE recipe_id = %s 
                    ORDER BY id
                """, (recipe_id,))
                ingredient_ids = [row[0] for row in self.db.cursor.fetchall()]
                
                for ing_id, ing_en in zip(ingredient_ids, json_recipe.get('ingredients_en', [])):
                    self.db.cursor.execute("""
                        UPDATE ingredients
                        SET name_en = %s
                        WHERE id = %s
                    """, (ing_en, ing_id))
                
                if ingredient_ids:
                    updated.append(f'{len(ingredient_ids)} ingredients')
            
            # 조리 단계 번역 업데이트
            if json_recipe.get('cooking_steps_en'):
                self.db.cursor.execute("""
                    SELECT id, step_number FROM cooking_steps 
                    WHERE recipe_id = %s 
                    ORDER BY step_number
                """, (recipe_id,))
                steps = self.db.cursor.fetchall()
                
                for (step_id, step_num), step_en in zip(steps, json_recipe.get('cooking_steps_en', [])):
                    self.db.cursor.execute("""
                        UPDATE cooking_steps
                        SET description_en = %s
                        WHERE id = %s
                    """, (step_en, step_id))
                
                if steps:
                    updated.append(f'{len(steps)} steps')
            
            self.db.conn.commit()
            return True, updated
            
        except Exception as e:
            self.db.conn.rollback()
            return False, str(e)
    
    def fix_all_missing_translations(self) -> dict:
        """모든 누락된 번역 자동 수정"""
        logger.info("\n🔧 번역 누락 검사 및 수정 시작...")
        
        # JSON 파일들 로드
        all_recipes = self.load_all_json_files()
        
        # 번역 누락된 레시피 찾기 (title_en이 없거나 한글 그대로인 경우)
        self.db.cursor.execute("""
            SELECT id, title 
            FROM recipes 
            WHERE title_en IS NULL 
               OR title_en = '' 
               OR title_en = title
            ORDER BY id
        """)
        missing_recipes = self.db.cursor.fetchall()
        
        if not missing_recipes:
            logger.info("✅ 모든 레시피에 번역이 있습니다.")
            return {
                'total': 0,
                'fixed': 0,
                'not_found': 0,
                'failed': 0
            }
        
        logger.info(f"🔍 번역 누락된 레시피: {len(missing_recipes)}개")
        
        fixed = 0
        not_found = 0
        failed = 0
        
        for recipe_id, title in missing_recipes:
            # JSON에서 해당 레시피 찾기
            json_recipe = self.find_recipe_by_title(all_recipes, title)
            
            if not json_recipe:
                logger.warning(f"⚠️  [{recipe_id}] {title[:40]}... - JSON에서 찾을 수 없음")
                not_found += 1
                continue
            
            # 번역 수정
            success, details = self.fix_recipe_translations(recipe_id, title, json_recipe)
            
            if success:
                logger.info(f"✅ [{recipe_id}] {title[:40]}... - {', '.join(details)}")
                fixed += 1
            else:
                logger.error(f"❌ [{recipe_id}] {title[:40]}... - 실패: {details}")
                failed += 1
        
        # 결과 요약
        result = {
            'total': len(missing_recipes),
            'fixed': fixed,
            'not_found': not_found,
            'failed': failed
        }
        
        logger.info(f"\n{'='*60}")
        logger.info(f"📊 번역 수정 결과")
        logger.info(f"{'='*60}")
        logger.info(f"   총 누락: {result['total']}개")
        logger.info(f"   ✅ 수정 완료: {result['fixed']}개")
        logger.info(f"   ⚠️  JSON 없음: {result['not_found']}개")
        logger.info(f"   ❌ 실패: {result['failed']}개")
        logger.info(f"{'='*60}\n")
        
        return result

