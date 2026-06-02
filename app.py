from flask import Flask, render_template, request, redirect
import sqlite3


app = Flask(__name__)

# Create Database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS account (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    balance REAL
)
''')

conn.commit()
conn.close()

# Home Page
@app.route('/')
def home():
    return render_template('landing.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')
# Create Account
@app.route('/create', methods=['POST'])
def create():

    name = request.form['name']
    balance = request.form['balance']

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO account(name, balance) VALUES (?, ?)",
        (name, balance)
    )

    conn.commit()
    conn.close()

    return redirect('/dashboard')

# Dashboard
@app.route('/dashboard')
def dashboard():

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM account")
    accounts = cursor.fetchall()

    conn.close()

    return render_template('dashboard.html', accounts=accounts)

# Deposit
@app.route('/deposit/<int:id>', methods=['GET', 'POST'])
def deposit(id):

    if request.method == 'POST':

        amount = float(request.form['amount'])

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE account SET balance = balance + ? WHERE id=?",
            (amount, id)
        )

        conn.commit()
        conn.close()

        return redirect('/dashboard')

    return render_template('deposit.html', id=id)

# Withdraw
@app.route('/withdraw/<int:id>', methods=['GET', 'POST'])
def withdraw(id):

    if request.method == 'POST':

        amount = float(request.form['amount'])

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE account SET balance = balance - ? WHERE id=?",
            (amount, id)
        )

        conn.commit()
        conn.close()

        return redirect('/dashboard')

    return render_template('withdraw.html', id=id)

# Run App
if __name__ == '__main__':
    app.run(debug=True)