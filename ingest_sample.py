# ingest_sample.py
from utils.embeddings import embed_and_store
import uuid

# Read the sample document
with open("data/raw/sample.txt", "r") as f:
    text = f.read()

# Split into chunks (simple for now - just one chunk)
chunks = [text]

# Create metadata
metadatas = [
    {
        "source": "sample.txt",
        "type": "sample",
        "topic": "MS overview"
    }
]

# Create unique IDs
ids = [str(uuid.uuid4()) for _ in chunks]

# Store in Chroma
count = embed_and_store(chunks, metadatas, ids)

print(f"Stored {count} total documents")