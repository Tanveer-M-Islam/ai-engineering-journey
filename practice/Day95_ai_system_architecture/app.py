import time
import uuid

import requests


# ============================================================
# CONFIGURATION
# ============================================================

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2"

MAX_PROMPT_LENGTH = 2000


# ============================================================
# SIMPLE CACHE
# ============================================================

response_cache = {}


# ============================================================
# REQUEST CONTEXT
# ============================================================

def create_request_context():

    return {
        "request_id": str(uuid.uuid4()),
        "start_time": time.perf_counter()
    }


# ============================================================
# INPUT GUARDRAIL
# ============================================================

def validate_input(prompt):

    if not isinstance(prompt, str):
        return False, "Prompt must be text."

    prompt = prompt.strip()

    if not prompt:
        return False, "Prompt cannot be empty."

    if len(prompt) > MAX_PROMPT_LENGTH:
        return False, "Prompt is too long."

    blocked_phrases = [
        "ignore all previous instructions",
        "reveal system prompt"
    ]

    normalized = prompt.lower()

    for phrase in blocked_phrases:

        if phrase in normalized:

            return False, (
                "Potential prompt injection detected."
            )

    return True, "Input accepted."


# ============================================================
# CACHE
# ============================================================

def get_cached_response(prompt):

    cache_key = prompt.lower().strip()

    return response_cache.get(cache_key)


def save_to_cache(prompt, response):

    cache_key = prompt.lower().strip()

    response_cache[cache_key] = response


# ============================================================
# SIMPLE ROUTER
# ============================================================

def route_request(prompt):

    normalized = prompt.lower()

    knowledge_keywords = [
        "rag",
        "embedding",
        "vector database",
        "llm",
        "machine learning",
        "ai"
    ]

    for keyword in knowledge_keywords:

        if keyword in normalized:

            return "llm"

    return "llm"


# ============================================================
# MODEL GATEWAY
# ============================================================

def call_model(prompt):

    payload = {
        "model": MODEL_NAME,
        "prompt": (
            "Answer clearly and concisely.\n\n"
            f"User question: {prompt}"
        ),
        "stream": False,
        "options": {
            "temperature": 0.2
        }
    }

    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=120
    )

    response.raise_for_status()

    data = response.json()

    return {
        "text": data.get(
            "response",
            ""
        ).strip(),

        "input_tokens": data.get(
            "prompt_eval_count",
            0
        ),

        "output_tokens": data.get(
            "eval_count",
            0
        )
    }


# ============================================================
# OUTPUT GUARDRAIL
# ============================================================

def validate_output(text):

    if not text:
        return False, (
            "Model returned an empty response."
        )

    if len(text) > 10000:
        return False, (
            "Model response exceeded output limit."
        )

    return True, "Output accepted."


# ============================================================
# OBSERVABILITY
# ============================================================

def log_request(
    request_id,
    route,
    cache_hit,
    latency,
    status
):

    print("\n--- OBSERVABILITY ---")

    print(
        "Request ID:",
        request_id
    )

    print(
        "Route:",
        route
    )

    print(
        "Cache Hit:",
        cache_hit
    )

    print(
        "Latency:",
        round(latency, 3),
        "seconds"
    )

    print(
        "Status:",
        status
    )


# ============================================================
# AI ORCHESTRATOR
# ============================================================

def process_request(prompt):

    context = create_request_context()

    request_id = context["request_id"]

    start_time = context["start_time"]

    # --------------------------------------------------------
    # Layer 1: Input guardrail
    # --------------------------------------------------------

    valid, reason = validate_input(
        prompt
    )

    if not valid:

        latency = (
            time.perf_counter()
            - start_time
        )

        log_request(
            request_id,
            "blocked",
            False,
            latency,
            "blocked"
        )

        return {
            "status": "blocked",
            "reason": reason
        }

    # --------------------------------------------------------
    # Layer 2: Cache
    # --------------------------------------------------------

    cached = get_cached_response(
        prompt
    )

    if cached:

        latency = (
            time.perf_counter()
            - start_time
        )

        log_request(
            request_id,
            "cache",
            True,
            latency,
            "success"
        )

        return {
            "status": "success",
            "source": "cache",
            "response": cached
        }

    # --------------------------------------------------------
    # Layer 3: Routing
    # --------------------------------------------------------

    route = route_request(
        prompt
    )

    # --------------------------------------------------------
    # Layer 4: Model Gateway
    # --------------------------------------------------------

    if route == "llm":

        model_result = call_model(
            prompt
        )

    else:

        raise ValueError(
            f"Unknown route: {route}"
        )

    # --------------------------------------------------------
    # Layer 5: Output Guardrail
    # --------------------------------------------------------

    output_valid, output_reason = (
        validate_output(
            model_result["text"]
        )
    )

    if not output_valid:

        latency = (
            time.perf_counter()
            - start_time
        )

        log_request(
            request_id,
            route,
            False,
            latency,
            "blocked"
        )

        return {
            "status": "blocked",
            "reason": output_reason
        }

    # --------------------------------------------------------
    # Layer 6: Save Cache
    # --------------------------------------------------------

    save_to_cache(
        prompt,
        model_result["text"]
    )

    # --------------------------------------------------------
    # Layer 7: Observability
    # --------------------------------------------------------

    latency = (
        time.perf_counter()
        - start_time
    )

    log_request(
        request_id,
        route,
        False,
        latency,
        "success"
    )

    return {
        "status": "success",
        "source": "model",
        "response": model_result["text"],
        "input_tokens": (
            model_result["input_tokens"]
        ),
        "output_tokens": (
            model_result["output_tokens"]
        )
    }


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 60)
    print("DAY 95 - AI SYSTEM ARCHITECTURE")
    print("=" * 60)

    while True:

        print(
            "\nType 'exit' to quit."
        )

        prompt = input(
            "\nEnter prompt: "
        )

        if prompt.lower().strip() == "exit":

            print("\nExiting...")
            break

        try:

            result = process_request(
                prompt
            )

            print("\n--- RESPONSE ---")

            if result["status"] == "blocked":

                print(
                    "Request blocked:"
                )

                print(
                    result["reason"]
                )

            else:

                print(
                    result["response"]
                )

                print(
                    "\nSource:",
                    result["source"]
                )

                if (
                    result["source"]
                    == "model"
                ):

                    print(
                        "Input Tokens:",
                        result["input_tokens"]
                    )

                    print(
                        "Output Tokens:",
                        result["output_tokens"]
                    )

        except requests.exceptions.ConnectionError:

            print(
                "\nERROR: Cannot connect to Ollama."
            )

            print(
                "Make sure Ollama is running."
            )

        except requests.exceptions.Timeout:

            print(
                "\nERROR: Model request timed out."
            )

        except Exception as error:

            print(
                "\nERROR:",
                error
            )


if __name__ == "__main__":
    main()