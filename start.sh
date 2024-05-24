#!/bin/sh

# Start the server
uvicorn app:app --host 0.0.0.0 --port $PORT
