from threading import Thread
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from router import mainRouter as mainRouter

from pyngrok import ngrok
ngrok.set_auth_token("3LxKRtH6JT9FSi0dGMJouQpBwUb_39TJoZkDivZ6VYZgMRLCN")

from config import Configs as cf

app = FastAPI()

app.mount(
    "/api/videos",
    StaticFiles(directory=cf.OUTPUT),
    name="videos"
)

app.include_router(mainRouter.router)

public_url = ngrok.connect(8000)
print("NGROK URL:", public_url)

thread = Thread(
    target=lambda: uvicorn.run(app, host="0.0.0.0", port=8000)
)
thread.start()