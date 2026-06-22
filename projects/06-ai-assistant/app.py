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
    ChatPromptTemplate,
    MessagesPlaceholder
)

from langchain_core.chat_history import (
    InMemoryChatMessageHistory
)

from langchain_core.runnables.history import (
    RunnableWithMessageHistory
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

    chunk_size=300,

    chunk_overlap=50
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


retriever = (
    vectorstore.as_retriever(
        search_kwargs={"k": 1}
    )
)


# ==========================
# LLM
# ==========================

model = ChatOllama(
    model="llama3.2"
)


# ==========================
# Prompt
# ==========================

prompt = ChatPromptTemplate.from_messages(

    [

        (
            "system",

            """
You are an AI Engineering tutor.

Use the retrieved context as the
primary source of truth.

If the answer exists in the context:

1. Answer using the context.
2. Provide additional explanation.
3. Stay consistent with the context.

If the answer does not exist:

Say:
'I could not find this information
in the knowledge base.'
"""
        ),

        MessagesPlaceholder(
            variable_name="history"
        ),

        (
            "human",

            """
Context:

{context}

Question:

{question}
"""
        )
    ]
)


# ==========================
# Parser
# ==========================

parser = StrOutputParser()


# ==========================
# Base Chain
# ==========================

base_chain = (

    prompt

    |

    model

    |

    parser
)


# ==========================
# Memory
# ==========================

store = {}


def get_session_history(
    session_id
):

    if session_id not in store:

        store[
            session_id
        ] = (
            InMemoryChatMessageHistory()
        )

    return store[
        session_id
    ]


memory_chain = (
    RunnableWithMessageHistory(

        base_chain,

        get_session_history,

        input_messages_key="question",

        history_messages_key="history"
    )
)


# ==========================
# Chat Loop
# ==========================

print(
    "AI Engineering Knowledge Assistant"
)

print(
    "Type 'exit' to quit.\n"
)


while True:

    question = input(
        "Question: "
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

    answer = memory_chain.invoke(

        {

            "question": question,

            "context": context
        },

        config={

            "configurable": {

                "session_id": "user1"
            }
        }
    )

    print(
        "\nAnswer:\n"
    )

    print(
        answer
    )

    print(
        "\nSources:"
    )

    for i, doc in enumerate(
    docs,
    start=1
   ):

     title = doc.page_content.split("\n")[0]

    print(
        f"{i}. {title}"
    )

    print()