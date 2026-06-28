from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

prompt = ChatPromptTemplate.from_messages(
    [("system","You are a helpful assistant. Answer only based on the context below.\n\n context: {context}"),
    ("human","{question}")
    ])
model = ChatOllama(model="gemma4")
parser=StrOutputParser()
chain=prompt | model | parser
def get_llm_answer(question:str, chunks:list):
    context="\n\n".join(chunks)
    return chain.invoke({"context": context,"question":question})