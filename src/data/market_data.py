import pandas as pd
import numpy as np
from datetime import datetime, timedelta

DATA_AS_OF = "2026-09-22"


def get_market_share_data(role="Executive"):
    """Get market share data for cloud providers, role-based granularity and insights.
    Returns a dict with keys:
      - data: DataFrame
      - top_opportunity/key_risk (Executive)
      - regional_alert/provider_comparison (Manager)
      - raw_data_export/advanced_insights (Analyst)
    """
    df = pd.DataFrame(
        {
            "Provider": [
                "AWS",
                "Azure",
                "Google Cloud",
                "Alibaba Cloud",
                "Tencent Cloud",
                "Huawei Cloud",
                "OVHCloud",
                "IBM Cloud",
                "Oracle Cloud",
                "Salesforce",
            ],
            "Market Share (%)": [29, 24, 13, 8, 5, 5, 3, 2, 4, 1.5],
            "Region": [
                "North America",
                "North America",
                "North America",
                "Asia Pacific",
                "Asia Pacific",
                "Asia Pacific",
                "Europe",
                "North America",
                "North America",
                "North America",
            ],
            "YoY Growth (%)": [19, 34, 31, 22, 19, 15, 13, 9, 50, 10],
        }
    )
    if role == "Executive":
        return {
            "data": df.nlargest(3, "Market Share (%)"),
            "top_opportunity": "Asia Pacific cloud growth (25% YoY) is the #1 expansion opportunity.",
            "key_risk": "North America market share is declining by 2%.",
        }
    elif role == "Manager":
        comparison = df.groupby("Region")["Market Share (%)"].sum().to_dict()
        return {
            "data": df.groupby("Region").apply(lambda x: x).reset_index(drop=True),
            "regional_alert": "Europe's market share is shrinking. Monitor compliance changes.",
            "provider_comparison": comparison,
        }
    else:  # Analyst
        outlier = df.loc[df["YoY Growth (%)"].idxmax()]
        return {
            "data": df,
            "raw_data_export": df.to_csv(index=False),
            "advanced_insights": f"Highest YoY growth: {outlier['Provider']} ({outlier['YoY Growth (%)']}%)",
        }


def get_growth_trends_data(role="Executive"):
    """Get historical growth trend data, role-based granularity and insights.
    Returns a dict with keys:
      - data: DataFrame
      - trend_summary (Executive/Manager)
      - raw_data_export/advanced_insights (Analyst)
    """
    dates = pd.date_range(start="2026-01-01", end="2026-12-31", freq="ME")
    data = {
        "Date": dates,
        "North America": np.cumsum(np.random.normal(1, 0.2, len(dates))),
        "Asia Pacific": np.cumsum(np.random.normal(1.2, 0.3, len(dates))),
        "Europe": np.cumsum(np.random.normal(0.8, 0.2, len(dates))),
    }
    df = pd.DataFrame(data)
    if role == "Executive":
        return {
            "data": df[["Date", "North America"]],
            "trend_summary": "North America growth is steady but lagging APAC.",
        }
    elif role == "Manager":
        return {
            "data": df[["Date", "North America", "Asia Pacific"]],
            "trend_summary": "Asia Pacific is outpacing other regions in growth.",
        }
    else:  # Analyst
        return {
            "data": df,
            "raw_data_export": df.to_csv(index=False),
            "advanced_insights": f"Std Dev (APAC): {df['Asia Pacific'].std():.2f}",
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
        "North America": {
            "value": "148.5B",
            "growth": "17.5%",
            "share": "43%",
            "share_change": "-2%",
        },
        "Asia Pacific": {
            "value": "118.9B",
            "growth": "27.3%",
            "share": "34%",
            "share_change": "2%",
        },
        "Europe": {
            "value": "76.4B",
            "growth": "16.9%",
            "share": "23%",
            "share_change": "0%",
        },
    }
    if role == "Executive":
        return {
            "data": {"North America": metrics["North America"]},
            "summary": "North America remains the largest market, but APAC is growing fastest.",
        }
    elif role == "Manager":
        return {
            "data": {k: v for k, v in metrics.items() if k != "Europe"},
            "regional_alert": "Monitor APAC for new compliance requirements.",
        }
    else:  # Analyst
        return {
            "data": metrics,
            "raw_data_export": pd.DataFrame(metrics).T.to_csv(),
            "advanced_insights": "Europe's share change is negative; investigate causes.",
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
        "Global AI Market Size": {"value": "202.8B", "change": "35.0%"},
        "Cloud Market Growth": {"value": "24.5%", "change": "1.6%"},
        "Active Providers": {"value": "168", "change": "11"},
        "Avg. Compliance Score": {"value": "91%", "change": "2%"},
    }
    if role == "Executive":
        return {
            "data": {
                k: v
                for k, v in metrics.items()
                if k in ["Global AI Market Size", "Cloud Market Growth"]
            },
            "kpi_summary": "AI and cloud markets are both growing rapidly.",
        }
    elif role == "Manager":
        return {
            "data": {k: v for k, v in metrics.items() if k != "Avg. Compliance Score"},
            "kpi_alert": "Active providers increased by 12 this year.",
        }
    else:  # Analyst
        return {
            "data": metrics,
            "raw_data_export": pd.DataFrame(metrics).T.to_csv(),
            "advanced_insights": "Compliance score change: 5%.",
        }
