# Trackr — Budget Tracker

A personal finance web app to track income and expenses, visualize spending trends, and connect bank accounts. Built with vanilla HTML/CSS/JS the frontend and Python on the backend.

---

## Features

- **Transaction Management** — Add income and expense entries with date, description, category, and amount
- **Financial Summary** — Live totals for balance, income, and expense for the current month
- **Spending Categories** — Organize transactions by Food, Transport, Housing, Shopping, or Other
- **Bank Connection UI** — Connect Chase, Bank of America, or Wells Fargo accounts
- **Financial Analysis** (Python backend) — Auto-generates:
  - Pie chart: expense breakdown by category
  - Line chart: 12-month balance trend
  - Bar chart: monthly income vs. expense side-by-side
- **User Authentication** — Sign-in page (in progress)

---

## Project Structure

```
budget.tracker/
├── index.html              # Main dashboard (transaction form + table)
├── home.html               # Home page (bank connect + transaction form)
├── sign_in.html            # Login page (in progress)
├── asset/
│   ├── home.css            # Styles for home.html
│   └── sign_in.css         # Styles for sign-in page
├── template/
│   └── index.html          # UI template / design reference
└── src/
    └── budget_tracker_account.py   # Python backend — account model + chart generation
```

## Getting Started

### Frontend


```bash
open home.html
```

### Python Backend

Install dependencies:

```bash
pip install numpy matplotlib

pip install numpy 
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

### Transaction Categories

`Food` · `Transport` · `Housing` · `Shopping` · `Other`

---

## Team

Built as a mini-project for UCLA — team of 3.

---

## Roadmap

- [ ] JavaScript logic connecting frontend form to Python backend via API
- [ ] User authentication (sign-in flow)
- [ ] Plaid API integration for real bank connections
- [ ] Persistent storage (database)
- [ ] Dashboard, Transaction, Budget, and Report pages (nav stubs visible in template)
- [ ] Spending charts rendered in-browser
