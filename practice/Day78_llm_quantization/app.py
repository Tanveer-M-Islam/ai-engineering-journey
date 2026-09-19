# ============================================================
# DAY 78 — LLM QUANTIZATION
# Memory Estimation Practice
# ============================================================

from dataclasses import dataclass


# ============================================================
# CONFIGURATION
# ============================================================

MODEL_PARAMETERS_BILLION = 7.0


# ============================================================
# PRECISION INFORMATION
# ============================================================

@dataclass
class Precision:
    name: str
    bits_per_parameter: int


PRECISIONS = [
    Precision("FP32", 32),
    Precision("FP16", 16),
    Precision("BF16", 16),
    Precision("INT8", 8),
    Precision("INT4", 4),
]


# ============================================================
# MEMORY CALCULATION
# ============================================================

def estimate_memory_gb(
    parameters_billion: float,
    bits_per_parameter: int
) -> float:

    total_bits = (
        parameters_billion
        * 1_000_000_000
        * bits_per_parameter
    )

    total_bytes = total_bits / 8

    memory_gb = total_bytes / (
        1024 ** 3
    )

    return memory_gb


# ============================================================
# DISPLAY RESULTS
# ============================================================

def main():

    print("=" * 65)
    print("DAY 78 — LLM QUANTIZATION")
    print("=" * 65)

    print(
        f"\nModel size: "
        f"{MODEL_PARAMETERS_BILLION} billion parameters"
    )

    print("\nEstimated weight memory:")
    print("-" * 65)

    for precision in PRECISIONS:

        memory = estimate_memory_gb(
            MODEL_PARAMETERS_BILLION,
            precision.bits_per_parameter
        )

        print(
            f"{precision.name:<8}"
            f"{precision.bits_per_parameter:>5} bits/parameter"
            f"{memory:>12.2f} GB"
        )

    print("-" * 65)

    fp32_memory = estimate_memory_gb(
        MODEL_PARAMETERS_BILLION,
        32
    )

    int4_memory = estimate_memory_gb(
        MODEL_PARAMETERS_BILLION,
        4
    )

    reduction = (
        1 - (int4_memory / fp32_memory)
    ) * 100

    print(
        f"\nApproximate FP32 → INT4 "
        f"weight-memory reduction: "
        f"{reduction:.1f}%"
    )

    print("\nImportant:")
    print(
        "These are theoretical weight-memory estimates."
    )

    print(
        "Actual runtime memory is higher because of "
        "activations, buffers, metadata, and framework overhead."
    )


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()