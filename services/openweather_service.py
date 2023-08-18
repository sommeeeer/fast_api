from typing import Optional
from dotenv import load_dotenv
import os
import httpx

from models.validation_error import ValidationError

load_dotenv()

OPENWEATHERMAP_API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")

if not OPENWEATHERMAP_API_KEY:
    raise Exception("NO VALID API KEY")

async def get_report(city: str, state: Optional[str], country: str, units: str) -> dict:
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
    return forecast

