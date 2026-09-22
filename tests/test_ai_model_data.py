import unittest
from src.data import ai_model_data


def test_get_ai_model_comparison():
    result = ai_model_data.get_ai_model_comparison("Analyst")
    df = result["data"]
    assert not df.empty
    assert set(
        [
            "Model Family",
            "Lab / Provider",
            "Provider Region",
            "Capability Tier",
            "Context Window (tokens)",
            "Input Price ($/1M tok)",
            "Output Price ($/1M tok)",
            "Agentic/Tool-Use Score",
        ]
    ).issubset(df.columns)


def test_get_ai_model_comparison_roles():
    for role in ["Executive", "Manager", "Analyst"]:
        result = ai_model_data.get_ai_model_comparison(role)
        assert not result["data"].empty


def test_manager_view_preserves_provider_region():
    result = ai_model_data.get_ai_model_comparison("Manager")
    assert "Provider Region" in result["data"].columns


def test_get_model_pricing_trend():
    result = ai_model_data.get_model_pricing_trend()
    df = result["data"]
    assert not df.empty
    assert "Quarter" in df.columns
