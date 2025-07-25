import streamlit as st
from datetime import datetime

def display_key_metrics(metrics_data):
    """Display key metrics in a row of columns."""
    cols = st.columns(len(metrics_data))
    for col, (metric, data) in zip(cols, metrics_data.items()):
        with col:
            st.metric(
                label=metric,
                value=data["value"],
                delta=data["change"]
            )

def display_regional_metrics(regional_data):
    """Display regional metrics in columns."""
    cols = st.columns(len(regional_data))
    for col, (region, data) in zip(cols, regional_data.items()):
        with col:
            st.metric(region, data["value"], f"↑ {data['growth']}")
            st.metric("Market Share", data["share"], data["share_change"])

def display_sidebar_navigation():
    """Display sidebar navigation with additional features."""
    st.sidebar.title("Navigation")
    
    # Main navigation
    page = st.sidebar.radio(
        "Go to",
        ["Home", "Market Intelligence", "Security & Compliance", 
         "Cost Analysis", "Performance Metrics", "Decision Helper",
         "Platform Comparisons", "Learning Resources", "Future Trends"]
    )
    
    # Additional sidebar components
    st.sidebar.markdown("---")
    
    # Filters section
    st.sidebar.subheader("Filters")
    selected_regions = st.sidebar.multiselect(
        "Regions",
        ["North America", "Europe", "Asia Pacific", "Latin America"],
        default=["North America", "Europe", "Asia Pacific"]
    )
    
    # Provider filter for drill-down
    provider_options = ["All Providers", "AWS", "Azure", "Google Cloud", "IBM Cloud", "Oracle Cloud"]
    selected_provider = st.sidebar.selectbox(
        "Provider",
        provider_options,
        index=0
    )
    
    time_range = st.sidebar.select_slider(
        "Time Range",
        options=["1M", "3M", "6M", "1Y", "2Y", "5Y"],
        value="1Y"
    )
    
    # Update indicator
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"🔄 Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return page, selected_regions, time_range, selected_provider
