import os

from langchain_core.documents import (
    Document
)

from langchain_community.vectorstores import (
    FAISS
)

from langchain_community.embeddings import (
    HuggingFaceEmbeddings
)

documents = []

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

    documents.append(

        Document(

            page_content=text,

            metadata={
                "source": filename
            }
        )
    )

embedding_model = (
    HuggingFaceEmbeddings(
        model_name=
        "sentence-transformers/all-MiniLM-L6-v2"
    )
)

vectorstore = FAISS.from_documents(
    documents,
    embedding_model
)

vectorstore.save_local(
    "faiss_index"
)

print(
    "Source-aware index created."
)