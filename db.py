from pymongo import MongoClient, GEO2D
from datetime import datetime

db = MongoClient().shoulddrive
db.places.create_index([("loc", GEO2D)])

# number of seconds to keep records
MAX_TIME = 4000
MAX_DISTANCE = 3000

# None on not found
def find_weather(location):
    now = datetime.utcnow()
    weather = db.weather.find_one({"loc":{
        "$nearSphere":{
            "$geometry":{
                "type":"Point",
                "coordinates":[location[0], location[1]]
            },
            "$maxDistance":MAX_DISTANCE
        }
    }})
    if weather and weather['utcdate']:
        delta = now - weather['utcdate']
        if delta.total_seconds() > MAX_TIME:
            # time to remove
            db.weather.remove({'_id':weather['_id']})
            weather = None
    return weather['data'] if weather else None

def store_weather(location, data):
    obj = { "loc": {
                "type":"Point",
                "coordinates":[location[0], location[1]]
            },
            "data": data,
            "utcdate":datetime.utcnow()
        }
    db.weather.insert(obj)
