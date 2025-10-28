-- Initialize new database
CREATE DATABASE recipe_ai_db;

-- Create user
CREATE USER recipe_keep WITH PASSWORD 'wkwjsrj4510*' CREATEDB;
GRANT ALL PRIVILEGES ON DATABASE recipe_ai_db TO recipe_keep;

\c recipe_ai_db

GRANT ALL ON SCHEMA public TO recipe_keep;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO recipe_keep;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO recipe_keep;

SELECT '✅ Database recipe_ai_db created!' as status;
SELECT '   Username: recipe_keep' as info;
SELECT '   Password: wkwjsrj4510*' as info;

