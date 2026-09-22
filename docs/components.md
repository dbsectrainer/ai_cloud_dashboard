# Component Guide

This guide provides detailed information about each component in the AI Cloud
Dashboard. All components are plain functions — there are no classes, no
processors, and no event system; `src/app.py` calls a `get_*` data function
and passes the result to a `display_*`/`create_*` function per page.

## Market Intelligence

### Overview
The Market Intelligence page shows cloud market share, growth trends, and
regional market data — all hardcoded in `src/data/market_data.py` and
refreshed manually (see the module's `DATA_AS_OF` constant).

### Implementation
```python
from src.data.market_data import (
    get_market_share_data,
    get_growth_trends_data,
    get_regional_metrics,
    get_key_metrics,
)
from src.visualizations.plots import (
    create_market_share_treemap,
    create_growth_trends_line,
    create_provider_comparison_radar,
)

market = get_market_share_data(role="Analyst")
fig = create_market_share_treemap(market["data"])
```

## Security & Compliance

### Overview
Tracks compliance requirement coverage, security certifications, and data
residency — hardcoded in `src/data/compliance_data.py`.

### Implementation
```python
from src.data.compliance_data import (
    get_compliance_matrix,
    get_security_certifications,
    get_data_residency_map,
)
from src.visualizations.compliance_plots import (
    create_compliance_heatmap,
    create_security_score_gauge,
    create_certification_timeline,
)

certs = get_security_certifications()
fig = create_certification_timeline(certs)
```

## Cost Analysis

### Overview
TCO calculator and provider cost comparisons, backed by
`src/data/performance_data.py`.

### Implementation
```python
from src.data.performance_data import get_cost_analysis, calculate_tco
from src.visualizations.performance_plots import create_cost_comparison, create_tco_analysis

tco = calculate_tco({"compute": 1, "storage": 1, "network": 1, "support": 1})
fig = create_tco_analysis(tco)
```

## Performance Metrics

### Overview
Latency, uptime, IOPS, throughput, and SLA comparisons across providers, from
`src/data/performance_data.py`. Note: `get_performance_metrics()` generates
values with `numpy.random` on every call, so figures change on each page
reload — this is illustrative synthetic data, not a live feed.

### Implementation
```python
from src.data.performance_data import get_performance_metrics, get_sla_comparisons
from src.visualizations.performance_plots import create_performance_radar, create_latency_heatmap

perf = get_performance_metrics()
fig = create_performance_radar(perf)
```

## AI Model Comparison

### Overview
Compares current frontier AI model families (Claude, GPT, Gemini, Llama,
etc.) on capability tier, context window, pricing, and modality — added to
track the fast-moving model ecosystem separately from cloud-provider
comparisons.

### Implementation
```python
from src.data.ai_model_data import get_ai_model_comparison
from src.components.ai_model_comparison import display_ai_model_comparison

models = get_ai_model_comparison(role="Analyst")
display_ai_model_comparison(role="Analyst")  # renders the full page
```

## Strategic Tools

### Overview
`decision_helper.py`, `platform_comparisons.py`, `learning_resources.py`, and
`future_trends.py` render standalone pages with hardcoded comparison tables,
scoring logic, and forecast charts — each exposes a single
`display_*()` function called directly from `src/app.py`'s page router.

### Implementation
```python
from src.components.decision_helper import display_decision_helper
from src.components.platform_comparisons import display_platform_comparisons

display_platform_comparisons()  # renders the full page
```

## Component Integration

Components are wired together directly in `src/app.py`'s `main()` function
via an `if page == "...": display_...()` chain driven by the sidebar radio
selection (`src/components/metrics.py: display_sidebar_navigation()`). There
is no event bus, pub/sub system, or inter-component messaging.

### Data Flow
1. `src/app.py` reads the selected page and user role from the sidebar
2. It calls the matching `get_*` function(s) in `src/data/`
3. The result is optionally filtered (`src/utils/helpers.py`) and passed to a
   `create_*` visualization function or a `display_*` component function
4. Streamlit renders the returned chart/table/markdown

## Best Practices

### Component Development
1. Keep each page's logic in a single `display_*()` function
2. Keep data literals in `src/data/`, not inline in components, so they're
   easy to find and refresh
3. Follow the existing `{"data": df, ...role keys...}` return pattern in
   `src/data/*.py` for any new role-based data source
4. Write a schema/shape test in `tests/` for any new data function

## Additional Resources

- [Architecture Overview](architecture.md)
- [Data Processing Guide](data-processing.md)
- [Developer Roadmap](DEVELOPER_ROADMAP_2026.md)
- [Contributing Guidelines](../CONTRIBUTING.md)
