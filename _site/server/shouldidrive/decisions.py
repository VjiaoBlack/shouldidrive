import db
import uber, wunderground
import json


def decision(origin, destination):
    ans = {'response':{
        'weather_destination':get_weather(destination),
        'uber':get_uber(origin, destination), 
        'drive':True
    }}
    return json.dumps(ans)

def get_uber(start, end):
    return {
        'price':uber.price(start, end)['prices'],
        'time':uber.time(start)['times']
    }

def get_weather(location):
    weather = db.find_weather(location)
    if not weather:
        state, city = wunderground.geocode(location)
        weather = wunderground.conditions(state, city.replace(' ', '_'))
        weather = weather['current_observation']
        weather = {
            'precip_today_in':weather['precip_today_in'],
            'temp_f':weather['temp_f'],
            'temp_c':weather['temp_c'],
            'weather':weather['weather'],
        }
        db.store_weather(location, weather)
        weather['fresh'] = True
    else:
        weather['fresh'] = False

    return weather
