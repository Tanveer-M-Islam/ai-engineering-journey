# ============================================================
# DAY 83
# PRODUCTION LLM API DESIGN
# ============================================================

import logging
import time
import uuid

from fastapi import (
    Depends,
    FastAPI,
    HTTPException,
    Request
)

from auth import verify_api_key
from limiter import check_rate_limit
from llm_service import (
    check_llm,
    generate
)
from schemas import (
    GenerateRequest,
    GenerateResponse
)


# ============================================================
# LOGGING
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format=(
        "%(asctime)s | "
        "%(levelname)s | "
        "%(message)s"
    )
)

logger = logging.getLogger(
    "llm_api"
)


# ============================================================
# FASTAPI
# ============================================================

app = FastAPI(
    title="Day 83 - Production LLM API",
    description=(
        "Production-style LLM API architecture"
    ),
    version="1.0.0"
)


# ============================================================
# REQUEST ID MIDDLEWARE
# ============================================================

@app.middleware("http")
async def request_id_middleware(
    request: Request,
    call_next
):

    request_id = str(
        uuid.uuid4()
    )

    start_time = time.perf_counter()

    response = await call_next(
        request
    )

    elapsed = (
        time.perf_counter()
        - start_time
    )

    response.headers[
        "X-Request-ID"
    ] = request_id

    logger.info(
        "request_id=%s method=%s path=%s "
        "status=%s duration=%.3fs",
        request_id,
        request.method,
        request.url.path,
        response.status_code,
        elapsed
    )

    return response


# ============================================================
# ROOT
# ============================================================

@app.get("/")
def root():

    return {
        "service": "Production LLM API",
        "version": "1.0.0",
        "endpoints": [
            "/health",
            "/generate",
            "/docs"
        ]
    }


# ============================================================
# HEALTH
# ============================================================

@app.get("/health")
def health():

    try:

        check_llm()

        return {
            "status": "healthy"
        }

    except Exception:

        return {
            "status": "unhealthy"
        }


# ============================================================
# GENERATE
# ============================================================

@app.post(
    "/generate",
    response_model=GenerateResponse
)
def generate_text(
    request: Request,
    data: GenerateRequest,
    authenticated: bool = Depends(
        verify_api_key
    )
):

    # --------------------------------------------------------
    # Identify client
    # --------------------------------------------------------

    client_id = (
        request.client.host
        if request.client
        else "unknown"
    )

    # --------------------------------------------------------
    # Rate limit
    # --------------------------------------------------------

    check_rate_limit(
        client_id
    )

    # --------------------------------------------------------
    # Generate response
    # --------------------------------------------------------

    try:

        result = generate(
            prompt=data.prompt,
            temperature=data.temperature,
            max_tokens=data.max_tokens
        )

        return result

    except Exception as error:

        logger.exception(
            "LLM generation failed: %s",
            error
        )

        raise HTTPException(
            status_code=503,
            detail=(
                "LLM service is temporarily "
                "unavailable."
            )
        )