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
  poetry run python main.py

unit-test:
    poetry run pytest --cov=. --cov-report=xml

# ----------------------------------g--------------------------------------------
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
