# ============================================================
# DAY 83
# SIMPLE IN-MEMORY RATE LIMITER
# ============================================================

import time

from fastapi import HTTPException


# ------------------------------------------------------------
# Configuration
# ------------------------------------------------------------

MAX_REQUESTS = 5

WINDOW_SECONDS = 60


# ------------------------------------------------------------
# Request storage
# ------------------------------------------------------------

request_history = {}


# ============================================================
# RATE LIMIT CHECK
# ============================================================

def check_rate_limit(client_id: str):

    current_time = time.time()

    timestamps = request_history.get(
        client_id,
        []
    )

    # --------------------------------------------------------
    # Keep only requests inside the current window
    # --------------------------------------------------------

    timestamps = [
        timestamp
        for timestamp in timestamps
        if current_time - timestamp
        < WINDOW_SECONDS
    ]

    # --------------------------------------------------------
    # Check limit
    # --------------------------------------------------------

    if len(timestamps) >= MAX_REQUESTS:

        raise HTTPException(
            status_code=429,
            detail=(
                "Rate limit exceeded. "
                "Please try again later."
            )
        )

    # --------------------------------------------------------
    # Add current request
    # --------------------------------------------------------

    timestamps.append(
        current_time
    )

    request_history[client_id] = timestamps