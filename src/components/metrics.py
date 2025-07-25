import streamlit as st
from datetime import datetime

def display_key_metrics(metrics_data):
    """Display key metrics in a row of columns with tooltips."""
    cols = st.columns(len(metrics_data))
    tooltips = {
        "Global AI Market Size": "Total global market value for AI in 2025 (USD).",
        "Cloud Market Growth": "Year-over-year growth rate for the global cloud market.",
        "Active Providers": "Number of active cloud service providers worldwide.",
        "Avg. Compliance Score": "Average compliance score across all providers."
    }
    for col, (metric, data) in zip(cols, metrics_data.items()):
        with col:
            st.metric(
                label=metric,
                value=data["value"],
                delta=data["change"]
            )
            st.caption(tooltips.get(metric, ""))

def display_regional_metrics(regional_data):
    """Display regional metrics in columns."""
    cols = st.columns(len(regional_data))
    for col, (region, data) in zip(cols, regional_data.items()):
        with col:
            st.metric(region, data["value"], f"↑ {data['growth']}")
            st.metric("Market Share", data["share"], data["share_change"])

def display_sidebar_navigation():
    """Display sidebar navigation with additional features and feedback widget."""
    st.sidebar.title("Navigation")
    # Main navigation
    page = st.sidebar.radio(
        "Go to",
        ["Home", "Market Intelligence", "Security & Compliance", 
         "Cost Analysis", "Performance Metrics", "Decision Helper",
         "Platform Comparisons", "Learning Resources", "Future Trends"]
    )
    st.sidebar.markdown("---")
    # Filters section
    st.sidebar.subheader("Filters")
    st.sidebar.info("Use filters to customize your dashboard view.")
    selected_regions = st.sidebar.multiselect(
        "Regions",
        ["North America", "Europe", "Asia Pacific", "Latin America"],
        default=["North America", "Europe", "Asia Pacific"],
        help="Select one or more regions to filter analytics."
    )
    provider_options = ["All Providers", "AWS", "Azure", "Google Cloud", "IBM Cloud", "Oracle Cloud"]
    selected_provider = st.sidebar.selectbox(
        "Provider",
        provider_options,
        index=0,
        help="Choose a provider to drill down into specific analytics."
    )
    time_range = st.sidebar.select_slider(
        "Time Range",
        options=["1M", "3M", "6M", "1Y", "2Y", "5Y"],
        value="1Y",
        help="Select the time range for data analysis."
    )
    st.sidebar.markdown("---")
    st.sidebar.subheader("Feedback")
    feedback = st.sidebar.text_area("Share your feedback or feature requests:")
    if st.sidebar.button("Submit Feedback"):
        st.sidebar.success("Thank you for your feedback!")
    return page, selected_regions, time_range, selected_provider
