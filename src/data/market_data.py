import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def get_market_share_data():
    """Get market share data for cloud providers."""
    return pd.DataFrame({
        "Provider": ["AWS", "Azure", "Google Cloud", "Alibaba Cloud", "Tencent Cloud", 
                    "Huawei Cloud", "OVHCloud", "IBM Cloud", "Oracle Cloud", "Salesforce"],
        "Market Share (%)": [32, 22, 11, 9, 6, 5, 3, 2.5, 2, 1.5],
        "Region": ["North America", "North America", "North America", 
                  "Asia Pacific", "Asia Pacific", "Asia Pacific", 
                  "Europe", "North America", "North America", "North America"],
        "YoY Growth (%)": [15, 21, 18, 25, 20, 17, 14, 10, 12, 8]
    })

def get_growth_trends_data():
    """Get historical growth trend data."""
    dates = pd.date_range(start='2023-01-01', end='2024-12-31', freq='M')
    return pd.DataFrame({
        'Date': dates,
        'North America': np.cumsum(np.random.normal(1, 0.2, len(dates))),
        'Asia Pacific': np.cumsum(np.random.normal(1.2, 0.3, len(dates))),
        'Europe': np.cumsum(np.random.normal(0.8, 0.2, len(dates)))
    })

def get_regional_metrics():
    """Get regional market metrics."""
    return {
        "North America": {"value": "125.7B", "growth": "18.2%", "share": "45%", "share_change": "-2%"},
        "Asia Pacific": {"value": "89.3B", "growth": "24.5%", "share": "32%", "share_change": "3%"},
        "Europe": {"value": "64.1B", "growth": "15.8%", "share": "23%", "share_change": "-1%"}
    }

def get_key_metrics():
    """Get key dashboard metrics."""
    return {
        "Global AI Market Size": {"value": "150.2B", "change": "34.3%"},
        "Cloud Market Growth": {"value": "22.9%", "change": "2.1%"},
        "Active Providers": {"value": "157", "change": "12"},
        "Avg. Compliance Score": {"value": "89%", "change": "5%"}
    }
