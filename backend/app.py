from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

def init_db():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS expenses (id INTEGER PRIMARY KEY, description TEXT, amount REAL)')
    conn.commit()
    conn.close()

@app.route('/add_expense', methods=['POST'])
def add_expense():
    data = request.get_json()
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute('INSERT INTO expenses (description, amount) VALUES (?, ?)', (data['description'], data['amount']))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Expense added successfully'})

@app.route('/get_expenses', methods=['GET'])
def get_expenses():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute('SELECT * FROM expenses')
    expenses = [{'id': row[0], 'description': row[1], 'amount': row[2]} for row in c.fetchall()]
    conn.close()
    return jsonify({'expenses': expenses})

if __name__ == '__main__':
    init_db()
    app.run(debug=True)