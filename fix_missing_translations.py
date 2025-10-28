#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
누락된 번역 자동 수정 스크립트 (독립 실행용)
main.py에서 자동으로 실행되므로 별도 실행은 필요 없습니다.
"""

import logging
import os
from dotenv import load_dotenv

# 프로젝트 루트로 이동
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.database import RecipeDB
from src.translation_fixer import TranslationFixer

# 환경 변수 로드
load_dotenv('config/.env')

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """메인 실행"""
    logger.info("=" * 60)
    logger.info("🔧 Translation Fixer - 독립 실행 모드")
    logger.info("=" * 60)
    logger.info("ℹ️  일반적으로 main.py에서 자동 실행됩니다.")
    logger.info("ℹ️  수동으로 번역 수정만 하고 싶을 때 이 스크립트를 사용하세요.\n")
    
    # DB 연결
    db_name = os.getenv('DB_NAME', 'recipe_ai_db')
    db_user = os.getenv('DB_USER', 'recipe_keep')
    
    db = RecipeDB(db_name, db_user)
    db.connect()
    
    # 번역 수정 실행
    fixer = TranslationFixer(db)
    result = fixer.fix_all_missing_translations()
    
    db.close()
    
    # 최종 결과
    if result['fixed'] > 0:
        logger.info("✅ 번역 수정이 완료되었습니다!")
    elif result['not_found'] > 0:
        logger.warning("⚠️  일부 레시피는 JSON 파일에서 번역을 찾을 수 없습니다.")
        logger.warning("   → 해당 레시피들을 다시 수집하거나 수동 번역이 필요합니다.")
    else:
        logger.info("✅ 모든 레시피에 번역이 있습니다!")


if __name__ == '__main__':
    main()

