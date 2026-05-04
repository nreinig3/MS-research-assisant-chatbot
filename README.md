# 🧠 Multiple Sclerosis Research Assistant

An intelligent RAG (Retrieval-Augmented Generation) chatbot that helps multiple sclerosis patients and researchers discover personalized treatment options, clinical trials, and research advances — with persistent user profiles, transparent citations, and international trial discovery.

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.41.1-red.svg)](https://streamlit.io/)
[![LangChain](https://img.shields.io/badge/langchain-0.3.15-green.svg)](https://www.langchain.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## 🎯 Why This Project?

General LLMs like ChatGPT hallucinate — they confidently invent studies that don't exist (I caught one inventing a primate CAR-T study). This chatbot solves that by:

- **Controlled knowledge base** — answers only from curated medical documents
- **Transparent citations** — every claim links to a specific source
- **Persistent user profiles** — remembers you across sessions
- **International trials** — includes research from China, Cuba, and beyond

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🔍 **RAG Architecture** | Retrieves relevant chunks from vector database before generating answers |
| 📚 **Curated Knowledge Base** | 800+ documents including clinical trials, guidelines, and research papers |
| 🌍 **International Trials** | Searches non-US registries (Chinese, Cuban, Brazilian) |
| 👤 **User Profiling** | Remembers age, MS type, location, and treatment priorities |
| 💬 **Conversation Memory** | Maintains context across multi-turn conversations |
| 📖 **Source Citations** | Every answer includes verifiable source links |
| 🚫 **Hallucination Resistant** | Refuses to answer when information isn't in the knowledge base |
| 🌐 **Live Demo** | [Deployed and accessible via browser](https://your-deployed-url.com) |

## 🏗️ Architecture
