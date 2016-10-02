import urllib, json
from os.path import exists
import json 
from flask import Flask

app = Flask(__name__)


@app.route('/')
def process():
    url = "https://gbfs.citibikenyc.com/gbfs/en/station_information.json"
    response = urllib.urlopen(url)
    print response
    data = json.loads(response.read())
     
    # data = json.load(open(in_file))
    result  = []
    for station in data['data']['stations']: 
        print station
        if 'region_id' in station:
            region_id = station['region_id']
        else:
            region_id = None 

        result.append({
            'geometry':{
                'type': 'Point',
                "coordinates" : [station['lon'], station['lat']]
            },
            'type' : "Feature",
            'properties' : {
                'station_id' : station['station_id'],
                'name' : station['name'],
                'region_id' : region_id,
                'capacity' : station['capacity'],
                'eightd_has_key_dispenser' : station['eightd_has_key_dispenser'],
                'KEY' : 'KEY' in station['rental_methods'],
                'CREDITCARD' : 'CREDITCARD' in station['rental_methods']
            }
        })

    geojson = {
        "type": "FeatureCollection",
        "features": result
    }

    # output = open('city_bike.geojson', 'w')
    return json.dumps(geojson)
     
