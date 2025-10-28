#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Recipe AI System - 통합 실행 스크립트
크롤링 → 번역 → DB 저장을 한 번에 실행
"""

import os
import json
import logging
from datetime import datetime
from dotenv import load_dotenv

from src.crawler import RecipeCrawler, build_category_url
from src.translator import RecipeTranslator
from src.database import RecipeDB
from src.translation_fixer import TranslationFixer

# 환경 변수 로드
load_dotenv('config/.env')

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/main.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class RecipeAISystem:
    """통합 레시피 AI 시스템"""
    
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.db_name = os.getenv('DB_NAME', 'recipe_ai_db')
        self.db_user = os.getenv('DB_USER', 'recipe_keep')
        
        # 크롤링 설정
        self.category = {
            'type': os.getenv('RECIPE_TYPE', '밑반찬'),
            'situation': os.getenv('RECIPE_SITUATION', '일상'),
            'ingredient': os.getenv('RECIPE_INGREDIENT', '소고기'),
            'method': os.getenv('RECIPE_METHOD', '볶음')
        }
        self.max_recipes = int(os.getenv('MAX_RECIPES', '10'))
        
        # 컴포넌트 초기화
        self.crawler = RecipeCrawler(delay=float(os.getenv('CRAWLING_DELAY', '1.0')))
        
        # 멀티 API 키 로드 (최대 10개)
        api_keys = []
        for i in range(1, 11):
            key_name = f'OPENAI_API_KEY_{i}' if i > 1 else 'OPENAI_API_KEY'
            key = os.getenv(key_name)
            if key and key != 'your-api-key-here':
                api_keys.append(key)
        
        self.translator = RecipeTranslator(
            api_keys=api_keys,
            model=os.getenv('OPENAI_MODEL', 'gpt-4o-mini'),
            delay=float(os.getenv('TRANSLATION_DELAY', '2.0'))
        )
        self.db = RecipeDB(self.db_name, self.db_user)
    
    def run(self, save_json: bool = True, fix_translations: bool = True):
        """전체 파이프라인 실행"""
        logger.info("=" * 60)
        logger.info("🚀 Recipe AI System Started")
        logger.info("=" * 60)
        
        try:
            # 1. 크롤링
            logger.info(f"\n📖 Step 1: Crawling recipes...")
            logger.info(f"   Category: {self.category}")
            logger.info(f"   Max recipes: {self.max_recipes}")
            
            category_url = build_category_url(
                recipe_type=self.category['type'],
                situation=self.category['situation'],
                ingredient=self.category['ingredient'],
                method=self.category['method']
            )
            recipes = self.crawler.crawl_batch(category_url, self.max_recipes)
            
            if not recipes:
                logger.error("No recipes crawled. Exiting.")
                return
            
            logger.info(f"✅ Crawled {len(recipes)} recipes")
            
            # 2. 번역
            logger.info(f"\n🌐 Step 2: Translating recipes...")
            translated_recipes = self.translator.translate_all(recipes)
            logger.info(f"✅ Translated {len(translated_recipes)} recipes")
            
            # 3. JSON 저장 (선택사항)
            if save_json:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                json_path = f"data/recipes_{timestamp}.json"
                os.makedirs('data', exist_ok=True)
                
                with open(json_path, 'w', encoding='utf-8') as f:
                    json.dump(translated_recipes, f, ensure_ascii=False, indent=2)
                logger.info(f"💾 Saved to {json_path}")
            
            # 4. DB 저장
            logger.info(f"\n💾 Step 3: Saving to database...")
            self.db.connect()
            success_count = self.db.insert_batch(translated_recipes)
            
            # 5. 번역 누락 자동 수정 (선택사항)
            if fix_translations:
                logger.info(f"\n🔧 Step 4: Fixing missing translations...")
                fixer = TranslationFixer(self.db)
                fix_result = fixer.fix_all_missing_translations()
            
            self.db.close()
            
            logger.info(f"✅ Saved {success_count}/{len(translated_recipes)} recipes to DB")
            
            # 결과 요약
            logger.info("\n" + "=" * 60)
            logger.info("📊 Summary")
            logger.info("=" * 60)
            logger.info(f"   Crawled: {len(recipes)} recipes")
            logger.info(f"   Translated: {len(translated_recipes)} recipes")
            logger.info(f"   Saved to DB: {success_count} recipes")
            if fix_translations:
                logger.info(f"   Fixed translations: {fix_result['fixed']} recipes")
            logger.info(f"   Database: {self.db_name}")
            logger.info("=" * 60)
            logger.info("✅ Pipeline completed successfully!")
            
        except Exception as e:
            logger.error(f"❌ Pipeline failed: {e}")
            raise


def main():
    """메인 실행"""
    import sys
    
    # 명령행 인자로 초기화 옵션 제공
    reset_db = False
    skip_prompt = False
    
    if '--reset-db' in sys.argv:
        reset_db = True
    if '--no-prompt' in sys.argv:
        skip_prompt = True  # 배치 실행 시 프롬프트 건너뛰기
    
    # 대화형 모드 (인자 없을 때만)
    if len(sys.argv) == 1 and not skip_prompt:
        print("\n" + "="*60)
        print("🍳 Recipe AI System")
        print("="*60)
        
        # DB 초기화 확인
        response = input("\n⚠️  DB를 초기화하고 시작하시겠습니까? (y/N): ").strip().lower()
        reset_db = response in ['y', 'yes', '예']
    
    system = RecipeAISystem()
    
    # DB 초기화
    if reset_db:
        logger.info("\n🗑️  DB 초기화 중...")
        try:
            import psycopg2
            conn = psycopg2.connect(
                dbname=system.db_name,
                user=system.db_user,
                password=os.getenv('DB_PASSWORD', 'wkwjsrj4510*'),
                host=os.getenv('DB_HOST', 'localhost')
            )
            cursor = conn.cursor()
            
            cursor.execute("""
                TRUNCATE recipes CASCADE;
                ALTER SEQUENCE recipes_id_seq RESTART WITH 1;
                ALTER SEQUENCE ingredients_id_seq RESTART WITH 1;
                ALTER SEQUENCE cooking_steps_id_seq RESTART WITH 1;
            """)
            
            conn.commit()
            cursor.close()
            conn.close()
            
            logger.info("✅ DB 초기화 완료\n")
        except Exception as e:
            logger.error(f"❌ DB 초기화 실패: {e}")
            return
    
    system.run(save_json=True)


if __name__ == '__main__':
    main()

