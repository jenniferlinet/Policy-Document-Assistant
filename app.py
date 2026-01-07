import streamlit as st
import faiss
import numpy as np
import re
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import ollama

st.title("Insurance Policy Q&A Assistant")

# Free offline embedding model
EMBEDDER = SentenceTransformer("all-MiniLM-L6-v2")

# -------- FUNCTIONS --------

def parse_pdf(path):
    """Parse uploaded insurance PDF into semantic chunks with page tags"""
    reader = PdfReader(path)
    text = ""
    for i, p in enumerate(reader.pages):
        t = p.extract_text() or ""
        text += f"\n\n---PAGE-{i+1}---\n" + t

    chunks = []
    for s in re.split(r'(?=\n[A-Z][A-Z ]{3,80})', text):
        s = re.sub(r'\s+', ' ', s).strip()
        if len(s) > 80:
            chunks.append(s)

    return chunks


def build_db(chunks):
    """Create FAISS vector index"""
    vec = EMBEDDER.encode(chunks)
    arr = np.array(vec).astype("float32")

    idx = faiss.IndexFlatL2(arr.shape[1])
    idx.add(arr)

    return idx


def retrieve(idx, chunks, query, k=5):
    """Semantic retrieval from FAISS"""
    qv = EMBEDDER.encode([query])
    qv = np.array(qv).astype("float32")

    D, I = idx.search(qv, k)

    return [chunks[i] for i in I[0] if i < len(chunks)]


def ask_llm(question, context):
    """Generate answer using free local LLM"""
    c = "\n".join(context)

    prompt = f"""
    You are INSURANCE POLICY EXPLAINER.
    RULES:
    - Answer ONLY from CONTEXT.
    - Cite PAGE tags if present.
    - Start with YES/NO/PARTIAL.
    - Do not invent.

    CONTEXT:
    {c}

    QUESTION:{question}

    Explain in very simple 3-5 sentences.
    """

    resp = ollama.chat(
        model="llama3",
        messages=[{"role": "user", "content": prompt}]
    )

    return resp["message"]["content"]

# -------- STREAMLIT UI FLOW --------

pdf = st.file_uploader("Upload Insurance Policy PDF", type=["pdf"])

if pdf:
    with open("uploaded_policy.pdf", "wb") as f:
        f.write(pdf.read())

    chunks = parse_pdf("uploaded_policy.pdf")
    idx = build_db(chunks)

    q = st.text_input("Ask your question")

    if q and st.button("Get Answer"):
        ctx = retrieve(idx, chunks, q)
        st.write(ask_llm(q, ctx))

        st.write("### Retrieved Clauses")
        for cl in ctx:
            st.write("- " + cl[:400] + "...")
