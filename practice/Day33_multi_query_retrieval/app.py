from langchain_community.vectorstores import (
    FAISS
)

from langchain_community.embeddings import (
    HuggingFaceEmbeddings
)


def generate_queries(question):

    queries = [

        question,

        f"Explain {question}",

        f"Definition of {question}",

        f"Information about {question}"

    ]

    return queries


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

    queries = generate_queries(
        question
    )

    print(
        "\nGenerated Queries:"
    )

    for q in queries:

        print(
            "-",
            q
        )

    all_results = []

    for query in queries:

        docs = vectorstore.similarity_search(
            query,
            k=2
        )

        all_results.extend(
            docs
        )

    unique_chunks = []

    seen = set()

    for doc in all_results:

        content = doc.page_content

        if content not in seen:

            seen.add(
                content
            )

            unique_chunks.append(
                content
            )

    print(
        "\nRetrieved Chunks:\n"
    )

    for i, chunk in enumerate(
        unique_chunks,
        start=1
    ):

        print(
            f"{i}. {chunk}"
        )

        print(
            "-" * 50
        )