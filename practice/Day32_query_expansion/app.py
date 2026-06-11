QUERY_EXPANSIONS = {

    "backend":
    "backend APIs FastAPI Python",

    "chatbot":
    "chatbot LangChain LLM",

    "search":
    "search embeddings FAISS retrieval"
}

def expand_query(
    query
):

    query_lower = query.lower()

    expanded = query

    for key, value in QUERY_EXPANSIONS.items():

        if key in query_lower:

            expanded += " " + value

    return expanded

from langchain_community.vectorstores import (
    FAISS
)

from langchain_community.embeddings import (
    HuggingFaceEmbeddings
)


QUERY_EXPANSIONS = {

    "backend":
    "backend APIs FastAPI Python",

    "chatbot":
    "chatbot LangChain LLM",

    "search":
    "search embeddings FAISS retrieval"
}

def expand_query(
    query
):

    query_lower = query.lower()

    expanded = query

    for key, value in QUERY_EXPANSIONS.items():

        if key in query_lower:

            expanded += " " + value

    return expanded


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

    expanded_query = expand_query(
        question
    )

    print(
        "\nExpanded Query:"
    )

    print(
        expanded_query
    )

    docs = vectorstore.similarity_search(
        expanded_query,
        k=3
    )

    print(
        "\nRetrieved Chunks:\n"
    )

    for doc in docs:

        print(
            doc.page_content
        )

        print(
            "-"*40
        )