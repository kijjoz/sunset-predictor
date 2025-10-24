from datetime import datetime
from astral import LocationInfo
from astral.sun import sun
import pytz

def get_sunset_time(lat=48.72, lon=21.26, date=None):
    if date is None:
        date = datetime.now()

    # Nastavíme časové pásmo pre Slovensko
    tz = pytz.timezone("Europe/Bratislava")

    location = LocationInfo(latitude=lat, longitude=lon)
    s = sun(location.observer, date=date, tzinfo=tz)

    # Výsledok je už preložený do slovenského času
    return s["sunset"]
