-- init-db/001_create_artifacts_table.sql
-- This script creates the artifacts table for the artifact database.

CREATE TABLE IF NOT EXISTS artifacts (
    id SERIAL PRIMARY KEY,
    knowledge_id TEXT NOT NULL UNIQUE,
    artifact JSONB NOT NULL,
    created_at TIMESTAMPTZ NOT NULL,
    -- Ensure the artifact JSON contains required top-level fields
    CONSTRAINT chk_artifact_has_required_fields CHECK (
        artifact ? 'id'
        AND artifact ? 'created_at'
        AND artifact ? 'content'
        AND artifact ? 'epistemic_trace'
    ),
    -- Ensure epistemic_trace object has required fields
    CONSTRAINT chk_epistemic_trace_fields CHECK (
        (artifact->'epistemic_trace') ? 'justification'
        AND (artifact->'epistemic_trace') ? 'diagnostic_flags'
        AND (artifact->'epistemic_trace') ? 'detected_by'
    ),
    -- Ensure knowledge_id matches artifact.id
    CONSTRAINT chk_knowledge_id_matches CHECK (
        artifact->>'id' = knowledge_id
    ),
    -- Ensure created_at matches artifact.created_at
    CONSTRAINT chk_created_at_matches CHECK (
        created_at = (artifact->>'created_at')::timestamptz
    )
);