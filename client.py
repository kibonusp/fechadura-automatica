import requests
import json

url = 'http://127.0.0.1:5000/'
file = {'image': open('static/faces/gato.jpg', 'rb')}
response = requests.post(url, files=file)
data = json.loads(response.text)
print(data['ans'])