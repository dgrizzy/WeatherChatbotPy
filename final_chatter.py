import aiml
import os
import requests
import json

#kernel attached
kernel = aiml.Kernel()

#AIML Files Loaded into Kearnel
aiml_files=os.listdir('aiml_data')
for file in aiml_files:
    kernel.learn(os.path.join('aiml_data/', file))


#define new response in kearnel
def exampleResponse(first, second):
    return 'first arg is {}, second arg is {}'.format(first, second)

kernel.addPattern("example {first} and {second}", exampleResponse)

try:
    cache_file = open('CACHE_FILE.txt', 'r')
    contents = cache_file.read()
    cache_file.close()
    cache_dict = json.loads(contents)
except:
    cache_dict = {}

#enable the weather repsonse
def coordnates(string):
    base_url = 'https://maps.googleapis.com/maps/api/geocode/json'
    params = {
            'address': string
            }
    request = requests.get(base_url, params)
    data = request.json()
    lat_long = data['results'][0]['geometry']['bounds']['northeast']
    final = (lat_long['lat'],lat_long['lng'])
    return final

def weather(tupel):
    base_url = 'https://api.darksky.net/forecast/4bd33476a630ff4fdf43d34658231690/'
    url = base_url + str(tupel[0]) + ',' + str(tupel[1]) + '?' + 'exclude=[flags, minutely]'
    darksky_request = requests.get(url)
    data = darksky_request.json()
    return data


#"What's the weather like in {city}?"
def get_weather(city):
    if city in cache_dict.keys():
        data = cache_dict[city]
        tempature = data ['currently']['temperature']
        skys = data['currently']['summary']
    else:
        try:
            coord = coordnates(city)
        except:
            return 'Is {} a city?'.format(city)
        try:
            data = weather(coord)
        except:
            return "Sorry, I don't know"
        cache_dict[city] = data
        tempature = data['currently']['temperature']
        skys= data['currently']['summary']
    return '{} is {} and {}'.format(city, tempature, skys)
kernel.addPattern("What's the weather like in {city}?", get_weather)


#Is it going to rain in Ypsilanti today?
def gonna_rain(city):


    if city in cache_dict.keys():
        data = cache_dict[city]
        precip_chance = data['daily']['data'][0]['precipProbability']


    else:
        try:
            coord = coordnates(city)
        except:
            return 'Is {} a city?'.format(city)
        try:
            data = weather(coord)
        except:
            return "Sorry, I don't know"

        cache_dict[city] = data
        precip_chance = data['daily']['data'][0]['precipProbability']

    if float(precip_chance) > .5:
        rain= "Yes"
        response = "will"
    else:
        rain='No'
        response='will not'

    return '{}, it {} rain in {} today.'.format(rain, response, city)

kernel.addPattern("Is it going to rain in {city} today?", gonna_rain)


#"How hot will it get in Ann Arbor this week?"
def max_heet(city):
    if city in cache_dict.keys():
        data = cache_dict[city]
        tempature = [float(x['temperatureMax']) for x in data['daily']['data']]
        max_temp = float(tempature[0])
        for i in tempature:
            if i > max_temp:
                max_temp = i
    else:
        try:
            coord = coordnates(city)
        except:
            return 'is {} a city?'.format(city)
        try:
            data = weather(coord)
        except:
            return "Sorry, I don't know"
        cache_dict[city] = data
        tempature = [float(x['temperatureMax']) for x in data['daily']['data']]
        max_temp = float(tempature[0])
        for i in tempature:
            if i > max_temp:
                max_temp = i
    return 'In {} it will reach {} degrees.'.format(city, max_temp)
kernel.addPattern("How hot will it get in {city} this week?", max_heet)

#"How cold will it get in Ann Arbor this week?"
def how_chilly(city):

    if city in cache_dict.keys():
        data = cache_dict[city]
        tempature = [float(x['temperatureMin']) for x in data['daily']['data']]
        min_temp = float(tempature[0])
        for i in tempature:
            if i < min_temp:
                min_temp = i
    else:
        try:
            coord = coordnates(city)
        except:
            return 'is {} a city?'.format(city)
        try:
            data = weather(coord)
        except:
            return "Sorry, I don't know"
        cache_dict[city] = data
        tempature = [float(x['temperatureMin']) for x in data['daily']['data']]
        min_temp = float(tempature[0])
        for i in tempature:
            if i < min_temp:
                min_temp = i
    return 'In {} it will be as cold as {} degrees.'.format(city, min_temp)
kernel.addPattern("How cold will it get in {city} this week?", how_chilly)

def week_rain(city):
    if city in cache_dict.keys():
        data = cache_dict[city]
        chance_precip = [float(x['precipProbability']) for x in data['daily']['data']]
        chance_no_precip = [(1-x) for x in chance_precip]
        chance_week_precip=1
        for x in chance_no_precip:
            chance_week_precip= chance_week_precip * x
        prob= 1- chance_week_precip
        if prob < .1:
            return "It almost definitely will not rain in {} this week.".format(city)
        elif prob < .5:
            return "It probably will not rain in {}.".format(city)
        elif prob < .9:
            return 'It probably will rain in {}.'.format(city)
        else:
            return 'It will almost definitely rain in {}.'.format(city)

    else:
        try:
            coord = coordnates(city)
        except:
            return 'is {} a city?'.format(city)
        try:
            data = weather(coord)
        except:
            return "Sorry, I don't know"
        cache_dict[city] = data
        chance_precip = [float(x['precipProbability']) for x in data['daily']['data']]
        chance_no_precip = [(1-x) for x in chance_precip]
        chance_week_precip=1
        for x in chance_no_precip:
            chance_week_precip= chance_week_precip * x
        prob= 1- chance_week_precip
        if prob < .1:
            return "It almost definitely will not rain in {} this week.".format(city)
        elif prob < .5:
            return "It probably will not rain in {}.".format(city)
        elif prob < .9:
            return 'It probably will rain in {}.'.format(city)
        else:
            return 'It will almost definitely rain in {} this week.'.format(city)

kernel.addPattern("Is it going to rain in {city} this week?", week_rain)

#How hot will it get in Detroit today?
def hot_today(city):
    if city in cache_dict.keys():
        data = cache_dict[city]
        tempature = data ["daily"] ["data"] [0] ["temperatureMax"]
    else:
        try:
            coord = coordnates(city)
        except:
            return 'Is {} a city?'.format(city)
        try:
            data = weather(coord)
        except:
            return "Sorry, I don't know"
        cache_dict[city] = data
        tempature = data ["daily"] ["data"] [0] ["temperatureMax"]
    return '{} will be as warm as {} degrees.'.format(city, tempature)

kernel.addPattern("How hot will it get in {city} today?", hot_today)

def cold_today(city):
    if city in cache_dict.keys():
        data = cache_dict[city]
        tempature = data ["daily"] ["data"] [0] ["temperatureMin"]
    else:
        try:
            coord = coordnates(city)
        except:
            return 'Is {} a city?'.format(city)
        try:
            data = weather(coord)
        except:
            return "Sorry, I don't know"
        cache_dict[city] = data
        tempature = data ["daily"] ["data"] [0] ["temperatureMin"]
    return '{} will be as cold as {} degrees.'.format(city, tempature)

kernel.addPattern("How cold will it get in {city} today?", cold_today)

#Loop to trigger the AI response
q='money'
print 'Hello!'
while q != 'exit':
    q=raw_input('>')
    print(kernel.respond(q))


cache_file=open('CACHE_FILE.txt', 'w')
cache_file.write(json.dumps(cache_dict, indent=4))
cache_file.close()
