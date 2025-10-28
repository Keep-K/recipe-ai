-- Migration: Add vector embedding column for semantic search
-- Created: 2025-10-20

-- Step 1: pgvector 확장 활성화
CREATE EXTENSION IF NOT EXISTS vector;

-- Step 2: recipes 테이블에 벡터 컬럼 추가
-- OpenAI text-embedding-3-small 모델 사용 시: 1536 차원
ALTER TABLE recipes 
ADD COLUMN IF NOT EXISTS embedding vector(1536);

-- Step 3: 벡터 검색을 위한 인덱스 생성
-- IVFFlat: 빠른 근사 검색 (Inverted File with Flat compression)
-- vector_cosine_ops: 코사인 유사도 기반 검색
CREATE INDEX IF NOT EXISTS idx_recipes_embedding 
ON recipes 
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

-- Step 4: 기존 레시피 수 확인
DO $$
DECLARE
    recipe_count INTEGER;
BEGIN
    SELECT COUNT(*) INTO recipe_count FROM recipes;
    RAISE NOTICE '============================================================';
    RAISE NOTICE '✅ 벡터 컬럼 추가 완료!';
    RAISE NOTICE '============================================================';
    RAISE NOTICE '📊 현재 레시피 수: %', recipe_count;
    RAISE NOTICE '📌 다음 단계: 벡터화 스크립트 실행';
    RAISE NOTICE '   python src/vectorizer.py';
    RAISE NOTICE '============================================================';
END $$;

-- 확인
SELECT 
    column_name, 
    data_type, 
    is_nullable 
FROM information_schema.columns 
WHERE table_name = 'recipes' 
AND column_name = 'embedding';

