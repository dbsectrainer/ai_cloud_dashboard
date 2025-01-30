import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def get_performance_metrics():
    """Get performance metrics for cloud providers."""
    providers = ["AWS", "Azure", "GCP", "Alibaba", "Tencent"]
    regions = ["US East", "US West", "EU", "Asia Pacific"]
    
    data = []
    for provider in providers:
        for region in regions:
            data.append({
                "Provider": provider,
                "Region": region,
                "Latency (ms)": round(np.random.normal(50, 10), 2),
                "Uptime (%)": round(99.9 + np.random.random() * 0.09, 3),
                "IOPS": int(np.random.normal(10000, 1000)),
                "Network Throughput (Gbps)": round(np.random.normal(25, 5), 1)
            })
    
    return pd.DataFrame(data)

def get_sla_comparisons():
    """Get SLA comparisons for different services."""
    return pd.DataFrame({
        "Service Type": [
            "Compute", "Storage", "Database", "CDN", 
            "Load Balancer", "Object Storage"
        ],
        "AWS": [99.99, 99.999, 99.99, 99.9, 99.99, 99.999],
        "Azure": [99.99, 99.99, 99.99, 99.9, 99.99, 99.99],
        "GCP": [99.99, 99.99, 99.99, 99.9, 99.99, 99.99],
        "Alibaba": [99.95, 99.99, 99.95, 99.9, 99.95, 99.99],
        "Tencent": [99.95, 99.99, 99.95, 99.9, 99.95, 99.99]
    })

def get_cost_analysis():
    """Get cost analysis data for cloud services."""
    services = [
        "Compute (per vCPU/hour)",
        "Storage (per GB/month)",
        "Data Transfer (per GB)",
        "Load Balancer (per hour)",
        "Database (per hour)"
    ]
    
    return pd.DataFrame({
        "Service": services,
        "AWS": [0.0464, 0.023, 0.09, 0.025, 0.12],
        "Azure": [0.0478, 0.024, 0.087, 0.025, 0.125],
        "GCP": [0.0456, 0.022, 0.085, 0.025, 0.118],
        "Alibaba": [0.0432, 0.021, 0.081, 0.023, 0.11],
        "Tencent": [0.0428, 0.020, 0.080, 0.022, 0.108]
    })

def calculate_tco(workload_profile):
    """Calculate Total Cost of Ownership based on workload profile."""
    base_costs = {
        "AWS": {"compute": 100, "storage": 50, "network": 30, "support": 20},
        "Azure": {"compute": 98, "storage": 52, "network": 28, "support": 22},
        "GCP": {"compute": 95, "storage": 48, "network": 32, "support": 25},
        "Alibaba": {"compute": 85, "storage": 45, "network": 25, "support": 15},
        "Tencent": {"compute": 82, "storage": 43, "network": 23, "support": 12}
    }
    
    tco_data = []
    for provider, costs in base_costs.items():
        monthly_cost = sum(
            cost * workload_profile.get(category, 1) 
            for category, cost in costs.items()
        )
        yearly_cost = monthly_cost * 12
        three_year_cost = yearly_cost * 3
        
        tco_data.append({
            "Provider": provider,
            "Monthly Cost": monthly_cost,
            "Yearly Cost": yearly_cost,
            "3-Year TCO": three_year_cost,
            "Savings vs. Highest": 0  # Will be calculated after
        })
    
    df = pd.DataFrame(tco_data)
    max_tco = df["3-Year TCO"].max()
    df["Savings vs. Highest"] = ((max_tco - df["3-Year TCO"]) / max_tco * 100).round(2)
    
    return df
