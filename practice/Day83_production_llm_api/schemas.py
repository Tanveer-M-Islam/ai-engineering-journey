# ============================================================
# DAY 83
# REQUEST AND RESPONSE SCHEMAS
# ============================================================

from pydantic import BaseModel, Field


class GenerateRequest(BaseModel):

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


class GenerateResponse(BaseModel):

    model: str

    response: str

    prompt_tokens: int

    generated_tokens: int

    total_duration_seconds: float


class ErrorResponse(BaseModel):

    error: str

    message: str