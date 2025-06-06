#!/bin/bash

cd "$(dirname "$0")"

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start backend with PM2 using interpreter and args
pm2 start ./venv/bin/uvicorn \
  --name API \
  --interpreter ./venv/bin/python \
  -- \
  main:app --host 0.0.0.0 --port 8000
