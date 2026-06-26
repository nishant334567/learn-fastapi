# import requests

# def text_embedding(text_content):
#     response = requests.post('http://localhost:11434/api/embeddings',
#     json={
#         "model": "nomic-embed-text",
#         "prompt": text_content
#     })
#     return response.json()["embedding"]


from langchain_ollama import OllamaEmbeddings

embedder = OllamaEmbeddings(model="nomic-embed-text")

def text_embedding(text_content):
    return embedder.embed_query(text_content)