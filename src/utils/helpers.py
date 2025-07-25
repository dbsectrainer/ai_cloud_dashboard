from datetime import datetime
import pandas as pd


def format_currency(value):
    """Format currency values with B/M suffix."""
    if isinstance(value, str):
        return value

    if value >= 1_000_000_000:
        return f"${value/1_000_000_000:.1f}B"
    elif value >= 1_000_000:
        return f"${value/1_000_000:.1f}M"
    else:
        return f"${value:,.0f}"


def format_percentage(value):
    """Format percentage values."""
    if isinstance(value, str):
        return value
    return f"{value:.1f}%"


def get_time_range_dates(time_range):
    """Convert time range string to start and end dates."""
    end_date = datetime.now()

    ranges = {
        "1M": pd.DateOffset(months=1),
        "3M": pd.DateOffset(months=3),
        "6M": pd.DateOffset(months=6),
        "1Y": pd.DateOffset(years=1),
        "2Y": pd.DateOffset(years=2),
        "5Y": pd.DateOffset(years=5),
    }

    start_date = end_date - ranges.get(time_range, ranges["1Y"])
    return start_date, end_date


def filter_data_by_regions(data, selected_regions):
    """Filter DataFrame based on selected regions."""
    if not selected_regions:
        return data
    return data[data["Region"].isin(selected_regions)]


def calculate_growth_rate(old_value, new_value):
    """Calculate growth rate between two values."""
    if old_value == 0:
        return 0
    return ((new_value - old_value) / old_value) * 100


def get_trend_indicator(value):
    """Return trend indicator (↑ or ↓) based on value."""
    if isinstance(value, str):
        value = float(value.strip("%"))
    return "↑" if value >= 0 else "↓"
