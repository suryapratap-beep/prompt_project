"""
Stage 1: Intent & Constraint Extraction Prompt
Few-shot prompt that converts messy natural language queries into strict JSON schema
separating non-negotiable hard constraints from soft user preferences.
"""

from pydantic import BaseModel, Field
from typing import List, Optional

class ParsedRequirements(BaseModel):
    category: str = Field(description="Product category: refrigerator, washing_machine, laptop, air_conditioner, microwave, or other")
    budget_max: Optional[float] = Field(description="Maximum numeric budget in INR (₹). Null if unstated.")
    hard_constraints: List[str] = Field(description="Strict mandatory requirements (e.g. price limit, capacity, specific essential feature)")
    soft_preferences: List[str] = Field(description="Flexible nice-to-have preferences (e.g. brand, color, smart connectivity)")
    household_context: Optional[str] = Field(description="Family size, usage context, or purpose (e.g. family of 3, college student)")

EXTRACTION_SYSTEM_PROMPT = """You are an expert requirement extraction engine for electronics and home appliances.
Analyze the user's natural language shopping query and parse it into structured JSON.
Distinguish strictly between HARD CONSTRAINTS (mandatory non-negotiables) and SOFT PREFERENCES (desirable but flexible).
Never confuse soft brand preference with hard budget bounds.
Always normalize budget into an integer/float in INR (e.g., '25k' or '25,000' -> 25000).
"""

EXTRACTION_FEW_SHOT = """
Example 1:
User: "I need a refrigerator under ₹25,000 for a family of three. Prefer double door frost-free if possible."
JSON:
{
  "category": "refrigerator",
  "budget_max": 25000,
  "hard_constraints": ["price <= 25000", "door_type == Double Door or Frost-Free"],
  "soft_preferences": ["energy efficient", "reputed brand"],
  "household_context": "Family of 3 members"
}

Example 2:
User: "Looking for a fast coding laptop under 50k. 16GB RAM is a must for Docker, would like decent battery."
JSON:
{
  "category": "laptop",
  "budget_max": 50000,
  "hard_constraints": ["price <= 50000", "ram >= 16GB"],
  "soft_preferences": ["long battery life", "lightweight"],
  "household_context": "Software development / programming"
}
"""

def build_extraction_prompt(user_query: str) -> str:
    return f"""{EXTRACTION_FEW_SHOT}

Now extract requirements from this user query:
User: "{user_query}"
JSON:"""
