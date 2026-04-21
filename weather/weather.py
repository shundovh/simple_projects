import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


def fetch_weather(city):
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        raise EnvironmentError("OPENWEATHER_API_KEY not set in .env file.")

    response = requests.get(BASE_URL, params={
        "q": city,
        "appid": api_key,
        "units": "metric",
        "lang": "pt_br",
    })

    if response.status_code == 404:
        raise ValueError(f"City '{city}' not found.")
    if response.status_code == 401:
        raise EnvironmentError("Invalid API key.")
    response.raise_for_status()

    return response.json()


def parse_weather(data):
    return {
        "city": data["name"],
        "country": data["sys"]["country"],
        "temp": round(data["main"]["temp"]),
        "feels_like": round(data["main"]["feels_like"]),
        "description": data["weather"][0]["description"].capitalize(),
        "humidity": data["main"]["humidity"],
        "wind_speed": round(data["wind"]["speed"] * 3.6),  # m/s → km/h
    }


def display_weather(weather):
    print(f"\nClima em {weather['city']}, {weather['country']}")
    print(f"  Temperatura : {weather['temp']}°C (sensacao: {weather['feels_like']}°C)")
    print(f"  Condicao    : {weather['description']}")
    print(f"  Umidade     : {weather['humidity']}%")
    print(f"  Vento       : {weather['wind_speed']} km/h")
