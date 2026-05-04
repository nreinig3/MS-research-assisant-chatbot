# test_retrieval.py
from utils.embeddings import retrieve

query = "What treatments exist for progressive MS?"

results = retrieve(query, top_k=3)

print(f"Query: {query}\n")
print(f"Found {len(results['documents'][0])} results:\n")

for i, (doc, metadata, distance) in enumerate(zip(
    results['documents'][0],
    results['metadatas'][0],
    results['distances'][0]
)):
    print(f"Result {i+1} (distance: {distance:.4f}):")
    print(f"  Source: {metadata.get('source', 'unknown')}")
    print(f"  Preview: {doc[:200]}...")
    print()