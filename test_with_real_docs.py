# test_with_real_docs.py
from utils.rag_pipeline import answer_question
from utils.embeddings import get_collection

print("=" * 70)
print("🧠 RAG Pipeline Test - Real Documents")
print("=" * 70)

# Show what's in the database
collection = get_collection()
print(f"\n📚 Total documents in collection: {collection.count()}")

# Get a sample of what's stored
sample = collection.get(limit=5)
print(f"\n📄 Sample document sources:")
for meta in sample['metadatas']:
    print(f"   - {meta.get('source', 'unknown')} ({meta.get('type', 'unknown')})")

print("\n" + "=" * 70)
print("🔍 Running Test Queries")
print("=" * 70)

# Test Query 1: General treatment question
print("\n\n--- QUERY 1: Treatments ---")
result1 = answer_question(
    "What treatments are available for multiple sclerosis?", 
    top_k=20
)
print(f"\n💬 ANSWER:\n{result1['answer']}")
print(f"\n📖 Sources ({len(result1['sources'])}):")
for s in result1['sources']:
    print(f"   - {s['source']}")

# Test Query 2: Clinical trial question (if your CSV has trials)
print("\n\n--- QUERY 2: Clinical Trials ---")
result2 = answer_question(
    "What clinical trials are currently recruiting for MS patients?",
    top_k=20
)
print(f"\n💬 ANSWER:\n{result2['answer']}")
print(f"\n📖 Sources ({len(result2['sources'])}):")
for s in result2['sources']:
    print(f"   - {s['source']}")

# Test Query 3: CAR-T question (if your documents mention it)
print("\n\n--- QUERY 2: Clinical Trials ---")
result3 = answer_question(
    "CAR-T?",
    top_k=20
)
print(f"\n💬 ANSWER:\n{result3['answer']}")
print(f"\n📖 Sources ({len(result3['sources'])}):")
for s in result3['sources']:
    print(f"   - {s['source']}")

# Test Query 4: Another specific question about something in your PDFs
print("\n\n--- QUERY 4: Specific Detail ---")
result4 = answer_question(
    "What does the research say about ocrelizumab for progressive MS?",
    top_k=20
)
print(f"\n💬 ANSWER:\n{result4['answer']}")
print(f"\n📖 Sources ({len(result4['sources'])}):")
for s in result4['sources']:
    print(f"   - {s['source']}")