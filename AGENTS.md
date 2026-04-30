# AGENTS.md

## Cursor Cloud specific instructions

### Overview

This is a single-process Python/Streamlit web app — a **Marketplace Personalization & Ad Targeting Simulator**. There are no external services, databases, or caches; all data is generated in-memory at runtime.

### Running the app

```
streamlit run streamlit_app.py --server.enableCORS false --server.enableXsrfProtection false --server.headless true
```

The app serves on port **8501**. See `README.md` for the canonical setup steps.

### Known issues

- The auction module (`auction.py`) has a `KeyError: 'seller_id'` bug when merging DataFrames in `run_auction()`. This causes Tabs 3 (Ads & Auction) and 4 (Metrics Dashboard) to fail at runtime. Tabs 1 (Simulation Config) and 2 (Personalized Results) work correctly.

### Lint / Test / Build

- **No automated test suite or linter configuration exists in this repo.** There are no `pytest`, `flake8`, `mypy`, or similar configs.
- To verify modules load correctly: `python3 -c "import streamlit_app"`
- The app has no build step — run it directly with `streamlit run`.
