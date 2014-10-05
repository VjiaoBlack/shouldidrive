import requests
from tokens import GMAPS_KEY as key
import time

def transit_duration(origin, destination):
    url = 'https://maps.googleapis.com/maps/api/directions/json'
    params = {
        'key':key,
        'origin':'%s,%s'%origin,
        'destination':'%s,%s'%destination,
        'mode':'transit',
        'departure_time':int(time.time())
    }
    return requests.get(url, params=params).json()
