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
