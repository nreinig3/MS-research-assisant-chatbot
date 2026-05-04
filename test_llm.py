# test_llm.py
from utils.llm_client import simple_query, get_model_name

print(f"Using model: {get_model_name()}")
print("Testing LLM connection...")

response = simple_query("Say 'Hello, RAG system is working!' in exactly 8 words.")
print(f"Response: {response}")
print("✅ LLM client works!")