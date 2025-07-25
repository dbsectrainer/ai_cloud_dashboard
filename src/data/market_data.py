import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def get_market_share_data(role="Executive"):
    """Get market share data for cloud providers, role-based granularity and insights.
    Returns a dict with keys:
      - data: DataFrame
      - top_opportunity/key_risk (Executive)
      - regional_alert/provider_comparison (Manager)
      - raw_data_export/advanced_insights (Analyst)
    """
    df = pd.DataFrame({
        "Provider": ["AWS", "Azure", "Google Cloud", "Alibaba Cloud", "Tencent Cloud", 
                    "Huawei Cloud", "OVHCloud", "IBM Cloud", "Oracle Cloud", "Salesforce"],
        "Market Share (%)": [32, 22, 11, 9, 6, 5, 3, 2.5, 2, 1.5],
        "Region": ["North America", "North America", "North America", 
                  "Asia Pacific", "Asia Pacific", "Asia Pacific", 
                  "Europe", "North America", "North America", "North America"],
        "YoY Growth (%)": [15, 21, 18, 25, 20, 17, 14, 10, 12, 8]
    })
    if role == "Executive":
        return {
            "data": df.nlargest(3, "Market Share (%)"),
            "top_opportunity": "Asia Pacific cloud growth (25% YoY) is the #1 expansion opportunity.",
            "key_risk": "North America market share is declining by 2%."
        }
    elif role == "Manager":
        comparison = df.groupby("Region")["Market Share (%)"].sum().to_dict()
        return {
            "data": df.groupby("Region").apply(lambda x: x).reset_index(drop=True),
            "regional_alert": "Europe's market share is shrinking. Monitor compliance changes.",
            "provider_comparison": comparison
        }
    else:  # Analyst
        outlier = df.loc[df["YoY Growth (%)"].idxmax()]
        return {
            "data": df,
            "raw_data_export": df.to_csv(index=False),
            "advanced_insights": f"Highest YoY growth: {outlier['Provider']} ({outlier['YoY Growth (%)']}%)"
        }

def get_growth_trends_data(role="Executive"):
    """Get historical growth trend data, role-based granularity and insights.
    Returns a dict with keys:
      - data: DataFrame
      - trend_summary (Executive/Manager)
      - raw_data_export/advanced_insights (Analyst)
    """
    dates = pd.date_range(start='2025-01-01', end='2025-12-31', freq='ME')
    data = {
        'Date': dates,
        'North America': np.cumsum(np.random.normal(1, 0.2, len(dates))),
        'Asia Pacific': np.cumsum(np.random.normal(1.2, 0.3, len(dates))),
        'Europe': np.cumsum(np.random.normal(0.8, 0.2, len(dates)))
    }
    df = pd.DataFrame(data)
    if role == "Executive":
        return {
            "data": df[["Date", "North America"]],
            "trend_summary": "North America growth is steady but lagging APAC."
        }
    elif role == "Manager":
        return {
            "data": df[["Date", "North America", "Asia Pacific"]],
            "trend_summary": "Asia Pacific is outpacing other regions in growth."
        }
    else:  # Analyst
        return {
            "data": df,
            "raw_data_export": df.to_csv(index=False),
            "advanced_insights": f"Std Dev (APAC): {df['Asia Pacific'].std():.2f}"
        }

def get_regional_metrics(role="Executive"):
    """Get regional market metrics, role-based granularity and insights.
    Returns a dict with keys:
      - data: dict
      - summary (Executive)
      - regional_alert (Manager)
      - raw_data_export/advanced_insights (Analyst)
    """
    metrics = {
        "North America": {"value": "125.7B", "growth": "18.2%", "share": "45%", "share_change": "-2%"},
        "Asia Pacific": {"value": "89.3B", "growth": "24.5%", "share": "32%", "share_change": "3%"},
        "Europe": {"value": "64.1B", "growth": "15.8%", "share": "23%", "share_change": "-1%"}
    }
    if role == "Executive":
        return {
            "data": {"North America": metrics["North America"]},
            "summary": "North America remains the largest market, but APAC is growing fastest."
        }
    elif role == "Manager":
        return {
            "data": {k: v for k, v in metrics.items() if k != "Europe"},
            "regional_alert": "Monitor APAC for new compliance requirements."
        }
    else:  # Analyst
        return {
            "data": metrics,
            "raw_data_export": pd.DataFrame(metrics).T.to_csv(),
            "advanced_insights": "Europe's share change is negative; investigate causes."
        }

def get_key_metrics(role="Executive"):
    """Get key dashboard metrics, role-based granularity and insights.
    Returns a dict with keys:
      - data: dict
      - kpi_summary (Executive)
      - kpi_alert (Manager)
      - raw_data_export/advanced_insights (Analyst)
    """
    metrics = {
        "Global AI Market Size": {"value": "150.2B", "change": "34.3%"},
        "Cloud Market Growth": {"value": "22.9%", "change": "2.1%"},
        "Active Providers": {"value": "157", "change": "12"},
        "Avg. Compliance Score": {"value": "89%", "change": "5%"}
    }
    if role == "Executive":
        return {
            "data": {k: v for k, v in metrics.items() if k in ["Global AI Market Size", "Cloud Market Growth"]},
            "kpi_summary": "AI and cloud markets are both growing rapidly."
        }
    elif role == "Manager":
        return {
            "data": {k: v for k, v in metrics.items() if k != "Avg. Compliance Score"},
            "kpi_alert": "Active providers increased by 12 this year."
        }
    else:  # Analyst
        return {
            "data": metrics,
            "raw_data_export": pd.DataFrame(metrics).T.to_csv(),
            "advanced_insights": "Compliance score change: 5%."
        }
