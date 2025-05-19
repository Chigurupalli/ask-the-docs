



# Ask the Docs - Mini RAG App

This is a Retrieval-Augmented Generation (RAG) application that allows users to query documents and get accurate answers powered by a Large Language Model (LLM). Built as part of the Cloud & Backend Engineering Internship task at Convolution Engineering Consultancy for the BidWiser product.

## Demo

*Live URL*: [https://your-app-url.com](https://your-app-url.com)

## Features

- Upload documents (PDF, TXT)
- Ask questions based on document content
- Uses embeddings and vector similarity search
- Generates accurate responses using LLM
- Deployed on AWS

---

## Architecture

1. *Document Ingestion*
   - Uploaded documents are parsed and chunked.
   - Embeddings are generated for each chunk using sentence-transformers.

2. *Vector Store*
   - Embeddings are stored in a vector store (e.g., *FAISS* or *ChromaDB*).
   - When a question is asked, similar chunks are retrieved using cosine similarity.

3. *LLM Response*
   - Retrieved context is passed to the LLM (e.g., OpenAI GPT-4 or HuggingFace model) via LangChain or custom prompt.
   - The final answer is generated using the retrieved chunks as context.

---

## Tech Stack

- *Frontend*: Streamlit (or Flask with HTML if used)
- *Backend*: Python (FastAPI or Flask)
- *Embeddings Model*: all-MiniLM-L6-v2 from sentence-transformers
- *Vector Store*: FAISS or ChromaDB
- *LLM*: OpenAI GPT-4 (via API) or open-source model via Hugging Face
- *Deployment*: AWS EC2 (or Render/Vercel if used)

---

## How to Run Locally

1. *Clone the repo*

```bash
git clone https://github.com/Chigurupalli/ask-the-docs-rag.git
cd ask-the-docs-rag

2. Install dependencies



pip install -r requirements.txt

3. Run the app



streamlit run app.py
# or
python app.py  # if using Flask


---

Folder Structure

ask-the-docs-rag/
│
├── app.py                 # Main application
├── utils/                 # Helpers for loading, embedding, searching
├── requirements.txt
├── README.md
├── .env                   # API keys (if needed)
└── data/                  # Sample documents


---

Notes on LLM / Models Used

Embedding Model: all-MiniLM-L6-v2
Efficient and lightweight transformer model to generate vector embeddings of text chunks.

LLM Used:

Primary: OpenAI GPT-4 via API for final response generation.

Alternate (optional): Mistral or Mixtral via Hugging Face Transformers for local setups.


Vector DB: FAISS is used for efficient similarity search, storing dense vector embeddings.



---

Method Summary

This project implements the RAG (Retrieval-Augmented Generation) approach:

1. Preprocess documents and split into manageable chunks.


2. Generate vector embeddings for each chunk.


3. Store in a vector database (FAISS/Chroma).


4. On question input:

Convert question to vector.

Find top-k similar chunks via vector similarity.

Pass relevant context + question to LLM.

Return generated response.

















