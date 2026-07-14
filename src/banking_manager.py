import json
import os 
from fastapi import APIRouter, Request, Form 
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

class BankingManager:
    def __init__(self, bank_name="boa"):
        self.banking_accounts = {}

        if bank_name == "boa":
            base = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(base, "..", "information", "boa.json")
            try:
                with open(file_path, "r") as file:
                    self.banking_accounts = json.load(file)
            except FileNotFoundError:
                print("boa.json was not found.")
            except json.JSONDecodeError:
                print("boa.json contains invalid JSON.")

    def user_credential_verification(self, user_id, password):
        if not user_id or not password:
            return {
                "success": False,
                "error": "All required fields need to be filled."
            }

        if user_id not in self.banking_accounts:
            return {
                "success": False,
                "error": "User ID was not found in the system."
            }

        stored_password = self.banking_accounts[user_id]["password"]

        if stored_password != password:
            return {
                "success": False,
                "error": "Incorrect password."
            }

        transactions = self.banking_accounts[user_id].get("transactions", [])

        return {
            "success": True,
            "transactions": transactions
        }
    