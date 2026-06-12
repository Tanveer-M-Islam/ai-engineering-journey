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

    results = (
        vectorstore.similarity_search_with_score(
            question,
            k=1
        )
    )

    reranked = sorted(
        results,
        key=lambda x: x[1]
    )

    print(
        "\nRe-Ranked Results:\n"
    )

    for rank, (doc, score) in enumerate(
        reranked,
        start=1
    ):

        print(
            f"Rank {rank}"
        )

        print(
            f"Score: {score:.4f}"
        )

        print(
            doc.page_content
        )

        print(
            "-" * 50
        )