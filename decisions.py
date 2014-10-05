import db
import uber, wunderground, gmaps
import json


def decision(origin, destination):
    ans = {'response':{
        'weather_destination':get_weather(destination),
        'uber':get_uber(origin, destination),
        'transit_time':get_transit_time(origin, destination),
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
        try:
            state, city = wunderground.geocode(location)
            weather = wunderground.conditions(state, city.replace(' ', '_'))
            weather = weather['current_observation']
            weather = {
                'precip_today_in':weather['precip_today_in'],
                'temp_f':weather['temp_f'],
                'temp_c':weather['temp_c'],
                'weather':weather['weather']
            }
            db.store_weather(location, weather)
            weather['fresh'] = True
        except:
            #bad error handling
            weather = {'error':'there was error'}
    else:
        weather['fresh'] = False

    return weather

def get_transit_time(origin, destination):
    routes = gmaps.transit_duration(origin, destination)['routes']
    if not routes:
        return {'error':'No routes available.'}
    seconds = reduce(lambda acc, leg: acc + leg['duration']['value'],
                     routes[0]['legs'], 0)
    return seconds
