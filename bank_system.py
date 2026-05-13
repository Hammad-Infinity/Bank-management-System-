import json
from pathlib import Path
from models import BankAccount, BankOpError, AcctNotExistError, IncorrectPwdError


class BankingSystem:
    
    def __init__(self, db_file="bank_data.json"):
        self.db_file = Path(db_file)
        self.all_accounts = self._load_from_disk()
        self.current_user = None
    
    def _load_from_disk(self):
        if not self.db_file.exists():
            return {}
        
        try:
            with open(self.db_file, 'r') as f:
                raw_data = json.load(f)
                restored_accounts = {}
                for acct_id, acct_data in raw_data.items():
                    restored_accounts[acct_id] = BankAccount.from_storage(acct_id, acct_data)
                return restored_accounts
        except (json.JSONDecodeError, IOError) as e:
            print(f"Could not load previous data: {e}")
            return {}
    
    def _save_to_disk(self):
        output_data = {}
        for acct_id, acct in self.all_accounts.items():
            output_data[acct_id] = acct.to_storage()
        
        with open(self.db_file, 'w') as f:
            json.dump(output_data, f, indent=2)
    
    def register_account(self, acct_num, name, pwd):
        if len(pwd) < BankAccount.MIN_PWD_LEN:
            raise ValueError(f"Password minimum {BankAccount.MIN_PWD_LEN} chars")
        
        if acct_num in self.all_accounts:
            raise BankOpError(f"Account {acct_num} already exists")
        
        new_acct = BankAccount(acct_num, name, pwd)
        self.all_accounts[acct_num] = new_acct
        self._save_to_disk()
        return new_acct
    
    def login_acct(self, acct_num, pwd):
        if acct_num not in self.all_accounts:
            raise AcctNotExistError(f"Account not found: {acct_num}")
        
        acct = self.all_accounts[acct_num]
        
        if acct.is_locked():
            raise BankOpError("Account locked. Try again later.")
        
        if not acct.check_pwd(pwd):
            acct.handle_login_fail()
            self._save_to_disk()
            raise IncorrectPwdError("Wrong password")
        
        acct.reset_login_attempts()
        self.current_user = acct
        return acct
    
    def logout_user(self):
        self.current_user = None
    
    def find_account(self, acct_num):
        return self.all_accounts.get(acct_num)
    
    def save_all(self):
        self._save_to_disk()
