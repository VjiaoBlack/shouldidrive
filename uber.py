from tokens import UBER_SERVER_TOKEN as server_token
import requests

"""
Location tuples are expected in the form (latitude, longitude)
"""


def price(origin, destination):
    url = 'https://api.uber.com/v1/estimates/price'
    params = {
        'server_token':server_token,
        'start_latitude':origin[0],
        'start_longitude':origin[1], 
        'end_latitude':destination[0],
        'end_longitude':destination[1] 
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data


