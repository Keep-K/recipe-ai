#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
레시피 AI 채팅 서버 (FastAPI)
"""

import os
import json
import logging
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

from src.database import RecipeDB
from src.vectorizer import RecipeVectorizer

# 환경 변수 로드
load_dotenv('config/.env')

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI 앱 생성
app = FastAPI(
    title="Recipe AI Chat API",
    description="레시피 추천 채팅 AI 서버",
    version="1.0.0"
)

# CORS 설정 (Firebase에서 접근 가능하도록)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 프로덕션에서는 특정 도메인으로 제한
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic 모델들
class ChatMessage(BaseModel):
    message: str
    user_id: Optional[str] = "default"
    # 사용자 취향 컨트롤: less|normal|more
    spiciness: Optional[str] = "normal"
    saltiness: Optional[str] = "normal"

class RecipeResponse(BaseModel):
    id: int
    title: str
    title_en: str
    description_en: str
    cooking_time: str  # 문자열로 변경
    servings: str      # 문자열로 변경
    similarity: float

class ChatResponse(BaseModel):
    message: str
    # 마크다운 형식의 응답 (섹션/리스트 포함)
    markdown_message: Optional[str] = None
    recipes: List[RecipeResponse]
    suggestions: List[str]

class RecipeDetail(BaseModel):
    id: int
    title: str
    title_en: str
    description_en: str
    cooking_time: str  # 문자열로 변경
    servings: str      # 문자열로 변경
    ingredients: List[str]
    cooking_steps: List[str]

class UserPrefs(BaseModel):
    user_id: Optional[str] = "default"
    spiciness: Optional[str] = "normal"
    saltiness: Optional[str] = "normal"

# 전역 변수
db = None
vectorizer = None
# 간단한 인메모리 대화 내역 저장소 (프로덕션은 Redis/DB 권장)
chat_histories: dict[str, list[dict[str, str]]] = {}
# 간단한 인메모리 사용자 취향 저장소
user_prefs: dict[str, dict[str, str]] = {}
translate_cache: dict[str, str] = {}

# -------- 유틸 함수들 --------
def format_duration_korean(value: Optional[str]) -> str:
    if not value:
        return "미정"
    s = str(value)
    # ISO8601 like PT30M, PT1H30M, PT45S
    if s.startswith('PT'):
        hours = minutes = seconds = 0
        cur = s[2:]
        num = ''
        for ch in cur:
            if ch.isdigit():
                num += ch
            else:
                if ch == 'H':
                    hours = int(num or 0)
                elif ch == 'M':
                    minutes = int(num or 0)
                elif ch == 'S':
                    seconds = int(num or 0)
                num = ''
        parts = []
        if hours:
            parts.append(f"{hours}시간")
        if minutes:
            parts.append(f"{minutes}분")
        if seconds and not parts:
            parts.append(f"{seconds}초")
        return ' '.join(parts) or "미정"
    # already like '30분'
    if any(u in s for u in ['분', '시간', '초']):
        return s
    # plain number treat as minutes
    try:
        n = int(''.join([c for c in s if c.isdigit()]))
        if n:
            return f"{n}분"
    except Exception:
        pass
    return s

def format_servings_korean(value: Optional[str]) -> str:
    if not value:
        return "미정"
    s = str(value)
    # e.g., '4 servings', '2인분'
    digits = ''.join([c for c in s if c.isdigit()])
    if digits:
        return f"{int(digits)}인분"
    return s

def translate_to_korean(openai_client, text: Optional[str]) -> str:
    if not text:
        return ""
    if text in translate_cache:
        return translate_cache[text]
    try:
        resp = openai_client.chat.completions.create(
            model=os.getenv('OPENAI_MODEL', 'gpt-4o-mini'),
            messages=[
                {"role": "system", "content": "Translate the following to natural Korean. Reply with Korean text only."},
                {"role": "user", "content": text}
            ],
            max_tokens=80,
            temperature=0.2
        )
        ko = (resp.choices[0].message.content or '').strip()
        translate_cache[text] = ko
        return ko
    except Exception:
        return text or ""

def classify_ingredient(name: str) -> str:
    text = (name or '').lower()
    seasoning_kw = [
        '간장','고추장','된장','소금','설탕','후추','식용유','참기름','고춧가루','다진 마늘','마늘','양념','청주','미림','식초','버터','올리브유','우스터','소스','후춧가루','설탕','꿀','고추기름','된장','쌈장','파우더','조미료'
    ]
    main_kw = [
        '닭','소고기','돼지고기','쇠고기','양고기','생선','새우','오징어','문어','두부','두유','베이컨','햄','계란','달걀','면','파스타','밥','쌀','감자','고구마','버섯','두껍','스테이크'
    ]
    if any(k in text for k in seasoning_kw):
        return 'seasoning'
    if any(k in text for k in main_kw):
        return 'main'
    return 'sub'

def split_ingredients_kor(ings: list[str]) -> dict:
    result = {'main': [], 'sub': [], 'seasoning': []}
    for ing in ings:
        cat = classify_ingredient(ing)
        result[cat].append(ing)
    return result

def group_steps_kor(steps: list[str]) -> list[tuple[str, list[str]]]:
    groups: list[tuple[str, list[str]]] = []
    buckets = {
        '준비': [],
        '볶기/굽기': [],
        '끓이기/조림': [],
        '마무리': []
    }
    for s in steps:
        t = s.lower()
        if any(k in t for k in ['손질','썰','자르','씻','준비','해동','다지']):
            buckets['준비'].append(s)
        elif any(k in t for k in ['볶','굽','부침','지지','볶아','팬','프라이팬']):
            buckets['볶기/굽기'].append(s)
        elif any(k in t for k in ['끓','조리','졸','끓이','煮']):
            buckets['끓이기/조림'].append(s)
        elif any(k in t for k in ['완성','담','섞','간','추가','서빙']):
            buckets['마무리'].append(s)
        else:
            buckets['마무리'].append(s)
    for k in ['준비','볶기/굽기','끓이기/조림','마무리']:
        if buckets[k]:
            groups.append((k, buckets[k]))
    return groups

@app.on_event("startup")
async def startup_event():
    """서버 시작 시 DB 연결 및 벡터화 모델 로드"""
    global db, vectorizer
    
    try:
        # DB 연결
        db_name = os.getenv('DB_NAME', 'recipe_ai_db')
        db_user = os.getenv('DB_USER', 'recipe_keep')
        db = RecipeDB(db_name, db_user)
        db.connect()
        
        # 벡터화 모델 로드
        use_openai = os.getenv('USE_OPENAI_EMBEDDINGS', 'true').lower() == 'true'
        vectorizer = RecipeVectorizer(use_openai=use_openai)
        
        logger.info("✅ 서버 시작 완료")
        
    except Exception as e:
        logger.error(f"❌ 서버 시작 실패: {e}")
        raise

@app.on_event("shutdown")
async def shutdown_event():
    """서버 종료 시 DB 연결 해제"""
    if db:
        db.close()
    logger.info("✅ 서버 종료")

@app.get("/")
async def root():
    """헬스 체크"""
    return {"message": "Recipe AI Chat API", "status": "running"}

@app.get("/health")
async def health_check():
    """상세 헬스 체크"""
    try:
        # DB 연결 확인
        db.cursor.execute("SELECT COUNT(*) FROM recipes")
        recipe_count = db.cursor.fetchone()[0]
        
        return {
            "status": "healthy",
            "database": "connected",
            "total_recipes": recipe_count,
            "vectorizer": "loaded"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")

@app.post("/search", response_model=List[RecipeResponse])
async def search_recipes(
    query: str,
    limit: int = 5,
    min_similarity: float = 0.0
):
    """벡터 검색으로 레시피 찾기"""
    try:
        # 쿼리를 벡터로 변환
        query_vector = vectorizer.vectorize(query)
        
        # 벡터 검색
        db.cursor.execute("""
            SELECT 
                id, 
                title, 
                title_en, 
                description_en,
                cooking_time,
                servings,
                1 - (embedding <=> %s::vector) as similarity
            FROM recipes
            WHERE embedding IS NOT NULL
              AND 1 - (embedding <=> %s::vector) >= %s
            ORDER BY embedding <=> %s::vector
            LIMIT %s
        """, (query_vector, query_vector, min_similarity, query_vector, limit))
        
        results = db.cursor.fetchall()
        
        return [
            RecipeResponse(
                id=row[0],
                title=row[1],
                title_en=row[2],
                description_en=row[3],
                cooking_time=str(row[4]) if row[4] else "미정",
                servings=str(row[5]) if row[5] else "미정",
                similarity=row[6]
            )
            for row in results
        ]
        
    except Exception as e:
        logger.error(f"검색 실패: {e}")
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

@app.get("/recipe/{recipe_id}", response_model=RecipeDetail)
async def get_recipe_detail(recipe_id: int):
    """레시피 상세 정보 조회 (한국어로 번역)"""
    try:
        from openai import OpenAI
        openai_client = OpenAI()
        
        # 레시피 기본 정보
        db.cursor.execute("""
            SELECT id, title, title_en, description_en, cooking_time, servings
            FROM recipes WHERE id = %s
        """, (recipe_id,))
        
        recipe = db.cursor.fetchone()
        if not recipe:
            raise HTTPException(status_code=404, detail="Recipe not found")
        
        # 재료 정보
        db.cursor.execute("""
            SELECT name_en FROM ingredients WHERE recipe_id = %s ORDER BY id
        """, (recipe_id,))
        ingredients_en = [row[0] for row in db.cursor.fetchall() if row[0]]
        
        # 조리 단계
        db.cursor.execute("""
            SELECT description_en FROM cooking_steps 
            WHERE recipe_id = %s ORDER BY step_number
        """, (recipe_id,))
        cooking_steps_en = [row[0] for row in db.cursor.fetchall() if row[0]]
        
        # GPT로 한국어 번역 (평문으로 깔끔하게)
        if ingredients_en or cooking_steps_en:
            translate_prompt = f"""
다음 레시피 정보를 한국어로 번역해주세요. 
- 개인적인 표현(~!, ^^, 감탄사 등) 제거
- 평문으로 간결하고 명확하게 번역
- 요리 설명서 스타일로 작성

재료 (영어): {ingredients_en}
조리 단계 (영어): {cooking_steps_en}

응답 형식:
{{
  "ingredients": ["한국어 재료1", "한국어 재료2", ...],
  "cooking_steps": ["한국어 단계1", "한국어 단계2", ...]
}}
"""
            
            try:
                response = openai_client.chat.completions.create(
                    model=os.getenv('OPENAI_MODEL', 'gpt-4o-mini'),
                    messages=[
                        {"role": "system", "content": "당신은 요리 번역 전문가입니다. 정확하고 자연스러운 한국어로 번역해주세요."},
                        {"role": "user", "content": translate_prompt}
                    ],
                    max_tokens=1000,
                    temperature=0.3
                )
                
                import json
                translated = json.loads(response.choices[0].message.content)
                ingredients = translated.get("ingredients", ingredients_en)
                cooking_steps = translated.get("cooking_steps", cooking_steps_en)
            except:
                # 번역 실패 시 원본 사용
                ingredients = ingredients_en
                cooking_steps = cooking_steps_en
        else:
            ingredients = ingredients_en
            cooking_steps = cooking_steps_en
        
        # 채팅식 레시피 설명 생성
        # 한국어 제목/시간/인분 정규화
        title_kr = recipe[1]
        title_en = recipe[2]
        # 한국어 제목이 없으면 즉시 번역 사용
        if not title_kr and title_en:
            title_kr = translate_to_korean(openai_client, title_en)
        title_display = title_kr or title_en
        time_kr = format_duration_korean(recipe[4])
        servings_kr = format_servings_korean(recipe[5])

        # 재료 분류 및 단계 그룹화
        ing_split = split_ingredients_kor(ingredients)
        step_groups = group_steps_kor(cooking_steps)

        # 마크다운 구성
        md_lines = []
        md_lines.append(f"🍳 **{title_display}** 레시피를 알려드릴게요!")
        md_lines.append("")
        md_lines.append(f"⏰ **조리시간**: {time_kr}")
        md_lines.append(f"👥 **인분**: {servings_kr}")
        md_lines.append("")
        md_lines.append("🥘 **재료**")
        if ing_split['main']:
            md_lines.append("- **주재료**:")
            md_lines += [f"  - {x}" for x in ing_split['main']]
        if ing_split['sub']:
            md_lines.append("- **부재료**:")
            md_lines += [f"  - {x}" for x in ing_split['sub']]
        if ing_split['seasoning']:
            md_lines.append("- **양념**:")
            md_lines += [f"  - {x}" for x in ing_split['seasoning']]
        if not any(ing_split.values()):
            md_lines.append("- 재료 정보 없음")
        md_lines.append("")
        md_lines.append("👨‍🍳 **조리 단계**")
        if step_groups:
            for group_title, steps_list in step_groups:
                md_lines.append(f"- **{group_title}**")
                for idx, st in enumerate(steps_list, 1):
                    md_lines.append(f"  {idx}. {st}")
        else:
            if cooking_steps:
                for idx, st in enumerate(cooking_steps, 1):
                    md_lines.append(f"{idx}. {st}")
            else:
                md_lines.append("- 조리 방법 정보 없음")
        md_lines.append("")
        md_lines.append("맛있게 만들어보세요! 😊")

        chat_style_recipe = "\n".join(md_lines)

        return RecipeDetail(
            id=recipe[0],
            title=recipe[1],
            title_en=recipe[2],
            description_en=chat_style_recipe,  # 채팅식 설명으로 변경
            cooking_time=str(recipe[4]) if recipe[4] else "미정",
            servings=str(recipe[5]) if recipe[5] else "미정",
            ingredients=ingredients,
            cooking_steps=cooking_steps
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"레시피 조회 실패: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get recipe: {str(e)}")

@app.post("/chat", response_model=ChatResponse)
async def chat_with_ai(chat_message: ChatMessage):
    """AI 채팅 - 레시피 추천"""
    try:
        from openai import OpenAI
        
        # OpenAI 클라이언트 초기화
        openai_client = OpenAI()
        
        # 1. 사용자 메시지를 명확한 검색 쿼리로 변환
        # "소고기 레시피" → "beef recipe"로 강화
        user_query = chat_message.message
        
        # 한국어 재료명을 영어로 키워드 확장
        ingredient_keywords = {
            '소고기': 'beef beef meat beef recipe',
            '돼지고기': 'pork pork meat pork recipe',
            '닭고기': 'chicken chicken meat chicken recipe',
            '생선': 'fish seafood fish recipe',
            '새우': 'shrimp seafood shrimp recipe',
            '연어': 'salmon fish seafood salmon recipe',
            '오징어': 'squid seafood squid recipe',
            '두부': 'tofu tofu recipe',
            '버섯': 'mushroom mushroom recipe',
            '파스타': 'pasta pasta recipe',
            '볶음밥': 'fried rice fried rice recipe',
            '떡볶이': 'rice cake rice cake recipe',
            '볶음': 'stir-fry stir fry recipe',
            '구이': 'grilled grill recipe',
            '조림': 'braised braised recipe',
            '찜': 'steamed steam recipe',
            '국': 'soup soup recipe',
            '찌개': 'stew stew recipe',
            '전': 'pancake pancake recipe',
            '무침': 'salad salad recipe'
        }
        
        # 한국어 키워드 추가
        enhanced_query = user_query
        for korean, english in ingredient_keywords.items():
            if korean in user_query:
                enhanced_query += f" {english}"
        
        # 취향 정보 추가
        pref_text = (
            f"Preferences: spiciness={chat_message.spiciness}, "
            f"saltiness={chat_message.saltiness}."
        )
        augmented_query = f"{enhanced_query}\n{pref_text}"
        query_vector = vectorizer.vectorize(augmented_query)
        
        db.cursor.execute("""
            SELECT 
                id, title, title_en, description_en, cooking_time, servings,
                1 - (embedding <=> %s::vector) as similarity
            FROM recipes
            WHERE embedding IS NOT NULL
              AND 1 - (embedding <=> %s::vector) >= 0.0
            ORDER BY embedding <=> %s::vector
            LIMIT 10
        """, (query_vector, query_vector, query_vector))
        
        search_results = db.cursor.fetchall()
        
        if not search_results:
            return ChatResponse(
                message="죄송해요, 관련 레시피를 찾을 수 없어요. 다른 재료나 요리법으로 다시 말씀해 주세요!",
                recipes=[],
                suggestions=["닭고기 요리", "간단한 파스타", "한국 전통 요리", "건강한 샐러드"]
            )
        
        # 2. 유사도가 높은 레시피만 필터링 (0.1 이상)
        filtered_results = [row for row in search_results if row[6] >= 0.1]
        
        # 3. 레시피 정보를 GPT에게 전달하여 추천 메시지 생성
        recipes_info = []
        for row in filtered_results[:5]:  # 최대 5개만
            # 제목 한국어 보정: 없으면 OpenAI로 즉시 번역
            title_kr = row[1] or ""
            title_en = row[2] or ""
            if not title_kr and title_en:
                title_kr = translate_to_korean(openai_client, title_en)
            recipes_info.append({
                "id": row[0],
                "title": title_kr or title_en,
                "title_en": title_en,
                "description": row[3] or "",
                "cooking_time": str(row[4]) if row[4] else "미정",
                "servings": str(row[5]) if row[5] else "미정",
                "similarity": row[6]
            })
        
        # 필터링 후 레시피가 없으면
        if not recipes_info:
            return ChatResponse(
                message="죄송해요, 관련 레시피를 찾을 수 없어요. 다른 재료나 요리법으로 다시 말씀해 주세요!",
                recipes=[],
                suggestions=["닭고기 요리", "간단한 파스타", "한국 전통 요리", "건강한 샐러드"]
            )
        
        # GPT 프롬프트
        system_prompt = (
            "당신은 친근한 한국어 레시피 챗봇입니다."
            " 항상 한국어로만 답변하세요."
            " 답변은 마크다운으로 구성하고, 섹션 제목(아이콘 포함), 목록, 단계 나열을 사용하세요."
            " 사용자의 취향(맵기/짜기)을 반영하여 우선순위를 조정하세요."
        )

        convo = chat_histories.get(chat_message.user_id or "default", [])

        instruction = (
            "다음은 사용자 대화 일부와 데이터베이스에서 찾은 관련 레시피입니다."
            " 사용자의 요청과 취향을 반영해 1~3개의 레시피를 추천하고,"
            " 각 레시피의 조리시간/인분/간단한 특징을 1-2문장으로 요약하세요."
            " 마지막 줄에는 '원하시면 1번/2번/3번 중에 선택해 주세요.'라고 안내하세요.\n\n"
            f"사용자 취향: 맵기={chat_message.spiciness}, 짠맛={chat_message.saltiness}\n"
            f"대화 일부: {json.dumps(convo[-6:], ensure_ascii=False)}\n"
            f"레시피 정보: {json.dumps(recipes_info, ensure_ascii=False)}\n"
            f"사용자 요청: {chat_message.message}"
        )
        
        # GPT 호출
        response = openai_client.chat.completions.create(
            model=os.getenv('OPENAI_MODEL', 'gpt-4o-mini'),
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": instruction}
            ],
            max_tokens=500,
            temperature=0.6
        )

        ai_message = response.choices[0].message.content

        # 대화 내역 업데이트 (간단한 저장)
        chat_histories.setdefault(chat_message.user_id or "default", []).extend([
            {"role": "user", "content": chat_message.message},
            {"role": "assistant", "content": ai_message or ""}
        ])
        # 메모리 폭주 방지: 최근 20개만 유지
        chat_histories[chat_message.user_id or "default"] = chat_histories[chat_message.user_id or "default"][-20:]
        
        # 3. 응답 구성
        recipe_responses = [
            RecipeResponse(
                id=recipe["id"],
                title=recipe["title"],
                title_en=recipe.get("title_en", recipe["title"]),
                description_en=recipe["description"],
                cooking_time=recipe["cooking_time"],
                servings=recipe["servings"],
                similarity=recipe["similarity"]
            )
            for recipe in recipes_info[:3]  # 상위 3개만 반환
        ]
        # 한국어 표기 보정
        for r in recipe_responses:
            r.cooking_time = format_duration_korean(r.cooking_time)
            r.servings = format_servings_korean(r.servings)
        
        # 추천 키워드 생성
        suggestions = [
            "더 많은 닭고기 요리",
            "간단한 요리",
            "건강한 요리",
            "한국 전통 요리"
        ]
        
        md_header = """🍽️ 추천 레시피\n\n**아래에서 원하는 레시피를 선택해 주세요. (1~3번)**\n\n"""

        return ChatResponse(
            message=ai_message,
            markdown_message=md_header + (ai_message or ""),
            recipes=recipe_responses,
            suggestions=suggestions
        )
        
    except Exception as e:
        logger.error(f"채팅 처리 실패: {e}")
        raise HTTPException(status_code=500, detail=f"Chat failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
