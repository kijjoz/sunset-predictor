import requests, os

API_KEY = os.getenv("OPENWEATHER_API_KEY")

def get_weather(lat=None, lon=None, city=None):
    if not API_KEY:
        print("Chýba OPENWEATHER_API_KEY")
        return None

    if lat and lon:
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric&lang=sk"
    elif city:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=sk"
    else:
        return None

    try:
        response = requests.get(url, timeout=5)
        data = response.json()

        if "cod" in data and data["cod"] != 200:
            print("OpenWeather API error:", data.get("message", ""))
            return None

        return {
            "clouds": data.get("clouds", {}).get("all", 0),
            "visibility": data.get("visibility", 10000),
            "humidity": data.get("main", {}).get("humidity", 50),
            "weather": data.get("weather", [{}])[0].get("main", "Clear"),
            "description": data.get("weather", [{}])[0].get("description", "")
        }
    except Exception as e:
        print("Chyba pri načítaní počasia:", e)
        return None
