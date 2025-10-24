from datetime import datetime, timedelta
from astral import LocationInfo
from astral.sun import sun

def get_sunset_time(city="Kosice", date=None):
    """Vypočíta čas západu slnka pre dané mesto a deň."""

    # Ak dátum nebol zadaný, použijeme dnešný
    if date is None:
        date = datetime.now()

    # Nastavenie súradníc podľa mesta (môžeš rozšíriť podľa potreby)
    cities = {
        "Kosice": (48.7164, 21.2611),
        "Bratislava": (48.1486, 17.1077),
        "Presov": (49.002, 21.241),
        "Zilina": (49.223, 18.739),
        "Poprad": (49.059, 20.297)
    }

    lat, lon = cities.get(city, (48.7164, 21.2611))  # default Košice

    location = LocationInfo(city, "Slovakia", "Europe/Bratislava", lat, lon)
    s = sun(location.observer, date=date, tzinfo=location.timezone)
    return s["sunset"]
