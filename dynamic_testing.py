import json
import requests as req

d = open('courier_0.json', mode='r').read()
url = 'http://localhost:8000/couriers'
response = req.post(url, data=d, headers={'Content-type': 'application/json'})
print(response.status_code, response.text)
