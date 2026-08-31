# 🏦 PR Bank

A simple **Bank Management Web Application** built using **Python Flask, SQLite, HTML, CSS, and JavaScript**.

PR Bank provides a basic banking experience where users can create an account, securely log in, manage their account balance, perform deposits and withdrawals, transfer money between accounts, and view transaction history.

> **Note:** This project is developed for educational and portfolio purposes. It is not intended for handling real financial transactions.

---

## 🚀 Live Demo

**Live Application:**\
[https://pr-bank.onrender.com/](https://pr-bank.onrender.com/)

**GitHub Repository:**\
[https://github.com/praneethnalamalapu-afk/PR\_bank](https://github.com/praneethnalamalapu-afk/PR_bank)

---

## ✨ Features

### 🔐 User Authentication

- User registration
- User login and logout
- Password hashing using Werkzeug
- Session-based authentication
- Security questions for account recovery
- Flash messages for login and registration status

### 👤 User Account

Users can provide:

- Full Name
- Username
- Email
- Phone Number
- Gender
- Password

Each registered user receives a bank account automatically.

### 💰 Banking Operations

#### Deposit

Users can add money to their account.

#### Withdraw

Users can withdraw money if sufficient balance is available.

#### Transfer

Users can transfer money from their account to another account.

The application validates:

- Sender account ownership
- Receiver account existence
- Transfer amount
- Available balance

### 📊 Transaction History

Users can view their previous transactions, including:

- Deposits
- Withdrawals
- Transfers
- Transaction amount
- Transaction time
- Destination account for transfers

---

## 🛠️ Technologies Used

| Technology   | Purpose                   |
| ------------ | ------------------------- |
| Python       | Backend programming       |
| Flask        | Web framework             |
| SQLite       | Database                  |
| HTML5        | Web page structure        |
| CSS3         | User interface styling    |
| JavaScript   | Client-side functionality |
| Jinja2       | Flask template rendering  |
| Werkzeug     | Password hashing          |
| Gunicorn     | Production WSGI server    |
| Git & GitHub | Version control           |
| Render       | Cloud deployment          |

---

## 📁 Project Structure

```text
PR_bank/
│
├── app.py
├── requirements.txt
├── README.md
├── prdb.db
│
├── templates/
│   ├── auth.html
│   ├── dashboard.html
│   └── transactions.html
│
└── static/
    ├── style1.css
    └── ...
```

### Main Files

#### `app.py`

Contains the Flask backend and application logic.

It handles:

- User authentication
- Registration
- Database operations
- Deposits
- Withdrawals
- Transfers
- Transactions
- Sessions
- Logout

#### `templates/`

Contains the HTML/Jinja2 templates used by Flask.

#### `static/`

Contains CSS, JavaScript, images, and other static files.

#### `prdb.db`

SQLite database containing application data.

#### `requirements.txt`

Contains the Python dependencies required to run the application.

---

# ⚙️ Installation

## 1. Clone the Repository

```bash
git clone https://github.com/praneethnalamalapu-afk/PR_bank.git
```

Navigate to the project:

```bash
cd PR_bank
```

---

## 2. Create a Virtual Environment

### Windows

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
```

Activate it:

```bash
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure Secret Key

The application uses an environment variable for the Flask secret key.

### Windows CMD

```bash
set SECRET_KEY=your-secret-key
```

### Windows PowerShell

```powershell
$env:SECRET_KEY="your-secret-key"
```

### Linux / macOS

```bash
export SECRET_KEY="your-secret-key"
```

For a stronger secret key, you can generate one using Python:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Do not commit your production secret key to GitHub.

---

# ▶️ Running the Application Locally

Run:

```bash
python app.py
```

The application should start on:

```text
http://127.0.0.1:5000
```

Open the address in your browser.

---

# 🌐 Render Deployment

PR Bank can be deployed using Render.

## 1. Create a Render Web Service

Go to:

[https://render.com/](https://render.com/)

Create a new:

```text
Web Service
```

Connect your GitHub repository:

```text
praneethnalamalapu-afk/PR_bank
```

---

## 2. Render Configuration

Use the following settings:

### Runtime

```text
Python 3
```

### Branch

```text
main
```

### Build Command

```bash
pip install -r requirements.txt
```

### Start Command

```bash
gunicorn app:app
```

---

## 3. Add Environment Variable

In Render:

```text
Environment
    ↓
Add Environment Variable
```

Add:

```text
Key: SECRET_KEY
Value: <your-secret-key>
```

Do not expose this value publicly.

---

## 4. Deploy

Click:

```text
Deploy Web Service
```

Render will:

```text
Clone GitHub repository
        ↓
Install Python
        ↓
Install requirements
        ↓
Install Gunicorn
        ↓
Start Flask application
        ↓
Deploy application
```

After successful deployment, Render will provide a URL similar to:

```text
https://your-project.onrender.com
```

---

# 🗄️ Database

PR Bank currently uses **SQLite**.

The database contains the following tables:

### `users`

Stores registered user information.

```text
id
username
password
full_name
email
phone
gender
```

### `accounts`

Stores bank account information.

```text
id
user_id
balance
```

### `transactions`

Stores banking transactions.

```text
id
account_id
type
amount
to_account
timestamp
```

### `recovery`

Stores security questions and hashed recovery answers.

```text
user_id
q1
a1
q2
a2
q3
a3
```

---

# 🔒 Security

The project implements several basic security practices:

- Passwords are hashed using Werkzeug.
- Recovery answers are hashed.
- SQL queries use parameterized statements.
- Flask sessions are used for authentication.
- Account ownership is validated for banking operations.
- Environment variables are used for sensitive configuration.
- Transfer operations use database transactions.

### Important

This project is **not a production banking system**.

For a real-world financial application, additional security measures would be required, including:

- HTTPS configuration
- CSRF protection
- Rate limiting
- Stronger authentication
- Multi-factor authentication
- Secure password policies
- Proper financial transaction handling
- PostgreSQL or another production database
- Database backups
- Audit logging
- Input validation
- Secure secret management
- Monitoring and alerting

---

# 🔄 Application Flow

```text
                    ┌───────────────┐
                    │   PR Bank     │
                    └───────┬───────┘
                            │
                            ▼
                    ┌───────────────┐
                    │     Login     │
                    └───────┬───────┘
                            │
                    ┌───────┴────────┐
                    │                │
                    ▼                ▼
              Existing User      New User
                    │                │
                    ▼                ▼
                Dashboard        Register
                    │                │
                    │                ▼
                    │             Account
                    │             Created
                    │                │
                    └───────┬────────┘
                            ▼
                       Dashboard
                            │
             ┌──────────────┼──────────────┐
             ▼              ▼              ▼
          Deposit        Withdraw       Transfer
             │              │              │
             └──────────────┼──────────────┘
                            ▼
                    Transaction History
```

---

# 💳 Banking Operations Flow

```text
User
 │
 ├── Deposit
 │      └── Increase Account Balance
 │
 ├── Withdraw
 │      └── Check Balance
 │             ├── Sufficient → Deduct Amount
 │             └── Insufficient → Reject
 │
 └── Transfer
        ├── Validate Sender
        ├── Validate Receiver
        ├── Check Balance
        ├── Deduct Sender Balance
        ├── Add Receiver Balance
        └── Record Transaction
```

---

# 🧪 Testing

The following operations should be tested after deployment:

### Authentication

- [ ] Register a new user
- [ ] Login with valid credentials
- [ ] Reject invalid credentials
- [ ] Logout
- [ ] Access dashboard without login

### Account

- [ ] Account creation
- [ ] Display account balance
- [ ] Deposit money
- [ ] Withdraw money
- [ ] Prevent withdrawal with insufficient balance

### Transfer

- [ ] Transfer to valid account
- [ ] Reject invalid account
- [ ] Reject insufficient balance
- [ ] Reject zero/negative amount
- [ ] Prevent unauthorized account access
- [ ] Prevent transferring to the same account

### Transactions

- [ ] Deposit appears in history
- [ ] Withdrawal appears in history
- [ ] Transfer appears in history
- [ ] Transaction timestamp is displayed

---

# 🐛 Troubleshooting

## `gunicorn: command not found`

Make sure `requirements.txt` contains:

```text
gunicorn==23.0.0
```

Then push the changes:

```bash
git add .
git commit -m "Add Gunicorn"
git push origin main
```

---

## `TemplateNotFound: auth.html`

Make sure the file exists here:

```text
templates/auth.html
```

Correct:

```text
PR_bank/
│
├── app.py
│
└── templates/
    └── auth.html
```

Incorrect:

```text
PR_bank/
│
├── app.py
└── auth.html
```

---

## CSS Not Loading

Use Flask's `url_for()` instead of Windows-style paths.

Use:

```html
<link rel="stylesheet"
      href="{{ url_for('static', filename='style1.css') }}">
```

instead of:

```html
<link rel="stylesheet" href="static\style1.css">
```

---

# 📌 Future Improvements

Possible improvements for future versions:

- [ ] PostgreSQL database
- [ ] Password reset functionality
- [ ] OTP/email verification
- [ ] Two-factor authentication
- [ ] User profile management
- [ ] Multiple bank accounts per user
- [ ] Account numbers
- [ ] Transaction search and filtering
- [ ] PDF transaction statements
- [ ] Admin dashboard
- [ ] Improved validation
- [ ] CSRF protection
- [ ] API integration
- [ ] Better responsive UI
- [ ] Docker deployment
- [ ] Automated testing
- [ ] CI/CD pipeline

---

# 👨‍💻 Author

**Praneeth Reddy Nalamalapu**

Software Developer

GitHub:

[https://github.com/praneethnalamalapu-afk](https://github.com/praneethnalamalapu-afk)

---

# 📄 License

This project is intended for **educational and portfolio purposes**.

You may modify and extend the project for learning and development.
