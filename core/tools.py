from langchain_core.tools import tool
from core.vectorstore import vectorstore

@tool
def find_documents_for_question(query:str)->list[{"document_id":str,"document_name":str}]:
    """Search the knwoledge base when the user wants to know which all documwents are already in his
    knowledge base"""
    docs = vectorstore.similarity_search(query,k=10)
    if not docs:
        return "No documents founds"
    docs_list = [{'document_id':doc.metadata['document_id'],'document_name':doc.metadata['document_name']} for doc in docs]
    return docs_list

