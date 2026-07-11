import os

from langchain_core.documents import Document

from langchain_community.vectorstores import FAISS

from langchain_huggingface import HuggingFaceEmbeddings


DATA_FOLDER = "documents"

documents = []

for file_name in os.listdir(DATA_FOLDER):

    file_path = os.path.join(
        DATA_FOLDER,
        file_name
    )

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as f:

        text = f.read()

    documents.append(

        Document(

            page_content=text,

            metadata={

                "source": file_name
            }
        )
    )


embeddings = HuggingFaceEmbeddings(

    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


vectorstore = FAISS.from_documents(

    documents,

    embeddings
)


vectorstore.save_local(

    "faiss_index"
)

print()

print("FAISS index created successfully.")

print("Indexed", len(documents), "documents.")