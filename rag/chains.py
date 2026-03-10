from google import genai
from app.config import LLM_MODEL
from rag.prompts import RAG_PROMPT
from rag.retriever import retrieve_documents
from memory.conversation import format_memory


def get_client():
    client=genai.Client()
    return client

def format_docs(documents):
    return "\n\n".join(doc.page_content for doc in documents)

def run_rag(query: str, memory=None):
    if memory is None:
        memory=[]
    documents=retrieve_documents(query)
    context=format_docs(documents)
    memory_text=format_memory(memory)
    prompt=RAG_PROMPT.format(context=context,question=query,memory=memory_text)
    client=get_client()
    response=client.models.generate_content(model=LLM_MODEL,contents=prompt)
    return response.text, documents