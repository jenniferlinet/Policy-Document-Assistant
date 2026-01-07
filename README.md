# Insurance Policy Document Q&A Assistant

A simple offline RAG system that:

- Parses uploaded Indian insurance policy PDFs  
- Performs semantic search using the free all-MiniLM embedding model  
- Answers questions using a free local LLM (Llama3 via Ollama)  
- Shows retrieved clauses for transparency to prevent hallucination.

## Setup

1. Install dependencies

pip install -r requirements.txt

2. Pull free model

ollama pull llama3

3. Run UI

streamlit run app.py

## Example Questions

- Does my policy cover sudden water leakage?  
- What damages are excluded?  
- What is the deductible amount?
