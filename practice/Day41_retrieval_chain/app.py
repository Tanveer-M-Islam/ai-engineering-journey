from langchain_community.document_loaders import (
    TextLoader
)

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)

from langchain_community.vectorstores import (
    FAISS
)

from langchain_community.embeddings import (
    HuggingFaceEmbeddings
)

from langchain_core.prompts import (
    ChatPromptTemplate
)

from langchain_core.output_parsers import (
    StrOutputParser
)

from langchain_ollama import (
    ChatOllama
)


# ==========================
# Load Documents
# ==========================

loader = TextLoader(
    "knowledge.txt"
)

documents = loader.load()


# ==========================
# Split Documents
# ==========================

splitter = RecursiveCharacterTextSplitter(

    chunk_size=200,

    chunk_overlap=20
)

chunks = splitter.split_documents(
    documents
)


# ==========================
# Embeddings
# ==========================

embedding_model = (
    HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )
)


# ==========================
# Vector Store
# ==========================

vectorstore = FAISS.from_documents(

    chunks,

    embedding_model
)

vectorstore.save_local(
    "faiss_index"
)



# ==========================
# Retriever
# ==========================

retriever = vectorstore.as_retriever(

    search_kwargs={
        "k": 3
    }
)


# ==========================
# Model
# ==========================

model = ChatOllama(
    model="llama3.2"
)


# ==========================
# Prompt
# ==========================

prompt = ChatPromptTemplate.from_template(
    """
You are a helpful AI assistant.

Use the retrieved context as the primary source
for your answer.

If the context contains the answer:

1. Answer using the context.
2. You may provide additional explanation.
3. Clearly stay consistent with the context.
4. Do not contradict the context.

Context:
{context}

Question:
{question}

Answer:
"""
)


# ==========================
# Parser
# ==========================

parser = StrOutputParser()


# ==========================
# Chat Loop
# ==========================

while True:

    question = input(
        "\nQuestion: "
    )

    if question.lower() == "exit":

        break

    docs = retriever.invoke(
        question
    )

    context = "\n\n".join(

        doc.page_content

        for doc in docs
    )

    chain = (

        prompt

        |

        model

        |

        parser
    )

    answer = chain.invoke(

        {
            "context": context,

            "question": question
        }
    )

    print(
        "\nAnswer:\n"
    )

    print(
        answer
    )