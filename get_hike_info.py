import requests
import pandas as pd
import time
import json
import lxml.html as lx

def read_key(keyfile):
    with open(keyfile) as f:
        return f.readline().strip("\n")
key = read_key("API_Key_google.txt")

url = "https://places.googleapis.com/v1/places:searchText"

def get_hike_info():
    result = requests.post(
        url=url,
        headers={
            "Content-Type": "application/json",
            "X-Goog-Api-Key": key,
            "X-Goog-FieldMask": "places.displayName,places.formattedAddress,places.rating,nextPageToken"
        },
        json={                                    
            "textQuery": "hiking_area",
            "locationBias": {
                "circle": {
                    "center": {
                        "latitude": 38.551683,
                        "longitude": -121.749776
                    },
                    "radius": 25000
                }
            },
        }
    )
    resultJson = result.json()
    nextPage = resultJson.get("nextPageToken")
    lst = [resultJson.get("places")[i].get("displayName") for i in range(len(resultJson.get("places")))]
    if nextPage:
        result2 = requests.post(
            url=url,
            headers={
                "Content-Type": "application/json",
                "pageToken": nextPage,
                "X-Goog-Api-Key": key,
                "X-Goog-FieldMask": "places.displayName,places.formattedAddress,places.rating,nextPageToken"
            },
            json={                                    
                "textQuery": "hiking_area",
                "locationBias": {
                    "circle": {
                        "center": {
                            "latitude": 38.551683,
                            "longitude": -121.749776
                        },
                        "radius": 25000
                    }
                },
            }
        )
        lst.append(str(len(lst)) + " total results")
        resultJson2 = result2.json()
        return print(pd.DataFrame([resultJson2.get("places")[i].get("displayName") for i in range(len(resultJson2.get("places")))])), "one"
    else:
        return print(pd.DataFrame([resultJson.get("places")[i].get("displayName") for i in range(len(resultJson.get("places")))])), "two"

get_hike_info()
