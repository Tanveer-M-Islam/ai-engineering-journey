from langchain_community.vectorstores import (
    FAISS
)

from langchain_community.embeddings import (
    HuggingFaceEmbeddings
)

QUERY_EXPANSIONS = {

    "financial help":
    "scholarship funding student aid",

    "study abroad":
    "admission IELTS international student",

    "accommodation":
    "hostel dormitory residence"
}


def expand_query(
    query
):

    expanded = query

    query_lower = query.lower()

    for key, value in QUERY_EXPANSIONS.items():

        if key in query_lower:

            expanded += " " + value

    return expanded


def generate_queries(
    question
):

    return [

        question,

        f"Explain {question}",

        f"Information about {question}",

        f"Definition of {question}"
    ]


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

    expanded_question = expand_query(
        question
    )

    print(
        "\nExpanded Query:"
    )

    print(
        expanded_question
    )

    queries = generate_queries(
        expanded_question
    )

    all_results = []

    for query in queries:

        docs = (
            vectorstore.similarity_search_with_score(
                query,
                k=2
            )
        )

        all_results.extend(
            docs
        )

    best_results = {}

    for doc, score in all_results:

        content = doc.page_content

        if (
            content not in best_results
            or
            score < best_results[
                content
            ][1]
        ):

            best_results[
                content
            ] = (
                doc,
                score
            )

    reranked = sorted(

        best_results.values(),

        key=lambda x: x[1]
    )

    print(
        "\nTop Results:\n"
    )

    for rank, (doc, score) in enumerate(

        reranked[:3],

        start=1
    ):

        print(
            f"Rank {rank}"
        )

        print(
            f"Score: {score:.4f}"
        )

        print(
            f"Source: {doc.metadata['source']}"
        )

        print(
            doc.page_content
        )

        print(
            "-" * 50
        )