import fastapi
import uvicorn

from starlette.staticfiles import StaticFiles

from views import home

api = fastapi.FastAPI()
api.mount("/static", StaticFiles(directory="static"), name="static")
api.include_router(home.router)


if __name__ == "__main__":
    uvicorn.run(api, port=8000, host="127.0.0.1")
