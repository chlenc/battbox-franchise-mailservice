import requests
r = requests.post("http://127.0.0.1:5000/email", json={'name': 'alexey', 'city': 'moscow', 'phone': '89151272664', 'mail': 'mail'})
print(r.status_code, r.reason, r.content)
