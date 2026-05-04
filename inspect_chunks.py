# inspect_chunks.py
from utils.embeddings import get_collection

collection = get_collection()

# Get all documents with their metadata
all_docs = collection.get()

print(f"Total documents: {len(all_docs['ids'])}\n")

# Find documents containing CAR-T keywords
print("🔍 Searching for CAR-T related documents...")
print("-" * 60)

car_t_docs = []
for i, (doc, metadata) in enumerate(zip(all_docs['documents'], all_docs['metadatas'])):
    doc_lower = doc.lower()
    if any(keyword in doc_lower for keyword in ['car-t', 'cart', 'car t', 'chimeric antigen']):
        car_t_docs.append((doc, metadata))

print(f"Found {len(car_t_docs)} chunks containing CAR-T keywords\n")

if car_t_docs:
    for idx, (doc, metadata) in enumerate(car_t_docs[:5]):
        print(f"Document {idx+1}:")
        print(f"  Source: {metadata.get('source', 'unknown')}")
        print(f"  Type: {metadata.get('type', 'unknown')}")
        print(f"  Preview: {doc[:300]}...")
        print()
else:
    print("No CAR-T chunks found in the database.")
    print("\nChecking if documents were actually added...")
    
    # Show all unique source files
    sources = set()
    for metadata in all_docs['metadatas']:
        sources.add(metadata.get('source', 'unknown'))
    
    print(f"Source files in database: {list(sources)}")