import os
import requests
import json
import pandas as pd
import geopandas as gpd
from dotenv import load_dotenv
import math
import src.SelectNeighOffices3 as neighOff
import src.SelectCity1 as city
import src.TotalOffices2 as totalOff
import src.SelectNeighOffices3 as neighOff
import src.FinalOffice4 as final


from pymongo import MongoClient

# Find top 5 cuntries and cities with more startups
c = city.collectionCompanies("companies")
city.findStartUps(c)

# Create the cvs with 100 offices from a rental estate webpage: San Francisco, 87-120 employees
urls = [f"https://www.squarefoot.com/office-space/m/ca/san_francisco/1aee3919-edd5-4fad-b301-76f335aae568?minOccupancy=87&maxOccupancy=120&page={i}&activeSizeFilter=SEATS&groupByBuilding=false" for i in range(1,9)]
totalOff.rentsCsv(urls)

# Create MongoDB with neighborhoods in San Francisco from the webscrapping
url = "https://www.squarefoot.com/office-space/m/ca/san_francisco/1aee3919-edd5-4fad-b301-76f335aae568?minOccupancy=87&maxOccupancy=120&&activeSizeFilter=SEATS&groupByBuilding=false"
js = neighOff.getJson(url)
# getNeighMongo(js, "neighborhoodsSF") -> if mongo collection empty or not existant

# Locate the offices in each neighborhood
neighOff.locateOffices("neighborhoodsSF", "data/officesSF.csv")

# List of offices in the chosen neighborhood:
list_offices = neighOff.officesChosen("neighborhoodsSF", "data/officesSF.csv", "South Of Market")

# Final Office
    # Coordinates from SoMa center:
lat = 37.7772222
lon = -122.4111111
df_schools = final.getSchools("school", lat, lon)
list_offices = neighOff.officesChosen("neighborhoodsSF", "data/officesSF.csv", "South Of Market")

# Check the distance of the offices from education insitutions for kids, choose the closest
list_offices_updated = final.schoolDistance(list_offices, df_schools)

# Check the distance of the uodate list of offices with the design startup
design_coordinates = final.getDesgin("companies")

# Final office coordinates
office_coord = final.getClosestDesign(design_coordinates, list_offices_updated, "data/officesSF.csv")