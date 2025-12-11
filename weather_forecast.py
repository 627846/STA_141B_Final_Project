import requests
import pandas as pd
import time
import json
import lxml.html as lx

headers = {
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:144.0) Gecko/20100101 Firefox/144.0"
}

def weather_forecast(latitude,longitude):
    result = requests.get(url = f"https://api.weather.gov/points/{latitude},{longitude}", headers = headers)
    resultJson = result.json()
    urlNew = resultJson.get("properties").get("forecastHourly")
    result2 = requests.get(url = urlNew, headers = headers)
    resultJson2 = result2.json()
    time = [resultJson2.get("properties").get("periods")[i].get("startTime") for i in range(len(resultJson2.get("properties").get("periods")))]
    temp = [resultJson2.get("properties").get("periods")[i].get("temperature") for i in range(len(resultJson2.get("properties").get("periods")))]
    tempForecast = {time[i]: temp[i] for i in range(len(time))}
    return tempForecast
