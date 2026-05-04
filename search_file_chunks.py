# search_file_chunks.py
from utils.embeddings import get_collection

collection = get_collection()
all_docs = collection.get()

# Look for your specific PDFs
target_files = [
    "Mei_2022_Chinese_Expert_Consensus_CAR_T.pdf",
    "Qin_2025_Anti-BCMA_CART_Pro_MS.pdf"
]

print("🔍 Searching for chunks from specific files...")
print("-" * 60)

for target in target_files:
    found_chunks = []
    for doc, metadata in zip(all_docs['documents'], all_docs['metadatas']):
        if metadata.get('source') == target:
            found_chunks.append(doc)
    
    print(f"\n📄 {target}:")
    print(f"   Chunks found: {len(found_chunks)}")
    
    if found_chunks:
        print(f"   First chunk preview (first 200 chars):")
        print(f"   {found_chunks[0][:200]}...")
    else:
        print(f"   ❌ No chunks found for this file")