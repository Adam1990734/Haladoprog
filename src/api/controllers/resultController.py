from fastapi import Request
from fastapi.templating import Jinja2Templates
from uuid import UUID

templates = Jinja2Templates(directory="public/templates")

async def get_result(request: Request, id: UUID):
    return templates.TemplateResponse(
        request,
        "result.html",
        {
            "url": "/api/videos/" + str(id) + "_censored.mp4"
        }
    )