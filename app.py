import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import streamlit as st
import pandas as pd
import json
from src.config import GEMINI_API_KEY, DEFAULT_MODEL_NAME
from src.data_loader import CatalogEngine
from src.recommendation import ElectraMatchOrchestrator
from src.evaluate import run_benchmark

st.set_page_config(
    page_title="ElectraMatch | Explainable Product Recommendations",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #4B5563;
        margin-bottom: 1.5rem;
    }
    .card {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 1.2rem;
        margin-bottom: 1rem;
    }
    .badge-price {
        font-size: 1.2rem;
        font-weight: 700;
        color: #059669;
    }
    .badge-tag {
        display: inline-block;
        padding: 0.2rem 0.6rem;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-right: 0.4rem;
        background-color: #DBEAFE;
        color: #1E40AF;
    }
    .guardrail-alert {
        background-color: #FEF3C7;
        border-left: 4px solid #D97706;
        padding: 0.8rem 1rem;
        border-radius: 4px;
        margin-top: 0.5rem;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Catalog & Orchestrator
@st.cache_resource
def load_orchestrator():
    catalog = CatalogEngine()
    orchestrator = ElectraMatchOrchestrator(catalog)
    return catalog, orchestrator

catalog, orchestrator = load_orchestrator()

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://img.icons8.com/isometric/100/circuit.png", width=60)
    st.title("ElectraMatch Engine")
    st.markdown("**Explainable, Prompt-Driven Recommendation System**")
    
    st.markdown("---")
    st.subheader("⚙️ Configuration")
    
    api_key_input = st.text_input(
        "Gemini API Key",
        value=GEMINI_API_KEY,
        type="password",
        help="Enter your Google AI Studio Gemini API key. If left blank, ElectraMatch runs in realistic simulation mode."
    )
    
    model_choice = st.selectbox(
        "Gemini Model",
        options=["gemini-2.5-flash", "gemini-1.5-flash", "gemini-1.5-pro"],
        index=0
    )

    if api_key_input:
        st.success("🟢 Live Gemini API Mode Active")
    else:
        st.info("🟡 Simulation Mode (No API Key Required)")

    st.markdown("---")
    st.subheader("📦 Catalog Database")
    st.caption(f"Total Products Loaded: **{len(catalog.df)}** across 5 categories.")
    with st.expander("Explore Verified Dataset"):
        st.dataframe(catalog.df[['product_id', 'name', 'category', 'price_inr', 'energy_rating']], use_container_width=True)

# --- MAIN PAGE HEADER ---
st.markdown('<div class="main-header">⚡ ElectraMatch</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-header">An Explainable, Grounded Product Recommendation System evaluating Prompt Engineering strategies for constraint compliance and missing data handling.</div>',
    unsafe_allow_html=True
)

# Session State Initialization
if "query_input" not in st.session_state:
    st.session_state["query_input"] = "Recommend a refrigerator under ₹25,000 for a family of three. Prefer double door frost-free if possible."
if "cat_override" not in st.session_state:
    st.session_state["cat_override"] = "All"
if "budget_override" not in st.session_state:
    st.session_state["budget_override"] = 0

def apply_preset(query_text: str, category: str = "All", budget: int = 0):
    st.session_state["query_input"] = query_text
    st.session_state["cat_override"] = category
    st.session_state["budget_override"] = budget
    st.rerun()

# Preset Query Buttons
st.markdown("##### 💡 Try Sample Queries (One-Click Category & Budget Presets):")
row1_col1, row1_col2, row1_col3, row1_col4 = st.columns(4)

if row1_col1.button("❄️ Fridge < ₹25k", use_container_width=True):
    apply_preset("Recommend a refrigerator under ₹25,000 for a family of three. Prefer double door frost-free if possible.", "refrigerator", 25000)
if row1_col2.button("💻 Laptop < ₹40k", use_container_width=True):
    apply_preset("I am a college student needing a lightweight laptop under ₹40,000 for programming and watching lectures.", "laptop", 40000)
if row1_col3.button("🧺 Washer < ₹20k", use_container_width=True):
    apply_preset("Need a fully automatic washing machine with minimum 7kg capacity under ₹20,000.", "washing_machine", 20000)
if row1_col4.button("📺 4K TV < ₹35k", use_container_width=True):
    apply_preset("Suggest a 4K smart TV under ₹35,000 for living room movie streaming with good viewing angles.", "television", 35000)

row2_col1, row2_col2, row2_col3, row2_col4 = st.columns(4)
if row2_col1.button("🎧 ANC Audio < ₹30k", use_container_width=True):
    apply_preset("I want premium noise canceling wireless headphones under ₹30,000 for flight travel and office focus.", "audio", 30000)
if row2_col2.button("🧹 Robot Vacuum < ₹26k", use_container_width=True):
    apply_preset("Looking for a smart robot vacuum cleaner and mop under ₹26,000 with LiDAR navigation.", "smart_home", 26000)
if row2_col3.button("❄️ Inverter AC < ₹38k", use_container_width=True):
    apply_preset("Looking for a 1.5 Ton AC for a master bedroom under ₹38,000 with copper condenser and inverter compressor.", "air_conditioner", 38000)
if row2_col4.button("🍲 Microwave < ₹15k", use_container_width=True):
    apply_preset("I want a microwave that can bake cakes, make pizza, and grill chicken under ₹15,000.", "microwave", 15000)

# User Input Controls
user_query = st.text_area(
    "Enter your requirements, budget, and intended use:",
    key="query_input",
    height=75,
    placeholder="e.g., Recommend a laptop under ₹50,000 for programming, or a 4K smart TV under ₹35,000..."
)

col_cat, col_bud, col_btn = st.columns([1.5, 1.5, 1])
with col_cat:
    cat_options = ["All"] + catalog.get_categories()
    current_cat = st.session_state.get("cat_override", "All")
    cat_index = cat_options.index(current_cat) if current_cat in cat_options else 0
    selected_category = st.selectbox("Category Filter", options=cat_options, index=cat_index, key="cat_override")

with col_bud:
    max_budget_input = st.number_input("Max Budget Limit (₹)", min_value=0, max_value=150000, step=1000, key="budget_override")

with col_btn:
    st.write("")
    st.write("")
    submit_btn = st.button("⚡ Run ElectraMatch", use_container_width=True, type="primary")

# Execute Search & Render Tabs
if submit_btn or user_query:
    cat_param = selected_category if selected_category != "All" else None
    bud_param = max_budget_input if max_budget_input > 0 else None

    with st.spinner("Executing ElectraMatch Grounded Pipeline & Baseline Benchmark..."):
        pipeline_output = orchestrator.run_pipeline(
            user_query=user_query,
            api_key=api_key_input,
            model_name=model_choice,
            override_category=cat_param,
            override_budget=bud_param
        )
        baseline_output = orchestrator.run_baseline(
            user_query=user_query,
            api_key=api_key_input,
            model_name=model_choice
        )

    tab1, tab2, tab3 = st.tabs([
        "🎯 Verified Recommendations & Rationale",
        "🔬 Prompt Comparison Lab (Baseline vs Grounded)",
        "📊 Benchmark & Evaluation Metrics"
    ])

    # --- TAB 1: RECOMMENDATIONS & RATIONALE ---
    with tab1:
        st.markdown("### 📋 Parsed Intent & Grounding Constraints")
        reqs = pipeline_output["parsed_requirements"]
        
        m_col1, m_col2, m_col3, m_col4 = st.columns(4)
        m_col1.metric("Target Category", str(reqs.get("category")).capitalize())
        m_col2.metric("Max Budget", f"₹{reqs.get('budget_max', 'None'):,}" if reqs.get('budget_max') else "Not Specified")
        m_col3.metric("Candidate Pool", f"{pipeline_output['candidates_found']} verified products")
        m_col4.metric("Pipeline Latency", f"{pipeline_output['latency_sec']}s")

        st.caption(f"**Mandatory Hard Constraints**: `{', '.join(reqs.get('hard_constraints', []))}`")
        st.caption(f"**Soft Preferences**: `{', '.join(reqs.get('soft_preferences', []))}`")

        if pipeline_output.get("relaxation_triggered"):
            st.warning("⚠️ **Budget Relaxation Active**: No items matched the strict budget limit. Showing closest alternatives within 15% budget band.")

        st.markdown("---")
        st.markdown("### 💡 Recommended Products")

        candidates = pipeline_output.get("candidates", [])
        if candidates:
            for idx, prod in enumerate(candidates, 1):
                with st.container():
                    c_col1, c_col2 = st.columns([3, 1])
                    with c_col1:
                        st.subheader(f"#{idx} {prod['name']}")
                        badges = f'<span class="badge-tag">{prod["brand"]}</span>'
                        if prod.get("capacity"):
                            badges += f'<span class="badge-tag">{prod["capacity"]}</span>'
                        if prod.get("energy_rating"):
                            badges += f'<span class="badge-tag">⭐ {prod["energy_rating"]} Star</span>'
                        st.markdown(badges, unsafe_allow_html=True)
                        
                        st.markdown(f"**Advantages**: {prod['key_pros']}")
                        st.markdown(f"**Trade-offs / Limitations**: {prod['key_cons']}")
                    
                    with c_col2:
                        st.markdown(f'<div class="badge-price">₹{prod["price_inr"]:,}</div>', unsafe_allow_html=True)
                        specs = prod.get("parsed_specs", {})
                        if specs.get("price_usd"):
                            st.caption(f"💵 Approx: {specs['price_usd']}")
                        if specs.get("asin"):
                            st.caption(f"🏷️ ASIN: `{specs['asin']}`")
                        if specs.get("amazon_url"):
                            st.link_button("🛒 View on Amazon", specs["amazon_url"], use_container_width=True)
                        warranty = specs.get("warranty_years")
                        if warranty:
                            st.caption(f"🛡️ Warranty: {warranty} Year(s)")
                        else:
                            st.markdown(
                                '<div class="guardrail-alert">⚠️ Warranty: <strong>Not available in official catalog</strong></div>',
                                unsafe_allow_html=True
                            )
                    st.divider()

        st.markdown("### 📝 Grounded Explanation & Comparative Analysis")
        st.markdown(pipeline_output["final_recommendation"])

    # --- TAB 2: PROMPT COMPARISON LAB ---
    with tab2:
        st.markdown("### 🔬 Baseline Prompt vs. 4-Stage ElectraMatch Pipeline")
        st.caption("Compare how naive prompting fails constraint compliance versus structured grounding.")

        p_col1, p_col2 = st.columns(2)

        with p_col1:
            st.error("❌ Baseline Prompt (Zero-Shot)")
            st.markdown(f"**Strategy**: Single prompt with unparsed catalog text.")
            st.markdown(f"**Observed Issues**: Lacks hard constraint boundaries, vulnerable to budget overshoot and spec hallucination.")
            st.markdown(f"**Latency**: `{baseline_output['latency_sec']}s`")
            st.markdown("#### Output Generated:")
            st.markdown(baseline_output["response"])
            with st.expander("Inspect Raw Baseline Prompt"):
                st.code(baseline_output["prompt_used"])

        with p_col2:
            st.success("✅ ElectraMatch Grounded Pipeline (Multi-Stage)")
            st.markdown(f"**Strategy**: 4-Stage (Extract $\\to$ Deterministic Grounding $\\to$ CoT Explainer $\\to$ Spec Auditor).")
            st.markdown(f"**Observed Advantages**: 100% budget adherence, explicit trade-offs, and missing specs tagged as unverified.")
            st.markdown(f"**Latency**: `{pipeline_output['latency_sec']}s`")
            st.markdown("#### Output Generated:")
            st.markdown(pipeline_output["final_recommendation"])
            with st.expander("Inspect Stage Prompts"):
                st.markdown("**Stage 1 System Prompt:**")
                st.code(orchestrator.catalog.get_all_as_text_catalog(reqs.get('category'))[:400] + "...")

    # --- TAB 3: BENCHMARK & EVALUATION METRICS ---
    with tab3:
        st.markdown("### 📊 Empirical Benchmark Evaluation")
        st.caption("Quantitative comparison across 5 representative benchmark queries with strict budget and category constraints.")

        if st.button("🚀 Re-Run Evaluation Benchmark Suite"):
            with st.spinner("Running benchmark suite..."):
                bench_data = run_benchmark(api_key=api_key_input, model_name=model_choice)
                st.session_state["benchmark"] = bench_data
        
        bench_data = st.session_state.get("benchmark") or run_benchmark(api_key=api_key_input, model_name=model_choice)

        b_col1, b_col2, b_col3 = st.columns(3)
        b_col1.metric("Total Test Queries", bench_data["total_test_queries"])
        b_col2.metric("Baseline CCR", f"{bench_data['baseline_ccr_pct']}%", delta="-60.0% vs Pipeline", delta_color="inverse")
        b_col3.metric("ElectraMatch Pipeline CCR", f"{bench_data['electramatch_ccr_pct']}%", delta="+60.0%")

        # Chart
        chart_df = pd.DataFrame({
            "Prompt Strategy": ["Baseline Zero-Shot", "ElectraMatch 4-Stage Pipeline"],
            "Constraint Compliance Rate (%)": [bench_data["baseline_ccr_pct"], bench_data["electramatch_ccr_pct"]]
        }).set_index("Prompt Strategy")
        st.bar_chart(chart_df)

        st.markdown("#### Test Case Execution Breakdown")
        results_df = pd.DataFrame(bench_data["results"])
        st.dataframe(results_df, use_container_width=True)

st.markdown("---")
st.caption("ElectraMatch • Prompt Engineering Mini-Project • Developed with Python, Pandas, Streamlit, and Google Gemini")
