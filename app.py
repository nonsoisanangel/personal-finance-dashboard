import os
import sqlite3
from datetime import date
from pathlib import Path

from flask import Flask, flash, redirect, render_template, request, url_for


BASE_DIR = Path(__file__).resolve().parent

app = Flask(__name__)
app.config.update(
    SECRET_KEY=os.environ.get("SECRET_KEY", "dev-secret-change-before-deployment"),
    DATABASE=os.environ.get("DATABASE_PATH", str(BASE_DIR / "finance.db")),
)

CATEGORIES = [
    "Salary",
    "Freelance",
    "Housing",
    "Food",
    "Transportation",
    "Utilities",
    "Entertainment",
    "Shopping",
    "Healthcare",
    "Education",
    "Other",
]


def get_db_connection():
    connection = sqlite3.connect(app.config["DATABASE"])
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    connection = get_db_connection()
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            amount REAL NOT NULL CHECK (amount > 0),
            type TEXT NOT NULL CHECK (type IN ('Income', 'Expense')),
            category TEXT NOT NULL,
            transaction_date TEXT NOT NULL
        )
        """
    )
    connection.commit()
    connection.close()


def validate_transaction(form):
    description = form.get("description", "").strip()
    transaction_type = form.get("type", "")
    category = form.get("category", "")
    transaction_date = form.get("transaction_date", "")

    try:
        amount = float(form.get("amount", ""))
    except ValueError:
        amount = 0

    errors = []
    if not description:
        errors.append("Description is required.")
    if amount <= 0:
        errors.append("Amount must be greater than zero.")
    if transaction_type not in {"Income", "Expense"}:
        errors.append("Choose a valid transaction type.")
    if category not in CATEGORIES:
        errors.append("Choose a valid category.")
    try:
        date.fromisoformat(transaction_date)
    except ValueError:
        errors.append("Choose a valid date.")

    return errors, description, amount, transaction_type, category, transaction_date


@app.route("/")
def home():
    search = request.args.get("search", "").strip()
    selected_type = request.args.get("type", "All")
    selected_category = request.args.get("category", "All")

    conditions = []
    parameters = []

    if search:
        conditions.append("description LIKE ?")
        parameters.append(f"%{search}%")
    if selected_type in {"Income", "Expense"}:
        conditions.append("type = ?")
        parameters.append(selected_type)
    if selected_category in CATEGORIES:
        conditions.append("category = ?")
        parameters.append(selected_category)

    where_clause = " WHERE " + " AND ".join(conditions) if conditions else ""

    connection = get_db_connection()
    transactions = connection.execute(
        f"SELECT * FROM transactions{where_clause} "
        "ORDER BY transaction_date DESC, id DESC",
        parameters,
    ).fetchall()

    totals = connection.execute(
        """
        SELECT
            COALESCE(SUM(CASE WHEN type = 'Income' THEN amount END), 0) AS income,
            COALESCE(SUM(CASE WHEN type = 'Expense' THEN amount END), 0) AS expenses
        FROM transactions
        """
    ).fetchone()

    expense_rows = connection.execute(
        """
        SELECT category, ROUND(SUM(amount), 2) AS total
        FROM transactions
        WHERE type = 'Expense'
        GROUP BY category
        ORDER BY total DESC
        """
    ).fetchall()
    connection.close()

    total_income = float(totals["income"])
    total_expenses = float(totals["expenses"])
    balance = total_income - total_expenses

    chart_labels = [row["category"] for row in expense_rows]
    chart_values = [row["total"] for row in expense_rows]

    return render_template(
        "index.html",
        transactions=transactions,
        total_income=total_income,
        total_expenses=total_expenses,
        balance=balance,
        categories=CATEGORIES,
        today=date.today().isoformat(),
        search=search,
        selected_type=selected_type,
        selected_category=selected_category,
        chart_labels=chart_labels,
        chart_values=chart_values,
    )


@app.route("/add", methods=["POST"])
def add_transaction():
    values = validate_transaction(request.form)
    errors, description, amount, transaction_type, category, transaction_date = values

    if errors:
        for error in errors:
            flash(error, "error")
        return redirect(url_for("home"))

    connection = get_db_connection()
    connection.execute(
        """
        INSERT INTO transactions
            (description, amount, type, category, transaction_date)
        VALUES (?, ?, ?, ?, ?)
        """,
        (description, amount, transaction_type, category, transaction_date),
    )
    connection.commit()
    connection.close()

    flash("Transaction added successfully.", "success")
    return redirect(url_for("home"))


@app.route("/edit/<int:transaction_id>", methods=["GET", "POST"])
def edit_transaction(transaction_id):
    connection = get_db_connection()
    transaction = connection.execute(
        "SELECT * FROM transactions WHERE id = ?", (transaction_id,)
    ).fetchone()

    if transaction is None:
        connection.close()
        flash("Transaction not found.", "error")
        return redirect(url_for("home"))

    if request.method == "POST":
        values = validate_transaction(request.form)
        errors, description, amount, transaction_type, category, transaction_date = values

        if errors:
            connection.close()
            for error in errors:
                flash(error, "error")
            return redirect(url_for("edit_transaction", transaction_id=transaction_id))

        connection.execute(
            """
            UPDATE transactions
            SET description = ?, amount = ?, type = ?, category = ?, transaction_date = ?
            WHERE id = ?
            """,
            (description, amount, transaction_type, category, transaction_date, transaction_id),
        )
        connection.commit()
        connection.close()
        flash("Transaction updated successfully.", "success")
        return redirect(url_for("home"))

    connection.close()
    return render_template(
        "edit.html", transaction=transaction, categories=CATEGORIES
    )


@app.route("/delete/<int:transaction_id>", methods=["POST"])
def delete_transaction(transaction_id):
    connection = get_db_connection()
    connection.execute("DELETE FROM transactions WHERE id = ?", (transaction_id,))
    connection.commit()
    connection.close()
    flash("Transaction deleted.", "success")
    return redirect(url_for("home"))


@app.template_filter("money")
def money(value):
    return f"${float(value):,.2f}"


with app.app_context():
    init_db()


if __name__ == "__main__":
    app.run(debug=True, port=5050)
