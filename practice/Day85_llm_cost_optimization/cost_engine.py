from dataclasses import dataclass


@dataclass
class Pricing:
    input_price_per_million: float
    output_price_per_million: float


@dataclass
class Usage:
    input_tokens: int
    output_tokens: int


def calculate_cost(
    usage: Usage,
    pricing: Pricing
) -> dict:

    input_cost = (
        usage.input_tokens / 1_000_000
    ) * pricing.input_price_per_million

    output_cost = (
        usage.output_tokens / 1_000_000
    ) * pricing.output_price_per_million

    total_cost = input_cost + output_cost

    return {
        "input_tokens": usage.input_tokens,
        "output_tokens": usage.output_tokens,
        "input_cost": round(input_cost, 8),
        "output_cost": round(output_cost, 8),
        "total_cost": round(total_cost, 8),
    }


def project_monthly_cost(
    cost_per_request: float,
    requests_per_day: int,
    days_per_month: int = 30
) -> float:

    monthly_cost = (
        cost_per_request
        * requests_per_day
        * days_per_month
    )

    return round(monthly_cost, 4)