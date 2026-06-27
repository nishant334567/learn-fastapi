from fastapi import APIRouter
from pydantic import BaseModel
from core.llm import get_llm_answer, chain
from core.vectorstore import vectorstore
from fastapi.responses import StreamingResponse

router = APIRouter()

class Query(BaseModel):
    user_question: str

@router.post("/query")
def answer_query(query: Query):
    docs = vectorstore.similarity_search(query.user_question, k=5)
    relavant_chunks = [doc.page_content for doc in docs]
    answer = get_llm_answer(query.user_question, relavant_chunks)
    return {"llm_answer": answer}

@router.post("/query/stream")
def stream_answer_query(query: Query):
    docs = vectorstore.similarity_search(query.user_question, k=5)
    relavant_chunks = [doc.page_content for doc in docs]
    return StreamingResponse(chain.stream({"context": "\n\n".join(relavant_chunks), "question": query.user_question}), media_type="text/plain")
    