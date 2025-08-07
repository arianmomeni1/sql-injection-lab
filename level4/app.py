from flask import Flask, request
import sqlite3, base64

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect("users.db")
    conn.row_factory = sqlite3.Row
    return conn

# ساخت دیتابیس اگه وجود نداشت
def setup_db():
    conn = get_db()
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, password TEXT)")
    c.execute("DELETE FROM users")
    c.execute("INSERT INTO users (name, password) VALUES ('admin', 'supersecret')")
    c.execute("INSERT INTO users (name, password) VALUES ('guest', 'guest123')")
    conn.commit()
    conn.close()

setup_db()

@app.route('/')
def index():
    return '''
    <html>
    <head>
        <title>🔐 سطح 4 - SQL Injection Challenge</title>
        <style>
            body {
                font-family: monospace;
                background-color: #0d1117;
                color: #c9d1d9;
                padding: 40px;
            }
            .container {
                max-width: 700px;
                margin: auto;
                border: 1px solid #30363d;
                padding: 30px;
                border-radius: 10px;
                background-color: #161b22;
            }
            code {
                background: #21262d;
                padding: 2px 6px;
                border-radius: 5px;
                color: #58a6ff;
            }
            h1 {
                color: #58a6ff;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🔐 SQL Injection Lab - Level 4</h1>
            <p>در این مرحله فقط یک پارامتر ورودی داریم به نام <code>x</code> که مقدار آن <b>base64 encode شده</b> است.</p>

            <p>مثال ساده:</p>
            <code>/lvl4?x=YWRtaW4=</code> <small>(که معادل "admin" است)</small>

            <hr>

            <h3>🎯 هدف:</h3>
            <p>با استفاده از تزریق SQL، کاری کنید که پاسخ از <code>❌</code> به <code>✅</code> تغییر کند. هیچ خطای مشخصی نمایش داده نمی‌شود، پس باید نتیجه را از روی رفتار بفهمید.</p>

            <p>🔒 ارورها مخفی شده‌اند و فقط با تحلیل دقیق می‌توانید تزریق را انجام دهید.</p>

            <hr>
            <p><b>نکته:</b> این مرحله برای تمرین Blind SQLi و بای‌پس فیلترها طراحی شده است.</p>
        </div>
    </body>
    </html>
    '''


@app.route('/lvl4')
def lvl10():
    encoded = request.args.get('x', '')

    try:
        user_input = base64.b64decode(encoded).decode('utf-8')
    except:
        return "❌ Invalid input"

    # تزریق آسیب‌پذیر اما ارور مبهم
    query = f"SELECT * FROM users WHERE name = '{user_input}'"
    try:
        conn = get_db()
        result = conn.execute(query).fetchall()
        conn.close()
    except:
        return "✅"

    if result:
        return "✅"
    return "❌"

if __name__ == '__main__':
    app.run(debug=False, port=5000)
