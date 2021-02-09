from geopy.geocoders import Nominatim
import requests
import pandas as pd
import googlemaps
import config






def toCoordinates(ADDRESS):
    KEY = config.googlemapsapikey
    #gets coordinates using google maps API
    #google bills me if more than 40,000 requests/month
    gmaps = googlemaps.Client(key = KEY)
    result = gmaps.geocode(ADDRESS)[0].get("geometry").get("location")
    lat = str(result.get("lat"))
    long = str(result.get("lng"))
    
    coordinates = [lat, long]
    return coordinates


def toZIP(coordinates):
    lat = str(coordinates[0])
    long = str(coordinates[1])
    
    newcoordinates = lat + ", " + long
    
    
    
    geolocator = Nominatim(user_agent="Will Armstrong")
    
    location = geolocator.reverse(newcoordinates)
    return location.raw["address"]["postcode"]


def toCensusTract(coordinates):
    FCCAPI1 = "https://geo.fcc.gov/api/census/block/find?latitude="
    FCCAPI2 = "&longitude="
    FCCAPI3 = "&showall=false&format=json"
    
    lat = str(coordinates[0])
    long = str(coordinates[1])
    
    website = FCCAPI1 + lat + FCCAPI2 + long + FCCAPI3
    
    response = requests.get(website)
    
    apiquerry = response.json() 
    df = pd.DataFrame.from_dict(apiquerry)
    geocode = df.iloc[0,0]
    tract = geocode[5:11]
    
    return tract
    
    
def censusCountyCode(coordinates):
    FCCAPI1 = "https://geo.fcc.gov/api/census/block/find?latitude="
    FCCAPI2 = "&longitude="
    FCCAPI3 = "&showall=false&format=json"
    
    lat = str(coordinates[0])
    long = str(coordinates[1])
    
    website = FCCAPI1 + lat + FCCAPI2 + long + FCCAPI3
    
    response = requests.get(website)
    
    apiquerry = response.json() 
    df = pd.DataFrame.from_dict(apiquerry)
    geocode = df.iloc[0,1]
    county = geocode[2:5]

    
    return county


def checkAddressTX(address):
    KEY = config.googlemapsapikey
    #gets coordinates using google maps API
    #google bills me if more than 40,000 requests/month
    gmaps = googlemaps.Client(key = KEY)
    
    result = gmaps.geocode(address)[0].get("geometry").get("location")
    
    if(isinstance(result, dict) == True):
        return True
    else:
        return False



