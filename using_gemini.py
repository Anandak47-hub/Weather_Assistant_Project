import requests
import json


def get_weather(city:str)->str:
    url = "https://geocoding-api.open-meteo.com/v1/search"
    #city = input("Enter The city name:")
    params = {
        "name":city,
        "count":1
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    if data.get('results'):
        latitude= data['results'][0]['latitude']
        longitude= data['results'][0]['longitude']

        url2 = "https://api.open-meteo.com/v1/forecast"
        params2 = {
            "latitude":latitude,
            "longitude":longitude,
            "current": "temperature_2m,relative_humidity_2m"
        }
        response2 = requests.get(url2, params=params2)
        response2.raise_for_status()
        info = response2.json()

        temp = info['current']['temperature_2m']
        hump = info['current']['relative_humidity_2m']
        units = info['current_units']

        print(response2)
        print(f"Temperature: {temp}{units['temperature_2m']}, Humidity: {hump}{units['relative_humidity_2m']}")

        return f"City: {city}\nTemperature: {temp}{units['temperature_2m']}\nHumidity: {hump}{units['relative_humidity_2m']}"
    else:
        return f"There is no such city named {city}"

from google.genai import Client, types
client = Client()

chat= client.chats.create(
    model= "gemini-3.5-flash-lite",
    config = types.GenerateContentConfig(tools=[get_weather])
)

gemini_response = chat.send_message("What's the weather like in Kolkata")
print(gemini_response.text)
gemini_response = chat.send_message("What's the weather like in Boombaboom")
print(gemini_response.text)