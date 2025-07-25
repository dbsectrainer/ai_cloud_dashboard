# Copilot Instructions for AI Coding Agents

## Project Overview
- **Purpose:** Real-time analytics dashboard for global AI & cloud computing strategy, targeting enterprise decision-makers.
- **Architecture:** Modular, component-based Python app (Streamlit frontend, Pandas/NumPy for data, Plotly for visualization).
- **Key Directories:**
  - `src/app.py`: Main entry point (Streamlit app)
  - `src/components/`: UI and logic modules (e.g., `metrics.py`, `decision_helper.py`)
  - `src/data/`: Data ingestion and processing (e.g., `market_data.py`)
  - `src/visualizations/`: Plotly-based charting modules
  - `src/utils/`: Shared helpers
  - `scripts/`: Utility scripts (e.g., diagram generation)
  - `docs/`: Architecture, API, and developer docs

## Essential Workflows
- **Run Locally:**
  ```bash
  streamlit run src/app.py
  ```
- **Install Dependencies:**
  ```bash
  pip install -r requirements.txt
  ```
- **Generate Diagrams:**
  ```bash
  ./scripts/generate_diagrams.sh
  ```
  (Requires Graphviz)

## Patterns & Conventions
- **Component Structure:**
  - Each `src/components/*.py` file encapsulates a dashboard feature (metrics, comparisons, etc.)
  - Data modules in `src/data/` are decoupled from UI logic
  - Visualizations are isolated in `src/visualizations/` and use Plotly
- **No hardcoded data in UI/components;** always source from `src/data/` or external APIs
- **All user-facing logic flows through `app.py`** (acts as orchestrator)
- **Docs:**
  - Architecture and workflow diagrams in `docs/diagrams/`
  - Developer onboarding: `docs/DEVELOPER_ROADMAP_2025.md`

## Integration & Extensibility
- **Add new dashboard features:**
  - Create a new module in `src/components/`
  - Register it in `app.py` for Streamlit routing
- **Add new data sources:**
  - Implement in `src/data/`, expose clean API to components
- **Update visualizations:**
  - Extend or modify `src/visualizations/` modules

## Project-Specific Notes
- **Security & Compliance:**
  - See `src/data/compliance_data.py` and `docs/security.md`
- **Performance:**
  - Data processing is optimized for real-time updates; avoid blocking UI
- **Testing:**
  - No explicit test suite found; follow modularity and separation of concerns for maintainability

## Examples
- To add a new performance metric: implement in `src/data/performance_data.py`, visualize in `src/visualizations/performance_plots.py`, and surface in `src/components/metrics.py`.

---
For more, see `README.md`, `docs/`, and code comments. When in doubt, follow the structure of existing modules.
