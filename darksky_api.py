import requests
import json

# Ann_Arbor=(42.2808, -83.7430)



#____GEO_CACHING____

def coordnates(string):

    base_url = 'https://maps.googleapis.com/maps/api/geocode/json'
    params={
            'address': string
            }

    request=requests.get(base_url, params)
    data= request.json()
    lat_long= data['results'][0]['geometry']['bounds']['northeast']
    final=(lat_long['lat'],lat_long['lng'])

    return final


print coordnates("Ann Arbor")

#___WEATHER____

def weather(tupel):
    base_url='https://api.darksky.net/forecast/4bd33476a630ff4fdf43d34658231690/'
    url=base_url + str(tupel[0]) + ',' + str(tupel[1]) + '?' + 'exclude=[flags, minutely]'
    darksky_request=requests.get(url)
    data=json.loads(darksky_request)
    return json.dumps(data, indent=4)



def get_weather(place):
    grid=coordnates(place)
    return weather(grid)
