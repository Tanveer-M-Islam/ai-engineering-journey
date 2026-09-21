from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel, Field

from multimodal_pipeline import process_multimodal_input


app = FastAPI(
    title="Multimodal LLM Fundamentals",
    version="1.0.0",
)


class MultimodalRequest(BaseModel):

    text: Optional[str] = Field(
        default=None,
        max_length=4000,
    )

    image_description: Optional[str] = Field(
        default=None,
        max_length=4000,
    )

    audio_transcript: Optional[str] = Field(
        default=None,
        max_length=4000,
    )


@app.get("/health")
def health():

    return {
        "status": "ok",
        "project": "Day 86 - Multimodal LLM Fundamentals",
    }


@app.post("/multimodal")
def multimodal(request: MultimodalRequest):

    return process_multimodal_input(
        text=request.text,
        image_description=request.image_description,
        audio_transcript=request.audio_transcript,
    )