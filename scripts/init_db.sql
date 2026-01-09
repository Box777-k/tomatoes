-- Initial database setup for Tomatoes ERP

-- Create database
CREATE DATABASE tomatoes_db;

-- Create user
CREATE USER tomatoes_user WITH PASSWORD 'tomatoes_pass';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE tomatoes_db TO tomatoes_user;

-- Connect to database and grant schema privileges
\c tomatoes_db
GRANT ALL ON SCHEMA public TO tomatoes_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO tomatoes_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO tomatoes_user;

