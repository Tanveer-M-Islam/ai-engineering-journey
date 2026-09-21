from fastapi import FastAPI
from pydantic import BaseModel, Field

from cost_engine import (
    Pricing,
    Usage,
    calculate_cost,
    project_monthly_cost,
)

from optimizer import (
    calculate_savings,
    reduce_context,
    estimate_cache_cost,
)


app = FastAPI(
    title="LLM Cost Optimization Lab",
    version="1.0.0",
)


# ---------------------------------------------------------
# Request Models
# ---------------------------------------------------------

class CostRequest(BaseModel):
    input_tokens: int = Field(
        gt=0,
        le=10_000_000
    )

    output_tokens: int = Field(
        gt=0,
        le=10_000_000
    )

    input_price_per_million: float = Field(
        gt=0
    )

    output_price_per_million: float = Field(
        gt=0
    )

    requests_per_day: int = Field(
        gt=0
    )


class ContextOptimizationRequest(BaseModel):
    input_tokens: int = Field(
        gt=0
    )

    reduction_percentage: float = Field(
        ge=0,
        le=99
    )

    output_tokens: int = Field(
        gt=0
    )

    input_price_per_million: float = Field(
        gt=0
    )

    output_price_per_million: float = Field(
        gt=0
    )


class CacheOptimizationRequest(BaseModel):
    total_requests: int = Field(
        gt=0
    )

    cache_hit_rate: float = Field(
        ge=0,
        le=1
    )

    input_tokens: int = Field(
        gt=0
    )

    output_tokens: int = Field(
        gt=0
    )

    input_price_per_million: float = Field(
        gt=0
    )

    output_price_per_million: float = Field(
        gt=0
    )


# ---------------------------------------------------------
# Health
# ---------------------------------------------------------

@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "LLM Cost Optimization Lab"
    }


# ---------------------------------------------------------
# Basic Cost Calculation
# ---------------------------------------------------------

@app.post("/cost")
def calculate_request_cost(
    request: CostRequest
):

    pricing = Pricing(
        input_price_per_million=request.input_price_per_million,
        output_price_per_million=request.output_price_per_million,
    )

    usage = Usage(
        input_tokens=request.input_tokens,
        output_tokens=request.output_tokens,
    )

    result = calculate_cost(
        usage=usage,
        pricing=pricing,
    )

    monthly_cost = project_monthly_cost(
        cost_per_request=result["total_cost"],
        requests_per_day=request.requests_per_day,
    )

    result["requests_per_day"] = request.requests_per_day
    result["estimated_monthly_cost"] = monthly_cost

    return result


# ---------------------------------------------------------
# Context Optimization
# ---------------------------------------------------------

@app.post("/optimize/context")
def optimize_context(
    request: ContextOptimizationRequest
):

    original_usage = Usage(
        input_tokens=request.input_tokens,
        output_tokens=request.output_tokens,
    )

    pricing = Pricing(
        input_price_per_million=request.input_price_per_million,
        output_price_per_million=request.output_price_per_million,
    )

    original = calculate_cost(
        usage=original_usage,
        pricing=pricing,
    )

    optimized_input_tokens = reduce_context(
        input_tokens=request.input_tokens,
        reduction_percentage=request.reduction_percentage,
    )

    optimized_usage = Usage(
        input_tokens=optimized_input_tokens,
        output_tokens=request.output_tokens,
    )

    optimized = calculate_cost(
        usage=optimized_usage,
        pricing=pricing,
    )

    savings = calculate_savings(
        original_cost=original["total_cost"],
        optimized_cost=optimized["total_cost"],
    )

    return {
        "original": original,
        "optimized": optimized,
        "optimization": {
            "original_input_tokens": request.input_tokens,
            "optimized_input_tokens": optimized_input_tokens,
            "reduction_percentage": request.reduction_percentage,
        },
        "savings": savings,
    }


# ---------------------------------------------------------
# Cache Optimization
# ---------------------------------------------------------

@app.post("/optimize/cache")
def optimize_cache(
    request: CacheOptimizationRequest
):

    pricing = Pricing(
        input_price_per_million=request.input_price_per_million,
        output_price_per_million=request.output_price_per_million,
    )

    usage = Usage(
        input_tokens=request.input_tokens,
        output_tokens=request.output_tokens,
    )

    single_request = calculate_cost(
        usage=usage,
        pricing=pricing,
    )

    original_total_cost = (
        request.total_requests
        * single_request["total_cost"]
    )

    optimized_total_cost = estimate_cache_cost(
        total_requests=request.total_requests,
        cache_hit_rate=request.cache_hit_rate,
        cost_per_llm_request=single_request["total_cost"],
    )

    savings = calculate_savings(
        original_cost=original_total_cost,
        optimized_cost=optimized_total_cost,
    )

    return {
        "total_requests": request.total_requests,
        "cache_hit_rate": request.cache_hit_rate,
        "llm_requests_after_cache": int(
            request.total_requests
            * (1 - request.cache_hit_rate)
        ),
        "original_total_cost": round(
            original_total_cost,
            8,
        ),
        "optimized_total_cost": round(
            optimized_total_cost,
            8,
        ),
        "savings": savings,
    }