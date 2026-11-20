# PolicyNest Frontend

Built with Vue 3.5, Vuetify 4.3, Vue Router 5, and Vite 8.

## Requirements

- Node.js `^20.19.0 || ^22.13.0 || >=24`

## Scripts

```sh
npm install                  # Install dependencies
npm run dev                  # Start Vite dev server
npm run build                # Build production bundle into dist/
npm run preview              # Preview production bundle
npm run lint                 # Lint and auto-fix with ESLint
npx eslint . --max-warnings 0 # Verify zero ESLint errors/warnings
npm run format               # Format src/ with Prettier
```

API requests use the relative `/api` base path (`src/services/api.js`) and are served alongside the built `dist/` bundle by the FastAPI backend on port `8000` (see the root [README](../README.md) for full-stack startup instructions).
