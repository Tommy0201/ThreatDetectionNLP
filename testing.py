import requests


url = "http://54.188.20.167:5000/detect"
local_url = "http://127.0.0.1:4900/detect"
data = "what is going on"

data2 = {"transcription": "234 call ambulance"}

response = requests.post(url,json=data2)


print(response.json())
