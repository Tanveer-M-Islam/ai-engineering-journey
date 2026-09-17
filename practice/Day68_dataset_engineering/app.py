import json
import os
import re
import hashlib
from collections import Counter


# ============================================================
# CONFIGURATION
# ============================================================

INPUT_FILE = "data/raw_dataset.jsonl"
OUTPUT_DIR = "outputs"
OUTPUT_FILE = os.path.join(
    OUTPUT_DIR,
    "cleaned_dataset.jsonl",
)

MIN_INSTRUCTION_LENGTH = 5
MIN_RESPONSE_LENGTH = 10


# ============================================================
# CREATE OUTPUT DIRECTORY
# ============================================================

os.makedirs(OUTPUT_DIR, exist_ok=True)


# ============================================================
# LOAD JSONL DATA
# ============================================================

def load_jsonl(file_path):
    records = []

    with open(
        file_path,
        "r",
        encoding="utf-8",
    ) as file:

        for line_number, line in enumerate(file, start=1):

            line = line.strip()

            if not line:
                continue

            try:
                record = json.loads(line)
                records.append(record)

            except json.JSONDecodeError:
                print(
                    f"Skipping invalid JSON at line {line_number}"
                )

    return records


# ============================================================
# TEXT NORMALIZATION
# ============================================================

def normalize_text(text):
    if not isinstance(text, str):
        return ""

    text = text.strip()

    text = re.sub(
        r"\s+",
        " ",
        text,
    )

    return text


# ============================================================
# RECORD CLEANING
# ============================================================

def clean_record(record):
    instruction = normalize_text(
        record.get("instruction", "")
    )

    response = normalize_text(
        record.get("response", "")
    )

    if len(instruction) < MIN_INSTRUCTION_LENGTH:
        return None

    if len(response) < MIN_RESPONSE_LENGTH:
        return None

    return {
        "instruction": instruction,
        "response": response,
    }


# ============================================================
# DUPLICATE KEY
# ============================================================

def record_hash(record):
    combined_text = (
        record["instruction"]
        + "|||"
        + record["response"]
    )

    return hashlib.md5(
        combined_text.encode("utf-8")
    ).hexdigest()


# ============================================================
# DEDUPLICATION
# ============================================================

def deduplicate_records(records):
    unique_records = []
    seen_hashes = set()

    for record in records:

        current_hash = record_hash(record)

        if current_hash in seen_hashes:
            continue

        seen_hashes.add(current_hash)
        unique_records.append(record)

    return unique_records


# ============================================================
# SAVE JSONL
# ============================================================

def save_jsonl(records, file_path):
    with open(
        file_path,
        "w",
        encoding="utf-8",
    ) as file:

        for record in records:
            file.write(
                json.dumps(
                    record,
                    ensure_ascii=False,
                )
                + "\n"
            )


# ============================================================
# DATASET STATISTICS
# ============================================================

def show_statistics(records, title):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)

    print(f"Number of records: {len(records)}")

    if not records:
        return

    instruction_lengths = [
        len(record["instruction"])
        for record in records
    ]

    response_lengths = [
        len(record["response"])
        for record in records
    ]

    print(
        "Average instruction length:",
        round(
            sum(instruction_lengths)
            / len(instruction_lengths),
            2,
        ),
    )

    print(
        "Average response length:",
        round(
            sum(response_lengths)
            / len(response_lengths),
            2,
        ),
    )

    print(
        "Minimum instruction length:",
        min(instruction_lengths),
    )

    print(
        "Maximum instruction length:",
        max(instruction_lengths),
    )

    print(
        "Minimum response length:",
        min(response_lengths),
    )

    print(
        "Maximum response length:",
        max(response_lengths),
    )


# ============================================================
# MAIN PIPELINE
# ============================================================

def main():

    print("=" * 60)
    print("DAY 68 - LLM DATASET ENGINEERING")
    print("=" * 60)

    raw_records = load_jsonl(INPUT_FILE)

    show_statistics(
        raw_records,
        "RAW DATASET STATISTICS",
    )

    cleaned_records = []

    for record in raw_records:

        cleaned_record = clean_record(record)

        if cleaned_record is not None:
            cleaned_records.append(cleaned_record)

    show_statistics(
        cleaned_records,
        "AFTER CLEANING",
    )

    unique_records = deduplicate_records(
        cleaned_records
    )

    show_statistics(
        unique_records,
        "AFTER DEDUPLICATION",
    )

    save_jsonl(
        unique_records,
        OUTPUT_FILE,
    )

    print("\nCleaned dataset saved to:")
    print(OUTPUT_FILE)

    print("\nFinal records:")

    for index, record in enumerate(
        unique_records,
        start=1,
    ):
        print(f"\nRecord {index}")
        print("Instruction:", record["instruction"])
        print("Response:", record["response"])

    print("\n" + "=" * 60)
    print("DATASET ENGINEERING COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    main()