from uuid import UUID

from fastapi import Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates

from services.videoService import VideoService
from config import Configs as cf

templates = Jinja2Templates(directory=str(cf.TEMPLATES))

async def get_statusAPI(request: Request, id: UUID, service: VideoService):
    video = await service.getStatus(id)
    if video is None:
        return JSONResponse(
            None,
            404
        )

    if video.errorMessage != "":
        return JSONResponse(
            jsonable_encoder(video),
            500
        )

    return JSONResponse(
        jsonable_encoder(video),
        200
    )

async def get_status(request: Request, id: UUID):
    return templates.TemplateResponse(
        request,
        "pending.html",
        {
            "videoName": id
        }
    )