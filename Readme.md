💳 Banking Web Application (Flask)
A secure, minimal banking web application built using Flask, SQLite, and HTML/CSS.
This project demonstrates core backend development concepts including authentication, transactions, and account recovery.

🚀 Features
🔐 Authentication
User Registration & Login
Password hashing using Werkzeug
Secure session handling
👤 User Profile
Stores Name, Email, Phone, Gender
Personalized dashboard:
Welcome Mr/Ms [Name]
💰 Banking Operations
Create account (auto-generated)
Deposit money
Withdraw money
Transfer funds between accounts
📊 Transactions
Full transaction history
Includes:
Type (Deposit / Withdraw / Transfer)
Amount
Receiver account (for transfers)
Timestamp
Sorting & filtering support
🔁 Account Recovery
3 Security Questions
Hashed answers
Password reset functionality
🛠️ Tech Stack
Backend: Python (Flask)
Frontend: HTML, CSS, JavaScript
Database: SQLite
Security: Werkzeug password hashing

📁 Project Structure
PR_bank/
│── app.py
│── prdb.db (not included in repo)
│── requirements.txt
│── Procfile
│
├── templates/
│   ├── base.html
│   ├── auth.html
│   ├── dashboard.html
│   ├── transactions.html
│   ├── recover.html
│   ├── reset_password.html
│
├── static/
│   ├── style.css
│   ├── script.js

⚙️ Setup Instructions (Local)
1. Clone the repository
git clone https://github.com/your-username/PR_bank.git
cd PR_bank
2. Install dependencies
pip install -r requirements.txt
3. Run the application
python app.py
4. Open browser
http://127.0.0.1:5000

🌐 Deployment
This project can be deployed on:
Render (recommended)
Railway
PythonAnywhere
⚠️ Note: SQLite is not ideal for production. Use PostgreSQL for persistence.

🔐 Security Notes
Passwords and recovery answers are hashed
Input validation implemented
Sessions secured using secret key
📌 Future Improvements
PostgreSQL integration
Email verification / OTP login
JWT authentication
Transaction analytics dashboard
Payment gateway integration
👨‍💻 Author
Praneeth Reddy

⭐ If you like this project
Give it a star ⭐ on GitHub!

