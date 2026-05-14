# 🏦 Banking System

A professional, modular Python banking management system with multiple accounts, transactions tracking, and persistent data storage.

## Features

✅ **Account Management**
- Create new bank accounts with secure password hashing
- Login/logout functionality
- Account lockout after failed login attempts (3 attempts = 15 min lockout)

✅ **Banking Operations**
- Deposit money with source tracking
- Withdraw money with daily limits ($50,000)
- Transfer money between accounts with transfer limits ($100,000)
- Complete transaction history with timestamps

✅ **Security**
- SHA-256 password hashing
- Failed login tracking
- Automatic account lockout mechanism
- Daily withdrawal limits to prevent suspicious activities

✅ **Data Persistence**
- Automatic JSON file storage
- Load/save account data on startup/shutdown
- Transaction logging for audit trail

## Project Structure

```
├── models.py           # Data models and business logic
├── bank_system.py      # Banking operations management
├── main.py            # Command-line user interface
├── bank_data.json     # Account data storage (auto-created)
└── README.md          # Documentation
```

### File Descriptions

**models.py** - Core Data Models
- `BankAccount` - Individual account with operations
- Custom Exceptions - `BankOpError`, `IncorrectPwdError`, `LowBalanceError`, `AcctNotExistError`
- Password hashing and validation logic
- Transaction logging system

**bank_system.py** - System Management
- `BankingSystem` - Manages all accounts and operations
- Account registration and authentication
- Data persistence (save/load JSON)
- User session management

**main.py** - User Interface
- `BankInterface` - Command-line menu system
- Input validation and error handling
- User-friendly screens for all operations

## Installation

### Requirements
- Python 3.7 or higher
- No external dependencies required

### Setup

1. **Clone or download the files:**
```bash
git clone <repository-url>
cd banking-system
```

2. **Run the application:**
```bash
python main.py
```

## Usage Guide

### Starting the Application
```bash
python main.py
```

### Main Menu Options

```
🏦 BANKING SYSTEM
1. Create account
2. Login
3. Exit
```

### Creating an Account

1. Select option `1`
2. Enter account number (e.g., ACC001)
3. Enter full name (e.g., John Doe)
4. Create password (minimum 4 characters)

**Example:**
```
Account number: ACC001
Full name: John Doe
Create password (4+ chars): mypassword123
✅ Account created! ACC001
```

### Logging In

1. Select option `2`
2. Enter account number
3. Enter password

**Example:**
```
Account number: ACC001
Password: mypassword123
✅ Logged in as John Doe
```

### User Menu Operations

Once logged in, access these features:

#### **1. Deposit Money**
```
Deposit amount ($): 500
Source of funds: salary
✅ Deposited $500.00
   Balance: $1500.00
```

#### **2. Withdraw Money**
```
Withdraw amount ($): 200
✅ Withdrawn $200.00
   Balance: $1300.00
```

#### **3. Send Money**
```
Recipient account: ACC002
Amount to send ($): 300
✅ Sent $300.00 to Jane Smith
   Your balance: $1000.00
```

#### **4. Check Balance**
```
ACCOUNT INFORMATION
Account#: ACC001
Name: John Doe
Balance: $1000.00
Transactions: 5
```

#### **5. Transaction History**
```
RECENT TRANSACTIONS
2024-05-06 10:30:45 | ACCOUNT_CREATED | $1000.00
2024-05-06 10:31:22 | DEPOSIT         | $500.00
2024-05-06 10:32:10 | SENT            | $300.00 to Jane Smith
```

#### **6. Logout**
Safely exit your session.

## Business Rules & Limits

| Rule | Limit |
|------|-------|
| **Minimum Password Length** | 4 characters |
| **Failed Login Attempts** | 3 attempts lock account |
| **Account Lockout Duration** | 15 minutes |
| **Daily Withdrawal Limit** | $50,000 |
| **Single Transfer Limit** | $100,000 |
| **Starting Balance** | $1,000 |

## Error Handling

The system provides clear error messages for common issues:

```
❌ Insufficient funds. Have: $500.00
❌ Daily limit exceeded. Can withdraw: $10,000.00
❌ Account locked. Try again later.
❌ Login failed: Wrong password
❌ Transfer limit: $100000
```

## Data Storage

All account data is automatically saved to `bank_data.json`:

```json
{
  "ACC001": {
    "name": "John Doe",
    "pwd_hash": "8d969eef6ecad3c29a3a873fba8305d2...",
    "balance": 1000.5,
    "txn_log": [
      {
        "type": "DEPOSIT",
        "amount": 500,
        "timestamp": "2024-05-06T10:31:22.123456",
        "balance_after": 1500
      }
    ],
    "failed_logins": 0,
    "locked_until": null,
    "daily_withdrawn": 200,
    "last_withdraw_date": "2024-05-06"
  }
}
```

## How Files Interact

```
main.py (User Interface)
   │
   ├─ imports ─> BankingSystem from bank_system.py
   │                  │
   │                  └─ imports ─> BankAccount from models.py
   │
   └─ imports ─> Exceptions from models.py

Data Flow:
User Input (main.py)
   ↓
Business Logic (bank_system.py)
   ↓
Data Models (models.py)
   ↓
JSON Storage (bank_data.json)
```

## Code Highlights

### Modular Design
- **models.py**: Data and exceptions (no UI code)
- **bank_system.py**: Business logic (independent from UI)
- **main.py**: User interface (only presentation)

### Key Features in Code

**Password Security** (models.py)
```python
@staticmethod
def _secure_pwd(pwd):
    return hashlib.sha256(pwd.encode()).hexdigest()
```

**Account Lockout** (models.py)
```python
def handle_login_fail(self):
    self.failed_login_count += 1
    if self.failed_login_count >= self.FAILED_LOGIN_THRESHOLD:
        self.locked_until = datetime.now() + timedelta(minutes=15)
```

**Daily Withdrawal Limit** (models.py)
```python
if self.daily_withdrawn + amt > self.DAILY_WITHDRAW_LIMIT:
    remaining = self.DAILY_WITHDRAW_LIMIT - self.daily_withdrawn
    raise LowBalanceError(f"Daily limit exceeded. Can withdraw: ${remaining:.2f}")
```

## Example Workflow

### Complete Banking Session

```bash
$ python main.py

🏦 BANKING SYSTEM
1. Create account
2. Login
3. Exit

Choose (1-3): 1

OPEN NEW ACCOUNT
Account number: ACC001
Full name: Alice Johnson
Create password (4+ chars): secure123
✅ Account created! ACC001

🏦 BANKING SYSTEM
Choose (1-3): 2

ACCOUNT LOGIN
Account number: ACC001
Password: secure123
✅ Logged in as Alice Johnson

MAIN MENU - Alice Johnson
1. Deposit money
2. Withdraw money
3. Send money
4. Check balance
5. Transaction history
6. Logout

Select (1-6): 1

--- DEPOSIT ---
Deposit amount ($): 1000
Source of funds: initial_deposit
✅ Deposited $1000.00
   Balance: $2000.00

Select (1-6): 4

ACCOUNT INFORMATION
Account#: ACC001
Name: Alice Johnson
Balance: $2000.00
Transactions: 2

Select (1-6): 6

📤 Goodbye!

🏦 BANKING SYSTEM
Choose (1-3): 3

✋ Thank you!
```

## Troubleshooting

### Issue: "Module not found" error
**Solution:** Make sure all three files (`models.py`, `bank_system.py`, `main.py`) are in the same directory.

### Issue: Cannot login after account creation
**Solution:** Password is case-sensitive. Enter the exact password you created.

### Issue: "Account locked" message
**Solution:** You've failed to login 3 times. Wait 15 minutes before trying again.

### Issue: JSON decode error
**Solution:** Delete `bank_data.json` and restart the application to create a fresh database.

## Architecture Benefits

✅ **Separation of Concerns**
- Models handle data
- System handles logic
- Interface handles UI

✅ **Easy to Extend**
- Add new account types by extending `BankAccount`
- Add new operations in `BankingSystem`
- Add new UI screens in `BankInterface`

✅ **Testable Code**
- Business logic independent from UI
- Can unit test `models.py` and `bank_system.py` separately

✅ **Maintainable**
- Clear file structure
- Single responsibility per class
- Well-documented code

## Future Enhancements

Possible additions to the system:

- [ ] Email notifications for transactions
- [ ] Admin dashboard
- [ ] Export transaction reports
- [ ] Savings accounts with interest
- [ ] Multiple user types (Admin, Customer, Operator)
- [ ] Transaction categories
- [ ] Mobile-friendly interface
- [ ] Database integration (SQLite/PostgreSQL)

## Security Notes

⚠️ **For Educational Use Only**

This is a demonstration project. For production use:
- Use proper database instead of JSON
- Implement OAuth/2FA authentication
- Use industry-standard encryption
- Add comprehensive logging and monitoring
- Implement SSL/TLS for network communication
- Add rate limiting
- Regular security audits

## Requirements

- Python 3.7+
- Standard library only (no pip packages needed)

```
- hashlib (password hashing)
- datetime (timestamps)
- pathlib (file paths)
- json (data storage)
```

## License

This project is open source and available for educational purposes.

## Support

For issues or questions:
1. Check the Troubleshooting section
2. Review the code comments
3. Check the usage examples

---

**Built with ❤️ using Python OOP principles**

*Last Updated: May 6, 2024*
