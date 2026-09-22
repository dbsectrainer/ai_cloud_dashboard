# AI Cloud Dashboard Developer Roadmap 2026

## Overview
This roadmap tracks the actual state of the AI Cloud Dashboard: a Streamlit
app with hardcoded/synthetic data across 10 pages. Earlier roadmap drafts
(now retired) described a much larger enterprise platform — real database
integrations, authentication, mobile apps, ML pipelines — none of which was
ever built. This version replaces that plan with an accurate account of
what's done and a short, realistic list of what's next.

## Completed (September 2026 refresh)

- Refreshed all data modules (`src/data/market_data.py`,
  `compliance_data.py`, `performance_data.py`) to current 2026 figures, with
  a `DATA_AS_OF` constant on each so freshness is visible in the UI going
  forward instead of silently baking a year into chart titles.
- Added a new AI Model Comparison page
  (`src/data/ai_model_data.py`, `src/visualizations/ai_model_plots.py`,
  `src/components/ai_model_comparison.py`) comparing current frontier model
  families on capability tier, context window, and pricing — closing the gap
  where an "AI Cloud Dashboard" had no AI-model-specific data at all.
- Corrected `docs/PROJECT_DEPENDENCIES.md`, `docs/architecture.md`,
  `docs/components.md`, and `docs/data-processing.md`, which previously
  described a fictional stack (React, FastAPI, PostgreSQL/MongoDB/Redis,
  TensorFlow, an "OpenAI GPT-4 API" dependency) never present in `src/`.
- Wired `pytest` into CI (`.github/workflows/ci.yml`) — `tests/` had real
  content that CI was never actually running.
- Bumped `requirements.txt` floors, which hadn't moved since January 2025.

### Resolved: "AI Strategy Advisor" / GPT-4 integration
Earlier roadmap drafts and `docs/TASK_TRACKING.md` carried a recurring
"GPT-4 API integration" task for an AI Strategy Advisor chatbot. That item is
superseded by the AI Model Comparison page above — this app compares model
families as reference data, it does not call any LLM API. No chatbot/API-
calling advisor exists or is currently planned.

## Next

- Consider a lightweight data-freshness check (e.g. a test asserting
  `DATA_AS_OF` is reasonably recent) so a future refresh doesn't silently go
  stale for 20 months again.
- Expand AI Model Comparison coverage as new frontier releases ship.
- Evaluate opt-in live data for one source (e.g. cloud compute pricing) as a
  scoped follow-up — not required by this refresh, since the app's data
  approach is intentionally static/hardcoded today.
- Add CONTRIBUTING guidance for how/when to refresh data module figures.

## Out of Scope

Authentication, a database layer, real-time data pipelines, mobile apps, and
ML model training are not implemented and are not planned in the near term.
If a future initiative decides to pursue any of these, it should start a new
roadmap section rather than resurrecting the retired 2025 plan, since none of
its infrastructure assumptions (Kubernetes, Kafka, Redis, FastAPI, etc.) match
this codebase.
