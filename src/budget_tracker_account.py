import numpy as np
# import queue
from datetime import datetime
import matplotlib.pyplot as plt 
import os 

class BudgetTrackerAccount: 
    def __init__(self, name : str):
        """
            balance, income, expense: list contains the pat 12-month report 
            transaction: list(dict)
        """
        self.owner_name = name
        self.balance = []
        self.income = []
        self.expense = []
        self.transactions = []
    
    def get_balance(self): 
        return self.balance[-1]
    
    def get_income(self): 
        return self.income[-1]
    
    def get_expense(self): 
        return self.expense[-1]
    
    def add_transaction(self, date, description, category, type, amount): 
        amount = abs(amount)
        if type == "Income": 
            self.balance[-1] += amount
            self.income[-1] += amount 
        elif type == "Expense": 
            self.balance[-1] -= amount 
            self.expense[-1] += amount 
        
        date_time = datetime.strptime(date, "%m/%d/%y")
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
        itemized_category_amounts = [(transaction['category'], transaction['amount']) for transaction in self.transactions if transaction['type'] == 'Expense']
        category_expenses = [0 for _ in range(5)]
        map_idx_category = {
            "Food": 0, 
            "Transport": 1, 
            "Housing": 2, 
            "Shopping": 3, 
            "Other": 4 
        }

        for category, amount in itemized_category_amounts: 
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

        plt.title(f"Expense Breakdown by Category - Account {self.owner_name}")
        plt.pie(category_expenses, labels=category_names)
        plt.savefig(self.__get_chart_path(f"pie_chart_{self.owner_name}.png"))
        plt.close()

    def __creating_line_chart(self): 
        """
            Creating line chart to show whether balance is increassing or decreasing over time
        """
        months = ["Jan", "Feb", "Mar", "April", "May", "June", "July", "Aug", "Sep", "Oct", "Nov", "Dec"]
        plt.figure(figsize=(10, 10))
        plt.title(f"12-Month Balance Trend - Account {self.owner_name}")
        plt.xlabel("Month")
        plt.ylabel("Total Balance")
        plt.legend()
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
        
        plt.figure(figsize=(10, 8))
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
        chart_paths = [
            self.__get_chart_path(f"pie_chart_{self.owner_name}.png"),
            self.__get_chart_path(f"line_chart_{self.owner_name}.png"),
            self.__get_chart_path(f"bar_chart_{self.owner_name}.png"),
        ]

        for path in chart_paths:
            if os.path.exists(path):
                os.remove(path)

        self.__creating_bar_chart() 
        self.__creating_line_chart() 
        self.__creating_pie_chart() 

# if __name__ == "__main__": 
#     account = BudgetTrackerAccount(
#         name="Henry",
#         balance=[3000, 3200, 3500, 3800, 4000, 4200, 4500, 4800, 5000, 5200, 5500, 5800],
#         income=[2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000],
#         expense=[800, 850, 900, 750, 800, 820, 780, 810, 790, 830, 860, 870]
#     )

#     account.add_transaction("06/01/25", "Grocery Store", "Food", "Expense", 120)
#     account.add_transaction("06/03/25", "Salary", "Other", "Income", 2000)
#     account.add_transaction("06/05/25", "Bus Pass", "Transport", "Expense", 50)
#     account.add_transaction("06/10/25", "Rent", "Housing", "Expense", 900)
#     account.add_transaction("06/12/25", "Amazon", "Shopping", "Expense", 75)
#     account.add_transaction("06/15/25", "Restaurant", "Food", "Expense", 45)
#     account.add_transaction("06/18/25", "Uber", "Transport", "Expense", 30)
#     account.add_transaction("06/20/25", "Netflix", "Other", "Expense", 15)
#     account.add_transaction("06/22/25", "Freelance", "Other", "Income", 500)
#     account.add_transaction("06/25/25", "Zara", "Shopping", "Expense", 200)

#     account.financial_analysis() 
        

        