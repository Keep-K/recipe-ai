#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
효율적인 레시피 크롤러
- JSON-LD 기반 데이터 추출
- 재사용 가능한 클래스 구조
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import logging
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)


class RecipeCrawler:
    """10000recipe.com 레시피 크롤러"""
    
    def __init__(self, delay: float = 1.0):
        self.base_url = "https://www.10000recipe.com"
        self.headers = {'User-Agent': 'Mozilla/5.0'}
        self.delay = delay
    
    def crawl_recipe(self, recipe_url: str) -> Optional[Dict]:
        """단일 레시피 크롤링"""
        try:
            response = requests.get(recipe_url, headers=self.headers, timeout=10)
            if response.status_code != 200:
                logger.error(f"Failed to fetch {recipe_url}: {response.status_code}")
                return None
            
            soup = BeautifulSoup(response.text, 'html.parser')
            json_ld = soup.find('script', {'type': 'application/ld+json'})
            
            if not json_ld:
                logger.warning(f"No JSON-LD found in {recipe_url}")
                return None
            
            data = json.loads(json_ld.string)
            
            return {
                'url': recipe_url,
                'title': data.get('name', ''),
                'description': data.get('description', ''),
                'servings': data.get('recipeYield', ''),
                'cooking_time': data.get('totalTime', ''),
                'ingredients': data.get('recipeIngredient', []),
                'cooking_steps': data.get('recipeInstructions', []),
                'image_url': data.get('image', ''),
                'author': data.get('author', {}).get('name', ''),
                'category': data.get('recipeCategory', '')
            }
        except Exception as e:
            logger.error(f"Error crawling {recipe_url}: {e}")
            return None
    
    def get_recipe_urls(self, category_url: str, max_count: int = 10) -> List[str]:
        """카테고리에서 레시피 URL 목록 추출"""
        try:
            response = requests.get(category_url, headers=self.headers, timeout=10)
            if response.status_code != 200:
                return []
            
            soup = BeautifulSoup(response.text, 'html.parser')
            links = soup.select('#contents_area_full > ul > ul > li > div.common_sp_thumb > a')
            
            urls = []
            for link in links[:max_count]:
                href = link.get('href')
                if href:
                    urls.append(self.base_url + href)
            
            logger.info(f"Found {len(urls)} recipe URLs")
            return urls
        except Exception as e:
            logger.error(f"Error getting recipe URLs: {e}")
            return []
    
    def crawl_batch(self, category_url: str, max_count: int = 10) -> List[Dict]:
        """배치 크롤링"""
        logger.info(f"Starting batch crawl (max: {max_count})")
        
        urls = self.get_recipe_urls(category_url, max_count)
        recipes = []
        
        for i, url in enumerate(urls, 1):
            logger.info(f"Crawling {i}/{len(urls)}: {url}")
            recipe = self.crawl_recipe(url)
            
            if recipe:
                recipes.append(recipe)
                logger.info(f"✅ Success: {recipe['title']}")
            else:
                logger.warning(f"❌ Failed: {url}")
            
            if i < len(urls):
                time.sleep(self.delay)
        
        logger.info(f"Batch crawl complete: {len(recipes)}/{len(urls)} successful")
        return recipes


def build_category_url(recipe_type: str, situation: str, ingredient: str, method: str) -> str:
    """카테고리 URL 생성 (10000recipe.com 실제 태그 사용)"""
    # crowling_next.py에서 추출한 실제 카테고리 태그
    CATEGORIES = {
        'type': {  # cat4
            '밑반찬': '63', '메인반찬': '56', '국/탕': '54', '찌개': '55', 
            '디저트': '60', '면/만두': '53', '밥/죽/떡': '52', '퓨전': '61', 
            '양념/잼/소스': '58', '양식': '65', '샐러드': '64', '스프': '68',
            '빵': '66', '과자': '69', '차/음료/술': '59',
            # 별칭
            '일품요리': '56', '찜': '55', '튀김': '60', '부침': '63', '김치': '63', '음료': '59'
        },
        'situation': {  # cat2
            '일상': '12', '초스피드': '18', '손님접대': '13', '술안주': '19', 
            '다이어트': '21', '도시락': '15', '영양식': '43', '간식': '17', 
            '야식': '45', '명절': '44'
        },
        'ingredient': {  # cat3
            '소고기': '70', '돼지고기': '71', '닭고기': '72', '육류': '23', 
            '채소류': '28', '해물류': '24', '달걀/유제품': '50', '쌀': '47', 
            '밀가루': '32', '건어물류': '25', '버섯류': '31', '과일류': '48', '곡류': '26',
            # 별칭 및 구체적 재료
            '생선류': '24', '오징어': '24', '낙지': '24', '새우': '24', 
            '조개류': '24', '전복': '24', '문어': '24', '해파리': '24', '게': '24',
            '두부': '50', '버섯': '31', '가지': '28', '호박': '28', '오이': '28',
            '감자': '28', '고구마': '28', '콩나물': '28', '시금치': '28', '파': '28',
            '고사리': '28', '도라지': '28', '더덕': '28', '마늘종': '28',
            '청경채': '28', '쑥갓': '28', '취나물': '28', '냉이': '28', '달래': '28',
            '부추': '28', '상추': '28', '배추': '28', '미나리': '28', '숙주': '28',
            '깻잎': '28', '브로콜리': '28', '김치': '28', '야채': '28',
            '김': '25', '참치': '25', '멸치': '25', '북어': '25', '어묵': '25',
            '계란': '50', '우유': '50', '치즈': '50', '베이컨': '50', '햄': '50',
            '면': '32', '파스타': '32', '떡': '47', '만두': '32', '빵': '32',
            '밥': '47', '잡곡': '47', '현미': '47', '보리': '47', '콩': '26',
            '당면': '32', '엿기름': '26', '한약재': '28', '계피': '48',
            '유자': '48', '대추': '48', '매실': '48', '모과': '48',
            '딸기': '48', '바나나': '48', '망고': '48', '블루베리': '48',
            '키위': '48', '아보카도': '48', '오렌지': '48', '사과': '48',
            '포도': '48', '토마토': '48', '당근': '48', '레몬': '48', '자몽': '48',
            '커피': '59', '녹차': '59', '차': '59', '과일': '48',
            '미역': '28', '된장': '28', '청국장': '28', '고추장': '28',
            '해물': '24', '소시지': '50', '순대': '71', '아귀': '24', '복어': '24',
            '미꾸라지': '24', '시래기': '28', '아욱': '28', '팥': '26',
            '흑임자': '26', '잣': '26', '녹두': '26', '도토리묵': '28',
            '청포묵': '28', '파래': '28', '톳': '28', '다시마': '28',
            '무': '28', '갓': '28', '열무': '28', '명란': '24', '명태': '24',
            '황석어': '24', '갈치': '24', '조기': '24', '꿀': '48', '얼음': '48',
            '가오리': '24', '굴': '24', '바지락': '24', '재첩': '24', '홍합': '24'
        },
        'method': {  # cat1
            '볶음': '6', '끓이기': '1', '부침': '7', '조림': '36', '무침': '41', 
            '비빔': '42', '찜': '8', '절임': '10', '튀김': '9', '삶기': '38', 
            '굽기': '67', '회': '37',
            # 별칭
            '구이': '67', '만들기': '6', '짓기': '1', '찌기': '8', '갈기': '6', 
            '얼리기': '10', '데우기': '1'
        }
    }
    
    t = CATEGORIES['type'].get(recipe_type, '63')
    s = CATEGORIES['situation'].get(situation, '12')
    i = CATEGORIES['ingredient'].get(ingredient, '70')
    m = CATEGORIES['method'].get(method, '6')
    
    return (f'https://www.10000recipe.com/recipe/list.html?'
            f'cat1={m}&cat2={s}&cat3={i}&cat4={t}&order=reco')

