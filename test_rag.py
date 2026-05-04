# test_rag.py
from utils.rag_pipeline import answer_question
from utils.embeddings import get_collection

print("=" * 60)
print("🧠 RAG Pipeline Test")
print("=" * 60)

# Check how many documents are in the database
collection = get_collection()
print(f"\n📚 Knowledge base contains {collection.count()} documents\n")

# Test query that should match your sample document
query = "What treatments are available for multiple sclerosis?"
print(f"🔍 Query: {query}\n")
print("-" * 60)

result = answer_question(query, user_profile=None, top_k=3)

print("\n" + "=" * 60)
print("💬 ANSWER:")
print("=" * 60)
print(result['answer'])

print("\n" + "=" * 60)
print("📖 SOURCES USED:")
print("=" * 60)
for i, source in enumerate(result['sources'], 1):
    print(f"{i}. Source: {source['source']} ({source['type']})")
    print(f"   Preview: {source['text'][:100]}...")

print(f"\n✅ Retrieved {result['retrieved_count']} documents")