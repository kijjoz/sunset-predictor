import requests
import os
from datetime import datetime, timedelta

API_KEY = os.getenv("OPENWEATHER_API_KEY")

def get_weather(lat=None, lon=None, city=None, sunset_time=None):
    """
    Získa predpoveď počasia pre dané GPS súradnice v čase západu slnka.
    Ak sunset_time nie je zadaný, použije sa aktuálny čas (fallback).
    """

    if not API_KEY:
        print("Chýba OPENWEATHER_API_KEY")
        return None

    # Kontrola vstupov
    if not lat or not lon:
        print("Chýbajú súradnice pre predpoveď počasia")
        return None

    # URL pre 3-hodinovú predpoveď
    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric&lang=sk"

    try:
        response = requests.get(url, timeout=8)
        data = response.json()

        if "cod" in data and int(data["cod"]) != 200:
            print("OpenWeather API error:", data.get("message", ""))
            return None

        # Ak nepoznáme sunset_time (napr. fallback), použijeme aktuálny čas
        if sunset_time is None:
            sunset_time = datetime.utcnow()

        # Najdi predpoveď, ktorá je najbližšie k času západu
        closest_forecast = min(
            data["list"],
            key=lambda e: abs(datetime.fromtimestamp(e["dt"]) - sunset_time)
        )

        # Vrátime relevantné dáta
        main = closest_forecast["main"]
        weather = closest_forecast["weather"][0]
        clouds = closest_forecast["clouds"]["all"]

        return {
            "clouds": clouds,
            "humidity": main["humidity"],
            "weather": weather["main"],
            "description": weather["description"],
            "forecast_time": datetime.fromtimestamp(closest_forecast["dt"]).strftime("%H:%M")
        }

    except Exception as e:
        print("Chyba pri načítaní predpovede počasia:", e)
        return None
