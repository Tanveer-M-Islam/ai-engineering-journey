# ============================================================
# DAY 83
# SIMPLE API KEY AUTHENTICATION
# ============================================================

import os

from fastapi import Header, HTTPException


# ------------------------------------------------------------
# Development key
# ------------------------------------------------------------

API_KEY = os.getenv(
    "LLM_API_KEY",
    "dev-secret-key"
)


# ============================================================
# AUTHENTICATION FUNCTION
# ============================================================

def verify_api_key(
    authorization: str | None = Header(default=None)
):

    if not authorization:

        raise HTTPException(
            status_code=401,
            detail="Authorization header is required."
        )

    if not authorization.startswith(
        "Bearer "
    ):

        raise HTTPException(
            status_code=401,
            detail="Authorization must use Bearer token."
        )

    provided_key = authorization[
        len("Bearer "):
    ]

    if provided_key != API_KEY:

        raise HTTPException(
            status_code=401,
            detail="Invalid API key."
        )

    return True