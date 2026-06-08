from langchain_community.vectorstores import (
    FAISS
)

from langchain_community.embeddings import (
    HuggingFaceEmbeddings
)

from langchain_ollama import (
    ChatOllama
)

from langchain_core.prompts import (
    ChatPromptTemplate
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

retriever = vectorstore.as_retriever(
    search_kwargs={
        "k":3
    }
)

llm = ChatOllama(
    model="llama3.2"
)

prompt = ChatPromptTemplate.from_template(
    """
You are an AI Knowledge Assistant.

Answer using ONLY the retrieved context.

Context:
{context}

Question:
{question}
"""
)

print(
    "\nAI Knowledge Base Assistant Started\n"
)

while True:

    question = input(
        "\nQuestion: "
    )

    if question.lower() == "exit":
        break

    docs = retriever.invoke(
        question
    )

    context = "\n".join(

        doc.page_content

        for doc in docs
    )

    print(
        "\nRetrieved Sources:"
    )

    for i, doc in enumerate(
        docs,
        start=1
    ):

        print(
            f"\n{i}.",
            doc.page_content
        )

    chain = prompt | llm

    response = chain.invoke(
        {
            "context": context,
            "question": question
        }
    )

    print(
        "\nAnswer:\n"
    )

    print(
        response.content
    )