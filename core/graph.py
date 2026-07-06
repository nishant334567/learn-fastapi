from langgraph.prebuilt import create_react_agent
from langchain_ollama import ChatOllama
from core.tools import find_documents_for_question, search_knowledge_base

tools = [find_documents_for_question, search_knowledge_base]
llm = ChatOllama(model="gemma4").bind_tools(tools)

app = create_react_agent(llm, tools)
