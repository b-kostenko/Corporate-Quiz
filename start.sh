#!/bin/bash

# Exit on any error
set -e

echo "Applying database migrations..."
alembic upgrade head

# Start the FastAPI application
echo "Starting FastAPI server..."
exec uvicorn main:create_app --host 0.0.0.0 --port 8000
