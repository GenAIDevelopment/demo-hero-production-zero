"""Gemini paid-tier prices and the exchange rate used for every cost shown in the workshop.

Checked on 2026-11-13:
- Prices: Google's Gemini API pricing page (paid tier, standard). gemini-3.8-flash's price is
  promotional until 31 December 2026 and doubles on 1 January 2027.
- Exchange rate: 1 USD = ₹94.25 (European Central Bank reference rate for 2026-11-13, via frankfurter.dev).
On the free tier these calls cost nothing; the numbers show what the same traffic costs in production.
"""
PRICES_CHECKED_ON = "2026-11-13"
USD_TO_INR = 94.25
USD_TO_INR_SOURCE = "ECB reference rate for 2026-11-13 (frankfurter.dev)"

# USD per 1 million tokens. Thinking tokens are billed as output.
PRICES = {
    "gemini-3.8-flash": {"input": 0.75, "cached_input": 0.075, "output": 3.75},
    "gemini-3.5-flash-lite": {"input": 0.30, "cached_input": 0.03, "output": 2.50},
    "gemini-embedding-001": {"input": 0.15, "cached_input": 0.15, "output": 0.0},
}


def cost_usd(model, input_tokens=0, output_tokens=0, cached_tokens=0):
    """Cost of one call. input_tokens includes cached_tokens (as Gemini reports them)."""
    p = PRICES[model]
    fresh = max(input_tokens - cached_tokens, 0)
    return (fresh * p["input"] + cached_tokens * p["cached_input"] + output_tokens * p["output"]) / 1_000_000


def cost_inr(model, input_tokens=0, output_tokens=0, cached_tokens=0):
    return cost_usd(model, input_tokens, output_tokens, cached_tokens) * USD_TO_INR


def usage_of(reply):
    """(input, output incl. thinking, cached) tokens from a LangChain AIMessage."""
    u = getattr(reply, "usage_metadata", None) or {}
    cached = (u.get("input_token_details") or {}).get("cache_read", 0) or 0
    return u.get("input_tokens", 0) or 0, u.get("output_tokens", 0) or 0, cached
