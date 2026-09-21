# Day 85 — LLM Cost Optimization

## Core Idea

LLM cost is primarily influenced by:

- Input tokens
- Output tokens
- Model pricing
- Number of requests

## Basic Formula

Input Cost:

(Input Tokens / 1,000,000) × Input Price

Output Cost:

(Output Tokens / 1,000,000) × Output Price

Total Cost:

Input Cost + Output Cost

## Monthly Cost

Monthly Cost:

Cost Per Request × Requests Per Day × Days Per Month

## Important Optimization Techniques

1. Prompt optimization
2. Context reduction
3. Caching
4. Model selection
5. Output limits
6. Batching
7. Model routing

## Context Reduction

Large RAG contexts can significantly increase input-token usage.

Instead of sending unnecessary documents:

Query
↓
Retriever
↓
Relevant chunks
↓
LLM

## Caching

If the same request can safely reuse an existing answer:

Request
↓
Cache
↓
Cache hit → return result

Cache miss:
↓
LLM
↓
Store result
↓
Return result

## Model Selection

Use smaller/cheaper models for simple tasks and larger models only
when the task requires them.

## Cost vs Latency vs Quality

LLM system design requires balancing:

- Cost
- Latency
- Quality

The cheapest model is not automatically the correct choice.

## Important Metrics

- Cost per request
- Cost per user
- Cost per endpoint
- Input tokens
- Output tokens
- Cache hit rate
- Requests per day
- Monthly cost
- Latency
- Quality score

## Production Considerations

The Day 85 project uses simulated pricing.

In production, pricing should come from the actual provider/model pricing configuration.

Real systems should also consider:

- Currency
- Provider-specific pricing
- Batch pricing
- Cached-input pricing
- Different model tiers
- Taxes/fees where applicable
- Retries
- Failed requests
- Tokenization differences

## Key Lesson

Observability tells us how an LLM system behaves.

Cost engineering uses that information to determine how expensive
the system is and where optimization is possible.