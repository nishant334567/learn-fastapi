# Streaming

## What is it?
Instead of waiting for the full LLM response, tokens are sent to the client as they are generated — word by word.

## Who does what?
- **Ollama/LLM** — generates tokens one by one (source of streaming)
- **LangChain** — `chain.stream()` receives tokens as they arrive
- **FastAPI** — `StreamingResponse` forwards them to the client immediately

```
Ollama generates token → LangChain receives it → FastAPI sends it → client prints it
```

## Code

```python
from fastapi.responses import StreamingResponse
from core.llm import chain

@router.post("/query/stream")
def stream_answer_query(query: Query):
    docs = vectorstore.similarity_search(query.user_question, k=5)
    chunks = [doc.page_content for doc in docs]
    return StreamingResponse(
        chain.stream({"context": "\n\n".join(chunks), "question": query.user_question}),
        media_type="text/plain"
    )
```

## Key differences from normal query

| Normal `/query` | Streaming `/query/stream` |
|---|---|
| `chain.invoke()` | `chain.stream()` |
| `return {"llm_answer": answer}` | `return StreamingResponse(...)` |
| waits for full response | sends token by token |

## media_type
Not strictly required but important for clients:
- Without it → defaults to `application/octet-stream` (raw binary)
- With `text/plain` → client knows it's readable text arriving in chunks
- Matters for browsers/frontends, not for curl

## Test with curl
```bash
curl -s -X POST http://localhost:8000/query/stream \
  -H "Content-Type: application/json" \
  -d '{"user_question": "what is GPT-5?"}' \
  --no-buffer
```
`--no-buffer` prints each token as it arrives instead of waiting for the full response.
