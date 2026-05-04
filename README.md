# 🧠 Multiple Sclerosis Research Chatbot

An intelligent RAG (Retrieval-Augmented Generation) chatbot that helps users learn more about MS treatment options, clinical trials, and research advances -- using a curated database of trusted studies and clinical trial data. Augmented with persistent user profiles and transparent citations.

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.41.1-red.svg)](https://streamlit.io/)
[![LangChain](https://img.shields.io/badge/langchain-0.3.15-green.svg)](https://www.langchain.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## Why This Project?

General LLMs like ChatGPT frequently hallucinate (fabricate) details of medical studies and other health data that can cause serious problems for patients if they trust the responses they get from the LLM (I caught one inventing a primate study on MS). This chatbot reduces the chance of misleading users by:

- **Controlled knowledge base** — answers only from curated medical documents
- **Transparent citations** — every claim links to a specific source
- **Persistent user profiles** — remembers you across sessions for personalized research help

## Features

| Feature | Description |
|---------|-------------|
| 🔍 **RAG Architecture** | Retrieves relevant chunks from vector database before generating answers |
| 📚 **Curated Knowledge Base** | 800+ documents including clinical trials, guidelines, and research papers |
| 🌍 **International Trials** | Searches non-US registries (EU, Chinese, and others) |
| 👤 **User Profiling** | Remembers age, MS type, location, and treatment priorities |
| 📖 **Source Citations** | Every answer includes verifiable source links |
| 🚫 **Hallucination Resistant** | Refuses to answer when information isn't in the knowledge base |
| 🌐 **Live Demo** | [Deployed and accessible via browser](https://your-deployed-url.com) |

## Architecture
