from ingestion.loaders import load_all_documents
from ingestion.chunking import chunk_documents
from ingestion.metadata import enrich_metadata

docs=load_all_documents()
docs=enrich_metadata(docs)
chunks=chunk_documents(docs)

print(f"Sample chunk:\n{chunks[0].page_content}")
print(f"Metadata:\n{chunks[0].metadata}")