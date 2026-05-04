# test_embeddings.py
from utils.embeddings import get_embedding_model, get_chroma_client, get_collection

print("Testing embedding setup...")

# Test embedding model
model = get_embedding_model()
print(f"Embedding dimension: {model.get_sentence_embedding_dimension()}")

# Test Chroma
client = get_chroma_client()
collection = get_collection()
print(f"Collection count: {collection.count()}")

print("✅ All embedding components work!")