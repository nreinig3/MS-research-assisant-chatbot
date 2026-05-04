# Fix for Streamlit + PyTorch compatibility issue
import torch
torch.classes.__path__ = []  # This bypasses the problematic attribute check

# Then your normal imports
import streamlit as st
# ... rest of your imports


# run_app.py
import subprocess
import sys

if __name__ == "__main__":
    subprocess.run([sys.executable, "-m", "streamlit", "run", "app/chatbot.py"])