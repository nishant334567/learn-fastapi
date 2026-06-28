from langchain_ollama import OllamaEmbeddings

embedder = OllamaEmbeddings(model="nomic-embed-text")

def text_embedding(text_content):
    return embedder.embed_query(text_content)