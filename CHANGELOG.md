# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
- Initial changelog setup.
- Updated `README.md` with new information or corrections.
- Enhanced `src/app.py` for improved dashboard orchestration or bug fixes.
- Refactored and updated `src/components/metrics.py` for metrics display logic.
- Improved or fixed visualizations in `src/visualizations/plots.py`.
- Added or updated documentation: `docs/security_quickstart.md`, `docs/user_guide.md`.
- Added new tests in `tests/` directory.
- Added `.github/`, `CODE_OF_CONDUCT.md` for project governance and contribution guidelines.
- Updated `Global_Cloud_AI_Strategy_2025.md` (since renamed to `Global_Cloud_AI_Strategy_2026.md`) with new strategic insights and recommendations.
- Enhanced `src/components/decision_helper.py` and `src/components/future_trends.py` for better decision support and future trend analysis.
- Improved data ingestion and compliance logic in `src/data/compliance_data.py` and `src/data/market_data.py`.
- Refined compliance and performance visualizations in `src/visualizations/compliance_plots.py`, `src/visualizations/performance_plots.py`, and `src/visualizations/plots.py`.
- Refreshed market, compliance, and cost data to 2026 figures; added `DATA_AS_OF` freshness markers throughout the UI.
- Added a new AI Model Comparison page (`src/data/ai_model_data.py`, `src/visualizations/ai_model_plots.py`, `src/components/ai_model_comparison.py`) covering current frontier model families.
- Rewrote `docs/PROJECT_DEPENDENCIES.md`, `docs/architecture.md`, `docs/components.md`, and `docs/data-processing.md` to describe the actual Streamlit/pandas stack instead of a fictional one; renamed `DEVELOPER_ROADMAP_2025.md` to `DEVELOPER_ROADMAP_2026.md` and rewrote `TASK_TRACKING.md`.
- Renamed and refreshed `Global_Cloud_AI_Strategy_2025.md` to `Global_Cloud_AI_Strategy_2026.md`.
- Bumped `requirements.txt` floors, added `requirements-dev.txt`, and wired `pytest` into CI.
