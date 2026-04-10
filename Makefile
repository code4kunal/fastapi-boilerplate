.PHONY: install dev run lint format test test-cov migrate revision security docker-build docker-run ci clean

UV ?= uv

install:
	$(UV) sync --all-extras

dev: install
	$(UV) run uvicorn siteops_platform.main:app --reload --host 0.0.0.0 --port 8000

run:
	$(UV) run uvicorn siteops_platform.main:app --host 0.0.0.0 --port 8000

lint:
	$(UV) run ruff check src tests
	$(UV) run ruff format --check src tests

format:
	$(UV) run ruff format src tests
	$(UV) run ruff check --fix src tests

test:
	$(UV) run pytest tests/unit tests/api -m "not integration"

test-cov:
	$(UV) run pytest tests --cov=siteops_platform --cov-branch --cov-report=term-missing

test-integration:
	$(UV) run pytest tests/integration -m integration

migrate:
	$(UV) run alembic upgrade head

revision:
	$(UV) run alembic revision --autogenerate -m "$(m)"

security:
	$(UV) run bandit -r src
	$(UV) run pip-audit
	$(UV) run vulture src --min-confidence 80

docker-build:
	docker build -t siteops_platform:local .

docker-run:
	docker compose up --build

ci: lint security test-cov

clean:
	rm -rf .pytest_cache .ruff_cache htmlcov .coverage dist build *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true