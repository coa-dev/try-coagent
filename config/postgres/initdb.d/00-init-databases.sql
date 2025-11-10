-- Initialize databases
-- This script runs first to ensure both databases exist

-- Create the coagent database (this might already exist from POSTGRES_DB env var)
SELECT 'CREATE DATABASE coagent'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'coagent')\gexec

-- Create the coagent-cloud database
SELECT 'CREATE DATABASE "coagent-cloud"'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'coagent-cloud')\gexec

-- Grant permissions to coagent user on both databases
GRANT ALL PRIVILEGES ON DATABASE coagent TO coagent;
GRANT ALL PRIVILEGES ON DATABASE "coagent-cloud" TO coagent;

\echo 'Successfully ensured both coagent and coagent-cloud databases exist'
