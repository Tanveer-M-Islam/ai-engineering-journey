import json
import os
import time

import requests


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2"

RESULTS_DIR = "results"
RESULTS_FILE = os.path.join(
    RESULTS_DIR,
    "benchmark_results.json"
)


TEST_CONFIGS = [
    {
        "name": "short_output",
        "prompt": "Explain RAG in one short sentence.",
        "num_predict": 50,
    },
    {
        "name": "medium_output",
        "prompt": "Explain RAG clearly in one short paragraph.",
        "num_predict": 150,
    },
    {
        "name": "long_output",
        "prompt": (
            "Explain retrieval augmented generation in detail, "
            "including retrieval, embeddings, vector databases, "
            "context construction, generation, advantages, "
            "limitations, and common use cases."
        ),
        "num_predict": 400,
    },
]


def call_ollama(prompt, num_predict):
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0,
            "num_predict": num_predict,
        },
    }

    start_time = time.perf_counter()

    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=300,
    )

    response.raise_for_status()

    end_time = time.perf_counter()

    data = response.json()

    return data, end_time - start_time


def safe_ns_to_seconds(value):
    if not value:
        return 0.0

    return value / 1_000_000_000


def calculate_metrics(data, measured_latency):
    prompt_tokens = data.get(
        "prompt_eval_count",
        0
    )

    output_tokens = data.get(
        "eval_count",
        0
    )

    prompt_duration = safe_ns_to_seconds(
        data.get("prompt_eval_duration", 0)
    )

    generation_duration = safe_ns_to_seconds(
        data.get("eval_duration", 0)
    )

    total_duration = safe_ns_to_seconds(
        data.get("total_duration", 0)
    )

    load_duration = safe_ns_to_seconds(
        data.get("load_duration", 0)
    )

    if generation_duration > 0:
        tokens_per_second = (
            output_tokens / generation_duration
        )
    else:
        tokens_per_second = 0

    return {
        "prompt_tokens": prompt_tokens,
        "output_tokens": output_tokens,
        "measured_latency_seconds": round(
            measured_latency,
            3
        ),
        "ollama_total_seconds": round(
            total_duration,
            3
        ),
        "model_load_seconds": round(
            load_duration,
            3
        ),
        "prompt_processing_seconds": round(
            prompt_duration,
            3
        ),
        "generation_seconds": round(
            generation_duration,
            3
        ),
        "generation_tokens_per_second": round(
            tokens_per_second,
            2
        ),
    }


def run_benchmark(config):
    print("\n" + "=" * 60)
    print("TEST:", config["name"])
    print("=" * 60)

    print(
        "Maximum output tokens:",
        config["num_predict"]
    )

    data, latency = call_ollama(
        config["prompt"],
        config["num_predict"]
    )

    metrics = calculate_metrics(
        data,
        latency
    )

    result = {
        "test_name": config["name"],
        "model": MODEL_NAME,
        "prompt": config["prompt"],
        "max_output_tokens": config["num_predict"],
        **metrics,
        "response": data.get(
            "response",
            ""
        ).strip(),
    }

    print(
        "Prompt tokens:",
        result["prompt_tokens"]
    )

    print(
        "Output tokens:",
        result["output_tokens"]
    )

    print(
        "Latency:",
        result["measured_latency_seconds"],
        "seconds"
    )

    print(
        "Generation speed:",
        result["generation_tokens_per_second"],
        "tokens/sec"
    )

    return result


def print_summary(results):
    print("\n")
    print("=" * 70)
    print("BENCHMARK SUMMARY")
    print("=" * 70)

    print(
        f"{'TEST':<20}"
        f"{'INPUT':<10}"
        f"{'OUTPUT':<10}"
        f"{'LATENCY':<12}"
        f"{'TOK/S':<10}"
    )

    print("-" * 70)

    for result in results:
        print(
            f"{result['test_name']:<20}"
            f"{result['prompt_tokens']:<10}"
            f"{result['output_tokens']:<10}"
            f"{result['measured_latency_seconds']:<12}"
            f"{result['generation_tokens_per_second']:<10}"
        )


def save_results(results):
    os.makedirs(
        RESULTS_DIR,
        exist_ok=True
    )

    with open(
        RESULTS_FILE,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            results,
            file,
            indent=4,
            ensure_ascii=False
        )

    print(
        "\nResults saved to:",
        RESULTS_FILE
    )


def main():
    print("=" * 60)
    print("DAY 94 - ADVANCED LLM OPTIMIZATION")
    print("=" * 60)

    results = []

    try:
        for config in TEST_CONFIGS:
            result = run_benchmark(config)
            results.append(result)

        print_summary(results)

        save_results(results)

    except requests.exceptions.ConnectionError:
        print(
            "\nERROR: Cannot connect to Ollama."
        )

        print(
            "Make sure Ollama is running."
        )

    except requests.exceptions.Timeout:
        print(
            "\nERROR: Ollama request timed out."
        )

    except Exception as error:
        print(
            "\nERROR:",
            error
        )


if __name__ == "__main__":
    main()