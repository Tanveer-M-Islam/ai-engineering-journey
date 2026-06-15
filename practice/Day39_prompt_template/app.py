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
# Model
# ==========================

model = ChatOllama(
    model="llama3.2"
)

parser = StrOutputParser()


# ==========================
# Explain Chain
# ==========================

explain_prompt = (
    ChatPromptTemplate.from_template(
        """
        Explain the following topic
        in beginner friendly language.

        Topic:
        {topic}
        """
    )
)

explain_chain = (

    explain_prompt

    |

    model

    |

    parser
)


# ==========================
# Interview Chain
# ==========================

interview_prompt = (
    ChatPromptTemplate.from_template(
        """
        Generate 5 interview questions
        about:

        {topic}
        """
    )
)

interview_chain = (

    interview_prompt

    |

    model

    |

    parser
)


# ==========================
# Quiz Chain
# ==========================

quiz_prompt = (
    ChatPromptTemplate.from_template(
        """
        Create 5 quiz questions
        about:

        {topic}
        """
    )
)

quiz_chain = (

    quiz_prompt

    |

    model

    |

    parser
)


# ==========================
# Main Loop
# ==========================

while True:

    print(
        "\n1. Explain Topic"
    )

    print(
        "2. Interview Questions"
    )

    print(
        "3. Quiz Questions"
    )

    print(
        "4. Exit"
    )

    choice = input(
        "\nChoose: "
    )

    if choice == "4":

        break

    topic = input(
        "\nTopic: "
    )

    if choice == "1":

        result = explain_chain.invoke(

            {
                "topic": topic
            }
        )

    elif choice == "2":

        result = interview_chain.invoke(

            {
                "topic": topic
            }
        )

    elif choice == "3":

        result = quiz_chain.invoke(

            {
                "topic": topic
            }
        )

    else:

        print(
            "Invalid choice."
        )

        continue

    print(
        "\nResult:\n"
    )

    print(
        result
    )