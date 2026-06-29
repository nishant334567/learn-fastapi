from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from core.vectorstore import vectorstore
from core.llm import get_llm_answer


class RAGState(TypedDict):
    question: str
    chunks: List[str]
    answer: str

def retrieve(state:RAGState):
    docs=vectorstore.similarity_search(state["question"],k=5)
    chunks=[doc.page_content for doc in docs]
    return {"chunks":chunks}

def generate(state:RAGState):
    answer=get_llm_answer(state["question"],state["chunks"])
    return {"answer":answer}

graph=StateGraph(RAGState)

graph.add_node("retrieve", retrieve)
graph.add_node("generate", generate)

graph.set_entry_point("retrieve")
graph.add_edge("retrieve","generate")
graph.add_edge("generate",END)

app=graph.compile()