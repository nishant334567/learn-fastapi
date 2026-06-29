import sys
import os
import asyncio

# Repo root on path so core.vectorstore is importable
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from livekit.agents import Agent, function_tool
from core.vectorstore import vectorstore


class ReceptionAgent(Agent):
    def __init__(self):
        super().__init__(
            instructions="""
You are a helpful voice AI assistant with access to a knowledge base.

Rules:
- Keep answers short and conversational — this is spoken audio
- No bullet points, markdown, or lists — speak in natural sentences
- Always search the knowledge base before answering factual questions
- Never make up facts. If the knowledge base has no answer, say so clearly.
""".strip()
        )

    @function_tool
    async def search_knowledge_base(self, question: str) -> str:
        """
        Search the knowledge base for information relevant to the user's question.
        Call this for any factual question before answering.
        """
        # vectorstore.similarity_search is synchronous — offload to thread
        docs = await asyncio.to_thread(vectorstore.similarity_search, question, k=5)
        if not docs:
            return "No relevant information found."
        return "\n\n".join(doc.page_content for doc in docs)
