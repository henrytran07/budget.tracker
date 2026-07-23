from .budget_tracker_account import * 
from .banking_manager import * 
import random 
from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import Optional
import json
import os


class BudgetTrackerManager: 
    def __init__(self):
        self.account_ids = set() 
        self.accounts = {}
        self.user_credentials = {}

        folder_path = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(folder_path, "..", "information", "trkr_account.json")
        with open(file_path, "r") as file: 
            saved_data = json.load(file)
            self.user_credentials = saved_data["user_credentials"]
        
        for _, data in self.user_credentials.items():
            user_id = data["user_id"]
            self.account_ids.add(user_id)
            self.accounts[user_id] = BudgetTrackerAccount(
                data["gv_name"],
                balance=list(data["balance"]),
                income=list(data["income"]),
                expense=list(data["expense"]),
            )

    def __generate_user_id(self):
        uid = random.randint(1, 10**9)
        while uid in self.account_ids: 
            uid = random.randint(1, 10**9)
        return uid
    
    def sign_up(self, gv_name, email, password):
        if email in self.user_credentials:
            return {"success": False, "error": "Email already registered"}
        
        if not gv_name or not email or not password:
            return {"success": False, "error": "All fields are required"}

        user_id = self.__generate_user_id()
        self.account_ids.add(user_id)
        self.user_credentials[email] = {
            "user_password": password,
            "user_id": user_id
        }
        self.accounts[user_id] = BudgetTrackerAccount(gv_name, balance=[0] * 12,
                                                    income=[0] * 12,
                                                    expense=[0] * 12)

        return {"success": True, "user_id": user_id}
    
    def sign_in(self, email, password): 
        if not email or not password:                         
            return {"success": False, "error": "All fields are required"}
        
        if email not in self.user_credentials:
            return {"success": False, "error": "Email is not registered in the system yet"}

        verified_password = self.user_credentials[email]["user_password"]
        if verified_password != password:
            return {"success": False, "error": "Wrong Email or Password"}

        user_id = self.user_credentials[email]["user_id"]

        return {"success": True, "user_id": user_id}
    

router = APIRouter() 
manager = BudgetTrackerManager()
bank_manager = BankingManager() 
templates = Jinja2Templates(directory="templates") 

@router.post("/")
def login(request: Request, email: str = Form(...), password: str = Form(...)):
    status = manager.sign_in(email, password)

    if status["success"]:
        return RedirectResponse(
            url=f"/dashboard/{status['user_id']}", 
            status_code=303
        )
    
    return templates.TemplateResponse(
        request=request,
        name="sign_in.html",
        context={"error": status["error"]}
    )
@router.get("/")
def login_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="sign_in.html",
        context={}
    )

@router.get("/logout")
def logout():
    return RedirectResponse(url="/", status_code=303)

@router.post("/sign-up")
def sign_up(request : Request, gv_name: str = Form(...), email: str = Form(...), password: str = Form(...)): 
    status = manager.sign_up(gv_name, email, password)
    if status["success"]:
        return RedirectResponse(
            url="/", 
            status_code=303
        )

    return templates.TemplateResponse(
        request=request, 
        name="sign_up.html", 
        context={"error": status["error"]}
    )

@router.get("/sign-up")
def sign_up_page(request : Request):
    return templates.TemplateResponse(
        request=request,
        name="sign_up.html",
        context={}
    )

@router.get("/dashboard/{user_id}")
def dashboard(request : Request, user_id: int): 
    account = manager.accounts[user_id]
    dashboard_info = account.get_dashboard_info()
    name = account.owner_name
    chart_path= account.financial_analysis()
    return templates.TemplateResponse(
        request=request, 
        name="home.html", 
        context={**dashboard_info, "transactions": account.transactions, "user_id": user_id, "name": name, "chart_paths": chart_path}
    )

@router.get("/choose-bank")
def choose_bank(bank_name: str, user_id: int):
    if bank_name == "boa":
        return RedirectResponse(
            url=f"/bank-of-america-login?user_id={user_id}",
            status_code=303
        )

    return {"error": "Unknown bank"}

@router.get("/bank-of-america-login")
def boa_login_page(request: Request, user_id: int):
    return templates.TemplateResponse(
        request=request,
        name="boa.html",
        context={"user_id": user_id}
    )

@router.post("/dashboard/{user_id}")
def create_transaction(user_id: int, date: str = Form(...), description: str = Form(...), amount: float = Form(...), transaction_type: str = Form(...), category: str = Form(...)): 
    account = manager.accounts[user_id]
    account.add_transaction(date, description, amount, transaction_type, category)
    return RedirectResponse(
        url=f"/dashboard/{user_id}", 
        status_code=303
    )

@router.post("/bank-of-america-login")
def boa_login_verification(request: Request, bank_user_id: str = Form(), password: str = Form(), user_id: int = Form()):
    status = bank_manager.user_credential_verification(bank_user_id, password)
    if status["success"] == True:
        print(f"user_id: {user_id}")
        transactions = status["transactions"]
        account = manager.accounts[user_id]
        for t in transactions:
            account.add_transaction(t["date"], t["description"], t["amount"], t["type"], t["category"])
        return RedirectResponse(url=f"/dashboard/{user_id}", status_code=303)
    
    return templates.TemplateResponse(
        request=request,
        name="boa.html",
        context={"error": "Invalid credentials", "user_id": user_id}
    )

