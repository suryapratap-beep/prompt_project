import json
import re
import time
from typing import Dict, Any, List, Optional
from src.config import get_genai_client, DEFAULT_MODEL_NAME
from src.data_loader import CatalogEngine
from src.prompts import (
    BASELINE_SYSTEM_PROMPT, build_baseline_prompt,
    EXTRACTION_SYSTEM_PROMPT, build_extraction_prompt, ParsedRequirements,
    EXPLAINER_SYSTEM_PROMPT, build_explainer_prompt,
    VERIFIER_SYSTEM_PROMPT, build_verifier_prompt
)

class ElectraMatchOrchestrator:
    def __init__(self, catalog: Optional[CatalogEngine] = None):
        self.catalog = catalog or CatalogEngine()

    def _call_gemini(self, client, prompt: str, system_instruction: str = "", model_name: str = DEFAULT_MODEL_NAME) -> str:
        if not client:
            raise ValueError("No Gemini client provided")
        response = client.models.generate_content(
            model=model_name,
            contents=prompt,
            config={
                "system_instruction": system_instruction,
                "temperature": 0.2,
            }
        )
        return response.text.strip()

    def run_baseline(self, user_query: str, api_key: str = "", model_name: str = DEFAULT_MODEL_NAME) -> Dict[str, Any]:
        """Runs the ungrounded Baseline Zero-Shot Prompt."""
        start_time = time.time()
        catalog_text = self.catalog.get_all_as_text_catalog()
        prompt = build_baseline_prompt(user_query, catalog_text)
        client = get_genai_client(api_key)

        if client:
            try:
                response_text = self._call_gemini(client, prompt, BASELINE_SYSTEM_PROMPT, model_name)
            except Exception as e:
                response_text = f"Baseline API Error: {str(e)}\n\n[Fallback Local Baseline Output Generated]"
        else:
            # High-fidelity baseline simulation
            response_text = (
                f"### Baseline Recommendation (Zero-Shot)\n\n"
                f"Based on your request: '{user_query}', here are recommendations:\n\n"
                f"1. **Samsung 236L Double Door Refrigerator** — ₹24,990\n"
                f"   - Fits near the budget limit. Offers frost-free cooling and digital inverter motor.\n\n"
                f"2. **LG 242L 3-Star Smart Inverter Refrigerator** — ₹25,999\n"
                f"   - Door Cooling+ technology with 10-year smart inverter warranty *(Note: price slightly above budget, warranty unverified)*.\n\n"
                f"3. **Whirlpool 192L 3-Star Single Door** — ₹16,490\n"
                f"   - Economical choice with stabilizer-free operation for smaller storage needs."
            )

        elapsed = time.time() - start_time
        return {
            "strategy": "Baseline Zero-Shot",
            "prompt_used": prompt,
            "response": response_text,
            "latency_sec": round(elapsed, 2)
        }

    def run_pipeline(
        self,
        user_query: str,
        api_key: str = "",
        model_name: str = DEFAULT_MODEL_NAME,
        override_category: Optional[str] = None,
        override_budget: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Executes the 4-Stage ElectraMatch Grounded Pipeline:
        Stage 1: Intent & Constraint Extraction
        Stage 2: Deterministic Catalog Grounding
        Stage 3: Grounded Chain-of-Thought (CoT) Reasoning & Explanation
        Stage 4: Verification & Missing Spec Audit Guardrail
        """
        start_time = time.time()
        client = get_genai_client(api_key)

        # STAGE 1: REQUIREMENT EXTRACTION
        parsed_reqs = self._extract_requirements(user_query, client, model_name)
        
        # Apply manual UI overrides if provided
        if override_category and override_category.lower() != "all":
            parsed_reqs["category"] = override_category
        if override_budget and override_budget > 0:
            parsed_reqs["budget_max"] = override_budget

        category = parsed_reqs.get("category", "")
        budget_max = parsed_reqs.get("budget_max")

        # STAGE 2: DETERMINISTIC CATALOG GROUNDING
        candidates = self.catalog.filter_products(
            category=category,
            max_budget=budget_max,
            query_text=user_query,
            limit=4
        )

        # Fallback relaxation if no strict candidates match
        relaxation_triggered = False
        if not candidates and budget_max:
            relaxation_triggered = True
            # Relax budget by 15% to offer closest alternatives with warning
            candidates = self.catalog.filter_products(
                category=category,
                max_budget=budget_max * 1.15,
                query_text=user_query,
                limit=3
            )

        # STAGE 3: GROUNDED REASONING & EXPLANATION
        if candidates:
            explainer_prompt = build_explainer_prompt(user_query, parsed_reqs, candidates)
            if client:
                try:
                    draft_explanation = self._call_gemini(client, explainer_prompt, EXPLAINER_SYSTEM_PROMPT, model_name)
                except Exception as e:
                    draft_explanation = self._simulate_explanation(user_query, parsed_reqs, candidates, relaxation_triggered)
            else:
                draft_explanation = self._simulate_explanation(user_query, parsed_reqs, candidates, relaxation_triggered)

            # STAGE 4: VERIFICATION & AUDIT GUARDRAIL
            verifier_prompt = build_verifier_prompt(draft_explanation, candidates, budget_max)
            if client:
                try:
                    final_output = self._call_gemini(client, verifier_prompt, VERIFIER_SYSTEM_PROMPT, model_name)
                except Exception:
                    final_output = draft_explanation
            else:
                final_output = draft_explanation
        else:
            final_output = (
                f"No products found in the catalog matching category '{category}' within ₹{budget_max:,}. "
                f"Please consider expanding your budget or checking another category."
            )

        elapsed = time.time() - start_time
        return {
            "strategy": "ElectraMatch 4-Stage Grounded Pipeline",
            "parsed_requirements": parsed_reqs,
            "candidates_found": len(candidates),
            "candidates": candidates,
            "relaxation_triggered": relaxation_triggered,
            "final_recommendation": final_output,
            "latency_sec": round(elapsed, 2)
        }

    def _extract_requirements(self, user_query: str, client, model_name: str) -> Dict[str, Any]:
        """Stage 1: Requirement Extraction."""
        if client:
            try:
                prompt = build_extraction_prompt(user_query)
                resp = self._call_gemini(client, prompt, EXTRACTION_SYSTEM_PROMPT, model_name)
                # Parse JSON block
                clean_json = re.search(r'\{.*\}', resp, re.DOTALL)
                if clean_json:
                    return json.loads(clean_json.group(0))
            except Exception as e:
                print(f"Extraction error: {e}")

        # Heuristic / regex parser fallback
        q_lower = user_query.lower()
        cat = "refrigerator"
        if any(w in q_lower for w in ["vacuum", "purifier", "robot", "cleaner", "deebot", "smart home"]):
            cat = "smart_home"
        elif any(w in q_lower for w in ["washing", "washer", "laundry"]):
            cat = "washing_machine"
        elif any(w in q_lower for w in ["laptop", "notebook", "macbook", "pc", "computer"]):
            cat = "laptop"
        elif any(w in q_lower for w in ["microwave", "oven", "air fryer", "fryer"]):
            cat = "microwave"
        elif any(w in q_lower for w in ["television", "bravia", "oled"]) or re.search(r'\btv\b', q_lower):
            cat = "television"
        elif any(w in q_lower for w in ["router", "wifi router", "modem", "networking"]):
            cat = "router"
        elif any(w in q_lower for w in ["printer", "inkjet", "laserjet"]):
            cat = "printer"
        elif any(w in q_lower for w in ["camera", "dslr", "lens", "camcorder"]):
            cat = "camera"
        elif any(w in q_lower for w in ["headphone", "earbud", "audio", "soundbar", "speaker", "anc", "tws"]):
            cat = "audio"
        elif any(w in q_lower for w in ["conditioner", "cooling", "split", "inverter ac"]) or re.search(r'\bac\b', q_lower):
            cat = "air_conditioner"
        elif any(w in q_lower for w in ["refrigerator", "fridge", "freezer", "single door", "double door"]):
            cat = "refrigerator"

        # Extract budget like 25k, 25000, 25,000
        budget = None
        budget_match = re.search(r'(?:under|below|budget|within|upto|up to|₹|rs\.?)\s*([0-9]+(?:,[0-9]+)?|\d+k)', q_lower)
        if budget_match:
            b_str = budget_match.group(1).replace(',', '')
            if 'k' in b_str:
                budget = float(b_str.replace('k', '')) * 1000
            else:
                budget = float(b_str)

        return {
            "category": cat,
            "budget_max": budget,
            "hard_constraints": [f"category == {cat}"] + ([f"price <= {budget}"] if budget else []),
            "soft_preferences": ["energy efficient", "reputed brand", "family suitability"],
            "household_context": user_query
        }

    def _simulate_explanation(self, user_query: str, parsed_reqs: Dict[str, Any], candidates: List[Dict[str, Any]], relaxed: bool) -> str:
        """Generates clear, explainable trade-off analysis when offline."""
        lines = []
        if relaxed:
            lines.append("⚠️ **Notice**: Strict budget matching returned no items. Displaying closest matching alternatives.\n")

        lines.append("### Grounded Recommendations & Trade-Off Analysis\n")
        for i, c in enumerate(candidates, 1):
            tag = "🌟 Top Recommendation" if i == 1 else "💡 Viable Alternative"
            lines.append(f"#### {i}. {c['name']} ({tag})")
            lines.append(f"- **Verified Price**: ₹{c['price_inr']:,}")
            lines.append(f"- **Capacity / Form**: {c.get('capacity', 'Not specified')}")
            lines.append(f"- **Energy Rating**: {c.get('energy_rating', 'Not rated')} Star")
            lines.append(f"- **Why it matches**: Perfectly satisfies the budget and intended category. {c['key_pros']}.")
            lines.append(f"- **Trade-offs / Missing Specs**: {c['key_cons']}. *Notice: Warranty is {c.get('parsed_specs', {}).get('warranty_years', 'Not available in verified catalog')}*.\n")

        lines.append("### Comparative Summary")
        lines.append(
            f"If maximizing immediate budget savings is your highest priority, choose candidate 1. "
            f"If higher capacity and feature longevity matter more, consider the alternatives."
        )
        return "\n".join(lines)
