# ============================================================
# DAY 81
# FASTAPI LLM SERVING
# ============================================================

from typing import Optional

import requests

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


# ============================================================
# CONFIGURATION
# ============================================================

OLLAMA_URL = "http://localhost:11434"

MODEL_NAME = "llama3.2"


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="Day 81 - FastAPI LLM Server",
    description="Simple LLM API using FastAPI and Ollama",
    version="1.0.0"
)


# ============================================================
# REQUEST SCHEMA
# ============================================================

class GenerateRequest(BaseModel):

    prompt: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="Prompt to send to the LLM"
    )

    temperature: float = Field(
        default=0.2,
        ge=0.0,
        le=2.0
    )

    max_tokens: Optional[int] = Field(
        default=300,
        ge=1,
        le=1000
    )


# ============================================================
# RESPONSE SCHEMA
# ============================================================

class GenerateResponse(BaseModel):

    model: str

    response: str

    prompt_tokens: int

    generated_tokens: int

    total_duration_seconds: float


# ============================================================
# HEALTH ENDPOINT
# ============================================================

@app.get("/health")
def health():

    try:

        response = requests.get(
            f"{OLLAMA_URL}/api/tags",
            timeout=5
        )

        response.raise_for_status()

        return {
            "status": "healthy",
            "ollama": "connected",
            "model": MODEL_NAME
        }

    except requests.RequestException:

        return {
            "status": "unhealthy",
            "ollama": "not reachable",
            "model": MODEL_NAME
        }


# ============================================================
# MODEL ENDPOINT
# ============================================================

@app.get("/models")
def models():

    try:

        response = requests.get(
            f"{OLLAMA_URL}/api/tags",
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        models = [
            model.get("name", "")
            for model in data.get("models", [])
        ]

        return {
            "models": models
        }

    except requests.RequestException as error:

        raise HTTPException(
            status_code=503,
            detail=f"Ollama unavailable: {error}"
        )


# ============================================================
# GENERATION ENDPOINT
# ============================================================

@app.post(
    "/generate",
    response_model=GenerateResponse
)
def generate(request: GenerateRequest):

    payload = {
        "model": MODEL_NAME,
        "prompt": request.prompt,
        "stream": False,
        "options": {
            "temperature": request.temperature,
            "num_predict": request.max_tokens
        }
    }

    try:

        response = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json=payload,
            timeout=300
        )

        response.raise_for_status()

        result = response.json()

    except requests.RequestException as error:

        raise HTTPException(
            status_code=503,
            detail=f"LLM service unavailable: {error}"
        )

    total_duration = result.get(
        "total_duration",
        0
    )

    total_duration_seconds = (
        total_duration / 1_000_000_000
    )

    return GenerateResponse(
        model=MODEL_NAME,
        response=result.get(
            "response",
            ""
        ),
        prompt_tokens=result.get(
            "prompt_eval_count",
            0
        ),
        generated_tokens=result.get(
            "eval_count",
            0
        ),
        total_duration_seconds=round(
            total_duration_seconds,
            3
        )
    )


# ============================================================
# ROOT
# ============================================================

@app.get("/")
def root():

    return {
        "message": "FastAPI LLM server is running.",
        "model": MODEL_NAME,
        "endpoints": [
            "/health",
            "/models",
            "/generate",
            "/docs"
        ]
    }