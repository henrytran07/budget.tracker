# Trackr — Budget Tracker

A personal finance web app to track income and expenses, visualize spending
trends, and import transactions from a connected bank. Built with a **FastAPI**
backend and **Jinja2** server-rendered templates. Most pages are vanilla
HTML/CSS; the dashboard summary cards are a **React** component bundled with
**Vite**. Charts are generated server-side with **Matplotlib**.

> UCLA mini-project · team of 3 · active development on the `api` branch

---
## Demo

![Trackr demo](video/demo.gif)
## Features

- **Sign Up / Sign In** — `BudgetTrackerManager` handles account creation,
  credential storage, and login verification. Existing users are loaded from
  `information/trkr_account.json` at startup.
- **Dashboard** — Live totals for balance, income, and expenses, plus a
  transaction history and an "add transaction" form.
- **Transaction Management** — Add income or expense entries with date,
  description, category, and amount. Balance updates automatically.
- **Spending Categories** — Food, Transport, Housing, Shopping, Other.
- **Financial Analysis** — `BudgetTrackerAccount` auto-generates three charts
  per account:
  - **Pie** — expense breakdown by category
  - **Line** — 12-month balance trend
  - **Bar** — monthly income vs. expense
- **Bank Connection (Bank of America)** — `BankingManager` verifies bank
  credentials against `information/boa.json` and imports that account's
  transactions into Trackr.
- **Summary Cards (React)** — `main.jsx` reads the balance, income, and expense
  totals from `data-*` attributes on the dashboard's `#root` element and renders
  three cards. `color_changing.jsx` colors them green, yellow, or red based on
  the expense-to-income ratio.
- **Transfer Page** — Animated bank → Trackr handoff with a dotted-arrow
  transition between the connected bank logo and the Trackr logo.

---


## Project Structure

```
budget.tracker/  (api branch)
├── main.py                          # FastAPI app: mounts static dirs, includes router
├── package.json                     # Frontend dependencies (React) + build scripts
├── vite.config.js                   # Vite build config: templates/main.jsx -> static/
├── README.md
├── src/
│   ├── budget_tracker_manager.py    # Manager + all routes: sign in/up, dashboard, bank
│   ├── budget_tracker_account.py    # Account model: transactions + chart generation
│   └── banking_manager.py           # Bank of America credential check + transaction import
├── templates/
│   ├── sign_in.html                 # Login page
│   ├── sign_up.html                 # Registration page (still working on it)
│   ├── home.html                    # Dashboard (summary, transactions, charts)
│   ├── boa.html                     # Bank of America connect page
│   ├── transfer_page.html           # Bank → Trackr transfer animation
│   ├── main.jsx                     # React entry point: dashboard summary cards
│   └── color_changing.jsx           # Card color logic from expense/income ratio
├── asset/
│   ├── sign_in.css
│   ├── main.css                     # Styles for the React summary cards
│   ├── home.css
│   ├── boa.css
│   └── transfer_page.css
├── images/                          # Logos and UI assets (Trackr, BoA, Chase, FDIC, etc.)
├── information/
│   ├── trkr_account.json            # Trackr user credentials + financial data
│   └── boa.json                     # Mock Bank of America accounts + transactions
├── static/                          # Vite build output (generated, git-ignored)
└── financial_analysis/              # Generated charts, per account (created at runtime)
```

---

## Getting Started

### 1. Install frontend dependencies

The dashboard summary cards are a React component, so they must be compiled
before the app will display them.

```bash
npm install
```

### 2. Build the frontend

```bash
npm run build
```

This bundles `templates/main.jsx` (and its CSS import) into `static/app.js` and
`static/app.css`, which `home.html` loads at runtime. While actively editing the
JSX, run `npm run dev` instead — it rebuilds automatically on save.

### 3. Install backend dependencies

```bash
pip install fastapi uvicorn jinja2 python-multipart numpy matplotlib
```

### 4. Run the app

From the project root (the folder containing `main.py`):

```bash
uvicorn main:app --reload
```

Then open <http://127.0.0.1:8000> in your browser.

> **Note:** the static mounts use relative paths, so the server must be started
> from the project root. Launching from a parent directory fails at startup.

### 5. Log in

Use one of the seed accounts in `information/trkr_account.json`, or register a
new one via the sign-up page.

---

## Routes

| Method | Path                        | Purpose                                    |
|--------|-----------------------------|--------------------------------------------|
| GET    | `/`                         | Login page                                 |
| POST   | `/`                         | Verify login, redirect to dashboard        |
| GET    | `/sign-up`                  | Registration page                          |
| POST   | `/sign-up`                  | Create account, redirect to login          |
| GET    | `/dashboard/{user_id}`      | Dashboard with summary, transactions, charts |
| POST   | `/dashboard/{user_id}`      | Add a transaction                          |
| GET    | `/choose-bank`              | Route to a bank's connect flow             |
| GET    | `/bank-of-america-login`    | Bank of America connect page               |
| POST   | `/bank-of-america-login`    | Verify bank credentials, import transactions |

Static mounts: `/static`, `/asset`, `/images`, `/financial_analysis`.

---
