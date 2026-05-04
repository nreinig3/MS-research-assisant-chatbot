# utils/llm_client.py
import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

def get_api_key():
    """Get API key from either st.secrets (cloud) or .env (local)."""
    # Try Streamlit secrets first (for cloud deployment)
    try:
        return st.secrets["DEEPSEEK_API_KEY"]
    except (FileNotFoundError, AttributeError, KeyError):
        # Fall back to .env for local development
        load_dotenv()
        api_key = os.getenv("DEEPSEEK_API_KEY")
        if not api_key:
            raise ValueError("No API key found. Set DEEPSEEK_API_KEY in .env or Streamlit secrets.")
        return api_key

def get_llm_client():
    """Get the LLM client based on environment configuration."""
    api_key = get_api_key()
    base_url = os.getenv("BASE_URL", "https://api.deepseek.com")
    
    client = OpenAI(
        api_key=api_key,
        base_url=base_url
    )
    return client

def get_model_name():
    """Get the model name from environment variables."""
    return os.getenv("LLM_MODEL", "deepseek-v4-flash")

def get_temperature():
    """Get the temperature setting from environment variables."""
    return float(os.getenv("TEMPERATURE", "0.2"))

def call_llm(messages, temperature=None):
    """
    Call the LLM with a list of messages.
    
    Args:
        messages: List of message dicts with 'role' and 'content'
        temperature: Override default temperature (optional)
    
    Returns:
        The model's response text
    """
    client = get_llm_client()
    model = get_model_name()
    temp = temperature if temperature is not None else get_temperature()
    
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temp
    )
    
    return response.choices[0].message.content

def simple_query(prompt):
    """
    Simple helper for one-off queries without conversation history.
    """
    messages = [{"role": "user", "content": prompt}]
    return call_llm(messages)