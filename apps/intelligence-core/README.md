# intelligence-core

FastAPI + LangGraph backend for Project Terra.

## Endpoints

- `POST /analyze/{ticker}`: Run the council skeleton for a ticker.
- `GET /health`: Health check.
- `WS /ws/council/{run_id}`: Stream council events.

## Local Run

```bash
uv run uvicorn src.main:app --reload --port 8000
```
