from threading import Thread
import uvicorn
from pyngrok import ngrok
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from router import mainRouter as mainRouter

from config import Configs as cf

import nest_asyncio
nest_asyncio.apply()

app = FastAPI()

app.mount(
    "/api/videos",
    StaticFiles(directory=cf.OUTPUT),
    name="videos"
)

app.include_router(mainRouter.router)

def run():
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        loop="asyncio"
    )

thread = Thread(
    target=run,
    daemon=False
)
thread.start()