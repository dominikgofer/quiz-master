#!/bin/bash

# Django Development Server Runner
# This script applies migrations and runs the Django development server
# Usage: ./run_django.sh [IP] [PORT]
# Example: ./run_django.sh 0.0.0.0 8080

# Get the directory where the script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# Change to project directory
cd "$PROJECT_DIR"

# Get IP and PORT from command line arguments (defaults: 127.0.0.1:8000)
IP="${1:-127.0.0.1}"
PORT="${2:-8000}"

# Apply database migrations
echo "Applying database migrations..."
uv run manage.py migrate

# Run Django development server using uv
echo "Starting Django development server at $IP:$PORT..."
uv run manage.py runserver "$IP:$PORT"
