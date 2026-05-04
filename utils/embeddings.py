# utils/embeddings.py
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.utils import embedding_functions
import os

# Global variables (will be initialized once)
_embedding_model = None
_chroma_client = None
_collection = None

def get_embedding_model():
    """Load the sentence transformer model (cached after first call)."""
    global _embedding_model
    if _embedding_model is None:
        print("Loading embedding model (first time may take a moment)...")
        _embedding_model = SentenceTransformer('pritamdeka/S-BioBERT-snli-mnli')
        print("✅ Embedding model loaded")
    return _embedding_model

def get_chroma_client():
    """Get or create Chroma DB client."""
    global _chroma_client
    if _chroma_client is None:
        _chroma_client = chromadb.PersistentClient(path="./chroma_db")
        print("✅ Chroma DB client initialized")
    return _chroma_client

def get_collection(collection_name="ms_research"):
    """Get or create a Chroma collection."""
    client = get_chroma_client()
    
    # Create embedding function for Chroma using sentence-transformers
    embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name='sentence-transformers/all-MiniLM-L6-v2'
    )
    
    # Get or create collection
    collection = client.get_or_create_collection(
        name=collection_name,
        embedding_function=embedding_fn
    )
    print(f"✅ Collection '{collection_name}' ready (contains {collection.count()} documents)")
    return collection

def embed_and_store(texts, metadatas, ids, collection_name="ms_research"):
    """Embed texts and store them in Chroma."""
    collection = get_collection(collection_name)
    
    # Chroma automatically embeds using the collection's embedding function
    collection.add(
        documents=texts,
        metadatas=metadatas,
        ids=ids
    )
    print(f"✅ Added {len(texts)} documents to collection")
    return collection.count()

def retrieve(query, top_k=5, collection_name="ms_research"):
    """Retrieve top_k most relevant documents for a query."""
    collection = get_collection(collection_name)
    
    results = collection.query(
        query_texts=[query],
        n_results=top_k
    )
    
    return results