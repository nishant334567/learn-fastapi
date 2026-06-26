# LangChain

## What is LangChain?
A wrapper/abstraction over LLMs, vector stores, and embeddings. Standardizes interfaces so swapping providers is one line change.

## Why use it?
- Swap models (Ollama → OpenAI → Gemini) with one line
- No manual HTTP calls or JSON parsing
- Readable pipelines using `|` operator

---

## Core Concepts

### LCEL — the pipe operator
```python
chain = prompt | model | parser
chain.invoke({"context": context, "question": question})
```
Each step's output feeds into the next. Same idea as Unix pipes.

### ChatPromptTemplate
Replaces f-strings. Separates system and human messages cleanly.
```python
prompt = ChatPromptTemplate.from_messages([
    ("system", "Answer based on context: {context}"),
    ("human", "{question}")
])
```

### ChatOllama
LangChain wrapper around Ollama — replaces `requests.post`.
```python
model = ChatOllama(model="gemma4")
```

### StrOutputParser
Extracts clean string from LLM response — replaces `response.json()["message"]["content"]`.
```python
parser = StrOutputParser()
```

### OllamaEmbeddings
Replaces manual embedding HTTP call.
```python
embedder = OllamaEmbeddings(model="nomic-embed-text")
embedder.embed_query(text)
```

### PGVector
LangChain's vector store for PostgreSQL. Handles embed + insert + similarity search.
```python
vectorstore = PGVector(
    connection=DATABASE_URL,
    embeddings=OllamaEmbeddings(model="nomic-embed-text"),
    collection_name="knowledge_chunks"
)

# save chunks (embeds automatically)
vectorstore.add_texts(chunks, metadatas=[{"doc_id": id}] * len(chunks))

# search (embeds query + SQL search automatically)
docs = vectorstore.similarity_search(question, k=5)
chunks = [doc.page_content for doc in docs]
```

---

## Before vs After

| Before | After |
|---|---|
| `requests.post` to Ollama | `ChatOllama` |
| f-string prompt | `ChatPromptTemplate` |
| `response.json()["message"]["content"]` | `StrOutputParser` |
| manual embed + raw SQL insert | `vectorstore.add_texts()` |
| manual embed + raw SQL search | `vectorstore.similarity_search()` |

---

## Paid API Keys
```python
# pass directly
model = ChatOpenAI(model="gpt-4o", api_key="sk-...")

# or via env (recommended)
export OPENAI_API_KEY="sk-..."
model = ChatOpenAI(model="gpt-4o")  # picks up automatically
```
Never hardcode keys — use `.env` + `.gitignore`.

---

## Project Structure After Migration

```
core/llm.py          → prompt | ChatOllama | StrOutputParser
core/embed.py        → OllamaEmbeddings.embed_query()
core/vectorstore.py  → shared PGVector instance
routers/kb.py        → vectorstore.add_texts()
routers/query.py     → vectorstore.similarity_search() + get_llm_answer()
main.py              → lifespan triggers vectorstore init on startup
```

---

## FastAPI Lifespan
Run code once on server start (like `useEffect(()=>{}, [])` in React).
```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    _ = vectorstore  # triggers PGVector table creation
    yield            # server runs here

app = FastAPI(lifespan=lifespan)
```
Before yield = startup. After yield = shutdown.

---

## Install
```bash
pip install langchain langchain-ollama langchain-postgres
```
