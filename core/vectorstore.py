import os
from langchain_postgres.vectorstores import PGVector
from langchain_ollama import OllamaEmbeddings
from dotenv import load_dotenv

load_dotenv()

vectorstore = PGVector(
    connection=os.getenv("DATABASE_URL"),
    embeddings=OllamaEmbeddings(model="nomic-embed-text"),
    collection_name="knowledge_chunks"
)
