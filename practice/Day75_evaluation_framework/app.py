import json
from pathlib import Path


DATA_FILE = Path("./evaluation.jsonl")


def load_data():
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def word_overlap(reference, response):
    reference_words = set(
        reference.lower().split()
    )

    response_words = set(
        response.lower().split()
    )

    if not reference_words:
        return 0.0

    overlap = reference_words.intersection(response_words)

    return len(overlap) / len(reference_words)


def evaluate_example(example):

    score = word_overlap(
        example["reference"],
        example["response"]
    )

    return score


def run_evaluation(data):

    scores = []

    print("\n" + "=" * 70)
    print("DAY 75 - LLM EVALUATION")
    print("=" * 70)

    for index, example in enumerate(data, start=1):

        score = evaluate_example(example)

        scores.append(score)

        print(f"\nExample {index}")
        print("-" * 70)

        print("Question:")
        print(example["question"])

        print("\nReference:")
        print(example["reference"])

        print("\nModel response:")
        print(example["response"])

        print(f"\nOverlap score: {score:.2f}")

    return scores


if __name__ == "__main__":

    if not DATA_FILE.exists():
        raise FileNotFoundError(
            f"Evaluation file not found: {DATA_FILE}"
        )

    data = load_data()

    scores = run_evaluation(data)

    average_score = sum(scores) / len(scores)

    print("\n" + "=" * 70)
    print("FINAL RESULT")
    print("=" * 70)

    print(f"Average overlap score: {average_score:.2f}")

    print("\nNote:")
    print(
        "This is a simple educational metric."
    )
    print(
        "It does NOT represent a complete LLM evaluation."
    )