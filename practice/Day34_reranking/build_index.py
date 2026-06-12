from langchain_community.vectorstores import (
    FAISS
)

from langchain_community.embeddings import (
    HuggingFaceEmbeddings
)

with open(
    "knowledge.txt",
    "r",
    encoding="utf-8"
) as f:

    text = f.read()

chunks = [

    chunk.strip()

    for chunk in text.split("\n\n")

    if chunk.strip()
]

embedding_model = (
    HuggingFaceEmbeddings(
        model_name=
        "sentence-transformers/all-MiniLM-L6-v2"
    )
)

vectorstore = FAISS.from_texts(
    chunks,
    embedding_model
)

vectorstore.save_local(
    "faiss_index"
)

print(
    "Index created."
)