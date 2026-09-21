# ============================================================
# DAY 80
# HIGH-PERFORMANCE LLM SERVING
# LLM SERVING SIMULATOR
# ============================================================

import json
import time
from pathlib import Path


# ============================================================
# CONFIGURATION
# ============================================================

BATCH_SIZE = 3

PROCESSING_TIME_PER_REQUEST = 0.8

REQUEST_FILE = Path("requests.json")


# ============================================================
# LOAD REQUESTS
# ============================================================

def load_requests():

    with open(
        REQUEST_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


# ============================================================
# PROCESS BATCH
# ============================================================

def process_batch(batch, batch_number):

    print("\n" + "=" * 70)
    print(f"PROCESSING BATCH {batch_number}")
    print("=" * 70)

    print(f"Batch size: {len(batch)}")

    start_time = time.perf_counter()

    for request in batch:

        print(
            f"\nProcessing: {request['id']}"
        )

        print(
            f"Prompt: {request['prompt']}"
        )

    # --------------------------------------------------------
    # Simulated GPU/model processing
    # --------------------------------------------------------

    simulated_time = (
        PROCESSING_TIME_PER_REQUEST
    )

    time.sleep(simulated_time)

    end_time = time.perf_counter()

    processing_time = (
        end_time - start_time
    )

    # --------------------------------------------------------
    # Create results
    # --------------------------------------------------------

    results = []

    for request in batch:

        results.append(
            {
                "id": request["id"],
                "processing_time": round(
                    processing_time,
                    3
                ),
                "batch_size": len(batch)
            }
        )

    return results, processing_time


# ============================================================
# SERVING SIMULATION
# ============================================================

def run_server_simulation(requests):

    print("=" * 70)
    print("DAY 80 — HIGH-PERFORMANCE LLM SERVING")
    print("=" * 70)

    print(
        f"\nTotal requests: {len(requests)}"
    )

    print(
        f"Batch size: {BATCH_SIZE}"
    )

    print(
        "\nStarting serving simulation..."
    )

    server_start = time.perf_counter()

    all_results = []

    # --------------------------------------------------------
    # Create batches
    # --------------------------------------------------------

    batches = []

    for i in range(
        0,
        len(requests),
        BATCH_SIZE
    ):

        batch = requests[
            i:i + BATCH_SIZE
        ]

        batches.append(batch)

    # --------------------------------------------------------
    # Process batches
    # --------------------------------------------------------

    for batch_number, batch in enumerate(
        batches,
        start=1
    ):

        results, processing_time = process_batch(
            batch,
            batch_number
        )

        all_results.extend(results)

        print(
            f"\nBatch processing time: "
            f"{processing_time:.3f} seconds"
        )

    server_end = time.perf_counter()

    total_time = (
        server_end - server_start
    )

    return all_results, total_time


# ============================================================
# CALCULATE METRICS
# ============================================================

def calculate_metrics(
    requests,
    results,
    total_time
):

    request_count = len(requests)

    if total_time > 0:

        requests_per_second = (
            request_count / total_time
        )

    else:

        requests_per_second = 0

    processing_times = [
        result["processing_time"]
        for result in results
    ]

    if processing_times:

        average_latency = (
            sum(processing_times)
            / len(processing_times)
        )

    else:

        average_latency = 0

    return {
        "total_requests": request_count,
        "total_time_seconds": round(
            total_time,
            3
        ),
        "average_latency_seconds": round(
            average_latency,
            3
        ),
        "requests_per_second": round(
            requests_per_second,
            3
        ),
        "batch_size": BATCH_SIZE,
        "number_of_batches": (
            (request_count + BATCH_SIZE - 1)
            // BATCH_SIZE
        )
    }


# ============================================================
# DISPLAY RESULTS
# ============================================================

def display_results(metrics):

    print("\n" + "=" * 70)
    print("SERVING METRICS")
    print("=" * 70)

    print(
        f"Total requests: "
        f"{metrics['total_requests']}"
    )

    print(
        f"Total processing time: "
        f"{metrics['total_time_seconds']} seconds"
    )

    print(
        f"Average latency: "
        f"{metrics['average_latency_seconds']} seconds"
    )

    print(
        f"Requests/second: "
        f"{metrics['requests_per_second']}"
    )

    print(
        f"Batch size: "
        f"{metrics['batch_size']}"
    )

    print(
        f"Number of batches: "
        f"{metrics['number_of_batches']}"
    )


# ============================================================
# MAIN
# ============================================================

def main():

    requests = load_requests()

    results, total_time = run_server_simulation(
        requests
    )

    metrics = calculate_metrics(
        requests,
        results,
        total_time
    )

    display_results(metrics)

    print("\n" + "=" * 70)
    print("REQUEST RESULTS")
    print("=" * 70)

    for result in results:

        print(
            f"{result['id']} | "
            f"batch={result['batch_size']} | "
            f"processing="
            f"{result['processing_time']}s"
        )

    print("\nSimulation completed.")


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()