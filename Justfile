mod analyser 'analyser/analyser.just'
mod dashboard 'dashboard/dashboard.just'

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
    just analyser::format
    just dashboard::format

format-check:
    just --fmt --check --unstable
    just analyser::format-check
    just dashboard::format-check
