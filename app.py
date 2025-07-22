from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Create table if not exists
def init_db():
    conn = sqlite3.connect('bills.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS bills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer TEXT NOT NULL,
            items TEXT NOT NULL,
            total REAL NOT NULL,
            date TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    customer = request.form['customer']
    items = request.form['items']
    total = float(request.form['total'])
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    conn = sqlite3.connect('bills.db')
    c = conn.cursor()
    c.execute('INSERT INTO bills (customer, items, total, date) VALUES (?, ?, ?, ?)',
              (customer, items, total, date))
    conn.commit()
    conn.close()

    return render_template('index.html', success=True)

@app.route('/view')
def view():
    conn = sqlite3.connect('bills.db')
    c = conn.cursor()
    c.execute('SELECT * FROM bills')
    bills = c.fetchall()
    conn.close()
    return render_template('view.html', bills=bills)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)

