from datetime import datetime
from astral import LocationInfo
from astral.sun import sun

def get_sunset_time(lat=48.72, lon=21.26, date=None):
    if date is None:
        date = datetime.now()

    location = LocationInfo(latitude=lat, longitude=lon)
    s = sun(location.observer, date=date)
    return s["sunset"]
