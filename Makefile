.PHONY: install dev run lint format test test-cov migrate revision security docker-build docker-run ci clean

UV ?= uv
# Prefer `uv run` when uv is on PATH; otherwise `python3 -m` (venv or pip install -e ".[dev]").
PYRUN := $(shell command -v $(UV) >/dev/null 2>&1 && echo "$(UV) run" || echo "python3 -m")

install:
	@if command -v $(UV) >/dev/null 2>&1; then \
		$(UV) sync --all-extras; \
	else \
		python3 -m pip install -U pip setuptools wheel && \
		python3 -m pip install -e ".[dev]"; \
	fi

dev: install
	$(PYRUN) uvicorn siteops_platform.main:app --reload --host 0.0.0.0 --port 8000

run:
	$(PYRUN) uvicorn siteops_platform.main:app --host 0.0.0.0 --port 8000

lint:
	$(PYRUN) ruff check src tests
	$(PYRUN) ruff format --check src tests

format:
	$(PYRUN) ruff format src tests
	$(PYRUN) ruff check --fix src tests

test:
	$(PYRUN) pytest tests/unit tests/api -m "not integration"

test-cov:
	$(PYRUN) pytest tests --cov=siteops_platform --cov-branch --cov-report=term-missing

test-integration:
	$(PYRUN) pytest tests/integration -m integration

migrate:
	$(PYRUN) alembic upgrade head

revision:
	$(PYRUN) alembic revision --autogenerate -m "$(m)"

security:
	$(PYRUN) bandit -r src
	$(PYRUN) pip-audit
	$(PYRUN) vulture src --min-confidence 80

docker-build:
	docker build -t siteops_platform:local .

docker-run:
	docker compose up --build

ci: lint security test-cov

clean:
	rm -rf .pytest_cache .ruff_cache htmlcov .coverage dist build *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true