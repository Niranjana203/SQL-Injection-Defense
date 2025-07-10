from flask import Flask, render_template, request
import sqlite3
import os

app = Flask(__name__)

# Initialize the database and insert a default user
def init_db():
    if not os.path.exists('users.db'):
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password TEXT NOT NULL
            )
        ''')
        # Insert a default user
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", ('admin', 'admin123'))
        conn.commit()
        conn.close()

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/vulnerable', methods=['POST'])
def vulnerable_login():
    username = request.form['username']
    password = request.form['password']

    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    # ❌ Vulnerable to SQL Injection
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    try:
        c.execute(query)
        result = c.fetchone()
    except Exception as e:
        print("SQL Error:", e)
        result = None
    conn.close()

    if result:
        return render_template('result.html', message="✅ Login successful (vulnerable route)")
    else:
        return render_template('result.html', message="❌ Login failed (vulnerable route)")

@app.route('/secure', methods=['POST'])
def secure_login():
    username = request.form['username']
    password = request.form['password']

    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    # ✅ Safe with parameterized query
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    result = c.fetchone()
    conn.close()

    if result:
        return render_template('result.html', message="✅ Login successful (secure route)")
    else:
        return render_template('result.html', message="❌ Login failed (secure route)")

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
