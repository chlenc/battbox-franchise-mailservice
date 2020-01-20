import requests

url = "http://127.0.0.1:5000/email"
headers = {'SECUREKEY': 'mytopthebestsecurekey'}
json = {'name': 'Алексей', 'city': 'Москва', 'phone': '+7 915 127 26 64', 'mail': 'alexnagorny.an@gmail.com'}
r = requests.post(url, json=json, headers=headers)
print(r.status_code, r.reason, r.content)
