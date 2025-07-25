import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np


def create_trend_forecast():
    """Create forecast visualization for key trends."""
    # Create yearly data points
    years = ["2025", "2026", "2027", "2028", "2029"]

    # Create market data dictionary
    market_data = {
        "Date": years,
        "AI Market Size ($B)": [220, 310, 420, 580, 750],
        "Cloud Market Size ($B)": [650, 840, 1100, 1400, 1800],
        "Edge Computing ($B)": [85, 140, 230, 380, 600],
    }

    # Create DataFrame
    data = pd.DataFrame(market_data)

    fig = go.Figure()

    for column in [
        "AI Market Size ($B)",
        "Cloud Market Size ($B)",
        "Edge Computing ($B)",
    ]:
        fig.add_trace(
            go.Scatter(
                x=data["Date"],
                y=data[column],
                name=column,
                mode="lines+markers",
                hovertemplate="%{y:$.0f}B<extra></extra>",
            )
        )

    fig.update_layout(
        title="Market Size Projections (2025-2029)",
        xaxis_title="Year",
        yaxis_title="Market Size (Billion USD)",
        hovermode="x unified",
    )

    return fig


def display_future_trends():
    """Display future trends and predictions."""
    st.title("🚀 Future Trends")

    # Market Projections
    st.plotly_chart(create_trend_forecast(), use_container_width=True)

    # Key Trends
    st.subheader("Key Trends Shaping the Future")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
        **Technology Trends**
        - 🧠 Advanced AI Models & Quantum Computing
        - 🌐 Edge Computing & 6G Integration
        - 🤖 Autonomous Cloud Operations
        - 🔗 Web3 & Decentralized Cloud
        - 🛡️ Zero-Trust Security Architecture
        
        **Market Trends**
        - 📈 Regional Cloud Market Growth
        - 🌍 Increased Market Fragmentation
        - 💰 New Pricing Models
        - 🤝 Strategic Partnerships
        - 🔄 Multi-Cloud Adoption
        """
        )

    with col2:
        st.markdown(
            """
        **Regulatory Trends**
        - 📜 AI Regulation Evolution
        - 🔒 Data Sovereignty Laws
        - 🌱 Green Computing Standards
        - 🤝 Cross-Border Agreements
        - ⚖️ Platform Governance
        
        **Industry Impact**
        - 🏭 Manufacturing Revolution
        - 🏥 Healthcare Transformation
        - 🏦 Financial Services Evolution
        - 🏛️ Government Modernization
        - 🎮 Digital Entertainment
        """
        )

    # Regional Development
    st.subheader("Regional Development Forecast")

    regional_forecast = pd.DataFrame(
        {
            "Region": [
                "North America",
                "Europe",
                "Asia Pacific",
                "Latin America",
                "Middle East",
            ],
            "Growth Rate": [25, 30, 35, 28, 32],
            "Key Focus Areas": [
                "AI/ML, Quantum",
                "Privacy, Green Tech",
                "IoT, Manufacturing",
                "Cloud Migration",
                "Smart Cities",
            ],
            "Investment Priority": ["High", "High", "Very High", "Medium", "High"],
        }
    )

    st.dataframe(regional_forecast, use_container_width=True)

    # Emerging Technologies
    st.subheader("Emerging Technologies Impact")

    impact_data = pd.DataFrame(
        {
            "Technology": [
                "Quantum Computing",
                "6G Networks",
                "Autonomous Systems",
                "Green Computing",
                "Neural Interfaces",
            ],
            "Expected Impact": [
                "Revolutionary",
                "Transformative",
                "Significant",
                "High",
                "Moderate",
            ],
            "Timeline": [
                "5-7 years",
                "4-6 years",
                "2-4 years",
                "1-3 years",
                "7-10 years",
            ],
            "Readiness": [
                "Research Phase",
                "Early Development",
                "Early Adoption",
                "Scaling",
                "Research Phase",
            ],
        }
    )

    st.dataframe(impact_data, use_container_width=True)

    # Strategic Recommendations
    st.subheader("Strategic Recommendations")

    st.markdown(
        """
    **For Government Agencies:**
    1. 📋 Develop comprehensive AI/cloud governance frameworks
    2. 🔒 Strengthen cybersecurity and data protection measures
    3. 🌐 Foster international cooperation in standards development
    4. 📚 Invest in workforce development and training
    5. 🤝 Create public-private partnership programs
    
    **For Enterprises:**
    1. 🎯 Adopt multi-cloud strategies for resilience
    2. 🔄 Implement continuous learning and adaptation
    3. 🛡️ Focus on security and compliance automation
    4. 💡 Invest in AI/ML capabilities
    5. 🌱 Prioritize sustainable computing practices
    
    **For Technology Providers:**
    1. 🔍 Focus on regional market requirements
    2. 🤖 Develop autonomous operations capabilities
    3. 🔐 Enhance security and compliance features
    4. 🌍 Build strong regional partnerships
    5. ♻️ Implement sustainable practices
    """
    )

    # Risk Factors
    st.subheader("Key Risk Factors to Monitor")

    risk_data = pd.DataFrame(
        {
            "Risk Category": [
                "Regulatory Changes",
                "Technology Disruption",
                "Market Competition",
                "Security Threats",
                "Environmental Impact",
            ],
            "Probability": ["High", "Medium", "High", "High", "Medium"],
            "Impact": ["Significant", "High", "Moderate", "Severe", "High"],
            "Mitigation Strategy": [
                "Proactive compliance",
                "Continuous innovation",
                "Market differentiation",
                "Enhanced security",
                "Green initiatives",
            ],
        }
    )

    st.dataframe(risk_data, use_container_width=True)
