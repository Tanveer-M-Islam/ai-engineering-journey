def calculate_savings(
    original_cost: float,
    optimized_cost: float
) -> dict:

    savings = original_cost - optimized_cost

    if original_cost > 0:
        savings_percentage = (
            savings / original_cost
        ) * 100
    else:
        savings_percentage = 0

    return {
        "original_cost": round(original_cost, 8),
        "optimized_cost": round(optimized_cost, 8),
        "savings": round(savings, 8),
        "savings_percentage": round(savings_percentage, 2),
    }


def reduce_context(
    input_tokens: int,
    reduction_percentage: float
) -> int:

    remaining_ratio = (
        1 - reduction_percentage / 100
    )

    optimized_tokens = (
        input_tokens * remaining_ratio
    )

    return max(1, int(optimized_tokens))


def estimate_cache_cost(
    total_requests: int,
    cache_hit_rate: float,
    cost_per_llm_request: float
) -> float:

    cache_hit_rate = max(
        0,
        min(cache_hit_rate, 1)
    )

    llm_requests = (
        total_requests
        * (1 - cache_hit_rate)
    )

    return llm_requests * cost_per_llm_request