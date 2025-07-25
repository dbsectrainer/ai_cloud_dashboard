import unittest
from src.components import metrics

def test_display_key_metrics():
    # Should not raise error with sample data
    sample = {"Test Metric": {"value": 100, "change": "+5%"}}
    try:
        metrics.display_key_metrics(sample)
    except Exception as e:
        assert False, f"display_key_metrics raised an exception: {e}"
