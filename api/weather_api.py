from typing import Optional
from fastapi import Depends
import fastapi

from models.location import Location
from services import openweather_service

router = fastapi.APIRouter()


@router.get("/api/weather/{city}")
async def weather(loc: Location = Depends(),
                  units: Optional[str] = "metric",):
    report = await openweather_service.get_report(loc.city, loc.state, loc.country, units)
    return report
