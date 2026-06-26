import requests
def get_llm_answer(question: str, chunks: list):
    context = "\n\n".join(chunks)
    prompt = f"""System: You are a helpful assistant. Answer only based on the context below.

Context:
{context}

User: {question}"""

    response = requests.post('http://localhost:11434/api/chat',
                json={
                "model": "gemma4",
                "messages": [
                    {
                    "role": "user",
                    "content": prompt
                    }
                ],
                "stream": False
            })
    return response.json()["message"]["content"]
