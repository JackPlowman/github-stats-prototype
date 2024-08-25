# ------------------------------------------------------------------------------
# Python
# ------------------------------------------------------------------------------

unit-test:
    poetry run pytest --cov=. --cov-report=xml

# ------------------------------------------------------------------------------
# Ruff
# ------------------------------------------------------------------------------

ruff-lint:
    poetry run ruff check .

ruff-lint-fix:
    poetry run ruff check . --fix

ruff-format:
    poetry run ruff format --check .

ruff-format-fix:
    poetry run ruff format .

# ------------------------------------------------------------------------------
# Other Python Tools
# ------------------------------------------------------------------------------

bandit:
    poetry run bandit -r .

vulture:
    poetry run vulture .
