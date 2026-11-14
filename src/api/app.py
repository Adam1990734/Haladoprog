from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from api.router import mainRouter as mainRouter

app = FastAPI()

app.mount(
    "/videos",
    StaticFiles(directory="output"),
    name="videos"
)

# Router regisztrációk:
app.include_router(mainRouter.router)