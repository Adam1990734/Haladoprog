from pathlib import Path
from uuid import UUID

from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates

from services.videoService import VideoService

templates = Jinja2Templates(directory="public/templates")

async def get_statusAPI(request: Request, id: UUID, service: VideoService):
    video = await service.getStatus(id)

    if video is None:
        return JSONResponse(
            None,
            404
        )

    if video.errorMessage != "":
        return JSONResponse(
            video,
            500
        )

    return JSONResponse(
        video,
        200
    )

async def get_status(request: Request, id: UUID):
    return templates.TemplateResponse(
        request,
        "pending.html",
        {
            "video_id": id
        }
    )