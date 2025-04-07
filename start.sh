#!/bin/bash

# Start backend in background
uvicorn backend.app:app --host 0.0.0.0 --port 8000 &

# Start frontend on Render's main port (10000)
streamlit run frontend/app.py --server.port 10000 --server.address 0.0.0.0
