import streamlit as st
import pandas as pd

def calculate_recommendation_score(inputs):
    """Calculate recommendation scores based on user inputs."""
    scores = {
        "US Providers": 0,
        "EU Providers": 0,
        "China Providers": 0
    }
    
    # Industry-specific scoring
    industry_weights = {
        "Tech": {"US": 1.0, "EU": 0.9, "China": 0.8},
        "Finance": {"US": 1.0, "EU": 1.0, "China": 0.6},
        "Healthcare": {"US": 1.0, "EU": 0.9, "China": 0.5},
        "Manufacturing": {"US": 0.9, "EU": 0.8, "China": 1.0},
        "AI Research": {"US": 1.0, "EU": 0.9, "China": 0.9},
        "Government": {"US": 1.0, "EU": 0.8, "China": 0.4},
        "Other": {"US": 1.0, "EU": 0.9, "China": 0.7}
    }
    
    weights = industry_weights.get(inputs["industry"], industry_weights["Other"])
    scores["US Providers"] += weights["US"] * 100
    scores["EU Providers"] += weights["EU"] * 100
    scores["China Providers"] += weights["China"] * 100
    
    # Budget considerations
    if inputs["budget_constraint"] == "High":
        scores["China Providers"] += 20
        scores["EU Providers"] += 10
    elif inputs["budget_constraint"] == "Low":
        scores["US Providers"] += 20
    
    # Data sovereignty requirements
    if inputs["data_sovereignty"] == "Must stay in country":
        scores["US Providers"] -= 20
        scores["China Providers"] -= 40
        if inputs["region"] == "Europe":
            scores["EU Providers"] += 30
    
    # Compliance requirements
    if inputs["compliance_needs"]["GDPR"]:
        scores["EU Providers"] += 30
        scores["US Providers"] += 20
        scores["China Providers"] -= 20
    if inputs["compliance_needs"]["HIPAA"]:
        scores["US Providers"] += 30
        scores["EU Providers"] += 10
        scores["China Providers"] -= 20
    if inputs["compliance_needs"]["FedRAMP"]:
        scores["US Providers"] += 40
        scores["EU Providers"] -= 10
        scores["China Providers"] -= 30
    
    # Technical requirements
    if inputs["tech_requirements"]["AI/ML"]:
        scores["US Providers"] += 20
        scores["China Providers"] += 20
    if inputs["tech_requirements"]["Edge Computing"]:
        scores["US Providers"] += 15
        scores["EU Providers"] += 15
    if inputs["tech_requirements"]["IoT"]:
        scores["China Providers"] += 20
        scores["EU Providers"] += 15
    
    # Normalize scores between 0 and 100
    max_score = max(scores.values())
    if max_score > 100:
        scores = {k: (v/max_score) * 100 for k, v in scores.items()}
    
    return scores

def display_decision_helper():
    """Display the enhanced decision helper interface."""
    st.title("🤖 AI & Cloud Decision Helper")
    
    # Basic Information
    st.subheader("Organization Profile")
    col1, col2 = st.columns(2)
    
    with col1:
        industry = st.selectbox(
            "Industry",
            ["Tech", "Finance", "Healthcare", "Manufacturing", 
             "AI Research", "Government", "Other"]
        )
        region = st.selectbox(
            "Primary Region of Operation",
            ["North America", "Europe", "Asia", "Global"]
        )
    
    with col2:
        budget_constraint = st.select_slider(
            "Budget Constraint Level",
            options=["Low", "Medium", "High"]
        )
        data_sovereignty = st.selectbox(
            "Data Sovereignty Requirements",
            ["No specific requirements", "Prefer local storage", "Must stay in country"]
        )
    
    # Compliance Requirements
    st.subheader("Compliance Requirements")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        gdpr = st.checkbox("GDPR Compliance")
        hipaa = st.checkbox("HIPAA Compliance")
    with col2:
        fedramp = st.checkbox("FedRAMP Compliance")
        pci = st.checkbox("PCI DSS Compliance")
    with col3:
        sox = st.checkbox("SOX Compliance")
        iso = st.checkbox("ISO 27001 Compliance")
    
    # Technical Requirements
    st.subheader("Technical Requirements")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        ai_ml = st.checkbox("AI/ML Capabilities")
        serverless = st.checkbox("Serverless Computing")
    with col2:
        edge = st.checkbox("Edge Computing")
        containers = st.checkbox("Container Orchestration")
    with col3:
        iot = st.checkbox("IoT Services")
        blockchain = st.checkbox("Blockchain Services")
    
    # Calculate recommendation
    inputs = {
        "industry": industry,
        "region": region,
        "budget_constraint": budget_constraint,
        "data_sovereignty": data_sovereignty,
        "compliance_needs": {
            "GDPR": gdpr,
            "HIPAA": hipaa,
            "FedRAMP": fedramp,
            "PCI": pci,
            "SOX": sox,
            "ISO": iso
        },
        "tech_requirements": {
            "AI/ML": ai_ml,
            "Serverless": serverless,
            "Edge Computing": edge,
            "Containers": containers,
            "IoT": iot,
            "Blockchain": blockchain
        }
    }
    
    scores = calculate_recommendation_score(inputs)
    
    # Display recommendations
    st.subheader("Recommendations")
    
    # Display scores as metrics
    cols = st.columns(3)
    for i, (provider, score) in enumerate(scores.items()):
        with cols[i]:
            st.metric(provider, f"{score:.1f}%")
    
    # Detailed recommendations
    st.markdown("### Detailed Analysis")
    
    # Sort providers by score
    sorted_providers = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    
    for provider, score in sorted_providers:
        if score > 70:
            st.success(f"✅ **{provider}** ({score:.1f}%) - Strongly Recommended")
        elif score > 50:
            st.warning(f"⚠️ **{provider}** ({score:.1f}%) - Consider with Caution")
        else:
            st.error(f"❌ **{provider}** ({score:.1f}%) - Not Recommended")
    
    # Additional considerations
    st.markdown("### Additional Considerations")
    considerations = []
    
    if any(inputs["compliance_needs"].values()):
        considerations.append("- Ensure detailed compliance verification for chosen providers")
    if inputs["data_sovereignty"] != "No specific requirements":
        considerations.append("- Review data residency requirements and provider capabilities")
    if budget_constraint == "High":
        considerations.append("- Consider multi-cloud strategy to optimize costs")
    if any(inputs["tech_requirements"].values()):
        considerations.append("- Verify specific technical capabilities with provider documentation")
    
    for consideration in considerations:
        st.markdown(consideration)
