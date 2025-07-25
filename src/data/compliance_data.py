from datetime import datetime
import pandas as pd

def get_compliance_matrix():
    """Get compliance requirements matrix."""
    return pd.DataFrame({
        "Requirement": [
            "GDPR", "HIPAA", "FedRAMP", "SOC 2", "ISO 27001", 
            "CCPA", "PCI DSS", "NIST"
        ],
        "US Providers": [
            "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅"
        ],
        "EU Providers": [
            "✅", "⚠️", "❌", "✅", "✅", "✅", "✅", "⚠️"
        ],
        "China Providers": [
            "❌", "❌", "❌", "⚠️", "✅", "❌", "⚠️", "❌"
        ]
    })

def get_security_certifications():
    """Get security certification data."""
    return pd.DataFrame({
        "Provider": ["AWS", "Azure", "GCP", "Alibaba", "Tencent"],
        "Certifications": [
            ["ISO 27001", "SOC 2", "FedRAMP", "HIPAA"],
            ["ISO 27001", "SOC 2", "FedRAMP", "HIPAA"],
            ["ISO 27001", "SOC 2", "FedRAMP", "HIPAA"],
            ["ISO 27001", "SOC 2"],
            ["ISO 27001", "SOC 2"]
        ],
        "Risk Score": [95, 94, 93, 85, 84],
        "Last Audit": [
            datetime(2025, 1, 15),
            datetime(2025, 1, 10),
            datetime(2025, 1, 5),
            datetime(2024, 12, 20),
            datetime(2024, 12, 15)
        ]
    })

def get_data_residency_map():
    """Get data residency information."""
    return {
        "North America": {
            "regions": ["us-east", "us-west", "ca-central"],
            "providers": ["AWS", "Azure", "GCP"],
            "compliance": ["HIPAA", "FedRAMP", "SOC 2"]
        },
        "Europe": {
            "regions": ["eu-west", "eu-central", "eu-north"],
            "providers": ["AWS", "Azure", "GCP", "OVHcloud"],
            "compliance": ["GDPR", "ISO 27001"]
        },
        "Asia": {
            "regions": ["ap-east", "ap-southeast", "ap-northeast"],
            "providers": ["AWS", "Azure", "Alibaba", "Tencent"],
            "compliance": ["ISO 27001", "APEC PRP"]
        }
    }
