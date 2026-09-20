# ============================================================
# DAY 79
# GGUF, GPTQ, AWQ & LOCAL LLM INFERENCE OPTIMIZATION
# ============================================================

import json
import os
import time

import requests


# ============================================================
# CONFIGURATION
# ============================================================

OLLAMA_URL = "http://localhost:11434/api/generate"

MODEL_NAME = "llama3.2"

PROMPT = (
    "Explain the difference between model quantization "
    "and model fine-tuning in simple terms."
)

OUTPUT_DIR = "results"
OUTPUT_FILE = os.path.join(
    OUTPUT_DIR,
    "benchmark.json"
)


# ============================================================
# CHECK OLLAMA
# ============================================================

def check_ollama():

    try:

        response = requests.get(
            "http://localhost:11434/api/tags",
            timeout=5
        )

        response.raise_for_status()

        return True

    except requests.RequestException:

        return False


# ============================================================
# CHECK MODEL
# ============================================================

def check_model():

    response = requests.get(
        "http://localhost:11434/api/tags",
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

    models = data.get("models", [])

    available_models = [
        model.get("name", "")
        for model in models
    ]

    return available_models


# ============================================================
# RUN INFERENCE
# ============================================================

def run_inference():

    payload = {
        "model": MODEL_NAME,
        "prompt": PROMPT,
        "stream": False,
        "options": {
            "temperature": 0.0
        }
    }

    start_time = time.perf_counter()

    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=300
    )

    end_time = time.perf_counter()

    response.raise_for_status()

    result = response.json()

    elapsed = end_time - start_time

    return result, elapsed


# ============================================================
# CALCULATE METRICS
# ============================================================

def calculate_metrics(
    result,
    elapsed
):

    eval_count = result.get(
        "eval_count",
        0
    )

    prompt_eval_count = result.get(
        "prompt_eval_count",
        0
    )

    if elapsed > 0 and eval_count:

        tokens_per_second = (
            eval_count / elapsed
        )

    else:

        tokens_per_second = 0

    return {
        "elapsed_seconds": round(
            elapsed,
            3
        ),
        "prompt_tokens": prompt_eval_count,
        "generated_tokens": eval_count,
        "tokens_per_second": round(
            tokens_per_second,
            2
        )
    }


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 70)
    print("DAY 79 — LOCAL LLM INFERENCE BENCHMARK")
    print("=" * 70)

    print(f"\nModel: {MODEL_NAME}")

    # --------------------------------------------------------
    # Check Ollama
    # --------------------------------------------------------

    print("\nChecking Ollama...")

    if not check_ollama():

        print(
            "\nERROR: Ollama is not running."
        )

        print(
            "Start Ollama and run this program again."
        )

        return

    print("Ollama is running.")

    # --------------------------------------------------------
    # Check available models
    # --------------------------------------------------------

    print("\nChecking available models...")

    try:

        available_models = check_model()

    except requests.RequestException as error:

        print(
            f"Could not retrieve models: {error}"
        )

        return

    print("\nAvailable models:")

    for model in available_models:

        print(f"  - {model}")

    # --------------------------------------------------------
    # Check requested model
    # --------------------------------------------------------

    if MODEL_NAME not in available_models:

        matching_model = any(
            model.startswith(MODEL_NAME + ":")
            for model in available_models
        )

        if not matching_model:

            print(
                f"\nModel '{MODEL_NAME}' "
                "was not found."
            )

            print(
                f"Run: ollama pull {MODEL_NAME}"
            )

            return

    # --------------------------------------------------------
    # Run inference
    # --------------------------------------------------------

    print("\nPrompt:")
    print(PROMPT)

    print("\nRunning inference...")

    try:

        result, elapsed = run_inference()

    except requests.RequestException as error:

        print(
            f"\nInference failed: {error}"
        )

        return

    # --------------------------------------------------------
    # Calculate metrics
    # --------------------------------------------------------

    metrics = calculate_metrics(
        result,
        elapsed
    )

    answer = result.get(
        "response",
        ""
    )

    # --------------------------------------------------------
    # Display output
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("MODEL RESPONSE")
    print("=" * 70)

    print(answer)

    print("\n" + "=" * 70)
    print("INFERENCE METRICS")
    print("=" * 70)

    print(
        f"Elapsed time: "
        f"{metrics['elapsed_seconds']} seconds"
    )

    print(
        f"Prompt tokens: "
        f"{metrics['prompt_tokens']}"
    )

    print(
        f"Generated tokens: "
        f"{metrics['generated_tokens']}"
    )

    print(
        f"Tokens/second: "
        f"{metrics['tokens_per_second']}"
    )

    # --------------------------------------------------------
    # Save result
    # --------------------------------------------------------

    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True
    )

    benchmark = {
        "model": MODEL_NAME,
        "prompt": PROMPT,
        "response": answer,
        "metrics": metrics
    }

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            benchmark,
            file,
            indent=4,
            ensure_ascii=False
        )

    print(
        f"\nBenchmark saved to: "
        f"{OUTPUT_FILE}"
    )

    print("\nBenchmark completed.")


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()