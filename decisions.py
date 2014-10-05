import db
import uber, wunderground, gmaps
import json

MIN_WALKING_TEMP = 25
MAX_TRANSIT_DELTA = 1020
MAX_PRICE = 100

def decision(origin, destination):
    ans = {'response':{
        'weather_destination':get_weather(destination),
        'uber':get_uber(origin, destination),
        'travel_time':get_transit_time(origin, destination),
    }}
    ans['decision'] = get_decision(ans['response'])
    return json.dumps(ans)

def get_decision(data):
    t_time = data['travel_time']
    if 'error' in data['error']:
        return False
    if 'error' in t_time or 'error' in t_time['public'] or 'error' in t_time['walking']:
        return True
    # t_delta is the number of seconds that non-uber will take more than uber
    if 'temp_f' in data['weather_destination'] and data['weather_destination']['temp_f'] < MIN_WALKING_TEMP:
        return True

    t_delta = min(t_time['public']['seconds'], 
                  t_time['walking']['seconds']) - (
                      t_time['driving']['seconds'] +
                      data['uber']['time'][0]['estimate']
                  )

    ans = t_delta > MAX_TRANSIT_DELTA
    ans = ans and data['uber']['time'][0]['estimate'] < MAX_TRANSIT_DELTA
    return ans

def get_uber(start, end):
    try:
        return {
            'price':sorted(uber.price(start, end)['prices'], 
                          key=lambda x: x['high_estimate']),
            'time':sorted(uber.time(start)['times'], 
                          key=lambda x: x['estimate'])
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
        return {'seconds':seconds}
    try:
        transit = gmaps.maps_duration(origin, destination, 'transit')['routes']
        walking = gmaps.maps_duration(origin, destination, 'walking')['routes']
        driving = gmaps.maps_duration(origin, destination, 'driving')['routes']
        return {
            'public':parse_gmaps(transit),
            'walking':parse_gmaps(walking),
            'driving':parse_gmaps(driving)
        }
    except:
        return {'error':'Data error'}
