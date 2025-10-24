import os
import requests
from datetime import datetime
from sunset_calc import get_sunset_time

API_KEY = os.getenv("OPENWEATHER_API_KEY")

def get_weather(lat=48.72, lon=21.26, target_date=None):
    if not API_KEY:
        print("CHYBA: OPENWEATHER_API_KEY nie je nastavený.")
        return None

    try:
        # Skús forecast ako primárny zdroj
        url_forecast = "https://api.openweathermap.org/data/2.5/forecast"
        params = {
            "lat": lat,
            "lon": lon,
            "appid": API_KEY,
            "units": "metric",
            "lang": "sk"
        }

        print(f"Volám Forecast API pre {lat}, {lon}")
        res = requests.get(url_forecast, params=params, timeout=10)
        data = res.json()

        # Ak forecast zlyhá, fallback na current weather
        if data.get("cod") != "200" or "list" not in data:
            print("Forecast zlyhal, skúšam current weather...")
            url_weather = "https://api.openweathermap.org/data/2.5/weather"
            res = requests.get(url_weather, params=params, timeout=10)
            data = res.json()
            if data.get("cod") != 200:
                print("Ani current weather nevyšiel:", data)
                return None

            weather = data["weather"][0]
            main = data["main"]
            clouds = data["clouds"]["all"]
            visibility = data.get("visibility", 10000)  # <── pridané

            return {
                "temperature": main["temp"],
                "humidity": main["humidity"],
                "clouds": clouds,
                "description": weather["description"],
                "visibility": visibility,   # <── pridané
                "city": data.get("name", "Neznáme miesto"),
                "lat": lat,
                "lon": lon
            }

        # Forecast funguje – vyber najbližší čas k západu
        sunset = get_sunset_time(lat, lon)
        sunset_timestamp = sunset.timestamp()
        closest = min(data["list"], key=lambda x: abs(x["dt"] - sunset_timestamp))

        main = closest["main"]
        weather = closest["weather"][0]
        clouds = closest["clouds"]["all"]
        visibility = closest.get("visibility", 10000)  # <── pridané

        return {
            "temperature": main["temp"],
            "humidity": main["humidity"],
            "clouds": clouds,
            "description": weather["description"],
            "visibility": visibility,  # <── pridané
            "city": data["city"]["name"],
            "lat": lat,
            "lon": lon
        }

    except Exception as e:
        print("Chyba pri načítaní počasia:", e)
        return None
