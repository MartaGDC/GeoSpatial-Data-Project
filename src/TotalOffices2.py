import pandas as pd
import requests
from bs4 import BeautifulSoup
import json


def getJson(url):
    res = requests.get(url)
    html = res.content
    soup = BeautifulSoup(html, 'html.parser')
    body = soup.find_all("script", {"id": "__NEXT_DATA__"})
    info = body[0].getText("application/json")
    js = json.loads(info)
    return js

def getEmployees(js):
    return [i["estimatedMaxOccupancy"] for i in js["props"]["pageProps"]["queryManager"]["values"]["listings"]]
def getLat(js):
    return [i["building"]["lat"] for i in js["props"]["pageProps"]["queryManager"]["values"]["listings"]]
def getLon(js):
    return [i["building"]["lng"] for i in js["props"]["pageProps"]["queryManager"]["values"]["listings"]]
def getAddress(js):
    return [i["building"]["address"] for i in js["props"]["pageProps"]["queryManager"]["values"]["listings"]]

def getDict(urls):
    employees = []
    lat = []
    lon = []
    address = []
    for i in urls:
        jsons = getJson(i)
        employees.extend(getEmployees(jsons))
        lat.extend(getLat(jsons))
        lon.extend(getLon(jsons))
        address.extend(getAddress(jsons))
    dict_ = {
        "employees": employees,
        "lat": lat,
        "lon": lon,
        "address": address
    }
    return dict_

def rentsCsv(urls):
    dict_rents = getDict(urls)
    rents = pd.DataFrame(dict_rents)
    rents.sort_values(by = "employees", ascending = True, inplace=True)
    rents["positions"] = rents.apply(lambda row: [row["lon"], row["lat"]], axis=1)
    rents.to_csv("data/officesSF.csv", index=False)


