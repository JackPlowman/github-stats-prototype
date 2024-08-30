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
# TypeScript
# ------------------------------------------------------------------------------

install:
    npm install

eslint-check:
    npx eslint .

prettier-check:
    prettier . --check
