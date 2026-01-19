#!/bin/bash

# Django Development Server Runner
# This script runs the Django development server

# Get the directory where the script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# Change to project directory
cd "$PROJECT_DIR"

# Run Django development server using uv
echo "Starting Django development server with uv..."
uv run manage.py runserver
