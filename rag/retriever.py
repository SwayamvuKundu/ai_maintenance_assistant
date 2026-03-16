from vectorstore.chroma_store import get_chroma_store
from app.config import TOP_K, FETCH_K, LAMBDA_MULT

def retrieve_documents(query: str,memory: str):
    vectorstore=get_chroma_store()
    retriever=vectorstore.as_retriever(search_type="mmr", search_kwargs={"k": TOP_K,"fetch_k":FETCH_K,"lambda_mult":LAMBDA_MULT})
    return retriever.invoke(query+memory)