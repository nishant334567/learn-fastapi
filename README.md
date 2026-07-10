# Job Apply LangGraph API

FastAPI + LangGraph pipeline that scores a resume against a job description and drafts a cover letter when the fit is strong enough.

## Flow

```
POST /agent/apply { jd, resume }
  → parse_jd
  → parse_resume
  → score_fit
  → score < 50? → reject
  → else → draft_cover
```

## Project Structure

```
├── main.py
├── core/
│   └── job_graph.py   # LangGraph pipeline
└── routers/
    └── agents.py      # POST /agent/apply
```

## Run Locally

```bash
python3 -m venv venv
source venv/bin/activate
pip install fastapi uvicorn langchain-ollama langchain-core langgraph
# Ollama must be running with gemma4 pulled
uvicorn main:app --reload
```

Server: `http://127.0.0.1:8000`  
Docs: `http://127.0.0.1:8000/docs`

## Test

```bash
curl -X POST http://127.0.0.1:8000/agent/apply \
  -H "Content-Type: application/json" \
  -d '{"jd":"Python, FastAPI required","resume":"Python dev, 2 years FastAPI"}'
```
