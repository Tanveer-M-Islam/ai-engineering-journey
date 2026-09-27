import json
import os
import time
import uuid

import requests


# ============================================================
# CONFIGURATION
# ============================================================

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2"

RESULTS_DIR = "results"

RESULTS_FILE = os.path.join(
    RESULTS_DIR,
    "evaluation_results.json"
)

LOG_FILE = os.path.join(
    RESULTS_DIR,
    "evaluation_logs.jsonl"
)


# ============================================================
# EVALUATION DATASET
# ============================================================

TEST_CASES = [
    {
        "question": "What does LLM stand for?",
        "expected_answer": "Large Language Model"
    },
    {
        "question": "What does RAG stand for?",
        "expected_answer": "Retrieval-Augmented Generation"
    },
    {
        "question": "What does API stand for?",
        "expected_answer": "Application Programming Interface"
    },
    {
        "question": "What does GPU stand for?",
        "expected_answer": "Graphics Processing Unit"
    },
    {
        "question": "What does NLP stand for?",
        "expected_answer": "Natural Language Processing"
    }
]


# ============================================================
# OLLAMA REQUEST
# ============================================================

def call_llm(question):

    prompt = f"""
Answer the following question directly and briefly.

Question:
{question}

Answer:
"""

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0
        }
    }

    start_time = time.perf_counter()

    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=120
    )

    response.raise_for_status()

    latency = time.perf_counter() - start_time

    data = response.json()

    return data, latency


# ============================================================
# SIMPLE QUALITY EVALUATION
# ============================================================

def normalize_text(text):

    return (
        text
        .lower()
        .strip()
        .replace(".", "")
        .replace(",", "")
        .replace("-", " ")
    )


def evaluate_answer(expected, generated):

    expected_normalized = normalize_text(expected)
    generated_normalized = normalize_text(generated)

    passed = (
        expected_normalized
        in generated_normalized
    )

    return passed


# ============================================================
# PERFORMANCE METRICS
# ============================================================

def calculate_tokens_per_second(data):

    output_tokens = data.get(
        "eval_count",
        0
    )

    eval_duration_ns = data.get(
        "eval_duration",
        0
    )

    if eval_duration_ns <= 0:
        return 0.0

    eval_duration_seconds = (
        eval_duration_ns / 1_000_000_000
    )

    return (
        output_tokens / eval_duration_seconds
    )


# ============================================================
# STRUCTURED LOGGING
# ============================================================

def write_log(log_data):

    os.makedirs(
        RESULTS_DIR,
        exist_ok=True
    )

    with open(
        LOG_FILE,
        "a",
        encoding="utf-8"
    ) as file:

        file.write(
            json.dumps(
                log_data,
                ensure_ascii=False
            )
            + "\n"
        )


# ============================================================
# RUN SINGLE TEST
# ============================================================

def run_test(test_case):

    request_id = str(uuid.uuid4())

    question = test_case["question"]

    expected = test_case[
        "expected_answer"
    ]

    print("\n" + "=" * 60)
    print("Question:", question)

    try:

        data, latency = call_llm(question)

        generated = data.get(
            "response",
            ""
        ).strip()

        input_tokens = data.get(
            "prompt_eval_count",
            0
        )

        output_tokens = data.get(
            "eval_count",
            0
        )

        tokens_per_second = (
            calculate_tokens_per_second(data)
        )

        passed = evaluate_answer(
            expected,
            generated
        )

        result = {
            "request_id": request_id,
            "question": question,
            "expected_answer": expected,
            "generated_answer": generated,
            "passed": passed,
            "latency_seconds": round(
                latency,
                3
            ),
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "tokens_per_second": round(
                tokens_per_second,
                2
            ),
            "status": "success"
        }

        write_log(result)

        print("Expected:", expected)
        print("Generated:", generated)

        print(
            "Evaluation:",
            "PASS" if passed else "FAIL"
        )

        print(
            "Latency:",
            result["latency_seconds"],
            "seconds"
        )

        print(
            "Input tokens:",
            input_tokens
        )

        print(
            "Output tokens:",
            output_tokens
        )

        print(
            "Generation speed:",
            result["tokens_per_second"],
            "tokens/sec"
        )

        return result

    except Exception as error:

        result = {
            "request_id": request_id,
            "question": question,
            "expected_answer": expected,
            "generated_answer": None,
            "passed": False,
            "status": "error",
            "error": str(error)
        }

        write_log(result)

        print(
            "ERROR:",
            error
        )

        return result


# ============================================================
# CALCULATE SUMMARY
# ============================================================

def calculate_summary(results):

    total_tests = len(results)

    successful_requests = sum(
        1
        for result in results
        if result["status"] == "success"
    )

    failed_requests = (
        total_tests - successful_requests
    )

    passed_tests = sum(
        1
        for result in results
        if result.get("passed", False)
    )

    quality_score = (
        passed_tests / total_tests
        if total_tests
        else 0
    )

    error_rate = (
        failed_requests / total_tests
        if total_tests
        else 0
    )

    successful_results = [
        result
        for result in results
        if result["status"] == "success"
    ]

    if successful_results:

        average_latency = sum(
            result["latency_seconds"]
            for result in successful_results
        ) / len(successful_results)

        average_tokens_per_second = sum(
            result["tokens_per_second"]
            for result in successful_results
        ) / len(successful_results)

        total_input_tokens = sum(
            result["input_tokens"]
            for result in successful_results
        )

        total_output_tokens = sum(
            result["output_tokens"]
            for result in successful_results
        )

    else:

        average_latency = 0
        average_tokens_per_second = 0
        total_input_tokens = 0
        total_output_tokens = 0

    return {
        "total_tests": total_tests,
        "passed_tests": passed_tests,
        "failed_quality_tests": (
            total_tests - passed_tests
        ),
        "quality_score_percent": round(
            quality_score * 100,
            2
        ),
        "successful_requests": successful_requests,
        "failed_requests": failed_requests,
        "error_rate_percent": round(
            error_rate * 100,
            2
        ),
        "average_latency_seconds": round(
            average_latency,
            3
        ),
        "average_tokens_per_second": round(
            average_tokens_per_second,
            2
        ),
        "total_input_tokens": total_input_tokens,
        "total_output_tokens": total_output_tokens
    }


# ============================================================
# SAVE FINAL RESULTS
# ============================================================

def save_results(results, summary):

    os.makedirs(
        RESULTS_DIR,
        exist_ok=True
    )

    output = {
        "model": MODEL_NAME,
        "summary": summary,
        "results": results
    }

    with open(
        RESULTS_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            output,
            file,
            indent=4,
            ensure_ascii=False
        )


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 60)
    print("DAY 93 - LLM EVALUATION & OBSERVABILITY")
    print("=" * 60)

    results = []

    for test_case in TEST_CASES:

        result = run_test(
            test_case
        )

        results.append(result)

    summary = calculate_summary(
        results
    )

    save_results(
        results,
        summary
    )

    print("\n")
    print("=" * 60)
    print("FINAL SUMMARY")
    print("=" * 60)

    print(
        "Tests:",
        summary["total_tests"]
    )

    print(
        "Passed:",
        summary["passed_tests"]
    )

    print(
        "Quality Score:",
        f"{summary['quality_score_percent']}%"
    )

    print(
        "Error Rate:",
        f"{summary['error_rate_percent']}%"
    )

    print(
        "Average Latency:",
        summary["average_latency_seconds"],
        "seconds"
    )

    print(
        "Average Generation Speed:",
        summary["average_tokens_per_second"],
        "tokens/sec"
    )

    print(
        "Total Input Tokens:",
        summary["total_input_tokens"]
    )

    print(
        "Total Output Tokens:",
        summary["total_output_tokens"]
    )

    print(
        "\nResults saved to:",
        RESULTS_FILE
    )

    print(
        "Logs saved to:",
        LOG_FILE
    )


if __name__ == "__main__":
    main()