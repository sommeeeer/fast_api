from datetime import datetime
from typing import Optional, Tuple


__cache = {("city", "state", "country", "units"): {"value": {}, "time": datetime.now()}}
lifetime_in_hours = 1.0


# get weather
def get_weather(
    city: str, state: Optional[str], country: str, units: str
) -> Optional[dict]:
    key = _create_key(city, state, country, units)
    data = __cache.get(key)

    if not data:
        return None

    last_seen = data["time"]
    dt = datetime.now() - last_seen
    if dt / datetime.timedelta(minutes=60) < lifetime_in_hours:
        return data["value"]

    del __cache[key]
    return None


# set weather
def set_weather(city: str, state: str, country: str, units: str, value: dict):
    key = _create_key(city, state, country, units)
    data = {"time": datetime.now(), "value": value}
    __cache[key] = data
    _clean_cache()


# create key
def _create_key(
    city: str, state: str, country: str, units: str
) -> Tuple[str, str, str, str]:
    if not city or not country or not units:
        raise Exception("City, country and units are required")

    if not state:
        state = ""

    return (
        city.strip().lower(),
        state.strip().lower(),
        country.strip().lower(),
        units.strip().lower(),
    )


# clean data cache
def _clean_cache():
    for key, data in list(__cache.items()):
        last_seen = data.get("time")
        dt = datetime.now() - last_seen
        if dt / datetime.timedelta(minutes=60) > lifetime_in_hours:
            del __cache[key]
