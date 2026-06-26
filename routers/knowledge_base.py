from fastapi import APIRouter, Depends
from pydantic import BaseModel
from core.embed import text_embedding
from core.chunker import chunk_text
from core.db import get_db
from core.vectorstore import vectorstore

router = APIRouter()

class TrainingData(BaseModel):
    full_content: str
    title: str

@router.post('/knowledge-base')
def train_data(trainingData: TrainingData, conn=Depends(get_db)):
    cursor = conn.cursor()

    # 1. Save document
    cursor.execute(
        'INSERT INTO documents (full_content, title) VALUES (%s, %s) RETURNING id',
        (trainingData.full_content, trainingData.title)
    )
    doc_id = cursor.fetchone()[0]
    conn.commit()

    # 2. Chunk → embed → save each chunk
    chunks = chunk_text(trainingData.full_content)
    # for chunk in chunks:
    #     embedding = text_embedding(chunk)
    #     cursor.execute(
    #         'INSERT INTO knowledge_chunks (docid, chunk_content, embed) VALUES (%s, %s, %s)',
    #         (doc_id, chunk, embedding)
    #     )
    vectorstore.add_texts(chunks, metadatas=[{"doc_id":doc_id}]*len(chunks))
    return {"message": "Document trained successfully", "id": doc_id, "chunks": len(chunks)}
