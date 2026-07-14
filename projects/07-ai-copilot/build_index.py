from pathlib import Path

from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


# -----------------------------
# Embedding Model
# -----------------------------

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# -----------------------------
# Load Documents
# -----------------------------

documents = []

document_folder = Path("documents")

for file in document_folder.glob("*.txt"):

    loader = TextLoader(
        str(file),
        encoding="utf-8",
    )

    docs = loader.load()

    for doc in docs:
        doc.metadata["source"] = file.name

    documents.extend(docs)

# -----------------------------
# Split Documents
# -----------------------------

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
)

chunks = splitter.split_documents(documents)

print(f"Loaded {len(chunks)} chunks.")

# -----------------------------
# Create Vector Store
# -----------------------------

vectorstore = FAISS.from_documents(
    chunks,
    embedding_model,
)

vectorstore.save_local("faiss_index")

print("FAISS index created successfully.")