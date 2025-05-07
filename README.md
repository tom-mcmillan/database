# artifact-db

This project provides a minimal PostgreSQL setup for storing immutable Knowledge Artifacts
as defined by the Conduct system. The database contains a single table, `artifacts`,
which stores atomic JSON objects with traceability and validation constraints.

## Features
- Immutable, insert-only storage of artifacts
- JSONB column with constraints enforcing required fields
- Unique `knowledge_id` matching the artifact's internal `id`
- Timestamp enforcement for `created_at`

## Getting Started

### Prerequisites

- Docker & Docker Compose

### Setup

1. Copy the example environment file and customize if needed:
   cp .env.example .env

2. Bring up the PostgreSQL service:
   docker-compose up -d

3. Connect to the database to verify schema:
   psql -h localhost -p ${POSTGRES_PORT} -U ${POSTGRES_USER} -d ${POSTGRES_DB}

### Schema Overview

The `artifacts` table schema:

| Column        | Type          | Description                                                 |
|---------------|---------------|-------------------------------------------------------------|
| id            | SERIAL        | Internal primary key                                        |
| knowledge_id  | TEXT UNIQUE   | Globally unique identifier, matches `artifact.id`           |
| artifact      | JSONB         | Full artifact object with required fields                   |
| created_at    | TIMESTAMPTZ   | Timestamp matching `artifact.created_at`                    |

Constraints:

- `chk_artifact_has_required_fields`: top-level JSON keys presence
- `chk_epistemic_trace_fields`: required sub-fields in `epistemic_trace`
- `chk_knowledge_id_matches`: `knowledge_id` equals `artifact.id`
- `chk_created_at_matches`: `created_at` equals parsed JSON timestamp

## Future Extensions

- JSONPath or GIN indexing on `artifact` for search
- Audit logs or soft-deletes
- Integration with exchange protocols

---

Generated as a minimal scaffold for the Conduct Knowledge Artifacts database.