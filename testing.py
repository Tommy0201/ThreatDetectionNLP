import requests


# url = "http://54.212.239.210:5000/detect"
local_url = "http://127.0.0.1:4900/detect"  # Make sure this matches the running server
data2 = {"transcription": "There is a bomb"}


response = requests.post(local_url,json=data2)


print(response.json())
