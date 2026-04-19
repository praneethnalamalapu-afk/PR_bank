from flask import Flask, render_template, request, redirect, session, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = "super_secret_key"

DB = os.path.join(os.path.dirname(__file__), "prdb.db")

# ---------------- DB ----------------
def get_db():
    conn = sqlite3.connect(DB, timeout=10, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn
def init_db():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("PRAGMA journal_mode=WAL;")
    # USERS
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        full_name TEXT,
        email TEXT,
        phone TEXT,
        gender TEXT
    )
    """)

    # ACCOUNTS
    cur.execute("""
    CREATE TABLE IF NOT EXISTS accounts(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        balance REAL DEFAULT 0
    )
    """)

    # TRANSACTIONS (FINAL FIXED)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS transactions(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        account_id INTEGER,
        type TEXT,
        amount REAL,
        to_account INTEGER,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # RECOVERY
    cur.execute("""
    CREATE TABLE IF NOT EXISTS recovery(
        user_id INTEGER,
        q1 TEXT, a1 TEXT,
        q2 TEXT, a2 TEXT,
        q3 TEXT, a3 TEXT
    )
    """)

    conn.commit()
    conn.close()


# ---------------- QUESTIONS ----------------
QUESTIONS = [
    "What is your childhood nickname?",
    "What was your first school?",
    "What is your favorite food?",
    "What is your pet’s name?",
    "What city were you born in?"
]


# ---------------- HOME ----------------
@app.route("/")
def index():
    if "user_id" in session:
        return redirect("/dashboard")
    return redirect("/login")


# ---------------- AUTH ----------------
@app.route("/login", methods=["GET","POST"])
@app.route("/register", methods=["GET","POST"])
def auth():
    if request.method == "POST":

        # -------- LOGIN --------
        if request.path == "/login":
            username = request.form["username"]
            password = request.form["password"]

            conn = get_db()
            cur = conn.cursor()
            cur.execute("SELECT * FROM users WHERE username=?", (username,))
            user = cur.fetchone()

            if user and check_password_hash(user["password"], password):
                session["user_id"] = user["id"]
                return redirect("/dashboard")
            else:
                flash("Invalid credentials", "error")
                return redirect("/login")

        # -------- REGISTER --------
        else:
            username = request.form["username"]
            password = generate_password_hash(request.form["password"])
            full_name = request.form["full_name"]
            phone = request.form["phone"]
            email = request.form["email"]
            gender = request.form["gender"]

            # VALIDATION
            if not phone.isdigit():
                flash("Invalid phone number", "error")
                return redirect("/register")

            if "@" not in email:
                flash("Invalid email", "error")
                return redirect("/register")

            q1, q2, q3 = request.form["q1"], request.form["q2"], request.form["q3"]
            a1 = generate_password_hash(request.form["a1"].lower())
            a2 = generate_password_hash(request.form["a2"].lower())
            a3 = generate_password_hash(request.form["a3"].lower())

            conn = get_db()
            cur = conn.cursor()

            try:
                cur.execute("""
                INSERT INTO users(username,password,full_name,email,phone,gender)
                VALUES(?,?,?,?,?,?)
                """, (username, password, full_name, email, phone, gender))

                user_id = cur.lastrowid

                cur.execute("""
                INSERT INTO recovery VALUES(?,?,?,?,?,?,?)
                """, (user_id, q1, a1, q2, a2, q3, a3))

                cur.execute("INSERT INTO accounts(user_id,balance) VALUES(?,0)", (user_id,))

                conn.commit()

                flash("Registered successfully", "success")
                return redirect("/login")

            except sqlite3.IntegrityError:
                flash("User exists", "error")
                return redirect("/register")

    return render_template("auth.html", questions=QUESTIONS)


# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/login")

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM users WHERE id=?", (session["user_id"],))
    user = cur.fetchone()

    cur.execute("SELECT * FROM accounts WHERE user_id=?", (session["user_id"],))
    accounts = cur.fetchall()

    return render_template("dashboard.html", user=user, accounts=accounts)


# ---------------- DEPOSIT ----------------
@app.route("/deposit/<int:acc_id>", methods=["POST"])
def deposit(acc_id):
    amount = float(request.form["amount"])

    conn = get_db()
    cur = conn.cursor()

    try:
        cur.execute("UPDATE accounts SET balance = balance + ? WHERE id=?", (amount, acc_id))

        cur.execute("""
        INSERT INTO transactions(account_id,type,amount,to_account)
        VALUES(?,?,?,NULL)
        """, (acc_id, "DEPOSIT", amount))

        conn.commit()
        flash("Deposit completed successfully", "success")
    finally:
        conn.close()

    return redirect("/dashboard")


# ---------------- WITHDRAW ----------------
@app.route("/withdraw/<int:acc_id>", methods=["POST"])
def withdraw(acc_id):
    amount = float(request.form["amount"])

    conn = get_db()
    cur = conn.cursor()

    try:
        cur.execute("SELECT balance FROM accounts WHERE id=?", (acc_id,))
        bal = cur.fetchone()["balance"]

        if bal >= amount:
            cur.execute("UPDATE accounts SET balance = balance - ? WHERE id=?", (amount, acc_id))

            cur.execute("""
            INSERT INTO transactions(account_id,type,amount,to_account)
            VALUES(?,?,?,NULL)
            """, (acc_id, "WITHDRAW", amount))

            conn.commit()
            flash("Withdrawal successful", "success")
        else:
            flash("Insufficient funds", "error")
    finally:
        conn.close()

    return redirect("/dashboard")


# ---------------- TRANSFER ----------------
@app.route("/transfer", methods=["POST"])
def transfer():
    if "user_id" not in session:
        return redirect("/login")

    from_acc = request.form["from"]
    to_acc = request.form["to"]
    amount = float(request.form["amount"])

    conn = get_db()
    cur = conn.cursor()

    try:
        # Validate sender
        cur.execute("SELECT * FROM accounts WHERE id=? AND user_id=?", 
                    (from_acc, session["user_id"]))
        sender = cur.fetchone()

        if not sender:
            flash("Unauthorized access", "error")
            return redirect("/dashboard")

        # Validate receiver
        cur.execute("SELECT * FROM accounts WHERE id=?", (to_acc,))
        receiver = cur.fetchone()

        if not receiver:
            flash("Invalid receiver account", "error")
            return redirect("/dashboard")

        if amount <= 0:
            flash("Invalid amount", "error")
            return redirect("/dashboard")

        if sender["balance"] < amount:
            flash("Insufficient balance", "error")
            return redirect("/dashboard")

        # ✅ Atomic operations
        cur.execute("UPDATE accounts SET balance = balance - ? WHERE id=?", (amount, from_acc))
        cur.execute("UPDATE accounts SET balance = balance + ? WHERE id=?", (amount, to_acc))

        cur.execute("""
        INSERT INTO transactions(account_id,type,amount,to_account)
        VALUES(?,?,?,?)
        """, (from_acc, "TRANSFER", amount, to_acc))

        conn.commit()
        flash("Transfer is successful", "success")

    except Exception as e:
        conn.rollback()
        print("ERROR:", e)
        flash("Transaction failed", "error")

    finally:
        conn.close()

    return redirect("/dashboard")


# ---------------- TRANSACTIONS PAGE ----------------
@app.route("/transactions")
def transactions():
    if "user_id" not in session:
        return redirect("/login")

    conn = get_db()
    cur = conn.cursor()

    try:
        cur.execute("""
        SELECT t.*
        FROM transactions t
        JOIN accounts a ON t.account_id = a.id
        WHERE a.user_id=?
        ORDER BY t.timestamp DESC
        """, (session["user_id"],))

        data = cur.fetchall()
        transactions = [dict(row) for row in data]

    finally:
        conn.close()

    return render_template("transactions.html", transactions=transactions)


# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# ---------------- MAIN ----------------
if __name__ == "__main__":
    init_db()
    app.run(debug=True)