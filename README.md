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

## Testing Reference Document

The assistant was tested using the PDF file **gecc129849942.pdf**, which contains real commercial Indian-style home insurance wording with sections on coverage, limits, exclusions, and conditions.  
This document was used **only for evaluation of retrieval and answer generation**, and the policy text itself is not claimed as original content of this repository.

### Example Inputs & Outputs

**Input 1**
Question: *Does the policy cover sudden water leakage?*

**Output 1**
Answer: YES – The policy explains under ---PAGE-1--- Section 1 that sudden and accidental water leakage, fire, explosion, theft are covered up to the scheduled sum insured. Gradual seepage is excluded in ---PAGE-1--- exclusion 3(a).

---

**Input 2**
Question: *Are gradual seepage damages covered?*

**Output 2**
Answer: NO – Clause ---PAGE-1--- Exclusion 3(a) clearly states that gradual seepage, poor maintenance, and pre-existing damages are not included.

---

**Input 3**
Question: *What is deductible for water damage claim?*

**Output 3**
Answer: PARTIAL – As per ---PAGE-1--- Condition 5 the deductible amount is INR 2,000 for any water damage FNOL/claim. Additional riders can change this limit.

---

### How Accuracy Was Evaluated

1. Embedding retrieval using **all-MiniLM-L6-v2** located the most relevant clauses from the PDF.  
2. The LLM generated answers strictly from retrieved context to minimise hallucination.  
3. Page tags were referenced in every response to ensure traceability.

### Benefits Demonstrated

- Customers can understand coverage without reading entire documents  
- Queries answered in plain language  
- Retrieval vs exclusions cross-checked in real time.

