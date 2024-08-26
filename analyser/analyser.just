# ------------------------------------------------------------------------------
# Python
# ------------------------------------------------------------------------------

clean:
  find . \( \
    -name '__pycache__' -o \
    -name '.coverage' -o \
    -name '.mypy_cache' -o \
    -name '.pytest_cache' -o \
    -name '.ruff_cache' -o \
    -name '*.pyc' -o \
    -name '*.pyd' -o \
    -name '*.pyo' -o \
    -name 'coverage.xml' -o \
    -name 'db.sqlite3' \
  \) -print | xargs rm -rfv


install:
  poetry install

run:
  poetry run python -m application

unit-test:
  poetry run pytest application --cov=application --cov-report=xml

# ------------------------------------------------------------------------------
# Ruff
# ------------------------------------------------------------------------------

ruff-lint:
  poetry run ruff check application

ruff-lint-fix:
  poetry run ruff check application --fix

ruff-format:
  poetry run ruff format --check application

ruff-format-fix:
  poetry run ruff format application

# ------------------------------------------------------------------------------
# Other Python Tools
# ------------------------------------------------------------------------------

bandit:
  poetry run bandit -r application -c pyproject.toml

vulture:
  poetry run vulture application
