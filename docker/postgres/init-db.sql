-- PostgreSQL 초기화 스크립트
-- Railway에서 자동으로 실행됩니다

-- pgvector 확장 활성화
CREATE EXTENSION IF NOT EXISTS vector;

-- 난이도 ENUM 타입
CREATE TYPE difficulty_level AS ENUM ('easy', 'medium', 'hard');

-- 레시피 메인 테이블 (pgvector 포함)
CREATE TABLE IF NOT EXISTS recipes (
    id SERIAL PRIMARY KEY,
    recipe_id VARCHAR(20) UNIQUE NOT NULL,
    title VARCHAR(300) NOT NULL,
    title_en VARCHAR(300),
    description TEXT,
    description_en TEXT,
    url VARCHAR(500),
    servings VARCHAR(50),
    cooking_time VARCHAR(50),
    difficulty difficulty_level DEFAULT 'medium',
    category VARCHAR(50),
    image_url TEXT,
    embedding VECTOR(1536),  -- OpenAI embedding 차원
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 재료 테이블
CREATE TABLE IF NOT EXISTS ingredients (
    id SERIAL PRIMARY KEY,
    recipe_id INTEGER REFERENCES recipes(id) ON DELETE CASCADE,
    name VARCHAR(200) NOT NULL,
    name_en VARCHAR(200),
    amount VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 조리 단계 테이블
CREATE TABLE IF NOT EXISTS cooking_steps (
    id SERIAL PRIMARY KEY,
    recipe_id INTEGER REFERENCES recipes(id) ON DELETE CASCADE,
    step_number INTEGER NOT NULL,
    description TEXT NOT NULL,
    description_en TEXT,
    image_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 인덱스 생성
CREATE INDEX IF NOT EXISTS idx_recipes_title ON recipes(title);
CREATE INDEX IF NOT EXISTS idx_recipes_title_en ON recipes(title_en);
CREATE INDEX IF NOT EXISTS idx_ingredients_recipe_id ON ingredients(recipe_id);
CREATE INDEX IF NOT EXISTS idx_cooking_steps_recipe_id ON cooking_steps(recipe_id);

-- 벡터 검색 인덱스 (pgvector)
CREATE INDEX IF NOT EXISTS idx_recipes_embedding 
    ON recipes USING ivfflat (embedding vector_l2_ops)
    WITH (lists = 100);

-- 성공 메시지
SELECT '✅ PostgreSQL + pgvector initialized successfully!' as status;


