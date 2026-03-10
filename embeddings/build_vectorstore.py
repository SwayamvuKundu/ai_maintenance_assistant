from ingestion.loaders import load_all_documents
from ingestion.chunking import chunk_documents
from ingestion.metadata import enrich_metadata
from utils.logger import get_logger

from vectorstore.chroma_store import get_chroma_store

logger=get_logger(__name__)


def build_vectorstore():
    documents=load_all_documents()
    documents=chunk_documents(documents)
    documents=enrich_metadata(documents)
    logger.info(f"Clean documents count:{len(documents)}")
    get_chroma_store(documents)
    logger.info("Vector store built successfully")

if __name__=="__main__":
    build_vectorstore()