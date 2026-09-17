import json
import os

from transformers import AutoTokenizer


MODEL_NAME = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

INPUT_FILE = "data/instruction_dataset.jsonl"
OUTPUT_FILE = "outputs/formatted_chat_dataset.jsonl"


def load_jsonl(file_path):
    """
    Load JSONL records from disk.
    """

    records = []

    if not os.path.exists(file_path):
        raise FileNotFoundError(
            f"Input file not found: {file_path}"
        )

    with open(file_path, "r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            line = line.strip()

            if not line:
                continue

            try:
                records.append(json.loads(line))

            except json.JSONDecodeError as error:
                print(
                    f"Skipping invalid JSON at line {line_number}: {error}"
                )

    return records


def convert_to_messages(record):
    """
    Convert instruction-response format into chat messages.
    """

    instruction = record.get("instruction", "").strip()
    response = record.get("response", "").strip()

    messages = [
        {
            "role": "system",
            "content": "You are a helpful AI assistant."
        },
        {
            "role": "user",
            "content": instruction
        },
        {
            "role": "assistant",
            "content": response
        }
    ]

    return messages


def format_with_chat_template(tokenizer, messages):
    """
    Apply the tokenizer's official chat template.
    """

    if tokenizer.chat_template is None:
        raise ValueError(
            "This tokenizer does not provide a chat template."
        )

    formatted_text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=False
    )

    return formatted_text


def save_jsonl(records, file_path):
    """
    Save records in JSONL format.
    """

    os.makedirs(
        os.path.dirname(file_path),
        exist_ok=True
    )

    with open(file_path, "w", encoding="utf-8") as file:
        for record in records:
            file.write(
                json.dumps(
                    record,
                    ensure_ascii=False
                ) + "\n"
            )


def main():
    print("Loading tokenizer...")

    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_NAME
    )

    print(f"Model: {MODEL_NAME}")
    print(f"Chat template available: {tokenizer.chat_template is not None}")

    raw_records = load_jsonl(INPUT_FILE)

    formatted_records = []

    for index, record in enumerate(raw_records, start=1):
        instruction = record.get("instruction", "").strip()
        response = record.get("response", "").strip()

        if not instruction or not response:
            print(
                f"Skipping invalid record at index {index}"
            )
            continue

        messages = convert_to_messages(record)

        formatted_text = format_with_chat_template(
            tokenizer,
            messages
        )

        formatted_records.append(
            {
                "messages": messages,
                "text": formatted_text
            }
        )

    save_jsonl(
        formatted_records,
        OUTPUT_FILE
    )

    print("\n========== RESULT ==========")
    print(f"Input records: {len(raw_records)}")
    print(f"Formatted records: {len(formatted_records)}")
    print(f"Output file: {OUTPUT_FILE}")

    if formatted_records:
        print("\n========== SAMPLE ==========")
        print(formatted_records[0]["text"])


if __name__ == "__main__":
    main()