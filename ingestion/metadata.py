def enrich_metadata(documents):
    for doc in documents:
        doc.metadata.setdefault("equipment","unknown")
        doc.metadata.setdefault("department", "maintenance")
    return documents