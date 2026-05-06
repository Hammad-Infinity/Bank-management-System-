import hashlib
from datetime import datetime, timedelta


class BankOpError(Exception):
    pass


class IncorrectPwdError(BankOpError):
    pass


class LowBalanceError(BankOpError):
    pass


class AcctNotExistError(BankOpError):
    pass


class BankAccount:
    
    STARTING_BALANCE = 1000
    MIN_PWD_LEN = 4
    DAILY_WITHDRAW_LIMIT = 50000
    MAX_SINGLE_TRANSFER = 100000
    FAILED_LOGIN_THRESHOLD = 3
    
    def __init__(self, acct_num, cust_name, pwd, start_bal=STARTING_BALANCE):
        self.acct_num = acct_num
        self.cust_name = cust_name
        self.pwd_hash = self._secure_pwd(pwd)
        self.balance = float(start_bal)
        self.txn_log = []
        self.failed_login_count = 0
        self.locked_until = None
        self.daily_withdrawn = 0
        self.last_withdraw_date = None
        
        self.txn_log.append({
            'type': 'ACCOUNT_CREATED',
            'amount': start_bal,
            'timestamp': datetime.now().isoformat(),
            'details': f'Account opened'
        })
    
    @staticmethod
    def _secure_pwd(pwd):
        return hashlib.sha256(pwd.encode()).hexdigest()
    
    def check_pwd(self, pwd):
        return self.pwd_hash == self._secure_pwd(pwd)
    
    def is_locked(self):
        if self.locked_until and datetime.now() < self.locked_until:
            return True
        elif self.locked_until and datetime.now() >= self.locked_until:
            self.locked_until = None
            self.failed_login_count = 0
        return False
    
    def handle_login_fail(self):
        self.failed_login_count += 1
        if self.failed_login_count >= self.FAILED_LOGIN_THRESHOLD:
            self.locked_until = datetime.now() + timedelta(minutes=15)
    
    def reset_login_attempts(self):
        self.failed_login_count = 0
        self.locked_until = None
    
    def deposit_money(self, amt, source=""):
        if amt <= 0:
            raise ValueError("Deposit must be positive")
        
        self.balance += amt
        self.txn_log.append({
            'type': 'DEPOSIT',
            'amount': amt,
            'timestamp': datetime.now().isoformat(),
            'balance_after': self.balance,
            'source': source
        })
    
    def withdraw_amount(self, amt):
        if amt <= 0:
            raise ValueError("Withdrawal must be positive")
        
        today = datetime.now().date()
        if self.last_withdraw_date != today:
            self.daily_withdrawn = 0
            self.last_withdraw_date = today
        
        if self.daily_withdrawn + amt > self.DAILY_WITHDRAW_LIMIT:
            remaining = self.DAILY_WITHDRAW_LIMIT - self.daily_withdrawn
            raise LowBalanceError(f"Daily limit exceeded. Can withdraw: ${remaining:.2f}")
        
        if amt > self.balance:
            raise LowBalanceError(f"Insufficient funds. Have: ${self.balance:.2f}")
        
        self.balance -= amt
        self.daily_withdrawn += amt
        self.txn_log.append({
            'type': 'WITHDRAWAL',
            'amount': amt,
            'timestamp': datetime.now().isoformat(),
            'balance_after': self.balance
        })
    
    def send_money(self, recipient_acct, amt):
        if amt <= 0:
            raise ValueError("Transfer must be positive")
        
        if amt > self.MAX_SINGLE_TRANSFER:
            raise ValueError(f"Transfer limit: ${self.MAX_SINGLE_TRANSFER}")
        
        if amt > self.balance:
            raise LowBalanceError(f"Not enough balance. Have: ${self.balance}")
        
        self.balance -= amt
        self.txn_log.append({
            'type': 'TRANSFER_OUT',
            'amount': amt,
            'recipient': recipient_acct.cust_name,
            'recipient_acct': recipient_acct.acct_num,
            'timestamp': datetime.now().isoformat(),
            'balance_after': self.balance
        })
        
        recipient_acct.balance += amt
        recipient_acct.txn_log.append({
            'type': 'TRANSFER_IN',
            'amount': amt,
            'sender': self.cust_name,
            'sender_acct': self.acct_num,
            'timestamp': datetime.now().isoformat(),
            'balance_after': recipient_acct.balance
        })
    
    def get_acct_info(self):
        return {
            'account_number': self.acct_num,
            'customer_name': self.cust_name,
            'current_balance': self.balance,
            'acct_locked': self.is_locked(),
            'recent_txns': len(self.txn_log)
        }
    
    def to_storage(self):
        return {
            'name': self.cust_name,
            'pwd_hash': self.pwd_hash,
            'balance': self.balance,
            'txn_log': self.txn_log,
            'failed_logins': self.failed_login_count,
            'locked_until': self.locked_until.isoformat() if self.locked_until else None,
            'daily_withdrawn': self.daily_withdrawn,
            'last_withdraw_date': self.last_withdraw_date.isoformat() if self.last_withdraw_date else None
        }
    
    @classmethod
    def from_storage(cls, acct_num, stored_data):
        acct = cls.__new__(cls)
        acct.acct_num = acct_num
        acct.cust_name = stored_data['name']
        acct.pwd_hash = stored_data['pwd_hash']
        acct.balance = stored_data['balance']
        acct.txn_log = stored_data['txn_log']
        acct.failed_login_count = stored_data.get('failed_logins', 0)
        
        locked_str = stored_data.get('locked_until')
        acct.locked_until = datetime.fromisoformat(locked_str) if locked_str else None
        
        withdraw_date_str = stored_data.get('last_withdraw_date')
        acct.last_withdraw_date = datetime.fromisoformat(withdraw_date_str).date() if withdraw_date_str else None
        acct.daily_withdrawn = stored_data.get('daily_withdrawn', 0)
        
        return acct
