from langchain_community.vectorstores import (
    FAISS
)

from langchain_community.embeddings import (
    HuggingFaceEmbeddings
)


embedding_model = (
    HuggingFaceEmbeddings(
        model_name=
        "sentence-transformers/all-MiniLM-L6-v2"
    )
)

vectorstore = FAISS.load_local(
    "faiss_index",
    embedding_model,
    allow_dangerous_deserialization=True
)

while True:

    question = input(
        "\nQuestion: "
    )

    if question.lower() == "exit":
        break

    docs = vectorstore.similarity_search(
        question,
        k=3
    )

    print(
        "\nRetrieved Chunks:\n"
    )

    for i, doc in enumerate(
        docs,
        start=1
    ):

        print(
            f"{i}.",
            doc.page_content
        )

        print(
            "-" * 50
        )

    for doc in docs:

         print(
        "\nContent:"
         )

         print(
        doc.page_content
         )

         print(
        "Metadata:"
         )

         print(
        doc.metadata
         )