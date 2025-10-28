-- Recipe AI System - Simple Schema (레시피 전용)

CREATE TYPE difficulty_level AS ENUM ('easy', 'medium', 'hard');

-- 레시피 메인 테이블
CREATE TABLE recipes (
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
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 재료 테이블
CREATE TABLE ingredients (
    id SERIAL PRIMARY KEY,
    recipe_id INTEGER REFERENCES recipes(id) ON DELETE CASCADE,
    name VARCHAR(200) NOT NULL,
    name_en VARCHAR(200),
    amount VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 조리 단계 테이블
CREATE TABLE cooking_steps (
    id SERIAL PRIMARY KEY,
    recipe_id INTEGER REFERENCES recipes(id) ON DELETE CASCADE,
    step_number INTEGER NOT NULL,
    description TEXT NOT NULL,
    description_en TEXT,
    image_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 인덱스
CREATE INDEX idx_recipes_title ON recipes(title);
CREATE INDEX idx_recipes_title_en ON recipes(title_en);
CREATE INDEX idx_ingredients_recipe_id ON ingredients(recipe_id);
CREATE INDEX idx_cooking_steps_recipe_id ON cooking_steps(recipe_id);

SELECT '✅ Schema created successfully!' as status;

