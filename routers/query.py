from fastapi import APIRouter, Depends
from pydantic import BaseModel
from core.embed import text_embedding
from core.llm import get_llm_answer
from core.db import get_db

router = APIRouter()

class Query(BaseModel):
    user_question: str

@router.post("/query")
def answer_query(query: Query, conn=Depends(get_db)):
    cursor = conn.cursor()
    query_embedding = text_embedding(query.user_question)
    cursor.execute('SELECT chunk_content FROM knowledge_chunks ORDER BY embed <-> %s LIMIT 5',
    (str(query_embedding),))
    rows = cursor.fetchall()
    relavant_chunks = [row[0] for row in rows]
    answer = get_llm_answer(query.user_question, relavant_chunks)
    return {"llm_answer": answer}
    