from typing import Optional
from fastapi import Depends
import fastapi

from models.location import Location
from models.validation_error import ValidationError
from services import openweather_service
from services.openweather_service import validate_units

router = fastapi.APIRouter()


@router.get("/api/weather/{city}")
async def weather(
    loc: Location = Depends(),
    units: Optional[str] = "metric",
):
    try:
        city, state, country, units = validate_units(
            loc.city, loc.state, loc.country, units
        )
        report = await openweather_service.get_report(city, state, country, units)
    except ValidationError as ve:
        return fastapi.Response(content=ve.error_msg, status_code=ve.status_code)
    except Exception as e:
        print(f"Server crashed while processing your request: {e}")
        return fastapi.Response(
            content="Error processing your request", status_code=500
        )

    return report
