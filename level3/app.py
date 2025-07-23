from flask import Flask, request, render_template
import sqlite3
import time

app = Flask(__name__)

def query_user(username):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # این کوئری مستعد Blind SQLi هست چون هیچ خروجی واضحی برنمی‌گردونه
    try:
        sql = f"SELECT * FROM users WHERE username = '{username}'"
        cursor.execute(sql)
        result = cursor.fetchone()
        if result:
            return True
        return False
    except:
        return False
    finally:
        conn.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    message = ""
    if request.method == 'POST':
        username = request.form.get('username')

        if query_user(username):
            message = "User exists!"
        else:
            message = "User does not exist."

    return render_template('index.html', message=message)

if __name__ == '__main__':
    app.run(debug=True)
