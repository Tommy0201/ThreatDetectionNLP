import requests


url = "http://127.0.0.1:5000/chat-history"
# data ="I am just joking"
response = requests.post(url)


print(response.json())


