#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
효율적인 레시피 번역기
- 한글만 선택 번역
- 멀티 API 키 로드밸런싱
- 병렬 처리
- 캐시 시스템
"""

import os
import json
import time
import logging
import re
from typing import List, Dict, Optional
from openai import OpenAI
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock
import random

logger = logging.getLogger(__name__)


class RecipeTranslator:
    """한글만 효율적으로 번역 (멀티 API 키 지원)"""
    
    def __init__(self, api_keys: List[str] = None, model: str = 'gpt-4o-mini', 
                 delay: float = 2.0, cache_file: str = 'logs/translation_cache.json'):
        # 멀티 API 키 설정
        if api_keys is None:
            # 환경변수에서 모든 API 키 로드
            api_keys = []
            for i in range(1, 11):  # 최대 10개까지
                key_name = f'OPENAI_API_KEY_{i}' if i > 1 else 'OPENAI_API_KEY'
                key = os.getenv(key_name)
                if key and key != 'your-api-key-here' and key not in api_keys:
                    api_keys.append(key)
        
        if not api_keys:
            raise ValueError("No valid API keys found")
        
        self.api_keys = api_keys
        self.clients = [OpenAI(api_key=key) for key in api_keys]
        self.current_key_index = 0
        
        logger.info(f"🔑 Loaded {len(self.api_keys)} API key(s)")
        
        self.model = model
        self.delay = delay
        self.cache_file = cache_file
        self.cache = self._load_cache()
        self.cache_lock = Lock()  # Thread-safe 캐시 접근
        self.hangul_pattern = re.compile(r'[\uAC00-\uD7A3]')
    
    def _get_client(self) -> OpenAI:
        """라운드 로빈 방식으로 클라이언트 선택"""
        client = self.clients[self.current_key_index]
        self.current_key_index = (self.current_key_index + 1) % len(self.clients)
        return client
    
    def _load_cache(self) -> Dict:
        """캐시 로드"""
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def _save_cache(self):
        """캐시 저장"""
        os.makedirs(os.path.dirname(self.cache_file), exist_ok=True)
        with open(self.cache_file, 'w', encoding='utf-8') as f:
            json.dump(self.cache, f, ensure_ascii=False, indent=2)
    
    def _has_korean(self, text: str) -> bool:
        """한글 포함 여부 확인"""
        return bool(text and self.hangul_pattern.search(text))
    
    def _translate_batch(self, texts: List[str]) -> List[str]:
        """배치 번역 (개별 처리로 정확성 보장)"""
        if not texts:
            return []
        
        results = []
        
        for text in texts:
            # 한글이 없으면 그대로 반환
            if not self._has_korean(text):
                results.append(text)
                continue
            
            # 캐시에 있으면 사용
            if text in self.cache:
                results.append(self.cache[text])
                continue
            
            # 개별 번역
            translated = self._translate_single(text)
            results.append(translated)
            
            # 캐시 저장
            self.cache[text] = translated
            self._save_cache()
            
            # API 호출 간 딜레이
            time.sleep(self.delay)
        
        return results
    
    def _translate_single(self, text: str) -> str:
        """단일 텍스트 번역 (멀티 키 사용, 딜레이 포함)"""
        result = self._translate_single_no_delay(text)
        time.sleep(self.delay)  # Rate limit 보호
        return result
    
    def _translate_single_no_delay(self, text: str) -> str:
        """단일 텍스트 번역 (딜레이 없음 - 병렬 처리용)"""
        prompt = (
            "Translate ONLY the Korean parts to plain English. "
            "Keep all English words, numbers, units unchanged. "
            "Output only the translated text.\n\n"
            f"{text}"
        )
        
        try:
            # 라운드 로빈으로 클라이언트 선택
            client = self._get_client()
            
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Translate only Korean to English. Keep formatting."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.2
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"Translation error: {e}")
            return text
    
    def translate_recipe(self, recipe: Dict) -> Dict:
        """레시피 전체 번역 (필드별 병렬 처리)"""
        translated = recipe.copy()
        
        # 모든 번역할 텍스트를 한 번에 수집
        to_translate = []
        
        # 제목
        title = recipe.get('title', '')
        if self._has_korean(title):
            to_translate.append(('title', title))
        
        # 설명
        desc = recipe.get('description', '')
        if self._has_korean(desc):
            to_translate.append(('description', desc))
        
        # 재료
        ingredients = recipe.get('ingredients', [])
        for i, ing in enumerate(ingredients):
            ing_text = ing if isinstance(ing, str) else ing.get('original', '')
            if self._has_korean(ing_text):
                to_translate.append(('ingredient', i, ing_text))
        
        # 조리 단계
        steps = recipe.get('cooking_steps', [])
        for i, step in enumerate(steps):
            step_text = step.get('text', '') if isinstance(step, dict) else step
            if self._has_korean(step_text):
                to_translate.append(('step', i, step_text))
        
        # 중복 제거 및 캐시 확인
        unique_texts = []
        text_to_item = {}
        
        for item in to_translate:
            text = item[-1]
            if text not in self.cache and text not in text_to_item:
                unique_texts.append(text)
                text_to_item[text] = item
        
        # 병렬 번역 (캐시에 없는 것만) - Thread-safe
        if unique_texts:
            with ThreadPoolExecutor(max_workers=min(len(self.clients), len(unique_texts))) as executor:
                future_to_text = {
                    executor.submit(self._translate_single_no_delay, text): text 
                    for text in unique_texts
                }
                
                for future in as_completed(future_to_text):
                    text = future_to_text[future]
                    try:
                        trans = future.result()
                        with self.cache_lock:  # Thread-safe
                            self.cache[text] = trans
                    except Exception as e:
                        logger.error(f"Translation failed: {e}")
                        with self.cache_lock:  # Thread-safe
                            self.cache[text] = text
            
            with self.cache_lock:  # Thread-safe
                self._save_cache()
        
        # 결과 적용
        translated['ingredients_en'] = [None] * len(ingredients)
        translated['cooking_steps_en'] = [None] * len(steps)
        
        for item in to_translate:
            text = item[-1]
            trans = self.cache.get(text, text)
            
            if item[0] == 'title':
                translated['title_en'] = trans
            elif item[0] == 'description':
                translated['description_en'] = trans
            elif item[0] == 'ingredient':
                translated['ingredients_en'][item[1]] = trans
            elif item[0] == 'step':
                translated['cooking_steps_en'][item[1]] = trans
        
        # None 제거
        translated['ingredients_en'] = [x for x in translated['ingredients_en'] if x]
        translated['cooking_steps_en'] = [x for x in translated['cooking_steps_en'] if x]
        
        logger.info(f"✅ Translated: {recipe.get('title', 'Unknown')}")
        return translated
    
    def translate_all(self, recipes: List[Dict]) -> List[Dict]:
        """모든 레시피 병렬 번역 (멀티 키 활용)"""
        logger.info(f"Translating {len(recipes)} recipes with {len(self.clients)} API key(s)...")
        
        if len(self.clients) == 1:
            # 단일 키면 순차 처리
            return [self.translate_recipe(r) for r in recipes]
        
        # 멀티 키면 병렬 처리
        max_workers = min(len(self.clients), len(recipes))
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(self.translate_recipe, recipe): recipe 
                      for recipe in recipes}
            
            results = []
            for future in as_completed(futures):
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    logger.error(f"Translation failed: {e}")
                    results.append(futures[future])  # 원본 유지
        
        # 원래 순서대로 정렬
        recipe_order = {r['url']: i for i, r in enumerate(recipes)}
        results.sort(key=lambda x: recipe_order.get(x['url'], 999))
        
        return results

