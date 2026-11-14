from pathlib import Path
from uuid import UUID

from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates

UPLOAD_DIR = Path("input")
UPLOAD_DIR.mkdir(exist_ok=True)

templates = Jinja2Templates(directory="public/templates")

async def get_statusAPI(request: Request, id: UUID):
    #service ide kéne
    video = None

    if video is None:
        return JSONResponse(
            None,
            404
        )

    return JSONResponse(
        video,
        200
    )

async def get_status(request: Request):
    return templates.TemplateResponse(
        request,
        "pending.html"
    )