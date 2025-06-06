#!/bin/bash

cd "$(dirname "$0")"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
  echo "Creating virtual environment..."
  python3 -m venv venv
fi

# Debian/Ubuntu (for your current setup):
sudo apt update && sudo apt install -y \
    portaudio19-dev \
    ffmpeg \
    build-essential \
    libsndfile1

# Activate it
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
pip install --upgrade pymongo

# Start backend with PM2
pm2 start ./venv/bin/uvicorn \
  --name backendA \
  --interpreter ./venv/bin/python \
  -- \
  main:app --host 0.0.0.0 --port 8000
