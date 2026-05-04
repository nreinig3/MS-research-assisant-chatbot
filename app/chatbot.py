# app/chatbot.py
import streamlit as st
import sys
import os

# Add parent directory to path so we can import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.rag_pipeline import answer_question
from utils.embeddings import get_collection

# Page configuration
st.set_page_config(
    page_title="MS Research Assistant",
    page_icon="🧠",
    layout="wide"
)

# Title and description
st.title("🧠 MS Research Assistant")
st.markdown("""
*Your AI-powered assistant for multiple sclerosis research, clinical trials, and treatment information.*
""")

# Sidebar for user profile and info
with st.sidebar:
    st.header("👤 Your Profile")
    st.markdown("Tell us about yourself for personalized responses.")
    
    # User profile inputs
    age = st.text_input("Age", placeholder="e.g., 45")
    disease_type = st.selectbox(
        "MS Type",
        ["Not specified", "RRMS", "PPMS", "SPMS", "PRMS"]
    )
    disease_duration = st.text_input("Years since diagnosis", placeholder="e.g., 5")
    location = st.text_input("Location (for trial matching)", placeholder="e.g., Seattle, WA")
    
    # Values clarification (MS-SUPPORT inspired)
    st.markdown("---")
    st.header("💭 What matters most to you?")
    priority = st.radio(
        "When considering treatment options, I prioritize:",
        ["Effectiveness", "Side effects", "Cost", "Convenience"]
    )
    
    # Store profile in session state
    st.session_state.user_profile = {
        "age": age,
        "disease_type": disease_type if disease_type != "Not specified" else None,
        "disease_duration_years": disease_duration,
        "location": location,
        "priority": priority
    }
    
    st.markdown("---")
    st.caption("⚠️ **Medical Disclaimer**")
    st.caption("This is a demonstration project. Not medical advice. Always consult a healthcare provider.")
    
    # Show database stats
    st.markdown("---")
    st.header("📊 Knowledge Base")
    try:
        collection = get_collection()
        doc_count = collection.count()
        st.metric("Documents", doc_count)
    except:
        st.metric("Documents", "Loading...")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I'm your MS research assistant. Ask me about treatments, clinical trials, or recent research. I'll provide answers based on my curated knowledge base with citations."}
    ]

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask about MS treatments, clinical trials, or research..."):
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get response from RAG pipeline
    with st.chat_message("assistant"):
        with st.spinner("Searching knowledge base..."):
            # Call your RAG pipeline with the user profile
            result = answer_question(
                prompt,
                user_profile=st.session_state.user_profile,
                top_k=20  # Increased from default
            )
            
            # Display the answer
            st.markdown(result['answer'])
            
            # Display sources in an expander
            if result['sources']:
                with st.expander("📚 Sources"):
                    for i, source in enumerate(result['sources'], 1):
                        st.markdown(f"**{i}. {source['source']}**")
                        st.caption(f"Preview: {source['text'][:150]}...")
                        st.markdown("---")
            
            # Add a disclaimer
            st.caption("⚠️ This information comes from curated sources. Please verify with a healthcare provider.")
    
    # Add assistant response to chat history
    st.session_state.messages.append(
        {"role": "assistant", "content": result['answer']}
    )