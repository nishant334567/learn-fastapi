from fastapi import APIRouter, Depends
from pydantic import BaseModel
from core.llm import get_llm_answer
from core.vectorstore import vectorstore

router = APIRouter()

class Query(BaseModel):
    user_question: str

@router.post("/query")
def answer_query(query: Query):
    docs = vectorstore.similarity_search(query.user_question,k=5)
    relavant_chunks = [doc.page_content for doc in docs]
    answer = get_llm_answer(query.user_question, relavant_chunks)
    return {"llm_answer": answer}
    