# Uptime Monitor - Sprint 1

## Run locally
python -m venv .venv
# activate venv
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

## Endpoints
GET /health
