"""
Baseline Zero-Shot Prompt Strategy
Passed directly to LLM with raw unstructured catalog excerpts and user request.
This mirrors standard naive LLM prompting without step-wise grounding or guardrails.
"""

BASELINE_SYSTEM_PROMPT = """You are a helpful product recommendation assistant.
Based on the user's budget, intended use, and preferences, recommend three suitable electrical or electronic products from the provided dataset.
Consider price, features, and specifications. Briefly explain why each product is suitable and compare their advantages.
Use only the available product information.
"""

def build_baseline_prompt(user_query: str, catalog_text: str) -> str:
    return f"""CATALOG DATASET:
{catalog_text}

USER REQUEST:
{user_query}

Please recommend 3 products. Include product name, price, key features, and your reasoning."""
