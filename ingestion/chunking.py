from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.config import CHUNK_SIZE,CHUNK_OVERLAP
from utils.logger import get_logger

logger=get_logger(__name__)

def chunk_documents(documents):
    splitter=RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE,chunk_overlap=CHUNK_OVERLAP)
    chunks=splitter.split_documents(documents)
    logger.info(f"Split into {len(chunks)} chunks")
    return chunks