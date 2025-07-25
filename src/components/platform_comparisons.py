import streamlit as st
import pandas as pd


def display_platform_comparisons():
    """Display detailed platform comparisons."""
    st.title("🔄 Platform Comparisons")

    # Platform Feature Comparison
    st.subheader("Feature Comparison Matrix")

    feature_data = pd.DataFrame(
        {
            "Feature Category": [
                "Core Computing",
                "Storage Solutions",
                "AI/ML Services",
                "Edge Computing",
                "IoT Platform",
                "Serverless",
                "Container Services",
                "Database Options",
                "Analytics",
                "Security Features",
            ],
            "US Providers (AWS/Azure/GCP)": [
                "EC2, VM, Compute Engine",
                "S3, Blob Storage, Cloud Storage",
                "SageMaker, Azure ML, Vertex AI",
                "Outposts, Stack, Anthos",
                "IoT Core, IoT Hub, Cloud IoT",
                "Lambda, Functions, Cloud Functions",
                "EKS, AKS, GKE",
                "20+ specialized options",
                "Advanced analytics, real-time",
                "IAM, Security Center, Cloud Security",
            ],
            "EU Providers": [
                "OVHcloud Compute, Scaleway",
                "Object storage, block storage",
                "Mistral AI, Aleph Alpha",
                "Limited edge solutions",
                "Basic IoT support",
                "Function as a Service",
                "Managed Kubernetes",
                "10+ database options",
                "Basic analytics tools",
                "GDPR-compliant security",
            ],
            "China Providers": [
                "ECS, CVM",
                "OSS, Cloud Storage",
                "PAI, TIONE",
                "Edge nodes",
                "IoT Suite",
                "Function Compute",
                "Container Service",
                "15+ database options",
                "MaxCompute, ODPS",
                "Security Suite",
            ],
        }
    )

    st.dataframe(feature_data, use_container_width=True)

    # Pricing Comparison
    st.subheader("Pricing Comparison (Average for Standard Tier)")

    pricing_data = pd.DataFrame(
        {
            "Service Type": [
                "Virtual Machine (per hour)",
                "Storage (per GB/month)",
                "Data Transfer (per GB)",
                "ML Training (per hour)",
                "Container Orchestration",
            ],
            "US Providers": ["$0.10", "$0.023", "$0.09", "$0.85", "$0.10"],
            "EU Providers": ["$0.12", "$0.025", "$0.08", "$0.80", "$0.12"],
            "China Providers": ["$0.08", "$0.020", "$0.07", "$0.75", "$0.08"],
        }
    )

    st.dataframe(pricing_data, use_container_width=True)

    # Regional Strengths
    st.subheader("Regional Platform Strengths")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
        **US Providers**
        - 🌟 Most comprehensive service offerings
        - 🌟 Advanced AI/ML capabilities
        - 🌟 Global infrastructure
        - 🌟 Enterprise-grade support
        - 🌟 Extensive documentation
        """
        )

    with col2:
        st.markdown(
            """
        **EU Providers**
        - 🌟 GDPR compliance
        - 🌟 Data sovereignty
        - 🌟 Privacy-focused
        - 🌟 Regional expertise
        - 🌟 Regulatory alignment
        """
        )

    with col3:
        st.markdown(
            """
        **China Providers**
        - 🌟 Cost-effective
        - 🌟 Asia-Pacific coverage
        - 🌟 Manufacturing focus
        - 🌟 IoT capabilities
        - 🌟 Local compliance
        """
        )

    # Integration & Ecosystem
    st.subheader("Integration & Ecosystem")

    ecosystem_data = pd.DataFrame(
        {
            "Category": [
                "Third-party Integrations",
                "Developer Tools",
                "Marketplace Solutions",
                "Partner Network",
                "Open Source Support",
            ],
            "US Providers": ["10,000+", "Extensive", "5,000+", "Large", "Strong"],
            "EU Providers": ["1,000+", "Growing", "500+", "Medium", "Strong"],
            "China Providers": ["2,000+", "Moderate", "1,000+", "Large", "Moderate"],
        }
    )

    st.dataframe(ecosystem_data, use_container_width=True)

    # Use Case Recommendations
    st.subheader("Best Fit Scenarios")

    st.markdown(
        """
    **US Providers Best For:**
    - Global enterprise deployments
    - Advanced AI/ML workloads
    - Multi-region applications
    - High-compliance industries (healthcare, finance)
    
    **EU Providers Best For:**
    - GDPR-sensitive workloads
    - European market focus
    - Data sovereignty requirements
    - Privacy-critical applications
    
    **China Providers Best For:**
    - Asia-Pacific operations
    - Manufacturing industry
    - Cost-sensitive workloads
    - IoT and edge computing in Asia
    """
    )
