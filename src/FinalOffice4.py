import os
import requests
import json
import pandas as pd
import geopandas as gpd
from dotenv import load_dotenv
import math
from pymongo import MongoClient


# https://geocode.xyz/ -> This web wasn't working correctly

def request_4sq(venue, lat, lon, radius = 3700, sort_by = "DISTANCE", limit = 20):
    load_dotenv()
    token = os.getenv("token")
    url = f"https://api.foursquare.com/v3/places/search?query={venue}&ll={lat}%2C{lon}&radius={radius}&sort={sort_by}&limit={limit}"
    headers = {
        "accept": "application/json",
        "Authorization": token
    }
    try:
        return requests.get(url, headers = headers).json()
    except:
        print("Request not found")

def distances(coordinates_1, coordinates_2):
    R = 6371000 # radius of Earth in meters
    lon_1, lat_1 = coordinates_1
    lon_2, lat_2 = coordinates_2
    phi_1 = math.radians(lat_1)
    phi_2 = math.radians(lat_2)
    delta_phi = math.radians(lat_2 - lat_1)
    delta_lambda = math.radians(lon_2 - lon_1)
    a = math.sin(delta_phi / 2.0) ** 2 + math.cos(phi_1) * math.cos(phi_2) * math.sin(delta_lambda / 2.0) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    km = round(R * c / 1000.0, 3)
    return km

def getSchools(venue, lat, lon, radius = 3700, sort_by = "DISTANCE", limit = 20):
    school_request = request_4sq(venue, lat, lon, radius, sort_by, limit)
    school_lat = [i["geocodes"]["main"]["latitude"] for i in school_request["results"]]
    school_lon = [i["geocodes"]["main"]["longitude"] for i in school_request["results"]]
    school_name = [i["name"] for i in school_request["results"]]
    school_open = [i["closed_bucket"] for i in school_request["results"]]
    df_schools = pd.DataFrame({"school_name":school_name, "school_categ": school_categ, "school_lat": school_lat, "school_lon": school_lon, "school_open": school_open})
    indexes = df_schools["school_categ"][df_schools["school_categ"].isin(["College and University", "Technology Business", "Language School", 
                                                "College Academic Building", "Music School", "College and University", "Law School",
                                                "College Academic Building", "Public Art"])].index
    df_schools.drop(indexes, inplace=True)
    indexes = df_schools["school_open"][df_schools["school_open"].isin(["Unsure", "LikelyClosed"])].index
    df_schools.drop(indexes, inplace=True)
    df_schools
    indexes = df_schools["school_name"][df_schools["school_name"].isin(["Bay Area Motorcycle School", "Tenderloin After-School Program Center", "SFUSD-Van Ness"])].index
    df_schools.drop(indexes, inplace=True)
    df_schools.drop(columns = "school_open", axis = 1, inplace=True)
    return df_schools

def schoolDistance(list, df):
    school_coordinates = [[row["school_lat"], row["school_lon"]] for index, row in df.iterrows()]
    school_distances = [{"office":j, "school":i, "distance": distances(i, [j["coordinates"][1],j["coordinates"][0]])} for j in list_offices for i in school_coordinates]
    df_school_distance = pd.DataFrame(school_distances).sort_values(by = "distance", ascending = True)
    df_school_distance[df_school_distance["distance"] <= 0.5]["office"].value_counts()
    x = pd.DataFrame(df_school_distance[df_school_distance["distance"] <= 0.5]["office"].value_counts())
    x.reset_index(inplace=True)
    list_offices_updated = [row["office"] for index, row in x.iterrows()]
    return list_offices_updated

def getDesgin(mongo):
    client = MongoClient("localhost:27017")
    db = client.get_database("Ironhack")
    c = db.get_collection(mongo)
    condition_1 = {"number_of_employees":{"$lt": 100}}
    condition_2 = {"tag_list": {"$regex": "[Dd]esign"}}
    condition_3 = {"offices.city": "San Francisco"}
    condition_4 = {"total_money_raised": {"$regex":".+M$"}}
    condition_5 = {"total_money_raised": {"$regex":".+B$"}}
    projection = {"offices.latitude": 1, "offices.longitude": 1, "_id": 0}
    position = list(c.find({"$and": [condition_1, condition_2, condition_3, {"$or": [condition_4, condition_5]}]}, projection))
    # There was only one company
    position = [position[0]["offices"][0]["longitude"], position[0]["offices"][0]["latitude"]]
    return position


def getClosestDesign(design_coordinates, list_offices_updated, csv_name): 
    designSF_coordinates = [{'offices': [{'latitude': design_coordinates[1], 'longitude': design_coordinates[0]}]}]
    design_distance = [{"office":i, "distance": distances(designSF_coordinates, [i["coordinates"][1],i["coordinates"][0]])} for i in list_offices_updated]
    df_design_distance = pd.DataFrame(design_distance).sort_values(by = "distance", ascending = True)
    coordinates = [row["office"] for index, row in df_design_distance.iterrows()][0]["coordinates"]
    csv = pd.read_csv(csv_name, encoding = "unicode_escape")
    print(csv[csv["positions"]== str(coordinates)])
    return coordinates
