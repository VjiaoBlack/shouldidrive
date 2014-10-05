"""
current temp, average temp, current condition
"""

import requests
from tokens import WUNDERGROUND_KEY as key

def conditions(state_code, city):
    url = 'http://api.wunderground.com/api/%s/conditions'%key
    url += '/q/%s/%s.json'%(state_code, city)
    response = requests.get(url)
    data = response.json()
    return data
    
# returns (state, city)
def geocode(location):
    url = 'http://api.wunderground.com/api/%s/geolookup/q/%s,%s.json'%(key, location[0], location[1])
    response = requests.get(url).json()
    loc = response['location']
    return loc['state'], loc['city']
