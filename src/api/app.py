from fastapi import FastAPI
from router import main as mainRouter

app = FastAPI()

app.mount(
    "/videos",
    StaticFiles(directory="output"),
    name="videos"
)

# Router regisztrációk:
app.include_router(mainRouter.router)