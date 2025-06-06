#!/bin/bash

cd "$(dirname "$0")"  # Enter the script directory

# Create venv if not present
if [ ! -d "venv" ]; then
    echo "🟡 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies from requirements.txt
echo "📦 Installing dependencies from requirements.txt..."
pip install --upgrade pip
pip install -r requirements.txt

# Start backend using pm2 with corrected module path
echo "🚀 Launching FastAPI backend with pm2..."
pm2 start "bash -c 'cd $(pwd) && source venv/bin/activate && uvicorn backend.main:app --host 0.0.0.0 --port 8000'" --name backend
