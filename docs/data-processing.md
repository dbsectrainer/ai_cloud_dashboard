# Data Processing Guide

This guide explains how "data" actually works in the AI Cloud Dashboard.
There is no pipeline, database, cache, or external API — every data source is
a plain Python function returning a hardcoded `pandas.DataFrame` or `dict`.

## How Data Sources Work

```
src/data/*.py  (hardcoded literals)
      │  get_*() function call
      ▼
src/app.py     (page router, calls the right get_*() for the page/role)
      │  DataFrame / dict
      ▼
src/visualizations/*.py  (create_*() builds a Plotly figure)
      │
      ▼
st.plotly_chart(...) in the Streamlit page
```

Each of the four data modules follows the same shape:

```python
# src/data/market_data.py
DATA_AS_OF = "2026-09-22"  # bump when the figures below are refreshed

def get_market_share_data(role="Executive"):
    df = pd.DataFrame({...})  # hardcoded literal
    if role == "Executive":
        return {"data": df.nlargest(3, "Market Share (%)"), "top_opportunity": "...", "key_risk": "..."}
    elif role == "Manager":
        return {"data": ..., "regional_alert": "...", "provider_comparison": {...}}
    else:  # Analyst
        return {"data": df, "raw_data_export": df.to_csv(index=False), "advanced_insights": "..."}
```

The four data modules and what they cover:

| Module | Covers |
|---|---|
| `src/data/market_data.py` | Cloud provider market share, growth trends, regional metrics, key headline metrics |
| `src/data/compliance_data.py` | Compliance requirement matrix, security certifications/audit dates, data residency |
| `src/data/performance_data.py` | Latency/uptime/IOPS (randomized via `numpy` on each call), SLAs, cost analysis, TCO calculator |
| `src/data/ai_model_data.py` | Frontier AI model family comparison (capability tier, context window, pricing) |

Some values (e.g. `market_data.get_growth_trends_data()`,
`performance_data.get_performance_metrics()`) are generated with
`numpy.random` for illustrative variance and are **not deterministic** —
they change on every page reload. Everything else is a fixed literal that
only changes when someone edits the source file.

## Data Freshness

Each data module declares a `DATA_AS_OF = "YYYY-MM-DD"` constant. Pages
render it via `src.utils.helpers.data_as_of_caption()` so staleness is
visible in the UI rather than silently baked into chart titles. **When you
refresh any figures in a data module, update its `DATA_AS_OF` constant in the
same change.**

## Adding a New Data Source

1. Add a `get_*()` function to the relevant `src/data/*.py` module (or a new
   module, following `ai_model_data.py` as the template) that returns
   `{"data": df_or_dict, ...role-specific keys...}`.
2. Add a `create_*()` visualization function in `src/visualizations/` if the
   data needs a chart, following the existing `px`/`go` patterns
   (colorblind-safe palette via `px.colors.qualitative.Safe`, an `aria-label`
   in `meta` for accessibility).
3. Wire it into a `display_*()` function in `src/components/` (or an existing
   page in `src/app.py`).
4. Add a shape/schema test in `tests/` (see `tests/test_ai_model_data.py` for
   the pattern) — assert the DataFrame is non-empty and has the expected
   columns; there's no requirement to assert exact values since several
   sources are intentionally randomized.

## Testing

Tests are schema/shape assertions only (`tests/test_*.py`), run via
`pytest tests/` and wired into `.github/workflows/ci.yml`. There is no
data-quality, freshness, or value-range validation today — reviewers should
sanity-check new figures by eye against public sources when a data module is
updated.

## Out of Scope

This codebase does not do real-time data collection, schema validation
(pydantic or otherwise), database persistence, caching, retry/backoff logic,
or structured logging — none of that infrastructure exists in `src/`. If a
future change adds live data (e.g. real cloud pricing via a provider API),
document the new flow here rather than assuming this pipeline description
still applies.

## Additional Resources

- [Architecture Overview](architecture.md)
- [Component Guide](components.md)
- [Developer Roadmap](DEVELOPER_ROADMAP_2026.md)
