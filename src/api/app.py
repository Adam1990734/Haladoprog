from fastapi import FastAPI
from router import main as mainRouter

app = FastAPI()

# Router regisztrációk:
app.include_router(mainRouter.router)