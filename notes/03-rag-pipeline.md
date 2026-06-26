# RAG Pipeline in FastAPI

## What is RAG?
Retrieval Augmented Generation — instead of asking an LLM from memory, you:
1. Store your own documents with embeddings
2. At query time, find relevant chunks
3. Send those chunks as context to the LLM

## Full Pipeline

### Training (POST /knowledge-base)
```
text → save to documents table → chunk → embed each chunk → save to knowledge_chunks
```

### Query (POST /query)
```
question → embed → find similar chunks in DB → send chunks + question to LLM → return answer
```

---

## Chunking (core/chunker.py)
Split long text into smaller pieces so embedding models can handle them.

```python
def chunk_text(text, chunk_size=500, overlap=50):
```
- `chunk_size` — characters per chunk
- `overlap` — shared characters between chunks (so sentences don't get cut off)

---

## Embeddings (core/embed.py)
Convert text to a list of 768 numbers (vector) via Ollama.

```python
response = requests.post('http://localhost:11434/api/embeddings',
    json={"model": "nomic-embed-text", "prompt": text})
return response.json()["embedding"]
```

---

## Vector Search (pgvector)
`<->` operator finds the closest vectors in the DB.

```sql
SELECT chunk_content FROM knowledge_chunks
ORDER BY embed <-> %s LIMIT 5
```

Pass embedding as a string tuple: `(str(query_embedding),)`

---

## LLM Call (core/llm.py)
Build a prompt with context and send to Gemma via Ollama.

```python
response = requests.post('http://localhost:11434/api/chat',
    json={
        "model": "gemma4",
        "messages": [{"role": "user", "content": prompt}],
        "stream": False
    })
return response.json()["message"]["content"]
```

`stream: False` — get the full response at once instead of word by word.

---

## Prompt Structure
```
System: Answer only based on the context below.

Context:
<chunk 1>
<chunk 2>

User: <question>
```

---

## Key Files
```
routers/knowledge_base.py  — training endpoint
routers/query.py           — query endpoint
core/chunker.py            — splits text into chunks
core/embed.py              — calls Ollama embeddings
core/llm.py                — builds prompt, calls Gemma
core/db.py                 — connection pool
```
