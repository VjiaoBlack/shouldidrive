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
    
