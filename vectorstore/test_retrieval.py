from vectorstore.chroma_store import retrieve_documents

query="When was the CNC-001 Vertical Milling Machine last maintained?"

results=retrieve_documents(query)

for i, doc in enumerate(results,1):
    print(f"\n--- Result {i} ---")
    print(doc.page_content[:10000])