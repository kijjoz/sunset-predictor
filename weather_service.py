import requests
import os

API_KEY = os.getenv("OPENWEATHER_API_KEY")
CITY = "Kosice"
URL = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric&lang=sk"

def get_weather():
    if not API_KEY:
        print("Chýba OPENWEATHER_API_KEY – nastav ho v prostredí.")
        return None
    try:
        response = requests.get(URL, timeout=5)
        data = response.json()

        if "cod" in data and data["cod"] != 200:
            print("OpenWeather API error:", data.get("message", ""))
            return None

        clouds = data.get("clouds", {}).get("all", 0)
        visibility = data.get("visibility", 10000)
        humidity = data.get("main", {}).get("humidity", 50)
        weather_main = data.get("weather", [{}])[0].get("main", "Clear")
        weather_desc = data.get("weather", [{}])[0].get("description", "")

        return {
            "clouds": clouds,
            "visibility": visibility,
            "humidity": humidity,
            "weather": weather_main,
            "description": weather_desc
        }

    except Exception as e:
        print("Chyba pri načítaní počasia:", e)
        return None
