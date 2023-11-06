#Find startup companies and their countries
from pymongo import MongoClient
import pandas as pd

def collectionCompanies(name):
    client = MongoClient("localhost:27017")
    db = client["Ironhack"]
    c = db.get_collection(name)
    return c

def findStartUps(collection):
    condition_1 = {"number_of_employees":{"$lt": 100}}
    condition_2 = {"total_money_raised": {"$regex":".+M$"}}
    condition_3 = {"total_money_raised": {"$regex":".+B$"}}
    projection = {"offices.city": 1, "offices.country_code": 1, "_id": 0}
    cities_countries = list(collection.find({"$and": [condition_1, {"$or": [condition_2, condition_3]}]}, projection))
    cities = [j["city"] for i in cities_countries for j in i["offices"]]
    countries = [j["country_code"] for i in cities_countries for j in i["offices"]]
    dict_countrycity = {"city": cities, "country": countries}
    print(pd.DataFrame(pd.DataFrame(dict_countrycity)["country"].value_counts()).head())
    print(pd.DataFrame(pd.DataFrame(dict_countrycity)["city"].value_counts()).head())


c = collectionCompanies("companies")
findStartUps(c)

