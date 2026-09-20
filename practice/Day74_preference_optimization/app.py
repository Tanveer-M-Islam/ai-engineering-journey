import json
import math
from pathlib import Path


DATA_FILE = Path("./preference.jsonl")


def load_preferences():
    data = []

    with open(DATA_FILE, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if line:
                data.append(json.loads(line))

    return data


def simple_quality_score(text):
    """
    Educational toy score.

    This is NOT a real reward model.
    It only demonstrates the idea of assigning
    a numerical score to a response.
    """

    words = text.split()

    score = 0.0

    # Slight preference for concise responses
    if len(words) <= 35:
        score += 1.0

    # Preference for useful technical keywords
    useful_terms = [
        "data",
        "model",
        "system",
        "software",
        "information",
        "learn",
        "answer",
        "python",
    ]

    for word in words:
        if word.lower().strip(".,!?") in useful_terms:
            score += 0.1

    return score


def analyze_preferences(data):

    print("\n" + "=" * 70)
    print("DAY 74 - PREFERENCE OPTIMIZATION DEMO")
    print("=" * 70)

    for i, item in enumerate(data, start=1):

        chosen_score = simple_quality_score(item["chosen"])
        rejected_score = simple_quality_score(item["rejected"])

        print(f"\nExample {i}")
        print("-" * 70)

        print("Prompt:")
        print(item["prompt"])

        print(f"\nChosen score:   {chosen_score:.2f}")
        print(f"Rejected score: {rejected_score:.2f}")

        if chosen_score > rejected_score:
            print("Toy evaluator prefers: CHOSEN")
        elif rejected_score > chosen_score:
            print("Toy evaluator prefers: REJECTED")
        else:
            print("Toy evaluator: TIE")


def preference_margin(chosen_score, rejected_score):
    return chosen_score - rejected_score


if __name__ == "__main__":

    if not DATA_FILE.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATA_FILE}"
        )

    preferences = load_preferences()

    analyze_preferences(preferences)

    print("\n" + "=" * 70)
    print("IMPORTANT")
    print("=" * 70)
    print(
        "This toy evaluator demonstrates preference scoring."
    )
    print(
        "It is NOT a real reward model or DPO implementation."
    )