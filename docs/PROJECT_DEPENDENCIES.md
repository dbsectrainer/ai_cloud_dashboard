# AI Cloud Dashboard Project Dependencies

This app uses hardcoded/synthetic data only — no databases, external APIs, or
ML frameworks are present in `src/`. The list below reflects what the codebase
actually imports and what CI actually runs, not an aspirational stack.

## Core Technologies

### Python Environment
- Python 3.12 (see `.github/workflows/ci.yml`)
- pip

### Application
- Streamlit 1.51+ (UI framework and dev server; see `requirements.txt`)
- pandas 2.3+ (all "data sources" are hardcoded DataFrames built in `src/data/`)
- Plotly 6.3+ (all charts in `src/visualizations/`)
- numpy 2.3+ (used for a handful of illustrative synthetic/random values)

## Development Tools

### Version Control
- Git
- GitHub

### CI/CD
- GitHub Actions (`.github/workflows/ci.yml`): lint (flake8), format check (black), test (pytest)

### Code Quality
- flake8
- Black (Python formatter)

### Testing
- pytest (see `requirements-dev.txt` and `tests/`)

## System Requirements

Runs comfortably on any machine capable of running a local Streamlit dev
server: no GPU, no database, no message queue, and no external network access
are required. A standard laptop (4GB+ RAM) is sufficient for local
development.

## Version Management

- Dependency floors are declared with `>=` in `requirements.txt` (application)
  and `requirements-dev.txt` (test/lint tooling); there is no lockfile.
- Bump floors when a refresh (like this one) reviews current data and content.

## Out of Scope / Not Present in This Codebase

The dashboard does **not** use, and has no plans to use unless a future
change explicitly adds it: React/React Native/Three.js/D3.js, FastAPI/GraphQL,
any database (PostgreSQL/MongoDB/Redis/Neo4j/Elasticsearch/TimescaleDB),
Kafka or other message queues, ML/AI frameworks (TensorFlow, PyTorch, Hugging
Face Transformers, scikit-learn, MLflow, Airflow) or any external LLM API
(including OpenAI's), observability stacks (Prometheus/Grafana/Jaeger),
container/infra tooling (Kubernetes/Docker/Terraform/Helm), mobile SDKs, or
cloud provider SDKs. If a future contribution adds any of these, update this
document alongside it.
