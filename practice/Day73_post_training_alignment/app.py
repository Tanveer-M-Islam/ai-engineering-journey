import json
from pathlib import Path


DATA_FILE = Path("./preferences.jsonl")


def load_preferences():
    data = []

    with open(DATA_FILE, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if line:
                data.append(json.loads(line))

    return data


def show_examples(data):
    print("\n" + "=" * 70)
    print("DAY 73 - PREFERENCE DATA")
    print("=" * 70)

    for i, item in enumerate(data, start=1):

        print(f"\nExample {i}")
        print("-" * 70)

        print("Prompt:")
        print(item["prompt"])

        print("\nChosen:")
        print(item["chosen"])

        print("\nRejected:")
        print(item["rejected"])


if __name__ == "__main__":

    if not DATA_FILE.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATA_FILE}"
        )

    preferences = load_preferences()

    print(f"\nTotal examples: {len(preferences)}")

    show_examples(preferences)