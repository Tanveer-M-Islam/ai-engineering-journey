# ============================================================
# DAY 84 — LLM API OBSERVABILITY
# Observable FastAPI + Ollama Application
# ============================================================

import json
import os
import time
import uuid
from datetime import datetime, timezone
from typing import Optional

import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


# ============================================================
# CONFIGURATION
# ============================================================

OLLAMA_URL = "http://localhost:11434/api/generate"

MODEL_NAME = "llama3.2"

LOG_DIR = "logs"

LOG_FILE = os.path.join(
    LOG_DIR,
    "requests.jsonl"
)


# ============================================================
# CREATE APPLICATION
# ============================================================

app = FastAPI(
    title="Observable LLM API",
    version="1.0.0"
)


# ============================================================
# SIMPLE IN-MEMORY METRICS
# ============================================================

metrics = {
    "total_requests": 0,
    "successful_requests": 0,
    "failed_requests": 0,
    "total_input_tokens": 0,
    "total_output_tokens": 0,
    "total_latency_seconds": 0.0
}


# ============================================================
# REQUEST MODEL
# ============================================================

class GenerateRequest(BaseModel):

    prompt: str

    temperature: float = 0.2

    max_tokens: Optional[int] = None


# ============================================================
# LOGGING FUNCTION
# ============================================================

def write_log(event: dict):

    os.makedirs(
        LOG_DIR,
        exist_ok=True
    )

    with open(
        LOG_FILE,
        "a",
        encoding="utf-8"
    ) as file:

        file.write(
            json.dumps(
                event,
                ensure_ascii=False
            )
            + "\n"
        )


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health():

    try:

        response = requests.get(
            "http://localhost:11434/api/tags",
            timeout=5
        )

        ollama_status = (
            response.status_code == 200
        )

    except requests.RequestException:

        ollama_status = False

    return {
        "status": "ok",
        "ollama_available": ollama_status,
        "model": MODEL_NAME
    }


# ============================================================
# METRICS ENDPOINT
# ============================================================

@app.get("/metrics")
def get_metrics():

    total = metrics["total_requests"]

    if total > 0:

        average_latency = (
            metrics["total_latency_seconds"]
            / total
        )

    else:

        average_latency = 0.0

    if metrics["total_latency_seconds"] > 0:

        tokens_per_second = (
            metrics["total_output_tokens"]
            / metrics["total_latency_seconds"]
        )

    else:

        tokens_per_second = 0.0

    if total > 0:

        error_rate = (
            metrics["failed_requests"]
            / total
        ) * 100

    else:

        error_rate = 0.0

    return {
        "total_requests": metrics["total_requests"],
        "successful_requests": metrics["successful_requests"],
        "failed_requests": metrics["failed_requests"],
        "error_rate_percent": round(
            error_rate,
            2
        ),
        "total_input_tokens": (
            metrics["total_input_tokens"]
        ),
        "total_output_tokens": (
            metrics["total_output_tokens"]
        ),
        "average_latency_seconds": round(
            average_latency,
            3
        ),
        "average_output_tokens_per_second": round(
            tokens_per_second,
            2
        )
    }


# ============================================================
# LLM GENERATION
# ============================================================

@app.post("/generate")
def generate(request: GenerateRequest):

    request_id = str(
        uuid.uuid4()
    )

    metrics["total_requests"] += 1

    start_time = time.perf_counter()

    started_at = datetime.now(
        timezone.utc
    ).isoformat()

    # --------------------------------------------------------
    # Log request start
    # --------------------------------------------------------

    write_log({
        "timestamp": started_at,
        "event": "request_started",
        "request_id": request_id,
        "model": MODEL_NAME
    })

    # --------------------------------------------------------
    # Ollama payload
    # --------------------------------------------------------

    options = {
        "temperature": request.temperature
    }

    if request.max_tokens is not None:

        options["num_predict"] = (
            request.max_tokens
        )

    payload = {
        "model": MODEL_NAME,
        "prompt": request.prompt,
        "stream": False,
        "options": options
    }

    try:

        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=300
        )

        response.raise_for_status()

        result = response.json()

    except requests.RequestException as error:

        metrics["failed_requests"] += 1

        elapsed = (
            time.perf_counter()
            - start_time
        )

        write_log({
            "timestamp": datetime.now(
                timezone.utc
            ).isoformat(),
            "event": "request_failed",
            "request_id": request_id,
            "error": str(error),
            "latency_seconds": round(
                elapsed,
                4
            )
        })

        raise HTTPException(
            status_code=503,
            detail="LLM service unavailable."
        )

    # --------------------------------------------------------
    # Extract metrics
    # --------------------------------------------------------

    elapsed = (
        time.perf_counter()
        - start_time
    )

    input_tokens = result.get(
        "prompt_eval_count",
        0
    )

    output_tokens = result.get(
        "eval_count",
        0
    )

    if elapsed > 0:

        tokens_per_second = (
            output_tokens / elapsed
        )

    else:

        tokens_per_second = 0.0

    # --------------------------------------------------------
    # Update metrics
    # --------------------------------------------------------

    metrics["successful_requests"] += 1

    metrics["total_input_tokens"] += (
        input_tokens
    )

    metrics["total_output_tokens"] += (
        output_tokens
    )

    metrics["total_latency_seconds"] += (
        elapsed
    )

    # --------------------------------------------------------
    # Log completion
    # --------------------------------------------------------

    write_log({
        "timestamp": datetime.now(
            timezone.utc
        ).isoformat(),
        "event": "request_completed",
        "request_id": request_id,
        "model": MODEL_NAME,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "latency_seconds": round(
            elapsed,
            4
        ),
        "tokens_per_second": round(
            tokens_per_second,
            2
        )
    })

    # --------------------------------------------------------
    # Return response
    # --------------------------------------------------------

    return {
        "request_id": request_id,
        "model": MODEL_NAME,
        "response": result.get(
            "response",
            ""
        ),
        "observability": {
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "latency_seconds": round(
                elapsed,
                4
            ),
            "tokens_per_second": round(
                tokens_per_second,
                2
            )
        }
    }