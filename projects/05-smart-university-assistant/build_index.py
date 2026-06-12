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

for filename in os.listdir(
    "documents"
):

    filepath = os.path.join(
        "documents",
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
    "Index Created"
)