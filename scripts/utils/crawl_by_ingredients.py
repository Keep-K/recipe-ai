#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Batch crawler that collects up to 100 recipes per ingredient keyword.
The script reuses the existing RecipeCrawler and stores raw crawl results
as JSON files under data/crawled_by_ingredient/.
"""

import json
import logging
import os
import sys
import time
from pathlib import Path
from typing import Dict, List
from urllib.parse import quote_plus

from dotenv import load_dotenv


# -----------------------------------------------------------------------------
# 프로젝트 루트 설정 (run_batch_10k.sh 스타일과 동일하게 루트 기준으로 작동)
# -----------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[2]
os.chdir(PROJECT_ROOT)

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.crawler import RecipeCrawler, build_search_url  # noqa: E402

# Max recipes to collect per ingredient keyword
COUNT_PER_INGREDIENT = 100

# Ingredient keywords provided by the user
INGREDIENTS: List[str] = [
    "소고기",
    "돼지고기",
    "닭고기",
    "양고기",
    "염소고기",
    "햄",
    "베이컨",
    "소시지",
    "고등어",
    "삼치",
    "갈치",
    "조기",
    "명태",
    "대구",
    "연어",
    "참치",
    "광어",
    "새우",
    "게",
    "랍스터",
    "오징어",
    "문어",
    "낙지",
    "바지락",
    "홍합",
    "굴",
    "전복",
    "키조개",
    "쌀",
    "잡곡",
    "파스타",
    "국수",
    "라면",
    "쌀국수",
    "당면",
    "우동면",
    "밀가루",
    "식빵",
    "바게트",
    "감자",
    "고구마",
    "옥수수",
    "카사바",
    "배추",
    "양배추",
    "상추",
    "시금치",
    "깻잎",
    "토마토",
    "오이",
    "가지",
    "호박",
    "고추",
    "파프리카",
    "무",
    "당근",
    "양파",
    "마늘",
    "생강",
    "두부",
    "콩나물",
    "숙주나물",
    "완두콩",
    "강낭콩",
    "표고버섯",
    "느타리버섯",
    "팽이버섯",
    "새송이버섯",
    "양송이버섯",
    "계란",
    "우유",
    "치즈",
    "버터",
    "요거트",
    "생크림",
    "땅콩",
    "아몬드",
    "호두",
    "밤",
    "사과",
    "배",
    "바나나",
    "딸기",
    "오렌지",
    "메추리",
    "토끼고기",
    "사슴고기",
    "말고기",
    "칠면조",
    "거위",
    "장어",
    "아귀",
    "붕장어",
    "해삼",
    "멍게",
    "성게",
    "가리비",
    "소라",
    "꼬막",
    "메밀",
    "퀴노아",
    "귀리",
    "렌틸콩",
    "병아리콩",
    "타피오카",
    "아스파라거스",
    "아보카도",
    "비트",
    "샐러리",
    "브로콜리",
    "콜리플라워",
    "케일",
    "루꼴라",
    "리크",
    "아티초크",
    "트뤼프(송로버섯)",
    "모렐버섯",
    "달걀흰자",
    "마스카르포네 치즈",
    "리코타 치즈",
    "페타 치즈",
    "사워크림",
    "크림치즈",
    "캐슈넛",
    "피스타치오",
    "잣",
    "마카다미아",
    "코코넛",
    "망고",
    "파인애플",
    "레몬",
    "라임",
    "베리류(블루베리, 라즈베리)",
    "올리브",
    "케이퍼",
    "바닐라",
    "샤프란",
    "쿠민",
    "타임",
    "로즈마리",
    "바질",
    "오레가노",
    "월계수잎",
    "타마린드",
    "간장",
    "고추장",
    "된장",
    "피시소스",
    "굴소스",
    "발사믹 식초",
    "올리브 오일",
    "참기름",
    "달팽이",
    "캐비어",
    "푸아그라",
    "철갑상어",
    "청어",
    "멸치",
    "전갱이",
    "도미",
    "참치 뱃살(토로)",
    "복어",
    "해파리",
    "보리새우",
    "민물가재",
    "성게알",
    "미역",
    "다시마",
    "김",
    "톳",
    "곤약",
    "파스타면(링귀니, 펜네, 라비올리)",
    "폴렌타",
    "타르타르",
    "피망",
    "브뤼셀 스프라우트",
    "펜넬",
    "차이브",
    "딜",
    "고수(실란트로)",
    "레디시",
    "와사비",
    "무화과",
    "자두",
    "석류",
    "패션프루트",
    "용과",
    "아가베 시럽",
    "메이플 시럽",
    "꿀",
    "아몬드 밀크",
    "코코넛 밀크",
    "타히니",
    "누룩",
    "식용 장미",
    "캐러웨이",
    "카르다몸",
    "정향",
    "팔각",
    "마조람",
    "시나몬",
    "터메릭(강황)",
    "칠리 파우더",
    "겨자씨",
    "팜슈거",
    "라이스페이퍼",
    "전분(옥수수, 감자)",
]


def slugify(keyword: str) -> str:
    """Return a filesystem-safe slug for the ingredient name."""
    return quote_plus(keyword.strip())


def ensure_output_directory() -> Path:
    base_dir = Path("data") / "crawled_by_ingredient"
    base_dir.mkdir(parents=True, exist_ok=True)
    return base_dir


def configure_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )


def crawl_for_ingredient(
    crawler: RecipeCrawler,
    ingredient: str,
    max_items: int,
) -> List[Dict]:
    search_url = build_search_url(ingredient)
    logging.info("Search URL: %s", search_url)
    recipes = crawler.crawl_batch(search_url, max_items)
    logging.info("Collected %d recipes for '%s'", len(recipes), ingredient)
    return recipes


def main():
    configure_logging()
    load_dotenv("config/.env")

    delay = float(os.getenv("CRAWLING_DELAY", "1.0"))
    max_pages = int(os.getenv("CRAWLING_MAX_PAGES", "20"))
    sleep_between_keywords = float(os.getenv("CRAWLING_KEYWORD_DELAY", "2.0"))

    crawler = RecipeCrawler(delay=delay, max_pages=max_pages)
    output_dir = ensure_output_directory()

    total_recipes = 0
    summary: List[Dict[str, str]] = []

    for index, ingredient in enumerate(INGREDIENTS, start=1):
        logging.info("=" * 80)
        logging.info("[%03d/%03d] Crawling ingredient: %s", index, len(INGREDIENTS), ingredient)
        logging.info("=" * 80)

        try:
            recipes = crawl_for_ingredient(crawler, ingredient, COUNT_PER_INGREDIENT)
        except Exception as exc:
            logging.exception("Failed to crawl ingredient '%s': %s", ingredient, exc)
            continue

        if not recipes:
            logging.warning("No recipes collected for '%s'", ingredient)
            continue

        slug = slugify(ingredient)
        output_path = output_dir / f"{index:03d}_{slug}.json"

        with output_path.open("w", encoding="utf-8") as file:
            json.dump(recipes, file, ensure_ascii=False, indent=2)

        summary.append(
            {
                "ingredient": ingredient,
                "slug": slug,
                "file": str(output_path),
                "count": len(recipes),
            }
        )

        total_recipes += len(recipes)
        logging.info("Saved %d recipes -> %s", len(recipes), output_path)

        time.sleep(sleep_between_keywords)

    summary_path = output_dir / "summary.json"
    with summary_path.open("w", encoding="utf-8") as file:
        json.dump(
            {
                "total_ingredients": len(INGREDIENTS),
                "total_recipes": total_recipes,
                "per_ingredient": summary,
            },
            file,
            ensure_ascii=False,
            indent=2,
        )

    logging.info("Finished crawling. Total recipes: %d", total_recipes)
    logging.info("Summary saved to %s", summary_path)


if __name__ == "__main__":
    main()

