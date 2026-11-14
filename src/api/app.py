from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from router import mainRouter as mainRouter

app = FastAPI()

app.mount(
    "/api/videos",
    StaticFiles(directory="C:\\Users\\palma\\GitHubProjects\\Haladoprog\\src\\output"),
    name="videos"
)

# Router regisztrációk:
app.include_router(mainRouter.router)