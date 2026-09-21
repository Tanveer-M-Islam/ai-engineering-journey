# ============================================================
# DAY 83
# LLM SERVICE
# ============================================================

import requests


# ============================================================
# CONFIGURATION
# ============================================================

OLLAMA_URL = "http://localhost:11434"

MODEL_NAME = "llama3.2"


# ============================================================
# LLM GENERATION
# ============================================================

def generate(
    prompt: str,
    temperature: float,
    max_tokens: int
):

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": temperature,
            "num_predict": max_tokens
        }
    }

    response = requests.post(
        f"{OLLAMA_URL}/api/generate",
        json=payload,
        timeout=300
    )

    response.raise_for_status()

    result = response.json()

    total_duration = result.get(
        "total_duration",
        0
    )

    return {
        "model": MODEL_NAME,
        "response": result.get(
            "response",
            ""
        ),
        "prompt_tokens": result.get(
            "prompt_eval_count",
            0
        ),
        "generated_tokens": result.get(
            "eval_count",
            0
        ),
        "total_duration_seconds": round(
            total_duration / 1_000_000_000,
            3
        )
    }


# ============================================================
# HEALTH CHECK
# ============================================================

def check_llm():

    response = requests.get(
        f"{OLLAMA_URL}/api/tags",
        timeout=5
    )

    response.raise_for_status()

    return True