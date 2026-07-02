# SauceDemo UI Automation

Playwright + pytest test suite for [saucedemo.com](https://www.saucedemo.com) using the Page Object Model.

## Setup

```bash
pip install -r requirements.txt
playwright install chromium
```

## Run Tests

```bash
pytest                           # all tests
pytest tests/test_login.py       # login tests only
pytest -k "test_p_"              # positive tests only
pytest -k "test_n_"              # negative tests only
```

HTML report is generated at `reports/report.html`.

## Project Structure

```
├── pages/              # Page Object classes
│   ├── login_page.py           # Login page
│   ├── inventory_page.py       # Products page
│   ├── cart_page.py            # Cart page
│   ├── checkout_page.py        # Checkout: Your Information
│   └── checkout_overview_page.py  # Checkout: Overview
├── tests/              # Test cases
│   ├── test_login.py           # 11 tests (7p, 4n)
│   ├── test_inventory.py       # 19 tests (all p)
│   └── test_checkout.py        # 16 tests (12p, 4n)
├── data/users.json     # Test user credentials
├── conftest.py         # Playwright fixtures
└── pytest.ini          # Pytest config
```

Test names use `test_p_` for positive scenarios and `test_n_` for negative scenarios.

## CI

GitHub Actions runs on every push — see `.github/workflows/test.yml`.
