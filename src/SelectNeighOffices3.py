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

def getNeighMongo(js, mongo):
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
    neighborhoodsSF = db.get_collection(mongo)
    neighborhoodsSF.insert_many(dict_neigh_rows) # -> if not already inserted

def locateOffices(mongo, csv_name):
    csv = pd.read_csv(csv_name, encoding = "unicode_escape")
    locations = [row["positions"] for index, row in csv.iterrows()]
    positions = [{"type": "Point", "coordinates": i} for i in locations]
    client = MongoClient("localhost:27017")
    db = client.get_database("Ironhack")
    neighborhoodsSF = db.get_collection(mongo)
    list_neigh = []
    for i in positions:
        try:
            list_neigh.append(
                {"neighborhoods": neighborhoodsSF.find_one(
                    {"geojson":
                    {"$geoIntersects":
                    {"$geometry": i}
                    }
                    })["name"]
                })
        except: # Some neightborhoods of San Francisco might not be included in the selection of renting venues
            list_neigh.append({"neighborhoods":None})
    print(pd.DataFrame(list_neigh).value_counts().head())


def officesChosen(mongo, csv_name, neigh):
    csv = pd.read_csv(csv_name, encoding = "unicode_escape")
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
