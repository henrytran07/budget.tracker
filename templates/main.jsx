import React from "react";
import ReactDOM from "react-dom/client";
import colorCard from "./color_changing";
import "../asset/main.css";

function App() {
    const root = document.getElementById("root");

    const balance = Number(root.dataset.balance);
    const income = Number(root.dataset.income);
    const expense = Number(root.dataset.expense);

    const colors = colorCard(expense, income, balance);

    return (
        <section className="summary">
            <h2 className="summary-title">Summary</h2>

            <div className="summary-card">
                <div className="balance">
                    <p className="label">Total Balance</p>
                    <h2 className={colors.balanceCard}>${balance}</h2>
                </div>

            <div className="income">
                <p className="label">Total Income</p>
                <h2 className={colors.incomeCard}>${income}</h2>
            </div>

                <div className="expense">
                    <p className="label">Total Expense</p>
                    <h2 className={colors.expenseCard}>${expense}</h2>
                </div>
            </div>
        </section>
    );
}

ReactDOM.createRoot(document.getElementById("root")).render(
    <React.StrictMode>
        <App />
    </React.StrictMode>
);