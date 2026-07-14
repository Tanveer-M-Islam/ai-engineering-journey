from langchain_community.vectorstores import FAISS

from langchain_huggingface import HuggingFaceEmbeddings


# -----------------------------
# Embedding Model
# -----------------------------

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# -----------------------------
# Load FAISS Index
# -----------------------------

vectorstore = FAISS.load_local(
    "faiss_index",
    embedding_model,
    allow_dangerous_deserialization=True,
)

# -----------------------------
# Retriever
# -----------------------------

retriever = vectorstore.as_retriever(
    search_kwargs={
        "k": 3
    }
)