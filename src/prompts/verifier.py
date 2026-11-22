"""
Stage 4: Hallucination Guardrail & Spec Audit Prompt
Audits generated recommendation text against exact dataset records.
Flags or replaces unsupported technical claims with 'Not available in specifications'.
"""

from typing import List, Dict, Any

VERIFIER_SYSTEM_PROMPT = """You are a strict technical specification auditor and fact-checking guardrail.
Your sole job is to review a proposed recommendation text against the ground-truth product catalog.
Rules:
1. Verify that every numeric specification, warranty claim, dimension, or feature stated in the draft actually exists in the ground truth.
2. If the draft states a claim not supported by the verified record (e.g. claiming 10-year warranty when only 1-year is verified or unstated), flag it and correct it to "Not available in official catalog" or remove the claim.
3. Verify that recommended products do NOT exceed the stated budget limit.
4. Output the final, verified, and audited recommendation response.
"""

def build_verifier_prompt(
    draft_recommendation: str,
    candidate_products: List[Dict[str, Any]],
    budget_max: float
) -> str:
    records_str = []
    for p in candidate_products:
        records_str.append(
            f"ID: {p['product_id']} | Price: ₹{p['price_inr']} | Specs: {p.get('specs_json')} | Warranty: {p.get('parsed_specs', {}).get('warranty_years', 'NOT SPECIFIED')}"
        )
    db_text = "\n".join(records_str)

    return f"""GROUND TRUTH DATABASE RECORDS:
{db_text}
MAX BUDGET LIMIT: ₹{budget_max if budget_max else 'None'}

DRAFT RECOMMENDATION TO AUDIT:
{draft_recommendation}

Please perform the audit:
- Check for budget compliance
- Check for unverified specification claims
- Provide the final clean, verified recommendation text with any hallucination corrected and missing specifications labeled as 'Not available in verified specifications'."""
