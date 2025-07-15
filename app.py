from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)
FLAG = "FLAG{sql_injection_lvl1}"

def init_db():
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
  
    c.execute("DELETE FROM users")
    c.execute("INSERT INTO users (username, password) VALUES ('admin', 'admin123')")
    c.execute("INSERT INTO users (username, password) VALUES ('test', 'test123')")
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def login():
    message = ''
    flag = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('db.sqlite3')
        c = conn.cursor()
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        print("[DEBUG] Executing:", query)
        try:
            c.execute(query)
            user = c.fetchone()
            if user:
                message = f"Welcome {user[1]}!"
                if user[1] == 'admin' and password != 'admin123':
                    flag = FLAG  
            else:
                message = "Login failed!"
        except Exception as e:
            message = f"Error: {e}"
        conn.close()
    return render_template('login.html', message=message, flag=flag)
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
