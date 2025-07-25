import unittest
from src.data import performance_data

def test_get_performance_metrics():
    df = performance_data.get_performance_metrics()
    assert not df.empty
    assert set(["Provider", "Region", "Latency (ms)", "Uptime (%)", "IOPS", "Network Throughput (Gbps)"]).issubset(df.columns)

def test_calculate_tco():
    profile = {"compute": 1, "storage": 1, "network": 1, "support": 1}
    df = performance_data.calculate_tco(profile)
    assert not df.empty
    assert "Provider" in df.columns
    assert "3-Year TCO" in df.columns
