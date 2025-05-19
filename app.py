
import streamlit as st
import pdfplumber
import os
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
import openai

# Set API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="Ask the Docs", layout="wide")
st.title("📚 Ask the Docs - Mini RAG Web App")

# Initialize session state for history
if "history" not in st.session_state:
    st.session_state.history = []

# Load embedding model
embedder = SentenceTransformer('all-MiniLM-L6-v2')
chunks = []
index = None

# File reading functions
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

# Tabs UI
tab1, tab2, tab3 = st.tabs(["📁 Upload & Process", "❓ Ask Questions", "📜 History"])

# --- Upload & Process Tab ---
with tab1:
    uploaded_files = st.file_uploader("Upload PDF or TXT files", type=["pdf", "txt"], accept_multiple_files=True)

    if uploaded_files:
        raw_text = ""
        for file in uploaded_files:
            raw_text += read_file(file) + "\n"

        if not raw_text.strip():
            st.error("❌ Failed to extract text from documents.")
        else:
            chunks = chunk_text(raw_text)
            st.success(f"✅ Split document into {len(chunks)} chunks.")

            embeddings = embedder.encode(chunks)
            embeddings = np.array(embeddings).astype("float32")
            dimension = embeddings.shape[1]
            index = faiss.IndexFlatL2(dimension)
            index.add(embeddings)
            st.session_state.chunks = chunks
            st.session_state.index = index
            st.success("✅ Embeddings and index created.")

# --- Ask Questions Tab ---
with tab2:
    if "index" not in st.session_state or "chunks" not in st.session_state:
        st.info("Please upload and process documents first in the Upload tab.")
    else:
        question = st.text_input("Enter your question about the documents:")
        if question and st.button("Get Answer"):
            q_embedding = embedder.encode([question])
            D, I = st.session_state.index.search(np.array(q_embedding).astype("float32"), k=3)
            relevant_chunks = [st.session_state.chunks[i] for i in I[0]]
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
                st.session_state.history.append((question, answer))
            except Exception as e:
                st.error(f"❌ Error in generating answer: {e}")

# --- History Tab ---
with tab3:
    st.subheader("📜 Question & Answer History")
    if st.session_state.history:
        for i, (q, a) in enumerate(st.session_state.history):
            st.markdown(f"**Q{i+1}:** {q}")
            st.markdown(f"**A{i+1}:** {a}")
            st.markdown("---")
    else:
        st.info("No questions asked yet.")
