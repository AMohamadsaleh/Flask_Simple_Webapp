import requests
import json


Base_url = "http://127.0.0.1:5000"

def get_request():
    end_point = "/items"
    url = Base_url+end_point
    response = requests.get(url)
    print(response.json())


get_request()

