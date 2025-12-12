import requests
import pandas as pd
import time
import json
import lxml.html as lx
from geopy import distance

def read_key(keyfile):
    with open(keyfile) as f:
        return f.readline().strip("\n")
key = read_key("API_Key_google.txt")

url = "https://places.googleapis.com/v1/places:searchText"

def get_hike_info():
    lst = []
    nextPage = None
    while True:
        result = requests.post(
            url=url,
            headers={
                "Content-Type": "application/json",
                "X-Goog-Api-Key": key,
                "X-Goog-FieldMask": "places.displayName,places.location,places.rating,nextPageToken"
            },
            json={
                "pageToken": nextPage,
                "textQuery": "hiking_area",
                "locationBias": {
                    "circle": {
                        "center": {
                            "latitude": 38.551683,
                            "longitude": -121.749776
                        },
                        "radius": 35000
                    }
                },
            }
        )
        resultJson = result.json()
        [lst.append(resultJson.get("places")[i]) for i in range(len(resultJson.get("places")))]
        
        if resultJson.get("nextPageToken"):
            nextPage = resultJson.get("nextPageToken")
        else: 
            return lst
        time.sleep(3)
df = get_hike_info()

def get_best_hike(df):
    rating = [df[i].get("rating") for i in range(len(df))]
    maxRating = max(rating)
    [df[i].get("rating") for i in range(len(df))]
    best = [df[i].get("displayName").get("text") for i in range(len(df)) if maxRating == df[i].get("rating")]
    return get_closest_hike(best)

def get_closest_hike(location):
    centralDavis = (38.551683, -121.749776)
    latitude = [df[i].get("location").get("latitude") 
                    for i in range(len(df)) for k in range(len(location)) if df[i].get("displayName").get("text") == location[k]]
    longitude = [df[i].get("location").get("longitude") 
                    for i in range(len(df)) for k in range(len(location)) if df[i].get("displayName").get("text") == location[k]]
    loc = [[latitude[i], longitude[i]] for i in range(len(latitude))]
    dist = [distance.distance(loc[i], centralDavis).km for i in range(len(loc))]
    closest = dist.index(min(dist))
    temp = loc[closest]
    result = [df[i].get("displayName").get("text")
                    for i in range(len(df)) if df[i].get("location").get("latitude") == temp[0] and df[i].get("location").get("longitude") == temp[1]]
    return result
get_hike_info()
get_best_hike(df)
