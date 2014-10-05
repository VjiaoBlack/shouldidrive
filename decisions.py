import db
import uber, wunderground, gmaps
import json

MIN_WALKING_TEMP = 25
MAX_TRANSIT_DELTA = 

def decision(origin, destination):
    ans = {'response':{
        'weather_destination':get_weather(destination),
        'uber':get_uber(origin, destination),
        'travel_time':get_transit_time(origin, destination),
    }}
    ans['decision'] = 
    return json.dumps(ans)

def get_decision(data):
    ans = True
    if data['transit_time'] > 
    

def get_uber(start, end):
    try:
        return {
            'price':uber.price(start, end)['prices'],
            'time':uber.time(start)['times']
        }
    except:
        return {
            'error':'No UBER data'
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
    def parse_gmaps(routes):
        if not routes:
            return {'error':'No routes available.'}
        seconds = reduce(lambda acc, leg: acc + leg['duration']['value'],
                         routes[0]['legs'], 0)
    try:
        transit = gmaps.transit_duration(origin, destination, 'transit')['routes']
        walking = gmaps.transit_duration(origin, destination, 'walking')['routes']
        return {
            'public':parse_gmaps(transit),
            'walking':parse_gmaps(walking)
        }
    except:
        return {'error':'Transit data error'}
