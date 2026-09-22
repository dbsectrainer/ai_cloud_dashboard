import pandas as pd
from datetime import datetime

DATA_AS_OF = "2026-09-22"


def get_ai_model_comparison(role="Executive"):
    """Get frontier AI model family comparison data, role-based granularity and insights.
    Returns a dict with keys:
      - data: DataFrame
      - top_opportunity/key_risk (Executive)
      - regional_alert/provider_comparison (Manager)
      - raw_data_export/advanced_insights (Analyst)
    """
    df = pd.DataFrame(
        {
            "Model Family": [
                "Claude Opus 4.5",
                "Claude Sonnet 4.5",
                "Claude Haiku 4.5",
                "GPT-5.1",
                "GPT-5.1 mini",
                "Gemini 3 Pro",
                "Gemini 3 Flash",
                "Grok 4",
                "Amazon Nova Premier",
                "Llama 4 Maverick",
                "Llama 4 Scout",
                "Mistral Large 3",
                "DeepSeek V3.2",
                "Qwen 3 Max",
            ],
            "Lab / Provider": [
                "Anthropic",
                "Anthropic",
                "Anthropic",
                "OpenAI",
                "OpenAI",
                "Google",
                "Google",
                "xAI",
                "Amazon",
                "Meta",
                "Meta",
                "Mistral AI",
                "DeepSeek",
                "Alibaba",
            ],
            "Provider Region": [
                "US",
                "US",
                "US",
                "US",
                "US",
                "US",
                "US",
                "US",
                "US",
                "US",
                "US",
                "EU",
                "China",
                "China",
            ],
            "Capability Tier": [
                "Frontier",
                "Advanced",
                "Efficient",
                "Frontier",
                "Efficient",
                "Frontier",
                "Efficient",
                "Frontier",
                "Advanced",
                "Advanced",
                "Efficient",
                "Advanced",
                "Advanced",
                "Advanced",
            ],
            "Context Window (tokens)": [
                200000,
                200000,
                200000,
                400000,
                400000,
                1000000,
                1000000,
                256000,
                1000000,
                1000000,
                10000000,
                256000,
                128000,
                256000,
            ],
            "Max Output (tokens)": [
                64000,
                64000,
                64000,
                128000,
                128000,
                64000,
                64000,
                64000,
                32000,
                32000,
                32000,
                32000,
                16000,
                32000,
            ],
            "Input Price ($/1M tok)": [
                5.00,
                3.00,
                1.00,
                4.00,
                0.40,
                2.50,
                0.15,
                3.00,
                2.50,
                0.35,
                0.15,
                2.00,
                0.28,
                1.60,
            ],
            "Output Price ($/1M tok)": [
                25.00,
                15.00,
                5.00,
                16.00,
                1.60,
                15.00,
                0.60,
                15.00,
                12.50,
                1.40,
                0.60,
                6.00,
                0.42,
                6.40,
            ],
            "Modality": [
                "Text, Vision, Audio",
                "Text, Vision, Audio",
                "Text, Vision",
                "Text, Vision, Audio",
                "Text, Vision",
                "Text, Vision, Audio, Video",
                "Text, Vision",
                "Text, Vision",
                "Text, Vision, Audio",
                "Text, Vision",
                "Text, Vision",
                "Text, Vision",
                "Text",
                "Text, Vision",
            ],
            "Open Weights": [
                False,
                False,
                False,
                False,
                False,
                False,
                False,
                False,
                False,
                True,
                True,
                False,
                True,
                False,
            ],
            "Release Date": [
                datetime(2025, 11, 24),
                datetime(2025, 9, 29),
                datetime(2025, 10, 15),
                datetime(2025, 11, 12),
                datetime(2025, 11, 12),
                datetime(2026, 2, 5),
                datetime(2026, 2, 5),
                datetime(2025, 7, 9),
                datetime(2025, 12, 1),
                datetime(2025, 4, 5),
                datetime(2025, 4, 5),
                datetime(2026, 3, 18),
                datetime(2025, 12, 20),
                datetime(2026, 1, 28),
            ],
            "Agentic/Tool-Use Score": [
                92,
                88,
                78,
                90,
                75,
                87,
                74,
                80,
                79,
                77,
                68,
                76,
                81,
                78,
            ],
        }
    )
    if role == "Executive":
        return {
            "data": df[df["Capability Tier"] == "Frontier"],
            "top_opportunity": "Frontier reasoning/agentic models now clear 200K+ token context as standard, unlocking whole-codebase and long-document workflows.",
            "key_risk": "Model pricing and capability shift roughly every 2-3 months; procurement decisions should assume rapid depreciation of any single vendor lock-in.",
        }
    elif role == "Manager":
        comparison = (
            df.groupby("Lab / Provider")["Agentic/Tool-Use Score"]
            .mean()
            .round(1)
            .to_dict()
        )
        return {
            "data": df.sort_values("Provider Region").reset_index(drop=True),
            "regional_alert": "Open-weight model families (Meta, DeepSeek) now match or beat prior-generation closed frontier models on cost-efficiency.",
            "provider_comparison": comparison,
        }
    else:  # Analyst
        outlier = df.loc[df["Agentic/Tool-Use Score"].idxmax()]
        return {
            "data": df,
            "raw_data_export": df.to_csv(index=False),
            "advanced_insights": f"Highest Agentic/Tool-Use Score: {outlier['Model Family']} ({outlier['Agentic/Tool-Use Score']}).",
        }


def get_model_pricing_trend():
    """Get a small illustrative time series of blended frontier model pricing decline.
    Returns a dict with keys:
      - data: DataFrame
      - trend_summary: str
    """
    df = pd.DataFrame(
        {
            "Quarter": [
                "2025-Q2",
                "2025-Q3",
                "2025-Q4",
                "2026-Q1",
                "2026-Q2",
                "2026-Q3",
            ],
            "Blended Price ($/1M tok, input+output avg)": [
                9.20,
                7.80,
                6.50,
                5.60,
                4.90,
                4.20,
            ],
        }
    )
    return {
        "data": df,
        "trend_summary": "Blended frontier model pricing has fallen roughly 55% over the past six quarters.",
    }
