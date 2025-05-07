DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'artifact_user') THEN
    CREATE ROLE artifact_user WITH LOGIN PASSWORD 'changeme';
  END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_database WHERE datname = 'artifact_db') THEN
    CREATE DATABASE artifact_db OWNER artifact_user;
  END IF;
END
$$;
