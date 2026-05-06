from bank_system import BankingSystem
from models import BankOpError, AcctNotExistError, IncorrectPwdError, LowBalanceError


class BankInterface:
    
    def __init__(self):
        self.bank = BankingSystem()
        self.user = None
    
    def _prompt_valid_number(self, msg):
        while True:
            try:
                val = float(input(msg))
                if val <= 0:
                    print("Must be positive")
                    continue
                return val
            except ValueError:
                print("Invalid number")
    
    def _prompt_text(self, msg):
        while True:
            val = input(msg).strip()
            if val:
                return val
            print("Cannot be empty")
    
    def create_new_acct(self):
        print("\n" + "="*34)
        print("OPEN NEW ACCOUNT")
        print("="*34)
        
        try:
            acct_num = self._prompt_text("Account number: ")
            full_name = self._prompt_text("Full name: ")
            pwd = self._prompt_text("Create password (4+ chars): ")
            
            new_acct = self.bank.register_account(acct_num, full_name, pwd)
            print(f"Account created! {acct_num}")
        except BankOpError as e:
            print(f"{e}")
        except ValueError as e:
            print(f"{e}")
    
    def login_screen(self):
        print("\n" + "="*34)
        print("ACCOUNT LOGIN")
        print("="*34)
        
        try:
            acct_num = self._prompt_text("Account number: ")
            pwd = input("Password: ")
            
            self.user = self.bank.login_acct(acct_num, pwd)
            print(f"Logged in as {self.user.cust_name}")
            return True
        except (AcctNotExistError, IncorrectPwdError, BankOpError) as e:
            print(f"Login failed: {e}")
            return False
    
    def deposit_money(self):
        print("\n___ DEPOSIT ___")
        try:
            amt = self._prompt_valid_number("Deposit amount ($): ")
            src = self._prompt_text("Source of funds: ")
            self.user.deposit_money(amt, src)
            print(f"Deposited ${amt:.2f}")
            print(f"Balance: ${self.user.balance:.2f}")
        except ValueError as e:
            print(f"{e}")
    
    def withdraw_money(self):
        """Withdraw screen"""
        print("\n--- WITHDRAWAL ---")
        try:
            amt = self._prompt_valid_number("Withdraw amount ($): ")
            self.user.withdraw_amount(amt)
            print(f"Withdrawn ${amt:.2f}")
            print(f"Balance: ${self.user.balance:.2f}")
        except (LowBalanceError, ValueError) as e:
            print(f"{e}")
    
    def transfer_money(self):
        """Transfer screen"""
        print("\n--- SEND MONEY ---")
        try:
            recv_acct_num = self._prompt_text("Recipient account: ")
            recv_acct = self.bank.find_account(recv_acct_num)
            
            if not recv_acct:
                print(f"Account {recv_acct_num} not found")
                return
            
            amt = self._prompt_valid_number("Amount to send ($): ")
            
            self.user.send_money(recv_acct, amt)
            self.bank.save_all()
            
            print(f"Sent ${amt:.2f} to {recv_acct.cust_name}")
            print(f"Your balance: ${self.user.balance:.2f}")
        except (LowBalanceError, ValueError) as e:
            print(f"{e}")
    
    def show_balance(self):
        """Show account info"""
        print("\n" + "-"*34)
        print("ACCOUNT INFORMATION")
        print("-"*34)
        info = self.user.get_acct_info()
        print(f"Account#: {info['account_number']}")
        print(f"Name: {info['customer_name']}")
        print(f"Balance: ${info['current_balance']:.2f}")
        print(f"Transactions: {info['recent_txns']}")
        print("-"*34)
    
    def show_transactions(self):
        print("\n" + "-"*34)
        print("RECENT TRANSACTIONS")
        print("-"*34)
        
        if not self.user.txn_log:
            print("No transactions yet")
        else:
            for txn in self.user.txn_log[-10:]:
                txn_time = txn['timestamp'][:19]
                txn_type = txn['type']
                amt = txn.get('amount', '')
                if txn_type == 'ACCOUNT_CREATED':
                    print(f"{txn_time} | {txn_type:15} | ${amt:>8.2f}")
                elif txn_type == 'TRANSFER_IN':
                    print(f"{txn_time} | {'RECEIVED':15} | ${amt:>8.2f} from {txn['sender']}")
                elif txn_type == 'TRANSFER_OUT':
                    print(f"{txn_time} | {'SENT':15} | ${amt:>8.2f} to {txn['recipient']}")
                else:
                    print(f"{txn_time} | {txn_type:15} | ${amt:>8.2f}")
        
        print("-"*34)
    
    def user_menu(self):
        print("\n" + "="*34)
        print(f"MAIN MENU - {self.user.cust_name}")
        print("="*34)
        print("1. Deposit money")
        print("2. Withdraw money")
        print("3. Send money")
        print("4. Check balance")
        print("5. Transaction history")
        print("6. Logout")
        print("="*34)
        
        choice = input("Select (1-6): ").strip()
        
        if choice == '1':
            self.deposit_money()
        elif choice == '2':
            self.withdraw_money()
        elif choice == '3':
            self.transfer_money()
        elif choice == '4':
            self.show_balance()
        elif choice == '5':
            self.show_transactions()
        elif choice == '6':
            print(f"Goodbye!")
            self.bank.logout_user()
            self.user = None
            return False
        else:
            print("Invalid choice")
        
        return True
    
    def main_menu(self):
        print("\n" + "="*34)
        print("BANKING SYSTEM")
        print("="*34)
        print("1. Create account")
        print("2. Login")
        print("3. Exit")
        print("="*34)
        
        choice = input("Choose (1-3): ").strip()
        
        if choice == '1':
            self.create_new_acct()
        elif choice == '2':
            if self.login_screen():
                while self.user:
                    if not self.user_menu():
                        break
        elif choice == '3':
            print("Thank you!")
            return False
        else:
            print("Invalid choice")
        
        return True
    
    def run(self):
        while self.main_menu():
            pass


if __name__ == "__main__":
    app = BankInterface()
    app.run()
