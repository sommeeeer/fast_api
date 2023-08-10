import fastapi
from typing import Optional

router = fastapi.APIRouter()


@router.get("/api/weather")
def weather(state: Optional[str], country: str, units: str):
    return "some weather"
