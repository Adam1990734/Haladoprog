from fastapi import Request
from fastapi.templating import Jinja2Templates

from models.videoRequestDto import VideoRequestDto
from services.videoService import VideoService

templates = Jinja2Templates(directory="public/templates")

async def get_upload(request: Request):
    return templates.TemplateResponse(
        request,
        "create.html"
    )

async def post_upload(
    request: Request,
    dto: VideoRequestDto,
    service: VideoService
):
    newVideo = await service.upload(dto)

    return templates.TemplateResponse(
        request,
        "pending.html",
        {
            "videoName": newVideo.getId()
        }
    )