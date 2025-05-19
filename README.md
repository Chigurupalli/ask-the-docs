# Ask the Docs - Mini RAG Web App

This is a mini Retrieval-Augmented Generation (RAG) web application built with Streamlit that allows users to upload PDF or TXT documents, split them into chunks, create embeddings, and ask questions about the document content using OpenAI's GPT-3.5 Turbo model.

## Features
- Upload PDF or TXT files
- Extract text and split into chunks for better context handling
- Generate sentence embeddings using SentenceTransformers (`all-MiniLM-L6-v2`)
- Use FAISS for fast similarity search of relevant document chunks
- Query the document via OpenAI GPT-3.5 Turbo chat completion API
- Display retrieved context and generated answers

## Requirements
- Python 3.7+
- Install dependencies with:
pip install -r requirements.txt

markdown
Copy
Edit
- An OpenAI API key set as environment variable `OPENAI_API_KEY`
- Docker (optional, for containerization)

## Usage

1. Clone the repo:
git clone https://github.com/Chigurupalli/ask-the-docs.git

cd ask-the-docs

vbnet
Copy
Edit

2. Set your OpenAI API key:
export OPENAI_API_KEY=i cant provide publicly

markdown
Copy
Edit

3. Run the app:
streamlit run app.py

4. Open your browser at `http://localhost:8501`

## Docker

To build and run with Docker:

docker build -t ask-the-docs .
docker run -d -p 8501:8501 ask-the-docs



Then open  
`http://13.60.56.228:8501/


## Notes
- Ensure your OpenAI API key has enough quota to avoid 429 errors.
- Supported file types: PDF and TXT only.
- Embeddings are created using the `all-MiniLM-L6-v2` SentenceTransformer model.
- FAISS is used for efficient similarity search.## Limitations
##LIMITATION ##
⚠️ **OpenAI API Quota**: This app uses OpenAI's GPT-3.5 Turbo model. If you see errors like `Error code: 429 - insufficient_quota`, it means your OpenAI API key has reached its free usage limit. To continue using the app, please ensure your OpenAI account has an active billing setup or available quota.

- 

## Author
Chigurupalli Hruthik Sai





















