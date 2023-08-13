from typing import Optional
from fastapi import Depends
import fastapi

from models.location import Location

router = fastapi.APIRouter()


@router.get("/api/weather/{city}")
def weather(
    loc: Location = Depends(),
    units: Optional[str] = "metric",
):
    return f"{loc.city} {loc.state} {loc.country} in {units}"
