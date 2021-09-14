import requests

r = requests.post('localhost:8000/items', data={'name': 'anh'})
print(r.content)
