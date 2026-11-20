from fastapi import Request
from fastapi.templating import Jinja2Templates
from uuid import UUID
from config import Configs as cf

templates = Jinja2Templates(directory=str(cf.TEMPLATES))

async def get_result(request: Request, id: UUID):
    return templates.TemplateResponse(
        request,
        "result.html",
        {
            "url": "/api/videos/" + str(id) + "_censored.mp4"
        }
    )