"""Generate credentials.json with hashed passwords"""
import hashlib
import secrets
import json

def hash_pw(password: str) -> str:
    salt = secrets.token_hex(16)
    h = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100_000).hex()
    string_repr = "pbkdf2${iterations}${salt}${hash}".replace("{iterations}", "100000").replace("{salt}", salt).replace("{hash}", h)
    return string_repr

users = {
    'admin': {'hash': hash_pw('bod@2026'), 'role': 'BOD'},
}

centers = ['Binh Phuoc', 'Hung Vuong', 'Le Duan', 'Nguyen Trai', 'Pham Van Thuan', 'Phuoc Tan', 'Tran Phu', 'Tran Van Xa', 'Trang Bom', 'Vo Thi Sau']
for center in centers:
    username = center.lower().replace(' ', '_')
    pw = center.lower().replace(' ', '') + '@2026'
    users[username] = {'hash': hash_pw(pw), 'role': center}

with open('credentials.json', 'w', encoding='utf-8') as f:
    json.dump(users, f, indent=2, ensure_ascii=False)

print("credentials.json created successfully!")
print(f"Total users: {len(users)}")

# Verify
entry = users['admin']
parts = users['admin']['hash'].split('$')
print(f"Admin format: prefix={parts[0]}, iter={parts[1]}, salt_len={len(parts[2])}, hash_len={len(parts[3])}")
