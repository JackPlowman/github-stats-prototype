mod analyser 'analyser/analyser.just'

# ------------------------------------------------------------------------------
# Prettier
# ------------------------------------------------------------------------------

prettier-check:
    prettier . --check

prettier-format:
    prettier . --check --write

# ------------------------------------------------------------------------------
# Justfile
# ------------------------------------------------------------------------------

format:
    just --fmt --unstable

format-check:
    just --fmt --check --unstable
