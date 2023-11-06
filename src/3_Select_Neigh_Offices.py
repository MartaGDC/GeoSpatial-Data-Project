import pandas as pd
import requests
from bs4 import BeautifulSoup
import json
from pymongo import MongoClient

def getJson(url):
    res = requests.get(url)
    html = res.content
    soup = BeautifulSoup(html, 'html.parser')
    body = soup.find_all("script", {"id": "__NEXT_DATA__"})
    info = body[0].getText("application/json")
    js = json.loads(info)
    return js

def getNeighMongo(js, name_collection):
    '''Only used if the collection doesn't exist'''
    neighborhoods = js["props"]["pageProps"]["queryManager"]["values"]["submarkets"][0]["neighborhoods"]
    name = [i["name"] for i in neighborhoods]
    geojson = [i["geojson"] for i in neighborhoods]
    dict_neigh = {
        "name": name,
        "geojson": geojson
    }
    dict_neigh_rows = []
    for index, row in pd.DataFrame(dict_neigh).iterrows():
        dict_neigh_rows.append({"name":row["name"], "geojson":row["geojson"]})
    
    client = MongoClient("localhost:27017")
    db = client.get_database("Ironhack")
    neighborhoodsSF = db.get_collection(name_collection)
    neighborhoodsSF.insert_many(dict_neigh_rows) # -> if not already inserted

def officesChosen(mongo, csv, neigh):
    client = MongoClient("localhost:27017")
    db = client.get_database("Ironhack")
    neighborhoodsSF = db.get_collection(mongo)
    locations = [row["positions"] for index, row in csv.iterrows()]
    positions = [{"type": "Point", "coordinates": i} for i in locations]
    list_offices = []
    for i in positions:
        try:
            if neighborhoodsSF.find_one(
                {"geojson":
                {"$geoIntersects":
                {"$geometry": i}
                }
                })["name"] == neigh:
                list_offices.append(i)
        except:
            pass
    return(list_offices)

url = "https://www.squarefoot.com/office-space/m/ca/san_francisco/1aee3919-edd5-4fad-b301-76f335aae568?minOccupancy=87&maxOccupancy=120&&activeSizeFilter=SEATS&groupByBuilding=false"
js = getJson(url)
# getNeighMongo(js, "neighborhoodsSF") -> if mongo collection empty or not existant
# There was another function to decide which neighborhood to pick, cheching the density of offices and the "party" criteria
list_offices = officesChosen("neighborhoodsSF", "data/officesSF.csv", "South Of Market")