import json
import os
import requests


# ============================================================
# CONFIGURATION
# ============================================================

OLLAMA_URL = "http://localhost:11434/api/generate"

MODEL_NAME = "llama3.2"

RESULTS_DIR = "results"

os.makedirs(RESULTS_DIR, exist_ok=True)


# ============================================================
# TEST CASES
# ============================================================

TEST_CASES = [
    {
        "id": 1,
        "question": "When was Python first released?",
        "context": (
            "Python was first released in 1991. "
            "It was created by Guido van Rossum."
        ),
        "answer": (
            "Python was first released in 1991."
        )
    },

    {
        "id": 2,
        "question": "Who created Python?",
        "context": (
            "Python was created by Guido van Rossum "
            "and first released in 1991."
        ),
        "answer": (
            "Python was created by Dennis Ritchie."
        )
    },

    {
        "id": 3,
        "question": "What is the capital of France?",
        "context": (
            "France is a country in Western Europe. "
            "Its capital city is Paris."
        ),
        "answer": (
            "The capital of France is Paris."
        )
    },

    {
        "id": 4,
        "question": "What programming language is discussed?",
        "context": (
            "Python is a high-level programming language "
            "used in artificial intelligence and data science."
        ),
        "answer": (
            "The document discusses Java."
        )
    }
]


# ============================================================
# OLLAMA REQUEST
# ============================================================

def ask_ollama(prompt):

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0
        }
    }

    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=120
    )

    response.raise_for_status()

    data = response.json()

    return data["response"]


# ============================================================
# HALLUCINATION EVALUATION
# ============================================================

def evaluate_answer(question, context, answer):

    prompt = f"""
You are an LLM hallucination evaluator.

Your task is to determine whether the ANSWER is supported
by the CONTEXT.

Rules:

1. If the answer is directly supported by the context,
   return SUPPORTED.

2. If the answer contradicts the context or introduces
   unsupported information, return UNSUPPORTED.

3. Do not use outside knowledge.

4. Return exactly one label:
   SUPPORTED
   or
   UNSUPPORTED

Question:
{question}

Context:
{context}

Answer:
{answer}

Label:
"""

    result = ask_ollama(prompt)

    result = result.strip().upper()

    if "SUPPORTED" in result and "UNSUPPORTED" not in result:
        label = "SUPPORTED"
    else:
        label = "UNSUPPORTED"

    return label


# ============================================================
# RUN EVALUATION
# ============================================================

def main():

    print("=" * 60)
    print("HALLUCINATION DETECTION EVALUATION")
    print("=" * 60)

    results = []

    supported_count = 0
    unsupported_count = 0

    for test in TEST_CASES:

        print("\n" + "-" * 60)

        print(f"Test Case: {test['id']}")
        print(f"Question: {test['question']}")
        print(f"Answer: {test['answer']}")

        label = evaluate_answer(
            test["question"],
            test["context"],
            test["answer"]
        )

        print(f"Evaluation: {label}")

        if label == "SUPPORTED":
            supported_count += 1
        else:
            unsupported_count += 1

        results.append({
            "id": test["id"],
            "question": test["question"],
            "context": test["context"],
            "answer": test["answer"],
            "evaluation": label
        })


    # ========================================================
    # SUMMARY
    # ========================================================

    total = len(TEST_CASES)

    supported_rate = (
        supported_count / total
    ) * 100

    unsupported_rate = (
        unsupported_count / total
    ) * 100


    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)

    print(f"Total cases:       {total}")
    print(f"Supported:         {supported_count}")
    print(f"Unsupported:       {unsupported_count}")
    print(f"Supported rate:    {supported_rate:.2f}%")
    print(f"Unsupported rate:  {unsupported_rate:.2f}%")


    # ========================================================
    # SAVE RESULTS
    # ========================================================

    output = {
        "model": MODEL_NAME,
        "total_cases": total,
        "supported": supported_count,
        "unsupported": unsupported_count,
        "supported_rate": round(supported_rate, 2),
        "unsupported_rate": round(unsupported_rate, 2),
        "cases": results
    }

    output_path = os.path.join(
        RESULTS_DIR,
        "hallucination_results.json"
    )

    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            output,
            file,
            indent=4,
            ensure_ascii=False
        )

    print(f"\nResults saved to: {output_path}")


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()