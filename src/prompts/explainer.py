"""
Stage 3: Grounded Chain-of-Thought (CoT) Explainer Prompt
Takes deterministically filtered candidate products and reasons step-by-step
over constraint matching, real-world utility, and explicit trade-offs.
"""

from typing import List, Dict, Any

EXPLAINER_SYSTEM_PROMPT = """You are ElectraMatch, an objective, explainable electronics recommendation advisor.
Your recommendations are grounded strictly in the verified product specifications provided.
You must adhere to the following principles:
1. Explain WHY each product matches the user's requirements.
2. Honestly highlight trade-offs, drawbacks, or limitations (key cons).
3. Compare the candidates to help the buyer make an informed decision.
4. NEVER invent or hallucinate specifications. If a specification is not in the record, do NOT assume it.
"""

def build_explainer_prompt(
    user_query: str,
    parsed_requirements: Dict[str, Any],
    candidate_products: List[Dict[str, Any]]
) -> str:
    products_formatted = []
    for idx, p in enumerate(candidate_products, 1):
        specs_str = ", ".join(f"{k}: {v}" for k, v in p.get('parsed_specs', {}).items())
        products_formatted.append(
            f"Product {idx}: [{p['product_id']}] {p['name']}\n"
            f"  - Price: ₹{p['price_inr']:,}\n"
            f"  - Capacity/Size: {p.get('capacity', 'N/A')}\n"
            f"  - Energy Rating: {p.get('energy_rating', 'N/A')} Star\n"
            f"  - Verified Specs: {specs_str}\n"
            f"  - Known Pros: {p.get('key_pros', 'N/A')}\n"
            f"  - Known Limitations: {p.get('key_cons', 'N/A')}"
        )
    catalog_context = "\n\n".join(products_formatted)

    return f"""USER QUERY: "{user_query}"

PARSED USER REQUIREMENTS:
- Target Category: {parsed_requirements.get('category')}
- Max Budget: ₹{parsed_requirements.get('budget_max', 'None')}
- Mandatory Hard Constraints: {parsed_requirements.get('hard_constraints')}
- Soft Preferences: {parsed_requirements.get('soft_preferences')}
- User Context: {parsed_requirements.get('household_context')}

CANDIDATE PRODUCTS FROM VERIFIED DATABASE:
{catalog_context}

INSTRUCTIONS:
Conduct step-by-step Chain-of-Thought reasoning:
1. Constraint Verification: Check how each candidate satisfies the mandatory constraints and budget.
2. Ranking: Rank the candidates from best match to alternative options.
3. For each recommended product provide:
   - Match Score / Verdict (e.g., Best Overall, Best Budget Alternative)
   - Why it fits the user's specific context
   - Honest Trade-offs & Limitations
4. Concluding comparative summary advising the user on the final decision."""
