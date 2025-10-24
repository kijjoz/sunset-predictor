from astral import LocationInfo
from astral.sun import sun
from datetime import datetime

def get_sunset_time(city_name):
    city = LocationInfo(
        name=city_name,
        region="Slovakia",
        timezone="Europe/Bratislava",
        latitude=48.7164,
        longitude=21.2611
    )
    s = sun(city.observer, date=datetime.now(), tzinfo=city.timezone)
    return s["sunset"]
