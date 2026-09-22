import streamlit as st

try:
    from data.ai_model_data import get_ai_model_comparison, DATA_AS_OF
    from utils.helpers import data_as_of_caption
    from visualizations.ai_model_plots import (
        create_model_pricing_scatter,
        create_model_capability_radar,
        create_model_pricing_bar,
    )
except ImportError:
    from src.data.ai_model_data import get_ai_model_comparison, DATA_AS_OF
    from src.utils.helpers import data_as_of_caption
    from src.visualizations.ai_model_plots import (
        create_model_pricing_scatter,
        create_model_capability_radar,
        create_model_pricing_bar,
    )


def display_ai_model_comparison(role="Executive"):
    """Display frontier AI model family comparison."""
    st.title("🧠 AI Model Comparison")
    data_as_of_caption(DATA_AS_OF)

    model_dict = get_ai_model_comparison(role)
    model_data = model_dict["data"]

    st.subheader("Frontier Model Landscape")
    st.dataframe(model_data, use_container_width=True)

    if role == "Executive":
        st.success(model_dict.get("top_opportunity", ""))
        st.warning(model_dict.get("key_risk", ""))
    elif role == "Manager":
        st.info(model_dict.get("regional_alert", ""))
        st.write(
            "**Provider Comparison (avg. Agentic Score):**",
            model_dict.get("provider_comparison", {}),
        )
    elif role == "Analyst":
        st.write(model_dict.get("advanced_insights", ""))
        st.download_button(
            "Download AI Model Data (CSV)",
            model_dict.get("raw_data_export", ""),
            file_name="ai_model_data.csv",
        )

    st.subheader("Pricing vs. Context Window")
    st.plotly_chart(create_model_pricing_scatter(model_data), use_container_width=True)

    st.subheader("Frontier Capability Comparison")
    st.plotly_chart(create_model_capability_radar(model_data), use_container_width=True)

    st.subheader("Token Pricing by Model")
    st.plotly_chart(create_model_pricing_bar(model_data), use_container_width=True)

    st.subheader("Best Fit by Capability Tier")
    st.markdown("""
    **Frontier tier:** Complex, long-horizon agentic work, large codebases, and
    multi-step reasoning where accuracy matters more than per-token cost.

    **Advanced tier:** General-purpose production workloads balancing capability
    and cost, including most customer-facing assistants and internal tooling.

    **Efficient tier:** High-volume, latency-sensitive tasks (classification,
    extraction, simple chat) where cost-per-request dominates the decision.
    """)
