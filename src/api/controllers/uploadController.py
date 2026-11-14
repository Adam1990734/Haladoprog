from pathlib import Path

from fastapi import File, UploadFile, Request
from fastapi.templating import Jinja2Templates

UPLOAD_DIR = Path("input")
UPLOAD_DIR.mkdir(exist_ok=True)

templates = Jinja2Templates(directory="public/templates")

async def get_upload(request: Request):
    return templates.TemplateResponse(
        request,
        "create.html"
    )

async def post_upload(
    request: Request,
    video: UploadFile = File(...)
):
    allowed_extensions = { ".mp4", ".avi" }

    extension = Path(video.filename).suffix.lower()

    if extension not in allowed_extensions:
        return templates.TemplateResponse(
            request,
            "result.html",
            {
                "error": "Not supported format (mp4, avi).",
                "filename": ""
            }
        )

    # service ide kéne majd

    

    return templates.TemplateResponse(
        request,
        "result.html",
        {
            "error": "",
            "filename": video.filename
        }
    )