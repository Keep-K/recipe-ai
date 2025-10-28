-- pgvector 확장 설치 및 벡터 컬럼 추가

-- 1. pgvector 확장 활성화
CREATE EXTENSION IF NOT EXISTS vector;

-- 2. recipes 테이블에 벡터 컬럼 추가
ALTER TABLE recipes ADD COLUMN IF NOT EXISTS embedding vector(1536);

-- 3. 벡터 검색을 위한 인덱스 생성
-- IVFFlat 인덱스 (빠른 근사 검색)
CREATE INDEX IF NOT EXISTS recipes_embedding_idx 
ON recipes USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

-- 4. 확인
SELECT 
    column_name, 
    data_type 
FROM information_schema.columns 
WHERE table_name = 'recipes' AND column_name = 'embedding';

-- 5. 통계
SELECT 
    COUNT(*) as total_recipes,
    COUNT(embedding) as vectorized_recipes,
    COUNT(*) - COUNT(embedding) as missing_vectors
FROM recipes;

