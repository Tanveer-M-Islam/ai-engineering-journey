from langchain_community.vectorstores import FAISS

from langchain_community.embeddings import (
    HuggingFaceEmbeddings
)

from langchain_ollama import ChatOllama

from langchain_core.prompts import (
    ChatPromptTemplate
)


embedding_model = (
    HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
)

vectorstore = FAISS.load_local(
    "faiss_index",
    embedding_model,
    allow_dangerous_deserialization=True
)

retriever = vectorstore.as_retriever(
    search_kwargs={
        "k": 3
    }
)

llm = ChatOllama(
    model="llama3.2"
)

prompt = ChatPromptTemplate.from_template(
    """
Answer using ONLY the context.

Context:
{context}

Question:
{question}
"""
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