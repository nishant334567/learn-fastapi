from fastapi import APIRouter
from pydantic import BaseModel
from core.vectorstore import vectorstore
from fastapi.responses import StreamingResponse
from core.graph import app as graph

router = APIRouter()

class Query(BaseModel):
    user_question: str

@router.post("/query")
def answer_query(query: Query):
    result = graph.invoke({"question": query.user_question, "chunks": [], "answer": ""})
    return {"llm_answer": result["answer"]}

@router.post("/query/stream")
def stream_answer_query(query: Query):
    docs = vectorstore.similarity_search(query.user_question, k=5)
    relavant_chunks = [doc.page_content for doc in docs]
    return StreamingResponse(chain.stream({"context": "\n\n".join(relavant_chunks), "question": query.user_question}), media_type="text/plain")
    