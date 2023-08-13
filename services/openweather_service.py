from typing import Optional
from dotenv import load_dotenv
import os
import httpx

load_dotenv()

OPENWEATHERMAP_API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")

if not OPENWEATHERMAP_API_KEY:
    raise Exception("NO VALID API KEY")


def get_report(city: str, state: Optional[str], country: str, units: str) -> dict:
    if state:
        q = f"{city},{state},{country}"
    else:
        q = f"{city},{country}"

    api_url = "https://api.openweathermap.org/data/2.5/weather"
    full_url = f"{api_url}?q={q}&appid={OPENWEATHERMAP_API_KEY}&units={units}"

    response = httpx.get(full_url)
    response.raise_for_status()

    data = response.json()
    forecast = data["main"]
    return forecast
