import os
from dotenv import load_dotenv

load_dotenv()

LLM_MODEL=os.getenv("LLM_MODEL")
EMBEDDING_MODEL=os.getenv("EMBEDDING_MODEL")

CHUNK_SIZE=600
CHUNK_OVERLAP=100

VECTOR_DB_PATH=os.getenv("VECTOR_DB_PATH")

TOP_K=8
FETCH_K=18
LAMBDA_MULT=0.7
