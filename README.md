# Trackr — Budget Tracker

A personal finance web app to track income and expenses, visualize spending trends, and connect bank accounts. Built with vanilla HTML/CSS/JS on the frontend and Python on the backend.

---

## Features

- **Transaction Management** — Add income and expense entries with date, description, category, and amount
- **Financial Summary** — Live totals for balance, income, and expenses for the current month
- **Spending Categories** — Organize transactions by Food, Transport, Housing, Shopping, or Other
- **Bank Connection UI** — Bank of America-styled connect flow (`boa.html`)
- **Transfer Page** — Animated bank → Trackr data transfer screen with a dotted-arrow handoff between the connected bank logo and the Trackr logo
- **User Sign Up / Sign In** (Python backend) — `BudgetTrackerManager` handles account creation, credential storage, and login verification
- **Financial Analysis** (Python backend) — `BudgetTrackerAccount` auto-generates:
  - Pie chart: expense breakdown by category
  - Line chart: 12-month balance trend
  - Bar chart: monthly income vs. expense side-by-side

---

## Project Structure

```
budget.tracker/  (api branch)
├── README.md
├── home.html                       # Home page (bank connect + transaction form)
├── boa.html                        # Bank of America connect page
├── sign_in.html                    # Login page (in progress)
├── transfer.html                   # Bank → Trackr data transfer page
├── asset/
│   ├── boa.css                     # Styles for boa.html
│   ├── home.css                    # Styles for home.html
│   ├── sign_in.css                 # Styles for sign-in page
│   └── transfer_page.css           # Styles for transfer page
├── images/
│   ├── bankofamerica.webp          # Bank of America logo asset
│   └── trackr_logo.png             # Trackr app icon
└── src/
    ├── budget_tracker_account.py   # Account model — transactions + chart generation
    └── budget_tracker_manager.py   # Manager class — sign up, sign in, account storage
```

---

## Getting Started

### Frontend

```bash
open home.html
```

### Python Backend

Install dependencies:

```bash
pip install numpy matplotlib
```

Run the account model demo:

```bash
python src/budget_tracker_account.py
```

This will generate three charts under `financial_analysis/<account_id>/`:

- `pie_chart_<id>.png`
- `line_chart_<id>.png`
- `bar_chart_<id>.png`

---

## Transaction Categories

`Food` · `Transport` · `Housing` · `Shopping` · `Other`

---

## Team

Built as a mini-project for UCLA — team of 3.

---

## Roadmap

- [ ] JavaScript logic connecting frontend form to Python backend via API
- [ ] Finish sign-in flow UI (`sign_in.html`)
- [ ] Wire up `transfer.html` to real bank connection state
- [ ] Plaid API integration for real bank connections
- [ ] Persistent storage (database) — currently in-memory via `BudgetTrackerManager`
- [ ] Dashboard, Transaction, Budget, and Report pages (nav stubs visible in template)
- [ ] Spending charts rendered in-browser