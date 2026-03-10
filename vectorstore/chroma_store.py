from langchain_chroma import Chroma
from embeddings.embedder import get_embedding_model
from app.config import VECTOR_DB_PATH,TOP_K,FETCH_K,LAMBDA_MULT

def get_chroma_store(documents=None):
    embedding_model=get_embedding_model()
    if documents:
        store=Chroma.from_documents(documents=documents, embedding=embedding_model, persist_directory=VECTOR_DB_PATH)
        return store
    return Chroma(persist_directory=VECTOR_DB_PATH,embedding_function=embedding_model)

def retrieve_documents(query: str):
    vectorstore=get_chroma_store()
    retriever=vectorstore.as_retriever(search_type="mmr", search_kwargs={"k": TOP_K,"fetch_k":FETCH_K,"lambda_mult":LAMBDA_MULT})
    return retriever.invoke(query)