from budget_tracker_account import * 
import random 

class BudgetTrackerManager: 
    def __init__(self):
        """
            account_ids: set(account_id)
            accounts: dict(account_ids : budget_tracker_account)
            user_credentials: dict(user_email : {user_password, and user_id}) 
            BudgetTrackerAccount: name, balance, income, expense, 
        """
        self.account_ids = set() 
        self.accounts = {}
        self.user_credentials = {}

    def __generate_user_id(self):
        n = max(len(self.account_ids), 1)
        pool = set(range(1, 5 * n + 1)) - set(self.account_ids)
        return random.choice(list(pool))
    
    def sign_up(self, gv_name, email, password):
        """
            api sent information of goverment name, email, password 
            Return False if email isn't in user_credentials or gv_name || email || password is a empty string ("")
            else Return True 
        """
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
        self.accounts[user_id] = BudgetTrackerAccount(gv_name)

        return {"success": True, "user_id": user_id}
    
    def sign_in(self, email, password): 
        """
            api sent email, and password to verify
        """
        if not email or not password:                         
            return {"success": False, "error": "All fields are required"}
        
        if email not in self.user_credentials:
            return {"success": False, "error": "Email is not registered in the system yet"}

        verified_password = self.user_credentials[email]["user_password"]
        if verified_password != password:
            return {"success": False, "error": "Wrong Email or Password"}

        user_id = self.user_credentials[email]["user_id"]
        return {"success": True, "account": self.accounts[user_id]}
    


# if __name__ == "__main__": 
#     manager = BudgetTrackerManager()

#     print("=" * 40)
#     print("SIGN UP TESTS")
#     print("=" * 40)

#     # Normal sign up
#     print(manager.sign_up("John Doe", "john@email.com", "pass123"))
#     # Expected: {"success": True, "user_id": ...}

#     # Duplicate email
#     print(manager.sign_up("John Doe", "john@email.com", "pass123"))
#     # Expected: {"success": False, "error": "Email already registered"}

#     # Empty fields
#     print(manager.sign_up("", "jane@email.com", "pass123"))
#     # Expected: {"success": False, "error": "All fields are required"}

#     print(manager.sign_up("Jane Doe", "", "pass123"))
#     # Expected: {"success": False, "error": "All fields are required"}

#     print(manager.sign_up("Jane Doe", "jane@email.com", ""))
#     # Expected: {"success": False, "error": "All fields are required"}

#     # Second valid user
#     print(manager.sign_up("Jane Doe", "jane@email.com", "mypassword"))
#     # Expected: {"success": True, "user_id": ...}

#     print("=" * 40)
#     print("SIGN IN TESTS")
#     print("=" * 40)

#     # Correct credentials
#     print(manager.sign_in("john@email.com", "pass123"))
#     # Expected: {"success": True, "account": <BudgetTrackerAccount>}

#     # Wrong password
#     print(manager.sign_in("john@email.com", "wrongpass"))
#     # Expected: {"success": False, "error": "Wrong Email or Password"}

#     # Email not registered
#     print(manager.sign_in("unknown@email.com", "pass123"))
#     # Expected: {"success": False, "error": "Email is not registered in the system yet"}

#     # Empty fields
#     print(manager.sign_in("", "pass123"))
#     # Expected: {"success": False, "error": "All fields are required"}

#     print(manager.sign_in("john@email.com", ""))
#     # Expected: {"success": False, "error": "All fields are required"}

#     print("=" * 40)
#     print("STATE CHECK")
#     print("=" * 40)

#     # Verify internal state looks correct
#     print("Account IDs:", manager.account_ids)
#     print("Registered emails:", list(manager.user_credentials.keys()))
#     print("Accounts:", manager.accounts)
