from rag.chains import run_rag
query="what all machines are you aware of?"

answer,sources=run_rag(query)

print("ANSWER:\n",answer)
print("\nSOURCES USED:",len(sources))