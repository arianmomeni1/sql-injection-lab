from flask import Flask, request, render_template
import sqlite3
import os

app = Flask(__name__)

DB_PATH = 'db.sqlite3'


def init_db():
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price INTEGER NOT NULL,
                category TEXT
            )
        ''')

        cursor.executemany('INSERT INTO products (name, price, category) VALUES (?, ?, ?)', [
            ("Mouse", 100, "Hardware"),
            ("Keyboard", 200, "Hardware"),
            ("T-shirt", 150, "Clothes"),
            ("Shoes", 300, "Clothes")
        ])
        conn.commit()
        conn.close()

@app.route('/')
def index():
    return '''
    <h2>Shop Injection Lab - Level 2</h2>
    <form method="GET" action="/shop">
        Category: <input name="cat">
        <input type="submit" value="Search">
    </form>
    '''

@app.route('/shop')
def shop():
    category = request.args.get('cat', '')
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    query = f"SELECT name, price FROM products WHERE category = '{category}'"
    try:
        cursor.execute(query)
        products = cursor.fetchall()
    except Exception as e:
        products = []
        print("SQL Error:", e)
    conn.close()
    return render_template('index.html', products=products)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
