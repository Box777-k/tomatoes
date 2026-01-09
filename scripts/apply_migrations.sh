#!/bin/bash

# Script to apply all Alembic migrations

cd "$(dirname "$0")/.."
uv run alembic upgrade head

