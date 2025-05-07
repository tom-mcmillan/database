#!/usr/bin/env python3
"""
CLI script to insert a Knowledge Artifact JSON into the artifact-db PostgreSQL database.

Usage:
  insert_artifact.py path/to/artifact.json

Dependencies:
  - psycopg2
  - python-dotenv
"""
import os
import sys
import json
import argparse

import psycopg2
from psycopg2.extras import Json

from dotenv import load_dotenv


def validate_structure(artifact):
    """
    Validate that the artifact JSON contains required fields and sub-fields.
    Raises ValueError if validation fails.
    """
    required_fields = ['id', 'created_at', 'content', 'epistemic_trace']
    for field in required_fields:
        if field not in artifact:
            raise ValueError(f"Missing required field: '{field}'")

    epistemic = artifact.get('epistemic_trace')
    if not isinstance(epistemic, dict):
        raise ValueError("Field 'epistemic_trace' must be an object")
    sub_fields = ['justification', 'diagnostic_flags', 'detected_by']
    for sub in sub_fields:
        if sub not in epistemic:
            raise ValueError(f"Missing required epistemic_trace field: '{sub}'")
    if not isinstance(epistemic.get('diagnostic_flags'), list):
        raise ValueError("Field 'diagnostic_flags' in 'epistemic_trace' must be a list")


def main():
    load_dotenv()
    parser = argparse.ArgumentParser(
        description="Insert an artifact JSON into the artifact-db database"
    )
    parser.add_argument(
        'json_file', help='Path to the artifact JSON file'
    )
    args = parser.parse_args()

    # Load JSON
    try:
        with open(args.json_file, 'r', encoding='utf-8') as f:
            artifact = json.load(f)
    except Exception as e:
        print(f"Error reading JSON file: {e}", file=sys.stderr)
        sys.exit(1)

    # Validate structure
    try:
        validate_structure(artifact)
    except ValueError as e:
        print(f"Validation error: {e}", file=sys.stderr)
        sys.exit(1)

    # Database connection parameters
    db_params = {
        'host': os.getenv('POSTGRES_HOST', 'localhost'),
        'port': os.getenv('POSTGRES_PORT', '5432'),
        'dbname': os.getenv('POSTGRES_DB'),
        'user': os.getenv('POSTGRES_USER'),
        'password': os.getenv('POSTGRES_PASSWORD'),
    }
    missing = [k for k, v in db_params.items() if v is None]
    if missing:
        print(f"Missing environment variables: {', '.join(missing)}", file=sys.stderr)
        sys.exit(1)

    # Connect to the database
    try:
        conn = psycopg2.connect(**db_params)
        conn.autocommit = True
    except Exception as e:
        print(f"Error connecting to database: {e}", file=sys.stderr)
        sys.exit(1)

    # Insert the artifact
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO artifacts (knowledge_id, artifact, created_at)
                VALUES (%s, %s, %s)
                """,
                (artifact['id'], Json(artifact), artifact['created_at'])
            )
        print(f"Artifact '{artifact['id']}' inserted successfully.")
    except Exception as e:
        print(f"Error inserting artifact: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        conn.close()


if __name__ == '__main__':  # pragma: no cover
    main()