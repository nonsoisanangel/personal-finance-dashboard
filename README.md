# FinanceFlow - Personal Finance Dashboard

A responsive full-stack personal finance application built with Flask, SQLite, HTML, CSS, and JavaScript. It tracks income and expenses, calculates financial totals, filters transactions, and visualizes spending by category.

## Features

- Add income and expense transactions
- Edit and delete existing transactions
- Automatic income, expense, and balance totals
- Transaction dates and spending categories
- Search and filter transaction history
- Expense breakdown doughnut chart
- Form validation and success/error messages
- Responsive layout for desktop and mobile
- SQLite database created automatically
- Automated tests for the main CRUD workflow

## Technology

- Python 3
- Flask
- SQLite
- Jinja templates
- HTML5 and CSS3
- JavaScript
- Chart.js

## Run locally

1. Open the project folder in VS Code.
2. Open the VS Code terminal.
3. Create a virtual environment:

   ```bash
   python3 -m venv .venv
   ```

4. Activate it on macOS or Linux:

   ```bash
   source .venv/bin/activate
   ```

5. Install the dependency:

   ```bash
   pip install -r requirements.txt
   ```

6. Start the application:

   ```bash
   python3 app.py
   ```

7. Open <http://127.0.0.1:5050> in a browser.

The `finance.db` database file is created automatically the first time the application starts.

## Run tests

```bash
python3 -m unittest discover -s tests
```

## GitHub setup

Create an empty GitHub repository named `personal-finance-dashboard`, then run these commands inside this project folder:

```bash
git init
git add .
git commit -m "Build personal finance dashboard"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/personal-finance-dashboard.git
git push -u origin main
```

Replace `YOUR-USERNAME` with your GitHub username.

## Resume description

**Personal Finance Dashboard | Python, Flask, SQLite, HTML, CSS, JavaScript**

- Developed a full-stack finance application with Flask and SQLite to manage categorized income and expense transactions.
- Implemented CRUD operations, automatic financial summaries, search and filtering, and a dynamic expense visualization.
- Designed a responsive interface with validation and automated workflow tests.
