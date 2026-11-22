import json
from pathlib import Path
from typing import List, Dict, Any, Optional
import pandas as pd
from src.config import DATA_PATH

class CatalogEngine:
    def __init__(self, csv_path: Any = DATA_PATH):
        self.csv_path = Path(csv_path)
        self.df = self._load_data()

    def _load_data(self) -> pd.DataFrame:
        if not self.csv_path.exists():
            raise FileNotFoundError(f"Dataset not found at {self.csv_path}")
        df = pd.read_csv(self.csv_path)
        # Parse JSON specifications safely
        def safe_json_parse(x):
            if isinstance(x, dict):
                return x
            if isinstance(x, str):
                try:
                    return json.loads(x)
                except Exception:
                    pass
            return {}
        
        if 'specs_json' in df.columns:
            df['parsed_specs'] = df['specs_json'].apply(safe_json_parse)
        else:
            df['parsed_specs'] = [{}] * len(df)
        return df

    def get_categories(self) -> List[str]:
        return sorted(self.df['category'].dropna().unique().tolist())

    def filter_products(
        self,
        category: Optional[str] = None,
        max_budget: Optional[float] = None,
        min_energy_rating: Optional[int] = None,
        brand: Optional[str] = None,
        query_text: Optional[str] = None,
        limit: int = 4
    ) -> List[Dict[str, Any]]:
        filtered = self.df.copy()

        # 1. Filter by category
        if category and category.lower() != "all":
            filtered = filtered[filtered['category'].str.lower() == category.lower()]

        # 2. Strict Hard Constraint: Filter by max budget
        if max_budget is not None and max_budget > 0:
            filtered = filtered[filtered['price_inr'] <= max_budget]

        # 3. Filter by minimum rating
        if min_energy_rating is not None and min_energy_rating > 0:
            filtered = filtered[filtered['energy_rating'].fillna(0) >= min_energy_rating]

        # 4. Filter by brand if provided
        if brand and brand.strip():
            filtered = filtered[filtered['brand'].str.contains(brand.strip(), case=False, na=False)]

        if filtered.empty:
            return []

        # 5. Smart Relevance & Budget Proximity Scoring
        def calculate_score(row):
            score = 0.0
            price = float(row['price_inr'])
            name_lower = str(row['name']).lower()
            pros_lower = str(row['key_pros']).lower()
            specs_lower = str(row['specs_json']).lower()

            # Budget utilization score: products that meaningfully utilize the budget
            if max_budget and max_budget > 0:
                utilization = price / max_budget
                score += utilization * 45.0
            else:
                score += 20.0

            # Energy / Star rating bonus (up to 15 pts)
            er = row.get('energy_rating')
            if pd.notna(er) and str(er).strip().isdigit() and float(er) > 0:
                score += float(er) * 3.0

            # Query keyword semantic matching bonus (up to 40 pts)
            if query_text:
                import re
                words = re.findall(r'\b\w+\b', query_text.lower())
                stopwords = {'under', 'need', 'want', 'with', 'from', 'this', 'that', 'prefer', 'looking', 'suggest', 'recommend', 'options'}
                for w in words:
                    if len(w) > 3 and w not in stopwords:
                        if w in name_lower:
                            score += 8.0
                        elif w in pros_lower or w in specs_lower:
                            score += 4.0

            return score

        filtered['relevance_score'] = filtered.apply(calculate_score, axis=1)

        # Sort primarily by relevance score, secondary by price descending (closest to budget)
        filtered = filtered.sort_values(by=['relevance_score', 'price_inr'], ascending=[False, False])

        records = filtered.head(limit).to_dict(orient='records')
        return records

    def get_all_as_text_catalog(self, category: Optional[str] = None) -> str:
        """Returns formatted string representation of catalog for raw LLM ingestion (Baseline)."""
        df_sub = self.df if not category or category.lower() == "all" else self.df[self.df['category'].str.lower() == category.lower()]
        lines = []
        for _, row in df_sub.iterrows():
            lines.append(
                f"- ID: {row['product_id']} | Name: {row['name']} | Price: ₹{row['price_inr']:,} | "
                f"Specs: {row['specs_json']} | Pros: {row['key_pros']} | Cons: {row['key_cons']}"
            )
        return "\n".join(lines)
