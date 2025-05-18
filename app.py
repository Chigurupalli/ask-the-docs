import streamlit as st
import pdfplumber
import os
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
import openai

# Read OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

st.title("Ask the Docs - Mini RAG Web App")

uploaded_file = st.file_uploader("Upload a PDF or TXT file", type=["pdf", "txt"])

chunks = []
index = None
embedder = SentenceTransformer('all-MiniLM-L6-v2')

def read_file(file):
    text = ""
    if file.type == "application/pdf":
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    elif file.type == "text/plain":
        text = file.read().decode("utf-8")
    else:
        st.error("Unsupported file type!")
    return text

def chunk_text(text, chunk_size=500, overlap=50):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks

if uploaded_file:
    raw_text = read_file(uploaded_file)
    if not raw_text.strip():
        st.error("Failed to extract any text from the document.")
    else:
        chunks = chunk_text(raw_text)
        st.success(f"Document split into {len(chunks)} chunks.")

        # create embeddings and faiss index
        embeddings = embedder.encode(chunks)
        embeddings = np.array(embeddings).astype("float32")
        dimension = embeddings.shape[1]
        index = faiss.IndexFlatL2(dimension)
        index.add(embeddings)

        # **Always show question input after splitting document**
        question = st.text_input("Enter your question about the document")

        # Only show "Get Answer" button and answer if question is entered
        if question and st.button("Get Answer"):
            q_embedding = embedder.encode([question])
            D, I = index.search(np.array(q_embedding).astype("float32"), k=3)
            relevant_chunks = [chunks[i] for i in I[0]]
            context = "\n\n".join(relevant_chunks)

            st.subheader("📌 Retrieved Context")
            st.write(context)

            prompt = f"""You are an assistant. Use the following document context to answer the question.

Context:
{context}

Question:
{question}

Answer:"""

            try:
                response = openai.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.2,
                )
                answer = response.choices[0].message.content.strip()
                st.subheader("🧠 Answer from LLM")
                st.write(answer)
            except Exception as e:
                st.error(f"Error in generating answer: {e}")
