# SauceDemo UI Automation

Playwright + pytest automation for [saucedemo.com](https://www.saucedemo.com) built with the Page Object Model.

## What This Repo Covers

- Login flows
- Inventory interactions
- Cart behavior
- Checkout flow

## Framework Choice

This project uses:

- `Playwright` for browser automation
- `pytest` for test structure and execution
- Page Object Model for maintainability

### Why This Stack

- `Playwright` is stable for modern web UI testing and provides reliable browser automation with good auto-waiting behavior.
- `pytest` keeps the suite simple to read, easy to extend, and flexible for fixtures, markers, and reporting.
- Page Objects reduce duplication and make selectors and flows easier to update when the UI changes.

## Project Layout

```text
.
├── pages/                  # Page Object classes
├── tests/                  # Test cases
├── data/                   # Shared constants and user data
├── utils/                  # Small helper functions
├── conftest.py             # Pytest / Playwright fixtures
├── pytest.ini              # Pytest configuration
└── .github/workflows/      # CI workflow
```

## Setup

```bash
pip install -r requirements.txt
playwright install chromium
```

## Run Tests

```bash
pytest
pytest tests/test_login.py
pytest -k "test_p_"
pytest -k "test_n_"
```

`pytest.ini` sets the base URL to `https://www.saucedemo.com` and configures HTML reporting.

## Reporting

The suite generates an HTML report at `reports/report.html` when tests run locally or in CI.

## CI

GitHub Actions runs the suite on push and pull request events using `.github/workflows/test.yml`.

## Extension Plan

### Parallelisation

- Add `pytest-xdist` to split tests across workers.
- Group tests by area so login, inventory, and checkout can run independently.
- Keep fixtures session-scoped where possible to avoid unnecessary browser startup cost.

### Reporting

- Keep the current HTML report for quick local inspection.
- Add richer reporting later with Allure or a CI artifact upload step.
- Preserve failure screenshots and traces for easier debugging when the suite grows.

## Notes

- Test data lives in `data/test_data.py` and `data/users.json`.
- Generated artifacts such as `reports/` are ignored by git.
