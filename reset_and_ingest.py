# reset_and_ingest.py
from utils.embeddings import get_collection

# 1. Clear the collection
collection = get_collection()
count_before = collection.count()
print(f"Deleting {count_before} documents...")

# Delete all documents
collection.delete(ids=collection.get()['ids'])

print(f"Collection now has {collection.count()} documents")

# 2. Now re-run your ingestion script
print("\n" + "=" * 60)
print("Re-running ingestion...")
print("=" * 60)

exec(open("ingest_all_documents.py").read())