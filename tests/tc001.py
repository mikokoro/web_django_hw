import requests, pprint

payload = {
    'username': 'mikokoro',
    'password': '88888888'
}
response = requests.post('http://127.0.0.1/api/mgr/signin',
                        data=payload)
pprint.pprint(response.json())

