# utils/rag_pipeline.py
from utils.embeddings import retrieve
from utils.llm_client import call_llm

# System prompt template - this is where RAG magic happens
SYSTEM_PROMPT = """You are a helpful assistant for multiple sclerosis (MS) patients and researchers.

Your task is to answer questions based ONLY on the provided context. If the context does not contain enough information to answer, say "I don't have that information in my knowledge base. Please consult a healthcare provider."

For every medical claim you make, cite the source document from the context.

Be accurate, clear, and compassionate. Never invent information.

--- CONTEXT START ---
{context}
--- CONTEXT END ---

User profile information (if provided):
{profile}

Remember: Only answer from the context above. If uncertain, say you don't know.
"""

def format_retrieved_results(results, include_full_text=True):
    """
    Format retrieved results into a single context string for the LLM.
    
    Args:
        results: The results dict from chromadb query
        include_full_text: If True, include full document text
    
    Returns:
        Formatted context string with source citations
    """
    if not results or not results['documents'][0]:
        return "No relevant documents found in the knowledge base."
    
    context_parts = []
    
    for i, (doc, metadata, distance) in enumerate(zip(
        results['documents'][0],
        results['metadatas'][0],
        results['distances'][0]
    )):
        source = metadata.get('source', 'unknown')
        doc_type = metadata.get('type', 'document')
        relevance_score = 1 - distance  # Convert distance to similarity
        
        # Truncate very long documents
        text_preview = doc[:800] + "..." if len(doc) > 800 else doc
        
        part = f"""[Document {i+1}] Source: {source} | Type: {doc_type} | Relevance: {relevance_score:.2f}
{text_preview if include_full_text else '[Content available]'}
---"""
        context_parts.append(part)
    
    return "\n".join(context_parts)

def build_profile_string(profile):
    """Convert user profile dict to a readable string for the prompt."""
    if not profile:
        return "No profile information provided."
    
    profile_lines = []
    for key, value in profile.items():
        if value:
            # Clean up key names for display
            display_key = key.replace('_', ' ').title()
            profile_lines.append(f"- {display_key}: {value}")
    
    if not profile_lines:
        return "No profile information provided."
    
    return "\n".join(profile_lines)

def answer_question(query, user_profile=None, top_k=5):
    """
    Main RAG function: retrieve context, build prompt, generate answer.
    
    Args:
        query: User's question (string)
        user_profile: Dict with user info (age, disease_type, etc.) - optional
        top_k: Number of documents to retrieve
    
    Returns:
        Dict containing answer, sources, and metadata
    """
    print(f"🔍 Retrieving top {top_k} documents for: {query[:50]}...")
    
    # Step 1: Retrieve relevant documents from Chroma
    results = retrieve(query, top_k=top_k)
    
    # Step 2: Format context from retrieved documents
    context = format_retrieved_results(results, include_full_text=True)
    
    # Step 3: Build user profile string
    profile_str = build_profile_string(user_profile)
    
    # Step 4: Build the prompt with system instructions
    system_prompt_with_context = SYSTEM_PROMPT.format(
        context=context,
        profile=profile_str
    )
    
    # Step 5: Create messages for the LLM
    messages = [
        {"role": "system", "content": system_prompt_with_context},
        {"role": "user", "content": query}
    ]
    
    # Step 6: Get LLM response
    print("🤖 Generating answer from LLM...")
    answer = call_llm(messages)
    
    # Step 7: Extract source information for display
    sources = []
    if results and results['documents'][0]:
        for doc, metadata in zip(results['documents'][0], results['metadatas'][0]):
            sources.append({
                "text": doc[:200] + "..." if len(doc) > 200 else doc,
                "source": metadata.get('source', 'unknown'),
                "type": metadata.get('type', 'document')
            })
    
    return {
        "answer": answer,
        "sources": sources,
        "retrieved_count": len(results['documents'][0]) if results['documents'] else 0,
        "query": query
    }