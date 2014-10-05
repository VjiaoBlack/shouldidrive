import requests
from tokens import GMAPS_KEY as key
import time

def maps_duration(origin, destination, mode):
    url = 'https://maps.googleapis.com/maps/api/directions/json'
    params = {
        'key':key,
        'origin':'%s,%s'%origin,
        'destination':'%s,%s'%destination,
        'mode':mode,
        'departure_time':int(time.time())
    }
    return requests.get(url, params=params).json()
