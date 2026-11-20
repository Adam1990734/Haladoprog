from fastapi import Request
from fastapi.templating import Jinja2Templates

from models.censor_mode import CensorMode
from models.videoRequestDto import VideoRequestDto
from services.videoService import VideoService
from config import Configs as cf

templates = Jinja2Templates(directory=str(cf.TEMPLATES))

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
    await service.startCensoring(
        newVideo.getId(),
        dto.getMode()
    )

    return templates.TemplateResponse(
        request,
        "pending.html",
        {
            "videoName": newVideo.getId()
        }
    )