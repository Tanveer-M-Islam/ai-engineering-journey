# ============================================================
# DAY 82
# STREAMING LLM RESPONSES
# ============================================================

import json
from typing import Iterator

import requests

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field


# ============================================================
# CONFIGURATION
# ============================================================

OLLAMA_URL = "http://localhost:11434"

MODEL_NAME = "llama3.2"


# ============================================================
# FASTAPI
# ============================================================

app = FastAPI(
    title="Day 82 - Streaming LLM API",
    description="Streaming LLM responses with FastAPI and Ollama",
    version="1.0.0"
)


# ============================================================
# REQUEST SCHEMA
# ============================================================

class StreamRequest(BaseModel):

    prompt: str = Field(
        ...,
        min_length=1,
        max_length=2000
    )

    temperature: float = Field(
        default=0.2,
        ge=0.0,
        le=2.0
    )

    max_tokens: int = Field(
        default=300,
        ge=1,
        le=1000
    )


# ============================================================
# STREAM GENERATOR
# ============================================================

def generate_stream(
    request: StreamRequest
) -> Iterator[str]:

    payload = {
        "model": MODEL_NAME,
        "prompt": request.prompt,
        "stream": True,
        "options": {
            "temperature": request.temperature,
            "num_predict": request.max_tokens
        }
    }

    try:

        with requests.post(
            f"{OLLAMA_URL}/api/generate",
            json=payload,
            stream=True,
            timeout=300
        ) as response:

            response.raise_for_status()

            for line in response.iter_lines():

                if not line:
                    continue

                data = json.loads(
                    line.decode("utf-8")
                )

                token = data.get(
                    "response",
                    ""
                )

                if token:

                    event = {
                        "type": "token",
                        "content": token
                    }

                    yield (
                        f"data: "
                        f"{json.dumps(event)}"
                        f"\n\n"
                    )

                if data.get("done"):

                    final_event = {
                        "type": "done",
                        "content": ""
                    }

                    yield (
                        f"data: "
                        f"{json.dumps(final_event)}"
                        f"\n\n"
                    )

                    break

    except requests.RequestException as error:

        error_event = {
            "type": "error",
            "message": str(error)
        }

        yield (
            f"data: "
            f"{json.dumps(error_event)}"
            f"\n\n"
        )


# ============================================================
# HEALTH
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
            "model": MODEL_NAME
        }

    except requests.RequestException:

        return {
            "status": "unhealthy"
        }


# ============================================================
# STREAM ENDPOINT
# ============================================================

@app.post("/stream")
def stream(request: StreamRequest):

    return StreamingResponse(
        generate_stream(request),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive"
        }
    )


# ============================================================
# ROOT
# ============================================================

@app.get("/")
def root():

    return {
        "message": "Streaming LLM API",
        "endpoint": "/stream"
    }