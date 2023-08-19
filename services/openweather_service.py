from typing import Optional, Tuple
from dotenv import load_dotenv
import os
import httpx
from constants.abbreviations import COUNTRY_CODES, US_STATES_CODES
from constants.units import VALID_OPEN_WEATHER_API_UNITS

from models.validation_error import ValidationError
from infrastructure import weather_cache

load_dotenv()

OPENWEATHERMAP_API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")

if not OPENWEATHERMAP_API_KEY:
    raise Exception("NO VALID API KEY")


async def get_report(city: str, state: Optional[str], country: str, units: str) -> dict:
    if forecast := weather_cache.get_weather(city, state, country, units):
        return forecast

    if state:
        q = f"{city},{state},{country}"
    else:
        q = f"{city},{country}"

    api_url = "https://api.openweathermap.org/data/2.5/weather"
    full_url = f"{api_url}?q={q}&appid={OPENWEATHERMAP_API_KEY}&units={units}"

    async with httpx.AsyncClient() as client:
        response = await client.get(full_url)
        if response.status_code != 200:
            raise ValidationError(response.text, response.status_code)

    data = response.json()
    forecast = data["main"]

    weather_cache.set_weather(city, state, country, units, forecast)
    return forecast


def validate_units(
    city: str, state: Optional[str], country: Optional[str], units: str
) -> Tuple[str, Optional[str], str, str]:
    city = city.strip().lower()

    if not country:
        country = "US"
    else:
        country = country.strip().upper()

    if country not in COUNTRY_CODES:
        error = f"Invalid country: {country}. It must be a two letter abbreviation such as US or GB."
        raise ValidationError(error_msg=error, status_code=400)

    if state:
        state = state.strip().upper()

    if state and state not in US_STATES_CODES:
        error = f"Invalid state: {state}. It must be a two letter abbreviation such as CA or TX."
        raise ValidationError(error_msg=error, status_code=400)

    if units:
        units = units.lower().strip()

    if units not in VALID_OPEN_WEATHER_API_UNITS:
        error = (
            f"Invalid units: {units}. It must be one of {VALID_OPEN_WEATHER_API_UNITS}"
        )
        raise ValidationError(error_msg=error, status_code=400)

    return city, state, country, units
