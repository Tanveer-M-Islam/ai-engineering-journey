from langchain_ollama import (
    ChatOllama
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


# ==========================
# Model
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

            "You are a helpful AI tutor."
        ),

        MessagesPlaceholder(
            variable_name="history"
        ),

        (
            "human",

            "{question}"
        )
    ]
)


# ==========================
# Parser
# ==========================

parser = StrOutputParser()


# ==========================
# Chain
# ==========================

chain = (

    prompt

    |

    model

    |

    parser
)


# ==========================
# Session Storage
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


# ==========================
# Memory Chain
# ==========================

memory_chain = (

    RunnableWithMessageHistory(

        chain,

        get_session_history,

        input_messages_key="question",

        history_messages_key="history"
    )
)


# ==========================
# Chat Loop
# ==========================

print(
    "Type 'exit' to quit.\n"
)

while True:

    question = input(
        "You: "
    )

    if question.lower() == "exit":

        break

    answer = memory_chain.invoke(

        {
            "question": question
        },

        config={

            "configurable": {

                "session_id": "user1"
            }
        }
    )

    print(
        "\nAI:",
        answer
    )

    print()