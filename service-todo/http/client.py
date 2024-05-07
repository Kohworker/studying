import requests
import json

url = 'http://localhost:4444'

r = requests.get(url)
print(r.text)

# r = requests.post(url, json={'name': 'John Doe'})
# print(r.text)
