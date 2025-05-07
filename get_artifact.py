#!/usr/bin/env python3
"""
CLI script to retrieve a Knowledge Artifact by knowledge_id from the artifact-db PostgreSQL database.

Usage:
  get_artifact.py KNOWLEDGE_ID

Dependencies:
  - psycopg2
  - python-dotenv
"""
import os
import sys
import json
import argparse

import psycopg2
from dotenv import load_dotenv


def main():
    load_dotenv()
    parser = argparse.ArgumentParser(
        description="Retrieve an artifact by knowledge_id"
    )
    parser.add_argument(
        'knowledge_id', help='Knowledge ID of the artifact to retrieve'
    )
    args = parser.parse_args()
    knowledge_id = args.knowledge_id

    # Database connection parameters from environment
    db_params = {
        'host': os.getenv('POSTGRES_HOST', 'localhost'),
        'port': os.getenv('POSTGRES_PORT', '5432'),
        'dbname': os.getenv('POSTGRES_DB'),
        'user': os.getenv('POSTGRES_USER'),
        'password': os.getenv('POSTGRES_PASSWORD'),
    }
    # Check for missing required parameters
    missing = [k for k, v in db_params.items() if v is None]
    if missing:
        print(f"Missing environment variables: {', '.join(missing)}", file=sys.stderr)
        sys.exit(1)

    # Connect to PostgreSQL
    try:
        conn = psycopg2.connect(**db_params)
    except Exception as e:
        print(f"Error connecting to database: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT artifact FROM artifacts WHERE knowledge_id = %s",
                (knowledge_id,)
            )
            rows = cur.fetchall()
    except Exception as e:
        print(f"Error querying artifact: {e}", file=sys.stderr)
        conn.close()
        sys.exit(1)
    finally:
        conn.close()

    # Handle results
    if not rows:
        print(f"No artifact found with knowledge_id '{knowledge_id}'")
        sys.exit(1)
    if len(rows) > 1:
        print(f"Warning: multiple ({len(rows)}) artifacts found for knowledge_id '{knowledge_id}'", file=sys.stderr)

    # Print each artifact as pretty JSON
    for row in rows:
        artifact = row[0]
        try:
            output = json.dumps(artifact, indent=2)
        except (TypeError, ValueError):
            # Fallback if artifact is returned as string
            output = json.dumps(json.loads(artifact), indent=2)
        print(output)


if __name__ == '__main__':  # pragma: no cover
    main()