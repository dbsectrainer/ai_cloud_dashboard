import streamlit as st
from datetime import datetime
import numpy as np

# Import custom modules
from data.market_data import (
    get_market_share_data,
    get_growth_trends_data,
    get_regional_metrics,
    get_key_metrics
)
from data.compliance_data import (
    get_compliance_matrix,
    get_security_certifications,
    get_data_residency_map
)
from data.performance_data import (
    get_performance_metrics,
    get_sla_comparisons,
    get_cost_analysis,
    calculate_tco
)
from visualizations.plots import (
    create_market_share_treemap,
    create_growth_trends_line,
    create_provider_comparison_radar
)
from visualizations.compliance_plots import (
    create_compliance_heatmap,
    create_security_score_gauge,
    create_data_residency_map,
    create_certification_timeline
)
from visualizations.performance_plots import (
    create_performance_radar,
    create_latency_heatmap,
    create_sla_comparison,
    create_cost_comparison,
    create_tco_analysis
)
from components.metrics import (
    display_key_metrics,
    display_regional_metrics,
    display_sidebar_navigation
)
from components.decision_helper import display_decision_helper
from components.platform_comparisons import display_platform_comparisons
from components.learning_resources import display_learning_resources
from components.future_trends import display_future_trends
from utils.helpers import (
    filter_data_by_regions,
    get_time_range_dates
)

# Set up Streamlit page configuration
st.set_page_config(
    page_title="Global AI & Cloud Intelligence Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    # User Role Selector
    st.sidebar.markdown("## User Role")
    user_role = st.sidebar.selectbox(
        "Select your role:",
        ["Executive", "Manager", "Analyst"],
        index=0,
        help="Choose a role to customize the dashboard view."
    )

    # Get navigation and filter selections (now includes provider)
    page, selected_regions, time_range, selected_provider = display_sidebar_navigation()

    # Home Page
    if page == "Home":
        st.title("🌐 Global AI & Cloud Intelligence Dashboard")
        key_metrics = get_key_metrics(user_role)
        regional_metrics = get_regional_metrics(user_role)
        display_key_metrics(key_metrics["data"])
        display_regional_metrics(regional_metrics["data"])
        # Show role-based insights
        if user_role == "Executive":
            st.info(key_metrics.get("kpi_summary", ""))
            st.success(get_market_share_data(user_role).get("top_opportunity", ""))
            st.warning(get_market_share_data(user_role).get("key_risk", ""))
        elif user_role == "Manager":
            st.info(key_metrics.get("kpi_alert", ""))
            st.info(get_market_share_data(user_role).get("regional_alert", ""))
            st.write("**Provider Comparison:**", get_market_share_data(user_role).get("provider_comparison", {}))
        elif user_role == "Analyst":
            st.info(key_metrics.get("advanced_insights", ""))
            st.write(get_market_share_data(user_role).get("advanced_insights", ""))
            st.download_button("Download Market Data (CSV)", get_market_share_data(user_role).get("raw_data_export", ""), file_name="market_data.csv")
        
        st.markdown("""
        ## Strategic Intelligence Platform for Government & Enterprise
        
        This dashboard provides comprehensive insights into the global AI and cloud computing landscape, 
        enabling data-driven decision making for government agencies and enterprises.

        ### Key Features:
        - 📊 **Real-time Market Intelligence**: Track global market movements and competitive dynamics
        - 🛡️ **Security & Compliance**: Monitor regulatory compliance and security standards
        - 💰 **Cost Analysis**: Compare pricing and calculate TCO across providers
        - ⚡ **Performance Metrics**: Track real-time performance and reliability metrics
        - 🤖 **Decision Support**: AI-powered recommendations for strategic planning
        """)

        # --- AI Insights Panel ---
        st.markdown("---")
        st.subheader("🤖 AI Insights")
        st.info("Automated trends, anomalies, and predictive analytics for enterprise decision-making.")
        
        # Example: Trend detection on market growth
        try:
            growth_trends = get_growth_trends_data(user_role)
            growth_data = growth_trends["data"]
            st.caption(growth_trends.get("trend_summary", ""))
            # Simple trend: compare last and first value
            if len(growth_data) > 1:
                first = growth_data.iloc[0][1:].mean()
                last = growth_data.iloc[-1][1:].mean()
                trend = "increasing" if last > first else "decreasing"
                st.write(f"**Market growth trend:** {trend.title()} ({first:.2f}% → {last:.2f}%)")
            # Anomaly detection (simple: large jump)
            numeric_growth_data = growth_data.select_dtypes(include=[np.number])
            diffs = numeric_growth_data.iloc[-5:].diff().abs().mean().mean()
            if diffs > 5:
                st.warning(f"Significant recent volatility detected in market growth (avg. change: {diffs:.2f}%)")
        except Exception as e:
            st.write("AI Insights unavailable: ", e)

    # Market Intelligence Page
    elif page == "Market Intelligence":
        st.title("📊 Global Market Intelligence")
        tab1, tab2, tab3 = st.tabs(["Market Share", "Growth Trends", "Regional Analysis"])
        # Get and filter data based on selections
        market_data_dict = get_market_share_data(user_role)
        market_data = filter_data_by_regions(market_data_dict["data"], selected_regions)
        growth_data_dict = get_growth_trends_data(user_role)
        growth_data = growth_data_dict["data"]
        # Provider drill-down
        if selected_provider != "All Providers":
            market_data = market_data[market_data["Provider"] == selected_provider]
            growth_data = growth_data  # (implement provider filter if needed)
        with tab1:
            st.plotly_chart(create_market_share_treemap(market_data), use_container_width=True)
            # Show role-based insights
            if user_role == "Executive":
                st.success(market_data_dict.get("top_opportunity", ""))
                st.warning(market_data_dict.get("key_risk", ""))
            elif user_role == "Manager":
                st.info(market_data_dict.get("regional_alert", ""))
                st.write("**Provider Comparison:**", market_data_dict.get("provider_comparison", {}))
            elif user_role == "Analyst":
                st.write(market_data_dict.get("advanced_insights", ""))
                st.download_button("Download Market Data (CSV)", market_data_dict.get("raw_data_export", ""), file_name="market_data.csv")
        with tab2:
            st.plotly_chart(create_growth_trends_line(growth_data), use_container_width=True)
            st.caption(growth_data_dict.get("trend_summary", ""))
            if user_role == "Analyst":
                st.write(growth_data_dict.get("advanced_insights", ""))
                st.download_button("Download Growth Data (CSV)", growth_data_dict.get("raw_data_export", ""), file_name="growth_data.csv")
        with tab3:
            if user_role in ["Manager", "Analyst"]:
                display_regional_metrics(get_regional_metrics(user_role)["data"])
            st.plotly_chart(create_provider_comparison_radar(market_data), use_container_width=True)

    # Security & Compliance Page
    elif page == "Security & Compliance":
        st.title("🛡️ Security & Compliance Dashboard")
        
        # Get compliance and security data
        compliance_data = get_compliance_matrix()
        security_data = get_security_certifications()
        residency_data = get_data_residency_map()
        
        # Security Score Overview
        st.plotly_chart(create_security_score_gauge(security_data), use_container_width=True)
        
        # Compliance Matrix
        if user_role in ["Manager", "Analyst"]:
            st.subheader("Compliance Requirements by Region")
            st.plotly_chart(create_compliance_heatmap(compliance_data), use_container_width=True)
        
        # Security Certifications Timeline
        if user_role == "Analyst":
            st.subheader("Security Certifications & Audit History")
            st.plotly_chart(create_certification_timeline(security_data), use_container_width=True)
        
        # Data Residency Map
        st.subheader("Global Data Residency")
        st.plotly_chart(create_data_residency_map(residency_data), use_container_width=True)

    # Cost Analysis Page
    elif page == "Cost Analysis":
        st.title("💰 Cost Analysis Dashboard")
        
        # Get cost data
        cost_data = get_cost_analysis()
        
        # TCO Calculator
        st.subheader("Total Cost of Ownership Calculator")
        
        # Workload profile inputs
        col1, col2 = st.columns(2)
        with col1:
            compute_factor = st.slider("Compute Intensity", 0.5, 5.0, 1.0)
            storage_factor = st.slider("Storage Requirements", 0.5, 5.0, 1.0)
        with col2:
            network_factor = st.slider("Network Usage", 0.5, 5.0, 1.0)
            support_factor = st.slider("Support Level", 0.5, 5.0, 1.0)
        
        # Calculate TCO
        workload_profile = {
            "compute": compute_factor,
            "storage": storage_factor,
            "network": network_factor,
            "support": support_factor
        }
        tco_data = calculate_tco(workload_profile)
        
        # Display TCO Analysis
        st.plotly_chart(create_tco_analysis(tco_data), use_container_width=True)
        
        # Service Cost Comparison
        if user_role in ["Manager", "Analyst"]:
            st.subheader("Service Cost Comparison")
            st.plotly_chart(create_cost_comparison(cost_data), use_container_width=True)

    # Performance Metrics Page
    elif page == "Performance Metrics":
        st.title("⚡ Performance Metrics Dashboard")
        performance_data = get_performance_metrics()
        sla_data = get_sla_comparisons()
        # Performance Overview
        st.plotly_chart(create_performance_radar(performance_data), use_container_width=True)
        # Role-based insights and advanced analytics
        if user_role == "Executive":
            top_perf = performance_data.loc[performance_data['Uptime (%)'].idxmax()]
            st.success(f"Top Performer: {top_perf['Provider']} (Uptime: {top_perf['Uptime (%)']}%)")
            st.info("Executive View: Focus on uptime and reliability KPIs.")
        elif user_role == "Manager":
            st.subheader("Global Latency Analysis")
            st.plotly_chart(create_latency_heatmap(performance_data), use_container_width=True)
            slowest = performance_data.loc[performance_data['Latency (ms)'].idxmax()]
            st.warning(f"Latency Alert: {slowest['Provider']} highest latency ({slowest['Latency (ms)']} ms)")
            st.info("Manager View: Monitor latency and regional performance.")
        elif user_role == "Analyst":
            st.subheader("Global Latency Analysis")
            st.plotly_chart(create_latency_heatmap(performance_data), use_container_width=True)
            st.subheader("Service Level Agreements")
            st.plotly_chart(create_sla_comparison(sla_data), use_container_width=True)
            st.write("Advanced Analytics: Outlier Detection")
            outlier = performance_data.loc[performance_data['Latency (ms)'].idxmax()]
            st.write(f"Provider with highest latency: {outlier['Provider']} ({outlier['Latency (ms)']} ms)")
            st.download_button("Download Performance Data (CSV)", performance_data.to_csv(index=False), file_name="performance_data.csv")

    # Decision Helper Page
    elif page == "Decision Helper":
        display_decision_helper()
    
    # Platform Comparisons Page
    elif page == "Platform Comparisons":
        display_platform_comparisons()
    
    # Learning Resources Page
    elif page == "Learning Resources":
        display_learning_resources()
    
    # Future Trends Page
    elif page == "Future Trends":
        display_future_trends()

    # Data Privacy & Export section in sidebar
    st.sidebar.markdown("---")
    st.sidebar.subheader("Data Privacy & Export")
    st.sidebar.markdown("View our [Privacy Policy](docs/security.md)")
    if st.sidebar.button("Export My Data"):
        st.sidebar.success("Your data export request has been received. (Feature coming soon)")

if __name__ == "__main__":
    main()
