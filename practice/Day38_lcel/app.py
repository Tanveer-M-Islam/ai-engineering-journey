from langchain_core.prompts import (
    ChatPromptTemplate
)

from langchain_core.output_parsers import (
    StrOutputParser
)

from langchain_ollama import (
    ChatOllama
)


# =====================
# Model
# =====================

model = ChatOllama(
    model="llama3.2"
)


# =====================
# Prompt
# =====================

prompt = ChatPromptTemplate.from_template(

    """
    You are an AI Engineering tutor.

    Explain the topic below
    in beginner-friendly language.

    Topic:
    {topic}
    """
)

quiz_prompt = ChatPromptTemplate.from_template(

    """
    Create 3 interview questions
    about:

    {topic}
    """
)

# =====================
# Parser
# =====================

parser = StrOutputParser()


# =====================
# LCEL Chain
# =====================

study_chain = (

    prompt

    |

    model

    |

    parser
)

quiz_chain = (

    quiz_prompt

    |

    model

    |

    parser
)

# =====================
# Chat Loop
# =====================

while True:

    topic = input(
        "\nTopic: "
    )

    if topic.lower() == "exit":

        break

    answer = study_chain.invoke(

        {
            "topic": topic
        }
    )

    print(
        "\nAnswer:\n"
    )

    print(
        answer
    )