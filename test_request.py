import requests

page_url = 'http://127.0.0.1:8000/add-user/'

params = {
    "username": "Dima",
    "age": "23",
    "password": "12345"

}

resource = requests.post(page_url, params=params)
print(resource.status_code)