import os

from langchain_community.vectorstores import (
    FAISS
)

from langchain_community.embeddings import (
    HuggingFaceEmbeddings
)


all_chunks = []

folder = "documents"

for filename in os.listdir(folder):

    filepath = os.path.join(
        folder,
        filename
    )

    with open(
        filepath,
        "r",
        encoding="utf-8"
    ) as f:

        text = f.read()

        all_chunks.append(
            text
        )

embedding_model = (
    HuggingFaceEmbeddings(
        model_name=
        "sentence-transformers/all-MiniLM-L6-v2"
    )
)

vectorstore = FAISS.from_texts(
    all_chunks,
    embedding_model
)

vectorstore.save_local(
    "faiss_index"
)

print(
    "Multi-document index created."
)