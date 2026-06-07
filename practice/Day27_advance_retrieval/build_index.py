# from langchain_community.vectorstores import FAISS

# from langchain_community.embeddings import (
#     HuggingFaceEmbeddings
# )

# with open(
#     "knowledge.txt",
#     "r",
#     encoding="utf-8"
# ) as f:

#     text = f.read()

# chunks = text.split("\n\n")

# embedding_model = (
#     HuggingFaceEmbeddings(
#         model_name=
#         "sentence-transformers/all-MiniLM-L6-v2"
#     )
# )

# vectorstore = FAISS.from_texts(
#     chunks,
#     embedding_model
# )

# vectorstore.save_local(
#     "faiss_index"
# )

# print(
#     "Index Created"
# )

#adding metadata 
from langchain_core.documents import (
    Document
)

from langchain_community.vectorstores import (
    FAISS
)

from langchain_community.embeddings import (
    HuggingFaceEmbeddings
)

documents = [

    Document(

        page_content=
        "Artificial Intelligence enables machines to perform intelligent tasks.",

        metadata={
            "topic":"AI"
        }
    ),

    Document(

        page_content=
        "RAG stands for Retrieval-Augmented Generation.",

        metadata={
            "topic":"RAG"
        }
    ),

    Document(

        page_content=
        "FAISS performs vector similarity search.",

        metadata={
            "topic":"FAISS"
        }
    )
]

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