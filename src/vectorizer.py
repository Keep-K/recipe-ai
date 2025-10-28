#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
레시피 벡터화 모듈
- OpenAI Embeddings 또는 SentenceTransformers 사용
- PostgreSQL에 벡터 저장
"""

import os
import logging
from typing import List, Dict, Optional, Union
from openai import OpenAI
import time

logger = logging.getLogger(__name__)


class RecipeVectorizer:
    """레시피를 벡터로 변환하는 클래스"""
    
    def __init__(self, use_openai: bool = True, model_name: Optional[str] = None):
        """
        Args:
            use_openai: True면 OpenAI, False면 SentenceTransformers
            model_name: 사용할 모델 이름 (None이면 기본값)
        """
        self.use_openai = use_openai
        
        if use_openai:
            self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
            self.model = model_name or "text-embedding-3-small"
            self.dimensions = 1536
            logger.info(f"🤖 Using OpenAI Embeddings: {self.model}")
        else:
            try:
                from sentence_transformers import SentenceTransformer
                self.model = SentenceTransformer(model_name or 'all-MiniLM-L6-v2')
                self.dimensions = self.model.get_sentence_embedding_dimension()
                logger.info(f"🤖 Using SentenceTransformers: {model_name or 'all-MiniLM-L6-v2'}")
            except ImportError:
                raise ImportError("sentence-transformers not installed. Run: pip install sentence-transformers")
    
    def create_recipe_text(self, recipe: Dict) -> str:
        """
        레시피를 하나의 텍스트로 통합
        
        Args:
            recipe: 레시피 딕셔너리 (title_en, description_en, ingredients_en, cooking_steps_en)
        
        Returns:
            통합된 텍스트
        """
        parts = []
        
        # 제목
        if recipe.get('title_en'):
            parts.append(f"Title: {recipe['title_en']}")
        
        # 설명
        if recipe.get('description_en'):
            parts.append(f"Description: {recipe['description_en']}")
        
        # 재료
        ingredients = recipe.get('ingredients_en', [])
        if ingredients:
            if isinstance(ingredients, list):
                parts.append(f"Ingredients: {', '.join(str(i) for i in ingredients if i)}")
            else:
                parts.append(f"Ingredients: {ingredients}")
        
        # 조리 단계
        steps = recipe.get('cooking_steps_en', [])
        if steps:
            if isinstance(steps, list):
                steps_text = ' '.join(str(s) for s in steps if s)
                parts.append(f"Cooking Steps: {steps_text}")
            else:
                parts.append(f"Cooking Steps: {steps}")
        
        return "\n".join(parts)
    
    def vectorize(self, text: str) -> List[float]:
        """
        단일 텍스트를 벡터로 변환
        
        Args:
            text: 변환할 텍스트
        
        Returns:
            벡터 (리스트)
        """
        if not text or text.strip() == "":
            logger.warning("Empty text provided for vectorization")
            return [0.0] * self.dimensions
        
        if self.use_openai:
            try:
                response = self.client.embeddings.create(
                    model=self.model,
                    input=text
                )
                return response.data[0].embedding
            except Exception as e:
                logger.error(f"OpenAI embedding error: {e}")
                raise
        else:
            # SentenceTransformers
            return self.model.encode(text, show_progress_bar=False).tolist()
    
    def vectorize_batch(self, texts: List[str], batch_size: int = 100, delay: float = 1.0) -> List[List[float]]:
        """
        여러 텍스트를 배치로 벡터화
        
        Args:
            texts: 변환할 텍스트 리스트
            batch_size: 배치 크기 (OpenAI는 2048까지 가능)
            delay: 배치 간 딜레이 (초)
        
        Returns:
            벡터 리스트
        """
        if not texts:
            return []
        
        embeddings = []
        
        if self.use_openai:
            # OpenAI는 배치 처리 지원
            for i in range(0, len(texts), batch_size):
                batch = texts[i:i+batch_size]
                
                try:
                    response = self.client.embeddings.create(
                        model=self.model,
                        input=batch
                    )
                    batch_embeddings = [item.embedding for item in response.data]
                    embeddings.extend(batch_embeddings)
                    
                    logger.info(f"✅ Vectorized {i+len(batch)}/{len(texts)} recipes")
                    
                    # Rate limiting
                    if i + batch_size < len(texts):
                        time.sleep(delay)
                
                except Exception as e:
                    logger.error(f"Batch embedding error: {e}")
                    # 실패한 배치는 개별 처리
                    for text in batch:
                        try:
                            embeddings.append(self.vectorize(text))
                        except:
                            embeddings.append([0.0] * self.dimensions)
        else:
            # SentenceTransformers는 로컬이라 빠름
            embeddings = self.model.encode(texts, show_progress_bar=True, batch_size=batch_size).tolist()
        
        return embeddings
    
    def vectorize_recipe(self, recipe: Dict) -> List[float]:
        """
        레시피를 벡터로 변환 (통합 텍스트 생성 + 벡터화)
        
        Args:
            recipe: 레시피 딕셔너리
        
        Returns:
            벡터
        """
        text = self.create_recipe_text(recipe)
        return self.vectorize(text)


def main():
    """테스트용 메인 함수"""
    import json
    
    logger.info("=" * 60)
    logger.info("🧪 Vectorizer Test")
    logger.info("=" * 60)
    
    # 테스트 레시피
    test_recipe = {
        'title_en': 'Spicy Chicken Stir-fry',
        'description_en': 'A delicious spicy chicken dish perfect for dinner',
        'ingredients_en': ['chicken breast', 'gochujang', 'garlic', 'onion'],
        'cooking_steps_en': [
            'Cut the chicken into bite-sized pieces',
            'Stir-fry with gochujang sauce',
            'Serve hot with rice'
        ]
    }
    
    # OpenAI 테스트
    logger.info("\n🔹 Testing OpenAI Embeddings...")
    try:
        vectorizer_openai = RecipeVectorizer(use_openai=True)
        text = vectorizer_openai.create_recipe_text(test_recipe)
        logger.info(f"Combined text:\n{text}\n")
        
        vector = vectorizer_openai.vectorize_recipe(test_recipe)
        logger.info(f"✅ Vector dimension: {len(vector)}")
        logger.info(f"✅ First 5 values: {vector[:5]}")
    except Exception as e:
        logger.error(f"❌ OpenAI test failed: {e}")
    
    # SentenceTransformers 테스트
    logger.info("\n🔹 Testing SentenceTransformers...")
    try:
        vectorizer_local = RecipeVectorizer(use_openai=False)
        vector = vectorizer_local.vectorize_recipe(test_recipe)
        logger.info(f"✅ Vector dimension: {len(vector)}")
        logger.info(f"✅ First 5 values: {vector[:5]}")
    except Exception as e:
        logger.error(f"❌ SentenceTransformers test failed: {e}")
    
    logger.info("\n" + "=" * 60)
    logger.info("✅ Test completed!")


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    main()

