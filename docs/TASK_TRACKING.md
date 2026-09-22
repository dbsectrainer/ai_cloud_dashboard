# AI Cloud Dashboard Task Tracking

The previous version of this file tracked tasks for a much larger platform
(Kubernetes, Kafka, FastAPI, mobile apps, ML pipelines, a GPT-4-powered
advisor) that was never built. This version tracks real, current tasks for
the Streamlit/pandas/plotly codebase that actually exists.

## September 2026 Refresh

- [x] Add `DATA_AS_OF` constants + UI caption helper (`src/utils/helpers.py`)
- [x] Refresh `market_data.py`, `compliance_data.py`, `performance_data.py`
      figures and dates to 2026
- [x] Add AI Model Comparison page (data, visualizations, component, nav,
      test)
- [x] Fix hardcoded "2025" strings in chart titles/aria-labels/tooltips
- [x] Rewrite `PROJECT_DEPENDENCIES.md`, `architecture.md`, `components.md`,
      `data-processing.md` to match the real stack
- [x] Retire `DEVELOPER_ROADMAP_2025.md` in favor of
      `DEVELOPER_ROADMAP_2026.md`
- [x] Refresh `Global_Cloud_AI_Strategy_2026.md` (renamed from the 2025
      whitepaper) with figures consistent with the refreshed dashboard
- [x] Bump `requirements.txt` floors; add `requirements-dev.txt`
- [x] Wire `pytest` into CI (`.github/workflows/ci.yml`)

## Next

- [ ] Add a data-freshness check (e.g. assert `DATA_AS_OF` is recent) to
      `tests/`
- [ ] Add CONTRIBUTING guidance for refreshing data module figures
- [ ] Expand AI Model Comparison coverage as new model families ship
- [ ] Evaluate opt-in live pricing data for one source, as a scoped follow-up

## Ongoing

- [ ] Keep `requirements.txt` floors current
- [ ] Re-check data figures periodically and bump `DATA_AS_OF`
- [ ] Keep docs in sync with `src/` as components are added or removed
