import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt 
import os 

class BudgetTrackerAccount: 
    def __init__(self, name : str, balance: list, income: list, expense: list):
        """
            balance, income, expense: list contains the past 12-month report 
            transaction: list(dict)
        """
        self.owner_name = name
        self.balance = balance
        self.income = income 
        self.expense = expense 
        self.transactions = []
    
    def get_dashboard_info(self): 
        balance = self.balance[-1]
        income = self.income[-1]
        expense = self.expense[-1]

        return {
            "balance": balance, 
            "income": income, 
            "expense": expense
        }
    
    def add_transaction(self, date, description, amount, type, category): 
        amount = abs(amount)
        if type == "income": 
            self.balance[-1] += amount
            self.income[-1] += amount 
        elif type == "expense": 
            self.balance[-1] -= amount 
            self.expense[-1] += amount 


        if isinstance(date, datetime):
            date_time = date
        else:
            for fmt in ("%Y-%m-%d", "%m/%d/%Y"):
                try:
                    date_time = datetime.strptime(date, fmt)
                    break
                except ValueError:
                    continue
            else:
                raise ValueError(f"Unrecognized date format: {date}")

        transaction = {
            "date": date_time, 
            "description": description, 
            "category": category, 
            "type": type, 
            "amount": amount
        }
        self.transactions.append(transaction)

    def categorize_expenses(self):
        """
            Sort out the expenses spent on each category
            itemized category_amount: list[tuple(str, int)]
                There are 5 categories: Food, Transport, Housing, Shopping, and Other
            Return: 
                category_expenses: list() size of 5 
                    using map_idx_category Food: idx 0, Transport: 1, Housing: 2, Shopping: 3, Other: 4
            
        """
        itemized_category_amounts = [(transaction['category'], transaction['amount']) for transaction in self.transactions if transaction['type'] == 'expense']
        category_expenses = [0 for _ in range(5)]
        map_idx_category = {
            "food": 0, 
            "transport": 1, 
            "housing": 2, 
            "shopping": 3, 
            "other": 4 
        }

        for category, amount in itemized_category_amounts: 
            if category in map_idx_category:
                category_expenses[map_idx_category[category]] += amount 
        
        return category_expenses

    def __get_chart_path(self, filename):
        base = os.path.dirname(os.path.abspath(__file__))
        folder_path = os.path.join(base, "..", "financial_analysis", self.owner_name)
        os.makedirs(folder_path, exist_ok=True)
        return os.path.join(folder_path, filename)
    
    def __creating_pie_chart(self): 
        """
            Creating pie chart to breakdown total expenses spent on each category
        """
        category_names = ["Food", "Transport", "Housing", "Shopping", "Other"]
        category_expenses = self.categorize_expenses() 

        plt.figure(figsize=(10, 10))
        plt.title(f"Expense Breakdown by Category - Account {self.owner_name}")
        if sum(category_expenses) > 0:
            plt.pie(category_expenses, labels=category_names)
        else:
            plt.text(0.5, 0.5, "The expense can't be categorized", ha="center", va="center", fontsize=20)
            plt.axis("off")
        plt.savefig(self.__get_chart_path(f"pie_chart_{self.owner_name}.png"))
        plt.close()

    def __creating_line_chart(self): 
        """
            Creating line chart to show whether balance is increasing or decreasing over time
        """
        months = ["Jan", "Feb", "Mar", "April", "May", "June", "July", "Aug", "Sep", "Oct", "Nov", "Dec"]
        plt.figure(figsize=(10, 10))
        plt.title(f"12-Month Balance Trend - Account {self.owner_name}")
        plt.xlabel("Month")
        plt.ylabel("Total Balance")
        plt.plot(months, self.balance)
        plt.savefig(self.__get_chart_path(f"line_chart_{self.owner_name}.png"))
        plt.close() 
    
    def __creating_bar_chart(self): 
        """
            Creating bar chart to show the income and expense side by side 
        """
        months = ["Jan", "Feb", "Mar", "April", "May", "June", "July", "Aug", "Sep", "Oct", "Nov", "Dec"]
        x = np.arange(len(months))
        height = 0.35
        
        plt.figure(figsize=(12, 12))
        plt.title(f"Monthly Income vs Expense - Account {self.owner_name}")
        plt.xlabel("Month")
        plt.ylabel("$")
        plt.barh(x + height/2, self.income, height, color="blue", label="Income")
        plt.barh(x - height/2, self.expense, height, color="red", label="Expense")
        plt.yticks(x, months)
        plt.legend() 
        plt.savefig(self.__get_chart_path(f"bar_chart_{self.owner_name}.png"))
        plt.close() 

    def financial_analysis(self): 
        filenames = [
            f"pie_chart_{self.owner_name}.png",
            f"line_chart_{self.owner_name}.png",
            f"bar_chart_{self.owner_name}.png",
        ]

        for filename in filenames:
            disk_path = self.__get_chart_path(filename)
            if os.path.exists(disk_path):
                os.remove(disk_path)

        self.__creating_bar_chart() 
        self.__creating_line_chart() 
        self.__creating_pie_chart()

        return [
            f"/financial_analysis/{self.owner_name}/{filename}"
            for filename in filenames
        ], ["pie_chart", "line_chart", "bar_chart"]
    
# if __name__ == "__main__": 
#     account = BudgetTrackerAccount("Henry", 
#         balance=[3000, 3200, 3500, 3800, 4000, 4200, 4500, 4800, 5000, 5200, 5500, 5800],
#         income=[2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000],
#         expense=[800, 850, 900, 750, 800, 820, 780, 810, 790, 830, 860, 870]
#     )

#     account.add_transaction("06/01/2025", "Grocery Store", 120, "expense", "food")
#     # account.add_transaction("06/10/25", "Rent", "Housing", "Expense", 900)
#     # account.add_transaction("06/12/25", "Amazon", "Shopping", "Expense", 75)
#     # account.add_transaction("06/15/25", "Restaurant", "Food", "Expense", 45)
#     # account.add_transaction("06/18/25", "Uber", "Transport", "Expense", 30)
#     # account.add_transaction("06/20/25", "Netflix", "Other", "Expense", 15)
#     # account.add_transaction("06/22/25", "Freelance", "Other", "Income", 500)
#     # account.add_transaction("06/25/25", "Zara", "Shopping", "Expense", 200)

#     account.financial_analysis() 