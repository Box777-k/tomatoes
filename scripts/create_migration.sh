#!/bin/bash

# Script to create a new Alembic migration

if [ -z "$1" ]; then
    echo "Usage: ./scripts/create_migration.sh \"migration description\""
    exit 1
fi

cd "$(dirname "$0")/.."
uv run alembic revision --autogenerate -m "$1"

