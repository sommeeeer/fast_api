import fastapi
import uvicorn

from starlette.staticfiles import StaticFiles

from views import home
from api import weather_api


api = fastapi.FastAPI()
api.mount("/static", StaticFiles(directory="static"), name="static")
api.include_router(home.router)
api.include_router(weather_api.router)


if __name__ == "__main__":
    uvicorn.run(api, port=8000, host="127.0.0.1")
