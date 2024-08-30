# ------------------------------------------------------------------------------
# Astro
# ------------------------------------------------------------------------------

astro-dev:
		npm run dev

astro-start:
		npm run start

astro-build:
		npm run build

astro-preview:
		npm run preview

# ------------------------------------------------------------------------------
# Justfile
# ------------------------------------------------------------------------------

format:
		just --fmt --unstable

format-check:
		just --fmt --check --unstable

