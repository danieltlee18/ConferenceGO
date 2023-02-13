import requests
from .keys import PEXEL_KEY, WEATHER_KEY
import json


def get_location_photo(city, state):
    headers = {"Authorization": PEXEL_KEY}

    url = f"https://api.pexels.com/v1/search?query={city}+{state}"
    resp = requests.get(url, headers=headers)
    return resp.json()["photos"][0]["url"]


def get_weather_data(city, state):
    if city == "Altlanta":
        city = "Atlanta"
    params = {
        "q": f"{city},{state},US",
        "appid": WEATHER_KEY}
    url = "http://api.openweathermap.org/geo/1.0/direct"
    response = requests.get(url, params=params)
    content = json.loads(response.content)
    try:
        latitude = content[0]["lat"]
        longitude = content[0]["lon"]
    except (KeyError, IndexError):
        return None

    params = {
        "lat": latitude,
        "lon": longitude,
        "units": "imperial",
        "appid": WEATHER_KEY,
    }

    url = "https://api.openweathermap.org/data/2.5/weather"
    response = requests.get(url, params=params)
    content = json.loads(response.content)
    try:
        temp = content["main"]["temp"]
        description = content["weather"][0]["description"]
        return {"temp": temp, "description": description}
    except (KeyError, IndexError):
        return None

