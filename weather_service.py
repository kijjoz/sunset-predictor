import os
import requests
from datetime import datetime, timedelta
from sunset_calc import get_sunset_time

API_KEY = os.getenv("OPENWEATHER_API_KEY")

def get_weather(lat=48.72, lon=21.26, target_date=None):
    """
    Získa predpoveď počasia pre dané súradnice.
    Vyberie čas najbližší k západu slnka.
    """
    if not API_KEY:
        print("CHYBA: OPENWEATHER_API_KEY nie je nastavený.")
        return None

    try:
        url = f"https://api.openweathermap.org/data/2.5/forecast"
        params = {
            "lat": lat,
            "lon": lon,
            "appid": API_KEY,
            "units": "metric",
            "lang": "sk"
        }

        print(f"Volám OpenWeather Forecast API pre {lat}, {lon}")
        res = requests.get(url, params=params, timeout=10)
        data = res.json()
        print("Odpoveď API:", data.get("cod"), data.get("message", ""))

        if data.get("cod") != "200" or "list" not in data:
            print("Chyba pri čítaní dát:", data)
            return None

        # Ak cieľový dátum nie je zadaný → dnešok
        if target_date is None:
            target_date = datetime.now()

        # Získaj čas západu slnka pre dané súradnice
        sunset = get_sunset_time(lat, lon, target_date)
        sunset_timestamp = sunset.timestamp()

        # Nájdeme čas v predpovedi najbližší k západu
        closest = min(data["list"], key=lambda x: abs(x["dt"] - sunset_timestamp))

        main = closest["main"]
        weather = closest["weather"][0]
        clouds = closest["clouds"]["all"]
        humidity = main["humidity"]
        description = weather["description"]

        print(f"Vybraná predpoveď: {closest['dt_txt']} ({description}, {clouds}% oblačnosť)")

        return {
            "temperature": main["temp"],
            "humidity": humidity,
            "clouds": clouds,
            "description": description,
            "lat": lat,
            "lon": lon,
            "city": data["city"]["name"]
        }

    except Exception as e:
        print("Chyba pri načítaní počasia:", e)
        return None
