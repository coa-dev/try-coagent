-- Initialize coagent-cloud database with organizations, users, and subscriptions tables
-- This script runs automatically when PostgreSQL container starts
-- Database creation is handled in 00-init-databases.sql

-- Connect to the coagent-cloud database
\c "coagent-cloud";

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Grant permissions (assuming coagent user exists)
GRANT ALL PRIVILEGES ON DATABASE "coagent-cloud" TO coagent;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO coagent;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO coagent;
GRANT USAGE ON SCHEMA public TO coagent;
