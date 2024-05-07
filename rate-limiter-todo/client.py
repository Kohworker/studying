import requests

SERVER = "localhost"
PORT = 3333

url = "http://" + SERVER + ":" + str(PORT)

query_parameters = ""

r = requests.get(url)
print(r.text)

r = requests.post(url)
print(r.text)