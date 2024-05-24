#!/bin/bash

# Load environment variables from config.yaml
export $(grep -v '^#' config.yaml | xargs)

# Start the FastAPI server
uvicorn app.app:app --host 0.0.0.0 --port 80
