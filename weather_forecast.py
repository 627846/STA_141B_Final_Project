import requests
import pandas as pd
import time
import json
import lxml.html as lx

headers = {
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:144.0) Gecko/20100101 Firefox/144.0"
}

def weather_forecast(latitude,longitude):
    today = date.today()
    result = requests.get(url = f"https://api.weather.gov/points/{latitude},{longitude}", headers = headers)
    resultJson = result.json()
    urlNew = resultJson.get("properties").get("forecastHourly")
    result2 = requests.get(url = urlNew, headers = headers)
    resultJson2 = result2.json()
    excess = str(today.year) + "-"
    forcastDate = [resultJson2.get("properties").get("periods")[i].get("startTime") for i in range(len(resultJson2.get("properties").get("periods")))]
    forcastDate = [forcastDate[i].replace(excess, "") for i in range(len(forcastDate))]
    forcastDate = [forcastDate[i].replace(":00:00-08:00", "") for i in range(len(forcastDate))]
    temp = [resultJson2.get("properties").get("periods")[i].get("temperature") for i in range(len(resultJson2.get("properties").get("periods")))]
    tempForecast = {forcastDate[i]: temp[i] for i in range(len(forcastDate))}
    coldest = min(tempForecast.values())
    hottest = max(tempForecast.values())
    if coldest <=32 and hottest >= 90:
        return print("Hiking is ill advised in this weather")
    elif [key for key, value in tempForecast.items() if 55 <= value <= 70]:
        return DateDecoder([key for key, value in tempForecast.items() if 55 <= value <= 70],
                           [value for key, value in tempForecast.items() if 55 <= value <= 70])
    elif hottest <= 70:
        return DateDecoder([key for key, value in tempForecast.items() if(value == hottest)], 
                           [value for key, value in tempForecast.items() if(value == hottest)])
    elif coldest >= 55:
        return DateDecoder([key for key, value in tempForecast.items() if(value == coldest)], 
                           [value for key, value in tempForecast.items() if(value == coldest)])

def DateDecoder(dates, temperature):
    forecastMonthDay = [dates[i].split("T")[0] for i in range(len(dates))]
    forecastTime = [dates[i].split("T")[1]+ ":00" for i in range(len(dates))]
    forecastMonth = [forecastMonthDay[i].split("-")[0] for i in range(len(forecastMonthDay))]
    forecastDay = [forecastMonthDay[i].split("-")[1] for i in range(len(forecastMonthDay))]
   
    dct = {"Month": forecastMonth, "Day": forecastDay, "Time": forecastTime, "Temperature": temperature}
    df = pd.DataFrame(dct)
    return df.head(10)
weather_forecast(get_distance_to_hike(get_best_hike(df))[1][0],get_distance_to_hike(get_best_hike(df))[1][1])
